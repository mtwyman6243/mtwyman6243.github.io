"""
build_project_map_template.py
------------------------------
Template pattern for adding a NEW project map (e.g. Wildfire Risk MCDA,
Retention Basin Site Selection) once the underlying GIS outputs are on hand.

Covers the three data types mentioned:
  - Vector  -> GeoPandas  (site boundaries, candidate polygons, points)
  - Raster  -> Xarray/rioxarray (hazard/exposure/suitability surfaces)
  - Database -> PostGIS (optional — only needed for live/dynamic querying;
                          skip this and just read files if the map is static)

Run with the geospatial stack installed:
    pip install leafmap geopandas rioxarray xarray rasterio
    # optional, only if using a live database:
    pip install sqlalchemy psycopg2-binary geoalchemy2
"""

import geopandas as gpd
import leafmap.foliumap as leafmap
import rioxarray  # noqa: F401  (registers the .rio accessor on xarray objects)
import xarray as xr

# ---------------------------------------------------------------------------
# 1. VECTOR DATA (GeoPandas) — e.g. candidate retention basin polygons,
#    populated place boundaries, tribal reservation boundaries
# ---------------------------------------------------------------------------
def load_vector_layer(path):
    gdf = gpd.read_file(path)
    # Leaflet/leafmap expects WGS84 (EPSG:4326)
    if gdf.crs and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    return gdf


# ---------------------------------------------------------------------------
# 2. RASTER DATA (Xarray / rioxarray) — e.g. Flood Mitigation Suitability
#    surface, composite Wildfire Risk index
# ---------------------------------------------------------------------------
def load_raster_layer(path):
    da = xr.open_dataarray(path)  # or rioxarray.open_rasterio(path) for multi-band
    if da.rio.crs and da.rio.crs.to_epsg() != 4326:
        da = da.rio.reproject("EPSG:4326")
    # For web display, export as a Cloud-Optimized GeoTIFF (COG) — leafmap
    # can render COGs client-side via a tile endpoint, or locally via
    # localtileserver during development.
    cog_path = path.replace(".tif", "_cog.tif")
    da.rio.to_raster(cog_path, driver="COG")
    return cog_path


# ---------------------------------------------------------------------------
# 3. (OPTIONAL) LIVE DATABASE — PostGIS, only if you want dynamic querying
#    rather than a static baked-in map. Requires a running Postgres/PostGIS
#    instance and a backend (e.g. FastAPI + pg_featureserv) — not compatible
#    with a purely static GitHub Pages deployment.
# ---------------------------------------------------------------------------
def load_from_postgis(table_name, connection_string):
    from sqlalchemy import create_engine
    engine = create_engine(connection_string)
    gdf = gpd.read_postgis(f"SELECT * FROM {table_name}", engine, geom_col="geom")
    return gdf


# ---------------------------------------------------------------------------
# Build the map
# ---------------------------------------------------------------------------
def build_map(vector_path=None, raster_path=None, center=(32.8, -116.9), zoom=10):
    m = leafmap.Map(center=center, zoom=zoom)
    m.add_basemap("Esri.WorldImagery")

    if raster_path:
        cog_path = load_raster_layer(raster_path)
        m.add_raster(cog_path, colormap="RdYlGn_r", layer_name="Suitability / Risk Surface")

    if vector_path:
        gdf = load_vector_layer(vector_path)
        m.add_gdf(gdf, layer_name="Candidate Sites")

    return m


if __name__ == "__main__":
    # Example — swap in real paths once the project's GIS outputs are exported
    m = build_map(
        vector_path="../data/candidate_sites.geojson",
        raster_path="../data/suitability_surface.tif",
    )
    m.to_html("../maps/new_project_map.html")

# mtwyman6243.github.io

Source for **Matt Twyman's geospatial portfolio**, live at **https://mtwyman6243.github.io**. Matt is a GIS Analyst in San Diego, CA, whose research applies multi-criteria decision analysis to environmental hazards.

It's a static, multi-page site (Home, Experience, Research, Publications, Contact) in plain HTML, CSS and JS. The Research page embeds one interactive Leaflet webmap per project.

## Project repositories

Each research project has its own repo with the data-prep code, the processed data and the webmap:

| Project | Repository |
|---|---|
| Wildfire Risk MCDA — San Diego County (M.S. thesis, NASA EEJ) | [wildfire-risk-mcda](https://github.com/mtwyman6243/wildfire-risk-mcda) |
| Flood Retention Basin Site Selection — Carinthia, Austria (Marshall Plan Fellowship) | [flood-mitigation-site-screening](https://github.com/mtwyman6243/flood-mitigation-site-screening) |
| Goldspotted Oak Borer Survey — Long Potrero Preserve (Back Country Land Trust) | [gsob-long-potrero-survey](https://github.com/mtwyman6243/gsob-long-potrero-survey) |

## Layout

```
index.html, experience.html, research.html, publications.html, contact.html
css/style.css   js/script.js
maps/           # standalone webmaps embedded via <iframe>, plus raster overlays in maps/assets/
tools/build_project_map_template.py   # reusable GeoPandas/rioxarray/leafmap template for new project maps
```

To preview it locally, run `python -m http.server` in the repo root and open http://localhost:8000.

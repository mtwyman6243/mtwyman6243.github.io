document.addEventListener('DOMContentLoaded', function () {
  var toggle = document.querySelector('.navtoggle');
  var links = document.querySelector('.navlinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
    });
  }

  // mark active nav link
  var current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.navlinks a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === current) a.classList.add('active');
  });

  // project tabs (research page)
  document.querySelectorAll('.tabbar').forEach(function (bar) {
    var group = bar.getAttribute('data-tabgroup');
    var buttons = bar.querySelectorAll('.tab-btn');
    var panels = document.querySelectorAll('.tab-panel[data-tabgroup="' + group + '"]');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b) { b.classList.remove('active'); });
        panels.forEach(function (p) { p.classList.remove('active'); });
        btn.classList.add('active');
        var target = document.querySelector(
          '.tab-panel[data-tabgroup="' + group + '"][data-tab="' + btn.getAttribute('data-tab') + '"]'
        );
        if (target) target.classList.add('active');
      });
    });
  });
});

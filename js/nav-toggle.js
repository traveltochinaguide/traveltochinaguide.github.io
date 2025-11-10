// nav-toggle.js - small helper to toggle mobile nav
document.addEventListener('click', function(e){
  // toggle button
  var t = e.target.closest('[data-nav-toggle]');
  if(t){
    var target = t.getAttribute('data-nav-target') || 'primary-nav';
    var nav = document.getElementById(target);
    if(nav){
      var open = nav.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
  }
  // close when clicking outside open nav
  if(!e.target.closest('.site-header')){
    document.querySelectorAll('.site-header .nav-links.open').forEach(function(n){ n.classList.remove('open'); });
    document.querySelectorAll('[data-nav-toggle]').forEach(function(b){ b.setAttribute('aria-expanded','false'); });
  }
}, false);

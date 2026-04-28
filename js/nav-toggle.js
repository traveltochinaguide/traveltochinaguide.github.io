// nav-toggle.js - mobile nav toggle + dropdown menu support
(function () {
  'use strict';

  // ── Mobile nav toggle ──
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-nav-toggle]');
    if (t) {
      var target = t.getAttribute('data-nav-target') || 'primary-nav';
      var nav = document.getElementById(target);
      if (nav) {
        var open = nav.classList.toggle('open');
        t.setAttribute('aria-expanded', open ? 'true' : 'false');
      }
    }
    // close when clicking outside open nav
    if (!e.target.closest('.site-header')) {
      document.querySelectorAll('.site-header .nav-links.open').forEach(function (n) { n.classList.remove('open'); });
      document.querySelectorAll('[data-nav-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    }
  }, false);

  // ── Dropdown menu toggle (click for mobile, hover+click for desktop) ──
  function closeAllDropdowns(except) {
    document.querySelectorAll('.nav-dropdown.open').forEach(function (dd) {
      if (dd !== except) {
        dd.classList.remove('open');
        var btn = dd.querySelector('[aria-haspopup]');
        if (btn) btn.setAttribute('aria-expanded', 'false');
        var panel = dd.querySelector('.dropdown-panel');
        if (panel) panel.classList.add('hidden');
      }
    });
  }

  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('.nav-dropdown [aria-haspopup]');
    if (trigger) {
      var dropdown = trigger.closest('.nav-dropdown');
      var panel = dropdown.querySelector('.dropdown-panel');
      var isOpen = dropdown.classList.contains('open');

      closeAllDropdowns(dropdown);

      if (isOpen) {
        dropdown.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
        panel.classList.add('hidden');
      } else {
        dropdown.classList.add('open');
        trigger.setAttribute('aria-expanded', 'true');
        panel.classList.remove('hidden');
      }
      e.stopPropagation();
      return;
    }

    // Click outside: close all dropdowns
    if (!e.target.closest('.nav-dropdown')) {
      closeAllDropdowns(null);
    }
  });

  // Desktop hover support (non-touch)
  if (!('ontouchstart' in window)) {
    document.querySelectorAll('.nav-dropdown').forEach(function (dd) {
      dd.addEventListener('mouseenter', function () {
        var panel = dd.querySelector('.dropdown-panel');
        var btn = dd.querySelector('[aria-haspopup]');
        dd.classList.add('open');
        if (btn) btn.setAttribute('aria-expanded', 'true');
        if (panel) panel.classList.remove('hidden');
      });
      dd.addEventListener('mouseleave', function () {
        var panel = dd.querySelector('.dropdown-panel');
        var btn = dd.querySelector('[aria-haspopup]');
        dd.classList.remove('open');
        if (btn) btn.setAttribute('aria-expanded', 'false');
        if (panel) panel.classList.add('hidden');
      });
    });
  }

  // Escape key closes everything
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeAllDropdowns(null);
      document.querySelectorAll('.site-header .nav-links.open').forEach(function (n) { n.classList.remove('open'); });
      document.querySelectorAll('[data-nav-toggle]').forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
    }
  });
})();

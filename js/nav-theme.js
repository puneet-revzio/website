(function () {
  // Ensure shared nav + animations are present on all pages,
  // even if a page forgot to include the script tags.
  (function ensureSharedScripts() {
    function hasSrc(endsWith) {
      return Array.from(document.scripts || []).some((s) => (s.getAttribute('src') || '').endsWith(endsWith));
    }

    function load(src) {
      const s = document.createElement('script');
      s.src = src;
      s.defer = true;
      document.body.appendChild(s);
    }

    const prefix = /\/blog\//.test(window.location.pathname) ? '../' : '';
    if (!hasSrc('/js/nav.js') && !hasSrc('js/nav.js')) load(prefix + 'js/nav.js');
    if (!hasSrc('/js/animations.js') && !hasSrc('js/animations.js')) load(prefix + 'js/animations.js');
  })();

  const nav = document.querySelector('nav');
  if (!nav) return;

  function applyNavState() {
    /* Always solid navy bar — no transparent overlay on hero */
    nav.classList.remove('nav--on-hero');
    nav.classList.add('scrolled', 'nav--over-dark');
  }

  window.addEventListener('scroll', applyNavState, { passive: true });
  window.addEventListener('resize', applyNavState, { passive: true });
  applyNavState();
})();

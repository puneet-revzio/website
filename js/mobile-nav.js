(function () {
  const MEGA_PAGES = {
    platform: 'platform.html',
    solutions: 'solutions.html',
    resources: 'resources.html',
  };

  function init() {
    const nav = document.querySelector('nav');
    if (!nav || nav.querySelector('.nav-toggle')) return;

    const navInner = nav.querySelector('.nav-inner');
    const navLinks = nav.querySelector('.nav-links');
    if (!navInner || !navLinks) return;

    const headerCta =
      navInner.querySelector('.btn-primary') ||
      navInner.querySelector('.btn-primary-nav') ||
      navInner.querySelector('a.btn-primary');
    const navActions = navInner.querySelector('.nav-actions');

    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'nav-toggle';
    toggle.setAttribute('aria-label', 'Open menu');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.innerHTML = '<span></span><span></span><span></span>';

    const drawer = document.createElement('div');
    drawer.className = 'nav-drawer';
    drawer.id = 'nav-drawer';
    drawer.setAttribute('aria-hidden', 'true');

    const backdrop = document.createElement('button');
    backdrop.type = 'button';
    backdrop.className = 'nav-drawer-backdrop';
    backdrop.setAttribute('aria-label', 'Close menu');

    const panel = document.createElement('div');
    panel.className = 'nav-drawer-panel';
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-modal', 'true');
    panel.setAttribute('aria-label', 'Navigation');

    const root = /\/blog\//.test(window.location.pathname) ? '../' : '';
    const head = document.createElement('div');
    head.className = 'nav-drawer-head';
    head.innerHTML =
      '<a href="/" class="logo" aria-label="revzio home">' +
      '<img src="' + root + 'assets/logos/revzio-icon.png" alt="" class="logo-mark" width="367" height="367" decoding="async" aria-hidden="true">' +
      '<span class="logo-word">revzio</span>' +
      '</a>' +
      '<button type="button" class="nav-drawer-close" aria-label="Close menu">×</button>';

    const drawerLinks = document.createElement('nav');
    drawerLinks.className = 'nav-drawer-links';

    navLinks.querySelectorAll('a[href]').forEach((link) => {
      drawerLinks.appendChild(link.cloneNode(true));
    });

    navLinks.querySelectorAll('.nav-mega-trigger').forEach((btn) => {
      const id = btn.getAttribute('data-mega');
      const a = document.createElement('a');
      a.href = MEGA_PAGES[id] || '/';
      a.textContent = btn.textContent.trim();
      a.className = 'nav-drawer-link';
      drawerLinks.appendChild(a);
    });

    const drawerCta = document.createElement('div');
    drawerCta.className = 'nav-drawer-cta';

    if (navActions) {
      navActions.querySelectorAll('a').forEach((btn) => {
        drawerCta.appendChild(btn.cloneNode(true));
      });
    }

    if (headerCta) {
      drawerCta.appendChild(headerCta.cloneNode(true));
    } else {
      const fallback = document.createElement('a');
      fallback.href = 'book-a-demo.html';
      fallback.className = 'btn btn-primary';
      fallback.textContent = 'Book a demo';
      drawerCta.appendChild(fallback);
    }

    panel.appendChild(head);
    panel.appendChild(drawerLinks);
    panel.appendChild(drawerCta);
    drawer.appendChild(backdrop);
    drawer.appendChild(panel);
    nav.appendChild(drawer);

    if (headerCta) navInner.insertBefore(toggle, headerCta);
    else if (navActions) navInner.insertBefore(toggle, navActions);
    else navInner.appendChild(toggle);

    const closeBtn = panel.querySelector('.nav-drawer-close');

    function openDrawer() {
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      document.body.classList.add('nav-open');
    }

    function closeDrawer() {
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('nav-open');
    }

    toggle.addEventListener('click', () => {
      if (drawer.classList.contains('is-open')) closeDrawer();
      else openDrawer();
    });
    backdrop.addEventListener('click', closeDrawer);
    closeBtn.addEventListener('click', closeDrawer);
    drawerLinks.querySelectorAll('a').forEach((a) => a.addEventListener('click', closeDrawer));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) closeDrawer();
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 900) closeDrawer();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

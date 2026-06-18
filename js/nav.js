(function () {
  function isBlogPath() {
    return /\/blog\//.test(window.location.pathname);
  }

  function rootPrefix() {
    return isBlogPath() ? '../' : '';
  }

  function withRoot(html) {
    const root = rootPrefix();
    if (!root) return html;
    return html.replace(/href="([^"]+)"/g, (match, url) => {
      if (/^(https?:|\/|#|mailto:|tel:)/.test(url)) return match;
      return 'href="' + root + url + '"';
    });
  }

  function logoMarkup(link) {
    const root = rootPrefix();
    const inner =
      '<img src="' + root + 'assets/logos/revzio-icon.png" alt="" class="logo-mark" width="367" height="367" decoding="async" aria-hidden="true">' +
      '<span class="logo-word">revzio</span>';
    if (link === false) {
      return '<div class="logo" aria-label="revzio">' + inner + '</div>';
    }
    return '<a href="/" class="logo" aria-label="revzio home">' + inner + '</a>';
  }

  function injectNav() {
    const nav = document.querySelector('nav');
    if (!nav) return;

    // Preserve any nav-level classes (e.g. nav--dark-header on book-a-demo).
    const navClass = nav.className ? ' ' + nav.className : '';

    const NAV_INNER = `
  <div class="container nav-inner">
    ${logoMarkup(true)}
    <div class="nav-links">
      <button type="button" class="nav-mega-trigger" data-mega="orion" aria-expanded="false">Orion Agents</button>
      <button type="button" class="nav-mega-trigger" data-mega="platform" aria-expanded="false">Platform</button>
      <button type="button" class="nav-mega-trigger" data-mega="solutions" aria-expanded="false">Solutions</button>
      <a href="pricing.html" data-nav-link="pricing">Pricing</a>
    </div>
    <a href="book-a-demo.html" class="btn btn-primary">Book a demo</a>
  </div>
`;

    nav.innerHTML = withRoot(NAV_INNER);
    if (navClass) nav.className = navClass.trim();

    // Mega menus injected adjacent to nav (so they're fixed-position siblings).
    const MEGA = `
<button type="button" class="mega-backdrop" id="mega-backdrop" aria-label="Close menu"></button>

<div class="mega-panel mega-panel--dark" id="mega-orion" role="dialog" aria-label="Orion Agents menu" aria-hidden="true">
  <div class="container">
    <div class="mega-solutions-grid">
      <div class="mega-col">
        <ul>
          <li>
            <a href="agent-suite.html">Orion agent suite</a>
          </li>
          <li style="margin-top: 18px;">
            <a href="how-it-works.html">How Orion Works</a>
          </li>
        </ul>
      </div>

      <div class="mega-col">
        <h4>Orion Agents</h4>
        <ul>
          <li><a href="agent-reconciliation.html">Reconciliation Agent</a></li>
          <li><a href="agent-journal-entry.html">Journal Entry Agent</a></li>
          <li><a href="agent-ap.html">AP Agent</a></li>
          <li><a href="agent-ar.html">AR Agent</a></li>
          <li><a href="agent-accruals.html">Accruals Agent</a></li>
          <li><a href="agent-revenue-validation.html">Revenue Validation Agent</a></li>
          <li><a href="agent-close-management.html">Close Management Agent</a></li>
        </ul>
      </div>

      <aside aria-label="Featured">
        <div class="mega-news-card" style="border-color: rgba(127, 207, 170, 0.32);">
          <div class="mega-news-eyebrow">NEW</div>
          <div class="mega-news-title">Meet Orion agent suite</div>
          <div class="mega-news-sub">Seven agents. Every finance workflow. One close.</div>
          <a class="mega-news-link" href="agent-suite.html">Explore <span aria-hidden="true">→</span></a>
        </div>
      </aside>
    </div>
  </div>
</div>

<div class="mega-panel mega-panel--dark" id="mega-platform" role="dialog" aria-label="Platform menu" aria-hidden="true">
  <div class="container">
    <div class="mega-solutions-grid" style="grid-template-columns: 1fr 1fr; gap: 56px;">
      <div class="mega-col">
        <h4>BY PROCESS</h4>
        <ul>
          <li><a href="order-to-cash.html">Order to Cash</a></li>
          <li><a href="record-to-report.html">Record to Report</a></li>
          <li><a href="procure-to-pay.html">Procure to Pay</a></li>
          <li><a href="trust-center.html">Data Governance &amp; Controls</a></li>
          <li><a href="reporting.html">Management Reporting</a></li>
        </ul>
      </div>
      <div class="mega-col">
        <h4>CAPABILITIES</h4>
        <ul>
          <li><a href="integrations.html">Integrations</a></li>
          <li><a href="security.html">Security</a></li>
          <li><a href="how-it-works.html">How It Works</a></li>
          <li><a href="platform.html">Platform Overview</a></li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="mega-panel mega-panel--dark" id="mega-solutions" role="dialog" aria-label="Solutions menu" aria-hidden="true">
  <div class="container">
    <div class="mega-solutions-grid" style="grid-template-columns: 1fr 1fr; gap: 56px;">
      <div class="mega-col">
        <h4>BY USE CASE</h4>
        <ul>
          <li><a href="data-ingestion.html">Data Ingestion</a></li>
          <li><a href="recon-automation.html">Recon Automation</a></li>
          <li><a href="continuous-close.html">Continuous Close</a></li>
          <li><a href="automated-workflows.html">Automated Workflows</a></li>
          <li><a href="controls-and-audit-trails.html">Controls &amp; Audit Trails</a></li>
          <li><a href="accelerate-reporting-cycles.html">Accelerate Reporting</a></li>
        </ul>
      </div>
      <div class="mega-col">
        <h4>BY INDUSTRY</h4>
        <ul>
          <li><a href="industry-saas.html">SaaS &amp; Subscription</a></li>
          <li><a href="industry-enterprise.html">Enterprise Finance</a></li>
          <li><a href="industry-startup.html">VC-Backed Startups</a></li>
        </ul>
        <div style="margin-top:32px;">
          <h4>COMPANY</h4>
          <ul>
            <li><a href="about.html">About revzio</a></li>
            <li><a href="customers.html">Customer Stories</a></li>
            <li><a href="pricing.html">Pricing</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
`;

    // Remove any previously-injected mega panels from older scripts (safety).
    document.getElementById('mega-backdrop')?.remove();
    document.getElementById('mega-orion')?.remove();
    document.getElementById('mega-platform')?.remove();
    document.getElementById('mega-solutions')?.remove();

    nav.insertAdjacentHTML('afterend', withRoot(MEGA));

    initMegaBehavior(nav);
    setActiveNav(nav);
  }

  function setActiveNav(nav) {
    const path = window.location.pathname.replace(/\/+$/, '');
    const file = (path.split('/').pop() || 'index.html') || 'index.html';
    const onBlog = /\/blog\//.test(window.location.pathname);

    function setActive(el) {
      if (!el) return;
      el.classList.add('is-active');
      if (el.tagName === 'A') el.setAttribute('aria-current', 'page');
    }

    const pricing = nav.querySelector('[data-nav-link="pricing"]');
    const platformTrigger = nav.querySelector('.nav-mega-trigger[data-mega="platform"]');
    const solutionsTrigger = nav.querySelector('.nav-mega-trigger[data-mega="solutions"]');
    const orionTrigger = nav.querySelector('.nav-mega-trigger[data-mega="orion"]');

    if (file === 'pricing.html') setActive(pricing);
    else if (/^(platform\.html|integrations\.html|security\.html|how-it-works\.html|order-to-cash\.html|record-to-report\.html|procure-to-pay\.html|reporting\.html|trust-center\.html)$/.test(file)) setActive(platformTrigger);
    else if (/^(solutions\.html|data-ingestion\.html|recon-automation\.html|continuous-close\.html|automated-workflows\.html|controls-and-audit-trails\.html|accelerate-reporting-cycles\.html|industry-saas\.html|industry-enterprise\.html|industry-startup\.html)$/.test(file)) setActive(solutionsTrigger);
    else if (/^(agent-suite\.html|agent-reconciliation\.html|agent-journal-entry\.html|agent-ap\.html|agent-ar\.html|agent-accruals\.html|agent-revenue-validation\.html|agent-close-management\.html)$/.test(file)) setActive(orionTrigger);
    else if (onBlog || file === 'blog.html' || file === 'resources.html' || file === 'guides.html' || file === 'glossary.html' || file === 'customers.html' || file === 'about.html') {
      // Keep it simple: resources grouping is still discoverable via mega menu; we don't highlight it as a top-level item.
    }
  }

  function initMegaBehavior(nav) {
    const backdrop = document.getElementById('mega-backdrop');
    const panels = {
      orion: document.getElementById('mega-orion'),
      platform: document.getElementById('mega-platform'),
      solutions: document.getElementById('mega-solutions'),
    };
    const triggers = nav.querySelectorAll('.nav-mega-trigger');
    let openId = null;
    let closeTimer = null;
    let panelTopPx = null;
    let topRaf = null;
    const CLOSE_DELAY = 60;
    const isMobile = () => window.matchMedia('(max-width: 900px)').matches;

    function isMegaHoverTarget(el) {
      if (!el || !el.closest) return false;
      return !!(el.closest('.mega-panel') || el.closest('.nav-mega-trigger'));
    }

    function cancelClose() {
      if (closeTimer) clearTimeout(closeTimer);
      closeTimer = null;
    }

    function scheduleClose(delay) {
      cancelClose();
      closeTimer = setTimeout(closeAll, delay == null ? CLOSE_DELAY : delay);
    }

    function setActiveTrigger(id, active) {
      const trigger = nav.querySelector('.nav-mega-trigger[data-mega="' + id + '"]');
      if (!trigger) return;
      trigger.classList.toggle('is-active', active);
      trigger.setAttribute('aria-expanded', active ? 'true' : 'false');
    }

    function syncPanelTop() {
      panelTopPx = nav.getBoundingClientRect().bottom + 'px';
      Object.values(panels).forEach((p) => {
        if (p) p.style.top = panelTopPx;
      });
    }

    function setPanelTop() {
      if (topRaf) return;
      topRaf = requestAnimationFrame(() => {
        topRaf = null;
        syncPanelTop();
      });
    }

    function hidePanel(id) {
      if (!id || !panels[id]) return;
      panels[id].classList.remove('is-open');
      panels[id].setAttribute('aria-hidden', 'true');
      setActiveTrigger(id, false);
    }

    function showPanel(id) {
      if (!panels[id]) return;
      panels[id].classList.add('is-open');
      panels[id].setAttribute('aria-hidden', 'false');
      setActiveTrigger(id, true);
    }

    function closeAll() {
      cancelClose();
      openId = null;
      nav.classList.remove('mega-open');
      backdrop?.classList.remove('is-open');
      Object.values(panels).forEach((p) => {
        p?.classList.remove('is-open');
        p?.setAttribute('aria-hidden', 'true');
      });
      triggers.forEach((t) => {
        t.classList.remove('is-active');
        t.setAttribute('aria-expanded', 'false');
      });
      document.body.style.overflow = '';
    }

    function open(id, options) {
      const opts = options || {};
      if (opts.toggle && openId === id) {
        closeAll();
        return;
      }
      if (openId === id) return;

      cancelClose();
      if (!panelTopPx) syncPanelTop();

      nav.classList.add('mega-open');
      backdrop?.classList.add('is-open');

      if (openId) hidePanel(openId);
      openId = id;
      showPanel(id);

      document.body.style.overflow = opts.lockScroll ? 'hidden' : '';
    }

    triggers.forEach((btn) => {
      const id = btn.getAttribute('data-mega');
      if (!id || !panels[id]) return;

      btn.addEventListener('mouseenter', () => {
        if (isMobile()) return;
        cancelClose();
        open(id);
      });
      btn.addEventListener('mouseleave', (e) => {
        if (isMobile()) return;
        if (isMegaHoverTarget(e.relatedTarget)) return;
        scheduleClose();
      });
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        if (!isMobile()) return;
        e.stopPropagation();
        cancelClose();
        open(id, { toggle: true, lockScroll: true });
      });
    });

    // If user hovers any non-mega link inside nav links, close menus.
    const navLinks = nav.querySelector('.nav-links');
    if (navLinks) {
      navLinks.querySelectorAll('a').forEach((link) => {
        link.addEventListener('mouseenter', () => {
          if (isMobile()) return;
          closeAll();
        });
      });
    }

    nav.querySelectorAll('.logo, .nav-inner > .btn-primary, .nav-inner > a.btn-primary').forEach((el) => {
      el.addEventListener('mouseenter', () => {
        if (isMobile()) return;
        closeAll();
      });
    });

    nav.addEventListener('mouseleave', (e) => {
      if (isMobile()) return;
      if (isMegaHoverTarget(e.relatedTarget)) return;
      scheduleClose();
    });

    Object.values(panels).forEach((panel) => {
      panel?.addEventListener('mouseenter', () => {
        if (isMobile()) return;
        cancelClose();
      });
      panel?.addEventListener('mouseleave', (e) => {
        if (isMobile()) return;
        if (isMegaHoverTarget(e.relatedTarget)) return;
        scheduleClose();
      });
    });

    backdrop?.addEventListener('click', closeAll);
    backdrop?.addEventListener('mouseenter', () => {
      if (isMobile()) return;
      scheduleClose();
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeAll();
    });

    setPanelTop();
    window.addEventListener('resize', () => {
      panelTopPx = null;
      setPanelTop();
    });
    window.addEventListener('scroll', () => {
      if (!openId) return;
      panelTopPx = null;
      setPanelTop();
    }, { passive: true });
  }

  function ensureIntegrationLogos() {
    if (!document.querySelector('.int-logo, .mock-knowledge-orbit[data-brand]')) return;
    var prefix = rootPrefix();
    if (!document.querySelector('link[href*="integration-logos.css"]')) {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = prefix + 'css/integration-logos.css';
      document.head.appendChild(link);
    }
    if (!document.querySelector('script[src*="integration-logos.js"]')) {
      var script = document.createElement('script');
      script.src = prefix + 'js/integration-logos.js';
      script.defer = true;
      document.body.appendChild(script);
    } else if (window.revzioIntegrationLogos) {
      window.revzioIntegrationLogos.hydrate();
    }
  }

  function onReady() {
    injectNav();
    ensureIntegrationLogos();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onReady);
  } else {
    onReady();
  }
})();


(function () {
  const MEGA_HTML = `
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
        <div class="mega-news-card">
          <div class="mega-news-eyebrow">NEW</div>
          <div class="mega-news-title">Meet Orion agent suite</div>
          <div class="mega-news-sub">Seven purpose-built agents for finance close. Human-in-the-loop. Audit-ready from day one.</div>
          <a class="mega-news-link" href="agent-suite.html">Explore Orion <span aria-hidden="true">→</span></a>
        </div>
      </aside>
    </div>
  </div>
</div>

<div class="mega-panel mega-panel--dark" id="mega-platform" role="dialog" aria-label="Platform menu" aria-hidden="true">
  <div class="container">
    <div class="mega-platform-grid">
      <div class="mega-platform-tabs">
        <div class="mega-tabs" role="tablist" aria-label="Platform sections">
          <button type="button" class="mega-tab is-active" data-mega-tab="process" role="tab" aria-selected="true">Process</button>
          <button type="button" class="mega-tab" data-mega-tab="capabilities" role="tab" aria-selected="false">Platform capabilities</button>
        </div>

        <div class="mega-panels">
          <div class="mega-panel-body is-active" data-mega-panel="process" role="tabpanel">
            <div class="mega-tile-grid">
              <a class="mega-tile" href="order-to-cash.html"><span>Order to Cash</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="record-to-report.html"><span>Record to Report</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="procure-to-pay.html"><span>Procure to Pay</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="trust-center.html"><span>Data Governance &amp; Controls</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="reporting.html"><span>Management Reporting</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
            </div>
            <div class="mega-platform-foot">
              <a class="mega-foot-link" href="platform.html">Explore the platform <span aria-hidden="true">→</span></a>
            </div>
          </div>

          <div class="mega-panel-body" data-mega-panel="capabilities" role="tabpanel" hidden>
            <div class="mega-tile-grid mega-tile-grid--cap">
              <a class="mega-tile" href="integrations.html"><span>Integrations</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="security.html"><span>Security</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="how-it-works.html#auditable-ai"><span>Auditable AI</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
              <a class="mega-tile" href="how-it-works.html"><span>How It Works</span><span class="mega-tile-arrow" aria-hidden="true">→</span></a>
            </div>
            <div class="mega-platform-foot">
              <a class="mega-foot-link" href="how-it-works.html">See how Orion works <span aria-hidden="true">→</span></a>
            </div>
          </div>
        </div>
      </div>
      <div class="mega-feature-col">
        <div class="mega-feature-visual" aria-hidden="true">
          <h3>Auditable AI</h3>
        </div>
        <a href="resources.html" class="mega-feature-card">
          <div>
            <div class="mega-feature-card-label">Featured release</div>
            <div class="mega-feature-card-title">Why Accounting Needs Auditable AI</div>
          </div>
          <span class="mega-feature-card-arrow" aria-hidden="true">→</span>
        </a>
      </div>
    </div>
  </div>
</div>

<div class="mega-panel mega-panel--dark" id="mega-solutions" role="dialog" aria-label="Solutions menu" aria-hidden="true">
  <div class="container">
    <div class="mega-solutions-layout">
      <div class="mega-solutions-left">
        <div class="mega-solutions-title">By use case</div>
        <div class="mega-solutions-tiles">
          <a class="mega-solution-tile" href="data-ingestion.html">
            <span class="mega-solution-icon" aria-hidden="true">⛓</span>
            <span class="mega-solution-label">Data ingestion</span>
            <span class="mega-solution-arrow" aria-hidden="true">→</span>
          </a>
          <a class="mega-solution-tile" href="recon-automation.html">
            <span class="mega-solution-icon" aria-hidden="true">≋</span>
            <span class="mega-solution-label">Recon automation</span>
            <span class="mega-solution-arrow" aria-hidden="true">→</span>
          </a>
          <a class="mega-solution-tile" href="continuous-close.html">
            <span class="mega-solution-icon" aria-hidden="true">⟲</span>
            <span class="mega-solution-label">Continuous close</span>
            <span class="mega-solution-arrow" aria-hidden="true">→</span>
          </a>

          <a class="mega-solution-tile" href="automated-workflows.html">
            <span class="mega-solution-icon" aria-hidden="true">▦</span>
            <span class="mega-solution-label">Automated workflows</span>
            <span class="mega-solution-arrow" aria-hidden="true">→</span>
          </a>
          <a class="mega-solution-tile" href="controls-and-audit-trails.html">
            <span class="mega-solution-icon" aria-hidden="true">✓</span>
            <span class="mega-solution-label">Controls &amp; audit trails</span>
            <span class="mega-solution-arrow" aria-hidden="true">→</span>
          </a>
          <a class="mega-solution-tile" href="accelerate-reporting-cycles.html">
            <span class="mega-solution-icon" aria-hidden="true">▤</span>
            <span class="mega-solution-label">Accelerate reporting cycles</span>
            <span class="mega-solution-arrow" aria-hidden="true">→</span>
          </a>
        </div>
      </div>

      <aside class="mega-solutions-right" aria-label="By industry">
        <div class="mega-col">
          <h4>By Industry</h4>
          <ul>
            <li><a href="industry-saas.html">SaaS &amp; Subscription</a></li>
            <li><a href="industry-enterprise.html">Enterprise Finance</a></li>
            <li><a href="industry-startup.html">VC-Backed Startups</a></li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</div>

<div class="mega-panel mega-panel--dark" id="mega-resources" role="dialog" aria-label="Resources menu" aria-hidden="true">
  <div class="container">
    <div class="mega-resources-grid">
      <ul class="mega-links">
        <li>
          <a href="about.html">
            <span class="mega-link-title">About revzio</span>
            <span class="mega-link-desc">The company building the AI platform for the next generation of accounting</span>
          </a>
        </li>
        <li>
          <a href="how-it-works.html">
            <span class="mega-link-title">How It Works</span>
            <span class="mega-link-desc">The technical story behind Orion agents</span>
          </a>
        </li>
        <li>
          <a href="blog.html">
            <span class="mega-link-title">Blog</span>
            <span class="mega-link-desc">Insights on AI-powered accounting</span>
          </a>
        </li>
        <li>
          <a href="index.html#product-showcase">
            <span class="mega-link-title">Product Tours</span>
            <span class="mega-link-desc">Explore the platform with guided product demos</span>
          </a>
        </li>
        <li>
          <a href="resources.html">
            <span class="mega-link-title">Customer Stories</span>
            <span class="mega-link-desc">Stories from teams transforming operations with revzio</span>
          </a>
        </li>
        <li>
          <a href="resources.html">
            <span class="mega-link-title">Industry Guides</span>
            <span class="mega-link-desc">SaaS, Enterprise, and Startup finance guides</span>
          </a>
        </li>
        <li>
          <a href="glossary.html">
            <span class="mega-link-title">Glossary</span>
            <span class="mega-link-desc">Compliance, accounting, and audit terms explained</span>
          </a>
        </li>
      </ul>
      <div>
        <div class="mega-resource-visual" aria-hidden="true">
          <span class="mega-logo-mark">
            <img src="assets/logos/revzio-icon.png" alt="" class="mega-logo-icon" width="367" height="367" decoding="async" aria-hidden="true">
            <span class="mega-logo-text">revzio</span>
          </span>
        </div>
        <a href="resources.html" class="mega-resource-card">
          <div>
            <div class="mega-resource-card-label">eBook</div>
            <div class="mega-resource-card-title">From Pencils to Agents: Audit AI Readiness Assessment</div>
          </div>
          <span class="mega-feature-card-arrow" aria-hidden="true">→</span>
        </a>
      </div>
    </div>
  </div>
</div>
`;


  function megaMenuRootPrefix() {
    return /\/blog\//.test(window.location.pathname) ? '../' : '';
  }

  function withMegaRoot(html) {
    const root = megaMenuRootPrefix();
    if (!root) return html;
    return html
      .replace(/href="([^"]+)"/g, (match, url) => {
        if (/^(https?:|\/|#|mailto:|tel:)/.test(url)) return match;
        return 'href="' + root + url + '"';
      })
      .replace(/src="([^"]+)"/g, (match, url) => {
        if (/^(https?:|\/|data:)/.test(url)) return match;
        return 'src="' + root + url + '"';
      });
  }

  function init() {
    const nav = document.querySelector('nav');
    if (!nav || document.getElementById('mega-platform')) return;

    const wrap = document.createElement('div');
    wrap.innerHTML = withMegaRoot(MEGA_HTML);
    while (wrap.firstChild) nav.parentNode.insertBefore(wrap.firstChild, nav.nextSibling);

    // Platform mega menu tabs (Process / Platform capabilities)
    (function initPlatformMegaTabs() {
      const root = document.getElementById('mega-platform');
      if (!root) return;
      const tabs = Array.from(root.querySelectorAll('[data-mega-tab]'));
      const panels = Array.from(root.querySelectorAll('[data-mega-panel]'));
      if (!tabs.length || !panels.length) return;

      function setActive(id) {
        tabs.forEach((t) => {
          const active = t.dataset.megaTab === id;
          t.classList.toggle('is-active', active);
          t.setAttribute('aria-selected', active ? 'true' : 'false');
        });
        panels.forEach((p) => {
          const active = p.dataset.megaPanel === id;
          p.classList.toggle('is-active', active);
          p.hidden = !active;
        });
      }

      tabs.forEach((t) => t.addEventListener('click', () => setActive(t.dataset.megaTab)));
      const initial = tabs.find((t) => t.classList.contains('is-active'))?.dataset.megaTab || tabs[0].dataset.megaTab;
      setActive(initial);
    })();

    const backdrop = document.getElementById('mega-backdrop');
    const panels = {
      orion: document.getElementById('mega-orion'),
      platform: document.getElementById('mega-platform'),
      solutions: document.getElementById('mega-solutions'),
      resources: document.getElementById('mega-resources'),
    };
    const triggers = document.querySelectorAll('.nav-mega-trigger');
    let openId = null;
    let closeTimer = null;
    let panelTopPx = null;
    let topRaf = null;
    const CLOSE_DELAY = 50;
    const isMobile = () => window.matchMedia('(max-width: 900px)').matches;

    /** Only triggers + dropdown count as “inside” the menu (not the whole nav bar). */
    function isMegaHoverTarget(el) {
      if (!el || !el.closest) return false;
      return !!(
        el.closest('.mega-panel') ||
        el.closest('.nav-mega-trigger')
      );
    }

    function cancelClose() {
      if (closeTimer) clearTimeout(closeTimer);
      closeTimer = null;
    }

    function scheduleClose(delay) {
      cancelClose();
      closeTimer = setTimeout(closeAll, delay == null ? CLOSE_DELAY : delay);
    }

    function setPanelTop() {
      if (topRaf) return;
      topRaf = requestAnimationFrame(() => {
        topRaf = null;
        syncPanelTop();
      });
    }

    function setActiveTrigger(id, active) {
      const trigger = document.querySelector('.nav-mega-trigger[data-mega="' + id + '"]');
      if (!trigger) return;
      trigger.classList.toggle('is-active', active);
      trigger.setAttribute('aria-expanded', active ? 'true' : 'false');
    }

    function hidePanel(id) {
      if (!id || !panels[id]) return;
      panels[id].classList.remove('is-open');
      panels[id].setAttribute('aria-hidden', 'true');
      setActiveTrigger(id, false);
    }

    function showPanel(id) {
      panels[id].classList.add('is-open');
      panels[id].setAttribute('aria-hidden', 'false');
      setActiveTrigger(id, true);
    }

    function closeAll() {
      cancelClose();
      openId = null;
      nav.classList.remove('mega-open');
      backdrop.classList.remove('is-open');
      Object.values(panels).forEach((p) => {
        p.classList.remove('is-open');
        p.setAttribute('aria-hidden', 'true');
      });
      triggers.forEach((t) => {
        t.classList.remove('is-active');
        t.setAttribute('aria-expanded', 'false');
      });
      document.body.style.overflow = '';
    }

    function syncPanelTop() {
      panelTopPx = nav.getBoundingClientRect().bottom + 'px';
      Object.values(panels).forEach((p) => {
        if (p) p.style.top = panelTopPx;
      });
    }

    function open(id, options) {
      const opts = options || {};
      if (opts.toggle && openId === id) {
        closeAll();
        return;
      }
      if (openId === id) return;

      cancelClose();

      if (openId) {
        hidePanel(openId);
        openId = id;
        showPanel(id);
        return;
      }

      openId = id;
      if (!panelTopPx) syncPanelTop();
      nav.classList.add('mega-open');
      backdrop.classList.add('is-open');
      showPanel(id);
      document.body.style.overflow = opts.lockScroll ? 'hidden' : '';
    }

    triggers.forEach((btn) => {
      const id = btn.getAttribute('data-mega');

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
        if (!isMobile()) {
          e.preventDefault();
          return;
        }
        e.preventDefault();
        e.stopPropagation();
        cancelClose();
        open(id, { toggle: true, lockScroll: true });
      });
    });

    const navLinks = nav.querySelector('.nav-links');
    if (navLinks) {
      navLinks.querySelectorAll('a:not(.nav-mega-trigger)').forEach((link) => {
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
      panel.addEventListener('mouseenter', () => {
        if (isMobile()) return;
        cancelClose();
      });
      panel.addEventListener('mouseleave', (e) => {
        if (isMobile()) return;
        if (isMegaHoverTarget(e.relatedTarget)) return;
        scheduleClose();
      });
    });

    backdrop.addEventListener('click', closeAll);
    backdrop.addEventListener('mouseenter', () => {
      if (isMobile()) return;
      scheduleClose();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeAll();
    });
    setPanelTop();
    let resizeTimer;
    window.addEventListener('resize', () => {
      panelTopPx = null;
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(setPanelTop, 100);
    });
    window.addEventListener('scroll', () => {
      if (!openId) return;
      panelTopPx = null;
      setPanelTop();
    }, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

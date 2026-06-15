(function () {
  function injectGlobalStyles() {
    if (document.getElementById('revzio-anim-styles')) return;
    const style = document.createElement('style');
    style.id = 'revzio-anim-styles';
    style.textContent = `
      .reveal-on-scroll {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.65s ease, transform 0.65s ease;
        will-change: opacity, transform;
      }
      .reveal-on-scroll.is-visible {
        opacity: 1;
        transform: translateY(0);
      }

      /* Agent-prepared badge component */
      .agent-prepared-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(10, 15, 12, 0.92);
        border: 1px solid rgba(127, 207, 170, 0.28);
        color: #FAFAF7;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-size: 12px;
      }
      .agent-prepared-badge svg {
        width: 14px;
        height: 14px;
        color: var(--hero-mint, #7FCFAA);
        flex-shrink: 0;
        filter: drop-shadow(0 0 10px rgba(127, 207, 170, 0.4));
      }

      /* Hover accent for agent card grids (no layout shift) */
      .card:hover,
      a.card:hover {
        box-shadow: inset 3px 0 0 var(--accent, #0F6B4E), var(--shadow);
      }
    `;
    document.head.appendChild(style);
  }

  function initRevealOnScroll() {
    const els = Array.from(document.querySelectorAll('.reveal-on-scroll, .reveal'));
    if (!els.length) return;

    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        // subpage.css expects `.reveal.in`
        e.target.classList.add('in');
        // other styles may use these visibility hooks
        e.target.classList.add('visible');
        e.target.classList.add('is-visible');
        obs.unobserve(e.target);
      });
    }, { threshold: 0.15 });

    els.forEach((el) => obs.observe(el));
  }

  function animateCountUp(el) {
    const raw = el.getAttribute('data-target');
    if (!raw) return;
    const target = Number(raw);
    if (!Number.isFinite(target)) return;

    const duration = 2000;
    const start = performance.now();
    const suffix = el.getAttribute('data-suffix') || '';
    const prefix = el.getAttribute('data-prefix') || '';

    function step(now) {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      const value = Math.round(target * eased);
      el.textContent = prefix + value + suffix;
      if (t < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  function initCountUps() {
    const els = Array.from(document.querySelectorAll('[data-target]'));
    if (!els.length) return;

    const started = new WeakSet();
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        if (started.has(e.target)) return;
        started.add(e.target);
        animateCountUp(e.target);
        obs.unobserve(e.target);
      });
    }, { threshold: 0.35 });

    els.forEach((el) => obs.observe(el));
  }

  function init() {
    injectGlobalStyles();
    initRevealOnScroll();
    initCountUps();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();


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

  function initOrionSuite() {
    const section = document.getElementById('orion-agent-suite');
    if (!section) return;

    const stage = section.querySelector('.orion-suite__stage');
    const pathEl = section.querySelector('.orion-suite__flow-path');
    const dotEl = section.querySelector('.orion-suite__flow-dot');
    const cards = section.querySelectorAll('.orion-card');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function drawFlowPath() {
      if (!stage || !pathEl || !cards.length || reducedMotion) return;
      if (window.innerWidth <= 900) return;

      const stageRect = stage.getBoundingClientRect();
      const points = Array.from(cards).map((card) => {
        const r = card.getBoundingClientRect();
        return {
          x: r.left + r.width / 2 - stageRect.left,
          y: r.top + r.height / 2 - stageRect.top,
        };
      });

      if (points.length < 2) return;

      let d = `M ${points[0].x.toFixed(1)} ${points[0].y.toFixed(1)}`;
      for (let i = 1; i < points.length; i += 1) {
        const prev = points[i - 1];
        const curr = points[i];
        const midX = ((prev.x + curr.x) / 2).toFixed(1);
        d += ` C ${midX} ${prev.y.toFixed(1)}, ${midX} ${curr.y.toFixed(1)}, ${curr.x.toFixed(1)} ${curr.y.toFixed(1)}`;
      }

      pathEl.setAttribute('d', d);
      const len = pathEl.getTotalLength();
      pathEl.style.strokeDasharray = `${len}`;
      pathEl.style.strokeDashoffset = `${len}`;

      requestAnimationFrame(() => {
        pathEl.style.transition = 'stroke-dashoffset 2s cubic-bezier(0.4, 0, 0.2, 1) 0.35s';
        pathEl.style.strokeDashoffset = '0';
      });

      if (dotEl && typeof pathEl.getPointAtLength === 'function') {
        const start = performance.now();
        const duration = 2400;
        const delay = 350;

        function moveDot(now) {
          const t = Math.min(1, Math.max(0, (now - start - delay) / duration));
          if (t <= 0) {
            requestAnimationFrame(moveDot);
            return;
          }
          const eased = 1 - Math.pow(1 - t, 2.2);
          const point = pathEl.getPointAtLength(len * eased);
          dotEl.setAttribute('cx', point.x.toFixed(1));
          dotEl.setAttribute('cy', point.y.toFixed(1));
          if (t < 1) requestAnimationFrame(moveDot);
        }

        requestAnimationFrame(moveDot);
      }
    }

    function activateSection() {
      if (section.classList.contains('is-active')) return;
      section.classList.add('is-active');
      requestAnimationFrame(() => {
        requestAnimationFrame(drawFlowPath);
      });
    }

    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        activateSection();
        obs.unobserve(section);
      });
    }, { threshold: 0.16 });

    obs.observe(section);

    requestAnimationFrame(() => {
      const rect = section.getBoundingClientRect();
      const inView = rect.top < window.innerHeight * 0.84 && rect.bottom > window.innerHeight * 0.16;
      if (inView) activateSection();
    });
  }

  function initPlatformShowcase() {
    const section = document.getElementById('product');
    if (!section) return;

    const rows = section.querySelectorAll('.platform-showcase__row');
    const navBtns = section.querySelectorAll('.platform-showcase__nav-btn');
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const chatTimers = [];

    function activateSection() {
      section.classList.add('is-active');
    }

    function setActivePillar(pillar) {
      navBtns.forEach((btn) => {
        btn.classList.toggle('is-active', btn.dataset.pillar === pillar);
      });
      rows.forEach((row) => {
        row.classList.toggle('is-focused', row.dataset.pillar === pillar);
      });
    }

    function runChatDemo(row) {
      const chat = row.querySelector('.mock-chat');
      if (!chat || chat.dataset.demoStarted === '1') return;
      chat.dataset.demoStarted = '1';

      const steps = chat.querySelectorAll('.chat-demo-step');
      const input = chat.querySelector('.mock-chat-input');
      const inputText = chat.querySelector('.mock-chat-input-text');
      const question = 'Why did deferred revenue move $18K this period?';

      if (reducedMotion) {
        steps.forEach((step) => step.classList.add('is-shown'));
        return;
      }

      const showStep = (idx) => steps[idx]?.classList.add('is-shown');
      const hideStep = (idx) => steps[idx]?.classList.remove('is-shown');

      chatTimers.push(setTimeout(() => {
        input?.classList.add('is-typing');
        let i = 0;
        const typeInterval = setInterval(() => {
          i += 1;
          if (inputText) inputText.textContent = question.slice(0, i);
          if (i >= question.length) {
            clearInterval(typeInterval);
            chatTimers.push(setTimeout(() => {
              showStep(1);
              if (inputText) inputText.textContent = 'Ask Orion anything about your close…';
              input?.classList.remove('is-typing');
              chatTimers.push(setTimeout(() => {
                showStep(2);
                chatTimers.push(setTimeout(() => {
                  hideStep(2);
                  showStep(3);
                }, 1200));
              }, 450));
            }, 320));
          }
        }, 32);
      }, 1200));
    }

    navBtns.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = btn.getAttribute('href')?.slice(1);
        const target = targetId ? document.getElementById(targetId) : null;
        if (target) {
          setActivePillar(btn.dataset.pillar || '');
          target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
        }
      });
    });

    const rowObs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const row = entry.target;
        if (!entry.isIntersecting) return;
        row.classList.add('is-visible');
        setActivePillar(row.dataset.pillar || '');
        if (row.dataset.pillar === 'orion-ai') runChatDemo(row);
      });
    }, { threshold: 0.42, rootMargin: '-18% 0px -32% 0px' });

    rows.forEach((row) => rowObs.observe(row));

    const sectionObs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        activateSection();
        sectionObs.unobserve(section);
      });
    }, { threshold: 0.12 });

    sectionObs.observe(section);

    requestAnimationFrame(() => {
      const rect = section.getBoundingClientRect();
      const inView = rect.top < window.innerHeight * 0.9 && rect.bottom > 0;
      if (inView) activateSection();
    });
  }

  function initWhyBenefits() {
    const section = document.getElementById('why-revzio');
    if (!section) return;

    function activateSection() {
      section.classList.add('is-active');
    }

    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        activateSection();
        obs.unobserve(section);
      });
    }, { threshold: 0.18 });

    obs.observe(section);

    requestAnimationFrame(() => {
      const rect = section.getBoundingClientRect();
      const inView = rect.top < window.innerHeight * 0.88 && rect.bottom > 0;
      if (inView) activateSection();
    });
  }

  function init() {
    injectGlobalStyles();
    initRevealOnScroll();
    initCountUps();
    initOrionSuite();
    initPlatformShowcase();
    initWhyBenefits();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();


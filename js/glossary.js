(function () {
  const terms = window.GLOSSARY_TERMS || [];
  const list = document.getElementById('glossary-list');
  const emptyState = document.getElementById('glossary-empty');
  const searchInput = document.getElementById('glossary-search');
  const searchForm = document.getElementById('glossary-search-form');

  const SUBJECT_LABELS = {
    'accounting-compliance': 'Accounting Compliance',
    'artificial-intelligence': 'Artificial Intelligence',
    'audit-management': 'Audit Management',
    'lease-accounting': 'Lease Accounting',
    'revenue-recognition': 'Revenue Recognition',
  };

  let state = {
    type: 'compliance',
    subjects: new Set(['all']),
    query: '',
  };

  function subjectLabel(key) {
    return SUBJECT_LABELS[key] || key;
  }

  function typeLabel(type) {
    return type === 'ai' ? 'AI Terms' : 'Compliance Terms';
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function getSelectedTypes() {
    const allCb = document.querySelector('[data-type-all]');
    if (allCb && allCb.checked) return new Set(['all']);
    const selected = new Set();
    document.querySelectorAll('[data-filter="type"] input[name="type"]').forEach((cb) => {
      if (cb.checked && cb.value !== 'all') selected.add(cb.value);
    });
    return selected.size ? selected : new Set(['all']);
  }

  function getSelectedSubjects() {
    const allCb = document.querySelector('[data-subject-all]');
    if (allCb && allCb.checked) return new Set(['all']);
    const selected = new Set();
    document.querySelectorAll('[data-filter="subject"] input[name="subject"]').forEach((cb) => {
      if (cb.checked && cb.value !== 'all') selected.add(cb.value);
    });
    return selected.size ? selected : new Set(['all']);
  }

  function matchesFilters(term) {
    const types = getSelectedTypes();
    const subjects = getSelectedSubjects();

    if (!types.has('all') && !types.has(term.type)) return false;

    if (!subjects.has('all')) {
      const hasSubject = term.subjects.some((s) => subjects.has(s));
      if (!hasSubject) return false;
    }

    if (state.query) {
      const hay = (term.title + ' ' + term.summary + ' ' + (term.body || '')).toLowerCase();
      if (!hay.includes(state.query)) return false;
    }

    return true;
  }

  function renderCards() {
    if (!list) return;

    list.innerHTML = terms
      .map((term, index) => {
        const subjectTags = term.subjects
          .map(
            (s) =>
              `<span class="glossary-tag glossary-tag--subject">${escapeHtml(subjectLabel(s))}</span>`
          )
          .join('');
        const bodyBlock =
          term.body && term.body.trim()
            ? `<div class="glossary-card-body">${term.body}</div>`
            : '';
        const expanded = index === 0 ? ' is-expanded' : ' is-collapsed';
        const toggleChar = index === 0 ? '−' : '+';

        return `<article class="glossary-card${expanded}" data-type="${term.type}" data-subject="${term.subjects.join(' ')}" data-id="${term.id}">
          <button type="button" class="glossary-card-toggle" aria-expanded="${index === 0 ? 'true' : 'false'}" aria-label="Toggle definition">${toggleChar}</button>
          <div class="glossary-card-tags">
            <span class="glossary-tag glossary-tag--type">${typeLabel(term.type)}</span>
            ${subjectTags}
          </div>
          <h3>${escapeHtml(term.title)}</h3>
          <p class="glossary-card-summary">${escapeHtml(term.summary)}</p>
          ${bodyBlock}
          <div class="glossary-card-footer">
            <a href="#${term.id}" class="glossary-card-read">
              Read now
              <span class="glossary-card-read-icon" aria-hidden="true">→</span>
            </a>
          </div>
        </article>`;
      })
      .join('');

    bindCardToggles();
    applyFilters();
  }

  function bindCardToggles() {
    list.querySelectorAll('.glossary-card').forEach((card) => {
      const btn = card.querySelector('.glossary-card-toggle');
      const read = card.querySelector('.glossary-card-read');
      if (btn) {
        btn.addEventListener('click', () => toggleCard(card));
      }
      if (read) {
        read.addEventListener('click', (e) => {
          if (!card.classList.contains('is-expanded')) {
            e.preventDefault();
            toggleCard(card, true);
          }
        });
      }
    });
  }

  function toggleCard(card, forceOpen) {
    const open = forceOpen || card.classList.contains('is-collapsed');
    card.classList.toggle('is-expanded', open);
    card.classList.toggle('is-collapsed', !open);
    const btn = card.querySelector('.glossary-card-toggle');
    if (btn) {
      btn.textContent = open ? '−' : '+';
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
  }

  function applyFilters() {
    let visible = 0;
    list.querySelectorAll('.glossary-card').forEach((card) => {
      const id = card.dataset.id;
      const term = terms.find((t) => t.id === id);
      const show = term && matchesFilters(term);
      card.classList.toggle('is-hidden', !show);
      if (show) visible += 1;
    });
    if (emptyState) emptyState.hidden = visible > 0;
    if (list) list.style.display = visible === 0 ? 'none' : '';
  }

  function syncHeroTabs() {
    const types = getSelectedTypes();
    const onlyAi = types.has('ai') && !types.has('compliance') && !types.has('all');
    const onlyComp = types.has('compliance') && !types.has('ai') && !types.has('all');
    document.querySelectorAll('[data-hero-type]').forEach((btn) => {
      const t = btn.dataset.heroType;
      btn.classList.toggle('is-active', (onlyAi && t === 'ai') || (onlyComp && t === 'compliance'));
    });
  }

  function applyHeroType(type, scroll) {
    state.type = type;
    syncHeroTabs();

    const allType = document.querySelector('[data-type-all]');
    const aiCb = document.querySelector('[data-filter="type"] input[value="ai"]');
    const compCb = document.querySelector('[data-filter="type"] input[value="compliance"]');

    if (allType) allType.checked = false;
    if (type === 'ai') {
      if (aiCb) aiCb.checked = true;
      if (compCb) compCb.checked = false;
    } else {
      if (compCb) compCb.checked = true;
      if (aiCb) aiCb.checked = false;
    }

    applyFilters();
    if (scroll) {
      const body = document.querySelector('.glossary-body');
      if (body) body.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  document.querySelectorAll('[data-hero-type]').forEach((btn) => {
    btn.addEventListener('click', () => {
      applyHeroType(btn.dataset.heroType || 'compliance', true);
    });
  });

  document.querySelectorAll('[data-filter="type"] input').forEach((cb) => {
    cb.addEventListener('change', () => {
      const allCb = document.querySelector('[data-type-all]');
      if (cb.dataset.typeAll) {
        if (cb.checked) {
          document.querySelectorAll('[data-filter="type"] input').forEach((x) => {
            if (x !== cb) x.checked = false;
          });
        }
      } else if (cb.checked) {
        if (allCb) allCb.checked = false;
      }
      const types = getSelectedTypes();
      if (types.has('ai') && !types.has('compliance') && !types.has('all')) {
        state.type = 'ai';
      } else if (types.has('compliance') && !types.has('ai') && !types.has('all')) {
        state.type = 'compliance';
      }
      syncHeroTabs();
      applyFilters();
    });
  });

  document.querySelectorAll('[data-filter="subject"] input').forEach((cb) => {
    cb.addEventListener('change', () => {
      const allCb = document.querySelector('[data-subject-all]');
      if (cb.dataset.subjectAll) {
        if (cb.checked) {
          document.querySelectorAll('[data-filter="subject"] input').forEach((x) => {
            if (x !== cb) x.checked = false;
          });
        }
      } else if (cb.checked) {
        if (allCb) allCb.checked = false;
      }
      applyFilters();
    });
  });

  if (searchForm) {
    searchForm.addEventListener('submit', (e) => e.preventDefault());
  }
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      state.query = searchInput.value.trim().toLowerCase();
      applyFilters();
    });
  }

  renderCards();
  syncHeroTabs();
  applyFilters();
})();

(function () {
  const tabs = Array.from(document.querySelectorAll('[data-platform-tab]'));
  const panels = Array.from(document.querySelectorAll('[data-platform-panel]'));

  if (!tabs.length || !panels.length) return;

  function setActive(id) {
    tabs.forEach((t) => {
      const active = t.dataset.platformTab === id;
      t.classList.toggle('is-active', active);
      t.setAttribute('aria-selected', active ? 'true' : 'false');
    });

    panels.forEach((p) => {
      const active = p.dataset.platformPanel === id;
      p.classList.toggle('is-active', active);
      p.hidden = !active;
    });
  }

  tabs.forEach((t) => {
    t.addEventListener('click', () => setActive(t.dataset.platformTab));
  });

  // Ensure initial state is valid even if HTML changes
  const initial = tabs.find((t) => t.classList.contains('is-active'))?.dataset.platformTab || tabs[0].dataset.platformTab;
  setActive(initial);
})();


(function () {
  const groups = Array.from(document.querySelectorAll('[data-solution-tabs]'));
  if (!groups.length) return;

  groups.forEach((root) => {
    const tabs = Array.from(root.querySelectorAll('[data-solution-tab]'));
    const panels = Array.from(root.querySelectorAll('[data-solution-panel]'));
    if (!tabs.length || !panels.length) return;

    function setActive(id) {
      tabs.forEach((t) => {
        const active = t.dataset.solutionTab === id;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      panels.forEach((p) => {
        const active = p.dataset.solutionPanel === id;
        p.hidden = !active;
      });
    }

    tabs.forEach((t) => t.addEventListener('click', () => setActive(t.dataset.solutionTab)));
    const initial = tabs.find((t) => t.classList.contains('is-active'))?.dataset.solutionTab || tabs[0].dataset.solutionTab;
    setActive(initial);
  });
})();


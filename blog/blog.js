const filters = document.querySelector('.filters');
if (filters) {
  filters.hidden = false;
  const buttons = [...filters.querySelectorAll('button')];
  const cards = [...document.querySelectorAll('.stories .story-card')];
  const feature = document.querySelector('.feature');
  const status = document.querySelector('#story-count');
  for (const button of buttons) {
    button.addEventListener('click', () => {
      const category = button.dataset.filter;
      for (const item of buttons) {
        const selected = item === button;
        item.classList.toggle('selected', selected);
        item.setAttribute('aria-pressed', String(selected));
      }
      let count = 0;
      for (const card of cards) {
        card.hidden = category !== 'all' && card.dataset.category !== category;
        if (!card.hidden) count++;
      }
      feature.hidden = category !== 'all';
      status.textContent = `${count} ${count === 1 ? 'članak' : count < 5 ? 'članka' : 'članaka'}`;
    });
  }
}

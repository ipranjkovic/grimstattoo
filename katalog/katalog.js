(() => {
  const WA = '387644154361';
  const KEY = 'grimOdabir';
  const track = (name, params) => { try { window.gtag && gtag('event', name, params || {}); } catch (e) {} };
  const motivi = (n) => (n % 10 === 1 && n % 100 !== 11 ? 'motiv' : 'motiva');
  const waLink = (text) => `https://wa.me/${WA}?text=${encodeURIComponent(text)}`;

  // ---------- Moj odabir (pamti se u pregledniku, vrijedi za sve kataloge) ----------
  let picks = [];
  try { picks = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { picks = []; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(picks)); } catch (e) {} };
  const isPicked = (s) => picks.some((p) => p.s === s);
  const bar = document.querySelector('.picks');

  function togglePick(s, thumb) {
    if (isPicked(s)) picks = picks.filter((p) => p.s !== s);
    else { picks.push({ s, t: thumb }); track('katalog_spremi', { motiv: s }); }
    save();
    syncFavs();
  }

  function syncFavs() {
    document.querySelectorAll('.fav[data-sifra]').forEach((b) => {
      const on = isPicked(b.dataset.sifra);
      b.setAttribute('aria-pressed', String(on));
      b.setAttribute('aria-label', (on ? 'Makni ' : 'Spremi ') + b.dataset.sifra + (on ? ' iz odabira' : ' u odabir'));
    });
    if (viewer && viewer.open) updateViewerFav();
    if (!bar) return;
    bar.hidden = picks.length === 0;
    const n = picks.length;
    bar.querySelector('.picks-count').textContent = `${n} ${motivi(n)}`;
    const thumbs = bar.querySelector('.picks-thumbs');
    thumbs.replaceChildren(...picks.slice(-4).map((p) => {
      const img = document.createElement('img');
      img.src = p.t; img.alt = p.s; img.width = 44; img.height = 44;
      return img;
    }));
    const codes = picks.map((p) => p.s).join(', ');
    bar.querySelector('.picks-send').href = waLink(`Pozdrav! Iz kataloga su mi se svidjeli motivi: ${codes}. Zanima me cijena i slobodan termin.`);
  }

  if (bar) {
    bar.querySelector('.picks-clear').addEventListener('click', () => { picks = []; save(); syncFavs(); });
    bar.querySelector('.picks-send').addEventListener('click', () => track('katalog_whatsapp_odabir', { broj: picks.length }));
  }

  // ---------- Filteri ----------
  const tiles = [...document.querySelectorAll('.motiv')];
  const count = document.querySelector('.count');
  const filters = document.querySelector('.filters');
  if (filters) {
    filters.hidden = false;
    filters.addEventListener('click', (e) => {
      const btn = e.target.closest('button[data-filter]');
      if (!btn) return;
      const f = btn.dataset.filter;
      filters.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
      let n = 0;
      tiles.forEach((t) => { t.hidden = f !== 'sve' && t.dataset.tema !== f; if (!t.hidden) n++; });
      if (count) count.textContent = `${n} ${motivi(n)}`;
      const tb = document.querySelector('.toolbar');
      if (tb && tb.getBoundingClientRect().top < 0) tb.scrollIntoView({ block: 'start' });
    });
  }

  document.addEventListener('click', (e) => {
    const fav = e.target.closest('.fav[data-sifra]');
    if (fav) { togglePick(fav.dataset.sifra, fav.dataset.thumb); return; }
    const open = e.target.closest('.motiv-open');
    if (open && viewer) { e.preventDefault(); openViewer(open.closest('.motiv')); }
  });

  // ---------- Preglednik ----------
  const viewer = document.querySelector('.viewer');
  if (!viewer) { syncFavs(); return; }
  const vImg = viewer.querySelector('.stage img');
  const vCode = viewer.querySelector('.info h2');
  const vTema = viewer.querySelector('.tag-tema');
  const vCount = viewer.querySelector('.viewer-count');
  const vAsk = viewer.querySelector('.ask');
  const vFav = viewer.querySelector('.btn-fav');
  const vFavText = viewer.querySelector('.btn-fav span');
  const kolekcija = document.body.dataset.kolekcija || '';
  let list = [];
  let idx = 0;

  const visible = () => tiles.filter((t) => !t.hidden);

  function show(i) {
    idx = (i + list.length) % list.length;
    const t = list[idx];
    const s = t.dataset.sifra;
    const thumb = t.querySelector('img');
    vImg.src = thumb.currentSrc || thumb.src;
    vImg.alt = thumb.alt;
    const full = new Image();
    full.onload = () => { if (list[idx] === t) vImg.src = full.src; };
    full.src = t.dataset.full;
    vCode.textContent = s;
    vTema.textContent = t.dataset.tema || '';
    vCount.textContent = `${idx + 1} / ${list.length}`;
    vAsk.href = waLink(`Pozdrav! Zanima me motiv ${s} iz kataloga ${kolekcija}. Možeš li mi javiti cijenu i slobodan termin?`);
    updateViewerFav();
    history.replaceState(null, '', '#' + s);
    [1, -1].forEach((d) => { const n = list[(idx + d + list.length) % list.length]; if (n) new Image().src = n.dataset.full; });
  }

  function updateViewerFav() {
    const t = list[idx];
    if (!t) return;
    const on = isPicked(t.dataset.sifra);
    vFav.setAttribute('aria-pressed', String(on));
    vFavText.textContent = on ? 'Spremljeno u odabir' : 'Spremi u odabir';
  }

  function openViewer(tile) {
    list = visible();
    if (!list.includes(tile)) list = tiles;
    show(list.indexOf(tile));
    if (!viewer.open) viewer.showModal();
    track('katalog_otvori', { motiv: tile.dataset.sifra });
  }

  viewer.querySelector('.prev').addEventListener('click', () => show(idx - 1));
  viewer.querySelector('.next').addEventListener('click', () => show(idx + 1));
  viewer.querySelector('.close').addEventListener('click', () => viewer.close());
  vFav.addEventListener('click', () => { const t = list[idx]; togglePick(t.dataset.sifra, t.querySelector('img').src); });
  vAsk.addEventListener('click', () => track('katalog_whatsapp_motiv', { motiv: list[idx].dataset.sifra }));
  viewer.addEventListener('close', () => { history.replaceState(null, '', location.pathname + location.search); });
  viewer.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
  });
  viewer.addEventListener('click', (e) => { if (e.target === viewer) viewer.close(); });

  // Povlačenje prstom
  const stage = viewer.querySelector('.stage');
  let x0 = null;
  stage.addEventListener('pointerdown', (e) => { x0 = e.clientX; });
  stage.addEventListener('pointerup', (e) => {
    if (x0 === null) return;
    const dx = e.clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
  });

  // Dijeljenje linka na motiv
  const share = viewer.querySelector('.share');
  if (share) share.addEventListener('click', async () => {
    const url = location.href;
    try {
      if (navigator.share) await navigator.share({ title: vCode.textContent, url });
      else { await navigator.clipboard.writeText(url); share.textContent = 'Link kopiran'; setTimeout(() => { share.textContent = 'Podijeli link na motiv'; }, 2000); }
    } catch (e) {}
  });

  // Otvori motiv iz linka (#BG-014)
  const fromHash = decodeURIComponent(location.hash.slice(1)).toUpperCase();
  if (fromHash) { const t = tiles.find((x) => x.dataset.sifra === fromHash); if (t) openViewer(t); }

  syncFavs();
})();

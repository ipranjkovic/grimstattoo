"""Generira stranice kataloga iz katalog/motivi.json.

Pokretanje (nakon katalog_slike.py):  python tools/katalog_stranice.py
"""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
K = ROOT / "katalog"
V = "?v=2"

KOLEKCIJE = {
    "black-and-grey": {
        "vol": "01", "naslov": "Black &amp; Grey", "naslov_txt": "Black & Grey",
        "opis": "Realistični crno-sivi motivi za veće površine: vikinzi, ratnici, mitologija, portreti, vjerski motivi, životinje i rukavi.",
        "format": "Veliki", "stil": "Realizam", "velicina": "", "ar": "4/5",
        "naslovna": ["BG-003"], "filteri": True,
        "seo": "Black and grey tattoo motivi: vikinzi, ratnici, mitologija, portreti, vjerski motivi i životinje. Katalog Grim’s Tattoo Studija u Vitezu.",
    },
    "skulls": {
        "vol": "02", "naslov": "Skulls", "naslov_txt": "Skulls",
        "opis": "Lubanje u baroknim ornamentima, dubokim sjenama i punom black and grey tonu. Veliki formati.",
        "format": "Veliki", "stil": "Ornamentalni", "velicina": "", "ar": "4/5",
        "naslovna": ["SK-026"], "filteri": False,
        "seo": "Black and grey tattoo motivi lubanja s baroknim ornamentima. Katalog Grim’s Tattoo Studija u Vitezu.",
    },
    "razni-motivi": {
        "vol": "03", "naslov": "Razni motivi", "naslov_txt": "Razni motivi",
        "opis": "Brodovi, svjetionici, kompasi, satovi, ruže, sove i portreti u mekoj olovci, uz valkire, šume i planine.",
        "format": "Srednji", "stil": "Olovka", "velicina": "srednji", "ar": "1/1",
        "naslovna": ["RM-003"], "filteri": True,
        "seo": "Tattoo motivi: brodovi, svjetionici, kompasi, satovi, ruže, sove, portreti, valkire i priroda. Katalog Grim’s Tattoo Studija u Vitezu.",
    },
    "peonies": {
        "vol": "04", "naslov": "Peonies", "naslov_txt": "Peonies",
        "opis": "Fini linijski božuri, pojedinačni cvjetovi i buketi. Manji formati koji se lako slažu uz druge motive.",
        "format": "Mali", "stil": "Fine line", "velicina": "mali", "ar": "1/1",
        "naslovna": ["PE-008"], "filteri": True,
        "seo": "Tattoo motivi božura u fine line stilu: pojedinačni cvjetovi i buketi. Katalog Grim’s Tattoo Studija u Vitezu.",
    },
    "arcanum": {
        "vol": "05", "naslov": "Arcanum", "naslov_txt": "Arcanum",
        "opis": "Motivi u stilu tarot karata: smrt, vrijeme i tihe figure uokvirene finom linijom. Manji formati, okomiti kadar.",
        "format": "Mali", "stil": "Tarot", "velicina": "uski", "ar": "9/16",
        "naslovna": ["AR-004", "AR-002"], "filteri": False,
        "seo": "Tattoo motivi u stilu tarot karata: smrt, vrijeme i figure u finoj liniji. Katalog Grim’s Tattoo Studija u Vitezu.",
    },
}
REDOSLIJED = list(KOLEKCIJE)

GTAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-SQT2XHML28"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-SQT2XHML28');</script>"""

HEART = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg>'
ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def motiv_word(n):
    return "motiv" if n % 10 == 1 and n % 100 != 11 else "motiva"


def head(title, desc, url, image):
    return f"""<!doctype html><html lang="hr"><head>{GTAG}<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#100f0d"><link rel="canonical" href="https://grimstattoo.com{url}"><meta property="og:title" content="{title}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="https://grimstattoo.com{url}"><meta property="og:type" content="website"><meta property="og:locale" content="hr_HR"><meta property="og:image" content="https://grimstattoo.com{image}"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Google+Sans+Flex:wght@400;500;600;700&amp;display=swap" rel="stylesheet"><link rel="stylesheet" href="/katalog/katalog.css{V}"><link rel="icon" type="image/svg+xml" href="/assets/grim-logo-for-the-bold.svg"></head>"""


HEADER = """<a class="skip" href="#main">Preskoči na sadržaj</a><header class="site-header wrap"><a class="brand" href="/">TATTOO STUDIO <span>BY GRIM</span></a><nav aria-label="Glavna navigacija"><a href="/#radovi">Radovi</a><a href="/katalog/" class="active" aria-current="page">Katalog</a><a href="/blog/">Blog</a><a class="nav-contact" href="/#termin">Dogovori termin</a></nav></header>"""

PICKS = f"""<aside class="picks" aria-label="Moj odabir" hidden><div class="picks-left"><div class="picks-thumbs"></div><div class="picks-text"><b>Moj odabir · <span class="picks-count"></span></b><button class="picks-clear" type="button">Očisti</button></div></div><a class="btn btn-primary picks-send" href="#" target="_blank" rel="noopener">Pošalji na WhatsApp</a></aside>"""

FOOTER = """<footer class="wrap"><div><a class="brand" href="/">TATTOO STUDIO <span>BY GRIM</span></a><p>Tattoo studio u Vitezu.<br>Vitez, Bosna i Hercegovina.</p></div><div class="footer-links"><a href="/">Studio</a><a href="/katalog/">Katalog</a><a href="/blog/">Blog</a><a href="https://www.instagram.com/grim.koji.tetovira/">Instagram</a></div></footer>"""


def img_path(kol, sifra, thumb=True):
    return f"/katalog/img/{kol}/{sifra.lower()}{'-t' if thumb else ''}.webp"


def kolekcija_stranica(kol, data):
    c = KOLEKCIJE[kol]
    teme = list(data.get("teme") or [])
    for m in data["motivi"]:
        if m["tema"] not in teme:
            teme.append(m["tema"])
    mot = sorted(data["motivi"], key=lambda m: teme.index(m["tema"]))
    by = {m["sifra"]: m for m in mot}
    n = len(mot)
    naslovna = "".join(
        f'<img src="{img_path(kol, s, False)}" alt="Naslovni motiv {s}" width="{by[s]["vw"]}" height="{by[s]["vh"]}" fetchpriority="high">'
        for s in c["naslovna"])
    filt = ""
    if c["filteri"]:
        btns = [f'<button type="button" data-filter="sve" aria-pressed="true">Svi<small>{n}</small></button>']
        for t in teme:
            k = sum(1 for m in mot if m["tema"] == t)
            label = "Buketi" if t == "Buket" else t
            btns.append(f'<button type="button" data-filter="{escape(t)}" aria-pressed="false">{escape(label)}<small>{k}</small></button>')
        filt = f'<div class="filters" role="group" aria-label="Filtriraj po temi" hidden>{"".join(btns)}</div>'
    else:
        filt = '<div></div>'
    tiles = []
    for i, m in enumerate(mot):
        s = m["sifra"]
        tema = m["tema"]
        alt = f"Tattoo motiv {s}" + (f", {tema.lower()}" if tema else "") + f" — {c['naslov_txt']}"
        lazy = 'loading="lazy" ' if i > 5 else ""
        tiles.append(
            f'<figure class="motiv" id="m-{s}" data-sifra="{s}" data-tema="{escape(tema)}" data-full="{img_path(kol, s, False)}">'
            f'<a class="motiv-open" href="{img_path(kol, s, False)}" aria-label="Otvori motiv {s}"><img src="{img_path(kol, s)}" alt="{escape(alt)}" width="{m["w"]}" height="{m["h"]}" {lazy}decoding="async"></a>'
            f'<button class="fav" type="button" data-sifra="{s}" data-thumb="{img_path(kol, s)}" aria-pressed="false" aria-label="Spremi {s} u odabir">{HEART}</button>'
            f'<figcaption><b>{s}</b><span>{escape(tema)}</span></figcaption></figure>')
    i = REDOSLIJED.index(kol)
    prev_k = REDOSLIJED[i - 1] if i > 0 else None
    next_k = REDOSLIJED[i + 1] if i + 1 < len(REDOSLIJED) else None
    prev_a = f'<a href="/katalog/{prev_k}/"><span>← Vol. {KOLEKCIJE[prev_k]["vol"]}</span><strong>{KOLEKCIJE[prev_k]["naslov"]}</strong></a>' if prev_k else '<a href="/katalog/"><span>← Katalog</span><strong>Sve kolekcije</strong></a>'
    next_a = f'<a href="/katalog/{next_k}/"><span>Vol. {KOLEKCIJE[next_k]["vol"]} →</span><strong>{KOLEKCIJE[next_k]["naslov"]}</strong></a>' if next_k else '<a href="/katalog/"><span>Katalog →</span><strong>Sve kolekcije</strong></a>'
    title = f"{c['naslov']} — katalog tattoo motiva | Grim’s Tattoo Studio"
    html = head(title, c["seo"], f"/katalog/{kol}/", img_path(kol, c["naslovna"][0], False))
    html += f'<body data-kolekcija="{escape(c["naslov_txt"])}">{HEADER}<main id="main" class="wrap">'
    html += f'<nav class="crumbs" aria-label="Putanja"><a href="/katalog/">Katalog</a><span aria-hidden="true">/</span><span>{c["naslov"]}</span></nav>'
    html += (f'<section class="hero"><div class="hero-copy"><div><p class="eyebrow">Vol. {c["vol"]} / {len(REDOSLIJED):02d}</p><h1>{c["naslov"]}</h1><p>{c["opis"]}</p></div>'
             f'<div><dl class="stats"><div><dt>Motiva</dt><dd>{n}</dd></div><div><dt>Format</dt><dd>{c["format"]}</dd></div><div><dt>Stil</dt><dd>{c["stil"]}</dd></div></dl>'
             f'<div class="hero-actions"><a class="btn btn-primary" href="#motivi">Listaj katalog</a><a class="btn btn-secondary" href="/katalog/">Sve kolekcije</a></div></div></div>'
             f'<div class="hero-art">{naslovna}</div></section>')
    html += (f'<section id="motivi" aria-label="Motivi"><div class="toolbar">{filt}<span class="count" role="status" aria-live="polite">{n} {motiv_word(n)}</span></div>'
             f'<div class="grid" data-size="{c["velicina"]}" style="--ar:{c["ar"]}">{"".join(tiles)}</div></section>')
    html += f'<nav class="next-vol" aria-label="Ostale kolekcije">{prev_a}{next_a}</nav></main>'
    html += VIEWER + PICKS + FOOTER + f'<script src="/katalog/katalog.js{V}" defer></script></body></html>'
    out = K / kol / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


VIEWER = f"""<dialog class="viewer" aria-label="Preglednik motiva"><div class="viewer-top"><span class="viewer-count"></span><button class="icon-btn close" type="button" aria-label="Zatvori preglednik"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div><div class="viewer-body"><div class="stage"><img src="" alt=""><button class="icon-btn prev" type="button" aria-label="Prethodni motiv"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button><button class="icon-btn next" type="button" aria-label="Sljedeći motiv"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button></div><div class="info"><div><span class="eyebrow">Motiv</span><h2></h2><div class="tags"><span class="tag-tema"></span></div><p>Svaki motiv prilagođavam veličini i položaju na tijelu. Detalje dogovaramo prije termina.</p></div><div class="info-actions"><a class="btn btn-primary ask" href="#" target="_blank" rel="noopener">Pitaj za ovaj motiv</a><button class="btn btn-secondary btn-fav" type="button" aria-pressed="false">{HEART}<span>Spremi u odabir</span></button><button class="share" type="button">Podijeli link na motiv</button></div></div></div></dialog>"""


def index_stranica(data):
    def thumbs(kol, sifre):
        by = {m["sifra"]: m for m in data[kol]["motivi"]}
        return "".join(f'<img src="{img_path(kol, s)}" alt="Motiv {s}" width="{by[s]["w"]}" height="{by[s]["h"]}" loading="lazy">' for s in sifre)

    def card(kol, cls, sifre):
        c = KOLEKCIJE[kol]
        n = len(data[kol]["motivi"])
        return (f'<a class="volume {cls}" href="/katalog/{kol}/"><div class="volume-art">{thumbs(kol, sifre)}</div>'
                f'<div class="volume-info"><div><span class="eyebrow">Vol. {c["vol"]} · {c["format"]} formati</span><h2>{c["naslov"]}</h2></div>'
                f'<div class="volume-meta"><span>{n} {motiv_word(n)}</span><span class="arrow-dot">{ARROW}</span></div></div></a>')

    desc = "Katalog tattoo motiva Grim’s Tattoo Studija: Black & Grey, Skulls, Razni motivi, Peonies i Arcanum. Listaj, spremi motive koji ti se sviđaju i pošalji upit na WhatsApp."
    html = head("Katalog tattoo motiva | Grim’s Tattoo Studio", desc, "/katalog/", img_path("black-and-grey", "BG-003", False))
    html += f'<body>{HEADER}<main id="main" class="wrap">'
    html += ('<section class="masthead"><div><p class="eyebrow">Grim’s Tattoo Studio / Katalog</p><h1>Katalog motiva.</h1></div>'
             '<p>Listaj gotove motive po kolekcijama, spremi one koji ti se sviđaju i pošalji mi odabir. Javit ću ti se s prijedlogom veličine i termina.</p></section>')
    html += ('<section class="volumes" aria-label="Kolekcije"><div class="volumes-row">'
             + card("black-and-grey", "volume-big", ["BG-003"])
             + card("skulls", "volume-big", ["SK-026"])
             + '</div><div class="volumes-row3">'
             + card("razni-motivi", "volume-small", ["RM-003", "RM-128", "RM-205"])
             + card("peonies", "volume-small", ["PE-001", "PE-030", "PE-008"])
             + card("arcanum", "volume-small", ["AR-004", "AR-002", "AR-024"])
             + '</div></section>')
    html += ('<section class="how" aria-label="Kako funkcionira">'
             '<div><b>01</b><h3>Listaj</h3><p>Otvori kolekciju i pregledaj motive. Svaki ima svoju šifru.</p></div>'
             '<div><b>02</b><h3>Spremi</h3><p>Klikni srce na motivima koji ti se sviđaju. Odabir se pamti dok listaš sve kataloge.</p></div>'
             '<div><b>03</b><h3>Pošalji</h3><p>Pošalji odabir na WhatsApp, a ja ti javim prijedlog veličine, cijenu i termin.</p></div></section>')
    html += '</main>' + PICKS + FOOTER + f'<script src="/katalog/katalog.js{V}" defer></script></body></html>'
    (K / "index.html").write_text(html, encoding="utf-8")


def main():
    data = json.loads((K / "motivi.json").read_text(encoding="utf-8"))
    for kol in REDOSLIJED:
        kolekcija_stranica(kol, data[kol])
    index_stranica(data)
    print("Gotovo.")


if __name__ == "__main__":
    main()

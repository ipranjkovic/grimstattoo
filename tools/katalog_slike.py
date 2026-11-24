"""Priprema slika za katalog motiva.

Uzima PNG-ove iz izvornog foldera (npr. "D:\\tattoo library\\000 za katalog"),
obrezuje bijeli rub i sprema WebP sličicu i veliku sliku u katalog/img/<kolekcija>/.
Popis motiva (šifra, tema, izvorna datoteka) je u katalog/motivi.json.

Pokretanje:  python tools/katalog_slike.py "<izvorni folder>"
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
VELICINE = {  # kolekcija: (sličica, velika) — dulja stranica u px
    "black-and-grey": (820, 1600),
    "skulls": (820, 1600),
    "razni-motivi": (640, 1400),
    "peonies": (560, 1200),
    "arcanum": (720, 1500),
}


def obrezi(im):
    rgb = Image.new("RGB", im.size, (255, 255, 255))
    im = im.convert("RGBA")
    rgb.paste(im, mask=im.split()[3])
    # Boja pozadine iz kutova; svijetlu (krem/sivu) pozadinu izbijeli
    w, h = rgb.size
    k = max(4, min(w, h) // 40)
    kutovi = [rgb.crop(b).resize((1, 1), Image.BOX).getpixel((0, 0)) for b in
              ((0, 0, k, k), (w - k, 0, w, k), (0, h - k, k, h), (w - k, h - k, w, h))]
    bg = tuple(sorted(c[i] for c in kutovi)[2] for i in range(3))
    if min(bg) > 170 and min(bg) < 252:
        rgb = Image.merge("RGB", [ch.point(lambda v, b=b: min(255, round(v * 255 / b))) for ch, b in zip(rgb.split(), bg)])
    maska = ImageOps.invert(rgb.convert("L")).point(lambda v: 255 if v > 24 else 0)
    bb = maska.getbbox() or (0, 0, *rgb.size)
    pad = int(max(rgb.size) * 0.035)
    bb = (max(0, bb[0] - pad), max(0, bb[1] - pad), min(rgb.width, bb[2] + pad), min(rgb.height, bb[3] + pad))
    return rgb.crop(bb)


def main(izvor):
    izvor = Path(izvor)
    motivi = json.loads((ROOT / "katalog" / "motivi.json").read_text(encoding="utf-8"))
    for kol, podaci in motivi.items():
        mala, velika = VELICINE[kol]
        out = ROOT / "katalog" / "img" / kol
        out.mkdir(parents=True, exist_ok=True)
        for m in podaci["motivi"]:
            dst_t = out / f"{m['sifra'].lower()}-t.webp"
            dst_v = out / f"{m['sifra'].lower()}.webp"
            if dst_t.exists() and dst_v.exists():
                continue
            img = obrezi(Image.open(izvor / m["izvor"]))
            v = img.copy(); v.thumbnail((velika, velika), Image.LANCZOS)
            v.save(dst_v, "WEBP", quality=80, method=6)
            t = img.copy(); t.thumbnail((mala, mala), Image.LANCZOS)
            t.save(dst_t, "WEBP", quality=78, method=6)
            m["w"], m["h"] = t.size
            m["vw"], m["vh"] = v.size
            print(m["sifra"], t.size, v.size)
    (ROOT / "katalog" / "motivi.json").write_text(json.dumps(motivi, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])

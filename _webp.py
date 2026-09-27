# -*- coding: utf-8 -*-
"""Bilder als WebP: erzeugt zu jedem JPG unter assets/ eine .webp-Datei (Qualitaet 82) und schreibt in allen
HTML-Seiten img-src und video-poster auf .webp um, wo die Datei existiert. Die JPGs bleiben liegen (Open-Graph-Bilder,
Fallback fuer alte Crawler). Laeuft nach _imgdim.py und _poster.py, vor _seo.py. Mehrfach ausfuehrbar."""
import glob
import os
import re

from PIL import Image

QUALITY = 82


def convert():
    made = 0
    for jpg in glob.glob("assets/**/*.jpg", recursive=True):
        webp = jpg[:-4] + ".webp"
        if os.path.exists(webp) and os.path.getmtime(webp) >= os.path.getmtime(jpg):
            continue
        try:
            im = Image.open(jpg)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.save(webp, "WEBP", quality=QUALITY, method=6)
            made += 1
        except Exception as e:
            print("  ! WebP fehlgeschlagen:", jpg, e)
    return made


def rewrite():
    n = 0
    for f in glob.glob("*.html"):
        h = open(f, encoding="utf-8").read()
        def sub(m):
            p = m.group(2)
            w = p[:-4] + ".webp"
            return m.group(1) + w + m.group(3) if os.path.exists(w) else m.group(0)
        h2 = re.sub(r'((?:src|poster)=")(assets/[^"]+\.jpg)(")', sub, h)
        if h2 != h:
            open(f, "w", encoding="utf-8").write(h2)
            n += 1
    return n


if __name__ == "__main__":
    print("WebP erzeugt: %d, Seiten umgeschrieben: %d" % (convert(), rewrite()))

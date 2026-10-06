# -*- coding: utf-8 -*-
"""Bilder als WebP: erzeugt zu jedem JPG unter assets/ eine .webp-Datei (Qualitaet 82) und schreibt in allen
HTML-Seiten img-src und video-poster auf .webp um, wo die Datei existiert. Die JPGs bleiben liegen (Open-Graph-Bilder,
Fallback fuer alte Crawler). Regel "webp" des Nachlaufs (_nachlauf.py): nach "headlines", vor "perf" und "seo".
seite() erzeugt fehlende oder veraltete WebP-Dateien der Seite gleich mit, convert() alle unter assets/.
Mehrfach ausfuehrbar. Einzeln aufrufbar (alle Seiten): python3 _webp.py"""
import glob
import os
import re

from PIL import Image

QUALITY = 82
ZAEHLER = {"erzeugt": 0, "seiten": 0}


def _ohne_webp(jpg):
    # Open-Graph-Bilder (_seo.py) bleiben JPG, eine WebP-Fassung braucht dort niemand
    return jpg.startswith(("assets/img/og/", "assets/img/og-default"))


def _erzeuge(jpg):
    """WebP zu jpg schreiben, wenn sie fehlt oder aelter ist. True, wenn neu geschrieben."""
    webp = jpg[:-4] + ".webp"
    if os.path.exists(webp) and os.path.getmtime(webp) >= os.path.getmtime(jpg):
        return False
    try:
        im = Image.open(jpg)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        im.save(webp, "WEBP", quality=QUALITY, method=6)
        ZAEHLER["erzeugt"] += 1
        return True
    except Exception as e:
        print("  ! WebP fehlgeschlagen:", jpg, e)
        return False


def convert():
    made = 0
    for jpg in glob.glob("assets/**/*.jpg", recursive=True):
        if _ohne_webp(jpg):
            continue
        if _erzeuge(jpg):
            made += 1
    return made


def seite(f, h):
    """Regel "webp": src und poster auf .webp, wo es die Datei gibt (fehlende werden zuerst erzeugt)."""
    def sub(m):
        p = m.group(2)
        w = p[:-4] + ".webp"
        if not _ohne_webp(p) and os.path.exists(p):
            _erzeuge(p)
        return m.group(1) + w + m.group(3) if os.path.exists(w) else m.group(0)
    h2 = re.sub(r'((?:src|poster)=")(assets/[^"]+\.jpg)(")', sub, h)
    if h2 != h:
        ZAEHLER["seiten"] += 1
    return h2


def bericht():
    return "WebP erzeugt: %d, Seiten umgeschrieben: %d" % (ZAEHLER["erzeugt"], ZAEHLER["seiten"])


if __name__ == "__main__":
    import _nachlauf
    convert()
    _nachlauf.einzeln(seite)
    print(bericht())

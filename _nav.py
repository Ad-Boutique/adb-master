# -*- coding: utf-8 -*-
"""Kopfzeile, Kontakt-Kreis und Menuepunkte auf allen Seiten gleich setzen (Feedback 15.10.2026, wie _footer.py fuer den Footer).
Quelle ist _gen.py (HEADER, MBTN, MENU_ITEMS), damit generierte und handgepflegte Seiten (index, work, agentur,
case-premium-neubau, case-kommunalkredit) dasselbe Markup tragen. Mehrfach ausfuehrbar, schreibt nur bei Aenderung.
Reihenfolge im Build: nach _footer.py, vor _perf.py (das die Menuebilder auf data-src stellt)."""
import glob
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))
import _gen as g

SKIP = ("_qa_template.html",)
HEADER_RX = re.compile(r'<header class="chrome">.*?</header>\n', re.S)
# alter Menue-Knopf samt Umlaufbahn, oder schon der neue Link
MBTN_RX = re.compile(r'(?:<button class="mbtn"[^>]*></button>\n<svg class="morbit".*?</svg>\n|<a class="mbtn"[^>]*></a>\n)', re.S)
ROW_RX = re.compile(r'(<nav class="msheet"[^>]*>\n  <div class="mrow">\n).*?(\n  </div>\n  <div class="mfoot">)', re.S)


def active(f):
    if f == "kontakt.html":
        return "kontakt.html"
    if f == "agentur.html":
        return "agentur.html"
    if f == "work.html" or f.startswith("case-"):
        return "work.html"
    if f.startswith("service-"):
        return "index.html#leistungen"
    return ""


def rows(act):
    out = []
    for href, label, mv in g.MENU_ITEMS:
        a = " act" if href == act else ""
        out.append('    <a class="mitem%s" href="%s">\n      <span class="mt">%s</span>\n      <span class="mthumb">%s</span>\n    </a>' % (a, href, label, mv))
    return "\n".join(out)


def main():
    n = 0
    for f in sorted(glob.glob("*.html")):
        if f in SKIP:
            continue
        h = open(f, encoding="utf-8").read()
        if 'class="msheet"' not in h:
            continue
        hdr = g.HEADER
        act = active(f)
        if act:
            hdr = hdr.replace('href="%s">' % act, 'href="%s" aria-current="page">' % act, 1)
        out = HEADER_RX.sub(lambda m: hdr, h, count=1)
        out = MBTN_RX.sub(lambda m: g.MBTN + "\n", out, count=1)
        out = ROW_RX.sub(lambda m: m.group(1) + rows(active(f)) + m.group(2), out, count=1)
        if hdr not in out or g.MBTN not in out:
            print("  ! %s: Kopfzeile oder Kontakt-Kreis nicht gesetzt" % f)
        if out != h:
            open(f, "w", encoding="utf-8").write(out)
            n += 1
    print("Navigation in %d Seiten gesetzt" % n)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Buendelt die Quell-Stylesheets und -Scripts zu je einer Datei, die alle Seiten laden:
assets/site.css (tokens.css, master.css, brand.css, brand-type/-ui/-layout/-motion/-keep.css in dieser festen Reihenfolge)
und assets/site.js (brand.js, dann master.js, jede Datei in eigenem Block).

site.css und site.js werden erzeugt, nie direkt bearbeiten. Bearbeitet werden die Einzeldateien, Werte in tokens.css.
Das Kuerzen ist bewusst vorsichtig: Kommentare fallen weg, Leerraum wird zusammengezogen, Leerzeichen nur an
{ } ; , und nach : entfernt. Strings und url(...) bleiben unberuehrt, die Reihenfolge der Regeln (Kaskade) bleibt gleich.
Leerzeichen vor : bleiben stehen (".a :is(.b)" ist ein Nachfahren-Selektor). Mehrfach ausfuehrbar: schreibt nur bei Aenderung.
Reihenfolge im Build (_build.sh): vor _brand_inplace.py."""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CSS = ("tokens.css", "master.css", "brand.css", "brand-type.css", "brand-ui.css",
       "brand-layout.css", "brand-motion.css", "brand-keep.css")
JS = ("brand.js", "master.js")
HEAD_CSS = "/* site.css: erzeugt von _css.py aus %s. Nicht bearbeiten, Quellen in assets/ aendern, Werte in tokens.css. */\n"
HEAD_JS = "/* site.js: erzeugt von _css.py aus %s. Nicht bearbeiten, Quellen in assets/ aendern. */\n"
TIGHT = "{};,"   # um diese Zeichen darf Leerraum ganz weg
WORD = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_%.#)")


def minify(css):
    """Kommentare raus, Leerraum zusammenziehen. Strings, url() und alles andere bleiben Zeichen fuer Zeichen."""
    out = []
    i, n = 0, len(css)
    pend = False            # steht Leerraum an (wird erst beim naechsten Zeichen entschieden)

    def last():
        return out[-1][-1] if out and out[-1] else ""

    def emit(tok):
        nonlocal pend
        if pend:
            prev = last()
            if prev and prev not in TIGHT and prev != ":" and tok[0] not in TIGHT:
                out.append(" ")
            pend = False
        out.append(tok)

    while i < n:
        c = css[i]
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            if j < 0:
                raise SystemExit("_css.py: offener Kommentar")
            i = j + 2
            # ein Kommentar zwischen zwei Wortzeichen trennt sie; sonst verschwindet er spurlos
            if last() in WORD and i < n and css[i] in WORD:
                pend = True
            continue
        if c in " \t\r\n\f":
            pend = True
            i += 1
            continue
        if c in "\"'":
            j = i + 1
            while j < n and css[j] != c:
                if css[j] == "\\":
                    j += 1
                elif css[j] == "\n":
                    raise SystemExit("_css.py: offener String")
                j += 1
            emit(css[i:j + 1])
            i = j + 1
            continue
        if css.startswith("url(", i) and (i == 0 or not (css[i - 1].isalnum() or css[i - 1] in "-_")):
            j = css.find(")", i)
            emit(css[i:j + 1])
            i = j + 1
            continue
        if c in TIGHT:
            pend = False
            if c == "}" and last() == ";":
                out[-1] = out[-1][:-1]   # letztes Semikolon vor } ist ueberfluessig
            out.append(c)
            i += 1
            continue
        if c == ":":
            emit(c)
            pend = False
            i += 1
            # Leerraum nach : faellt weg (prop: wert, @media (x: y))
            while i < n and css[i] in " \t\r\n\f":
                i += 1
            continue
        emit(c)
        i += 1
    return "".join(out).strip() + "\n"


def write(path, text):
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != text:
        open(path, "w", encoding="utf-8").write(text)
        return True
    return False


def main():
    src = [open(os.path.join("assets", f), encoding="utf-8").read() for f in CSS]
    css = HEAD_CSS % ", ".join(CSS) + "".join(minify(s) for s in src)
    js_parts = []
    for f in JS:
        body = open(os.path.join("assets", f), encoding="utf-8").read().rstrip()
        # eigener Block je Datei; das Semikolon schuetzt vor einem fehlenden Abschluss der vorigen Datei
        js_parts.append("/* ---------- %s ---------- */\n;{\n%s\n}\n" % (f, body))
    js = HEAD_JS % ", ".join(JS) + "".join(js_parts)
    a = write(os.path.join("assets", "site.css"), css)
    b = write(os.path.join("assets", "site.js"), js)
    print("site.css %d Zeichen (Quellen %d)%s, site.js %d Zeichen%s" % (
        len(css), sum(len(s) for s in src), " neu" if a else "", len(js), " neu" if b else ""))


if __name__ == "__main__":
    main()

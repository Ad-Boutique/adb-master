# -*- coding: utf-8 -*-
"""Brand 2026 fuer handgebaute Seiten: Adobe-Fonts-Kit, brand.css und brand.js in den Kopf,
Seitenklasse, dazu auf Startseite und Agentur die Bausteine (Kapitel-Leiste, Punkt, Punktzeile,
Akt-Ringe, Punkt-Zoom). Mehrfach ausfuehrbar: was da ist, wird nicht doppelt eingesetzt.
Reihenfolge: nach den Generatoren, vor _bump.py."""
import glob
import re

SKIP = ("_qa_template.html",)


def head(h):
    if "brand.css" in h:
        return h
    m = re.search(r'<link rel="stylesheet" href="assets/master\.css\?v=(\d+)">', h)
    if not m:
        return h
    v = m.group(1)
    h = h.replace(m.group(0), m.group(0) + '\n<link rel="stylesheet" href="https://use.typekit.net/udf8wjj.css">\n<link rel="stylesheet" href="assets/brand.css?v=%s">' % v, 1)
    h = h.replace('<script src="assets/master.js?v=%s" defer></script>' % v,
                  '<script src="assets/brand.js?v=%s" defer></script>\n<script src="assets/master.js?v=%s" defer></script>' % (v, v), 1)
    h = re.sub(r"<body([^>]*)>", lambda mm: ("<body%s class=\"brand\">" % mm.group(1)) if "class=" not in mm.group(1) else ("<body%s>" % mm.group(1).replace('class="', 'class="brand ')), h, count=1)
    return h


def rep(h, old, new, what):
    assert h.count(old) == 1, "%s: %d Treffer fuer %r" % (what, h.count(old), old[:60])
    return h.replace(old, new)


def index(h):
    if 'class="chapnav"' in h:
        return h
    h = rep(h, '<span class="rl"><span>Kein Zufall.</span></span>', '<span class="rl"><span><i>Kein Zufall.</i></span></span>', "Hero-Zeile")
    h = rep(h, '<div class="hpitch">\n      <span class="label">', '<div class="hpitch">\n      <span class="bdot" aria-hidden="true"></span>\n      <span class="label">', "Hero-Punkt")
    h = rep(h, '<section class="sec fg-light stats bg-paper"', '<section class="sec fg-light stats bg-paper dotzoom dotzoom--dark"', "Punkt-Zoom Zahlen")
    h = rep(h, "<main>", '''<main class="apl">

  <!-- KAPITEL-LEISTE -->
  <nav class="chapnav" aria-label="Kapitel">
    <span class="cn-title">ad.boutique</span>
    <a href="#work">Work</a>
    <a href="#leistungen">Leistungen</a>
    <a href="#team">Team</a>
    <a class="cn-cta" href="#kontakt">Kontakt</a>
  </nav>
''', "main")
    h = rep(h, '  <!-- 04, WORK-TEASER -->\n  <section class="sec fg-light bg-paper"', '  <!-- 04, WORK-TEASER -->\n  <section id="work" class="sec fg-light bg-paper"', "Work-ID")
    h = rep(h, '<section class="sec fg-light team-int bg-paper"', '<section id="team" class="sec fg-light team-int bg-paper"', "Team-ID")
    h = rep(h, 'Wir gewinnen nur, wenn Sie gewinnen.</p>\n      <div class="hbtns"',
            'Wir gewinnen nur, wenn Sie gewinnen.</p>\n      <div class="dotline" data-fade style="--i:1"><span>strategie</span><span>creative</span><span>digital</span><span>growth</span></div>\n      <div class="hbtns"', "Punktzeile")
    h = rep(h, '<span class="label">Wofür wir stehen</span>', '<div class="actring" aria-hidden="true"></div>\n      <span class="label">Wofür wir stehen</span>', "Ring These")
    h = rep(h, '<span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(30px,4vw,54px)">Reden wir</span>',
            '<div class="actring" aria-hidden="true"></div>\n      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(30px,4vw,54px)">Reden wir</span>', "Ring Kontakt")
    return h


def agentur(h):
    if 'class="chapnav"' in h:
        return h
    h = rep(h, "<main>", '''<main class="apl">

  <!-- KAPITEL-LEISTE -->
  <nav class="chapnav" aria-label="Kapitel">
    <span class="cn-title">Agentur</span>
    <a href="#zahlen">Zahlen</a>
    <a href="#koennen">Können</a>
    <a href="#team">Team</a>
    <a href="#jobs">Mitarbeiten</a>
    <a class="cn-cta" href="kontakt.html">Kontakt</a>
  </nav>
''', "main")
    h = rep(h, '<section class="sec fg-light stats bg-paper"', '<section id="zahlen" class="sec fg-light stats bg-paper"', "Zahlen-ID")
    h = rep(h, '  <!-- 03, CAPABILITIES (Creme) -->\n  <section class="sec fg-light bg-cream"', '  <!-- 03, CAPABILITIES (Creme) -->\n  <section id="koennen" class="dotzoom sec fg-light bg-cream"', "Koennen-ID")
    h = rep(h, '<section class="sec fg-light ateam bg-paper"', '<section id="team" class="sec fg-light ateam bg-paper"', "Team-ID")
    h = rep(h, '  <!-- 05, JOIN / WORK (Vorlage: Join us, Work with us) -->\n  <section class="sec fg-light bg-paper"', '  <!-- 05, JOIN / WORK (Vorlage: Join us, Work with us) -->\n  <section id="jobs" class="sec fg-light bg-paper"', "Jobs-ID")
    h = rep(h, '<h1 class="dispn" data-lines>\n        <span class="rl"><span>Wir bauen Marken und Kampagnen</span></span>',
            '<span class="bdot" aria-hidden="true"></span>\n      <h1 class="dispn" data-lines>\n        <span class="rl"><span>Wir bauen Marken und Kampagnen</span></span>', "Hero-Punkt")
    h = rep(h, '<span class="rl"><span>auf Zahlen gebaut sind.</span></span>', '<span class="rl"><span><i>auf Zahlen gebaut sind.</i></span></span>', "Hero-Kursiv")
    h = rep(h, '<a class="alink" href="work.html" data-fade style="margin-top:30px">Die Beweise ansehen →</a>',
            '<div class="dotline" data-fade style="justify-content:flex-start;margin-top:22px"><span>strategen</span><span>kreative</span><span>performance-nerds</span></div>\n      <a class="alink" href="work.html" data-fade style="margin-top:30px">Die Beweise ansehen →</a>', "Punktzeile")
    h = rep(h, '<div><span class="label" style="color:var(--grey-dark)">Was wir können</span></div>',
            '<div><div class="actring" aria-hidden="true"></div><span class="label" style="color:var(--grey-dark)">Was wir können</span></div>', "Ring Koennen")
    h = rep(h, '<h2 class="dispn" data-lines>\n        <span class="rl"><span>Ein Team aus Strategen, Kreativen</span></span>',
            '<div class="actring" aria-hidden="true" style="margin:0 auto 26px"></div>\n      <h2 class="dispn" data-lines>\n        <span class="rl"><span>Ein Team aus Strategen, Kreativen</span></span>', "Ring Team")
    return h


def main():
    n = 0
    for f in sorted(glob.glob("*.html")):
        if f in SKIP or f.endswith("-brand.html"):
            continue
        h = open(f, encoding="utf-8").read()
        out = head(h)
        if f == "index.html":
            out = index(out)
        elif f == "agentur.html":
            out = agentur(out)
        if out != h:
            open(f, "w", encoding="utf-8").write(out)
            n += 1
    print("Brand in %d Seiten eingesetzt" % n)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Brand-2026-Testseiten: Startseite und Performance-Seite im neuen Design.
Ableitung aus den bestehenden Seiten: Adobe-Fonts-Kit, brand.css und brand.js eingebunden,
Hintergruende auf die neue Palette gemappt, Kontakt und Anfrage auf Lime, Punkt im Hero,
Punkt-Graphen im Beweisteil der Leistungsseite."""
import re

BG = {"#F3EDE1": "#f4f3ec", "#EFE7D6": "#e9e8df", "#0A0A0A": "#0f0f0f", "#0E0E10": "#0f0f0f",
      "#070708": "#0f0f0f", "#08080A": "#0f0f0f", "#060607": "#0f0f0f"}


def common(h, title):
    v = re.search(r'master\.css\?v=(\d+)', h).group(1)
    h = re.sub(r"<title>(.*?)</title>", "<title>Brand-Test, " + title + "</title>", h, count=1, flags=re.S)
    h = h.replace('<link rel="stylesheet" href="assets/master.css?v=%s">' % v,
                  '<link rel="stylesheet" href="assets/master.css?v=%s">\n<link rel="stylesheet" href="https://use.typekit.net/udf8wjj.css">\n<link rel="stylesheet" href="assets/brand.css?v=%s">' % (v, v), 1)
    h = h.replace('<script src="assets/master.js?v=%s" defer></script>' % v,
                  '<script src="assets/brand.js?v=%s" defer></script>\n<script src="assets/master.js?v=%s" defer></script>' % (v, v), 1)
    assert h.count("brand.css") == 1 and h.count("brand.js") == 1, "Einbindung fehlt"
    h = re.sub(r"<body([^>]*)>", lambda m: "<body%s class=\"brand\">" % m.group(1) if "class=" not in m.group(1) else "<body%s>" % m.group(1).replace('class="', 'class="brand '), h, count=1)
    for a, b in BG.items():
        h = h.replace('data-bg="%s"' % a, 'data-bg="%s"' % b).replace("background:%s" % a, "background:%s" % b).replace("background: %s" % a, "background: %s" % b)
    return h


def index():
    h = open("index.html", encoding="utf-8").read()
    h = common(h, "ad.boutique 2026")
    # Zweite Hero-Zeile als kursive Serife, der Punkt als Aufmerksamkeit
    old = '<span class="rl"><span>Kein Zufall.</span></span>'
    assert h.count(old) == 1
    h = h.replace(old, '<span class="rl"><span><i>Kein Zufall.</i></span></span>')
    old2 = '<div class="hpitch">\n      <span class="label">'
    assert h.count(old2) == 1
    h = h.replace(old2, '<div class="hpitch">\n      <span class="bdot" aria-hidden="true"></span>\n      <span class="label">')
    old3 = '<section class="sec fg-light stats bg-paper"'
    assert h.count(old3) == 1
    h = h.replace(old3, '<section class="sec fg-light stats bg-paper dotzoom dotzoom--dark"')
    open("index-brand.html", "w", encoding="utf-8").write(h)
    print("index-brand.html", len(h))


def service():
    h = open("service-performance-marketing.html", encoding="utf-8").read()
    h = common(h, "Performance Marketing, ad.boutique 2026")
    old0 = '<section id="problem" class="sec fg-dark kapsec kapsec--dark"' if 'id="problem"' in h else '<section class="sec fg-dark kapsec kapsec--dark"'
    assert h.count(old0) == 1, "Ausgangslage nicht gefunden"
    h = h.replace(old0, old0.replace('class="sec', 'class="dotzoom sec'))
    # Punkt statt Glyph im Hero
    old = '<div class="svc-glyph" data-fade></div>'
    assert h.count(old) == 1
    h = h.replace(old, '<div class="svc-glyph" data-fade></div><span class="bdot" aria-hidden="true" data-fade></span>')
    # Arbeitsweise als Punktzeile unter dem Hero-Text, Sprache des Boards: "strategie. creative. digital. growth."
    old_sub = 'Mit Attribution, der Sie trauen können.</p>'
    assert h.count(old_sub) == 1
    h = h.replace(old_sub, old_sub + '\n      <div class="dotline" data-fade style="--i:1"><span>testen</span><span>messen</span><span>umschichten</span><span>berichten</span></div>')
    # Die alte Balkengrafik unter dem Beweis-Kopf faellt weg, die Punkt-Graphen zeigen dieselben Zahlen
    h = re.sub(r'      <div class="proofone">.*?      </div>\n      </div>\n', '', h, count=1, flags=re.S)
    assert "proofone" not in h, "proofone noch da"
    # Akt-Marken: die gepunktete Ringform vor den Kapitelanfaengen
    for anchor in ['<span class="label" style="color:var(--champ);display:block;margin-bottom:16px">Die Ausgangslage</span>',
                   '<span class="label" style="color:var(--champ-deep);display:block;text-align:center">Ergebnisse</span>',
                   '<span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(16px,1.8vw,24px)">Bevor wir starten</span>']:
        assert h.count(anchor) == 1, anchor[:60]
        center = ' style="margin:0 auto 26px"' if "text-align:center" in anchor else ""
        h = h.replace(anchor, '<div class="pring" aria-hidden="true"%s></div>\n          ' % center + anchor)
    # Punkt-Graphen vor den Cases: jede Anfrage ein Punkt, jeder Euro zwei Punkte
    sec = '''  <!-- PUNKT-GRAPHEN: jede Einheit ein Punkt -->
  <section class="sec fg-light bg-paper dotsec" data-bg="#f4f3ec" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Punkt für Punkt</span>
        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)"><span class="rl"><span>Ein Motiv,</span></span><span class="rl"><span><i>54 von 100 Anfragen.</i></span></span></h2>
        <p class="lt3" data-fade style="margin-top:22px">Vier Motive liefen gegeneinander. Jeder Punkt ist ein Prozent der 489 Anfragen, die Lime-Punkte kamen aus dem einen Interior-Motiv.</p>
      </div>
      <div>
        <div class="dotgraph" data-total="100" data-value="54" style="--cols:10" aria-label="54 von 100 Punkten"></div>
        <div class="dotcap" data-fade><span class="dv">54 %</span><span class="dl">aller Anfragen aus einem einzigen Motiv, 262 von 489</span></div>
        <div class="dotbars" data-fade>
          <div class="row"><span class="rl">Instant Form, Eigennutzer</span><span class="dots" data-n="30" data-on="5"></span><span class="rv">€ 9,59</span></div>
          <div class="row"><span class="rl">Instant Form, Anleger</span><span class="dots" data-n="30" data-on="4"></span><span class="rv">€ 8,43</span></div>
          <div class="row hi"><span class="rl">Website-Formular</span><span class="dots" data-n="30" data-on="29"></span><span class="rv">€ 58,05</span></div>
        </div>
        <p class="dotnote" data-fade>Ein Punkt sind zwei Euro je Anfrage. Dieselbe Zielgruppe, dieselbe Woche: Die Strecke entscheidet über den Preis.</p>
      </div>
    </div>
  </section>

'''
    mark = "  <!-- 07, CASES -->"
    assert h.count(mark) == 1
    h = h.replace(mark, sec + mark)
    open("service-performance-marketing-brand.html", "w", encoding="utf-8").write(h)
    print("service-performance-marketing-brand.html", len(h))


if __name__ == "__main__":
    index()
    service()

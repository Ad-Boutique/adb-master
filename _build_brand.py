# -*- coding: utf-8 -*-
"""Brand-2026-Testseiten aus den bestehenden Seiten: Startseite und zwei Leistungsseiten.
Gemeinsam: Adobe-Fonts-Kit, brand.css und brand.js, Hintergruende auf die neue Palette, Seitenklasse apl.
Leistungsseiten: Punkt im Hero, Punktzeile, Kapitel-Leiste, Akt-Ringe, Punkt-Zoom auf der Ausgangslage,
Punkt-Graphen im Beweisteil, Punktfeld im Hero (ChatGPT). Nach jedem Generatorlauf neu ausfuehren."""
import re

BG = {"#F3EDE1": "#f4f3ec", "#EFE7D6": "#e9e8df", "#0A0A0A": "#0f0f0f", "#0E0E10": "#0f0f0f",
      "#070708": "#0f0f0f", "#08080A": "#0f0f0f", "#060607": "#0f0f0f"}

LABEL = '<span class="label" style="color:%s;display:block;%s">%s</span>'


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


def rep(h, old, new, what):
    assert h.count(old) == 1, "%s: %d Treffer fuer %r" % (what, h.count(old), old[:70])
    return h.replace(old, new)


def index():
    h = open("index.html", encoding="utf-8").read()
    h = common(h, "ad.boutique 2026")
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
    # Punkte unter den Zahlen: auf Kundenwunsch weggelassen, die Zahl steht allein
    open("index-brand.html", "w", encoding="utf-8").write(h)
    print("index-brand.html", len(h))


SERVICES = {
 "service-performance-marketing": dict(
   title="Performance Marketing, ad.boutique 2026",
   chap_title="Performance Marketing",
   dotline=["testen", "messen", "umschichten", "berichten"],
   sub_anchor="Mit Attribution, der Sie trauen können.</p>",
   rings=[LABEL % ("var(--champ)", "margin-bottom:16px", "Die Ausgangslage"),
          LABEL % ("var(--champ-deep)", "text-align:center", "Ergebnisse"),
          LABEL % ("var(--champ-deep)", "margin-bottom:clamp(16px,1.8vw,24px)", "Bevor wir starten")],
   drop_proofone=True,
   dotfield='''      <div class="dotfield-wrap" data-fade style="--i:3">
        <canvas class="dotfield" data-total="489" data-lime="262" data-form="262" aria-label="489 Punkte, 262 davon in Lime"></canvas>
        <p class="dotfield-cap"><b>489 Anfragen</b> für ein Neubauprojekt in Wien aus € 5.755 Mediabudget, <b>262 davon aus einem einzigen Motiv</b>. Jeder Punkt eine Anfrage.<span class="dothint">Antippen</span></p>
      </div>
''',
   tline='''      <div class="tline" data-fade>
        <div class="tldots" data-seg="h1 b1 t4 e1" aria-label="Sieben Schritte als Punkte"></div>
        <div class="tllegend"><span><i class="tl-h"></i>Heute: Anfrage</span><span><i class="tl-b"></i>Unter 24 h: Ersteinschätzung</span><span><i class="tl-t"></i>Tag 2 bis 5: Audit im Konto</span><span><i class="tl-e"></i>Danach: klare Empfehlung</span></div>
      </div>
''',
   graph='''  <!-- PUNKT-GRAPHEN: jede Einheit ein Punkt -->
  <section class="sec fg-light bg-paper dotsec" data-bg="#f4f3ec" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Punkt für Punkt</span>
        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)"><span class="rl"><span>Die Strecke</span></span><span class="rl"><span><i>entscheidet, in Punkten.</i></span></span></h2>
        <p class="lt3" data-fade style="margin-top:22px">Zwei Fälle aus dem Reporting. Dieselbe Zielgruppe, dieselbe Woche, drei Strecken: Der Preis je Anfrage hängt am Weg, nicht am Budget. Und eine Plattform, die mit gleichem Geld das Dreifache holte.</p>
      </div>
      <div>
        <div class="dotbars" data-fade style="margin-top:0">
          <div class="row"><span class="rl">Instant Form, Eigennutzer</span><span class="dots" data-n="30" data-on="5"></span><span class="rv">€ 9,59</span></div>
          <div class="row"><span class="rl">Instant Form, Anleger</span><span class="dots" data-n="30" data-on="4"></span><span class="rv">€ 8,43</span></div>
          <div class="row hi"><span class="rl">Website-Formular</span><span class="dots" data-n="30" data-on="29"></span><span class="rv">€ 58,05</span></div>
        </div>
        <p class="dotnote" data-fade>Wohnbau-Projekt, ein Punkt sind zwei Euro je Anfrage.</p>
        <div class="dotbars" data-fade>
          <div class="row"><span class="rl">Investments vorher</span><span class="dots" data-n="50" data-on="16"></span><span class="rv">16</span></div>
          <div class="row hi"><span class="rl">Investments mit uns</span><span class="dots" data-n="50" data-on="50"></span><span class="rv">50</span></div>
        </div>
        <p class="dotnote" data-fade>Crowdinvesting-Plattform, gleiches Budget, ein Punkt ein Investment. ROAS 8,75 statt 2,14.</p>
      </div>
    </div>
  </section>

''',
   chap=[("Problem", "problem", "  <!-- AKT 1: DAS PROBLEM -->\n  <section class=\"dotzoom sec fg-dark kapsec kapsec--dark\""),
         ("Nutzen", "nutzen", "  <!-- AKT 1: THESE UND NUTZEN -->\n  <section class=\"sec fg-light bg-cream\""),
         ("Beweis", "beweis", "  <!-- 06, PROOF 2: ERGEBNISSE -->\n  <section class=\"sec fg-light bg-paper\""),
         ("Cases", "cases", "  <!-- 07, CASES -->\n  <section class=\"sec fg-light bg-cream\"")]),

 "service-chatgpt-ads": dict(
   title="ChatGPT Ads, ad.boutique 2026",
   chap_title="ChatGPT Ads",
   dotline=["prüfen", "schreiben", "bauen", "lesen"],
   sub_anchor="Das ist Ihr Vorteil, wenn Sie jetzt starten.</p>",
   rings=[LABEL % ("var(--champ)", "margin-bottom:16px", "Die Ausgangslage"),
          LABEL % ("var(--champ-deep)", "text-align:center", "Woher wir das wissen"),
          LABEL % ("var(--champ-deep)", "margin-bottom:clamp(16px,1.8vw,24px)", "Bevor wir starten")],
   drop_proofone=False,
   # Punktfeld im Hero: 489 Anfragen fuer ein Neubauprojekt, 262 aus einem einzigen Satz (Case Premium-Neubau)
   dotfield='''      <div class="dotfield-wrap" data-fade style="--i:3">
        <canvas class="dotfield" data-total="489" data-lime="262" data-form="262" aria-label="489 Punkte, 262 davon in Lime"></canvas>
        <p class="dotfield-cap"><b>489 Anfragen</b> für ein Neubauprojekt in Wien, <b>262 davon aus einem einzigen Satz</b>. Der Satz entscheidet, im Feed wie in der Antwort. Jeder Punkt eine Anfrage.<span class="dothint">Antippen</span></p>
      </div>
''',
   graph='''  <!-- PUNKT-GRAPHEN: jede Einheit ein Punkt -->
  <section class="sec fg-light bg-paper dotsec" data-bg="#f4f3ec" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Punkt für Punkt</span>
        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)"><span class="rl"><span>Relevanz,</span></span><span class="rl"><span><i>in Punkten gezählt.</i></span></span></h2>
        <p class="lt3" data-fade style="margin-top:22px">Zwei Marken, zwei Zahlen aus dem Reporting. Was in der Antwort zählt, hat dort schon gezählt: die richtige Botschaft im richtigen Moment, nicht mehr Budget.</p>
      </div>
      <div>
        <div class="dotbars" data-fade style="margin-top:0">
          <div class="row"><span class="rl">Jahresumsatz vorher</span><span class="dots" data-n="42" data-on="26"></span><span class="rv">€ 520k</span></div>
          <div class="row hi"><span class="rl">Jahresumsatz mit uns</span><span class="dots" data-n="42" data-on="41"></span><span class="rv">€ 817k</span></div>
        </div>
        <p class="dotnote" data-fade>D2C-Lifestyle-Marke, ein Punkt sind € 20.000. Plus 57 Prozent im besten Jahr der Firma, Blended ROAS 5,57.</p>
        <div class="dotbars" data-fade>
          <div class="row"><span class="rl">Benchmark Black Friday</span><span class="dots" data-n="42" data-on="23"></span><span class="rv">2,3</span></div>
          <div class="row hi"><span class="rl">Mit uns</span><span class="dots" data-n="42" data-on="40"></span><span class="rv">4,02</span></div>
        </div>
        <p class="dotnote" data-fade>Premium-Consumer-Brand, ein Punkt sind 0,1 ROAS. 75 Prozent über der Benchmark in der lautesten Woche des Jahres.</p>
        <div class="dotbars" data-fade>
          <div class="row"><span class="rl">Investments vorher</span><span class="dots" data-n="50" data-on="16"></span><span class="rv">16</span></div>
          <div class="row hi"><span class="rl">Investments mit uns</span><span class="dots" data-n="50" data-on="50"></span><span class="rv">50</span></div>
        </div>
        <p class="dotnote" data-fade>Crowdinvesting-Plattform, gleiches Budget, ein Punkt ein Investment. ROAS 8,75 statt 2,14: Struktur statt mehr Geld.</p>
      </div>
    </div>
  </section>

''',
   chap=[("Problem", "problem", "  <!-- AKT 1: DAS PROBLEM -->\n  <section class=\"dotzoom sec fg-dark kapsec kapsec--dark\""),
         ("Nutzen", "nutzen", "  <!-- AKT 1: THESE UND NUTZEN -->\n  <section class=\"sec fg-light bg-cream\""),
         ("Beweis", "beweis", "  <!-- 06, PROOF 2: ERGEBNISSE -->\n  <section class=\"sec fg-light bg-paper\""),
         ("Cases", "cases", "  <!-- 07, CASES -->\n  <section class=\"sec fg-light bg-cream\"")],
   rate="",  # Kalkulator auf Wunsch des Kunden wieder raus
   tline='''      <div class="tline" data-fade>
        <div class="tldots" data-seg="h1 b9 g4 t28" aria-label="42 Tage als Punkte"></div>
        <div class="tllegend"><span><i class="tl-h"></i>Heute: Anfrage und Einschätzung</span><span><i class="tl-b"></i>Tag 2 bis 10: Konto, Karten, Seite</span><span><i class="tl-t"></i>Woche 3 bis 6: der Test, jede Woche gelesen</span></div>
      </div>
'''),
}


def service(slug, c):
    h = open(slug + ".html", encoding="utf-8").read()
    h = common(h, c["title"])
    # Seitenklasse und Kapitel-Leiste
    links = "".join('    <a href="#%s">%s</a>\n' % (i, l) for l, i, _ in c["chap"])
    h = rep(h, "<main>", '<main class="apl">\n\n  <!-- KAPITEL-LEISTE -->\n  <nav class="chapnav" aria-label="Kapitel">\n    <span class="cn-title">%s</span>\n%s    <a class="cn-cta" href="#anfrage">Anfragen</a>\n  </nav>\n' % (c["chap_title"], links), "main")
    # Punkt-Zoom auf der Ausgangslage
    h = rep(h, "  <!-- AKT 1: DAS PROBLEM -->\n  <section class=\"sec fg-dark kapsec kapsec--dark\"",
            "  <!-- AKT 1: DAS PROBLEM -->\n  <section class=\"dotzoom sec fg-dark kapsec kapsec--dark\"", "Punkt-Zoom")
    # Kapitel-IDs
    for _, cid, anchor in c["chap"]:
        h = rep(h, anchor, anchor.replace("<section ", '<section id="%s" ' % cid), "Kapitel " + cid)
    # Punkt statt Glyph im Hero, Punktzeile unter dem Hero-Text, Punktfeld
    h = rep(h, '<div class="svc-glyph" data-fade></div>', '<div class="svc-glyph" data-fade></div><span class="bdot" aria-hidden="true" data-fade></span>', "Hero-Punkt")
    h = rep(h, c["sub_anchor"], c["sub_anchor"] + '\n      <div class="dotline" data-fade style="--i:1">' + "".join("<span>%s</span>" % w for w in c["dotline"]) + "</div>", "Punktzeile")
    if c.get("dotfield"):
        h = rep(h, '<div data-fade style="--i:2;margin-top:28px"><a class="alink" href="#anfrage">Direkt anfragen ↓</a></div>\n',
                '<div data-fade style="--i:2;margin-top:28px"><a class="alink" href="#anfrage">Direkt anfragen ↓</a></div>\n' + c["dotfield"], "Punktfeld")
    # Alte Balkengrafik unter dem Beweis-Kopf weg, wo es sie gibt
    if c["drop_proofone"]:
        h = re.sub(r'      <div class="proofone">.*?      </div>\n      </div>\n', '', h, count=1, flags=re.S)
        assert "proofone" not in h, "proofone noch da"
    # Akt-Marken
    for anchor in c["rings"]:
        center = ' style="margin:0 auto 26px"' if "text-align:center" in anchor else ""
        h = rep(h, anchor, '<div class="actring" aria-hidden="true"%s></div>\n          ' % center + anchor, "Akt-Marke")
    # Punkt-Graphen vor den Cases, danach der Budget-Regler, wo es ihn gibt
    h = rep(h, "  <!-- 07, CASES -->", c["graph"] + c.get("rate", "") + "  <!-- 07, CASES -->", "Punkt-Graphen")
    # Zeitleiste im Ablauf
    if c.get("tline"):
        h = rep(h, '      <div class="oplist oplist--steps">', c["tline"] + '      <div class="oplist oplist--steps">', "Zeitleiste")
    out = slug + "-brand.html"
    open(out, "w", encoding="utf-8").write(h)
    print(out, len(h))




def agentur():
    h = open("agentur.html", encoding="utf-8").read()
    h = common(h, "Agentur, ad.boutique 2026")
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
    # Hero: Punkt, dritte Zeile als kursive Antwort, Punktzeile mit den drei Rollen
    h = rep(h, '<h1 class="dispn" data-lines>\n        <span class="rl"><span>Wir bauen Marken und Kampagnen</span></span>',
            '<span class="bdot" aria-hidden="true"></span>\n      <h1 class="dispn" data-lines>\n        <span class="rl"><span>Wir bauen Marken und Kampagnen</span></span>', "Hero-Punkt")
    h = rep(h, '<span class="rl"><span>auf Zahlen gebaut sind.</span></span>', '<span class="rl"><span><i>auf Zahlen gebaut sind.</i></span></span>', "Hero-Kursiv")
    h = rep(h, '<a class="alink" href="work.html" data-fade style="margin-top:30px">Die Beweise ansehen →</a>',
            '<div class="dotline" data-fade style="justify-content:flex-start;margin-top:22px"><span>strategen</span><span>kreative</span><span>performance-nerds</span></div>\n      <a class="alink" href="work.html" data-fade style="margin-top:30px">Die Beweise ansehen →</a>', "Punktzeile")
    # Akt-Ringe
    h = rep(h, '<div><span class="label" style="color:var(--grey-dark)">Was wir können</span></div>',
            '<div><div class="actring" aria-hidden="true"></div><span class="label" style="color:var(--grey-dark)">Was wir können</span></div>', "Ring Koennen")
    h = rep(h, '<h2 class="dispn" data-lines>\n        <span class="rl"><span>Ein Team aus Strategen, Kreativen</span></span>',
            '<div class="actring" aria-hidden="true" style="margin:0 auto 26px"></div>\n      <h2 class="dispn" data-lines>\n        <span class="rl"><span>Ein Team aus Strategen, Kreativen</span></span>', "Ring Team")
    open("agentur-brand.html", "w", encoding="utf-8").write(h)
    print("agentur-brand.html", len(h))


def case():
    """Projektseite: Basis ist die v3-Fassung des Funkhaus-Cases (schon mit Kapitel-Leiste und apl)."""
    h = open("case-premium-neubau-v3.html", encoding="utf-8").read()
    h = common(h, "Premium-Neubau, ad.boutique 2026")
    for lab in ['<span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Die Kampagne</span>',
                '<span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Die Seite</span>',
                '<span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Die Wellen</span>',
                '<span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(22px,3vw,40px)">Was der Kunde sagt</span>']:
        h = rep(h, lab, '<div class="actring" aria-hidden="true"></div>\n        ' + lab, "Ring " + lab[-30:])
    # Die These oeffnet sich aus einem Punkt
    h = rep(h, '<section class="cstate fg-dark"', '<section class="dotzoom cstate fg-dark"', "Punkt-Zoom These")
    # Punkt fuer Punkt: das Feld und die Strecken, vor dem Motiv-Viewer
    sec = '''  <!-- PUNKT FUER PUNKT -->
  <section class="sec fg-light bg-paper dotsec" data-bg="#f4f3ec" data-fg="dark" style="padding-top:clamp(30px,4vw,60px)">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Punkt für Punkt</span>
        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)"><span class="rl"><span>Jede Anfrage</span></span><span class="rl"><span><i>ein Punkt.</i></span></span></h2>
        <p class="lt3" data-fade style="margin-top:22px">489 Anfragen, 262 davon aus einem einzigen Motiv. Darunter die Strecken: Das Formular im Feed brachte die Anfrage für weniger als die Hälfte des Preises der Website.</p>
      </div>
      <div>
        <div class="dotfield-wrap" data-fade style="margin:0 0 30px;max-width:none">
          <canvas class="dotfield" data-total="489" data-lime="262" data-form="262" aria-label="489 Punkte, 262 davon in Lime"></canvas>
          <p class="dotfield-cap"><b>Jeder Punkt eine Anfrage</b>, die Lime-Punkte aus dem Interior-Motiv.<span class="dothint">Antippen</span></p>
        </div>
        <div class="dotbars" data-fade>
          <div class="row"><span class="rl">Instant Form</span><span class="dots" data-n="32" data-on="14"></span><span class="rv">€ 6,97</span></div>
          <div class="row hi"><span class="rl">Website-Formular</span><span class="dots" data-n="32" data-on="31"></span><span class="rv">€ 15,66</span></div>
        </div>
        <p class="dotnote" data-fade>Ein Punkt sind 50 Cent je Anfrage.</p>
        <div class="dotbars" data-fade>
          <div class="row hi"><span class="rl">Erste Welle, zehn Tage</span><span class="dots" data-n="20" data-on="17"></span><span class="rv">84 zu € 5,00</span></div>
          <div class="row hi"><span class="rl">Zweite Welle</span><span class="dots" data-n="20" data-on="13"></span><span class="rv">65 zu € 4,99</span></div>
          <div class="row hi"><span class="rl">Dritte Welle</span><span class="dots" data-n="20" data-on="19"></span><span class="rv">94 zu € 5,78</span></div>
        </div>
        <p class="dotnote" data-fade>Ein Punkt sind fünf Anfragen.</p>
      </div>
    </div>
  </section>

'''
    h = rep(h, "  <!-- VIEWER: die vier Motive, per Chip statt per Absatz -->", sec + "  <!-- VIEWER: die vier Motive, per Chip statt per Absatz -->", "Punkt-Sektion")
    open("case-premium-neubau-brand.html", "w", encoding="utf-8").write(h)
    print("case-premium-neubau-brand.html", len(h))


if __name__ == "__main__":
    index()
    agentur()
    case()
    for slug, c in SERVICES.items():
        service(slug, c)

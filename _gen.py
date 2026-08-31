# Seiten-Generator: 5 Service-LPs + 8 Case-Dossiers (Funkhaus bleibt handgebaut)
# Alle Zahlen aus uploads/AdBoutique_Referenzen_9Cases_Erweiterungsbriefing.md (bindend, anonymisiert)
# -*- coding: utf-8 -*-

HEAD = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} · ad.boutique Master</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@700;800;900&family=Hanken+Grotesk:wght@400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap">
<link rel="stylesheet" href="assets/master.css?v=13">
<script src="assets/master.js?v=13" defer></script>
</head>
<body style="background-color:{bodybg}" class="on-light">

<div class="pt"><div class="ptw">ad<i>.</i>boutique</div></div>

<header class="chrome">
  <a href="index.html" class="logo">ad<i>.</i>boutique</a>
  <a href="index.html#kontakt" class="ctc">Kontakt</a>
</header>

'''

MENU_ITEMS = [
    ("index.html", "Start", '''<span class="mv">
        <span class="half-d"><img loading="lazy" decoding="async" src="assets/img/funkhaus.jpg" alt=""></span>
        <span class="half-p"></span>
        <span class="bars" style="left:56%;top:26%;width:34%"><i style="width:92%"></i><i style="width:76%"></i><i style="width:84%"></i><i style="width:30%;height:8px;margin-top:5px"></i></span>
      </span>'''),
    ("work.html", "Work", '''<span class="mv">
        <span class="grid4">
          <span><img loading="lazy" decoding="async" src="assets/img/isi.jpg" alt=""></span>
          <span><img loading="lazy" decoding="async" src="assets/img/a_funk2.jpg" alt=""></span>
          <span style="background:#1C2530"></span>
          <span><img loading="lazy" decoding="async" src="assets/img/a_otta1.jpg" alt=""></span>
        </span>
      </span>'''),
    ("case-premium-neubau.html", "Case · Neubau Wien", '''<span class="mv">
        <img loading="lazy" decoding="async" src="assets/img/fx-66.jpg" alt="" style="position:absolute;inset:0;height:100%">
        <span class="bars" style="left:7%;bottom:10%;width:30%;filter:invert(1)"><i style="width:100%"></i><i style="width:60%"></i></span>
      </span>'''),
    ("index.html#leistungen", "Leistungen", '''<span class="mv" style="background:#F3EDE1">
        <span class="bars" style="left:8%;top:22%;width:40%"><i style="width:95%;height:9px"></i><i style="width:70%;height:9px"></i><i style="width:50%;margin-top:6px"></i><i style="width:26%;height:10px;margin-top:8px"></i></span>
        <img loading="lazy" decoding="async" src="assets/img/isi.jpg" alt="" style="position:absolute;right:6%;top:18%;width:36%;height:64%;border-radius:2px">
      </span>'''),
    ("agentur.html", "Agentur", '''<span class="mv">
        <span class="grid4" style="grid-template-columns:1fr 1fr">
          <span><img loading="lazy" decoding="async" src="assets/img/retreat-08.jpg" alt=""></span>
          <span><img loading="lazy" decoding="async" src="assets/img/retreat-01.jpg" alt=""></span>
        </span>
      </span>'''),
    ("index.html#kontakt", "Kontakt", '''<span class="mv" style="background:#EFE7D6">
        <span class="bars" style="left:8%;top:24%;width:84%"><i style="width:70%;height:9px"></i><i style="width:100%;height:1px;opacity:.3;margin:7px 0"></i><i style="width:52%;height:9px"></i><i style="width:100%;height:1px;opacity:.3;margin:7px 0"></i><i style="width:44%;height:9px"></i></span>
      </span>'''),
]

def menu(active):
    rows = []
    for href, label, mv in MENU_ITEMS:
        act = " act" if href == active else ""
        rows.append('    <a class="mitem%s" href="%s">\n      <span class="mt">%s</span>\n      <span class="mthumb">%s</span>\n    </a>' % (act, href, label, mv))
    return '''<button class="mbtn" aria-label="Menü öffnen"></button>
<svg class="morbit" viewBox="0 0 124 124" aria-hidden="true">
  <defs><path id="mpath" d="M62,62 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs>
  <text class="t-open"><textPath href="#mpath" startOffset="2%">Menü</textPath></text>
  <text class="t-close"><textPath href="#mpath" startOffset="2%">Schließen</textPath></text>
</svg>
<div class="mdim"></div>
<nav class="msheet" aria-label="Hauptmenü">
  <div class="mrow">
''' + "\n".join(rows) + '''
  </div>
  <div class="mfoot">
    <span class="fl">ad.boutique · Master-Preview</span>
    <span class="soc">
      <a href="https://www.instagram.com/ad.boutique.vienna/" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.linkedin.com/company/ad-boutique/" target="_blank" rel="noopener">LinkedIn</a>
    </span>
  </div>
</nav>

'''

FOOTER = '''  <footer data-bg="#070708" data-fg="light" style="padding-top:20px">
    <div class="wrap">
      <div class="fbase" style="margin-top:0">
        <span>© 2026 ad.boutique · Tuchlauben 13, 1010 Wien · Zürich in Vorbereitung</span>
        <span style="display:flex;gap:22px"><a href="index.html">Start</a><a href="work.html">Work</a><a href="agentur.html">Agentur</a><a href="index.html#kontakt">Kontakt</a></span>
      </div>
    </div>
    <div class="fword"><div>ad<i>.</i>boutique</div></div>
  </footer>
</main>
</body>
</html>
'''

LOGO = lambda names: "\n      ".join(
    '<img loading="lazy" decoding="async" src="assets/logos/%s.png" alt="%s">' % (n, n) for n in names)


BRANCH_LOGOS = {
    "Finance": ["ifa", "conda", "raiffeisen"],
    "Real Estate": ["winegg", "funkhaus", "seeresidenz", "soravia", "rhomberg", "vonpoll"],
    "D2C / Retail": ["looops", "isi", "nordicspirit", "ilbosso", "kaisers", "jti"],
    "Consumer": ["isi", "looops", "nordicspirit", "jti", "ilbosso", "kaisers"],
    "E-Commerce": ["looops", "isi", "nordicspirit", "ilbosso", "kaisers", "jti"],
    "Energie": ["hagent", "robin", "fabrik1230"],
}
LOGO_TILE_BGS = [
    ("#FBF8F2", "lt"), ("#0E0E10", "dk"), ("#EFE7D6", "lt"), ("#22382C", "dk"),
    ("#E9D8BC", "lt"), ("#1C2530", "dk"), ("#FFFFFF", "lt"), ("#4A3328", "dk"),
]
def logogrid(names):
    names = list(names)
    slots = 8
    per = max(1, (len(names) + slots - 1) // slots)
    while len(names) < slots * per:
        names += names[: slots * per - len(names)]
    out = []
    for i in range(slots):
        bg, tone = LOGO_TILE_BGS[i]
        chunk = names[i * per:(i + 1) * per]
        out.append('<span class="lslot" data-set="%s"></span>' % ",".join(chunk))
    return "\n        ".join(out)

def logocycle(names, slots=3):
    names = list(names)
    per = max(1, (len(names) + slots - 1) // slots)
    out = []
    for i in range(0, len(names), per):
        out.append('<span class="lslot" data-set="%s"></span>' % ",".join(names[i:i+per]))
    return "\n        ".join(out)

# ============================================================
# CASES (Reihenfolge = Staerke laut Briefing; Kette fuer "Naechster Case")
# ============================================================
CASES = [
 dict(slug="case-immobilien-investment", img="assets/prev/case-immobilien-investment.jpg", ziel="Zurechenbares Kapital", nav_title="Immobilien-Investment",
  title=["Immobilien-", "Investment."], sub="€ 36k Budget. € 4,65 Mio. Kapital. Zurechenbar.",
  clr="#2E3A2F", fg="#EDF2EC", big="129×", biglabel="zurechenbares Kapital",
  disz=[("Strategie & Funnel", "service-strategie.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Websites & Landingpages", "service-websites.html")],
  erg=["<em>129×</em> Return auf Google-Spend", "<em>€ 4,65 Mio.</em> zurechenbares Kapital", "<em>€ 3.004</em> Cost per Investor"],
  rahmen="Finance · Immobilien-Investment<br>3 Quartale<br>Google · Funnel · CRM",
  big_scrub="Ein hochwertiges Investment-Angebot ohne planbaren Zufluss <b>qualifizierter Investoren</b>: Vertrauen, Regulatorik und ein komplexer Entscheidungsweg machten reine <b>Reichweiten-Logik</b> wirkungslos.",
  body="Wir haben einen Investoren-Funnel gebaut, der Vertrauen Schritt für Schritt aufbaut, von der Aufklärung bis zur Zeichnung. Sauberes Tracking machte jeden Euro zurechenbar: € 4,65 Mio. Kapital aus € 36.043 Google-Budget, ein 129-facher Return. Über den gesamten Funnel wurden aus € 320k Spend € 12,8 Mio. Kapital, 446 Leads und 43 Zeichnungen.",
  statement=["Im Finance zählt der Cost per", "zugerechnetem Kapital.", "Nicht der CPL."],
  lens=[("Effizienz", "Cost per Investor von € 3.004, bei Zeichnungssummen weit darüber. Der Funnel rechnet sich ab der ersten Zeichnung."),
        ("Zielgruppe", "Kapitalstark und themenaffin: Qualität vor Quantität, konsequent bis in die Gebotsstrategie."),
        ("Message", "Investieren mit stabiler Planrendite: Aufklärung baut Vertrauen auf, Vertrauen führt zur Handlung."),
        ("Creative", "Bewegtbild für Vertrauen, Daten-Visuals für die Entscheidung."),
        ("Kanal", "Google sauber zurechenbar, CRM-Nurture für die Reife langer Entscheidungswege.")],
  nums=[("(Return on Ad Spend)", "129×"), ("(zurechenbares Kapital)", "€ 4,65 Mio."), ("(Cost per Investor)", "€ 3.004"), ("(Zeichnungen im Funnel)", "43")],
  note="Gesamt-Funnel: € 320k Spend, € 12,8 Mio. Kapital, 446 Leads. Ehrlich gemessen: Ein paralleler Paid-Media-Test über € 278.727 brachte 0 zugerechnete Zeichnungen und wurde gestoppt.",
  learn=["Im Finance zählt der Cost per zugerechnetem Kapital, nicht der CPL.",
         "Ehrlich, auch unbequem: Ein € 278k-Test brachte 0 Zeichnungen und wurde gestoppt.",
         "Sauberes Tracking ist die Voraussetzung für jede ehrliche Aussage."]),
 dict(slug="case-d2c-lifestyle", img="assets/img/c_candle.jpg", ziel="Profitables Wachstum", nav_title="D2C-Lifestyle-Marke",
  title=["D2C-Lifestyle-", "Marke."], sub="€ 520k → € 817k Umsatz. Das beste Jahr der Firmengeschichte.",
  clr="#4A3328", fg="#F4EEE8", big="+57 %", biglabel="Jahresumsatz",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>+57 %</em> Jahresumsatz", "<em>5,57</em> Blended ROAS, Ziel 3,5", "<em>+56 %</em> Bestellungen"],
  rahmen="D2C / Retail<br>12 Monate<br>Google · Pinterest · Meta · CRO",
  big_scrub="Solide Reichweite, aber <b>Conversion unter Benchmark</b>: Steigende Klickpreise drückten die Marge, der <b>Checkout</b> verlor Käufer, das <b>Tracking</b> verschleierte mehr, als es zeigte.",
  body="Erst gemessen, dann gehandelt: serverseitiges Tracking und saubere Produkt-Feeds als Fundament, Checkout vereinfacht, Produktseiten auf Conversion getrimmt, Ad-Struktur nach Deckungsbeitrag, Creatives systematisch getestet. Und Pinterest als unterschätzten Effizienz-Kanal erschlossen: € 312k Umsatz aus € 56k Mediabudget.",
  statement=["Der unterschätzte Kanal", "liefert oft den", "besten ROAS."],
  lens=[("Effizienz", "Pinterest führte mit ROAS 6,99, Google folgte mit 5,98. Inklusive Agentur-Fee blieb der Blend bei 4,17."),
        ("Zielgruppe", "Kaufstärkste Kohorten isoliert, kalte Streuung gestoppt."),
        ("Message", "Weniger Rabatt-Sprache, mehr Produktwert: Das hob den durchschnittlichen Warenkorb."),
        ("Creative", "UGC schlug Studio-Content beim ROAS deutlich."),
        ("Kanal", "Meta für Demand-Gen, Google für Abverkauf, Pinterest für Effizienz, sauber zugerechnet.")],
  nums=[("(Jahresumsatz)", "+57 %"), ("(Blended ROAS, Ziel 3,5)", "5,57"), ("(Bestellungen)", "+56 %"), ("(Umsatz aus € 56k Budget)", "€ 312k")],
  note="€ 520k auf € 817k Jahresumsatz in zwölf Monaten, aus demselben Traffic. Alle Werte aus den Accounts, anonymisierte Darstellung.",
  learn=["Umsatzwachstum beginnt im Tracking und im Checkout, nicht im Ad-Account.",
         "UGC hat den größten Conversion-Hebel.",
         "Profitabilität schlägt Reichweite, jede Woche aufs Neue."]),
 dict(slug="case-premium-neubau", nav_title="Premium-Neubau, Wien", handmade=True),
 dict(slug="case-crowdinvesting", img="assets/case/case-crowdinvesting/g0.jpg", ziel="Kapital je Projekt, planbar", nav_title="Crowdinvesting-Plattform",
  title=["Crowdinvesting-", "Plattform."], sub="Gleiches Budget. 4× mehr Kapital.",
  clr="#1C2530", fg="#E8EDF2", big="8,75", biglabel="ROAS, vorher 2,14",
  disz=[("Strategie & Funnel", "service-strategie.html"), ("Performance Marketing", "service-performance-marketing.html")],
  erg=["<em>€ 172.117</em> Kapital, +293 %", "<em>8,75</em> ROAS, +309 %", "<em>−69 %</em> Kosten je Investor"],
  rahmen="Finance · Crowdinvesting<br>POC-Phase<br>Meta · Google · Funnel",
  big_scrub="Investoren-Kampagnen liefen <b>projektweise</b>, ohne gemeinsame Datenbasis: Bei rund € 20k Budget kamen 16 Investments und € 43.740 Kapital zustande, <b>ROAS 2,14</b>, Kosten je Investor € 1.277.",
  body="Wir haben von Einzelkampagnen auf eine plattformbasierte Struktur umgestellt: gemeinsame Daten, klare KPI-Logik mit Kosten je Investor, Ø Investment, Volumen und ROAS, projektübergreifendes Lernen. Bei nahezu gleichem Budget wurden daraus € 172.117 Kapital, 50 Investments und ein ROAS von 8,75.",
  statement=["Struktur schlägt", "Einzelkampagne."],
  lens=[("Effizienz", "Das Top-Projekt erreichte ROAS 26,1: aus € 2.121 wurden € 55.400."),
        ("Zielgruppe", "Kapitalaffine Segmente projektübergreifend geschärft."),
        ("Message", "Rendite-Sicherheit vor Produktdetails."),
        ("Creative", "Projektspezifische Angles auf gemeinsamer Vorlage."),
        ("Kanal", "Plattform-Logik schlägt Projekt-Silo deutlich.")],
  nums=[("(Kapital, vorher € 43.740)", "€ 172.117"), ("(ROAS, vorher 2,14)", "8,75"), ("(Investments, vorher 16)", "50"), ("(Kosten je Investor, vorher € 1.277)", "€ 393")],
  note="Gleicher Spend, anderes Ergebnis: Der Beweis liegt im Vorher-Nachher der POC-Phase. Better selling through data.",
  learn=["Struktur schlägt Einzelkampagne.",
         "Die KPI-Definition vorab ist die halbe Miete.",
         "Gleicher Spend, anderes Ergebnis: Der Beweis liegt im Vorher-Nachher."]),
 dict(slug="case-wohnbau-floridsdorf", img="assets/prev/case-wohnbau-floridsdorf.jpg", ziel="Qualifizierte Kaufinteressenten", nav_title="Wohnbau, Floridsdorf",
  title=["Wohnbau,", "Floridsdorf."], sub="460 Kaufinteressenten zu € 12,77 pro Lead.",
  clr="#33383E", fg="#EFF1F3", big="460", biglabel="Leads · € 12,77 CPL",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html"), ("Websites & Landingpages", "service-websites.html")],
  erg=["<em>460</em> Leads", "<em>€ 12,77</em> gewichteter CPL", "<em>€ 9,59</em> CPL Instant Form Eigennutzer"],
  rahmen="Real Estate · Wohnbau<br>Q1 2026<br>Meta Instant Forms · Website",
  big_scrub="Neubau-Eigentumswohnungen ab € 247.800 mit <b>zwei sehr unterschiedlichen Zielgruppen</b>, Eigennutzer und Anleger, und einem <b>unsteten Anfragefluss</b> über Website-Formulare.",
  body="Vier Kampagnen, Eigennutzer und Anleger sauber getrennt, Schwerpunkt auf Meta Instant Forms, Botschaften je Zielgruppe gegeneinander getestet. Das Ergebnis: 460 Leads aus € 5.874 Spend, ein gewichteter CPL von € 12,77, und Instant Forms, die das Website-Formular beim CPL um den Faktor 3 bis 6 schlugen.",
  statement=["Eigennutzer und Anleger", "sind zwei Märkte.", "Kein gemeinsamer."],
  lens=[("Effizienz", "Instant Form schlug das Website-Formular beim CPL um Faktor 3 bis 6: € 9,59 statt € 58,05 bei Eigennutzern."),
        ("Zielgruppe", "Eigennutzer lieferten Volumen mit 425 Leads, Anleger Präzision mit 35."),
        ("Message", "Bei Anlegern schlug Service und Erstvermietung mit € 8,43 die Nachhaltigkeits-Story mit € 19,54 um das 2,3-Fache."),
        ("Creative", "Static für Eigennutzer, Video für Anleger."),
        ("Kanal", "Instant Form als Volumen-Hebel, die Website als Ort für Tiefe.")],
  nums=[("(Leads gesamt)", "460"), ("(gewichteter CPL)", "€ 12,77"), ("(Instant Form Eigennutzer)", "€ 9,59"), ("(bester Anleger-Angle)", "€ 8,43")],
  note="Spend gesamt: € 5.874. Stärkster Eigennutzer-Angle: Ab-Preis plus Lage mit 331 Leads zu € 9,76.",
  learn=["Eigennutzer und Anleger sind zwei Märkte, kein gemeinsamer.",
         "Anleger wollen Rendite-Sicherheit, keine Zertifikate.",
         "Ehrlicher CPL entsteht durch Testing."]),
 dict(slug="case-consumer-brand",
  phones=dict(h="Gebaut für den Daumen.", t="Die Saison lebt mobil: Kampagnen-Site und Sujets, dort wo der Kauf beginnt.",
              imgs=["assets/img/web_twistnsparkle_m0.jpg", "assets/img/web_twistnsparkle_m1.jpg", "assets/img/web_twistnsparkle_m2.jpg", "assets/img/web_twistnsparkle_ms0.jpg"]),
  ziel="Profitabler Saison-Peak", nav_title="Premium-Consumer-Brand",
  title=["Premium-", "Consumer-Brand."], sub="Black-Friday-ROAS 4,02. 75 % über dem eigenen Benchmark.",
  img="assets/img/isi.jpg", big="4,02", biglabel="BFCM-ROAS",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>4,02</em> BFCM-ROAS, Benchmark 2,3", "<em>€ 0,99</em> Awareness-CPM, −72 %", "<em>7,26 Mio.</em> Impressions"],
  rahmen="Consumer · Beverage-Lifestyle<br>Saison-Peaks<br>Meta",
  big_scrub="Eine starke Marke mit <b>saisonalen Spitzen</b> wie Black Friday und Weihnachten, aber Mediakosten und Sales-Effizienz schwankten ohne klare <b>Kampagnen-Architektur</b>.",
  body="Wir haben die Saison als getaktete Architektur gebaut: effiziente Awareness im Vorlauf, Sales-Druck im Peak, sauberes Audience-Layering und Retargeting. Der BFCM-ROAS lag mit 4,02 um 75 Prozent über dem Account-Benchmark von 2,3, die Awareness kostete mit € 0,99 CPM 72 Prozent weniger als der Benchmark.",
  statement=["Saison ist Architektur.", "Kein Zufall."],
  lens=[("Effizienz", "Peak-ROAS deutlich über Benchmark bei gleichzeitig günstigerer Awareness."),
        ("Zielgruppe", "Die Vorlauf-Awareness wärmt die spätere Sales-Audience."),
        ("Message", "Lifestyle im Vorlauf, klares Angebot im Peak."),
        ("Creative", "Saisonale Motive je Phase."),
        ("Kanal", "Meta, in Phasen orchestriert.")],
  nums=[("(BFCM-ROAS, Benchmark 2,3)", "4,02"), ("(Awareness-CPM, Benchmark € 3,50)", "€ 0,99"), ("(Always-On-Sales)", "295"), ("(Impressions)", "7,26 Mio.")],
  note="Benchmark schlagen heißt: den eigenen Account kennen. Alle Werte aus dem Ad-Manager, anonymisierte Darstellung.",
  learn=["Saison ist Architektur, kein Zufall.",
         "Günstige Awareness im Vorlauf macht den Peak profitabel.",
         "Benchmark schlagen heißt: den eigenen Account kennen."]),
 dict(slug="case-bautraeger-portfolio",
  phones=dict(h="Sujets, die im Feed bestehen.", t="Lage plus Lebensgefühl statt Floskeln: die Motive aus dem laufenden Portfolio.",
              imgs=["assets/img/a_otta1.jpg", "assets/img/a_otta2.jpg", "assets/img/a_otta3.jpg"]),
  ziel="Planbare Leads im Portfolio", nav_title="Bauträger-Portfolio, Wien",
  title=["Bauträger-", "Portfolio, Wien."], sub="€ 4,72 pro Lead. Der effizienteste im ganzen Portfolio.",
  img="assets/img/a_otta1.jpg", big="€ 4,72", biglabel="Cost per Lead",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>109</em> Leads aus € 515 Spend", "<em>€ 4,72</em> Cost per Lead", "<em>2,24 %</em> CTR"],
  rahmen="Real Estate · Wohnbau<br>Laufend, mehrere Projekte<br>Meta Instant Forms",
  big_scrub="Ein Bauträger mit mehreren parallelen Wiener Projekten brauchte <b>planbare, vergleichbare Lead-Qualität</b> über das gesamte Portfolio, nicht projektweise <b>Bauchentscheidungen</b>.",
  body="Wir haben ein wiederholbares Lead-System über alle Projekte ausgerollt: gleiche Test-Mechanik, lagespezifische Lifestyle-Botschaften, konsequente Creative-Selektion nach CPL. Im Projekt im 7. Bezirk: 109 Leads aus € 515 Spend zu € 4,72, der niedrigste CPL im gesamten Wohnbau-Portfolio.",
  statement=["Ein gutes System ist", "wiederholbar. Über", "Projekte hinweg."],
  lens=[("Effizienz", "Das Winner-Creative Puls des 7. brachte 98 Leads zu € 4,56."),
        ("Zielgruppe", "Eigennutzer mit Lagebezug."),
        ("Message", "Bezirks-Lebensgefühl schlägt generische Neubau-Sprache."),
        ("Creative", "Collage plus Grundriss als Effizienz-Variante mit € 3,01 CPL."),
        ("Kanal", "Instant Form, projektübergreifend standardisiert.")],
  nums=[("(Leads, 7. Bezirk)", "109"), ("(Cost per Lead)", "€ 4,72"), ("(Winner-Creative)", "€ 4,56"), ("(Effizienz-Variante)", "€ 3,01")],
  note="Spend: € 515, CTR 2,24 %. Der niedrigste CPL im gesamten Wohnbau-Portfolio, aus Disziplin, nicht aus Glück.",
  learn=["Ein gutes System ist wiederholbar, über Projekte hinweg.",
         "Lage plus Lebensgefühl schlagen Floskeln.",
         "Niedrige CPL kommt aus Disziplin, nicht aus Glück."]),
 dict(slug="case-health-brand", img="assets/prev/case-health-brand.jpg", ziel="Profitable Skalierung", nav_title="Dental-/Health-Marke",
  title=["Dental-/", "Health-Marke."], sub="1.385 Verkäufe in 7 Monaten. Und der ehrliche Blick darauf.",
  clr="#1F3833", fg="#EAF1EE", big="1.385", biglabel="Verkäufe in 7 Monaten",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>1.385</em> Verkäufe", "<em>€ 60</em> Retargeting-CPA", "<em>−58 %</em> CPA durch UGC"],
  rahmen="E-Commerce · Health<br>7 Monate<br>Meta",
  big_scrub="Wachstum bei steigendem Spend, aber die <b>Profitabilität blieb unter Zielwert</b>: ein klassischer <b>Skalierungs-Konflikt</b>.",
  body="Wir haben über € 200k Mediabudget systematisch gesteuert: Kampagnen nach Rolle getrennt, Creatives nach CPA getestet, Budget auf die effizientesten Hebel verschoben. Und offen reportet, wo das Ziel noch nicht erreicht wurde: Blended ROAS 1,07 bei Ziel 1,50. Der effizienteste Hebel war Retargeting mit € 60 CPA.",
  statement=["Ehrlichkeit schlägt", "Schönfärben."],
  lens=[("Effizienz", "Retargeting mit € 60 CPA und UGC trugen die Wirtschaftlichkeit."),
        ("Zielgruppe", "Warme Retargeting-Audiences waren am profitabelsten."),
        ("Message", "Nutzen vor Produktdetails."),
        ("Creative", "UGC schlug klassische Produkt-Videos beim CPA um rund 58 Prozent: € 82 bis 99 statt € 200."),
        ("Kanal", "Eine Haupt-Kampagne trug den Großteil des Spends, mit klarer Skalierungs-Empfehlung.")],
  nums=[("(Verkäufe)", "1.385"), ("(Spend, gesteuert)", "€ 200,5k"), ("(Retargeting-CPA)", "€ 60"), ("(Blended ROAS, Ziel 1,50)", "1,07")],
  note="Ein Ziel-Gap gehört offen ins Reporting: Der Blended ROAS lag mit 1,07 unter dem Ziel von 1,50, der Weg dorthin steht im Report, nicht im Kleingedruckten.",
  learn=["Ehrlichkeit schlägt Schönfärben: Ein Ziel-Gap gehört offen ins Reporting.",
         "Der größte Hebel war das Creative, nicht das Budget.",
         "Retargeting ist der effizienteste Euro."]),
 dict(slug="case-photovoltaik", img="assets/img/a_gmund1.jpg", ziel="Qualifizierte Anfragen", nav_title="Photovoltaik-Anbieter",
  title=["Photovoltaik-", "Anbieter."], sub="406 Leads. Und +487 % mehr Website-Besucher.",
  clr="#3A3A2E", fg="#F0F0E6", big="+487 %", biglabel="Website-Besucher",
  disz=[("Websites & Landingpages", "service-websites.html"), ("Performance Marketing", "service-performance-marketing.html")],
  erg=["<em>406</em> Leads", "<em>€ 30,83</em> pro Lead", "<em>+487 %</em> Website-Besucher"],
  rahmen="Energie · Photovoltaik<br>Kampagnenphase<br>Google Search · Konfigurator",
  big_scrub="Hohe Nachfrage im Markt, aber zu wenig <b>Sichtbarkeit</b> und kein Mechanismus, Interessenten in <b>qualifizierte Anfragen</b> zu verwandeln.",
  body="Wir haben Google Search auf kaufnahe Intents ausgerichtet und einen PV-Konfigurator als Lead-Magnet gebaut: Der Besucher rechnet seinen Bedarf und wird dabei zum Lead. 406 Leads zu € 30,83, und 487 Prozent mehr Website-Besucher.",
  statement=["Der Konfigurator selbst", "ist das beste Creative."],
  lens=[("Effizienz", "Kaufnahe Search-Intents statt teurer Reichweite."),
        ("Zielgruppe", "Aktiv Suchende mit hoher Abschlussnähe."),
        ("Message", "Bedarf in zwei Minuten berechnen."),
        ("Creative", "Der Konfigurator selbst ist das beste Creative."),
        ("Kanal", "Search als Nachfrage-Erntemaschine.")],
  nums=[("(Leads)", "406"), ("(Cost per Lead)", "€ 30,83"), ("(Website-Besucher)", "+487 %"), ("(Mechanik)", "Konfigurator")],
  note="Sichtbarkeit und Conversion-Mechanik gehören zusammen: Search erntet Nachfrage, die schon da ist, der Konfigurator macht sie zur Anfrage.",
  learn=["Ein interaktiver Lead-Magnet schlägt das Standard-Formular.",
         "Search erntet Nachfrage, die schon da ist.",
         "Sichtbarkeit und Conversion-Mechanik gehören zusammen."]),
]

def case_page(c, nxt):
    world = c.get("clr", "#22382C")
    wfg = c.get("fg", "#EDF2EC")
    if c.get("img"):
        hero = """<section class="chero" data-bg="%s" data-fg="light">
    <img src="%s" alt="%s">
    <div class="hcap">
      <div class="cl" style="font-size:15px">%s <span>· %s</span></div>
      <div class="serif" style="font-size:clamp(34px,4.4vw,72px);margin-top:10px;text-shadow:0 2px 24px rgba(0,0,0,0.4)">%s</div>
    </div>
    <div class="hkpi"><div class="kv">%s</div><div class="kl">(%s)</div></div>
    <div class="scrollhint">Scrollen</div>
  </section>""" % (world, c["img"], c["nav_title"], c["nav_title"], c["rahmen"].split("<br>")[0].split("·")[0].strip(), c["sub"], c["big"], c["biglabel"])
    else:
        hero = """<section class="chero" data-bg="%s" data-fg="light" style="background:%s;color:%s">
    <div class="hcap">
      <div class="cl" style="font-size:15px">%s <span style="opacity:.65">· %s</span></div>
      <div class="serif" style="font-size:clamp(34px,4.4vw,72px);margin-top:10px">%s</div>
    </div>
    <div class="hkpi"><div class="kv" style="font-size:clamp(60px,7vw,120px)">%s</div><div class="kl">(%s)</div></div>
    <div class="scrollhint">Scrollen</div>
  </section>""" % (world, world, wfg, c["nav_title"], c["rahmen"].split("<br>")[0].split("·")[0].strip(), c["sub"], c["big"], c["biglabel"])
    disz_links = "\n          ".join('<a href="%s">%s</a>' % (h, t) for t, h in c["disz"])
    lens_rows = "\n".join('        <div class="lrow" data-fade><div class="ll">%s</div><div class="lt">%s</div></div>' % (l, t) for l, t in c["lens"])
    nums = "\n".join('        <div class="n" data-fade><div class="l">%s</div><div class="v num serif">%s</div></div>' % (l, v) for l, v in c["nums"])
    learn = "\n".join('        <p class="serif" data-fade style="font-size:clamp(20px,1.9vw,28px);padding:18px 0;border-top:1px solid var(--line-d)%s">%s</p>' % (
        (";border-bottom:1px solid var(--line-d)" if i == len(c["learn"]) - 1 else ""), t) for i, t in enumerate(c["learn"]))
    stmt = "\n".join('        <span class="rl"><span>%s</span></span>' % x for x in c["statement"])
    svc_t, svc_h = c["disz"][0]
    phones_sec = ""
    if c.get("phones"):
        ph = c["phones"]
        screens = ph["imgs"]
        if screens and isinstance(screens[0], list):
            screens = [x for grp in screens for x in grp]
        seen = set(); flat = []
        for x in screens:
            if x not in seen:
                seen.add(x); flat.append(x)
        colA = flat[0::2]; colB = flat[1::2]
        def _col(items, speed):
            fr = "\n          ".join('<div class="phframe"><img loading="lazy" decoding="async" src="%s" alt=""></div>' % i for i in items)
            return '<div class="phcol" data-drift="%s">\n          %s\n        </div>' % (speed, fr)
        phones_sec = """  <!-- MOBILE: Screens ziehen vorbei -->
  <section class="sec fg-light bg-paper phonesec" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap phwrap">
      <div class="phtxt">
        <div class="lchap" style="grid-template-columns:1fr;gap:18px">
          <div class="lh" data-lines><span class="rl"><span>""" + ph["h"] + """</span></span></div>
          <p class="lt3" data-fade>""" + ph["t"] + """</p>
        </div>
      </div>
      <div class="phcols">
        """ + _col(colA, "0.14") + """
        """ + _col(colB, "0.24") + """
      </div>
    </div>
  </section>

"""
    if nxt.get("handmade"):
        nxt_media = '<img loading="lazy" decoding="async" src="assets/img/funkhaus.jpg" alt="">'
        nxt_sub = "489 Leads zu € 11,77. Ein Motiv trug 54 %."
        nxt_name = "Premium-Neubau, Wien."
    else:
        nxt_name = " ".join(nxt["title"])
        nxt_sub = nxt["sub"]
        if nxt.get("img"):
            nxt_media = '<img loading="lazy" decoding="async" src="%s" alt="">' % nxt["img"]
        else:
            nxt_media = '<span style="display:flex;align-items:flex-end;aspect-ratio:4/3;background:%s;color:%s;padding:24px;border-radius:3px"><span style="font-family:var(--f-disp);font-weight:680;font-size:clamp(40px,4vw,64px);font-variant-numeric:tabular-nums">%s</span></span>' % (nxt.get("clr", "#22382C"), nxt.get("fg", "#EDF2EC"), nxt.get("big", ""))
    nxt_href = nxt["slug"] + ".html"
    page = HEAD.format(title="Case · " + c["nav_title"], bodybg=world) + menu("work.html") + """<main>

  <!-- HERO: Vollbild in der Case-Farbwelt -->
  """ + hero + """

  <!-- INTRO auf Papier: Story links, Key Facts rechts -->
  <section class="sec fg-light cintro bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap grid">
      <div>
        <span class="label" style="color:var(--grey-dark)">""" + c["rahmen"].replace("<br>", " · ") + """</span>
        <p class="serif" data-scrub style="margin-top:22px">""" + c["big_scrub"] + """</p>
        <p class="body" data-fade style="--i:1">""" + c["body"] + """</p>
        <div data-fade style="--i:2;margin-top:32px;display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn-i" href="mailto:hello@ad.boutique?subject=Projekt wie """ + c["nav_title"] + """">Ähnliches Projekt anfragen</a>
          <a class="btn btn-o" href="work.html">Alle Cases</a>
        </div>
      </div>
      <div class="cmeta" data-stagger>
        <div class="m" data-fade><div class="ml">Branche</div><div class="mv2">""" + c["rahmen"].split("<br>")[0] + """</div></div>
        <div class="m" data-fade><div class="ml">Zeitraum</div><div class="mv2">""" + c["rahmen"].split("<br>")[1] + """</div></div>
        <div class="m" data-fade><div class="ml">Kanäle</div><div class="mv2">""" + c["rahmen"].split("<br>")[2] + """</div></div>
        <div class="m" data-fade><div class="ml">Ziel</div><div class="mv2">""" + c.get("ziel", "") + """</div></div>
        <div class="m" data-fade><div class="ml">Leistungen</div><div class="mv2">
          """ + disz_links + """
        </div></div>
      </div>
    </div>
  </section>

  <!-- STATEMENT in der Farbwelt -->
  <section class="cstate fg-dark" data-bg="""" + world + """" data-fg="light" style="--case-clr:""" + world + """">
    <div class="inner">
      <span class="label" style="color:var(--champ)">So denken wir</span>
      <h2 class="serif" data-lines>
""" + stmt + """
      </h2>
    </div>
  </section>

  <!-- FÜNF PERSPEKTIVEN -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(30px,4vw,50px)">Fünf Perspektiven</span>
      <div class="lens" data-stagger>
""" + lens_rows + """
      </div>
    </div>
  </section>

  <!-- ERGEBNIS -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:0">
    <div class="wrap">
      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(30px,4vw,50px)">Ergebnis</span>
      <div class="cnums" data-stagger>
""" + nums + """
      </div>
      <p class="cfoot-note" data-fade>""" + c["note"] + """</p>
    </div>
  </section>

""" + phones_sec + """  <!-- LEARNINGS -->
  <section class="sec fg-dark" data-bg="""" + world + """" data-fg="light" style="background:""" + world + """">
    <div class="wrap" style="max-width:900px">
      <span class="label" style="color:var(--champ);display:block;margin-bottom:26px">Learnings</span>
      <div data-stagger>
""" + learn + """
      </div>
    </div>
  </section>

  <!-- NEXT CASE -->
  <section class="sec npro-sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-bottom:0">
    <div class="wrap">
      <div class="npbar2"><span>Nächster Case</span><a href="work.html">Alle ansehen</a></div>
      <a class="npro" href="""" + nxt_href + """">
        <span>
          <span class="nptit">""" + nxt_name + """</span>
          <span class="npsub2" style="display:block">""" + nxt_sub + """</span>
          <span class="npgo">Case ansehen</span>
        </span>
        <span class="npim2" data-scale>""" + nxt_media + """</span>
      </a>
    </div>
  </section>

""" + FOOTER
    return page

for i, c in enumerate(CASES):
    if c.get("handmade"):
        continue
    nxt = CASES[(i + 1) % len(CASES)]
    open(c["slug"] + ".html", "w", encoding="utf-8").write(case_page(c, nxt))
    print("case", c["slug"])
print("cases done")

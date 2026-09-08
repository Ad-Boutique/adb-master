# Seiten-Generator: 5 Service-LPs + 8 Case-Dossiers (Funkhaus bleibt handgebaut)
# Alle Zahlen aus uploads/AdBoutique_Referenzen_9Cases_Erweiterungsbriefing.md (bindend, anonymisiert)
# -*- coding: utf-8 -*-

HEAD = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} - ad.boutique Master</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">


<link rel="stylesheet" href="assets/master.css?v=72">
<script src="assets/master.js?v=72" defer></script>
</head>
<body style="background-color:{bodybg}" class="on-light">

<div class="pt"><div class="ptw">ad<i>.</i>boutique</div></div>

<header class="chrome">
  <a href="index.html" class="logo">ad<i>.</i>boutique</a>
  <a href="kontakt.html" class="ctc">Kontakt</a>
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
    ("kontakt.html", "Kontakt", '''<span class="mv" style="background:#EFE7D6">
        <span class="bars" style="left:8%;top:24%;width:84%"><i style="width:70%;height:9px"></i><i style="width:100%;height:1px;opacity:.3;margin:7px 0"></i><i style="width:52%;height:9px"></i><i style="width:100%;height:1px;opacity:.3;margin:7px 0"></i><i style="width:44%;height:9px"></i></span>
      </span>'''),
]

BACKCIRCLE = """<a class="bkbtn" href="work.html" aria-label="Zurück zur Übersicht"><span class="bkar">&#8592;</span></a>
<svg class="bkorbit" viewBox="0 0 100 100" aria-hidden="true">
  <defs><path id="bkpath" d="M50,50 m-38,0 a38,38 0 1,1 76,0 a38,38 0 1,1 -76,0"/></defs>
  <text><textPath href="#bkpath" startOffset="2%">Übersicht</textPath></text>
</svg>
"""


def menu(active, back=False):
    rows = []
    for href, label, mv in MENU_ITEMS:
        act = " act" if href == active else ""
        rows.append('    <a class="mitem%s" href="%s">\n      <span class="mt">%s</span>\n      <span class="mthumb">%s</span>\n    </a>' % (act, href, label, mv))
    return (BACKCIRCLE if back else "") + '''<button class="mbtn" aria-label="Menü öffnen"></button>
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
    <span class="fl">ad.boutique Master-Preview</span>
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
        <span>© 2026 ad.boutique, Tuchlauben 13, 1010 Wien. Zürich in Vorbereitung</span>
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
  rahmen="Finance, Immobilien-Investment<br>3 Quartale<br>Google, Funnel, CRM",
  big_scrub="Ein hochwertiges Investment-Angebot ohne planbaren Zufluss <b>qualifizierter Investoren</b>: Vertrauen, Regulatorik und ein komplexer Entscheidungsweg machten reine <b>Reichweiten-Logik</b> wirkungslos.",
  body="Wir haben einen Investoren-Funnel gebaut, der Vertrauen Schritt für Schritt aufbaut, von der Aufklärung bis zur Zeichnung. Sauberes Tracking machte jeden Euro zurechenbar: € 4,65 Mio. Kapital aus € 36.043 Google-Budget, ein 129-facher Return. Über den gesamten Funnel wurden aus € 320k Spend € 12,8 Mio. Kapital, 446 Leads und 43 Zeichnungen.",
  statement=["Im Finance zählt der Cost per", "zugerechnetem Kapital.", "Nicht der CPL."],
  lens=[("Effizienz", "Cost per Investor von € 3.004, bei Zeichnungssummen weit darüber. Der Funnel rechnet sich ab der ersten Zeichnung."),
        ("Zielgruppe", "Kapitalstark und themenaffin: Qualität vor Quantität, konsequent bis in die Gebotsstrategie."),
        ("Message", "Investieren mit stabiler Planrendite: Aufklärung baut Vertrauen auf, Vertrauen führt zur Handlung."),
        ("Creative", "Bewegtbild für Vertrauen, Daten-Visuals für die Entscheidung."),
        ("Kanal", "Google sauber zurechenbar, CRM-Nurture für die Reife langer Entscheidungswege.")],
  nums=[("(Return on Ad Spend)", "129×"), ("(zurechenbares Kapital)", "€ 4,65 Mio."), ("(Cost per Investor)", "€ 3.004"), ("(Zeichnungen im Funnel)", "43")],
  note="Gesamt-Funnel: € 320k Spend, € 12,8 Mio. Kapital, 446 Leads. Ehrlich gemessen: Ein zweiter Paid-Kanal lief beim Kunden bereits, bevor wir kamen. Wir haben ihn messbar gemacht, parallel den zurechenbaren Kanal aufgebaut, und als sich bestätigte, dass er keine Zeichnungen bringt, geschlossen.",
  learn=["Im Finance zählt der Cost per zugerechnetem Kapital, nicht der CPL.",
         "Ehrlich, auch unbequem: Ein bestehender Kanal wurde messbar gemacht, die Hypothese bestätigt, dass er nichts bringt, und geschlossen.",
         "Sauberes Tracking ist die Voraussetzung für jede ehrliche Aussage."]),
 dict(slug="case-d2c-lifestyle", img="assets/img/c_candle.jpg", ziel="Profitables Wachstum", nav_title="D2C-Lifestyle-Marke",
  title=["D2C-Lifestyle-", "Marke."], sub="€ 520k → € 817k Umsatz. Das beste Jahr der Firma.",
  clr="#4A3328", fg="#F4EEE8", big="+57 %", biglabel="Jahresumsatz",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>+57 %</em> Jahresumsatz", "<em>5,57</em> Blended ROAS, Ziel 3,5", "<em>+56 %</em> Bestellungen"],
  rahmen="D2C / Retail<br>12 Monate<br>Google, Pinterest, Meta, CRO",
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
  rahmen="Finance, Crowdinvesting<br>POC-Phase<br>Meta, Google, Funnel",
  big_scrub="Investoren-Kampagnen liefen <b>projektweise</b>ohne gemeinsame Datenbasis: Bei rund € 20k Budget kamen 16 Investments und € 43.740 Kapital zustande, <b>ROAS 2,14</b>Kosten je Investor € 1.277.",
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
  clr="#33383E", fg="#EFF1F3", big="460", biglabel="Leads, € 12,77 CPL",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html"), ("Websites & Landingpages", "service-websites.html")],
  erg=["<em>460</em> Leads", "<em>€ 12,77</em> gewichteter CPL", "<em>€ 9,59</em> CPL Instant Form Eigennutzer"],
  rahmen="Real Estate, Wohnbau<br>Q1 2026<br>Meta Instant Forms, Website",
  big_scrub="Neubau-Eigentumswohnungen ab € 247.800 mit <b>zwei sehr unterschiedlichen Zielgruppen</b>Eigennutzer und Anleger, und einem <b>unsteten Anfragefluss</b> über Website-Formulare.",
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
  title=["Premium-", "Consumer-Brand."], sub="Black-Friday-ROAS 4,02. 75 % über Benchmark.",
  img="assets/img/isi.jpg", big="4,02", biglabel="BFCM-ROAS",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>4,02</em> BFCM-ROAS, Benchmark 2,3", "<em>€ 0,99</em> Awareness-CPM, −72 %", "<em>7,26 Mio.</em> Impressions"],
  rahmen="Consumer, Beverage-Lifestyle<br>Saison-Peaks<br>Meta",
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
  title=["Bauträger-", "Portfolio, Wien."], sub="€ 4,72 pro Lead. Der effizienteste im Portfolio.",
  img="assets/img/a_otta1.jpg", big="€ 4,72", biglabel="Cost per Lead",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>109</em> Leads aus € 515 Spend", "<em>€ 4,72</em> Cost per Lead", "<em>2,24 %</em> CTR"],
  rahmen="Real Estate, Wohnbau<br>Laufend, mehrere Projekte<br>Meta Instant Forms",
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
  title=["Dental-/", "Health-Marke."], sub="1.385 Verkäufe in 7 Monaten, ehrlich gerechnet.",
  clr="#1F3833", fg="#EAF1EE", big="1.385", biglabel="Verkäufe in 7 Monaten",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Content Creation", "service-content-creation.html")],
  erg=["<em>1.385</em> Verkäufe", "<em>€ 60</em> Retargeting-CPA", "<em>−58 %</em> CPA durch UGC"],
  rahmen="E-Commerce, Health<br>7 Monate<br>Meta",
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
  rahmen="Energie, Photovoltaik<br>Kampagnenphase<br>Google Search, Konfigurator",
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
 dict(slug="case-seeresidenz", ziel="Kaufinteressenten für ein Seeprojekt", nav_title="Seeresidenz Gmunden",
  title=["Seeresidenz", "Gmunden."], sub="Ein Projekt am See. Anfragen aus dem ganzen Land.",
  clr="#2A3D4A", fg="#E8EEF2", big="1.761", biglabel="Anfragen über Meta",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Strategie & Funnel", "service-strategie.html"), ("Content Creation", "service-content-creation.html")],
  rahmen="Real Estate, Seeprojekt<br>Juli 2024 bis Dezember 2025<br>Meta, Google Search, Landingpage",
  big_scrub="Ein Premium-Projekt am Traunsee mit <b>österreichweiter Zielgruppe</b>: Wer hier kauft, wohnt selten um die Ecke. Reichweite gab es, aber die <b>Anfragen</b> kamen unstet und teuer.",
  body="Wir haben Meta und Google Search als Paar gebaut: Meta erzeugt die Nachfrage mit Sujets vom See, Google fängt sie, wenn gesucht wird. In eineinhalb Jahren: 3,4 Millionen Impressionen und 43.000 Klicks über Meta, 4,6 Millionen Impressionen und 76.000 Klicks über Google, 1.761 Anfragen. Im Jahr 2024 kostete eine Anfrage im Schnitt 8 Euro.",
  statement=["Reichweite ist billig.", "Anfragen sind der Beweis."],
  lens=[("Effizienz", "1.460 Anfragen aus 9.540 Euro Mediabudget im Jahr 2024, rund 8 Euro je Anfrage."),
        ("Zielgruppe", "Zweitwohnsitz und Kapitalanlage, österreichweit statt regional."),
        ("Message", "Der See als Argument, der Preis als Filter."),
        ("Creative", "Stimmungsbilder vom Wasser im Hochformat, der Grundriss erst auf der Seite."),
        ("Kanal", "Meta erzeugt Nachfrage, Google Search erntet sie, beides zurechenbar bis zur Anfrage.")],
  nums=[("(Anfragen, 18 Monate)", "1.761"), ("(Impressionen Google)", "4,6 Mio."), ("(Klicks Meta und Google)", "119.000"), ("(je Anfrage, 2024)", "€ 8")],
  note="Werte aus den Konto-Exporten Juli 2024 bis Dezember 2025 und dem Lead-Report der Gruppe für 2024. Über die gesamte Projektgruppe des Kunden stieg der Online-Anteil der Anfragen innerhalb eines Jahres von rund der Hälfte auf hundert Prozent, der Preis je Anfrage fiel von 405 auf 48 Euro.",
  phones=dict(h="Der See im Hochformat.", t="Sujets aus der Kampagne, gebaut für den Feed.",
              imgs=["assets/img/a_gmund1.jpg", "assets/img/gmunden.jpg", "assets/img/a_gmund2.jpg"]),
  chapters=[dict(label="Zweites Kapitel, die Gruppe", h=["Sechs Projekte,", "eine Lead-Logik."],
    p1="Das Seeprojekt war eines von sechs, die wir für die Gruppe parallel geführt haben: zwei Türme an der Donau, ein Schlosspark, ein Gewerbeprojekt im Süden Wiens, ein nachhaltiges Bürohaus. Jedes mit eigener Zielgruppe, alle mit derselben Zurechnungslogik bis zur Anfrage.",
    p2="<b>Das Ergebnis über die Gruppe:</b> Binnen eines Jahres kamen die Anfragen nicht mehr zur Hälfte, sondern vollständig online, und der Preis je Anfrage fiel von 405 auf 48 Euro. Das Donau-Projekt brachte 172 Anfragen, das Gewerbeprojekt 162 Mietinteressenten über Google.",
    nums=[("(Projekte parallel)", "6"), ("(Anfragen, Donau-Projekt)", "172"), ("(Gewerbe-Anfragen über Google)", "162"), ("(Online-Anteil, Ende 2024)", "100 %")],
    note="Alle Werte aus dem monatlichen Lead-Report, den wir für die Gruppe geführt haben.",
    links=[("service-strategie.html", "Strategie & Funnel"), ("service-performance-marketing.html", "Performance Marketing")])],
  quote=("Eure professionelle und verlässliche Arbeitsweise hat wesentlich zum Erfolg unserer bisherigen Projekte beigetragen.", "Marketing Managerin, Soravia"),
  learn=["Reichweite ist billig, Anfragen sind der Beweis.",
         "Meta und Google sind kein Entweder-oder, sondern ein Paar.",
         "Der Online-Anteil der Anfragen ist die Kennzahl, an der man eine Gruppe steuert."]),
 dict(slug="case-nordic-spirit", ziel="Markteinführung mit messbaren Abschlüssen", nav_title="Nordic Spirit, JTI",
  title=["Nordic Spirit,", "JTI."], sub="Von 800 auf 7.800 Bestellungen im Monat.",
  clr="#0F2A44", fg="#E6EEF6", big="23.579", biglabel="Abschlüsse in zwölf Monaten",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Strategie & Funnel", "service-strategie.html"), ("E-Commerce Growth", "service-ecommerce.html")],
  rahmen="Consumer, Markteinführung<br>Juli 2025 bis Juni 2026<br>Meta, Google, Sampling-Funnel",
  big_scrub="Eine neue Marke in einer <b>regulierten Kategorie</b>, ohne Bekanntheit in Österreich, mit einem Ziel, das sich zählen lässt: <b>Gratis-Samples</b>, die zu Kunden werden. Und mit Regeln, die viele Werbemittel und Zielgruppen ausschließen.",
  body="Wir haben den Funnel als Sampling-Maschine gebaut: Meta für Volumen mit Angeboten wie vier Dosen gratis, Google für Effizienz auf der Suche, Ziel-CPA-Gebote als Steuerung, Gewinnspiele und Kooperationen bewusst getrennt vom Sales-Funnel. Aus 275.906 Euro Mediabudget wurden 23.579 Abschlüsse zu 11,70 Euro, die Bestellungen stiegen von 800 auf 7.800 im Monat.",
  statement=["Meta bringt Volumen.", "Google bringt Effizienz.", "Zusammen bringen sie Kunden."],
  lens=[("Effizienz", "Google mit 7,18 Euro je Abschluss, Search Always-on bei 4,80 Euro. Meta-CPA in den Conversion-Kampagnen von 13,01 auf 8,36 Euro gesenkt."),
        ("Zielgruppe", "Erwachsene Umsteiger, geschärft über Signale aus dem Sampling, kein Streuverlust in gesperrte Segmente."),
        ("Message", "Gratis probieren schlägt jedes Markenversprechen: Hol dir das Discovery Kit."),
        ("Creative", "Angebots-Statics und ein Markenfilm, wöchentlich neue Varianten gegen die Ermüdung."),
        ("Kanal", "Meta mit 73 Prozent des Budgets für Reichweite und Abschlüsse, Google mit 27 Prozent als Effizienzkanal, dazu ein Loyalty-Programm für Wiederkäufer.")],
  nums=[("(Abschlüsse)", "23.579"), ("(je Abschluss, gesamt)", "€ 11,70"), ("(Bestellungen je Monat, Peak)", "7.800"), ("(Reichweite Meta)", "2,8 Mio.")],
  note="Mediabudget 275.906 Euro, davon 202.221 Euro Meta und 73.685 Euro Google, 46,1 Millionen Impressionen. Peak von September bis Dezember 2025 mit über 6.000 Abschlüssen im Monat. Werte aus dem Performance Review an den Kunden. Die Kampagnen liefen bis 30. Juni 2026 im damals gültigen rechtlichen Rahmen, danach griff die neue Gesetzeslage für die Kategorie und die Bewerbung wurde planmäßig beendet.",
  chapters=[dict(label="Zweites Kapitel, die Übergabe", h=["Aufbauen, skalieren,", "sauber übergeben."],
    p1="Neben dem Sales-Funnel liefen zwei Nebenschauplätze mit eigener Logik: über zwanzig Gewinnspiel-Kooperationen mit rund 65.000 Interaktionen zu höchstens 52 Cent je Interaktion, und ein Loyalty-Programm für Wiederkäufer, das mit 4.499 Euro 142 Anmeldungen brachte. Beides bewusst getrennt gemessen, damit keine Zahl die andere verfälscht.",
    p2="<b>Zum 30. Juni 2026 haben wir das Konto übergeben:</b> mit Struktur, Dokumentation und den Learnings aus einem Jahr. Der Zeitpunkt war kein Zufall, sondern das Datum, an dem die neue Gesetzeslage für die Kategorie griff. Ein Mandat muss nicht ewig laufen, um ein gutes Mandat zu sein. Es muss sauber gebaut sein und zum richtigen Zeitpunkt enden.",
    nums=[("(Gewinnspiel-Kooperationen)", "20+"), ("(Interaktionen daraus)", "65.000"), ("(je Interaktion, maximal)", "€ 0,52"), ("(Loyalty-Anmeldungen)", "142")],
    note="Werte aus dem Performance Review zum Abschluss der Zusammenarbeit im Juni 2026.",
    links=[("service-strategie.html", "Strategie & Funnel"), ("service-ecommerce.html", "E-Commerce Growth")])],
  learn=["Ziel-CPA-Gebote waren der größte Hebel, nicht das Budget.",
         "Gewinnspiele gehören getrennt vom Sales-Funnel, sonst verfälschen sie jede Zahl.",
         "Eine Marke ohne Bekanntheit gewinnt über das Angebot, nicht über das Versprechen."]),
 dict(slug="case-medcenter", ziel="Patientenanfragen für ein neues Zentrum", nav_title="MedCenter 1030",
  title=["MedCenter", "1030."], sub="Ein Arztzentrum. Sichtbar in einer Woche.",
  clr="#3E5A52", fg="#EEF3F1", big=None, biglabel="",
  disz=[("Websites & Landingpages", "service-websites.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  rahmen="Health, Arztzentrum<br>Seit März 2026, laufend<br>Website, Google, Meta",
  big_scrub="Ein neues Arztzentrum im dritten Bezirk, mehrere Fachrichtungen unter einem Dach, aber <b>kein Auftritt</b>, keine Sichtbarkeit und ein Startdatum, das <b>nicht wartete</b>.",
  body="Innerhalb einer Woche standen Website und Kampagnen-Setup: eine Seite, die Fachrichtungen, Team und Termine ohne Umweg zeigt, dazu Google für die aktive Suche und Meta für die Nachbarschaft, mit Sujets, die das Zentrum als Ort zeigen, nicht als Leistungsverzeichnis. Die Kampagnen laufen seit dem Frühjahr, die Zahlen lesen wir vierteljährlich mit der Praxisleitung.",
  statement=["Gesundheit braucht Nähe.", "Auch online."],
  lens=[("Effizienz", "Ein Setup, zwei Kanäle, ein Reporting, ohne Agenturaufwand, der eine Ordination überfordert."),
        ("Zielgruppe", "Menschen im Grätzel und Suchende mit konkretem Anliegen."),
        ("Message", "Ein Zentrum, viele Fachrichtungen, kurze Wege."),
        ("Creative", "Ruhige Statics in der Farbwelt des Zentrums, Menschen statt Geräte."),
        ("Kanal", "Google für die Suche, Meta für die Nachbarschaft.")],
  nums=[], note="",
  phones=dict(h="Sujets für das Grätzel.", t="Kampagnen-Statics aus dem Setup, gebaut für den Feed.",
              imgs=["assets/case/medcenter/g0.jpg", "assets/case/medcenter/g1.jpg", "assets/case/medcenter/g2.jpg", "assets/case/medcenter/g3.jpg", "assets/case/medcenter/g4.jpg"]),
  quote=("Die Seite sieht echt schon sehr gut aus.", "Marketing-Koordination, MedCenter 1030, nach der ersten Abnahme"),
  learn=["Eine Ordination braucht keinen Konzern-Auftritt, sondern einen, der in einer Woche steht.",
         "Empfehlungen entstehen aus Arbeit: Der Kontakt kam über eine Projektmanagerin aus dem Immobilienumfeld.",
         "Gesundheit verkauft sich über Nähe, nicht über Rabatt."]),
 dict(slug="case-juwel", ziel="Qualifizierte Eventanfragen", nav_title="Juwel Wien",
  title=["Juwel", "Wien."], sub="Eine Location im 15. Stock. Sichtbar in der ganzen Stadt.",
  clr="#2B2620", fg="#EFE6D6", big=None, biglabel="",
  disz=[("Content Creation", "service-content-creation.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Websites & Landingpages", "service-websites.html")],
  rahmen="Event-Location, Gastronomie<br>Seit November 2025, laufend<br>Instagram, Meta, Google, LinkedIn",
  big_scrub="Eine Rooftop-Location über den Dächern Wiens, die jeder kennt, der oben war, und zu wenige, die noch nicht oben waren. <b>Social Media lief nebenbei</b>, Anfragen kamen <b>über Umwege</b>.",
  body="Wir führen die Kanäle als verlängertes Team der Location: zwölf Beiträge und Stories im Monat, Content-Tage alle zwei Monate, Community-Management, dazu Kampagnen auf Meta, Google und LinkedIn für Firmenevents, Hochzeiten und private Feiern. Seit dem Sommer 2026 mit eigenen Landingpages je Anlass und einem Vergütungsmodell, das am Eventwert hängt: Wir verdienen mit, wenn gebucht wird.",
  statement=["Wir verdienen,", "wenn gebucht wird."],
  lens=[("Effizienz", "Erfolgsbeteiligung statt Fixhonorar für die Kampagnen, gestaffelt nach Eventwert."),
        ("Zielgruppe", "Firmen, die einen Ort für ihre Feier suchen, Paare vor der Hochzeit, Gastgeber privater Runden."),
        ("Message", "Der Blick ist das Versprechen, der Service das Argument."),
        ("Creative", "Editorial-Shooting mit Models statt Eventfotografie, damit die Location wie eine Marke aussieht."),
        ("Kanal", "Instagram als Bühne, Meta und Google für Anfragen, LinkedIn für Firmenevents.")],
  nums=[], note="",
  phones=dict(h="Silvester über der Stadt.", t="Sujets und Stories aus der Kampagne zum Jahreswechsel.",
              imgs=["assets/img/a_silv1.jpg", "assets/case/juwel/g0.jpg", "assets/img/a_silv2.jpg", "assets/case/juwel/g2.jpg"]),
  quote=("Passt perfekt!", "Geschäftsführung, Juwel Wien, zum Vergütungsmodell nach Eventwert"),
  learn=["Eine Location ist eine Marke, wenn man sie so fotografiert.",
         "Landingpages je Anlass schlagen die eine Kontaktseite.",
         "Erfolgsbeteiligung macht aus Agentur und Kunde ein Team."]),
 dict(slug="case-bella-vita", img="assets/prev/herogroup.jpg", ziel="Kaufinteressenten für 49 fertige Wohnungen", nav_title="Bella Vita, Hero Group",
  title=["Bella Vita,", "Wiener Neustadt."], sub="Fertig gebaut. Jetzt wird verkauft.",
  clr="#3B3A36", fg="#F1EEE8", big="21", biglabel="Anfragen in der ersten Woche",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  rahmen="Real Estate, Wohnbau<br>Seit Mai 2026, laufend<br>Meta, Google, Makler-Übergabe",
  big_scrub="49 fertiggestellte Wohnungen in Wiener Neustadt, zwei Maklerhäuser im Vertrieb und eine Vorgänger-Agentur, bei der eine Google-Anfrage rund <b>80 Euro</b> kostete. Das Projekt brauchte <b>Volumen zu einem Preis, der trägt</b>, und Anfragen, die beim Makler ankommen.",
  body="Wir haben in drei Wochen Setup, Sujets und Funnel gebaut und im Mai mit Meta gestartet: 21 Anfragen in der ersten Woche, rund 57 bis Mitte Juli, überwiegend Eigennutzer mit drei bis vier Zimmern und einem Budget zwischen 280.000 und 450.000 Euro. Jede Anfrage geht automatisch an eines der beiden Maklerhäuser, mit einer Rückmeldeschleife zur Qualität. Seit August ergänzt Google die Suche nach dem Projekt.",
  statement=["Der Lead ist erst", "beim Makler ein Lead."],
  lens=[("Effizienz", "Wenige Sujets, klare Zielgruppe, wöchentliche Umschichtung: Volumen ohne Streuverlust."),
        ("Zielgruppe", "Eigennutzer aus der Region mit konkretem Zeithorizont von sechs bis zwölf Monaten."),
        ("Message", "Fertig, besichtigbar, sofort beziehbar. Das Argument eines fertigen Projekts."),
        ("Creative", "Renderings und Bewegtbild aus dem Projekt, der Grundriss erst auf der Seite."),
        ("Kanal", "Meta für Volumen, Google seit August für die aktive Suche, Übergabe je zur Hälfte an zwei Makler.")],
  nums=[("(Anfragen, erste Woche)", "21"), ("(Anfragen bis Mitte Juli)", "57"), ("(Zeithorizont der Interessenten)", "6 bis 12 Monate"), ("(Maklerhäuser im Vertrieb)", "2")],
  note="Werte aus der Lead-Liste an die Makler, Mai bis Juli 2026. Preis je Anfrage und Verkäufe reportieren wir, sobald das Quartal geschlossen ist.",
  chapters=[dict(label="Zweites Kapitel, nach dem Lead", h=["Zwei Makler,", "eine Rückmeldeschleife."],
    p1="Jede Anfrage landet bei einem der beiden Maklerhäuser, und jede Rückmeldung landet wieder bei uns: Exposé verschickt, Telefonat geführt, nicht erreichbar, zu teuer, zu wenig zentral. Aus diesen Notizen lernen die Kampagnen, welche Botschaft die Menschen bringt, die dann auch besichtigen.",
    p2="<b>Das wichtigste Learning kam vom Kunden selbst:</b> Social-Media-Anfragen müssen innerhalb von Stunden kontaktiert werden, sonst sind sie kalt. Deshalb ist die Erstkontakt-Zeit der Makler Teil unseres Reportings, nicht nur der Preis je Anfrage.",
    links=[("service-performance-marketing.html", "Performance Marketing"), ("case-web-noma.html", "Noma Living, das zweite Projekt mit Hero Group")])],
  quote=("Social-Media-Leads müssen sehr kurzfristig kontaktiert werden, um zum Erfolg zu kommen.", "Projektleitung, Hero Group, an die Maklerhäuser"),
  learn=["Der Lead ist erst beim Makler ein Lead.",
         "Ein fertiges Projekt verkauft sich über Verfügbarkeit, nicht über Visionen.",
         "Die Erstkontakt-Zeit gehört ins Reporting."]),
]

# Weitere Kapitel und Kundenstimmen je Case, Quelle: Reportings, Angebote und Kundenmails (Recherche 7.9.2026).
# Kunden bleiben anonymisiert, Zitate tragen nur die Rolle.
EXTRA = {
 "case-immobilien-investment": dict(
  rahmen="Finance, Immobilien-Investment<br>Seit 2023, laufend<br>Google, LinkedIn, Funnel, CRM, Video",
  disz=[("Strategie & Funnel", "service-strategie.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Websites & Landingpages", "service-websites.html"), ("Content Creation", "service-content-creation.html")],
  chapters=[dict(label="Zweites Kapitel, Bewegtbild", h=["Ein komplexes Produkt,", "erklärt vom Vorstand."],
    p1="Ein Bauherrenmodell versteht niemand aus einer Anzeige. Deshalb haben wir mit dem Vorstand gedreht: sechs Kurzvideos für Feed und Search-Begleitung, eine Langversion, ein Erklärvideo, das den Weg vom Investment bis zur Steuerwirkung in wenigen Minuten aufmacht, dazu Making-of für die eigenen Kanäle.",
    p2="<b>Dahinter läuft seit 2023 die Maschine:</b> Always-on-Suche, Kampagnen je Objekt mit Learning-Transfer von Projekt zu Projekt, LinkedIn für die Anleihe, und ein Lead-Dashboard mit täglichem Datenfeed, das jede Anfrage bis zur Zeichnung mitführt. 2024 kamen 80 Prozent der Anfragen online, bei einem Preis je Online-Anfrage, der gegenüber dem Vorjahr um 19 Prozent sank.",
    nums=[("(Kurzvideos aus einem Drehtag)", "6"), ("(Online-Anteil der Anfragen 2024)", "80 %"), ("(Preis je Online-Anfrage, zu 2023)", "−19 %")],
    note="Werte aus dem Lead-Report des Kunden für 2023 und 2024. Das Erklärvideo läuft auf der Website, in Search-Begleitkampagnen und im Vertrieb.",
    links=[("service-content-creation.html", "Content Creation"), ("service-strategie.html", "Strategie & Funnel")])]),
 "case-d2c-lifestyle": dict(
  chapters=[dict(label="Zweites Kapitel, das Fundament", h=["Erst messen,", "dann kaufen."],
    p1="Bevor ein Euro mehr in Anzeigen floss, haben wir das Fundament gelegt: Tag Manager, Analytics und serverseitiges Tracking, damit jede Bestellung einmal gezählt wird, dazu saubere Produkt-Feeds über ein Feed-Management, das Meta, Google und Pinterest aus einer Quelle versorgt.",
    p2="<b>Dann drei Kanäle mit klaren Rollen:</b> Meta für Nachfrage, Google für den Abverkauf, Pinterest als unterschätzter Effizienz-Kanal für eine Marke, deren Produkt von Bildern lebt. Saisonal getaktet auf Weihnachten und Valentinstag, wöchentlich gelesen, wöchentlich umgeschichtet.",
    links=[("service-ecommerce.html", "E-Commerce Growth"), ("service-performance-marketing.html", "Performance Marketing")])]),
 "case-crowdinvesting": dict(
  rahmen="Finance, Crowdinvesting<br>Zwei POC-Phasen, laufend<br>Meta, Google, Funnel, UGC",
  disz=[("Strategie & Funnel", "service-strategie.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  learn=["Struktur schlägt Einzelkampagne.",
         "Die KPI-Definition vorab ist die halbe Miete.",
         "Eine laufende Plattform-Kampagne schlägt die Einzelkampagne beim Return um den Faktor 2,5.",
         "Gleicher Spend, anderes Ergebnis: Der Beweis liegt im Vorher-Nachher."],
  chapters=[dict(label="Zweites Kapitel, die Skalierung", h=["Vom Beweis", "zur Maschine."],
    p1="Nach dem ersten Proof of Concept kam der zweite, mit einer Hypothese: nicht mehr das einzelne Projekt bewerben, sondern die Plattform. Gemeinsame Daten über alle Emissionen, eine laufende Kampagne statt Stop-and-go, Google als Abschlusskanal für die Nachfrage, die Meta erzeugt. Dazu Talking-Head-Videos und UGC statt Stockbilder.",
    p2="<b>Das Budget wurde mehr als verdreifacht, der Return stieg trotzdem:</b> 67.180 Euro Mediabudget brachten 114 Investments und 1,26 Millionen Euro Kapital, ein ROAS von 18,7. Die reine Plattform-Kampagne lag bei 42, die Markensuche bei Google über 100. Und das durchschnittliche Investment war fast dreimal so hoch wie geplant.",
    nums=[("(ROAS, zweite POC-Phase)", "18,7"), ("(Kapital in drei Monaten)", "€ 1,26 Mio."), ("(Investments)", "114"), ("(Ø Investment, Ziel € 3.800)", "€ 11.039")],
    note="Vergütung in dieser Phase: Selbstkosten plus Beteiligung am zurechenbaren Zeichnungsvolumen. Wir haben nur verdient, wenn gezeichnet wurde. Geschwister-Varianten desselben Motivs fielen durch, und die Markensuche erntet Nachfrage, sie erzeugt sie nicht.",
    links=[("service-strategie.html", "Strategie & Funnel"), ("service-content-creation.html", "Content Creation")])]),
 "case-wohnbau-floridsdorf": dict(
  rahmen="Real Estate, Wohnbau<br>Seit Jänner 2026, laufend<br>Meta Instant Forms, Website, Landingpage",
  learn=["Eigennutzer und Anleger sind zwei Märkte, kein gemeinsamer.",
         "Anleger wollen Rendite-Sicherheit, keine Zertifikate.",
         "Was die Plattform zählt und was im Postfach ankommt, sind zwei Zahlen. Wir berichten beide.",
         "Ehrlicher CPL entsteht durch Testing."],
  chapters=[dict(label="Zweites Kapitel, das zweite Quartal", h=["Volumen war da.", "Verbindlichkeit fehlte."],
    p1="Im zweiten Quartal kamen weitere 232 Anfragen zu 16,60 Euro. Die Auswertung mit dem Vertrieb zeigte den Engpass hinter der Zahl: Viele Interessenten waren nach dem Formular schwer erreichbar, der Erstkontakt kam zu spät, und was Meta als Anfrage zählte, war nicht immer das, was im Postfach des Kunden ankam.",
    p2="<b>Unsere Antwort war kein größeres Budget, sondern eine andere Strecke:</b> weg vom reinen Instant Form, hin zu Website-Anfragen mit eigener Projekt-Landingpage, Terminbuchung und einer Rückruf-Logik, die den Vertrieb schneller macht. Weniger Anfragen, dafür bessere. Genau das, was ein Bauträger braucht, um zu verkaufen.",
    nums=[("(Anfragen im zweiten Quartal)", "232"), ("(gewichteter CPL Q2)", "€ 16,60"), ("(Meta zählte in drei Wochen)", "18"), ("(im Postfach ankamen)", "8")],
    note="Die Differenz zwischen Plattform-Zählung und echten Anfragen ist kein Schönheitsfehler, sondern die wichtigste Zahl im Report. Wir klären sie, bevor wir optimieren."),
   dict(label="Drittes Kapitel, die Landingpage", h=["Eine eigene Seite", "für das Projekt."],
    p1="Die Bauträger-Website war für das Portfolio gebaut, nicht für eine Kampagne. Deshalb bekam das Projekt eine eigene Landingpage: ein Versprechen, eine Preisspanne, ein Formular, eine Terminbuchung, alles in der Bildsprache der Sujets, die darauf führen.",
    p2="Seit August laufen die Kampagnen auf diese Seite. Damit ist die Strecke vom ersten Kontakt bis zum Beratungstermin durchgehend in unserer Hand und messbar.",
    links=[("service-websites.html", "Websites & Landingpages"), ("service-performance-marketing.html", "Performance Marketing")])],
  quote=("Vielen lieben Dank zunächst für die tollen Creatives. Ausführung und Umsetzung gefallen uns bereits sehr gut!", "Marketing, Wiener Bauträger")),
 "case-consumer-brand": dict(
  rahmen="Consumer, Beverage-Lifestyle<br>Saison-Peaks, Produktlaunch<br>Meta, Kampagnen-Site",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html"), ("Websites & Landingpages", "service-websites.html")],
  chapters=[dict(label="Zweites Kapitel, der Produktlaunch", h=["Eine Seite, drei Sprachen,", "vier Termine."],
    p1="Für ein neues Produkt der Marke haben wir die Kampagnen-Site gebaut, an der die gesamte Einführung hing: Messe in Frankfurt im Februar, US-Messen Ende Februar, B2B-Start in Kanada im März, Launch in Österreich, Deutschland und den USA im April. Deutsch, Englisch, Französisch, ein Formular für Händler und Endkunden, Anbindung an das CRM des Kunden.",
    p2="<b>Der Content der Kreativagentur kam spät, die Termine standen.</b> Also haben wir mit Platzhaltern gebaut, in Etappen live gestellt und die Seite bis heute weiterentwickelt: neue Produktfarben, Bewegtbild im Header, mobile Videos. Ein Learning aus der Performance-Zeit gilt auch hier: Ein Produkt, das nicht lieferbar ist, zerstört jede Lernphase der Kampagne.",
    links=[("case-web-twistnsparkle.html", "Die Kampagnen-Site im Detail"), ("service-websites.html", "Websites & Landingpages")])],
  quote=("Mit der Zusammenarbeit im Performance-Bereich war und bin ich sehr zufrieden, und auch die Ergebnisse können sich sehen lassen.", "Teamlead E-Commerce, Consumer-Marke")),
 "case-bautraeger-portfolio": dict(
  rahmen="Real Estate, Wohnbau<br>Laufend, drei Projekte<br>Meta Instant Forms, Landingpages",
  disz=[("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html"), ("Websites & Landingpages", "service-websites.html")],
  chapters=[dict(label="Zweites Kapitel, zwei Projekte im zweiten Quartal", h=["Zwei Projekte,", "ein System, ein Quartal."],
    p1="Im zweiten Quartal 2026 liefen zwei Projekte des Portfolios parallel mit derselben Mechanik: getrennte Zielgruppen, wenige Sujets im Test, wöchentliche Umschichtung auf den Sieger. Das eine Projekt brachte 287 Anfragen zu 6,33 Euro, das andere 259 Anfragen zu 5,93 Euro, dem besten Preis im gesamten Portfolio.",
    p2="<b>In beiden Projekten trug ein einziges Sujet über 90 Prozent der Anfragen.</b> Das ist kein Zufall, sondern der Grund, warum wir testen, statt zu diskutieren: Der Sieger steht nach zwei Wochen fest, danach fließt jeder Euro dorthin.",
    nums=[("(Anfragen, Projekt A)", "287"), ("(CPL, Projekt A)", "€ 6,33"), ("(Anfragen, Projekt B)", "259"), ("(CPL, Projekt B)", "€ 5,93")],
    note="Spend im Quartal: 1.817 Euro und 1.535 Euro, Reichweite 79.648 und 59.250 Personen. Alle Werte aus dem Quartalsreport an den Kunden."),
   dict(label="Drittes Kapitel, nach dem Lead", h=["Der Engpass sitzt", "hinter dem Formular."],
    p1="Die CRM-Auswertung zeigte, was Kampagnenzahlen nicht zeigen: 44 Prozent der Anfragen waren beim ersten Versuch nicht erreichbar, bei über 90 Prozent stand 'erneut kontaktieren' im System. Preis oder Lage waren fast nie der Einwand.",
    p2="Deshalb bauen wir seit dem Sommer die Strecke um: eigene Projekt-Landingpages statt Portfolio-Website, Terminbuchung statt Rückruf-Lotterie, und ein Reporting, das die Erstkontakt-Zeit des Vertriebs genauso ausweist wie den CPL.",
    links=[("service-websites.html", "Websites & Landingpages"), ("service-performance-marketing.html", "Performance Marketing")])],
  quote=("Danke für den Start. Wir haben schon einige Leads seit gestern Abend hereinbekommen.", "Verkauf, Wiener Bauträger, am Morgen nach dem Kampagnenstart")),
 "case-health-brand": dict(
  rahmen="E-Commerce, Health<br>Seit Herbst 2025, laufend<br>Meta, Google, Creator, Workshop",
  disz=[("E-Commerce Growth", "service-ecommerce.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html"), ("Strategie & Funnel", "service-strategie.html")],
  chapters=[dict(label="Zweites Kapitel, der Weg zum Ziel", h=["Ein Ziel-Gap ist", "ein Arbeitsauftrag."],
    p1="Der Report zeigte 1,07 bei Ziel 1,50. Statt die Zahl zu erklären, haben wir den Weg gebaut: Der Creator schlug das Produktvideo beim Preis je Kauf um mehr als die Hälfte, 82 Euro gegen 215 bis 232 Euro, die Rabatt-Statics brachten den besten Return, Retargeting blieb der effizienteste Euro.",
    p2="<b>Daraus wurde die Roadmap für das Jahr:</b> Advertorial-Landingpage, Video Sales Letter, Newsletter, Split-Tests auf der Produktseite, Ziel-Return in Stufen von 1,4 über 1,6 auf über 1,8. Begonnen hat alles mit einem Strategie-Workshop, in dem Produkt, Zielgruppe und Zahlenlogik auf einen Tisch kamen.",
    nums=[("(Creator, Preis je Kauf)", "€ 82"), ("(Produktvideo, Preis je Kauf)", "€ 215"), ("(bester Return, Rabatt-Static)", "1,37"), ("(Zielstufen im Jahr)", "3")],
    note="Die Stufen: 1,4 im Mai, 1,6 im Juni, über 1,8 ab Juli. Jede Stufe hat einen Hebel, der sie tragen soll, und ein Datum, an dem sie gemessen wird.",
    links=[("service-strategie.html", "Strategie & Funnel"), ("service-content-creation.html", "Content Creation")])],
  quote=("Wir wollten uns nur kurz für den produktiven und inspirierenden Workshop gestern bedanken, es hat uns viel Freude gemacht.", "Geschäftsführer, Health-Marke")),
}
for _c in CASES:
    _c.update(EXTRA.get(_c["slug"], {}))

# Hero-Zeilen als echte Headlines, keine Erklaerungen
SUBS = {
 "case-immobilien-investment": "Aus 36.000 Euro wurden 4,65 Millionen. Zurechenbar.",
 "case-d2c-lifestyle": "Das beste Jahr der Firma. Aus demselben Traffic.",
 "case-crowdinvesting": "Gleiches Budget. Viermal mehr Kapital.",
 "case-wohnbau-floridsdorf": "Zwei Märkte, ein Projekt. Sauber getrennt gewonnen.",
 "case-consumer-brand": "Wenn alle schreien, gewinnt Relevanz.",
 "case-bautraeger-portfolio": "Ein System. Drei Projekte. Der beste Preis im Portfolio.",
 "case-health-brand": "Ehrlich gerechnet. Und trotzdem gewachsen.",
 "case-photovoltaik": "Der Konfigurator ist das Creative.",
}
for _c in CASES:
    if _c["slug"] in SUBS:
        _c["sub"] = SUBS[_c["slug"]]


def _chapters(c):
    out = []
    for i, k in enumerate(c.get("chapters", [])):
        # Kapitel wechseln den Grund ab: creme, papier, creme
        bg, bgcls = ("#EFE7D6", "bg-cream") if i % 2 == 0 else ("#F3EDE1", "bg-paper")
        head = "".join('<span class="rl"><span>%s</span></span>' % x for x in k["h"])
        links = ""
        if k.get("links"):
            links = ('        <div data-fade style="display:flex;gap:clamp(22px,3vw,44px);flex-wrap:wrap;margin-top:22px">\n'
                     + "".join('          <a class="zalink" href="%s">%s</a>\n' % l for l in k["links"]) + '        </div>\n')
        nums = ""
        if k.get("nums"):
            nums = ('    <div class="wrap" style="margin-top:clamp(44px,5.5vw,80px)">\n      <div class="cnums" data-stagger>\n'
                    + "\n".join('        <div class="n" data-fade><div class="l">%s</div><div class="v num serif">%s</div></div>' % (l, v) for l, v in k["nums"])
                    + '\n      </div>\n' + ('      <p class="cfoot-note" data-fade>%s</p>\n' % k["note"] if k.get("note") else "") + '    </div>\n')
        out.append('  <!-- KAPITEL: %s -->\n'
                   '  <section class="sec fg-light %s" data-bg="%s" data-fg="dark">\n'
                   '    <div class="wrap lchap">\n'
                   '      <div>\n'
                   '        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">%s</span>\n'
                   '        <h2 class="dispn" data-lines style="font-size:clamp(26px,2.7vw,42px)">%s</h2>\n'
                   '      </div>\n'
                   '      <div data-stagger>\n'
                   '        <p class="lt3" data-fade>%s</p>\n'
                   '        <p class="lt3" data-fade>%s</p>\n'
                   '%s'
                   '      </div>\n'
                   '    </div>\n'
                   '%s'
                   '  </section>\n\n' % (k["label"].upper(), bgcls, bg, k["label"], head, k["p1"], k["p2"], links, nums))
    return "".join(out)


def _cquote(c):
    q = c.get("quote")
    if not q:
        return ""
    return ('  <!-- WAS DER KUNDE SAGT -->\n'
            '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">\n'
            '    <div class="wrap" style="max-width:980px">\n'
            '      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(22px,3vw,40px)">Was der Kunde sagt</span>\n'
            '      <p class="serif" data-fade style="font-size:clamp(24px,2.6vw,40px);line-height:1.3;letter-spacing:-0.01em">&bdquo;%s&ldquo;</p>\n'
            '      <div data-fade style="margin-top:22px;font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--grey-dark)">%s</div>\n'
            '    </div>\n'
            '  </section>\n\n') % q


def case_page(c, nxt):
    world = c.get("clr", "#22382C")
    wfg = c.get("fg", "#EDF2EC")
    if c.get("img"):
        hero = """<section class="chero" data-bg="%s" data-fg="light">
    <img src="%s" alt="%s">
    <div class="hcap">
      <div class="cl" style="font-size:15px">%s <span>%s</span></div>
      <div class="dispn" style="--n:%d">%s</div>
    </div>
    <div class="hkpi"><div class="kv">%s</div><div class="kl">(%s)</div></div>
    <div class="scrollhint">Scrollen</div>
  </section>""" % (world, c["img"], c["nav_title"], c["nav_title"], c["rahmen"].split("<br>")[0].split(",")[0].strip(), len(c["sub"]), c["sub"], c["big"], c["biglabel"])
    else:
        hero = """<section class="chero" data-bg="%s" data-fg="light" style="background:%s;color:%s">
    <div class="hcap">
      <div class="cl" style="font-size:15px">%s <span style="opacity:.65">%s</span></div>
      <div class="dispn" style="--n:%d">%s</div>
    </div>
%s
    <div class="scrollhint">Scrollen</div>
  </section>""" % (world, world, wfg, c["nav_title"], c["rahmen"].split("<br>")[0].split(",")[0].strip(), len(c["sub"]), c["sub"],
                   "")  # Farbwelt-Hero ohne Kennzahl, die Zahl steht im Ergebnis
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
            nxt_media = '<span style="display:flex;align-items:flex-end;aspect-ratio:4/3;background:%s;color:%s;padding:24px;border-radius:3px"><span style="font-family:var(--f-disp);font-weight:680;font-size:clamp(40px,4vw,64px);font-variant-numeric:tabular-nums">%s</span></span>' % (nxt.get("clr", "#22382C"), nxt.get("fg", "#EDF2EC"), nxt.get("big") or nxt["nav_title"])
    nxt_href = nxt["slug"] + ".html"
    page = HEAD.format(title="Case, " + c["nav_title"], bodybg=world) + menu("work.html", back=True) + """<main>

  <!-- HERO: Vollbild in der Case-Farbwelt -->
  """ + hero + """

  <!-- INTRO auf Papier: Story links, Key Facts rechts -->
  <section class="sec fg-light cintro bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap grid">
      <div>
        <span class="label" style="color:var(--grey-dark)">""" + c["rahmen"].replace("<br>", ", ") + """</span>
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
      <h2 class="dispn" data-lines>
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

""" + (("""  <!-- ERGEBNIS -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:0">
    <div class="wrap">
      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(30px,4vw,50px)">Ergebnis</span>
      <div class="cnums" data-stagger>
""" + nums + """
      </div>
      <p class="cfoot-note" data-fade>""" + c["note"] + """</p>
    </div>
  </section>

""") if c.get("nums") else "") + _chapters(c) + _cquote(c) + phones_sec + """  <!-- LEARNINGS -->
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

if __name__ == "__main__":
    for i, c in enumerate(CASES):
        if c.get("handmade"):
            continue
        nxt = CASES[(i + 1) % len(CASES)]
        open(c["slug"] + ".html", "w", encoding="utf-8").write(case_page(c, nxt))
        print("case", c["slug"])
    print("cases done")

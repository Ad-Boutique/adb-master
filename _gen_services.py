# Service-LP-Generator: Schema Problem → Konsequenz → Lösung → Differenzierung →
# Proof ×3 → Logos → Case-Liste → FAQ → No-Brainer + Risikoumkehr → CTA
# -*- coding: utf-8 -*-
from _gen import HEAD, FOOTER, menu, logocycle, logogrid, CASES
from _gen_web import WEBCASES

def logos_row(names, label):
    imgs = "\n      ".join('<img loading="lazy" decoding="async" src="assets/logos/%s.png" alt="%s">' % (n, n) for n in names)
    return '''  <!-- LOGOS -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: clamp(44px,5vw,70px) 0">
    <div class="wrap" style="display:flex;align-items:center;gap:clamp(28px,4vw,64px);flex-wrap:wrap;border-top:1px solid var(--line-l);border-bottom:1px solid var(--line-l);padding-top:34px;padding-bottom:34px">
      <span class="label" style="color:var(--grey-dark)">%s</span>
      <div class="logowall" style="flex:1">
      %s
      </div>
    </div>
  </section>

''' % (label, imgs)

SVC_COLS = {"service-ecommerce": [["assets/case/juwel/g0.jpg", "assets/case/juwel/g2.jpg", "assets/case/medcenter/g4.jpg", "assets/case/case-health-brand/g3.jpg", "assets/case/case-web-ib7/g1.jpg"], ["assets/case/medcenter/g0.jpg", "assets/case/medcenter/g2.jpg", "assets/case/case-consumer-brand/v0.mp4", "assets/case/case-consumer-brand/g0.jpg", "assets/case/grandgarden/g3.jpg"], ["assets/case/grandgarden/g0.jpg", "assets/case/grandgarden/g2.jpg", "assets/case/case-health-brand/v0.mp4", "assets/case/case-health-brand/g0.jpg", "assets/case/case-web-ib7/g4.jpg"], ["assets/case/juwel/g1.jpg", "assets/case/juwel/g3.jpg", "assets/case/grandgarden/v0.mp4", "assets/case/case-health-brand/g1.jpg", "assets/case/case-web-ib7/g0.jpg"], ["assets/case/medcenter/g1.jpg", "assets/case/medcenter/g3.jpg", "assets/case/case-health-brand/v1.mp4", "assets/case/grandgarden/g1.jpg", "assets/case/juwel/g5.jpg"], ["assets/case/case-health-brand/g2.jpg", "assets/case/juwel/g4.jpg", "assets/case/case-web-ib7/g2.jpg", "assets/case/case-web-ib7/g3.jpg", "assets/case/case-web-ib7/g5.jpg"]], "service-performance-marketing": [["assets/case/case-premium-neubau/g0.jpg", "assets/case/case-premium-neubau/g1.jpg", "assets/case/medcenter/g2.jpg", "assets/case/case-immobilien-investment/v0.mp4", "assets/case/grandgarden/g3.jpg"], ["assets/case/grandgarden/g0.jpg", "assets/case/case-wohnbau-floridsdorf/g1.jpg", "assets/case/juwel/g2.jpg", "assets/case/herogroup/v0.mp4", "assets/case/case-premium-neubau/g4.jpg"], ["assets/case/case-wohnbau-floridsdorf/g0.jpg", "assets/case/medcenter/g1.jpg", "assets/case/case-premium-neubau/g3.jpg", "assets/case/case-immobilien-investment/v1.mp4", "assets/case/herogroup/g1.jpg"], ["assets/case/medcenter/g0.jpg", "assets/case/juwel/g1.jpg", "assets/case/case-wohnbau-floridsdorf/g3.jpg", "assets/case/herogroup/v1.mp4", "assets/case/case-immobilien-investment/g1.jpg"], ["assets/case/juwel/g0.jpg", "assets/case/case-premium-neubau/g2.jpg", "assets/case/medcenter/g3.jpg", "assets/case/grandgarden/v0.mp4", "assets/case/case-immobilien-investment/g0.jpg"], ["assets/case/herogroup/g0.jpg", "assets/case/grandgarden/g2.jpg", "assets/case/juwel/g3.jpg", "assets/case/grandgarden/g1.jpg", "assets/case/case-wohnbau-floridsdorf/g2.jpg"]], "service-content-creation": [["assets/case/juwel/g0.jpg", "assets/case/medcenter/g1.jpg", "assets/case/case-premium-neubau/g2.jpg", "assets/case/kommunalkredit/g0.jpg", "assets/case/kommunalkredit/g2.jpg"], ["assets/case/grandgarden/g0.jpg", "assets/case/case-premium-neubau/g1.jpg", "assets/case/juwel/g3.jpg", "assets/case/case-health-brand/g0.jpg", "assets/case/kommunalkredit/g3.jpg"], ["assets/case/medcenter/g0.jpg", "assets/case/juwel/g2.jpg", "assets/case/medcenter/g3.jpg", "assets/case/kommunalkredit/g1.jpg", "assets/case/case-health-brand/g3.jpg"], ["assets/case/herogroup/g0.jpg", "assets/case/case-health-brand/g2.jpg", "assets/case/case-premium-neubau/g3.jpg", "assets/case/case-health-brand/g1.jpg", "assets/case/grandgarden/g3.jpg"], ["assets/case/case-premium-neubau/g0.jpg", "assets/case/grandgarden/g2.jpg", "assets/case/juwel/g4.jpg", "assets/case/grandgarden/g1.jpg", "assets/case/kommunalkredit/g4.jpg"], ["assets/case/juwel/g1.jpg", "assets/case/medcenter/g2.jpg", "assets/case/herogroup/v0.mp4", "assets/case/herogroup/v1.mp4", "assets/case/herogroup/g1.jpg"]], "service-websites": [["assets/case/case-web-noma/g0.jpg", "assets/case/case-premium-neubau/g3.jpg", "assets/case/grandgarden/g3.jpg", "assets/case/case-web-ib7/g0.jpg", "assets/case/case-web-noma/g2.jpg"], ["assets/case/case-premium-neubau/g0.jpg", "assets/case/grandgarden/v0.mp4", "assets/case/case-web-ib7/g2.jpg", "assets/case/case-web-pharmacom/g0.jpg", "assets/case/case-web-noma/g3.jpg"], ["assets/case/grandgarden/g0.jpg", "assets/case/grandgarden/v1.mp4", "assets/case/case-web-ib7/g3.jpg", "assets/case/case-web-trattner/g0.jpg", "assets/case/case-web-noma/g4.jpg"], ["assets/case/case-premium-neubau/g1.jpg", "assets/case/case-premium-neubau/v0.mp4", "assets/case/case-web-noma/g1.jpg", "assets/case/case-web-ib7/g4.jpg", "assets/case/case-web-noma/g5.jpg"], ["assets/case/case-premium-neubau/g2.jpg", "assets/case/grandgarden/v2.mp4", "assets/case/case-web-trattner/g1.jpg", "assets/case/case-premium-neubau/g4.jpg", "assets/case/case-web-ib7/g1.jpg"], ["assets/case/grandgarden/g2.jpg", "assets/case/case-premium-neubau/v1.mp4", "assets/case/grandgarden/g1.jpg", "assets/case/case-premium-neubau/g5.jpg", "assets/case/case-web-ib7/g5.jpg"]], "service-strategie": [["assets/case/grandgarden/g0.jpg", "assets/case/case-premium-neubau/g2.jpg", "assets/case/case-crowdinvesting/g0.jpg", "assets/case/kommunalkredit/g1.jpg", "assets/case/kommunalkredit/g4.jpg"], ["assets/case/herogroup/g0.jpg", "assets/case/case-premium-neubau/g3.jpg", "assets/case/kommunalkredit/g0.jpg", "assets/case/case-crowdinvesting/g2.jpg", "assets/case/case-premium-neubau/g4.jpg"], ["assets/case/case-premium-neubau/g0.jpg", "assets/case/case-crowdinvesting/g4.jpg", "assets/case/grandgarden/g1.jpg", "assets/case/kommunalkredit/g2.jpg", "assets/case/case-crowdinvesting/g5.jpg"], ["assets/case/case-crowdinvesting/g1.jpg", "assets/case/case-immobilien-investment/v0.mp4", "assets/case/herogroup/v1.mp4", "assets/case/case-crowdinvesting/g3.jpg", "assets/case/herogroup/g1.jpg"], ["assets/case/case-premium-neubau/g1.jpg", "assets/case/herogroup/v0.mp4", "assets/case/grandgarden/v0.mp4", "assets/case/grandgarden/g3.jpg", "assets/case/case-immobilien-investment/g1.jpg"], ["assets/case/grandgarden/g2.jpg", "assets/case/case-immobilien-investment/v1.mp4", "assets/case/herogroup/v2.mp4", "assets/case/kommunalkredit/g3.jpg", "assets/case/case-immobilien-investment/g0.jpg"]], "service-chatgpt-ads": [["assets/img/ag_strategy.jpg", "assets/img/ag_cam1.jpg", "assets/img/retreat-06.jpg"], ["assets/img/ag_board1.jpg", "assets/img/ag_shoot1.jpg", "assets/img/retreat-08.jpg"], ["assets/img/ag_talk.jpg", "assets/img/ag_vision1.jpg", "assets/img/ag_cam2.jpg"], ["assets/img/ag_meeting.jpg", "assets/img/ag_poster.jpg", "assets/img/ag_vision2.jpg"], ["assets/img/ag_review.jpg", "assets/img/retreat-02.jpg", "assets/img/retreat-01.jpg"], ["assets/img/ag_laugh.jpg", "assets/img/retreat-04.jpg", "assets/img/retreat-10.jpg"]]}

SVC_WALL = {"service-content-creation": [["assets/case/juwel/g0.jpg", "assets/case/herogroup/g0.jpg", "assets/case/medcenter/g1.jpg", "assets/case/grandgarden/g2.jpg"], ["assets/case/kommunalkredit/g0.jpg", "assets/case/juwel/g1.jpg", "assets/case/herogroup/v0.mp4", "assets/case/medcenter/g2.jpg"], ["assets/case/case-health-brand/g0.jpg", "assets/case/kommunalkredit/g1.jpg", "assets/case/juwel/g2.jpg", "assets/case/herogroup/v1.mp4"], ["assets/case/grandgarden/g0.jpg", "assets/case/case-health-brand/g1.jpg", "assets/case/kommunalkredit/g2.jpg", "assets/case/juwel/g3.jpg"], ["assets/case/medcenter/g0.jpg", "assets/case/grandgarden/g1.jpg", "assets/case/case-health-brand/g2.jpg", "assets/case/kommunalkredit/g3.jpg"]], "service-websites": [["assets/img/web_daphi_m.jpg", "assets/img/web_northpoint_m.jpg", "assets/case/case-consumer-brand/m0.jpg", "assets/case/case-web-ib7/m2.jpg"], ["assets/img/web_funkhausliving_m.jpg", "assets/img/web_pharmacom_m.jpg", "assets/case/case-premium-neubau/m0.jpg", "assets/case/case-web-northpoint/m0.jpg"], ["assets/img/web_havenstone_m.jpg", "assets/img/web_trattner_m.jpg", "assets/case/case-premium-neubau/m1.jpg", "assets/case/case-web-pharmacom/m0.jpg"], ["assets/img/web_ib7_m.jpg", "assets/img/web_twistnsparkle_m.jpg", "assets/case/case-web-ib7/m0.jpg", "assets/case/case-web-trattner/m0.jpg"], ["assets/img/web_noma_m.jpg", "assets/img/web_unio_m.jpg", "assets/case/case-web-ib7/m1.jpg", "assets/img/web_funkhausliving_m.jpg"]]}

SERVICES = [
 dict(slug="service-ecommerce", nav="E-Commerce Growth", label="Leistung, E-Commerce Growth",
  h1=["Ihr Shop wächst.", "Planbar."], ital=1,
  tags=["Meta, Google, TikTok, Pinterest", "Shop & Conversion", "Server-side Tracking", "UGC & Creatives"],
  sub="Ads, Creatives, Shop und Tracking aus einer Hand, vergütet am Ergebnis.",
  problem_h=["Das Problem"],
  problem=["Sie kaufen Besucher, aber zu wenige kaufen: Steigende Klickpreise drücken die Marge, der Checkout verliert Käufer, und das Reporting verschleiert mehr, als es zeigt.",
           "<b>Mehr Budget skaliert dann nur das Problem.</b> Jeder Monat mit undichtem Funnel wird teurer, während Wettbewerber mit sauberem Setup denselben Klick in mehr Umsatz übersetzen."],
  intro="Mehr <b>Spend</b> löst selten das Problem. Der Hebel liegt im Zusammenspiel aus <b>Creative</b>, <b>Shop</b> und <b>Messung</b>. Wir bauen das System, nicht die Einzelmaßnahme.",
  acc=[("Ads & Creatives", "Iteratives Creative-Testing statt Bauchgefühl: Wir lassen Varianten gegeneinander laufen und schichten Budget wöchentlich auf die Gewinner um.",
        ["Meta, Google, TikTok, Pinterest", "UGC- und Studio-Produktion", "Systematisches Creative-Testing", "Budget-Steuerung, wöchentlich"]),
       ("Shop & Conversion", "Mehr Umsatz beginnt fast immer im Checkout, nicht im Ad-Account. Wir optimieren dort, wo der Klick zu Geld wird.",
        ["Landingpages je Kampagne", "Checkout- und Produktseiten", "A/B-Tests mit klaren Hypothesen", "Angebots- und Bundle-Logik"]),
       ("Tracking & Daten", "Ehrliche Attribution verhindert, dass dieselbe Conversion zweimal gefeiert wird. Ein Dashboard, alle Kanäle, Blended-Sicht.",
        ["Server-side Tracking, consent-konform", "Ein Dashboard, alle Kanäle", "Blended-ROAS statt Kanal-Ego", "Saubere Produkt-Feeds"]),
       ("Reporting & Modell", "Wöchentliches Reporting, auch wenn es unbequem ist: Ziel-Gaps stehen bei uns im Report, nicht im Kleingedruckten.",
        ["Wöchentliches Reporting", "Ehrliche Ziel-Gaps", "Basis-Fixum plus Umsatzbeteiligung", "Kein Ticketsystem, direkter Draht"])],
  diff=[("Anders als üblich", "System statt Einzelmaßnahme", "Creatives, Landingpages, Angebot und Tracking greifen ineinander, mit klaren Zielwerten je Kanal. Eine schöne Kampagne auf einem undichten Shop ist verbranntes Budget.", "assets/img/ag_strategy.jpg"),
        ("Anders als üblich", "Ehrlichkeit im Reporting", "Blended-Sicht statt Kanal-Ego: Was nicht funktioniert, steht im Report und wird gestoppt, bevor es teuer wird.", "assets/img/retreat-04.jpg"),
        ("Anders als üblich", "Skin in the Game", "Unsere Vergütung ist an den messbaren Umsatz gekoppelt. Wir gewinnen nur, wenn Sie gewinnen.", "assets/img/ag_meeting.jpg")],
  zoom=dict(img="assets/img/c_candle.jpg", side="right", al="Ein Fall",
            ah=["Erst messen.", "Dann skalieren."],
            alink=("case-d2c-lifestyle.html", "Den Fall im Detail"), aside="Erst messen, dann skalieren: Der Hebel lag im Checkout und im Creative, nicht im Budget.",
            zl="D2C-Lifestyle-Marke, Meta, Google, Pinterest", zt="+57 % Jahresumsatz. Blended ROAS 5,57."),
  proof_h=["Ein Shop.", "Jede Stufe nachgerechnet."],
  proof_lead="Statt Bestwerte aus mehreren Marken nebeneinanderzustellen, nehmen wir eine D2C-Lifestyle-Marke und zeigen die Kette: Mediabudget, Kanal-Mix, Blended-Sicht, Jahresumsatz.",
  proof_nums=[],
  tell=dict(
    h="Ein Jahr, vier Zahlen.",
    t="Wie aus € 56k Mediabudget € 312k Umsatz wurden, Station für Station statt als Bestwert.",
    steps=[
      ("€ 56k", "Mediabudget im Jahr", "Das Budget",
       "Verteilt auf Meta, Google und Pinterest. Die Frage war nie, ob mehr Budget hilft, sondern welcher Kanal welchen Euro verdient."),
      ("6,99", "ROAS im stärksten Kanal", "Der Kanal-Mix",
       "Pinterest lief auf 6,99, Google folgte mit 5,98. Statt den Sieger zu feiern, haben wir Budget wöchentlich umgeschichtet."),
      ("4,17", "Blended ROAS inklusive Fee", "Die ehrliche Zahl",
       "Inklusive Agentur-Fee blieb der Blend bei 4,17. Diese Zahl steht bei uns im Report, nicht die schönste Kanalzahl."),
      ("€ 312k", "Umsatz aus dem Mediabudget", "Das Jahr",
       "Plus 57 Prozent gegenüber dem Vorjahr, bei 56 Prozent mehr Bestellungen. Aus demselben Traffic, anders geführt."),
    ]),
  channels=dict(
    label="Return on Ad Spend je Kanal, D2C-Lifestyle-Marke",
    rows=[("Pinterest", 100, "6,99"), ("Google", 86, "5,98"), ("Blended, inkl. Fee", 60, "4,17")],
    note="Kein Kanal-Ego: Wir reporten den Blend inklusive unserer Fee, weil nur das die Marge des Shops beschreibt.",
    link=("case-d2c-lifestyle.html", "D2C-Lifestyle-Marke im Detail")),
  proofsplit=dict(label="Zwei Blickwinkel",
                  h=["Was die Kanalzahl", "verschweigt."],
                  t="Links der Kanal-Vergleich einer D2C-Marke: Pinterest führt, Google folgt, der Blend liegt darunter. Rechts, was ein Kunde daraus mitnimmt. Beides gehört zusammen, sonst liest man nur die Hälfte."),
  crew=dict(label="Wer daran arbeitet",
            h=["Vier Rollen,", "die am Umsatz hängen."],
            t="Shop, Creative und Kampagne entstehen im selben Team. Wer den Checkout ändert, sitzt auch im Call über den ROAS.",
            people=[("Fabi", "Performance Manager", "Steuert die Kanäle und schichtet Budget wöchentlich auf die Gewinner um.", "assets/img/ag_strategy.jpg"),
                    ("Suman", "Social Media", "Baut die Sujets, die im Feed gegeneinander antreten, und liest die Kommentare mit.", "assets/img/team/suman.jpg"),
                    ("Evgenia", "Design", "Gestaltet Produktseiten und Angebotslogik dort, wo der Klick zu Geld wird.", "assets/img/team/evgenia.jpg"),
                    ("Martin", "Founder", "Verantwortet die Blended-Sicht und sagt, wenn ein Kanal gestoppt wird.", "assets/img/team/martin.jpg")]),
  voice=dict(label="Was Kunden sagen",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Solche Sätze stehen bei uns im Reporting, nicht im Kleingedruckten. Einmal im Monat gehen wir sie gemeinsam durch, inklusive der Kanäle, die wir gestoppt haben."),
  fit=dict(label="Bevor wir starten",
           h=["Der Fit entscheidet.", "Nicht die Shopgröße."],
           yes_h="Wir passen zusammen, wenn",
           no_h="Wir sind die Falschen, wenn",
           intro="Wir sind keine Agentur, die Accounts sammelt. Wir sitzen in Ihren Meetings, kennen Ihre Marge und streiten mit Ihnen über Motive. Das funktioniert nur, wenn die Zusammenarbeit auf beiden Seiten passt, deshalb prüfen wir das vorher, offen und in beide Richtungen.",
           yes=["Sie haben Produkt-Markt-Fit und wollen skalieren, nicht testen",
                "Mediabudget ab etwa € 5k im Monat",
                "Der Shop darf angefasst werden: Produktseite, Checkout, Angebotslogik",
                "Sie wollen die Blended-Sicht sehen, nicht die schönste Kanalzahl"],
           no=["Der Shop soll unangetastet bleiben und nur Traffic bekommen",
               "Die Marge trägt keine bezahlten Klicks",
               "Es braucht Ergebnisse in zwei Wochen",
               "Reporting soll gut aussehen statt stimmen"]),
  steps_next=dict(
    h="Von der Anfrage zum Klartext.",
    rows=[("Heute", "Anfrage in zwei Minuten", "Was Sie verkaufen und wo es hängt. Zwei Sätze reichen."),
          ("Unter 24 h", "Ehrliche Ersteinschätzung", "Wir sagen, ob wir passen, und was wir vorab an Zugängen brauchen."),
          ("Tag 2 bis 10", "Shop- und Account-Audit", "Kampagnen, Creatives, Produktseiten, Checkout und Tracking, im Konto statt auf Screenshots."),
          ("Danach", "Klare Empfehlung", "Ein Termin, eine Seite: Wo Budget verdampft, wo die Marge liegt, was zuerst passiert.")]),
  deliver=["Audit über Kampagnenstruktur, Creatives, Tracking und Checkout",
           "Blended-Sicht über alle Kanäle in einem Dashboard",
           "Priorisierte Liste: was zuerst, was später, was gar nicht",
           "Ein Termin, in dem wir die Zahlen erklären statt sie zu senden"],
  trust=["Kein Vertrag für das Audit", "Zugänge bleiben bei Ihnen", "Vergütung am Ergebnis möglich"],
  proof_quote="„Pinterest führte mit ROAS 6,99, Google folgte mit 5,98. Inklusive Agentur-Fee blieb der Blend bei 4,17.“ Solche Sätze stehen bei uns im Reporting, nicht im Kleingedruckten.",
  visual=("panels", dict(label="Gebaute Auftritte",
                          h="Ein Shop verkauft nicht, weil er schön ist. Sondern weil jeder Schritt sitzt.",
                          t="Markenwelt, Produktseite und Checkout entstehen bei uns im selben Zug wie die Kampagne, die darauf führt. Was Sie hier sehen, läuft live und trägt Mediabudget.",
                          d1=("Commerce", "Shop-Systeme, Produktseiten, Checkout-Optimierung, Bundle- und Angebotslogik"),
                          d2=("Performance", "Meta, Google, Pinterest, Creative-Testing, Server-side Tracking"),
                          imgs=["assets/case/case-consumer-brand/d0.jpg", "assets/case/case-web-ib7/d0.jpg", "assets/img/web_twistnsparkle_d.jpg", "assets/case/case-web-ib7/d1.jpg"])),
  logos=["looops", "isi", "nordicspirit", "ilbosso", "kaisers", "jti", "juwel", "bojito"],
  oplist=[("case-consumer-brand.html", "Premium-Consumer-Brand", "4,02", "BFCM-ROAS, +75 %"),
          ("case-d2c-lifestyle.html", "D2C-Lifestyle-Marke", "+57 %", "Jahresumsatz, ROAS 5,57"),
          ("case-health-brand.html", "Dental-/Health-Marke", "1.385", "Verkäufe, ehrlich reportet"),
          ("case-nordic-spirit.html", "Nordic Spirit, JTI", "7.800", "Bestellungen im Monat am Peak, vorher 800")],
  faq=[("Wir haben schon eine Agentur. Warum wechseln?", "Nicht wechseln, vergleichen: Der Audit zeigt in zwei Wochen, wo Ihr Setup Geld liegen lässt. Danach entscheiden Sie mit Zahlen, nicht mit Bauchgefühl."),
       ("Was, wenn der ROAS nicht kommt?", "Dann verdienen wir weniger: Unsere Vergütung ist an den messbaren Umsatz gekoppelt. Skin in the Game heißt, dass Ihr Risiko auch unseres ist."),
       ("Wie schnell sehen wir Ergebnisse?", "Erste Signale nach dem Audit, belastbare Trends nach sechs bis acht Wochen Testing. Wir versprechen keine Wunder in Woche eins, dafür eine Kurve, die hält.")],
  offer_h="Der Einstieg ist ein Audit. Kein Vertrag.",
  offer=["Wir prüfen Ads, Shop, Tracking und Checkout und zeigen Ihnen in zwei Wochen konkret, wo Umsatz liegen bleibt. Danach entscheiden Sie: umsetzen mit uns, umsetzen ohne uns, oder gar nicht.",
         "<b>Und wenn wir zusammenarbeiten, gilt die Risikoumkehr:</b> Basis-Fixum plus Beteiligung am messbaren Umsatz. Wächst Ihr Umsatz nicht, verdienen wir weniger. Wo sich Umsatz nicht sauber messen lässt, sagen wir das vorher, nicht nachher."],
  chips=["Shop-Audit", "Ads-Setup", "UGC & Creatives", "Landingpage", "Tracking-Setup", "Conversion-Optimierung", "Zweitmeinung", "Growth-Partnerschaft"]),

 dict(slug="service-performance-marketing", nav="Performance Marketing", label="Leistung, Performance Marketing",
  tell=dict(
    h="Ein Projekt, vier Zahlen.",
    t="Wie aus einem überschaubaren Budget 489 qualifizierte Kaufinteressenten wurden, Station für Station.",
    steps=[
      ("€ 5.755", "Mediabudget, das eingesetzt wurde", "Das Budget",
       "Ein überschaubarer Betrag für ein Premium-Neubauprojekt in Wien. Die Frage war nie, ob mehr Budget hilft."),
      ("489", "qualifizierte Kaufinteressenten", "Die Leads",
       "Vier Motive im Test, konsequente Umschichtung auf den Sieger, gemessen über Instant Forms statt Website-Formular."),
      ("€ 11,77", "gewichteter Cost per Lead", "Der Preis pro Anfrage",
       "Das stärkste Motiv lieferte zu € 6,93. Der Schnitt über alle Motive blieb bei € 11,77, inklusive der Tests, die nicht liefen."),
      ("54 %", "aller Leads aus einem einzigen Motiv", "Die Erkenntnis",
       "Das Creative ist der Hebel, nicht das Budget. Genau deshalb testen wir, statt zu argumentieren."),
    ]),
  proofsplit=dict(label="Zwei Rechnungen",
                  h=["Wo der Unterschied", "wirklich entsteht."],
                  t="Links ein Wohnbau-Projekt: dieselbe Zielgruppe, dieselbe Woche, drei Strecken, sechsfacher Preisunterschied. Rechts eine Crowdinvesting-Plattform: nahezu gleiches Budget, andere Struktur. Beide Zahlen stehen so im Reporting, inklusive der Strecke, die wir gestoppt haben."),
  bars=dict(
    label="Return on Ad Spend, Crowdinvesting-Plattform",
    link=("case-crowdinvesting.html", "Crowdinvesting-Plattform im Detail"),
    rows=[("Vorher", 24, "2,14"), ("Mit uns", 100, "8,75")],
    note="Nahezu gleiches Budget, andere Struktur: aus 16 Investments wurden 50, die Kosten je Investor fielen um 69 Prozent."),
  channels=dict(
    label="Cost per Lead je Strecke, Wohnbau-Projekt",
    rows=[("Instant Form, Eigennutzer", 100, "€ 9,59"), ("Instant Form, Anleger", 88, "€ 8,43"),
          ("Website-Formular", 22, "€ 58,05")],
    note="Dieselbe Zielgruppe, dieselbe Woche: Die Strecke entscheidet über den Preis der Anfrage."),
  quote=("Endlich jemand, der nicht Reichweite feiert, sondern zeigt, wo der Euro wirklich landet.",
         "Head of Marketing, Commerce"),
  fit=dict(
    label="Bevor wir starten",
    h=["Der Fit entscheidet.", "Nicht das Budget."],
    yes_h="Wir passen zusammen, wenn",
    no_h="Wir sind die Falschen, wenn",
    intro="Wir übernehmen wenige Accounts, die dafür ganz. Wir verstehen uns als verlängerte Marketingabteilung: Wir sitzen in Ihren Runden, kennen Ihre Zahlen und widersprechen, wenn es nötig ist. Das trägt nur, wenn es auf beiden Seiten passt, deshalb prüfen wir den Fit vorher, offen und in beide Richtungen.",
    yes=["Sie geben bereits Mediabudget aus und wollen wissen, was es wirklich bringt",
         "Produkt oder Projekt trägt eine Marge, die Wachstum erlaubt",
         "Creatives dürfen angefasst werden, nicht nur das Werbekonto",
         "Entscheidungen fallen bei Ihnen schnell und direkt"],
    no=["Es geht um Reichweite, Awareness-Preise oder Followerzahlen",
        "Das Budget soll monatlich neu verhandelt werden",
        "Tracking und Datenzugriff bleiben verschlossen",
        "Der erste Monat soll bereits die Bilanz retten"]),
  steps_next=dict(
    h="Von der Anfrage zum Klartext.",
    rows=[("Heute", "Anfrage in zwei Minuten", "Kanäle, Budget, Ziel. Mehr brauchen wir für den Start nicht."),
          ("Unter 24 h", "Ehrliche Ersteinschätzung", "Ein Gründer sieht sich das an und meldet sich, auch wenn es ein Nein wird."),
          ("Tag 2 bis 5", "Account- und Tracking-Audit", "Struktur, Gebote, Zurechnung, Creatives. Wir schauen in die Konten, nicht auf Screenshots."),
          ("Danach", "Klare Empfehlung", "Top-3-Hebel, geschätztes Potenzial, klare Ja/Nein-Empfehlung zur Zusammenarbeit.")]),
  deliver=["Top-3-Hebel, priorisiert nach Umsatz-Wirkung",
           "Wo Budget verdampft, in Euro pro Monat geschätzt",
           "Ehrliche Ja/Nein-Empfehlung zur Zusammenarbeit"],
  trust=["Kostenlos", "Unverbindlich", "Ein Gründer prüft", "Antwort unter 24 h"],
  h1=["Jeder Euro.", "Zurechenbar."], ital=1,
  tags=["Meta, Google, TikTok", "Lead-Generierung", "Creative-Testing", "Ehrliche Attribution"],
  sub="Kampagnen, die Leads und Verkäufe bringen, nicht Reichweite. Mit Attribution, der Sie trauen können.",
  problem_h=["Das Problem"],
  problem=["Budget läuft, Dashboards leuchten, aber niemand kann sagen, welcher Euro wirklich Umsatz gebracht hat. Doppelt gezählte Conversions feiern Erfolge, die es nie gab.",
           "<b>Ohne saubere Zurechnung fließt Budget monatelang in Kanäle, die nur Klicks liefern.</b> Der CPL steigt, die Pipeline bleibt leer, und am Ende heißt es: Performance funktioniert bei uns nicht."],
  intro="<b>Meta, Google und TikTok</b> mit einer Regel: <b>Das Creative ist der Hebel</b>, nicht das Budget. Systematisch getestet, ehrlich gemessen, <b>wöchentlich</b> umgeschichtet.",
  acc=[("Kampagnen-Setup", "Strukturen, die skalieren können: nach Rolle getrennte Kampagnen, saubere Zielwerte, Budgets dort, wo der ehrliche CPL hinzeigt.",
        ["Meta, Google, TikTok", "Instant Forms & Lead-Strecken", "Kaufnahe Search-Intents", "Budget-Steuerung, wöchentlich"]),
       ("Creative-Testing", "Viele Varianten, klare Sieger: Bei einem Wiener Neubauprojekt trug ein einziges Interior-Motiv 54 Prozent aller Leads.",
        ["Systematische Testing-Loops", "Winner-Selektion nach CPL und CPA", "UGC gegen Studio getestet", "Botschaften je Zielgruppe"]),
       ("Tracking & Attribution", "Server-side Tracking und Blended-Sicht: Jede Conversion wird einmal gezählt, nicht zweimal gefeiert.",
        ["Server-side Tracking", "Blended-Sicht statt Kanal-Ego", "CRM-Anbindung", "Consent-konform"]),
       ("Reporting", "Wöchentlich, transparent, auch unbequem: Ziel-Gaps und gestoppte Tests stehen im Report.",
        ["Wöchentliches Reporting", "Ehrliche Ziel-Gaps", "Klare Handlungsempfehlungen", "Direkter Draht, kein Ticketsystem"])],
  diff=[("Anders als üblich", "Das Creative ist der Hebel", "Nicht das größte Budget gewinnt, sondern das stärkste Motiv. Wir verschieben Budget konsequent auf die Gewinner.", "assets/img/ag_strategy.jpg"),
        ("Anders als üblich", "Ehrlich, auch wenn es wehtut", "Ein Finance-Kunde hatte einen Paid-Kanal schon laufen, als wir kamen. Wir haben ihn messbar gemacht, parallel den zweiten Kanal aufgebaut, und als die Zahlen bestätigten, dass der erste keine zurechenbaren Zeichnungen bringt, haben wir ihn geschlossen.", "assets/img/ag_board1.jpg"),
        ("Anders als üblich", "Ein Kanal sauber statt fünf halb", "Lieber einen Kanal ausreizen und beweisen, als Budget über fünf Kanäle verdampfen lassen.", "assets/img/ag_talk.jpg")],
  zoom=dict(img="assets/img/funkhaus.jpg", side="right", al="Ein Fall",
            ah=["Das Creative", "ist der Hebel."],
            alink=("case-premium-neubau.html", "Den Fall im Detail"), aside="Das stärkste Creative ist der größte Hebel, nicht das größte Budget.",
            zl="Premium-Neubau Wien, Instant Forms", zt="489 Leads zu € 11,77. Ein Motiv trug 54 %."),
  proof_h=["Ein Projekt.", "Vollständig nachgerechnet."],
  proof_lead="Statt Bestwerte aus fünf Mandaten nebeneinanderzustellen, nehmen wir ein Projekt und zeigen jede Stufe: das Budget, die Motive, den Preis pro Anfrage, die Erkenntnis.",
  proof_nums=[],
  proof_quote="Konstanz über Regionen und Projekte zeigt: Das Motiv trägt, nicht der Zufall. Niedrige CPL kommt aus Disziplin, nicht aus Glück.",
  visual=("phones", dict(h=["Creatives,", "die im Feed bestehen."], t="Gebaut für den Daumen: Sujets aus laufenden Kampagnen, getestet gegen echte Benchmarks, nicht gegen Geschmack.",
                          phones=["assets/case/case-premium-neubau/v0.mp4", "assets/case/case-crowdinvesting/v0.mp4", "assets/case/grandgarden/v0.mp4", "assets/case/case-premium-neubau/v1.mp4", "assets/case/herogroup/v0.mp4", "assets/case/case-immobilien-investment/v0.mp4"])),
  crew=dict(label="Wer daran arbeitet",
            h=["Vier Rollen,", "die am Ergebnis hängen."],
            t="Kein Ticketsystem, kein Junior am Konto. Wer Ihre Kampagne baut, sitzt auch im Call, in dem sie erklärt wird.",
            people=[("Steve", "Performance Manager", "Baut die Kontostruktur und schichtet Budget um, sobald ein Motiv kippt.", "assets/img/team/steve.jpg"),
                    ("Constantin", "Design", "Entwirft die Sujets, die gegeneinander antreten, jede Woche neue Varianten.", "assets/img/team/constantin.jpg"),
                    ("Leny", "Film und Foto", "Produziert das Material im Hochformat, gedreht für den Feed statt für den Katalog.", "assets/img/retreat-04.jpg"),
                    ("Daniel", "Founder", "Sitzt im Reporting-Call und verantwortet die Zahl, die dort steht.", "assets/img/team/daniel.jpg")]),
  voice=dict(label="Was Kunden sagen",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Wir schicken kein Dashboard, das niemand liest. Wir gehen einmal im Monat gemeinsam durch die Zahlen und sagen auch, was nicht funktioniert hat."),
  logos=["winegg", "funkhaus", "ifa", "conda", "soravia", "rhomberg", "vonpoll", "seeresidenz"],
  oplist=[("case-premium-neubau.html", "Premium-Neubau, Wien", "489", "Leads, € 11,77 CPL, Wellen unter € 5"),
          ("case-bautraeger-portfolio.html", "Bauträger-Portfolio, Wien", "€ 5,93", "CPL im zweiten Quartal, 546 Anfragen aus zwei Projekten"),
          ("case-wohnbau-floridsdorf.html", "Wohnbau, Floridsdorf", "460", "Leads, € 12,77 CPL, dann Pivot auf Qualität"),
          ("case-crowdinvesting.html", "Crowdinvesting-Plattform", "18,7", "ROAS in der zweiten POC-Phase, vorher 2,14"),
          ("case-health-brand.html", "Dental-/Health-Marke", "1.385", "Verkäufe, Ziel-Gap offen reportet"),
          ("case-nordic-spirit.html", "Nordic Spirit, JTI", "23.579", "Abschlüsse in zwölf Monaten, € 11,70 je Abschluss")],
  faq=[("Unsere Zielgruppe ist zu speziell für Performance.", "Das hören wir oft, auch von Investoren-Funnels und Premium-Neubau. Genau dort entscheidet die Botschaft je Zielgruppe: Bei Anlegern schlug der Service-Angle die Nachhaltigkeits-Story um das 2,3-Fache."),
       ("Woher wissen wir, dass die Zahlen stimmen?", "Server-side Tracking, Blended-Sicht und auf Wunsch der Blick in den Ad-Manager: Wir reporten die Realität, nicht die schönste Zählweise."),
       ("Was passiert, wenn ein Kanal nicht liefert?", "Dann wird er geschlossen, nicht schöngeredet. Bei einem Finance-Kunden lief ein Kanal schon vor uns. Wir haben ihn messbar gemacht, die Hypothese bestätigt, dass er keine zurechenbaren Zeichnungen bringt, und ihn geschlossen, während der zweite Kanal lieferte.")],
  offer_h="Der Einstieg ist ein Account-Audit. Kein Vertrag.",
  offer=["Wir prüfen Kampagnenstruktur, Creatives, Tracking und Zurechnung und zeigen Ihnen in zwei Wochen, wo Budget verdampft und wo der ehrliche CPL liegt. Danach entscheiden Sie.",
         "<b>Risikoumkehr inklusive:</b> Wo sich Umsatz messen lässt, koppeln wir unsere Vergütung daran. Basis-Fixum plus Erfolgsbeteiligung, wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Account-Audit", "Meta-Setup", "Google-Setup", "Lead-Kampagne", "Creative-Testing", "Tracking-Setup", "Zweitmeinung", "Skalierung"]),

 dict(slug="service-content-creation", nav="Content Creation", label="Leistung, Content Creation",
  h1=["Content,", "der verkauft."], ital=1,
  tags=["UGC & Studio", "Foto & Film", "Social-Formate", "Creative-System"],
  sub="Foto, Film und UGC, produziert für Performance: gemessen am CPA, nicht am Applaus.",
  problem_h=["Das Problem"],
  problem=["Feeds voller Hochglanz, aber die CPMs steigen und niemand misst, welches Motiv wirklich trägt. Schöner Content, der nichts verkauft, ist Dekoration.",
           "<b>Die Konsequenz: teure Produktionen ohne Wirkung.</b> Jedes Shooting ohne Testing-Plan produziert Material fürs Archiv, während die Kampagne mit dem falschen Motiv weiterläuft."],
  intro="<b>Content und Performance</b> sitzen bei uns an einem Tisch. Jedes Motiv läuft gegen echte <b>Zahlen</b>, nicht gegen Geschmack. Was trägt, wird skaliert, egal wie <b>schön</b> der Rest war.",
  acc=[("UGC-Produktion", "Echte Menschen, echte Nutzung: In einem Health-Mandat schlug UGC die klassischen Produkt-Videos beim CPA um rund 58 Prozent.",
        ["Creator-Casting & Briefing", "Skripte nach Hook-Logik", "Iterationen nach CPA", "Rechte & Freigaben sauber"]),
       ("Studio & On-Location", "Produktwelten, Interiors, Menschen: produziert mit Blick auf den Feed, nicht auf das Portfolio.",
        ["Foto & Film", "Produkt-Stills & Interiors", "Kampagnen-Sujets", "Cinematography"]),
       ("Social-Formate", "Formate, die die Plattform belohnt: schnell, nativ, mit Hook in den ersten Sekunden.",
        ["Reels & Stories", "Statics & Collagen", "Karussells & Grundriss-Formate", "Saisonale Motive je Phase"]),
       ("Creative-System", "Kein Kampagnenfeuerwerk, sondern ein Loop: produzieren, testen, lernen, nachproduzieren.",
        ["Testing-Loop mit Performance", "Winner-Selektion nach Zahlen", "Motiv-Bibliothek je Marke", "Monatliche Nachproduktion"])],
  diff=[("Anders als üblich", "Gemessen statt gemeint", "Interior-Motive trugen bei einem Neubauprojekt 54 Prozent aller Leads. Solche Antworten liefert Testing, kein Bauchgefühl.", "assets/img/ag_cam2.jpg"),
        ("Anders als üblich", "Content + Performance, ein Team", "Die Produktion kennt die Zahlen von gestern, die Kampagne bekommt Nachschub, bevor das Motiv müde wird.", "assets/img/ag_cam1.jpg"),
        ("Anders als üblich", "UGC ernst genommen", "UGC ist bei uns keine Billig-Alternative, sondern der oft effizienteste Hebel: minus 58 Prozent CPA gegen Studio-Video.", "assets/img/ag_shoot1.jpg")],
  wall=dict(label="Aus laufenden Mandaten",
            h=["Wir produzieren nicht", "für die Mappe."],
            t="Jede Woche entstehen neue Sujets für laufende Kampagnen: Gastro, Event, Immobilie, Produkt. Hochformat, weil dort geschaut wird.",
            link=("work.html", "Alle Cases ansehen")),
  zoom=dict(img="assets/img/c_champ.jpg", side="left", al="Ein Fall",
            ah=["Produziert", "für den Feed."],
            alink=("case-premium-neubau.html", "Den Fall im Detail"), aside="Produziert für den Feed: Content, der gemessen wird, nicht nur gefällt.",
            zl="Content-Produktion, Food", zt="Jedes Motiv tritt gegen Benchmarks an."),
  proof_h=["Wie ein Motiv", "entsteht."],
  proof_lead="Content ist bei uns Handwerk mit Messpunkt: Wir zeigen den Weg von der Idee zum Sujet, das im Feed bestehen muss. Die Zahlen stehen am Ende, nicht am Anfang.",
  proof_nums=[],
  tell=dict(
    h="Ein Motiv, vier Stationen.",
    t="Vom Briefing bis zum Sujet, das gegen echte Benchmarks antritt statt gegen Geschmack.",
    steps=[
      ("1 Tag", "Dreh statt Studio-Woche", "Der Dreh",
       "Wir drehen dort, wo das Produkt lebt: in der Wohnung, im Lokal, auf der Baustelle. Hochformat, Available Light, kein Set-Aufbau über Tage."),
      ("4", "Varianten je Idee", "Der Schnitt",
       "Aus einem Dreh entstehen mehrere Sujets mit unterschiedlichem Einstieg. Getestet wird der Hook, nicht das Motiv als Ganzes."),
      ("−58 %", "CPA durch UGC statt Studio-Video", "Der Test",
       "Bei einer Dental-Marke schlug das UGC-Sujet das Studio-Video deutlich. Nicht weil es schöner war, sondern weil es weniger nach Werbung aussah."),
      ("54 %", "aller Leads aus einem einzigen Motiv", "Die Erkenntnis",
       "Bei einem Wiener Neubauprojekt trug ein Interior-Motiv über die Hälfte aller Anfragen. Deshalb produzieren wir laufend, nicht einmalig."),
    ]),
  proofsplit=dict(label="Was zählt",
                  h=["Nicht schön.", "Wirksam."],
                  t="Ein Sujet muss zwei Prüfungen bestehen: den Daumen in der ersten Sekunde und den Report am Monatsende. Was nur die erste besteht, ist Deko."),
  crew=dict(label="Wer daran arbeitet",
            h=["Vier Rollen,", "die am Motiv arbeiten."],
            t="Kamera, Schnitt und Kampagne sitzen im selben Team. Wer dreht, weiß, wogegen das Sujet antreten muss.",
            people=[("Leny", "Film und Foto", "Dreht im Hochformat, mit dem Licht, das da ist, statt mit dem, das gebaut wird.", "assets/img/retreat-04.jpg"),
                    ("Constantin", "Design", "Setzt Typo und Hook, damit die erste Sekunde die Botschaft trägt.", "assets/img/team/constantin.jpg"),
                    ("Sarah", "Graphic Design", "Baut die Varianten, die gegeneinander antreten, und hält die Marke zusammen.", "assets/img/team/sarah.jpg"),
                    ("Suman", "Social Media", "Bringt die Reaktionen aus dem Feed zurück in die nächste Produktion.", "assets/img/team/suman.jpg")]),
  voice=dict(label="Was Kunden sagen",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Wir liefern keine Mediathek zum Archivieren. Jedes Sujet läuft in einer Kampagne und wird daran gemessen, wie es dort abschneidet."),
  fit=dict(label="Bevor wir starten",
           h=["Der Fit entscheidet.", "Nicht das Briefing."],
           yes_h="Wir passen zusammen, wenn",
           no_h="Wir sind die Falschen, wenn",
           intro="Wir arbeiten als verlängerte Marketingabteilung, nicht als Produktionsdienstleister. Wir müssen Ihre Marke verstehen, bevor wir die Kamera aufstellen, und Sie müssen uns zutrauen, dass wir Motive verwerfen. Deshalb prüfen wir den Fit vorher, in beide Richtungen.",
           yes=["Es gibt Kampagnen, in denen das Material laufen soll",
                "Hochformat ist erlaubt, auch wenn es weniger nach Katalog aussieht",
                "Laufende Produktion statt einmaliges Shooting",
                "Freigaben in Tagen, nicht in Wochen"],
           no=["Das Material soll nur in die Mediathek",
               "Jedes Motiv braucht eine Freigaberunde über mehrere Instanzen",
               "Nur Studio-Look, kein Available Light",
               "Ein Shooting soll ein Jahr tragen"]),
  steps_next=dict(
    h="Von der Anfrage zum ersten Sujet.",
    rows=[("Heute", "Anfrage in zwei Minuten", "Was beworben wird und wo das Material laufen soll."),
          ("Unter 24 h", "Ehrliche Ersteinschätzung", "Wir sagen, ob wir passen, und was für den Dreh nötig ist."),
          ("Tag 3 bis 10", "Dreh vor Ort", "Ein Tag, mehrere Sujets, Hochformat. Kein Set-Aufbau über eine Woche."),
          ("Danach", "Erste Testrunde", "Die Varianten laufen gegeneinander, der Sieger bekommt Budget.")]),
  deliver=["Ein Drehtag vor Ort, Hochformat, mit dem Licht, das da ist",
           "Mehrere Sujets je Idee, für den Test gegeneinander gebaut",
           "Hook-Varianten statt einer finalen Fassung",
           "Auswertung, welches Sujet im Feed bestanden hat"],
  trust=["Kein Vertrag für den Erstdreh", "Material bleibt bei Ihnen", "Nutzungsrechte unbefristet"],
  proof_quote="Der größte Hebel war das Creative, nicht das Budget. Das gilt in Commerce, Real Estate und Health gleichermaßen.",
  visual=("phones", dict(h=["Gebaut", "für den Daumen."], t="Sujets aus laufenden Mandaten: Gastro, Event, Immobilie, Produkt. Immer mit Hook, immer messbar.",
                          phones=["assets/case/kommunalkredit/v0.mp4", "assets/case/juwel/v0.mp4", "assets/case/case-health-brand/v1.mp4", "assets/case/kommunalkredit/v1.mp4", "assets/case/juwel/v1.mp4", "assets/case/case-health-brand/v2.mp4"])),
  logos=["isi", "looops", "juwel", "nordicspirit", "jti", "ilbosso", "kaisers", "funkhaus"],
  oplist=[("case-health-brand.html", "Dental-/Health-Marke", "−58 %", "CPA durch Creator statt Produktvideo"),
          ("case-premium-neubau.html", "Premium-Neubau, Wien", "54 %", "aller Leads aus einem Motiv"),
          ("case-kommunalkredit.html", "Kommunalkredit, Sommergespräche", "19", "Social Clips, Recap und Doku aus drei Drehtagen"),
          ("case-d2c-lifestyle.html", "D2C-Lifestyle-Marke", "+57 %", "Jahresumsatz, UGC schlug Studio")],
  faq=[("Wir haben schon einen Fotografen.", "Gut so, den ersetzen wir nicht zwingend. Wir ergänzen das System dahinter: Hooks, Testing, Winner-Selektion. Content ohne Messung bleibt Dekoration."),
       ("Ist UGC nicht billig fürs Markenbild?", "Falsch produziert: ja. Richtig produziert wirkt UGC glaubwürdiger als Hochglanz und senkte den CPA in unserem Health-Mandat um rund 58 Prozent."),
       ("Wie viel Content brauchen wir wirklich?", "Weniger, als Sie denken, aber öfter: Ein monatlicher Nachproduktions-Loop schlägt das eine große Shooting pro Jahr.")],
  offer_h="Der Einstieg ist ein Creative-Audit. Kein Vertrag.",
  offer=["Wir analysieren Ihre laufenden Motive gegen Benchmarks und zeigen Ihnen, welche Creatives Geld verdienen, welche Geld verbrennen und was als Nächstes produziert gehört.",
         "<b>Risikoumkehr:</b> Läuft die Produktion mit Performance-Mandat, koppeln wir die Vergütung an messbare Ergebnisse. Wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Creative-Audit", "UGC-Produktion", "Studio-Shooting", "Reels & Social", "Kampagnen-Sujets", "Testing-Loop", "Zweitmeinung", "Content-Partnerschaft"]),

 dict(slug="service-websites", nav="Websites & Landingpages", label="Leistung, Websites & Landingpages",
  h1=["Seiten, die", "abschließen."], ital=1,
  tags=["Landingpages", "Shops & Websites", "Konfiguratoren", "CRO & A/B-Tests"],
  sub="Landingpages, Shops und interaktive Lead-Magnete: gebaut auf Conversion, gemessen am Abschluss.",
  problem_h=["Das Problem"],
  problem=["Teure Klicks landen auf Seiten, die nicht konvertieren: langsam, überladen, ohne klares Nutzenversprechen über dem Falz und ohne Message-Match zur Anzeige.",
           "<b>Jeder Euro Mediabudget wird dadurch entwertet.</b> Wer € 3 pro Klick zahlt und 1 Prozent konvertiert, zahlt € 300 pro Lead, und wundert sich über den Markt."],
  intro="Wir bauen Seiten vom <b>Abschluss</b> her: eine Botschaft, ein Ziel, <b>Message-Match</b> zur Kampagne. Und wir sagen Ihnen, wann ein <b>Instant Form</b> die bessere Wahl ist.",
  acc=[("Landingpages je Kampagne", "Eine Seite pro Botschaft: Headline, Beweis und CTA passen zur Anzeige, nicht zur Sitemap.",
        ["Message-Match zur Kampagne", "Ein Ziel pro Seite", "Proof an den Entscheidungspunkten", "Noindex, schnell, mobil zuerst"]),
       ("Shops & Websites", "Vom Produkt bis zum Checkout: Auftritte, die Markenwelt und Abschluss verbinden.",
        ["Shop-Systeme & Checkout", "Markenwelten & Kataloge", "Performance & Core Web Vitals", "Content-Pflege ohne Agentur-Zwang"]),
       ("Interaktive Lead-Magnete", "Der Konfigurator ist das beste Creative: Ein PV-Anbieter bekam darüber 406 Leads und 487 Prozent mehr Besucher.",
        ["Konfiguratoren & Rechner", "Mehrstufige Lead-Strecken", "Qualifizierung im Formular", "Übergabe ans CRM"]),
       ("CRO & Testing", "Hypothese, Test, Entscheidung: Conversion-Optimierung als Routine, nicht als Projekt.",
        ["A/B-Tests mit klaren Hypothesen", "Heatmaps & Session-Analysen", "Checkout-Optimierung", "Wöchentliche Iteration"])],
  diff=[("Anders als üblich", "Message-Match statt Sitemap", "Die Landingpage gehört zur Kampagne, nicht zur IT: Headline und Beweis wechseln mit der Anzeigengruppe.", "assets/img/ag_vision2.jpg"),
        ("Anders als üblich", "Der Lead-Magnet als Creative", "Ein Konfigurator, der den Bedarf rechnet, schlägt jedes Standard-Formular: 406 Leads für einen PV-Anbieter.", "assets/img/ag_vision1.jpg"),
        ("Anders als üblich", "Ehrlicher Kanalvergleich", "Bei einem Neubauprojekt lieferten Instant Forms Leads zu € 6,97, die Website zu € 15,66. Wir sagen auch, wenn die Landingpage nicht der beste Ort ist.", "assets/img/ag_review.jpg")],
  zoom=dict(img="assets/case/case-web-noma/d0.jpg", side="right", al="Ein Fall",
            ah=["Tiefe statt", "Teaser."],
            alink=("case-web-noma.html", "Den Fall im Detail"), aside="Die Landingpage als Ort für Tiefe: Grundrisse, Vertrauen, Abschluss.",
            zl="Projekt-Landingpage, Premium-Neubau", zt="Landingpage und Instant Forms im Verbund."),
  proof_h=["Wie eine Seite", "entsteht."],
  proof_lead="Eine Seite ist kein Bildband und kein Formular. Wir zeigen den Weg von der Struktur zum Auftritt, der Mediabudget tragen kann.",
  proof_nums=[],
  tell=dict(
    h="Eine Seite, vier Stationen.",
    t="Von der Reihenfolge über die Bildsprache bis zur Strecke, die aus dem Besuch eine Anfrage macht.",
    steps=[
      ("1", "Frage je Bildschirm", "Die Struktur",
       "Jeder Abschnitt beantwortet genau eine Frage. Was keine Frage beantwortet, fliegt raus, auch wenn es gut aussieht."),
      ("9:16", "Format, in dem gebaut wird", "Die Bildsprache",
       "Wir entwerfen mobil zuerst, weil dort besucht wird. Das Desktop-Layout entsteht danach, nicht umgekehrt."),
      ("€ 6,97", "CPL über die Instant-Form-Strecke", "Die Strecke",
       "Bei einem Wiener Neubauprojekt lag die Anfrage über die Instant Form bei € 6,97, über das Website-Formular bei € 15,66. Beides steht im Report."),
      ("+487 %", "Website-Besucher", "Der Auftritt",
       "Bei einem Photovoltaik-Anbieter kamen Sichtbarkeit und Konfigurator zusammen: fast das Sechsfache an Besuchern, 406 Anfragen."),
    ]),
  proofsplit=dict(label="Zwei Prüffragen",
                  h=["Schön genug.", "Klar genug."],
                  t="Eine Seite muss zwei Prüfungen bestehen: Sie muss die Marke tragen und sie muss führen. Fällt eine davon durch, ist die andere umsonst."),
  wall=dict(label="Gebaute Auftritte",
            h=["Gebaut für den Ort,", "an dem besucht wird."],
            t="Die Auftritte aus laufenden Mandaten, so wie die meisten Besucher sie sehen: am Telefon, Seite für Seite.",
            link=("work.html", "Alle Auftritte ansehen")),
  crew=dict(label="Wer daran arbeitet",
            h=["Vier Rollen,", "die die Seite bauen."],
            t="Struktur, Gestaltung und Kampagne entstehen im selben Zug. Wer die Seite baut, weiß, welche Anzeige darauf führt.",
            people=[("Constantin", "Design", "Entwirft mobil zuerst und hält jede Sektion auf eine Frage.", "assets/img/team/constantin.jpg"),
                    ("Valentina", "Graphic Design", "Bringt Bildsprache und Typo in eine Form, die die Marke trägt.", "assets/img/team/valentina.jpg"),
                    ("Philipp", "Sales", "Prüft jede Strecke aus Sicht der Anfrage: Was fehlt bis zum Termin.", "assets/img/ag_talk.jpg"),
                    ("Florian", "Founder", "Verantwortet, dass die Seite das Mediabudget trägt, das darauf führt.", "assets/img/team/florian.jpg")]),
  voice=dict(label="Was Kunden sagen",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Wir bauen keine Seite, die danach niemand anfassen darf. Änderungen an Struktur und Strecken gehören zum laufenden Betrieb."),
  fit=dict(label="Bevor wir starten",
           h=["Der Fit entscheidet.", "Nicht der Umfang."],
           yes_h="Wir passen zusammen, wenn",
           no_h="Wir sind die Falschen, wenn",
           intro="Wir bauen keine Seite und verschwinden. Wir arbeiten als verlängerte Marketingabteilung weiter daran, wenn die Zahlen etwas anderes sagen als der Entwurf. Das setzt Vertrauen in beide Richtungen voraus, deshalb prüfen wir den Fit vorher.",
           yes=["Die Seite soll Anfragen bringen, nicht nur repräsentieren",
                "Mobil zuerst ist in Ordnung, auch wenn Desktop später kommt",
                "Struktur darf sich ändern, wenn die Zahlen es sagen",
                "Es gibt Kampagnen, die auf die Seite führen"],
           no=["Die Seite ist ein Selbstzweck ohne Ziel",
               "Jede Änderung braucht eine Gremiumsrunde",
               "Der Inhalt kommt erst nach dem Livegang",
               "Es darf nichts gemessen werden"]),
  steps_next=dict(
    h="Von der Anfrage zum Auftritt.",
    rows=[("Heute", "Anfrage in zwei Minuten", "Was verkauft werden soll und für wen die Seite arbeitet."),
          ("Unter 24 h", "Ehrliche Ersteinschätzung", "Wir sagen, ob wir passen, und was an Inhalt schon da ist."),
          ("Tag 2 bis 7", "Seiten-Audit oder Struktur-Entwurf", "Bestehende Seite im Test, oder die Reihenfolge für die neue auf einer Seite."),
          ("Danach", "Klare Empfehlung", "Was zuerst gebaut wird, was das kostet, was es bringen soll.")]),
  deliver=["Struktur auf einer Seite: welche Frage in welcher Reihenfolge",
           "Entwurf mobil zuerst, Desktop danach",
           "Strecken bis zur Anfrage, inklusive Messpunkte",
           "Übergabe, mit der Ihr Team weiterarbeiten kann"],
  trust=["Kein Vertrag für das Audit", "Code und Inhalte bleiben bei Ihnen", "Keine Lizenzbindung"],
  proof_quote="Sichtbarkeit und Conversion-Mechanik gehören zusammen: Search erntet Nachfrage, die schon da ist, die Seite macht sie zur Anfrage.",
  visual=("phones", dict(h=["Mobil zuerst", "gebaut."], t="Die Auftritte aus laufenden Mandaten, dort wo sie besucht werden: am Telefon.",
                          phones=["assets/img/web_noma_m.jpg", "assets/img/web_funkhausliving_m.jpg", "assets/img/web_trattner_m.jpg", "assets/img/web_unio_m.jpg", "assets/case/case-web-ib7/m0.jpg", "assets/img/web_pharmacom_m.jpg"])),
  logos=["funkhaus", "winegg", "seeresidenz", "vonpoll", "rhomberg", "soravia", "isi", "hagent"],
  oplist=[("case-premium-neubau.html", "Premium-Neubau, Wien", "€ 6,97", "CPL Instant Form vs. € 15,66 Website, dazu die Projekt-Website"),
          ("case-web-noma.html", "Noma Wien", "13 von 26", "Wohnungen verkauft, wenige Monate nach Go-live"),
          ("case-web-twistnsparkle.html", "Twist'n Sparkle, isi", "3", "Sprachen, vier Launch-Termine"),
          ("case-immobilien-investment.html", "Immobilien-Investment", "129×", "Funnel bis zur Zeichnung"),
          ("case-photovoltaik.html", "Photovoltaik-Anbieter", "+487 %", "Besucher, 406 Leads")],
  faq=[("Wir haben schon eine Website.", "Und sie hat einen Job: abschließen. Wenn sie das nicht tut, braucht es selten einen Relaunch, sondern eine Landingpage pro Kampagne und einen sauberen Test-Plan."),
       ("Warum nicht einfach ein Baukasten?", "Für den Start völlig okay. Sobald Mediabudget auf die Seite trifft, entscheiden Ladezeit, Message-Match und Testing, und da rechnet sich Handarbeit schnell."),
       ("Landingpage oder Instant Form?", "Das entscheiden die Zahlen, nicht die Vorliebe: Wir testen beides und schichten dorthin um, wo der ehrliche CPL liegt.")],
  offer_h="Der Einstieg ist ein Seiten-Audit. Kein Vertrag.",
  offer=["Wir prüfen Ladezeit, Message-Match, Formulare und Checkout und zeigen Ihnen in zwei Wochen, wo Ihre Seite Anfragen verliert. Danach entscheiden Sie.",
         "<b>Risikoumkehr:</b> Läuft die Seite im Performance-Mandat, hängt unsere Vergütung an messbaren Ergebnissen. Wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Seiten-Audit", "Landingpage", "Shop-Projekt", "Konfigurator", "CRO & Testing", "Relaunch-Begleitung", "Zweitmeinung", "Betreuung im Mandat"]),

 dict(slug="service-strategie", nav="Strategie & Funnel", label="Leistung, Strategie & Funnel",
  h1=["Struktur schlägt", "Bauchgefühl."], ital=1,
  tags=["Funnel-Architektur", "KPI-Logik", "Attribution", "Positionierung"],
  sub="Vom Einzelprojekt zur Plattform: Funnel, KPI-Logik und Attribution, die Entscheidungen tragen.",
  problem_h=["Das Problem"],
  problem=["Jede Kampagne beginnt bei null: eigene Zielgruppen, eigene Zahlen, keine gemeinsame Datenbasis. Was funktioniert hat, weiß hinterher niemand genau.",
           "<b>Teuer erkaufte Learnings verpuffen.</b> Eine Plattform, die mit ROAS 2,14 lief, blieb genau so lange ineffizient, bis Struktur, KPI-Logik und projektübergreifendes Lernen kamen: Danach stand sie bei 8,75."],
  intro="Erst die <b>Struktur</b>, dann das Budget: <b>Funnel</b>, KPI-Definitionen, die vorab feststehen, und eine <b>Attribution</b>, die jeden Euro zurechenbar macht.",
  acc=[("Funnel-Architektur", "Vom ersten Kontakt bis zur Zeichnung: Ein Investoren-Funnel übersetzte € 36k Google-Budget in € 4,65 Mio. zurechenbares Kapital.",
        ["Journey vom Lead bis zum Abschluss", "Vertrauensaufbau Schritt für Schritt", "CRM-Nurture für lange Wege", "Klare Übergaben an Vertrieb"]),
       ("KPI-Logik & Attribution", "Die KPI-Definition vorab ist die halbe Miete: Kosten je Investor, Ø Investment, Volumen, ROAS, sauber zugerechnet.",
        ["KPI-Set je Geschäftsmodell", "Server-side Tracking", "Zurechenbarkeit statt Zählweisen", "Dashboards, die Entscheidungen tragen"]),
       ("Zielgruppen & Positionierung", "Eigennutzer und Anleger sind zwei Märkte: Wer beide gleich anspricht, verliert bei beiden.",
        ["Segment-Logik & Botschaften", "Message-Testing je Zielgruppe", "Preis- und Angebotslogik", "Positionierung gegen den Markt"]),
       ("Plattform statt Projekt-Silo", "Projektübergreifendes Lernen macht jedes weitere Projekt günstiger: gleiches Budget, viermal mehr Kapital.",
        ["Gemeinsame Datenbasis", "Wiederholbare Test-Mechanik", "Portfolio-Sicht auf CPL und ROAS", "Skalierung mit System"])],
  diff=[("Anders als üblich", "KPI-Definition vorab", "Bevor der erste Euro läuft, steht fest, woran der Erfolg gemessen wird. Das verhindert schöngerechnete Kampagnen.", "assets/img/ag_strategy.jpg"),
        ("Anders als üblich", "Vertrauen als Funnel-Stufe", "Im Finance zählt der Cost per zugerechnetem Kapital, nicht der CPL: Aufklärung, Vertrauen, Handlung.", "assets/img/retreat-06.jpg"),
        ("Anders als üblich", "Ehrliches Schließen", "Ein bestehender Paid-Kanal wurde erst messbar gemacht, dann an der Hypothese geprüft, dann geschlossen, während der zurechenbare Kanal parallel wuchs. Genau dafür ist Struktur da.", "assets/img/ag_board1.jpg")],
  zoom=dict(img="assets/img/ag_meeting.jpg", side="left", al="Ein Fall",
            ah=["Erst die Struktur.", "Dann das Budget."],
            alink=("case-crowdinvesting.html", "Den Fall im Detail"), aside="Erst die Struktur, dann das Budget: Strategie-Session in Wien.",
            zl="Strategie & Funnel", zt="€ 36k Budget wurden € 4,65 Mio. Kapital."),
  proof_h=["Ein Mandat.", "Von der Struktur zur Zahl."],
  proof_lead="Ein Immobilien-Investment-Mandat, Stufe für Stufe: das eingesetzte Budget, die Struktur, die Zurechnung, das eingesammelte Kapital.",
  proof_nums=[],
  tell=dict(
    h="Ein Mandat, vier Zahlen.",
    t="Wie aus € 36k Mediabudget € 4,65 Mio. Kapital wurden, Stufe für Stufe nachgerechnet.",
    steps=[
      ("€ 36k", "Mediabudget über die Laufzeit", "Das Budget",
       "Für ein Investment-Mandat ist das kein großer Hebel, sondern ein kleiner. Genau deshalb musste die Reihenfolge stimmen."),
      ("3", "Stufen statt Einzelkampagnen", "Die Struktur",
       "Nicht mehr Kampagnen, sondern eine Reihenfolge: Aufmerksamkeit, Vertrauen, Termin. Jede Stufe mit eigener Botschaft je Zielgruppe."),
      ("2,3×", "Vorsprung des stärkeren Angles", "Die Zurechnung",
       "Bei Anlegern schlug der Service-Angle die Nachhaltigkeits-Story um das 2,3-Fache. Gemessen, nicht vermutet."),
      ("129×", "Return, sauber zugerechnet", "Das Kapital",
       "€ 4,65 Mio. eingesammeltes Kapital, auf die Kampagne zugerechnet. Das ist ein Return von 129 zu 1."),
    ]),
  channels=dict(
    label="Investments je Laufzeit, Crowdinvesting-Plattform",
    rows=[("Vorher", 32, "16"), ("Mit uns", 100, "50")],
    note="Nahezu gleiches Budget, andere Struktur: Aus 16 Investments wurden 50, die Kosten je Investor fielen um 69 Prozent.",
    link=("case-crowdinvesting.html", "Crowdinvesting-Plattform im Detail")),
  bars=dict(
    label="Return on Ad Spend, Crowdinvesting-Plattform",
    link=("case-crowdinvesting.html", "Dieselbe Plattform, andere Zahl"),
    rows=[("Vorher", 24, "2,14"), ("Mit uns", 100, "8,75")],
    note="Der Sprung kam nicht aus mehr Spend, sondern aus der Reihenfolge: erst die Struktur, dann das Budget."),
  proofsplit=dict(label="Zwei Rechnungen",
                  h=["Was Struktur", "wirklich bewegt."],
                  t="Beide Zahlen kommen aus demselben Mandat, links die Kosten je Investor, rechts der Return on Ad Spend. Das Budget blieb nahezu gleich, geändert hat sich die Reihenfolge."),
  crew=dict(label="Wer daran arbeitet",
            h=["Vier Rollen,", "die an der Struktur bauen."],
            t="Strategie ohne Umsetzung ist eine Folie. Wer die Reihenfolge festlegt, verantwortet auch die Zahl am Ende.",
            people=[("Daniel", "Founder", "Legt die Reihenfolge fest und verantwortet die Zahl, die am Ende im Report steht.", "assets/img/team/daniel.jpg"),
                    ("Florian", "Founder", "Führt die Strategie-Session und übersetzt Geschäftsziele in messbare Stufen.", "assets/img/team/florian.jpg"),
                    ("Steve", "Performance Manager", "Baut die Struktur in die Konten und misst, ob die Reihenfolge trägt.", "assets/img/team/steve.jpg"),
                    ("Alexis", "Sales", "Bringt die Sicht des Vertriebs ein: Welche Anfrage ist wirklich eine Anfrage.", "assets/img/team/alexis.jpg")]),
  voice=dict(label="Was Kunden sagen",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Wir liefern keine Strategie-Folien zum Abheften. Wir legen die Reihenfolge fest, setzen sie um und rechnen sie nach."),
  fit=dict(label="Bevor wir starten",
           h=["Der Fit entscheidet.", "Nicht die Vorlage."],
           yes_h="Wir passen zusammen, wenn",
           no_h="Wir sind die Falschen, wenn",
           intro="Wir liefern keine Strategie zum Abheften. Wir setzen sie um und verantworten die Zahl am Ende, als verlängerte Marketingabteilung. Das geht nur mit Mandaten, bei denen die Zusammenarbeit trägt, deshalb prüfen wir den Fit vorher, in beide Richtungen.",
           yes=["Es gibt ein Ziel in Zahlen: Kapital, Einheiten, Anfragen",
                "Sie wollen die Umsetzung mit derselben Hand, nicht nur das Konzept",
                "Mehrere Zielgruppen mit unterschiedlichen Botschaften",
                "Der Vertrieb ist bereit, Anfragen zeitnah zu bearbeiten"],
           no=["Es soll eine Präsentation für ein Gremium werden",
               "Die Umsetzung übernimmt später jemand anderes",
               "Das Ziel ist Bekanntheit ohne messbare Handlung",
               "Entscheidungen brauchen mehrere Monate Vorlauf"]),
  steps_next=dict(
    h="Von der Anfrage zum Fahrplan.",
    rows=[("Heute", "Anfrage in zwei Minuten", "Was verkauft werden soll und in welchem Zeitraum."),
          ("Unter 24 h", "Ehrliche Ersteinschätzung", "Wir sagen, ob wir passen, und was wir für die Session brauchen."),
          ("Tag 2 bis 14", "Strategie-Session", "Ein halber Tag in Wien oder digital: Zielgruppen, Reihenfolge, Botschaften, Messpunkte."),
          ("Danach", "Fahrplan auf einer Seite", "Die Reihenfolge, die Zahlen, die wir erwarten, und der erste Schritt.")]),
  deliver=["Strategie-Session mit Zielgruppen, Reihenfolge und Botschaften",
           "Funnel-Architektur je Zielgruppe, inklusive Messpunkte",
           "Fahrplan auf einer Seite: Reihenfolge, Erwartung, erster Schritt",
           "Auf Wunsch die Umsetzung mit derselben Hand"],
  trust=["Kein Vertrag für die Session", "Ergebnis bleibt bei Ihnen", "Umsetzung optional"],
  proof_quote="Gleicher Spend, anderes Ergebnis: Der Beweis liegt im Vorher-Nachher. Struktur schlägt Einzelkampagne.",
  visual=("stage", dict(img="assets/case/case-web-northpoint/d0.jpg", cap="Aus dem Mandat, Auftritt mit Funnel-Logik")),
  logos=["ifa", "conda", "raiffeisen", "soravia", "fabrik1230", "hagent", "winegg", "buxbaum"],
  oplist=[("case-immobilien-investment.html", "Immobilien-Investment", "129×", "€ 36k → € 4,65 Mio. Kapital"),
          ("case-crowdinvesting.html", "Crowdinvesting-Plattform", "18,7", "ROAS nach Umbau auf Plattform-Logik, vorher 2,14"),
          ("case-consumer-brand.html", "Premium-Consumer-Brand", "4,02", "Saison als Architektur"),
          ("case-health-brand.html", "Dental-/Health-Marke", "3", "Zielstufen aus einem Workshop: 1,4, 1,6, 1,8")],
  faq=[("Brauchen wir wirklich Strategie, oder einfach bessere Ads?", "Wenn die Struktur steht, reichen oft bessere Ads. Wenn nicht, verbrennt auch das beste Creative Budget: ROAS 2,14 wurde erst durch Struktur zu 8,75."),
       ("Wie lange dauert so etwas?", "Die Strategie-Phase ist in zwei bis vier Wochen durch, danach wird umgesetzt. Strategie ohne Umsetzung verkaufen wir nicht."),
       ("Was, wenn die Analyse zeigt, dass wenig zu holen ist?", "Dann sagen wir das. Eine ehrliche Absage ist billiger als zwölf Monate Mandat ohne Hebel.")],
  offer_h="Der Einstieg ist eine Strategie-Session. Kein Vertrag.",
  offer=["Status quo, Zielbild, KPI-Logik: In einer strukturierten Session zeigen wir, wo Ihr Funnel Kapital liegen lässt und was zuerst gebaut gehört. Danach entscheiden Sie.",
         "<b>Risikoumkehr:</b> Geht die Strategie in ein Umsetzungs-Mandat über, koppeln wir die Vergütung an messbare Ergebnisse. Wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Strategie-Session", "Funnel-Architektur", "KPI-Logik", "Attribution-Setup", "Positionierung", "Portfolio-Struktur", "Zweitmeinung", "Umsetzungs-Mandat"]),
 dict(slug="service-chatgpt-ads", nav="ChatGPT Ads", label="Leistung, ChatGPT Ads, Frühzugang vor der Öffnung für Europa",
  h1=["Werben, wo andere", "nicht werben."], ital=1,
  tags=["Neu in Österreich seit 24. August", "Im Moment der Entscheidung", "Fühlt sich nicht wie Werbung an", "Frühzugang vor dem Self-Service"],
  sub="Ihre Kunden fragen ChatGPT, bevor sie entscheiden. Wir haben Kampagnen aufgesetzt, bevor der Self-Service für Europa geöffnet wurde, und übernehmen für Sie Prüfung, Aufbau, Text und Messung. Der Kanal ist noch leer. Das ist Ihr Vorteil, wenn Sie jetzt starten.",
  content_label="Aus dem Studio",
  sol_label="Die Ausgangslage",
  problem_h=["Das Problem"],
  problem=["", ""],
  intro="Wer ChatGPT fragt, will entscheiden. Die Aufmerksamkeit ist hoch, und bis vor wenigen Wochen konnte dort <b>niemand werben</b>. Jetzt steht Ihr Angebot unter der Antwort, <b>als Empfehlung</b>, nicht als Banner.",
  acc=[("Wo der Fokus heute liegt", "Die Frage nach dem richtigen Produkt, dem richtigen Anbieter, dem richtigen nächsten Schritt wird immer öfter ChatGPT gestellt. Wer dort antwortet, erreicht Menschen in dem Moment, in dem sie wirklich zuhören.",
        ["Entscheidungen werden im Gespräch vorbereitet", "Volle Aufmerksamkeit, kein Scrollen, kein Lärm", "Eine Antwort statt einer Trefferliste", "Ihr Angebot als Teil dieser Antwort"]),
       ("Warum es sich nicht wie Werbung anfühlt", "Die Karte erscheint nur, wenn das Gespräch zu Ihrem Angebot passt. Keine Unterbrechung, kein Störgefühl: Der Mensch bekommt genau das, wonach er gerade gefragt hat, und Ihre Marke steht als Empfehlung daneben.",
        ["Ausspielung passend zum Gespräch", "Gekennzeichnet, aber ohne Werbedruck", "Kein Retargeting, kein Verfolgen", "Die Marke bleibt mit der Antwort im Kopf"]),
       ("Warum jetzt", "Jeder neue Kanal hat eine kurze Phase, in der wenige um viel Aufmerksamkeit konkurrieren. Wer sie nutzt, sammelt Erfahrung, die später niemand mehr nachkaufen kann, und ist präsent, bevor es voll wird.",
        ["Der Kanal ist in Österreich noch fast leer", "Erfahrung entsteht nur durch Schalten", "Freigaben brauchen Vorlauf", "Wer wartet, konkurriert später, statt jetzt zu lernen"])],
  diff=[("Was wir beitragen", "Erfahrung aus dem Frühzugang", "Wir haben Kampagnen aufgesetzt, bevor der Ads Manager in Europa geöffnet wurde. Sie starten mit dem, was wir dort gelernt haben, nicht mit Vermutungen.", "assets/img/ag_strategy.jpg"),
        ("Was wir beitragen", "Wir prüfen zuerst, ob Sie überhaupt dürfen", "Nicht jede Branche ist freigegeben, manche brauchen eine Zustimmung von OpenAI. Wir klären das, bevor ein Euro läuft. Kommt keine Freigabe, gibt es keine Kampagne und keine Rechnung.", "assets/img/ag_board1.jpg"),
        ("Was wir beitragen", "Wir schreiben Antworten, keine Anzeigen", "Die Karte wirkt, wenn sie sich wie der natürliche nächste Schritt anfühlt. Wir schreiben sie aus der Frage heraus, die gerade gestellt wird, und bauen die Seite dahinter so, dass sie das Versprechen einlöst.", "assets/img/ag_talk.jpg")],
  zoom=dict(img="assets/img/gpt/card-hero.jpg", side="right", al="So sieht es aus",
            ah=["Ihr Angebot,", "Teil der Antwort."],
            alink=("kontakt.html?w=Eignungs-Check&from=service-chatgpt-ads", "Eignung prüfen lassen"),
            aside="Gekennzeichnet, aber ohne Werbedruck: Ihr Bild, Ihr Satz, Ihr Link, direkt unter dem, was der Mensch gerade wissen wollte. Das Beispiel zeigt eine Projektplattform.",
            zl="Beispielkarte", zt="Sie stört nicht. Sie antwortet."),
  proof_label="Woher wir das wissen",
  proof_h=["Der Ort ist neu.", "Das Handwerk nicht."],
  proof_lead="In ChatGPT werben kann seit wenigen Wochen jeder mit Zugang. Was zählt, ist, ob man es kann: die richtige Botschaft im richtigen Moment, eine Strecke, die hält, und Zahlen, die stimmen. Vier Ergebnisse aus vier Branchen, so wie sie im Reporting stehen.",
  proof_nums=[],
  proof_quote="",
  tell=dict(
    label="Vier Branchen, vier Zahlen",
    steps=[
      ("+57 %", "Jahresumsatz, D2C-Lifestyle-Marke", "Wachstum aus der Botschaft",
       "Von € 520k auf € 817k im besten Jahr der Firma, Blended ROAS 5,57. Nicht mehr Budget hat das gebracht, sondern die richtige Ansprache am richtigen Punkt der Entscheidung. Genau dort setzt die Karte an."),
      ("4,02", "Return on Ad Spend am Black Friday, Consumer-Brand", "Gewinnen, wenn alle schreien",
       "75 Prozent über der Benchmark, in der lautesten Woche des Jahres. Wer sich dort durchsetzt, tut es mit Relevanz. In der Antwort von ChatGPT ist Relevanz die einzige Währung."),
      ("489", "Anfragen für ein Neubauprojekt in Wien", "Der Satz entscheidet",
       "Vier Botschaften im Test, eine trug mehr als die Hälfte aller Anfragen. Welche Formulierung Menschen zum Handeln bringt, wissen wir nach dem Test, nicht davor. Deshalb testen wir auch die Karte, statt sie zu raten."),
      ("8,75", "Return on Ad Spend, Crowdinvesting, vorher 2,14", "Struktur statt mehr Geld",
       "Nahezu gleiches Budget, aus 16 Investments wurden 50. Wer den Aufbau versteht, holt aus demselben Geld das Vierfache. Das gilt für jeden Kanal, auch für einen neuen."),
    ]),
  channels=dict(
    label="Jahresumsatz, D2C-Lifestyle-Marke",
    rows=[("Vorher", 64, "€ 520k"), ("Mit uns", 100, "€ 817k")],
    note="Plus 57 Prozent im besten Jahr der Firma, Blended ROAS 5,57. Das Wachstum kam aus Botschaft, Strecke und Struktur, nicht aus mehr Budget.",
    link=("case-d2c-lifestyle.html", "D2C-Marke im Detail")),
  bars=dict(
    label="Return on Ad Spend am Black Friday, Premium-Consumer-Brand",
    link=("case-consumer-brand.html", "Consumer-Brand im Detail"),
    rows=[("Branchen-Benchmark", 57, "2,3"), ("Mit uns", 100, "4,02")],
    note="75 Prozent über der Benchmark in der lautesten Woche des Jahres. Wer dort gewinnt, gewinnt über Relevanz. In der Antwort zählt nichts anderes."),
  proofsplit=dict(label="Zwei davon als Grafik",
                  h=["Zwei Marken,", "ein Muster."],
                  t="Links eine D2C-Marke, die im besten Jahr der Firma um 57 Prozent wuchs. Rechts eine Consumer-Brand, die am Black Friday 75 Prozent über der Benchmark lag. Beides kam aus Relevanz im Moment der Entscheidung, und genau dafür ist die Karte in ChatGPT gebaut."),
  visual=("panels", dict(label="Drei Situationen, drei Karten",
                          h="Ein Shop, ein Finanzteam, eine Eventlocation. Jede Karte fühlt sich an wie der nächste logische Schritt.",
                          t="Die Beispiele sind gebaut, nicht geschaltet. Sie zeigen, worum es geht: nicht laut sein, sondern passend. Wer gerade nach einem Geschenk, einer Software oder einem Ort für die Feier fragt, bekommt eine Antwort, und Ihr Angebot steht darin.",
                          d1=("Was wir schreiben", "Antworten auf die Frage, die gerade gestellt wird, im Ton des Gesprächs"),
                          d2=("Was wir bauen", "Konto, Karten, die Seite dahinter und die Messung, alles aus einer Hand"),
                          imgs=["assets/img/gpt/card-shop.jpg", "assets/img/gpt/card-b2b.jpg", "assets/img/gpt/card-event.jpg", "assets/img/gpt/card-hero.jpg"])),
  voice=dict(label="Was Kunden sagen",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Wir liefern kein Dashboard, das niemand liest. Einmal in der Woche gehen wir die Zahlen gemeinsam durch, auch die, die nicht funktioniert haben."),
  crew=dict(label="Wer daran arbeitet",
            h=["Vier Rollen,", "ein Team für Ihr Konto."],
            t="Wer die Situationen schreibt, in denen Ihr Angebot die Antwort ist, liest auch die Zahlen dazu und sitzt mit Ihnen im Call.",
            people=[("Steve", "Performance Manager", "Baut das Konto und liest, in welchen Gesprächen Ihre Karte geklickt wird.", "assets/img/team/steve.jpg"),
                    ("Constantin", "Design", "Baut Karte und Seite dahinter: klar, ruhig, ohne Umweg.", "assets/img/team/constantin.jpg"),
                    ("Philipp", "Sales", "Klärt vor dem Start, ob Ihre Branche werben darf, und holt die Freigabe ein.", "assets/img/ag_talk.jpg"),
                    ("Daniel", "Founder", "Schreibt die Situationen mit Ihnen und verantwortet die Empfehlung am Ende.", "assets/img/team/daniel.jpg")]),
  logos=[],
  oplist=[("case-d2c-lifestyle.html", "D2C-Lifestyle-Marke", "+57 %", "Jahresumsatz, Blended ROAS 5,57"),
          ("case-consumer-brand.html", "Premium-Consumer-Brand", "4,02", "ROAS am Black Friday, Benchmark 2,3"),
          ("case-premium-neubau.html", "Premium-Neubau, Wien", "489", "Anfragen, eine Botschaft trug 54 %")],
  fit=dict(label="Bevor wir starten",
           h=["Passt es?", "In beide Richtungen."],
           yes_h="Wir passen zusammen, wenn",
           no_h="Wir sind die Falschen, wenn",
           intro="Der Kanal ist in Österreich seit wenigen Wochen offen, die meisten Wettbewerber prüfen noch. Wer heute startet, ist dort präsent, wo Entscheidungen fallen, bevor es voll wird. Gleichzeitig gilt: Nicht jede Branche ist freigegeben. Wir prüfen das im ersten Gespräch, offen und in beide Richtungen.",
           yes=["Shop mit klarem Produktversprechen, das man empfehlen kann",
                "B2B und Software, wo Menschen erst fragen und dann kaufen",
                "Gastro, Event, Reise, Bildung ohne Gesundheitsbezug",
                "Plattformen und Marktplätze, auch für Immobilien"],
           no=["Einzelne Wohnungen oder Objekte als Anzeigenziel",
               "Finanzdienstleistungen ohne Freigabe von OpenAI",
               "Gesundheit, Recht, Glücksspiel, Dating",
               "Der Kanal soll in vier Wochen Google ersetzen"]),
  steps_next=dict(
    h="Von der Anfrage zur ersten Karte.",
    rows=[("Heute", "Anfrage und erste Einschätzung", "Branche, Angebot, Erwartung: zwei Minuten. Innerhalb eines Tages sagen wir Ihnen, ob Sie dort werben dürfen und ob sich ein Test lohnt."),
          ("Tag 2 bis 10", "Wir bauen Ihre Präsenz in der Antwort", "Das Konto bleibt in Ihrem Besitz. Wir schreiben die Situationen, in denen Ihr Angebot die Antwort ist, und bauen Karten, Seite und Messung."),
          ("Woche 3 bis 6", "Vier Wochen Test, eine klare Antwort", "Mehrere Karten laufen gegeneinander, wöchentlich lesen wir die Zahlen mit Ihnen. Am Ende wissen Sie, ob der Kanal für Sie trägt.")]),
  deliver=["Klare Aussage, ob Ihre Branche werben darf, innerhalb eines Tages",
           "Karten, die sich wie Antworten anfühlen, und die Seite dahinter",
           "Messung bis auf die einzelne Karte, ohne Schönrechnen",
           "Wöchentliche Lesung und nach vier Wochen eine klare Empfehlung"],
  trust=["Eignungs-Check kostenlos", "Kein Vertrag für den Test", "Konto bleibt bei Ihnen", "Keine Freigabe, keine Rechnung"],
  faq=[("Warum jetzt und nicht in einem Jahr?", "Weil der Platz in der Antwort begrenzt ist und der Kanal in Österreich gerade erst aufgeht. Wer heute startet, ist dort präsent, wo Entscheidungen fallen, bevor Wettbewerber es sind, und kennt in sechs Monaten seine Botschaften und Kosten, während andere anfangen."),
       ("Fühlt sich das für meine Kunden nicht wie Werbung an?", "Die Karte erscheint nur, wenn das Gespräch zu Ihrem Angebot passt, und sie unterbricht nichts. Sie ist als gesponsert gekennzeichnet, wirkt aber wie eine Empfehlung im richtigen Moment. Das ist der Unterschied zu jedem Banner."),
       ("Können wir das nicht selbst machen?", "Das Konto anlegen: ja. Der Unterschied liegt in der Prüfung vorab, in Karten, die aus der Frage heraus geschrieben sind, in der Seite dahinter und in einer Messung, die die Grenzen des Kanals kennt. Genau das bringen wir aus dem Frühzugang mit."),
       ("Dürfen wir überhaupt werben?", "Nicht jede Branche ist freigegeben: Finanz und Gesundheit brauchen im europäischen Raum eine Zustimmung, einzelne Immobilienobjekte sind ausgeschlossen, Plattformen erlaubt. Wir klären das im ersten Gespräch, und ohne Freigabe gibt es keine Kampagne und keine Rechnung."),
       ("Was kostet der Test?", "Das Mediabudget legen Sie fest. Unsere Leistung für den Vier-Wochen-Test ist pauschal, ohne Vertrag darüber hinaus. Der Eignungs-Check davor ist kostenlos."),
       ("Und wenn der Kanal nichts bringt?", "Dann steht das nach vier Wochen so im Report, mit der Empfehlung zu stoppen. Sie haben dann für überschaubares Geld eine Antwort, die Ihre Wettbewerber noch nicht haben.")],
  offer_h="Der Einstieg ist ein Eignungs-Check. Kostenlos, ohne Vertrag.",
  offer=["Wir prüfen, ob Ihre Branche in ChatGPT werben darf, schreiben drei Situationen, in denen Ihr Angebot die Antwort ist, und eine Karte als Vorschlag. Innerhalb eines Tages wissen Sie, ob sich ein Test lohnt. Danach entscheiden Sie.",
         "<b>Risikoumkehr inklusive:</b> Braucht Ihre Branche eine Freigabe, holen wir sie ein, bevor ein Euro läuft. Kommt sie nicht, gibt es keine Kampagne und keine Rechnung. Und nach vier Wochen sagen wir Ihnen ehrlich, ob es sich lohnt weiterzumachen."],
  chips=["Eignungs-Check", "Vier-Wochen-Test", "Konto-Setup", "Gesprächssituationen", "Kartenvarianten", "Landingpage", "Pixel & CAPI", "Zweitmeinung"]),

]


# Stoerer vor dem Angebot: ein Bild, ein Satz zur Risikoumkehr, dunkel gesetzt
STOER = {
 "service-performance-marketing": dict(img="assets/img/retreat-04.jpg", side="left", al="Die Risikoumkehr",
    ah=["Wir gewinnen nur,", "wenn Sie gewinnen."],
    aside="Basis-Fixum plus Erfolgsbeteiligung: Unsere Vergütung hängt an dem, was sich messen lässt. Das ist kein Marketing-Satz, sondern unser Vertrag.",
    zl="Wie wir arbeiten", zt="Dieselben Leute im Call, die auch die Kampagne bauen."),
 "service-ecommerce": dict(img="assets/img/retreat-11.jpg", side="left", al="Die Risikoumkehr",
    ah=["Beteiligt am Umsatz.", "Nicht am Aufwand."],
    aside="Basis-Fixum plus Beteiligung am messbaren Umsatz statt Retainer. Wo sich Umsatz nicht sauber messen lässt, sagen wir das vorher, nicht nachher.",
    zl="Wie wir arbeiten", zt="Ads, Shop und Tracking aus einer Hand."),
 "service-content-creation": dict(img="assets/img/retreat-08.jpg", side="left", al="Die Risikoumkehr",
    ah=["Verkauft es nicht,", "zählt es nicht."],
    aside="Läuft die Produktion mit Performance-Mandat, koppeln wir die Vergütung an messbare Ergebnisse. Wir gewinnen nur, wenn Sie gewinnen.",
    zl="Wie wir arbeiten", zt="Wer dreht, liest auch die Zahlen zum Motiv."),
 "service-websites": dict(img="assets/img/retreat-01.jpg", side="left", al="Die Risikoumkehr",
    ah=["Anfragen statt Lob.", "Daran messen wir uns."],
    aside="Läuft die Seite im Performance-Mandat, hängt unsere Vergütung an messbaren Ergebnissen. Wir gewinnen nur, wenn Sie gewinnen.",
    zl="Wie wir arbeiten", zt="Design, Text und Tracking sitzen im selben Raum."),
 "service-strategie": dict(img="assets/img/retreat-05.jpg", side="left", al="Die Risikoumkehr",
    ah=["Strategie, gemessen", "am Ergebnis."],
    aside="Geht die Strategie in ein Umsetzungs-Mandat über, koppeln wir die Vergütung an messbare Ergebnisse. Wir gewinnen nur, wenn Sie gewinnen.",
    zl="Wie wir arbeiten", zt="Zielbild, KPI-Logik, Reihenfolge. Dann bauen."),
 "service-chatgpt-ads": dict(img="assets/img/retreat-06.jpg", side="left", al="Die Risikoumkehr",
    ah=["Keine Freigabe,", "keine Rechnung."],
    aside="Braucht Ihre Branche eine Freigabe, holen wir sie ein, bevor ein Euro läuft. Kommt sie nicht, gibt es keine Kampagne. Und nach vier Wochen sagen wir ehrlich, ob es weitergeht.",
    zl="Wie wir arbeiten", zt="Präsent, wo entschieden wird. Vor allen anderen."),
}

import json as _json
_MF = _json.load(open("assets/content.json", encoding="utf-8"))
_ORIENT = {}
for _slug, _e in _MF.items():
    for _im in _e.get("imgs", []):
        _ORIENT[_im["src"]] = _im["portrait"]
    for _v in _e.get("vids", []):
        _ORIENT[_v["src"]] = True

def _wall(s):
    w = s.get("wall")
    cols = SVC_WALL.get(s["slug"], [])
    if not w or not cols:
        return ""
    speeds = ["0.055", "0.105", "0.075", "0.125", "0.09"]
    ratios = ["r1", "r2", "r1", "r3", "r2", "r1", "r3", "r2"]
    parts = []
    for i, col in enumerate(cols):
        cells = []
        for j, m in enumerate(col):
            cls = ratios[(i * 3 + j) % len(ratios)]
            inner = ('<video data-auto muted loop playsinline preload="none" src="%s"></video>' % m) if m.endswith(".mp4") \
                    else ('<img loading="lazy" decoding="async" src="%s" alt="">' % m)
            cells.append('<span class="cwt %s">%s</span>' % (cls, inner))
        parts.append('        <div class="cwcol" data-drift="%s">\n          %s\n        </div>'
                     % (speeds[i % len(speeds)], "\n          ".join(cells)))
    head = "".join('<span class="rl"><span>%s</span></span>' % x for x in w["h"])
    link = ('<a class="zalink" href="%s">%s</a>' % w["link"]) if w.get("link") else ""
    return ('  <!-- CONTENT-WAND: HOCHFORMAT AUS LAUFENDEN MANDATEN -->\n'
            '  <section class="cwall" data-bg="#08080A" data-fg="light">\n'
            '      <div class="cwcols">\n%s\n      </div>\n'
            '      <div class="cwfront"><div class="cwbar">\n'
            '      <div class="cwveil"></div>\n'
            '      <div class="cwtxt">\n'
            '        <span class="label" style="color:var(--champ)">%s</span>\n'
            '        <h2 class="cwh" data-lines>%s</h2>\n'
            '        <p class="cwp" data-fade>%s</p>\n'
            '        %s\n'
            '      </div>\n'
            '      </div></div>\n'
            '  </section>\n\n') % ("\n".join(parts), w["label"], head, w["t"], link)


def _content_section(slug, label="Aus laufenden Mandaten"):
    cols = SVC_COLS.get(slug, [])
    if not cols:
        return ""
    speeds = ["0.042", "0.068", "0.05", "0.075", "0.056", "0.072"]
    parts = []
    for i, col in enumerate(cols):
        if not col:
            continue
        cells = []
        for m in col:
            if m.endswith(".mp4"):
                cells.append('<video data-auto muted loop playsinline preload="none" src="%s"></video>' % m)
            else:
                cells.append('<img loading="lazy" decoding="async" src="%s" alt="">' % m)
        parts.append('      <div class="cpcol" data-drift="%s">\n        %s\n      </div>' % (speeds[i], "\n        ".join(cells)))
    return ('  <!-- CONTENT AUS DEM MANDAT -->\n'
            '  <section class="collage collage--tight" data-bg="#08080A" data-fg="light" style="background:#08080A">\n'
            '    <div class="wrap" style="position:relative;z-index:2;margin-bottom:clamp(30px,4vw,60px)">\n'
            '      <span class="label" style="color:var(--champ)">' + label + '</span>\n'
            '    </div>\n'
            '    <div class="cplane">\n%s\n    </div>\n  </section>\n\n') % ("\n".join(parts))


def _heronum(s):
    hn = s.get("heronum")
    if not hn:
        return ""
    return ('      <div class="hnumline" data-fade style="--i:3">\n'
            '        <span class="hv">%s</span>\n'
            '        <span class="hl">%s</span>\n'
            '      </div>\n') % (hn[0], hn[1])

def _tell(s):
    t = s.get("tell")
    if not t:
        return ""
    steps = "\n        ".join(
        '<div class="ts%s" data-v="%s" data-l="%s">\n          <div class="tt">%s</div>\n          <p>%s</p>\n        </div>'
        % ((" on" if i == 0 else ""), v, l, tt, p) for i, (v, l, tt, p) in enumerate(t["steps"]))
    first = t["steps"][0]
    return ('  <!-- ERGEBNIS ALS STATIONEN (scrollgesteuert) -->\n'
            '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(70px,9vw,140px)">\n'
            '    <div class="wrap">\n'
            '      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(30px,3.6vw,52px)">%s</span>\n'
            '      <div class="tell">\n'
            '        <div class="tsteps">\n        %s\n        </div>\n'
            '        <div class="tfix">\n'
            '          <div class="tv">%s</div>\n'
            '          <div class="tl">%s</div>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n  </section>\n\n') % (t.get("label", "Ein Fall, nachgerechnet"), steps, first[0], first[1])

def _channels(s):
    c = s.get("channels")
    if not c:
        return ""
    rows = "\n        ".join(
        '<div class="cr%s"><span class="cn">%s</span><span class="ct"><i class="cf" data-w="%d"></i></span><span class="cv">%s</span></div>'
        % ((" blend" if i == len(c["rows"]) - 1 else ""), n, w, v) for i, (n, w, v) in enumerate(c["rows"]))
    return ('      <div>\n'
            '        <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:20px">%s</span>\n'
            '        <div class="chrow">\n        %s\n        </div>\n'
            '        <p style="font-size:12.5px;color:var(--grey-dark);margin-top:16px;max-width:56ch">%s</p>\n'
            '      </div>\n') % (c["label"], rows, c["note"])

def _quote(s):
    q = s.get("quote")
    if not q:
        return ""
    return ('      <div class="qbox" data-fade>\n'
            '        <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:18px">Eine Stimme</span>\n'
            '        <p class="qt">&bdquo;%s&ldquo;</p>\n'
            '        <div class="qa">%s</div>\n'
            '      </div>\n') % (q[0], q[1])

def _fit(s):
    f = s.get("fit")
    if not f:
        return ""
    yes = "\n            ".join("<li>%s</li>" % x for x in f["yes"])
    no = "\n            ".join("<li>%s</li>" % x for x in f["no"])
    head = "".join('<span class="rl"><span>%s</span></span>' % x
                   for x in (f["h"] if isinstance(f["h"], list) else [f["h"]]))
    cap = ('      <div class="fitcap" data-fade>\n'
           '        <span class="fcnum">%s</span>\n'
           '        <span class="fctxt">%s</span>\n'
           '      </div>\n') % (f.get("cap_v", ""), f.get("cap_t", "")) if f.get("cap_t") and f.get("cap_v") else ""
    return ('  <!-- GEGENSEITIGE PRUEFUNG -->\n'
            '  <section class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark" style="padding:clamp(90px,11vw,150px) 0">\n'
            '    <div class="wrap">\n'
            '      <div class="fithead">\n'
            '        <div>\n'
            '          <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(16px,1.8vw,24px)">%s</span>\n'
            '          <h2 class="dispn fitH" data-lines>' + head + '</h2>\n'
            '        </div>\n'
            '        <p class="fitlead" data-fade>%s</p>\n'
            '      </div>\n'
            + cap +
            '      <div class="fit" data-stagger>\n'
            '        <div class="fcol yes" data-fade><div class="fh">%s</div>\n          <ul>\n            %s\n          </ul>\n        </div>\n'
            '        <div class="fcol no" data-fade><div class="fh">%s</div>\n          <ul>\n            %s\n          </ul>\n        </div>\n'
            '      </div>\n'
            '    </div>\n  </section>\n\n') % (f.get("label", "Bevor wir starten"), f["intro"],
       f.get("yes_h", "Wir passen zusammen, wenn"), yes,
       f.get("no_h", "Wir sind die Falschen, wenn"), no)

def _next(s):
    n = s.get("steps_next")
    if not n:
        return ""
    rows = "\n        ".join(
        '<div class="op">\n'
        '          <span class="owhen">%s</span>\n'
        '          <span class="otitle">%s</span>\n'
        '          <span class="odesc">%s</span>\n'
        '        </div>' % (w, t, d)
        for w, t, d in n["rows"])
    return ('  <!-- WAS ALS NAECHSTES PASSIERT (dunkles Kapitel, Zeilen werden beim Scrollen aktiv) -->\n'
            '  <section class="sec fg-dark nextsec" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">\n'
            '    <div class="wrap">\n'
            '      <span class="label" style="color:var(--champ);display:block;margin-bottom:clamp(24px,3vw,40px)">Was als Nächstes passiert</span>\n'
            '      <h2 class="dispn" data-lines style="font-size:clamp(32px,3.8vw,62px);margin-bottom:clamp(36px,4.4vw,60px)"><span class="rl"><span>%s</span></span></h2>\n'
            '      <div class="oplist oplist--steps">\n        %s\n      </div>\n'
            '    </div>\n  </section>\n\n') % (n["h"], rows)

def _stoer(s):
    z = STOER.get(s["slug"])
    if not z:
        return ""
    pos = "left:clamp(24px,6vw,110px)" if z["side"] == "right" else "right:clamp(24px,6vw,110px)"
    ah = "".join('<span class="rl"><span>%s</span></span>' % x for x in z["ah"])
    return ('  <!-- STOERER: RISIKOUMKEHR ALS BILD -->\n'
            '  <section class="zoomsec zoomsec--dark" data-side="%s" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">\n'
            '    <div class="zsticky">\n'
            '      <div class="zaside fg-dark" style="%s">\n'
            '        <span class="label" style="color:var(--champ)">%s</span>\n'
            '        <h3 class="zah" data-lines>%s</h3>\n'
            '        <p class="zasub">%s</p>\n'
            '      </div>\n'
            '      <div class="zmedia"><img src="%s" alt=""></div>\n'
            '      <div class="zcap">\n'
            '        <span class="zl">%s</span>\n'
            '        <div class="zt">%s</div>\n'
            '      </div>\n'
            '    </div>\n'
            '  </section>\n\n') % (z["side"], pos, z["al"], ah, z["aside"], z["img"], z["zl"], z["zt"])

def _deliver(s):
    d = s.get("deliver")
    if not d:
        return ""
    return ('        <ul style="list-style:none;margin:22px 0 0;padding:0;display:flex;flex-direction:column;gap:10px">\n'
            + "\n".join('          <li style="font-size:14.5px;color:var(--ink);padding-left:18px;position:relative"><i style="position:absolute;left:0;top:0.62em;width:9px;height:1.5px;background:var(--champ-deep)"></i>%s</li>' % x for x in d)
            + '\n        </ul>\n')

def _trust(s):
    t = s.get("trust")
    if not t:
        return ""
    return ('      <div class="trust" data-fade>' + "".join("<span>%s</span>" % x for x in t) + '</div>\n')


def _bars(s):
    b = s.get("bars")
    if not b:
        return ""
    rows = "\n        ".join(
        '<div class="brow%s"><span class="bwho">%s</span><span class="btrack"><i class="bfill" data-w="%d"></i></span><span class="bval">%s</span></div>'
        % ((" now" if i == len(b["rows"]) - 1 else ""), w, pct, v) for i, (w, pct, v) in enumerate(b["rows"]))
    blink = ('        <a class="zalink" href="%s">%s</a>\n' % b["link"]) if b.get("link") else ""
    solo = "" if s.get("tell") else " barsblock--solo"
    return ('      <div class="barsblock%s">\n'
            '        <span class="label bt">%s</span>\n'
            '        <div class="bacmp">\n        %s\n        </div>\n'
            '        <p class="bnote">%s</p>\n'
            '%s'
            '      </div>\n') % (solo, b["label"], rows, b["note"], blink)

def _crew(s):
    c = s.get("crew")
    if not c:
        return ""
    cells = "\n        ".join(
        '<div class="pcell" data-fade style="--i:%d">\n'
        '          <div class="pportrait" data-scale><img loading="lazy" decoding="async" src="%s" alt=""></div>\n'
        '          <div class="pname"><b>%s</b><span>%s</span></div>\n'
        '          <p class="prole">%s</p>\n'
        '        </div>' % (i, img, name, role, txt)
        for i, (name, role, txt, img) in enumerate(c["people"]))
    head = "\n        ".join('<span class="rl"><span>%s</span></span>' % x for x in c["h"])
    return ('  <!-- WER DARAN ARBEITET -->\n'
            '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">\n'
            '    <div class="wrap">\n'
            '      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(20px,2.4vw,32px)">%s</span>\n'
            '      <h2 class="disp" data-lines style="text-transform:none;letter-spacing:-0.028em">\n'
            '        %s\n'
            '      </h2>\n'
            '      <p data-fade style="max-width:50ch;margin-top:clamp(20px,2.4vw,32px);color:var(--grey-dark);font-size:16px;line-height:1.65">%s</p>\n'
            '      <div class="pgrid pgrid--role" data-stagger>\n'
            '        %s\n'
            '      </div>\n'
            '    </div>\n'
            '  </section>\n\n') % (c["label"], head, c["t"], cells)


def _voice(s):
    v = s.get("voice")
    if not v:
        return ""
    if v.get("video"):
        media = ('      <div class="vmedia vmedia--video" data-fade>\n'
                 '        <div class="pwiv">\n'
                 '          <video class="ivplayer" data-auto muted loop playsinline preload="metadata" poster="%s" width="640" height="1138" src="%s"></video>\n'
                 '          <button class="ivsound" type="button" aria-label="Ton einschalten"><span class="ivbars"><i></i><i></i><i></i></span><span class="ivlabel">Ton an</span></button>\n'
                 '        </div>\n'
                 '      </div>\n') % (v["video"].replace(".mp4", "-poster.jpg"), v["video"])
    else:
        media = ('      <div class="vmedia" data-fade><span data-scale><img loading="lazy" decoding="async" src="%s" alt=""></span></div>\n'
                 % v["img"])
    quote = ('        <p class="vq" data-fade>&bdquo;%s&ldquo;</p>\n' % v["q"]) if v.get("q") else \
            ('        <p class="vq vq--lead" data-fade>%s</p>\n' % v.get("lead", ""))
    return ('  <!-- WAS KUNDEN SAGEN -->\n'
            '  <section class="sec fg-dark" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">\n'
            '    <div class="wrap vsplit">\n'
            '      <div class="vtxt">\n'
            '        <span class="label" style="color:var(--champ)">%s</span>\n'
            + quote +
            '        <div class="va" data-fade>%s</div>\n'
            '        <p class="vnote" data-fade>%s</p>\n'
            '      </div>\n'
            + media +
            '    </div>\n'
            '  </section>\n\n') % (v["label"], v["a"], v["note"])


# Handgebaute Cases und ihre Leistungen (stehen nicht in CASES/WEBCASES als Daten)
HAND_CASES = {
    "case-premium-neubau.html": ("Premium-Neubau, Wien", ["service-performance-marketing.html", "service-content-creation.html", "service-websites.html"]),
    "case-kommunalkredit.html": ("Kommunalkredit, Sommergespräche", ["service-content-creation.html", "service-performance-marketing.html", "service-strategie.html"]),
}

def _all_cases_for(slug):
    """(href, titel) aller Cases, die die Leistung <slug> als Leistung ausweisen"""
    href = slug + ".html"
    out = []
    for c in CASES:
        if c.get("handmade"):
            continue
        if any(h == href for _, h in c["disz"]):
            out.append((c["slug"] + ".html", c["nav_title"]))
    for c in WEBCASES:
        disz = c.get("disz", [("Websites & Landingpages", "service-websites.html")])
        if any(h == href for _, h in disz):
            out.append((c["slug"] + ".html", c["name"]))
    for h, (t, svcs) in HAND_CASES.items():
        if href in svcs:
            out.append((h, t))
    return out

def _more_cases(s):
    listed = {h for h, _, _, _ in s.get("oplist", [])}
    allc = _all_cases_for(s["slug"])
    for h in listed:
        if h not in {a for a, _ in allc}:
            print("  Hinweis: %s listet %s, aber der Case verlinkt die Leistung nicht" % (s["slug"], h))
    rest = [(h, t) for h, t in allc if h not in listed]
    if not rest:
        return ""
    return ('      <p class="morecases" data-fade><span>Auch mit dieser Leistung</span>'
            + "".join('<a href="%s">%s</a>' % (h, t) for h, t in rest) + '</p>\n')

def render_service(s):
    aside_pos = "left:clamp(24px,6vw,110px)" if s["zoom"]["side"] == "right" else "right:clamp(24px,6vw,110px)"
    tags = "\n        ".join("<span>%s</span>" % t for t in s["tags"])
    h1 = ('<span class="rl"><span>%s</span></span>\n        <span class="rl"><span><i style="font-style:italic;color:var(--champ-deep)">%s</i></span></span>'
          % (s["h1"][0], s["h1"][1]))
    acc_items = []
    for t, p, lis in s["acc"]:
        li = "\n              ".join("<li>%s</li>" % x for x in lis)
        acc_items.append('''<div class="aitem">
          <button class="ahead">%s <span class="plus">+</span></button>
          <div class="abody"><div class="abody-in">
            <p>%s</p>
            <ul>
              %s
            </ul>
          </div></div>
        </div>''' % (t, p, li))
    acc = "\n        ".join(acc_items)
    dimgs = "\n            ".join(
        '<img loading="lazy" decoding="async" src="%s" alt="" class="%s">' % (img, "on" if i == 0 else "")
        for i, (k, t, p, img) in enumerate(s["diff"]))
    dblocks = "\n          ".join('''<div class="dblock" data-fade>
            <div class="pk2">%s, 0%d</div>
            <div class="ht2">%s</div>
            <p>%s</p>
          </div>''' % (k, i + 1, t, p) for i, (k, t, p, img) in enumerate(s["diff"]))
    z = s["zoom"]
    aside_pos = "left:clamp(24px,6vw,110px)" if z["side"] == "right" else "right:clamp(24px,6vw,110px)"
    nums_sec = ""
    if s.get("proof_nums"):
        nums_sec = ('      <div class="wnums" data-stagger style="justify-content:center;margin-top:clamp(30px,4vw,50px)">\n        %s\n      </div>\n'
                    % "\n        ".join('<div class="n" data-fade><div class="v num serif">%s</div><div class="l">%s</div></div>' % (v, l) for v, l in s["proof_nums"]))
    lead_sec = ""
    if s.get("proof_lead"):
        lead_sec = ('      <p data-fade style="font-family:var(--f-serif);font-size:clamp(17px,1.5vw,22px);line-height:1.6;color:var(--grey-dark);max-width:56ch;margin:clamp(26px,3vw,40px) auto 0;text-align:center">%s</p>\n'
                    % s["proof_lead"])
    vkind, vd = s["visual"]
    if vkind == "panels":
        imgs = vd["imgs"]
        col1 = "\n          ".join('<img loading="lazy" decoding="async" src="%s" alt="">' % i for i in imgs[0::2])
        col2 = "\n          ".join('<img loading="lazy" decoding="async" src="%s" alt="">' % i for i in imgs[1::2])
        visual = '''  <!-- PROOF, PANELS (Editorial, Screens scrollen vorbei) -->
  <section class="panelscroll" data-bg="#0A0A0A" data-fg="light">
    <div class="wrap pswrap">
      <div class="pstxt">
        <span class="pslabel">%s</span>
        <p class="psbody" data-fade>%s</p>
        <p class="psbody" data-fade>%s</p>
        <div class="pslinks" data-fade>
          <a href="work.html">Alle Cases</a>
          <a href="#anfrage">Projekt anfragen</a>
        </div>
        <div class="psdisc" data-stagger>
          <div data-fade><div class="dt">%s</div><div class="dd">%s</div></div>
          <div data-fade><div class="dt">%s</div><div class="dd">%s</div></div>
        </div>
      </div>
      <div class="pscols">
        <div class="pscol" data-drift="0.16">
          %s
        </div>
        <div class="pscol" data-drift="0.26">
          %s
        </div>
      </div>
    </div>
  </section>

''' % (vd.get("label", "Aus dem Mandat"), vd["h"], vd["t"],
       vd.get("d1", ("Leistungen", ""))[0], vd.get("d1", ("", ""))[1],
       vd.get("d2", ("Ergebnis", ""))[0], vd.get("d2", ("", ""))[1],
       col1, col2)
    elif vkind == "phones":
        screens = vd["phones"]
        if screens and isinstance(screens[0], list):
            screens = [x for grp in screens for x in grp]
        colA = screens[0::2]; colB = screens[1::2]
        def _pc(items, speed):
            def _pf(src):
                if src.endswith(".mp4"):
                    return '<div class="phframe"><video data-auto muted loop playsinline preload="none" src="%s"></video></div>' % src
                return '<div class="phframe"><img loading="lazy" decoding="async" src="%s" alt=""></div>' % src
            fr = "\n          ".join(_pf(i) for i in items)
            return '<div class="phcol" data-drift="%s">\n          %s\n        </div>' % (speed, fr)
        phh_lines = "".join('<span class="rl"><span>%s</span></span>' % x
                            for x in (vd["h"] if isinstance(vd["h"], list) else [vd["h"]]))
        visual = '''  <!-- PROOF, PHONES (Screens ziehen vorbei) -->
  <section class="sec fg-light bg-paper phonesec" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap phwrap">
      <div class="phtxt">
        <h2 class="phh" data-lines>%s</h2>
        <p class="lt3 phsub" data-fade>%s</p>
      </div>
      <div class="phcols">
        %s
        %s
      </div>
    </div>
  </section>

''' % (phh_lines, vd["t"], _pc(colA, "0.14"), _pc(colB, "0.24"))
    else:
        visual = '''  <!-- PROOF, STAGE -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: 0 0 clamp(110px,14vw,200px)">
    <div class="wrap">
      <div class="stage" data-fade><img loading="lazy" decoding="async" src="%s" alt=""></div>
      <p data-fade style="font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--grey-dark);margin-top:16px">%s</p>
    </div>
  </section>

''' % (vd["img"], vd["cap"])
    ops = "\n        ".join('''<a class="op" href="%s" data-fade>
          <span class="onum">0%d</span>
          <span><span class="otitle">%s</span></span>
          <span class="okpi"><span class="v">%s</span><span class="l">%s</span></span>
        </a>''' % (h, i + 1, t, v, l) for i, (h, t, v, l) in enumerate(s["oplist"]))
    more = _more_cases(s)
    cases_sec = ("""  <!-- 07, CASES -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(60px,7vw,100px)">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(28px,3.4vw,48px)">Ausgewählte Ergebnisse</span>
      <div class="oplist" data-stagger>
        """ + ops + """
      </div>
""" + more + """    </div>
  </section>

""") if s.get("oplist") else ""
    faqs = "\n        ".join('''<div class="qa aitem" data-fade>
          <button class="ahead q" type="button">%s <span class="plus">+</span></button>
          <div class="abody"><div class="abody-in"><p>%s</p></div></div>
        </div>''' % (q, a) for q, a in s["faq"])
    chips_sel = "\n        ".join('<button class="nopt" data-v="%s" style="--i:%d">%s <span class="plus">+</span></button>' % (cv, 7 - i, cv) for i, cv in enumerate(s["chips"]))
    logos = logogrid(s["logos"]) if s.get("logos") else ""
    logos_sec = ("""  <!-- LOGOS: zentriert, 2x4, flaechig -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: clamp(70px,9vw,130px) 0">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;text-align:center;margin-bottom:clamp(30px,4vw,50px)">Marken, mit denen wir in diesem Feld arbeiten</span>
      <div class="logocycle logogrid" data-fade>
        """ + logos + """
      </div>
    </div>
  </section>

""") if s.get("logos") else ""
    content_sec = _content_section(s["slug"], s.get("content_label", "Aus laufenden Mandaten"))
    content_before = content_sec if s.get("tell") else ""
    content_after = "" if s.get("tell") else content_sec
    zah = "\n          ".join('<span class="rl"><span>%s</span></span>' % x for x in s["zoom"].get("ah", []))
    zalink = ('<a class="zalink" href="%s">%s</a>' % s["zoom"]["alink"]) if s["zoom"].get("alink") else ""
    heronum_sec = _heronum(s)
    tell_sec = _tell(s)
    channels_sec = _channels(s)
    quote_sec = _quote(s)
    bars_sec = _bars(s)
    pq_sec = "" if s.get("quote") else ('<p class="serif" data-fade style="font-size:clamp(17px,1.4vw,21px);color:var(--grey-dark);max-width:52ch;margin:clamp(30px,4vw,46px) auto 0;text-align:center">%s</p>' % s["proof_quote"])
    # Beleg-Paar: was rechts neben den Kanalzeilen steht
    bars_here = "" if (s.get("tell") and s.get("bars")) else bars_sec
    right_sec = bars_sec if (s.get("tell") and s.get("bars")) else quote_sec
    proofsplit_sec = ""
    if s.get("channels") or right_sec:
        ps = s.get("proofsplit") or {}
        ps_head = "".join('<span class="rl"><span>%s</span></span>' % x
                          for x in ps.get("h", ["Wo der Unterschied", "wirklich entsteht."]))
        proofsplit_sec = ('  <!-- BELEG: ZWEI RECHNUNGEN AUS ZWEI MANDATEN -->\n'
            '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(50px,6vw,90px)">\n'
            '    <div class="wrap">\n'
            '      <div class="pshead">\n'
            '        <div>\n'
            '          <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(16px,1.8vw,24px)">%s</span>\n'
            '          <h2 class="dispn" data-lines style="font-size:clamp(30px,3.4vw,54px)">%s</h2>\n'
            '        </div>\n'
            '        <p class="pslead" data-fade>%s</p>\n'
            '      </div>\n'
            '      <div class="proofsplit">\n') % (
                ps.get("label", "Zwei Rechnungen"), ps_head,
                ps.get("t", "Zwei Mandate, zwei Fragen: Welche Strecke bringt die Anfrage billiger, und was passiert, wenn die Struktur stimmt statt das Budget wächst. Beide Zahlen stehen so im Reporting."))
        # Grafiken enthalten Prozentzeichen: erst formatieren, dann anhaengen
        proofsplit_sec += (channels_sec or "      <div></div>\n") + (right_sec or "      <div></div>\n")
        proofsplit_sec += '      </div>\n    </div>\n  </section>\n\n'
    wall_sec = _wall(s)
    crew_sec = _crew(s)
    voice_sec = _voice(s)
    fit_sec = _fit(s)
    next_sec = _next(s) + _stoer(s)
    deliver_sec = _deliver(s)
    trust_sec = _trust(s)

    page = HEAD.format(title=s["nav"], bodybg="#F3EDE1") + menu("index.html#leistungen") + '''<main>

  <!-- 01, HERO -->
  <section class="svc-hero fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="position:relative">
    <a class="svc-back" href="index.html#leistungen">← Alle Leistungen</a>
    <div class="wrap">
      <div class="svc-glyph" data-fade></div>
      <span class="label slabel" data-fade>''' + s["label"] + '''</span>
      <h1 data-lines>
        ''' + h1 + '''
      </h1>
      <div class="tags" data-fade>
        ''' + tags + '''
      </div>
      <p class="ssub" data-fade style="--i:1">''' + s["sub"] + '''</p>
      <div data-fade style="--i:2;margin-top:28px"><a class="alink" href="#anfrage">Direkt anfragen ↓</a></div>
''' + heronum_sec + '''
    </div>
  </section>

  <!-- 03, LÖSUNG: INTRO + AKKORDEON -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(30px,4vw,60px)">
    <div class="wrap svc-split">
      <div class="intro">
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:20px">''' + s.get("sol_label", "Die Lösung") + '''</span>
        <p class="serif" data-scrub>''' + s["intro"] + '''</p>
      </div>
      <div class="acc">
        ''' + acc + '''
      </div>
    </div>
  </section>

  <!-- 04, WAS WIR ANDERS MACHEN (BiA-Split: links sticky, rechts Text) -->
  <section class="sec diffsec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(40px,5vw,70px)">Was wir anders machen</span>
      <div class="dgrid">
        <div class="dleft">
          <div class="dnum">01</div>
          <div class="dimg">
            ''' + dimgs + '''
          </div>
        </div>
        <div class="dright">
          ''' + dblocks + '''
        </div>
      </div>
    </div>
  </section>

  <!-- 05, PROOF 1: ZOOM -->
  <section class="zoomsec" data-side="''' + z["side"] + '''" data-bg="#F3EDE1" data-fg="dark">
    <div class="zsticky">
      <div class="zaside fg-light" style="''' + aside_pos + '''">
        <span class="label" style="color:var(--champ-deep)">''' + z.get("al", "Der Beweis") + '''</span>
        <h3 class="zah" data-lines>''' + zah + '''</h3>
        <p class="zasub">''' + z["aside"] + '''</p>
        ''' + zalink + '''
      </div>
      <div class="zmedia"><img src="''' + z["img"] + '''" alt=""></div>
      <div class="zcap">
        <span class="zl">''' + z["zl"] + '''</span>
        <div class="zt">''' + z["zt"] + '''</div>
      </div>
    </div>
  </section>

  <!-- 06, PROOF 2: ERGEBNISSE -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap" style="max-width:1100px">
      <span class="label" style="color:var(--champ-deep);display:block;text-align:center">''' + s.get("proof_label", "Ergebnisse") + '''</span>
      <h2 class="dispn" data-lines style="font-size:clamp(36px,4.6vw,78px);text-align:center;margin-top:22px">
        <span class="rl"><span>''' + s["proof_h"][0] + '''</span></span>
        <span class="rl"><span><i style="font-style:italic">''' + s["proof_h"][1] + '''</i></span></span>
      </h2>
''' + nums_sec + lead_sec + pq_sec + bars_here + '''
    </div>
  </section>

''' + tell_sec + content_before + proofsplit_sec + visual + wall_sec + crew_sec + voice_sec + cases_sec + logos_sec + content_after + fit_sec + '''  <!-- 08, FAQ -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap faq">
      <div>
        <h2 class="disp" data-lines style="text-transform:none;letter-spacing:-0.02em"><span class="rl"><span>Die ehrlichen</span></span><span class="rl"><span>Fragen.</span></span></h2>
        <p class="fint" data-fade>Was uns vor dem Start wirklich gefragt wird, und was wir antworten.</p>
      </div>
      <div data-stagger>
        ''' + faqs + '''
      </div>
    </div>
  </section>

''' + next_sec + '''  <!-- 09, NO-BRAINER + RISIKOUMKEHR -->
  <section class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Das Angebot</span>
        <div class="lh" data-lines><span class="rl"><span>''' + s["offer_h"] + '''</span></span></div>
      </div>
      <div data-stagger>
        <p class="lt3" data-fade>''' + s["offer"][0] + '''</p>
        <p class="lt3" data-fade>''' + s["offer"][1] + '''</p>
''' + deliver_sec + '''
      </div>
    </div>
  </section>

  <!-- 10, CTA: ANFRAGE-MECHANIK -->
  <section id="anfrage" class="sec fg-light bg-cream help" data-bg="#EFE7D6" data-fg="dark" style="padding-top:0">
    <div class="wrap">
      <h2 data-lines>
        <span class="rl"><span>Womit können</span></span>
        <span class="rl"><span>wir helfen?</span></span>
      </h2>
      <div class="needbar" data-fade>
        <span class="nlead">Ich brauche</span>
        <span class="nsel"></span>
        <button class="ngo">Weiter →</button>
      </div>
      <div class="needgrid" data-fade>
        ''' + chips_sel + '''
      </div>
      <p data-fade style="font-size:13px;color:var(--grey-dark);margin-top:26px">Auswahl treffen, weiter klicken, und Ihre Anfrage ist vorformuliert.</p>
''' + trust_sec + '''
    </div>
  </section>

''' + FOOTER
    return page

for s in SERVICES:
    open(s["slug"] + ".html", "w", encoding="utf-8").write(render_service(s))
    print("service", s["slug"])
print("services done")

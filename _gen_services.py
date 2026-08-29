# Service-LP-Generator: Schema Problem → Konsequenz → Lösung → Differenzierung →
# Proof ×3 → Logos → Case-Liste → FAQ → No-Brainer + Risikoumkehr → CTA
# -*- coding: utf-8 -*-
from _gen import HEAD, FOOTER, menu, logocycle

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

SERVICES = [
 dict(slug="service-ecommerce", nav="E-Commerce Growth", label="Leistung · E-Commerce Growth",
  h1=["Ihr Shop wächst.", "Planbar."], ital=1,
  tags=["Meta · Google · TikTok · Pinterest", "Shop & Conversion", "Server-side Tracking", "UGC & Creatives"],
  sub="Ads, Creatives, Shop und Tracking aus einer Hand, vergütet am Ergebnis.",
  problem_h=["Das Problem"],
  problem=["Sie kaufen Besucher, aber zu wenige kaufen: Steigende Klickpreise drücken die Marge, der Checkout verliert Käufer, und das Reporting verschleiert mehr, als es zeigt.",
           "<b>Mehr Budget skaliert dann nur das Problem.</b> Jeder Monat mit undichtem Funnel wird teurer, während Wettbewerber mit sauberem Setup denselben Klick in mehr Umsatz übersetzen."],
  intro="Wir skalieren <b>D2C-Marken</b>, die wachsen wollen, statt Budget zu testen. Der Hebel liegt selten in mehr <b>Spend</b>, sondern im Zusammenspiel aus <b>Creative</b>, <b>Shop</b> und <b>Messung</b>. Deshalb bauen wir das System, nicht die Einzelmaßnahme.",
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
  zoom=dict(img="assets/img/isi.jpg", side="right", aside="Saison als Architektur statt Zufall: Awareness im Vorlauf, Sales-Druck im Peak.",
            zl="Premium-Consumer-Brand · Meta", zt="Black-Friday-ROAS 4,02. Benchmark 2,3."),
  proof_h=["+57 % Jahresumsatz.", "Aus demselben Traffic."],
  proof_nums=[("5,57", "Blended ROAS, Ziel war 3,5"), ("€ 312k", "Umsatz aus € 56k Mediabudget"), ("+56 %", "Bestellungen im Rekordjahr")],
  proof_quote="„Pinterest führte mit ROAS 6,99, Google folgte mit 5,98. Inklusive Agentur-Fee blieb der Blend bei 4,17.“ Solche Sätze stehen bei uns im Reporting, nicht im Kleingedruckten.",
  visual=("panels", dict(h="Der Auftritt, der verkauft.", t="Shop, Markenwelt und Kampagne aus einem Guss: Auftritte aus laufenden Commerce-Mandaten.",
                          imgs=["assets/img/d_isi.jpg", "assets/img/d_noma.jpg", "assets/img/d_ib7.jpg", "assets/img/d_funkhaus.jpg"])),
  logos=["looops", "isi", "nordicspirit", "ilbosso", "kaisers", "jti"],
  oplist=[("case-consumer-brand.html", "Premium-Consumer-Brand", "4,02", "BFCM-ROAS · +75 %"),
          ("case-d2c-lifestyle.html", "D2C-Lifestyle-Marke", "+57 %", "Jahresumsatz · ROAS 5,57"),
          ("case-health-brand.html", "Dental-/Health-Marke", "1.385", "Verkäufe · ehrlich reportet")],
  faq=[("Wir haben schon eine Agentur. Warum wechseln?", "Nicht wechseln, vergleichen: Der Audit zeigt in zwei Wochen, wo Ihr Setup Geld liegen lässt. Danach entscheiden Sie mit Zahlen, nicht mit Bauchgefühl."),
       ("Was, wenn der ROAS nicht kommt?", "Dann verdienen wir weniger: Unsere Vergütung ist an den messbaren Umsatz gekoppelt. Skin in the Game heißt, dass Ihr Risiko auch unseres ist."),
       ("Wie schnell sehen wir Ergebnisse?", "Erste Signale nach dem Audit, belastbare Trends nach sechs bis acht Wochen Testing. Wir versprechen keine Wunder in Woche eins, dafür eine Kurve, die hält.")],
  offer_h="Der Einstieg ist ein Audit. Kein Vertrag.",
  offer=["Wir prüfen Ads, Shop, Tracking und Checkout und zeigen Ihnen in zwei Wochen konkret, wo Umsatz liegen bleibt. Danach entscheiden Sie: umsetzen mit uns, umsetzen ohne uns, oder gar nicht.",
         "<b>Und wenn wir zusammenarbeiten, gilt die Risikoumkehr:</b> Basis-Fixum plus Beteiligung am messbaren Umsatz. Wächst Ihr Umsatz nicht, verdienen wir weniger. Wo sich Umsatz nicht sauber messen lässt, sagen wir das vorher, nicht nachher."],
  chips=["Shop-Audit", "Ads-Setup", "UGC & Creatives", "Landingpage", "Tracking-Setup", "Conversion-Optimierung", "Zweitmeinung", "Growth-Partnerschaft"]),

 dict(slug="service-performance-marketing", nav="Performance Marketing", label="Leistung · Performance Marketing",
  h1=["Jeder Euro.", "Zurechenbar."], ital=1,
  tags=["Meta · Google · TikTok", "Lead-Generierung", "Creative-Testing", "Ehrliche Attribution"],
  sub="Kampagnen, die Leads und Verkäufe bringen, nicht Reichweite. Mit Attribution, der Sie trauen können.",
  problem_h=["Das Problem"],
  problem=["Budget läuft, Dashboards leuchten, aber niemand kann sagen, welcher Euro wirklich Umsatz gebracht hat. Doppelt gezählte Conversions feiern Erfolge, die es nie gab.",
           "<b>Ohne saubere Zurechnung fließt Budget monatelang in Kanäle, die nur Klicks liefern.</b> Der CPL steigt, die Pipeline bleibt leer, und am Ende heißt es: Performance funktioniert bei uns nicht."],
  intro="Wir steuern <b>Meta, Google und TikTok</b> mit einer Regel: <b>Das Creative ist der Hebel</b>, nicht das Budget. Getestet wird systematisch, gemessen wird ehrlich, umgeschichtet wird <b>wöchentlich</b>.",
  acc=[("Kampagnen-Setup", "Strukturen, die skalieren können: nach Rolle getrennte Kampagnen, saubere Zielwerte, Budgets dort, wo der ehrliche CPL hinzeigt.",
        ["Meta, Google, TikTok", "Instant Forms & Lead-Strecken", "Kaufnahe Search-Intents", "Budget-Steuerung, wöchentlich"]),
       ("Creative-Testing", "Viele Varianten, klare Sieger: Bei einem Wiener Neubauprojekt trug ein einziges Interior-Motiv 54 Prozent aller Leads.",
        ["Systematische Testing-Loops", "Winner-Selektion nach CPL und CPA", "UGC gegen Studio getestet", "Botschaften je Zielgruppe"]),
       ("Tracking & Attribution", "Server-side Tracking und Blended-Sicht: Jede Conversion wird einmal gezählt, nicht zweimal gefeiert.",
        ["Server-side Tracking", "Blended-Sicht statt Kanal-Ego", "CRM-Anbindung", "Consent-konform"]),
       ("Reporting", "Wöchentlich, transparent, auch unbequem: Ziel-Gaps und gestoppte Tests stehen im Report.",
        ["Wöchentliches Reporting", "Ehrliche Ziel-Gaps", "Klare Handlungsempfehlungen", "Direkter Draht, kein Ticketsystem"])],
  diff=[("Anders als üblich", "Das Creative ist der Hebel", "Nicht das größte Budget gewinnt, sondern das stärkste Motiv. Wir verschieben Budget konsequent auf die Gewinner.", "assets/img/a_funk2.jpg"),
        ("Anders als üblich", "Ehrlich, auch wenn es wehtut", "In einem Finance-Mandat brachte ein Paid-Test über € 278.727 null zurechenbare Zeichnungen. Wir haben ihn gestoppt und umgeschichtet.", "assets/img/ag_board1.jpg"),
        ("Anders als üblich", "Ein Kanal sauber statt fünf halb", "Lieber einen Kanal ausreizen und beweisen, als Budget über fünf Kanäle verdampfen lassen.", "assets/img/ag_talk.jpg")],
  zoom=dict(img="assets/img/funkhaus.jpg", side="right", aside="Das stärkste Creative ist der größte Hebel, nicht das größte Budget.",
            zl="Premium-Neubau, Wien · Instant Forms", zt="489 Leads zu € 11,77. Ein Motiv trug 54 %."),
  proof_h=["€ 4,72 pro Lead.", "Der effizienteste im Portfolio."],
  proof_nums=[("5,87×", "Ø ROAS über alle Accounts"), ("€ 4,72", "CPL, Bauträger-Portfolio Wien"), ("489", "Leads, Premium-Neubau Wien")],
  proof_quote="Konstanz über Regionen und Projekte zeigt: Das Motiv trägt, nicht der Zufall. Niedrige CPL kommt aus Disziplin, nicht aus Glück.",
  visual=("phones", dict(h="Creatives, die im Feed bestehen.", t="Gebaut für den Daumen: Sujets aus laufenden Kampagnen, getestet gegen echte Benchmarks, nicht gegen Geschmack.",
                          phones=[["assets/img/a_funk2.jpg", "assets/img/a_otta1.jpg"], ["assets/img/a_gmund1.jpg", "assets/img/a_funk3.jpg"]])),
  logos=["winegg", "funkhaus", "ifa", "conda", "soravia", "rhomberg"],
  oplist=[("case-premium-neubau.html", "Premium-Neubau, Wien", "489", "Leads · € 11,77 CPL"),
          ("case-bautraeger-portfolio.html", "Bauträger-Portfolio, Wien", "€ 4,72", "CPL · der effizienteste im Portfolio"),
          ("case-wohnbau-floridsdorf.html", "Wohnbau, Floridsdorf", "460", "Leads · € 12,77 CPL")],
  faq=[("Unsere Zielgruppe ist zu speziell für Performance.", "Das hören wir oft, auch von Investoren-Funnels und Premium-Neubau. Genau dort entscheidet die Botschaft je Zielgruppe: Bei Anlegern schlug der Service-Angle die Nachhaltigkeits-Story um das 2,3-Fache."),
       ("Woher wissen wir, dass die Zahlen stimmen?", "Server-side Tracking, Blended-Sicht und auf Wunsch der Blick in den Ad-Manager: Wir reporten die Realität, nicht die schönste Zählweise."),
       ("Was passiert, wenn ein Kanal nicht liefert?", "Dann wird er gestoppt, nicht schöngeredet. Ein € 278k-Test ohne zurechenbares Ergebnis flog bei uns aus dem Plan.")],
  offer_h="Der Einstieg ist ein Account-Audit. Kein Vertrag.",
  offer=["Wir prüfen Kampagnenstruktur, Creatives, Tracking und Zurechnung und zeigen Ihnen in zwei Wochen, wo Budget verdampft und wo der ehrliche CPL liegt. Danach entscheiden Sie.",
         "<b>Risikoumkehr inklusive:</b> Wo sich Umsatz messen lässt, koppeln wir unsere Vergütung daran. Basis-Fixum plus Erfolgsbeteiligung, wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Account-Audit", "Meta-Setup", "Google-Setup", "Lead-Kampagne", "Creative-Testing", "Tracking-Setup", "Zweitmeinung", "Skalierung"]),

 dict(slug="service-content-creation", nav="Content Creation", label="Leistung · Content Creation",
  h1=["Content,", "der verkauft."], ital=1,
  tags=["UGC & Studio", "Foto & Film", "Social-Formate", "Creative-System"],
  sub="Foto, Film und UGC, produziert für Performance: gemessen am CPA, nicht am Applaus.",
  problem_h=["Das Problem"],
  problem=["Feeds voller Hochglanz, aber die CPMs steigen und niemand misst, welches Motiv wirklich trägt. Schöner Content, der nichts verkauft, ist Dekoration.",
           "<b>Die Konsequenz: teure Produktionen ohne Wirkung.</b> Jedes Shooting ohne Testing-Plan produziert Material fürs Archiv, während die Kampagne mit dem falschen Motiv weiterläuft."],
  intro="Bei uns sitzen <b>Content und Performance</b> an einem Tisch: Jedes Motiv wird gegen echte <b>Benchmarks</b> getestet, nicht gegen Geschmack. Was trägt, wird skaliert. Was nicht trägt, fliegt raus, egal wie <b>schön</b> es ist.",
  acc=[("UGC-Produktion", "Echte Menschen, echte Nutzung: In einem Health-Mandat schlug UGC die klassischen Produkt-Videos beim CPA um rund 58 Prozent.",
        ["Creator-Casting & Briefing", "Skripte nach Hook-Logik", "Iterationen nach CPA", "Rechte & Freigaben sauber"]),
       ("Studio & On-Location", "Produktwelten, Interiors, Menschen: produziert mit Blick auf den Feed, nicht auf das Portfolio.",
        ["Foto & Film", "Produkt-Stills & Interiors", "Kampagnen-Sujets", "Cinematography"]),
       ("Social-Formate", "Formate, die die Plattform belohnt: schnell, nativ, mit Hook in den ersten Sekunden.",
        ["Reels & Stories", "Statics & Collagen", "Karussells & Grundriss-Formate", "Saisonale Motive je Phase"]),
       ("Creative-System", "Kein Kampagnenfeuerwerk, sondern ein Loop: produzieren, testen, lernen, nachproduzieren.",
        ["Testing-Loop mit Performance", "Winner-Selektion nach Zahlen", "Motiv-Bibliothek je Marke", "Monatliche Nachproduktion"])],
  diff=[("Anders als üblich", "Gemessen statt gemeint", "Interior-Motive trugen bei einem Neubauprojekt 54 Prozent aller Leads. Solche Antworten liefert Testing, kein Bauchgefühl.", "assets/img/a_funk1.jpg"),
        ("Anders als üblich", "Content + Performance, ein Team", "Die Produktion kennt die Zahlen von gestern, die Kampagne bekommt Nachschub, bevor das Motiv müde wird.", "assets/img/ag_cam1.jpg"),
        ("Anders als üblich", "UGC ernst genommen", "UGC ist bei uns keine Billig-Alternative, sondern der oft effizienteste Hebel: minus 58 Prozent CPA gegen Studio-Video.", "assets/img/ag_shoot1.jpg")],
  zoom=dict(img="assets/img/c_food1.jpg", side="left", aside="Produziert für den Feed: Content, der gemessen wird, nicht nur gefällt.",
            zl="Content-Produktion · Food", zt="Jedes Motiv tritt gegen Benchmarks an."),
  proof_h=["Ein Motiv trug", "54 % aller Leads."],
  proof_nums=[("54 %", "aller Leads aus einem Interior-Motiv"), ("−58 %", "CPA durch UGC statt Studio-Video"), ("€ 0,99", "Awareness-CPM, 72 % unter Benchmark")],
  proof_quote="Der größte Hebel war das Creative, nicht das Budget. Das gilt in Commerce, Real Estate und Health gleichermaßen.",
  visual=("phones", dict(h="Gebaut für den Daumen.", t="Sujets aus laufenden Mandaten: Gastro, Event, Immobilie, Produkt. Immer mit Hook, immer messbar.",
                          phones=[["assets/img/c_champ.jpg", "assets/img/c_club.jpg"], ["assets/img/a_silv1.jpg", "assets/img/c_car.jpg"]])),
  logos=["isi", "looops", "juwel", "nordicspirit", "jti", "ilbosso"],
  oplist=[("case-health-brand.html", "Dental-/Health-Marke", "−58 %", "CPA durch UGC"),
          ("case-premium-neubau.html", "Premium-Neubau, Wien", "54 %", "aller Leads aus einem Motiv"),
          ("case-d2c-lifestyle.html", "D2C-Lifestyle-Marke", "+57 %", "Jahresumsatz · UGC schlug Studio")],
  faq=[("Wir haben schon einen Fotografen.", "Gut so, den ersetzen wir nicht zwingend. Wir ergänzen das System dahinter: Hooks, Testing, Winner-Selektion. Content ohne Messung bleibt Dekoration."),
       ("Ist UGC nicht billig fürs Markenbild?", "Falsch produziert: ja. Richtig produziert wirkt UGC glaubwürdiger als Hochglanz und senkte den CPA in unserem Health-Mandat um rund 58 Prozent."),
       ("Wie viel Content brauchen wir wirklich?", "Weniger, als Sie denken, aber öfter: Ein monatlicher Nachproduktions-Loop schlägt das eine große Shooting pro Jahr.")],
  offer_h="Der Einstieg ist ein Creative-Audit. Kein Vertrag.",
  offer=["Wir analysieren Ihre laufenden Motive gegen Benchmarks und zeigen Ihnen, welche Creatives Geld verdienen, welche Geld verbrennen und was als Nächstes produziert gehört.",
         "<b>Risikoumkehr:</b> Läuft die Produktion mit Performance-Mandat, koppeln wir die Vergütung an messbare Ergebnisse. Wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Creative-Audit", "UGC-Produktion", "Studio-Shooting", "Reels & Social", "Kampagnen-Sujets", "Testing-Loop", "Zweitmeinung", "Content-Partnerschaft"]),

 dict(slug="service-websites", nav="Websites & Landingpages", label="Leistung · Websites & Landingpages",
  h1=["Seiten, die", "abschließen."], ital=1,
  tags=["Landingpages", "Shops & Websites", "Konfiguratoren", "CRO & A/B-Tests"],
  sub="Landingpages, Shops und interaktive Lead-Magnete: gebaut auf Conversion, gemessen am Abschluss.",
  problem_h=["Das Problem"],
  problem=["Teure Klicks landen auf Seiten, die nicht konvertieren: langsam, überladen, ohne klares Nutzenversprechen über dem Falz und ohne Message-Match zur Anzeige.",
           "<b>Jeder Euro Mediabudget wird dadurch entwertet.</b> Wer € 3 pro Klick zahlt und 1 Prozent konvertiert, zahlt € 300 pro Lead, und wundert sich über den Markt."],
  intro="Wir bauen Seiten vom <b>Abschluss</b> her: eine Botschaft, ein Ziel, <b>Message-Match</b> zur Kampagne. Und wir messen ehrlich, wann eine Landingpage der richtige Ort ist, und wann ein <b>Instant Form</b> schlicht besser performt.",
  acc=[("Landingpages je Kampagne", "Eine Seite pro Botschaft: Headline, Beweis und CTA passen zur Anzeige, nicht zur Sitemap.",
        ["Message-Match zur Kampagne", "Ein Ziel pro Seite", "Proof an den Entscheidungspunkten", "Noindex, schnell, mobil zuerst"]),
       ("Shops & Websites", "Vom Produkt bis zum Checkout: Auftritte, die Markenwelt und Abschluss verbinden.",
        ["Shop-Systeme & Checkout", "Markenwelten & Kataloge", "Performance & Core Web Vitals", "Content-Pflege ohne Agentur-Zwang"]),
       ("Interaktive Lead-Magnete", "Der Konfigurator ist das beste Creative: Ein PV-Anbieter bekam darüber 406 Leads und 487 Prozent mehr Besucher.",
        ["Konfiguratoren & Rechner", "Mehrstufige Lead-Strecken", "Qualifizierung im Formular", "Übergabe ans CRM"]),
       ("CRO & Testing", "Hypothese, Test, Entscheidung: Conversion-Optimierung als Routine, nicht als Projekt.",
        ["A/B-Tests mit klaren Hypothesen", "Heatmaps & Session-Analysen", "Checkout-Optimierung", "Wöchentliche Iteration"])],
  diff=[("Anders als üblich", "Message-Match statt Sitemap", "Die Landingpage gehört zur Kampagne, nicht zur IT: Headline und Beweis wechseln mit der Anzeigengruppe.", "assets/img/d_funkhaus.jpg"),
        ("Anders als üblich", "Der Lead-Magnet als Creative", "Ein Konfigurator, der den Bedarf rechnet, schlägt jedes Standard-Formular: 406 Leads für einen PV-Anbieter.", "assets/img/ag_vision1.jpg"),
        ("Anders als üblich", "Ehrlicher Kanalvergleich", "Bei einem Neubauprojekt lieferten Instant Forms Leads zu € 6,97, die Website zu € 15,66. Wir sagen auch, wenn die Landingpage nicht der beste Ort ist.", "assets/img/ag_review.jpg")],
  zoom=dict(img="assets/img/d_funkhaus.jpg", side="right", aside="Die Landingpage als Ort für Tiefe: Grundrisse, Vertrauen, Abschluss.",
            zl="Projekt-Landingpage · Premium-Neubau", zt="Landingpage und Instant Forms im Verbund."),
  proof_h=["+487 % Besucher.", "406 Leads."],
  proof_nums=[("406", "Leads über den PV-Konfigurator"), ("+487 %", "Website-Besucher"), ("€ 6,97", "CPL Instant Form im ehrlichen Vergleich")],
  proof_quote="Sichtbarkeit und Conversion-Mechanik gehören zusammen: Search erntet Nachfrage, die schon da ist, die Seite macht sie zur Anfrage.",
  visual=("panels", dict(h="Auftritte aus laufenden Mandaten.", t="Markenwelt, Projekt-Landingpage, Shop: gebaut auf Conversion, gepflegt im Mandat.",
                          imgs=["assets/img/d_funkhaus.jpg", "assets/img/d_isi.jpg", "assets/img/d_noma.jpg", "assets/img/d_ib7.jpg"])),
  logos=["funkhaus", "winegg", "seeresidenz", "vonpoll", "rhomberg", "soravia"],
  oplist=[("case-photovoltaik.html", "Photovoltaik-Anbieter", "+487 %", "Besucher · 406 Leads"),
          ("case-premium-neubau.html", "Premium-Neubau, Wien", "€ 6,97", "CPL Instant Form vs. € 15,66 Website"),
          ("case-immobilien-investment.html", "Immobilien-Investment", "129×", "Funnel bis zur Zeichnung")],
  faq=[("Wir haben schon eine Website.", "Und sie hat einen Job: abschließen. Wenn sie das nicht tut, braucht es selten einen Relaunch, sondern eine Landingpage pro Kampagne und einen sauberen Test-Plan."),
       ("Warum nicht einfach ein Baukasten?", "Für den Start völlig okay. Sobald Mediabudget auf die Seite trifft, entscheiden Ladezeit, Message-Match und Testing, und da rechnet sich Handarbeit schnell."),
       ("Landingpage oder Instant Form?", "Das entscheiden die Zahlen, nicht die Vorliebe: Wir testen beides und schichten dorthin um, wo der ehrliche CPL liegt.")],
  offer_h="Der Einstieg ist ein Seiten-Audit. Kein Vertrag.",
  offer=["Wir prüfen Ladezeit, Message-Match, Formulare und Checkout und zeigen Ihnen in zwei Wochen, wo Ihre Seite Anfragen verliert. Danach entscheiden Sie.",
         "<b>Risikoumkehr:</b> Läuft die Seite im Performance-Mandat, hängt unsere Vergütung an messbaren Ergebnissen. Wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Seiten-Audit", "Landingpage", "Shop-Projekt", "Konfigurator", "CRO & Testing", "Relaunch-Begleitung", "Zweitmeinung", "Betreuung im Mandat"]),

 dict(slug="service-strategie", nav="Strategie & Funnel", label="Leistung · Strategie & Funnel",
  h1=["Struktur schlägt", "Bauchgefühl."], ital=1,
  tags=["Funnel-Architektur", "KPI-Logik", "Attribution", "Positionierung"],
  sub="Vom Einzelprojekt zur Plattform: Funnel, KPI-Logik und Attribution, die Entscheidungen tragen.",
  problem_h=["Das Problem"],
  problem=["Jede Kampagne beginnt bei null: eigene Zielgruppen, eigene Zahlen, keine gemeinsame Datenbasis. Was funktioniert hat, weiß hinterher niemand genau.",
           "<b>Teuer erkaufte Learnings verpuffen.</b> Eine Plattform, die mit ROAS 2,14 lief, blieb genau so lange ineffizient, bis Struktur, KPI-Logik und projektübergreifendes Lernen kamen: Danach stand sie bei 8,75."],
  intro="Wir bauen die <b>Struktur</b>, bevor wir Budget bewegen: <b>Funnel-Architektur</b>, KPI-Definitionen, die vorab feststehen, und eine <b>Attribution</b>, die jeden Euro zurechenbar macht. Erst dann wird skaliert.",
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
        ("Anders als üblich", "Ehrliches Stoppen", "Ein Paid-Test über € 278.727 brachte null Zeichnungen: Er wurde gestoppt, das Budget umgeschichtet. Genau dafür ist Struktur da.", "assets/img/ag_board1.jpg")],
  zoom=dict(img="assets/img/ag_strategy.jpg", side="left", aside="Erst die Struktur, dann das Budget: Strategie-Session in Wien.",
            zl="Strategie & Funnel", zt="€ 36k Budget wurden € 4,65 Mio. Kapital."),
  proof_h=["Aus € 36k wurden", "€ 4,65 Mio. Kapital."],
  proof_nums=[("129×", "Return, sauber zugerechnet"), ("8,75", "ROAS, vorher 2,14"), ("−69 %", "Kosten je Investor")],
  proof_quote="Gleicher Spend, anderes Ergebnis: Der Beweis liegt im Vorher-Nachher. Struktur schlägt Einzelkampagne.",
  visual=("stage", dict(img="assets/img/d_noma.jpg", cap="Aus dem Mandat · Auftritt mit Funnel-Logik")),
  logos=["ifa", "conda", "raiffeisen", "soravia", "fabrik1230", "hagent"],
  oplist=[("case-immobilien-investment.html", "Immobilien-Investment", "129×", "€ 36k → € 4,65 Mio. Kapital"),
          ("case-crowdinvesting.html", "Crowdinvesting-Plattform", "8,75", "ROAS, vorher 2,14"),
          ("case-consumer-brand.html", "Premium-Consumer-Brand", "4,02", "Saison als Architektur")],
  faq=[("Brauchen wir wirklich Strategie, oder einfach bessere Ads?", "Wenn die Struktur steht, reichen oft bessere Ads. Wenn nicht, verbrennt auch das beste Creative Budget: ROAS 2,14 wurde erst durch Struktur zu 8,75."),
       ("Wie lange dauert so etwas?", "Die Strategie-Phase ist in zwei bis vier Wochen durch, danach wird umgesetzt. Strategie ohne Umsetzung verkaufen wir nicht."),
       ("Was, wenn die Analyse zeigt, dass wenig zu holen ist?", "Dann sagen wir das. Eine ehrliche Absage ist billiger als zwölf Monate Mandat ohne Hebel.")],
  offer_h="Der Einstieg ist eine Strategie-Session. Kein Vertrag.",
  offer=["Status quo, Zielbild, KPI-Logik: In einer strukturierten Session zeigen wir, wo Ihr Funnel Kapital liegen lässt und was zuerst gebaut gehört. Danach entscheiden Sie.",
         "<b>Risikoumkehr:</b> Geht die Strategie in ein Umsetzungs-Mandat über, koppeln wir die Vergütung an messbare Ergebnisse. Wir gewinnen nur, wenn Sie gewinnen."],
  chips=["Strategie-Session", "Funnel-Architektur", "KPI-Logik", "Attribution-Setup", "Positionierung", "Portfolio-Struktur", "Zweitmeinung", "Umsetzungs-Mandat"]),
]

def render_service(s):
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
            <div class="pk2">%s · 0%d</div>
            <div class="ht2">%s</div>
            <p>%s</p>
          </div>''' % (k, i + 1, t, p) for i, (k, t, p, img) in enumerate(s["diff"]))
    z = s["zoom"]
    aside_pos = "left:clamp(24px,6vw,110px)" if z["side"] == "right" else "right:clamp(24px,6vw,110px)"
    nums = "\n        ".join('''<div class="n" data-fade><div class="v num serif">%s</div><div class="l">%s</div></div>''' % (v, l) for v, l in s["proof_nums"])
    vkind, vd = s["visual"]
    if vkind == "panels":
        imgs = vd["imgs"]
        col1 = "\n          ".join('<img loading="lazy" decoding="async" src="%s" alt="">' % i for i in imgs[0::2])
        col2 = "\n          ".join('<img loading="lazy" decoding="async" src="%s" alt="">' % i for i in imgs[1::2])
        visual = '''  <!-- PROOF · PANELS (dunkel, Screens scrollen vorbei) -->
  <section class="panelscroll" data-bg="#0A0A0A" data-fg="light">
    <div class="wrap pswrap">
      <div class="pstxt">
        <div class="chlab" data-lines><span class="rl"><span>%s</span></span></div>
        <p class="chtxt" data-fade>%s</p>
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

''' % (vd["h"], vd["t"], col1, col2)
    elif vkind == "phones":
        phs = []
        for pi, imgs in enumerate(vd["phones"]):
            inner = "\n            ".join('<img loading="lazy" decoding="async" src="%s" alt="">' % i for i in imgs)
            phs.append('''<div class="phframe"><div class="phinner" data-drift="0.%d">
            %s
          </div></div>''' % (10 + pi * 8, inner))
        visual = '''  <!-- PROOF · PHONES (hell, Inhalte scrollen im Frame) -->
  <section class="sec fg-light bg-paper phonesec" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap phwrap">
      <div>
        <div class="lchap" style="grid-template-columns:1fr;gap:18px">
          <div class="lh" data-lines><span class="rl"><span>%s</span></span></div>
          <p class="lt3" data-fade>%s</p>
        </div>
      </div>
      <div class="phones">
        %s
      </div>
    </div>
  </section>

''' % (vd["h"], vd["t"], "\n        ".join(phs))
    else:
        visual = '''  <!-- PROOF · STAGE -->
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
    faqs = "\n        ".join('''<div class="qa" data-fade>
          <div class="q">%s</div>
          <div class="a">%s</div>
        </div>''' % (q, a) for q, a in s["faq"])
    chips_sel = "\n        ".join('<button class="nopt" data-v="%s" style="--i:%d">%s <span class="plus">+</span></button>' % (cv, 7 - i, cv) for i, cv in enumerate(s["chips"]))
    logos = logocycle(s["logos"])

    page = HEAD.format(title=s["nav"], bodybg="#F3EDE1") + menu("index.html#leistungen") + '''<main>

  <!-- 01 · HERO -->
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
    </div>
  </section>

  <!-- 03 · LÖSUNG: INTRO + AKKORDEON -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(30px,4vw,60px)">
    <div class="wrap svc-split">
      <div class="intro">
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:20px">Die Lösung</span>
        <p class="serif" data-scrub>''' + s["intro"] + '''</p>
      </div>
      <div class="acc">
        ''' + acc + '''
      </div>
    </div>
  </section>

  <!-- 04 · WAS WIR ANDERS MACHEN (BiA-Split: links sticky, rechts Text) -->
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

  <!-- 05 · PROOF 1: ZOOM -->
  <section class="zoomsec" data-side="''' + z["side"] + '''" data-bg="#F3EDE1" data-fg="dark">
    <div class="zsticky">
      <div class="zaside fg-light" style="''' + aside_pos + '''">
        <span class="label" style="color:var(--champ-deep)">Der Beweis</span>
        <p class="serif" style="font-size:clamp(19px,1.7vw,26px);color:var(--ink)">''' + z["aside"] + '''</p>
      </div>
      <div class="zmedia"><img src="''' + z["img"] + '''" alt=""></div>
      <div class="zcap">
        <span class="zl">''' + z["zl"] + '''</span>
        <div class="zt">''' + z["zt"] + '''</div>
      </div>
    </div>
  </section>

  <!-- 06 · PROOF 2: ERGEBNISSE -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap" style="max-width:1100px">
      <span class="label" style="color:var(--champ-deep);display:block;text-align:center">Ergebnisse</span>
      <h2 class="serif" data-lines style="font-size:clamp(34px,4.4vw,72px);text-align:center;margin-top:22px">
        <span class="rl"><span>''' + s["proof_h"][0] + '''</span></span>
        <span class="rl"><span><i style="font-style:italic">''' + s["proof_h"][1] + '''</i></span></span>
      </h2>
      <div class="wnums" data-stagger style="justify-content:center;margin-top:clamp(30px,4vw,50px)">
        ''' + nums + '''
      </div>
      <p class="serif" data-fade style="font-size:clamp(17px,1.4vw,21px);color:var(--grey-dark);max-width:52ch;margin:clamp(30px,4vw,46px) auto 0;text-align:center">''' + s["proof_quote"] + '''</p>
    </div>
  </section>

''' + visual + '''  <!-- LOGOS -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: clamp(40px,5vw,64px) 0">
    <div class="wrap" style="display:flex;align-items:center;gap:clamp(28px,4vw,64px);flex-wrap:wrap;border-top:1px solid var(--line-l);border-bottom:1px solid var(--line-l);padding-top:34px;padding-bottom:34px">
      <span class="label" style="color:var(--grey-dark)">Marken, die bleiben</span>
      <div class="logocycle" style="flex:1">
      ''' + logos + '''
      </div>
    </div>
  </section>

  <!-- 07 · CASES -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(60px,7vw,100px)">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(28px,3.4vw,48px)">Ausgewählte Ergebnisse</span>
      <div class="oplist" data-stagger>
        ''' + ops + '''
      </div>
    </div>
  </section>

  <!-- 08 · FAQ -->
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

  <!-- 09 · NO-BRAINER + RISIKOUMKEHR -->
  <section class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Das Angebot</span>
        <div class="lh" data-lines><span class="rl"><span>''' + s["offer_h"] + '''</span></span></div>
      </div>
      <div data-stagger>
        <p class="lt3" data-fade>''' + s["offer"][0] + '''</p>
        <p class="lt3" data-fade>''' + s["offer"][1] + '''</p>
      </div>
    </div>
  </section>

  <!-- 10 · CTA: ANFRAGE-MECHANIK -->
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
      <p data-fade style="font-size:13px;color:var(--grey-dark);margin-top:26px">Auswahl treffen, weiter klicken, und Ihre Anfrage ist vorformuliert. Antwort in unter 24 Stunden.</p>
    </div>
  </section>

''' + FOOTER
    return page

for s in SERVICES:
    open(s["slug"] + ".html", "w", encoding="utf-8").write(render_service(s))
    print("service", s["slug"])
print("services done")

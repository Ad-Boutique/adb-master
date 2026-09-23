# -*- coding: utf-8 -*-
"""KPI-Board "Auf einen Blick": ein Baustein fuer Cases, Web-Cases, handgebaute Seiten und Leistungen.

Drei Kartentypen, eine Grammatik (Label, grosse Zahl in Amandine, Lime-Pille, Punkt-Grafik, Satz):
  jump   Zahlen-Sprung: vorher durchgestrichen, nachher zaehlt hoch, Delta in der Pille
  count  Produktion oder Volumen: eine Zahl zaehlt von null, jeder Punkt eine Einheit
  text   Qualitatives Ergebnis: kurzer Satz in Amandine, optional Stationen als Punktzeile
  quote  Kundenstimme als Ergebnis
  media  Die Arbeit selbst: drei Ausschnitte aus dem Projekt

Grafiken je Karte: line (Werte), rows (Punktreihen: Label, n, an, hervorgehoben), waffle (total, wert, spalten),
stations (Punktzeile), imgs (Streifen). Nur Zahlen, die auf der Seite oder im Reporting stehen.
Alle Punkt-Grafiken fuellen sich beim Ankommen (brand.js: .kpi, .dotgraph, .dotbars, .dotline)."""
import os

HTML_ARROW = '<span class="karrow" aria-hidden="true">&rarr;</span>'


def _q(s):
    return s.replace('"', "&quot;")


def card(c):
    kind = c.get("kind", "jump")
    # Kopfzeile: Label links, Pille rechts, beides im Fluss, damit lange Labels nicht unter die Pille laufen
    pill = ('<span class="kpill">%s</span>' % c["pill"]) if c.get("pill") else ""
    out = ['        <div class="kpi kpi--%s" data-fade>' % kind,
           '          <div class="khead"><span class="kl">%s</span>%s</div>' % (c["l"], pill)]
    if kind == "quote":
        out.append('          <p class="kquote">&bdquo;%s&ldquo;</p>' % c["q"])
        out.append('          <span class="kqa">%s</span>' % c["a"])
    else:
        vals = []
        if c.get("frm"):
            vals.append('<span class="kfrom">%s</span>%s' % (c["frm"], HTML_ARROW))
        attrs = ""
        cnt = c.get("cnt")
        if cnt:
            frm_v, to_v, dec = cnt[0], cnt[1], cnt[2]
            pre = cnt[3] if len(cnt) > 3 else ""
            suf = cnt[4] if len(cnt) > 4 else ""
            attrs = ' data-from="%s" data-to="%s" data-decimals="%d" data-prefix="%s" data-suffix="%s"' % (frm_v, to_v, dec, _q(pre), _q(suf))
        cls = "kto kto--txt" if kind in ("text", "media") else "kto"
        vals.append('<span class="%s"%s>%s</span>' % (cls, attrs, c["to"]))
        if c.get("unit"):
            vals.append('<span class="kunit">%s</span>' % c["unit"])
        out.append('          <div class="kvals">%s</div>' % "".join(vals))
    if c.get("line"):
        out.append('          <svg class="kline" viewBox="0 0 260 90" data-points="%s" aria-hidden="true"></svg>'
                   % ",".join(str(v) for v in c["line"]))
    if c.get("rows"):
        out.append('          <div class="kdots" aria-hidden="true">')
        for label, n, on, hi in c["rows"]:
            out.append('            <div class="row%s"><span class="rl">%s</span><span class="dots" data-n="%d" data-on="%d"></span></div>'
                       % (" hi" if hi else "", label, n, on))
        out.append('          </div>')
    if c.get("waffle"):
        total, value, cols = c["waffle"]
        out.append('          <div class="dotgraph kwaffle" data-total="%d" data-value="%d" style="--cols:%d" aria-hidden="true"></div>' % (total, value, cols))
    if c.get("stations"):
        out.append('          <div class="dotline kst" aria-hidden="true">%s</div>' % "".join("<span>%s</span>" % s for s in c["stations"]))
    if c.get("imgs"):
        imgs = [i for i in c["imgs"] if os.path.exists(i)][:3]
        if imgs:
            out.append('          <div class="kstrip">%s</div>' % "".join('<img loading="lazy" decoding="async" src="%s" alt="">' % i for i in imgs))
    if c.get("cap"):
        out.append('          <p class="kcap">%s</p>' % c["cap"])
    if c.get("link"):
        out.append('          <a class="zalink klink" href="%s">%s</a>' % c["link"])
    out.append('        </div>')
    return "\n".join(out)


def board(b, bg="paper", sec_id=None, style=None):
    """Sektion mit Label, Headline (zweite Zeile kursiv) und drei Karten."""
    label = b.get("label", "Auf einen Blick")
    h0, h1 = b.get("h", ("Was besser wurde,", "in drei Zahlen."))
    bgc = "#EFE7D6" if bg == "cream" else "#F3EDE1"
    note = ('      <p class="cfoot-note knote" data-fade>%s</p>\n' % b["note"]) if b.get("note") else ""
    st = style if style is not None else "padding-top:clamp(60px,7vw,110px);padding-bottom:clamp(50px,6vw,90px)"
    idattr = (' id="%s"' % sec_id) if sec_id else ""
    return ('  <!-- AUF EINEN BLICK: drei Karten, vorher, nachher, der Sprung in Lime -->\n'
            '  <section%s class="sec fg-light bg-%s kpisec" data-bg="%s" data-fg="dark" style="%s">\n'
            '    <div class="wrap">\n'
            '      <div class="kpihead">\n'
            '        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">%s</span>\n'
            '        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)"><span class="rl"><span>%s</span></span><span class="rl"><span><i>%s</i></span></span></h2>\n'
            '      </div>\n'
            '      <div class="kpiboard" data-stagger>\n%s\n      </div>\n'
            '%s'
            '    </div>\n'
            '  </section>\n\n') % (idattr, bg, bgc, st, label, h0, h1, "\n".join(card(c) for c in b["cards"]), note)


def mini(nums, note=None):
    """Kleine Zahlenkarten fuer Kapitel: dieselbe Grammatik wie das Board, ohne Grafik."""
    cards = "\n".join('        <div class="kpi kpi--mini" data-fade><span class="kl">%s</span><div class="kvals"><span class="kto">%s</span></div></div>'
                      % (l.strip("()"), v) for l, v in nums)
    out = '      <div class="kpiboard kpiboard--mini" data-stagger>\n%s\n      </div>\n' % cards
    if note:
        out += '      <p class="cfoot-note knote" data-fade>%s</p>\n' % note
    return out


def dotrows(rows, per=25):
    """Balken in Punktreihen: (Name, Prozent, Wert) -> 25 Punkte, der Bestwert Lime."""
    hi = max(range(len(rows)), key=lambda i: rows[i][1])
    out = ['        <div class="dotbars dotbars--ch" data-fade>']
    for i, (name, pct, val) in enumerate(rows):
        on = max(1, int(round(pct / 100.0 * per)))
        out.append('          <div class="row%s"><span class="rl">%s</span><span class="dots" data-n="%d" data-on="%d"></span><span class="rv">%s</span></div>'
                   % (" hi" if i == hi else "", name, per, on, val))
    out.append('        </div>')
    return "\n".join(out)


def L(c, href, text="Case ansehen"):
    d = dict(c)
    d["link"] = (href, text)
    return d


def web_imgs(key):
    cand = ["assets/img/web_%s_ds0.jpg", "assets/img/web_%s_d1.jpg", "assets/img/web_%s_ds1.jpg", "assets/img/web_%s_m0.jpg", "assets/img/web_%s_d2.jpg"]
    return [p % key for p in cand]


# ---------------------------------------------------------------- Karten, die mehrfach gebraucht werden
FUNKHAUS_CPL = dict(kind="jump", l="Preis je Anfrage", frm="€ 11,77", to="€ 5,00", cnt=(11.77, 5.00, 2, "€ ", ""), pill="−57 %",
                    line=[11.77, 6.97, 5.88, 5.00, 4.99, 5.78],
                    cap="Vom Schnitt der ersten Kampagne zur ersten Welle. Dazwischen: Instant Form € 6,97, Februar € 5,88, danach € 4,99 und € 5,78.")
FUNKHAUS_STRECKE = dict(kind="jump", l="Strecke zur Anfrage", frm="€ 15,66", to="€ 6,97", cnt=(15.66, 6.97, 2, "€ ", ""), pill="−55 %",
                        rows=[("Website", 32, 31, False), ("Instant Form", 32, 14, True)],
                        cap="Dieselbe Kampagne, zwei Wege zur Anfrage. Das Formular im Feed kostet weniger als die Hälfte. Ein Punkt sind 50 Cent.")
FUNKHAUS_MOTIV = dict(kind="jump", l="Anteil des stärksten Motivs", frm="4 Motive", to="262 von 489", cnt=(0, 262, 0, "", " von 489"), pill="54 %",
                      waffle=(100, 54, 20),
                      cap="Ein einziges Interior-Motiv trug mehr als die Hälfte aller Anfragen. Jeder Punkt ein Prozent.")

D2C_UMSATZ = dict(kind="jump", l="Jahresumsatz", frm="€ 520k", to="€ 817k", cnt=(520, 817, 0, "€ ", "k"), pill="+57 %",
                  rows=[("Vorher", 82, 52, False), ("Mit uns", 82, 82, True)],
                  cap="Aus demselben Traffic, anders geführt. Ein Punkt sind 10.000 Euro.")
D2C_ROAS = dict(kind="jump", l="Blended ROAS", frm="Ziel 3,5", to="5,57", cnt=(3.5, 5.57, 2, "", ""), pill="+59 % über Ziel",
                rows=[("Pinterest", 70, 70, True), ("Google", 70, 60, False), ("Blend inkl. Fee", 70, 42, False)],
                cap="Pinterest 6,99, Google 5,98, inklusive Agentur-Fee 4,17. Ein Punkt sind 0,1 ROAS.")
D2C_BUDGET = dict(kind="jump", l="Umsatz aus dem Mediabudget", frm="€ 56k Budget", to="€ 312k", cnt=(56, 312, 0, "€ ", "k"), pill="Faktor 5,6",
                  rows=[("Mediabudget", 31, 6, False), ("Umsatz", 31, 31, True)],
                  cap="Meta für Nachfrage, Google für Abverkauf, Pinterest als Effizienz-Kanal. Ein Punkt sind 10.000 Euro.")

CONSUMER_ROAS = dict(kind="jump", l="ROAS am Black Friday", frm="Benchmark 2,3", to="4,02", cnt=(2.3, 4.02, 2, "", ""), pill="+75 %",
                     rows=[("Benchmark", 40, 23, False), ("Mit uns", 40, 40, True)],
                     cap="Der Account-Benchmark gegen die lauteste Woche des Jahres. Ein Punkt sind 0,1 ROAS.")
CONSUMER_CPM = dict(kind="jump", l="Awareness-CPM im Vorlauf", frm="€ 3,50", to="€ 0,99", cnt=(3.5, 0.99, 2, "€ ", ""), pill="−72 %",
                    rows=[("Benchmark", 35, 35, False), ("Mit uns", 35, 10, True)],
                    cap="Preis je tausend Kontakte. Günstige Awareness im Vorlauf macht den Peak profitabel. Ein Punkt sind 10 Cent.")

CROWD_KAPITAL = dict(kind="jump", l="Kapital je POC-Phase", frm="€ 43.740", to="€ 172.117", cnt=(43740, 172117, 0, "€ ", ""), pill="+293 %",
                     rows=[("Vorher", 34, 9, False), ("Mit uns", 34, 34, True)],
                     cap="Nahezu gleiches Budget, andere Struktur. Ein Punkt sind 5.000 Euro.")
CROWD_ROAS = dict(kind="jump", l="Return on Ad Spend", frm="2,14", to="8,75", cnt=(2.14, 8.75, 2, "", ""), pill="+309 %",
                  line=[2.14, 8.75, 18.7],
                  cap="Vorher, erste POC-Phase, zweite POC-Phase mit Plattform-Logik: 18,7 bei mehr als verdreifachtem Budget.")
CROWD_INVESTOR = dict(kind="jump", l="Kosten je Investor", frm="€ 1.277", to="€ 393", cnt=(1277, 393, 0, "€ ", ""), pill="−69 %",
                      rows=[("Vorher", 26, 26, False), ("Mit uns", 26, 8, True)],
                      cap="Aus 16 Investments wurden 50, bei nahezu gleichem Spend. Ein Punkt sind 50 Euro.")

FLORIDSDORF_STRECKE = dict(kind="jump", l="Preis je Anfrage, Eigennutzer", frm="€ 58,05 Website", to="€ 9,59", cnt=(58.05, 9.59, 2, "€ ", ""), pill="Faktor 6",
                           rows=[("Website-Formular", 58, 58, False), ("Instant Form", 58, 10, True)],
                           cap="Dieselbe Zielgruppe, zwei Wege zur Anfrage. Ein Punkt ist ein Euro.")

HEALTH_CREATOR = dict(kind="jump", l="Preis je Kauf", frm="€ 215 Produktvideo", to="€ 82", cnt=(215, 82, 0, "€ ", ""), unit="Creator", pill="Faktor 2,6",
                      rows=[("Produktvideo", 22, 22, False), ("Creator", 22, 8, True)],
                      cap="Der Creator schlug das Produktvideo beim Preis je Kauf um mehr als die Hälfte. Ein Punkt sind 10 Euro.")

NORDIC_ORDERS = dict(kind="jump", l="Bestellungen je Monat", frm="800", to="7.800", cnt=(800, 7800, 0, "", ""), pill="Faktor 9,75",
                     rows=[("Vorher", 39, 4, False), ("Am Peak", 39, 39, True)],
                     cap="Eine neue Marke in einer regulierten Kategorie, gewonnen über das Angebot. Ein Punkt sind 200 Bestellungen.")

INVEST_129 = dict(kind="jump", l="Aus Budget wird Kapital", frm="€ 36.043", to="€ 4,65 Mio.", cnt=(0, 4.65, 2, "€ ", " Mio."), pill="129×",
                  rows=[("Google-Budget", 1, 1, False), ("Zurechenbares Kapital", 129, 129, True)],
                  cap="Jeder Punkt ist einmal das eingesetzte Google-Budget: 129 Mal.")

NOMA_VERKAUFT = dict(kind="jump", l="Wohnungen verkauft", frm="26 Wohnungen", to="13 von 26", cnt=(0, 13, 0, "", " von 26"), pill="50 %",
                     waffle=(26, 13, 13),
                     cap="Ein halbes Jahr nach Go-live. Jeder Punkt eine Wohnung.")
HAVENSTONE_WOCHEN = dict(kind="text", l="Vom Briefing bis Go-live", to="Vier Wochen.", pill="4 Partner, eine Meinung",
                         stations=["Briefing", "5 Bildstile", "Header-Film", "Freigabe", "Live"],
                         cap="Nicht diskutiert, sondern gezeigt: fünf Bildstile zur Auswahl, ein Bewegtbild im Header, wenige Worte.")
PV_BESUCHER = dict(kind="jump", l="Website-Besucher, indexiert", frm="100", to="587", cnt=(100, 587, 0, "", ""), pill="+487 %",
                   rows=[("Vorher", 59, 10, False), ("Mit uns", 59, 59, True)],
                   cap="Google Search auf kaufnahe Suchbegriffe, der Konfigurator als Lead-Magnet. Ein Punkt sind zehn Indexpunkte.")
KK_CLIPS = dict(kind="count", l="Social Clips 2026", to="19", cnt=(0, 19, 0, "", ""), pill="3 Drehtage",
                rows=[("Social Clips", 19, 19, True), ("Recap, Doku, Intro", 3, 3, False)],
                cap="Jeder Punkt ein Film: 19 Clips im Hoch- und Querformat, ein Recap in zweieinhalb Minuten, eine zwölfminütige Dokumentation, ein Introfilm.")

# ---------------------------------------------------------------- Cases aus _gen.py
H_NUM = ("Was besser wurde,", "in drei Zahlen.")
H_PROD = ("Was entstanden ist,", "in drei Zahlen.")
H_QUAL = ("Was das Projekt ausmacht,", "in drei Punkten.")

CASE_KPI = {
 "case-immobilien-investment": dict(h=H_NUM, cards=[
    INVEST_129,
    dict(kind="count", l="Online-Anteil der Anfragen 2024", to="80 %", cnt=(0, 80, 0, "", " %"), pill="−19 % je Anfrage", waffle=(100, 80, 20),
         cap="Vier von fünf Anfragen kamen 2024 online, der Preis je Online-Anfrage sank gegenüber 2023 um 19 Prozent. Jeder Punkt ein Prozent."),
    dict(kind="jump", l="Vom Lead zur Zeichnung", frm="446 Leads", to="43", cnt=(0, 43, 0, "", ""), unit="Zeichnungen", pill="€ 3.004 je Investor", waffle=(100, 10, 20),
         cap="Rund jeder zehnte Lead im Funnel zeichnet. Jeder Punkt ein Prozent der Leads.")]),
 "case-d2c-lifestyle": dict(h=H_NUM, cards=[D2C_UMSATZ, D2C_ROAS, D2C_BUDGET]),
 "case-crowdinvesting": dict(h=H_NUM, cards=[CROWD_KAPITAL, CROWD_ROAS, CROWD_INVESTOR]),
 "case-wohnbau-floridsdorf": dict(h=H_NUM, cards=[
    FLORIDSDORF_STRECKE,
    dict(kind="count", l="Anfragen im ersten Quartal", to="460", cnt=(0, 460, 0, "", ""), pill="€ 12,77 je Anfrage",
         rows=[("Eigennutzer", 43, 43, True), ("Anleger", 43, 4, False)],
         cap="425 Eigennutzer, 35 Anleger, aus 5.874 Euro Spend. Ein Punkt sind zehn Anfragen."),
    dict(kind="jump", l="Gezählt gegen angekommen", frm="18 laut Meta", to="8", cnt=(18, 8, 0, "", ""), unit="im Postfach", pill="die wichtigste Zahl",
         rows=[("Meta zählte", 18, 18, False), ("Im Postfach", 18, 8, True)],
         cap="Drei Wochen im zweiten Quartal. Die Differenz klären wir, bevor wir optimieren. Jeder Punkt eine Anfrage.")]),
 "case-consumer-brand": dict(h=H_NUM, cards=[
    CONSUMER_ROAS, CONSUMER_CPM,
    dict(kind="media", l="Die Seite dahinter", to="Drei Sprachen, vier Termine.", pill="3 Länder",
         imgs=["assets/img/web_twistnsparkle_m0.jpg", "assets/img/web_twistnsparkle_m1.jpg", "assets/img/web_twistnsparkle_m2.jpg"],
         cap="Die Kampagnen-Site trägt die Saison und den Produktlaunch, gebaut gegen die Zeit.", link=("case-web-twistnsparkle.html", "Die Seite im Detail"))]),
 "case-bautraeger-portfolio": dict(h=H_NUM, cards=[
    dict(kind="count", l="Preis je Anfrage, drei Projekte", to="€ 4,72", cnt=(0, 4.72, 2, "€ ", ""), pill="3 Projekte",
         rows=[("7. Bezirk", 63, 47, True), ("Projekt A", 63, 63, False), ("Projekt B", 63, 59, False)],
         cap="€ 4,72, € 6,33 und € 5,93, dieselbe Mechanik in jedem Projekt. Ein Punkt sind 10 Cent."),
    dict(kind="count", l="Anfragen im zweiten Quartal", to="546", cnt=(0, 546, 0, "", ""), pill="€ 3.352 Spend",
         rows=[("Projekt A", 29, 29, False), ("Projekt B", 29, 26, True)],
         cap="287 und 259 Anfragen aus zwei Projekten parallel. Ein Punkt sind zehn Anfragen."),
    dict(kind="jump", l="Ein Sujet trägt", frm="wenige Sujets im Test", to="98 von 109", cnt=(0, 98, 0, "", " von 109"), pill="90 %", waffle=(100, 90, 20),
         cap="Im 7. Bezirk brachte das Winner-Creative 98 der 109 Anfragen. Jeder Punkt ein Prozent.")]),
 "case-health-brand": dict(h=H_NUM, cards=[
    HEALTH_CREATOR,
    dict(kind="jump", l="Blended ROAS", frm="Ziel 1,50", to="1,07", cnt=(0, 1.07, 2, "", ""), pill="Ziel-Gap offen",
         rows=[("Ziel", 15, 15, True), ("Erreicht", 15, 11, False)],
         cap="Steht so im Report. Die Stufen dorthin: 1,4, 1,6, über 1,8, jede mit Hebel und Datum. Ein Punkt sind 0,1 ROAS."),
    dict(kind="count", l="Verkäufe in sieben Monaten", to="1.385", cnt=(0, 1385, 0, "", ""), pill="€ 200,5k gesteuert",
         rows=[("Verkäufe", 28, 28, True)],
         cap="Ein Punkt sind 50 Verkäufe. Retargeting blieb mit € 60 je Kauf der effizienteste Euro.")]),
 "case-photovoltaik": dict(h=H_NUM, cards=[
    PV_BESUCHER,
    dict(kind="count", l="Anfragen", to="406", cnt=(0, 406, 0, "", ""), pill="€ 30,83 je Anfrage",
         rows=[("Anfragen", 41, 41, True)],
         cap="Aus Google Search auf kaufnahe Suchbegriffe. Ein Punkt sind zehn Anfragen."),
    dict(kind="text", l="Der Lead-Magnet", to="Der Konfigurator ist das Creative.", pill="2 Minuten",
         stations=["Suche", "Konfigurator", "Bedarf", "Anfrage"],
         cap="Der Besucher rechnet seinen Bedarf und wird dabei zur Anfrage.")]),
 "case-seeresidenz": dict(h=H_NUM, cards=[
    dict(kind="jump", l="Preis je Anfrage, Projektgruppe", frm="€ 405", to="€ 48", cnt=(405, 48, 0, "€ ", ""), pill="−88 %",
         rows=[("Vorher", 41, 41, False), ("Ein Jahr später", 41, 5, True)],
         cap="Über sechs Projekte der Gruppe, innerhalb eines Jahres. Ein Punkt sind 10 Euro."),
    dict(kind="jump", l="Online-Anteil der Anfragen", frm="rund die Hälfte", to="100 %", cnt=(50, 100, 0, "", " %"), pill="+50 Punkte",
         rows=[("Vorher", 50, 25, False), ("Ende 2024", 50, 50, True)],
         cap="Die Kennzahl, an der man eine Gruppe steuert. Ein Punkt sind zwei Prozent."),
    dict(kind="count", l="Anfragen für das Seeprojekt", to="1.761", cnt=(0, 1761, 0, "", ""), pill="18 Monate",
         rows=[("Anfragen", 35, 35, True)],
         cap="Meta erzeugt die Nachfrage, Google erntet sie. 2024 rund 8 Euro je Anfrage. Ein Punkt sind 50 Anfragen.")]),
 "case-nordic-spirit": dict(h=H_NUM, cards=[
    NORDIC_ORDERS,
    dict(kind="jump", l="Preis je Abschluss, Meta", frm="€ 13,01", to="€ 8,36", cnt=(13.01, 8.36, 2, "€ ", ""), pill="−36 %",
         rows=[("Meta vorher", 26, 26, False), ("Meta danach", 26, 17, True), ("Google", 26, 14, False)],
         cap="Google lag bei € 7,18, Search always-on bei € 4,80. Ein Punkt sind 50 Cent."),
    dict(kind="count", l="Abschlüsse in zwölf Monaten", to="23.579", cnt=(0, 23579, 0, "", ""), pill="€ 11,70 je Abschluss", waffle=(100, 73, 20),
         cap="73 Prozent des Budgets liefen auf Meta für Volumen, 27 auf Google für Effizienz. Jeder Punkt ein Prozent Budget.")]),
 "case-medcenter": dict(h=H_QUAL, cards=[
    dict(kind="text", l="Vom Briefing zum Start", to="Sichtbar in einer Woche.", pill="1 Woche",
         stations=["Briefing", "Website", "Google", "Meta", "Live"],
         cap="Website und Kampagnen-Setup standen innerhalb einer Woche, ohne Agenturaufwand, der eine Ordination überfordert."),
    dict(kind="media", l="Sujets fürs Grätzel", to="Menschen statt Geräte.", pill="2 Kanäle",
         imgs=["assets/case/medcenter/g0.jpg", "assets/case/medcenter/g1.jpg", "assets/case/medcenter/g2.jpg"],
         cap="Ruhige Statics in der Farbwelt des Zentrums, gebaut für den Feed. Google für die Suche, Meta für die Nachbarschaft."),
    dict(kind="quote", l="Nach der ersten Abnahme", q="Die Seite sieht echt schon sehr gut aus.", a="Marketing-Koordination, MedCenter 1030",
         cap="Zahlen lesen wir vierteljährlich mit der Praxisleitung. Hier stehen sie, wenn sie belastbar sind.")]),
 "case-juwel": dict(h=H_PROD, cards=[
    dict(kind="count", l="Beiträge und Stories im Monat", to="12", cnt=(0, 12, 0, "", ""), pill="Content-Tag alle 2 Monate",
         rows=[("Beiträge im Monat", 12, 12, True)],
         cap="Jeder Punkt ein Beitrag. Dazu Community-Management als verlängertes Team der Location."),
    dict(kind="media", l="Editorial statt Eventfoto", to="Eine Location wie eine Marke.", pill="4 Kanäle",
         imgs=["assets/img/a_silv1.jpg", "assets/case/juwel/g0.jpg", "assets/img/a_silv2.jpg"],
         cap="Shooting mit Models, damit die Location wie eine Marke aussieht. Instagram, Meta, Google, LinkedIn."),
    dict(kind="quote", l="Zum Vergütungsmodell", q="Passt perfekt!", a="Geschäftsführung, Juwel Wien",
         cap="Erfolgsbeteiligung statt Fixhonorar, gestaffelt nach Eventwert. Wir verdienen, wenn gebucht wird.")]),
 "case-bella-vita": dict(h=H_QUAL, cards=[
    dict(kind="count", l="Anfragen in der ersten Woche", to="21", cnt=(0, 21, 0, "", ""), pill="3 Wochen Setup",
         rows=[("Erste Woche", 57, 21, True), ("Bis Mitte Juli", 57, 57, False)],
         cap="Jeder Punkt eine Anfrage. Preis je Anfrage und Verkäufe folgen, sobald das Quartal geschlossen ist."),
    dict(kind="text", l="Wer anfragt", to="€ 280.000 bis 450.000", pill="3 bis 4 Zimmer",
         cap="Überwiegend Eigennutzer aus der Region, Zeithorizont sechs bis zwölf Monate. Fertig, besichtigbar, sofort beziehbar."),
    dict(kind="text", l="Vom Lead zum Makler", to="Der Lead ist erst beim Makler ein Lead.", pill="2 Maklerhäuser",
         stations=["Anfrage", "Makler", "Rückmeldung", "Kampagne lernt"],
         cap="Jede Anfrage geht automatisch an eines der beiden Maklerhäuser, jede Rückmeldung kommt zurück zu uns.")]),
}

# ---------------------------------------------------------------- Web-Cases aus _gen_web.py
WEB_KPI = {
 "case-web-noma": dict(h=H_NUM, cards=[
    NOMA_VERKAUFT,
    dict(kind="count", l="Anfragen in elf Wochen", to="70", cnt=(0, 70, 0, "", ""), pill="35 Interessenten",
         rows=[("Anfragen", 70, 70, False), ("davon Anleger", 70, 7, True)],
         cap="Über die Website, fast ausschließlich mobil. Jeder Punkt eine Anfrage."),
    dict(kind="text", l="Der größte Hebel", to="Ladezeit, nicht Sujet.", pill="16 Sekunden vorher",
         stations=["Name", "Marke", "Website", "Broschüre", "Bauzaun", "Kampagne"],
         cap="Vom Namen bis zum Kaufvertrag aus einer Hand. Die Seite lud am Telefon in 16 Sekunden, das war der Conversion-Hebel.")]),
 "case-web-trattner": dict(h=H_QUAL, cards=[
    dict(kind="text", l="Zwei Zielgruppen", to="Suchende und Eigentümer, getrennt abgeholt.", pill="1 Auftritt",
         stations=["Objektsuche", "Suchende", "Eigentümer", "Kontakt"],
         cap="Klare Objektsuche, ruhige Typografie, eine Struktur, die zwei Gruppen führt."),
    dict(kind="media", l="Die Seite", to="So souverän wie im Gespräch.", pill="Traditionsbetrieb", imgs=web_imgs("trattner"),
         cap="Ein Makler-Traditionsbetrieb, der digital so auftritt wie im persönlichen Gespräch."),
    dict(kind="text", l="Was wir gemacht haben", to="Strategie, Struktur, Design, Copy, Umsetzung.", pill="Aus einer Hand",
         cap="Ein Auftritt, der Seriosität zeigt, ohne laut zu werden.")]),
 "case-web-unio": dict(h=H_PROD, cards=[
    dict(kind="count", l="Bausteine in unter zwölf Monaten", to="10", cnt=(0, 10, 0, "", ""), pill="12 Monate",
         rows=[("Bausteine", 10, 10, True)],
         cap="Brand Guide, drei Storylines, Trailer, Pitch-Decks, Faltschilder, Banner, Karten, Plakate, Beschilderung, Website."),
    dict(kind="count", l="Ausschreibungs-Framework", to="7", cnt=(0, 7, 0, "", ""), unit="Ausschlusskriterien", pill="2 Lose",
         rows=[("Ausschlusskriterien", 7, 7, True), ("Lose", 7, 2, False)],
         cap="Macht aus einer Agenturauswahl eine Entscheidung mit Kriterien: Marketing und Vermarktung getrennt."),
    dict(kind="text", l="Unsere Rolle", to="Skin in the Game, wörtlich.", pill="Beteiligt",
         cap="Marketing-Engine von UNIO und Beteiligte am Venture, auf beiden Seiten des Tisches.")]),
 "case-web-havenstone": dict(h=H_QUAL, cards=[
    HAVENSTONE_WOCHEN,
    dict(kind="count", l="Was ein neues Haus am ersten Tag braucht", to="5", cnt=(0, 5, 0, "", ""), unit="Bausteine", pill="Ein Auftritt, eine Sprache",
         rows=[("Bausteine", 5, 5, True)],
         cap="E-Mail-Signaturen, Präsentationsvorlage, LinkedIn-Design, Exposé-Vorlage, Arbeitsplatz in der Cloud."),
    dict(kind="quote", l="Was der Kunde sagt", q="Wir fühlen uns damit sehr wohl und möchten uns noch einmal herzlich für den persönlichen Einsatz in so kurzer Zeit bedanken.",
         a="Robert Petrović, Partner und Co-Founder, Havenstone")]),
 "case-web-northpoint": dict(h=H_QUAL, cards=[
    dict(kind="text", l="Die Erzählung", to="Vertrauen, in zwei Sprachen.", pill="DE, EN",
         stations=["Strategie", "Struktur", "Verantwortung"],
         cap="Die Beratungsleistung übersetzt in eine klare, vertrauensbildende Erzählung."),
    dict(kind="media", l="Der Auftritt", to="Ruhige Bildwelt, präzise Sprache.", pill="Advisory", imgs=web_imgs("northpoint"),
         cap="Wenig Lärm, viel Klarheit: ein Auftritt, der Beratung wie Beratung aussehen lässt."),
    dict(kind="text", l="Was wir gemacht haben", to="Positionierung, Design, Copy, Umsetzung.", pill="Aus einer Hand",
         cap="Von der Strategie bis zur zweisprachigen Umsetzung.")]),
 "case-web-pharmacom": dict(h=H_QUAL, cards=[
    dict(kind="text", l="Vom Angebot zur Unterschrift", to="Drei Stunden.", pill="5 Wochen bis live",
         stations=["Angebot", "Unterschrift", "Design", "Dreh", "Live"],
         cap="Drei Stunden nach dem Angebot kam die Unterschrift zurück. Fünf Wochen später stand die Seite."),
    dict(kind="count", l="Seiten in zwei Sprachen", to="6", cnt=(0, 6, 0, "", ""), unit="Seiten", pill="plus Blog und Jobs",
         rows=[("Seiten", 6, 6, True), ("Blog, Jobs", 6, 2, False)],
         cap="Anfrageformular, CMS, ein halber Drehtag für Fotos und Screenrecordings der eigenen Software."),
    dict(kind="quote", l="Was der Kunde sagt", q="Unterschrieben anbei. Wir freuen uns auf die Zusammenarbeit.", a="Christoph Siegesleuthner, Geschäftsführung, Pharmacom",
         cap="Aus dem Projekt wurde ein zweites: die Website der Schwesterfirma DaPhi.")]),
 "case-web-daphi": dict(h=H_QUAL, cards=[
    dict(kind="text", l="Vom Kick-off zur Übergabe", to="Zwölf Wochen.", pill="Sprint-Plan in Kalenderwochen",
         stations=["Kick-off", "Sitemap", "Wireframes", "Screendesign", "Umsetzung", "Übergabe"],
         cap="Kick-off Mitte November, Übergabe Mitte Februar. Ein Plan mit Kalenderwochen statt einer Wunschliste."),
    dict(kind="count", l="Seiten in zwei Sprachen", to="6", cnt=(0, 6, 0, "", ""), unit="Seiten", pill="Webflow, Figma",
         rows=[("Seiten", 6, 6, True), ("Blog, Karriere", 6, 2, False)],
         cap="Gebaut in Webflow nach Wireframes und Screendesign in Figma."),
    dict(kind="quote", l="Was der Kunde sagt", q="Danke fürs schnelle Fixen! Ihr habt schon sehr viel für uns gemacht.", a="Hendrik Walter, Projektleitung, DaPhi",
         cap="Der Auftrag kam über einen Kunden: DaPhi ist das Schwesterprojekt von Pharmacom.")]),
 "case-web-ib7": dict(h=H_PROD, cards=[
    dict(kind="count", l="Was schon steht", to="4", cnt=(0, 4, 0, "", ""), unit="Bausteine", pill="Marke bis Performance",
         rows=[("Bausteine", 4, 4, True)],
         cap="Website mit Hero-Film, Founder-Reel, UGC-Anzeigen, Sampling-Formular für den Vertrieb."),
    dict(kind="media", l="Marke im Feed", to="Antikes Wissen, moderne Wissenschaft.", pill="Social, Grafik, Foto, Film",
         imgs=["assets/case/case-web-ib7/g0.jpg", "assets/case/case-web-ib7/g1.jpg", "assets/case/case-web-ib7/g2.jpg"],
         cap="Feed und Stories, Anzeigen, Sampling-Karten, Produktfotografie und Bewegtbild aus einer Hand."),
    dict(kind="text", l="Die Zahlen", to="Zeigen wir, wenn sie belastbar sind.", pill="Kampagnen gestartet",
         cap="Nicht wenn sie gut aussehen. Wer die Seite baut, sitzt auch im Call, in dem die ersten Zahlen gelesen werden.")]),
 "case-web-twistnsparkle": dict(h=H_NUM, cards=[
    L(CONSUMER_ROAS, "case-consumer-brand.html", "Zum Performance-Case"),
    CONSUMER_CPM,
    dict(kind="count", l="Launch-Termine", to="4", cnt=(0, 4, 0, "", ""), pill="3 Sprachen, 3 Länder",
         rows=[("Launch-Termine", 4, 4, True), ("Länder", 4, 3, False), ("Sprachen", 4, 3, False)],
         cap="Frankfurt, US-Messen, Kanada, dann Österreich, Deutschland und die USA. Gebaut gegen die Zeit, mit Platzhaltern zuerst.")]),
}

# ---------------------------------------------------------------- handgebaute Seiten (_brand_inplace.py, _build_funkhaus_v3.py)
HAND_KPI = {
 "case-premium-neubau": dict(h=H_NUM, cards=[FUNKHAUS_CPL, FUNKHAUS_STRECKE, FUNKHAUS_MOTIV]),
 "case-kommunalkredit": dict(h=H_PROD, cards=[
    KK_CLIPS,
    dict(kind="jump", l="Reichweite eines Beitrags", frm="€ 164 Budget", to="24.000", cnt=(0, 24000, 0, "", ""), unit="Personen", pill="vorzeitig gestoppt",
         rows=[("Erreichte Personen", 24, 24, True)],
         cap="Ein gesponserter LinkedIn-Beitrag zur Konferenz in Berlin, gestoppt, weil das Ziel erreicht war. Ein Punkt sind 1.000 Personen."),
    dict(kind="quote", l="Zum Introfilm", q="VO ist super. Musikwahl ist super. Tempo ist super.", a="Leitung Kommunikation und Marketing",
         cap="Freigabe nach dem ersten Schnitt. Rund 6.500 Klicks brachten die Kampagnen bis Ende August auf die Veranstaltungsseite.")]),
}

# ---------------------------------------------------------------- Leistungen (_gen_services.py): drei Mandate, drei Spruenge, je mit Link
SERVICE_KPI = {
 "service-ecommerce": dict(h=("Drei Marken,", "drei Sprünge."), cards=[
    L(D2C_UMSATZ, "case-d2c-lifestyle.html"), L(CONSUMER_ROAS, "case-consumer-brand.html"), L(NORDIC_ORDERS, "case-nordic-spirit.html")]),
 "service-performance-marketing": dict(h=("Drei Projekte,", "drei Sprünge."), cards=[
    L(FUNKHAUS_CPL, "case-premium-neubau.html"), L(FLORIDSDORF_STRECKE, "case-wohnbau-floridsdorf.html"), L(CROWD_ROAS, "case-crowdinvesting.html")]),
 "service-content-creation": dict(h=("Drei Mandate,", "drei Belege."), cards=[
    L(HEALTH_CREATOR, "case-health-brand.html"), L(FUNKHAUS_MOTIV, "case-premium-neubau.html"), L(KK_CLIPS, "case-kommunalkredit.html")]),
 "service-websites": dict(h=("Drei Seiten,", "drei Belege."), cards=[
    L(NOMA_VERKAUFT, "case-web-noma.html"), L(HAVENSTONE_WOCHEN, "case-web-havenstone.html"), L(PV_BESUCHER, "case-photovoltaik.html")]),
 "service-strategie": dict(h=("Drei Mandate,", "drei Sprünge."), cards=[
    L(INVEST_129, "case-immobilien-investment.html"), L(CROWD_INVESTOR, "case-crowdinvesting.html"), L(CONSUMER_CPM, "case-consumer-brand.html")]),
 "service-chatgpt-ads": dict(h=("Drei Mandate,", "drei Sprünge."), cards=[
    L(NORDIC_ORDERS, "case-nordic-spirit.html"), L(CROWD_ROAS, "case-crowdinvesting.html"), L(CONSUMER_CPM, "case-consumer-brand.html")]),
}

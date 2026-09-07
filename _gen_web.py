# Web-Case-Generator: 10 Homepage-Cases (neue Website inkl. Strategie), ohne erfundene KPIs
# Assets: web_<name>_d.jpg (Hero), web_<name>_d1/d2 (Scroll), web_<name>_ds0..2 (Unterseiten),
#         web_<name>_m0..m2 + web_<name>_ms0..1 (mobil). Galerien bauen sich aus dem, was existiert.
# -*- coding: utf-8 -*-
import os
from _gen import HEAD, FOOTER, menu

WEBCASES = [
 dict(slug="case-web-noma", key="noma", name="Noma Wien", url="https://www.noma.wien",
  branche="Real Estate, Projekt-Vermarktung",
  line="Projekt-Website mit Wohnungsfinder für 26 Wohnungen.",
  story="Ein Neubauprojekt am Prater brauchte einen Auftritt, der Ruhe ausstrahlt und trotzdem verkauft: klare Struktur, Wohnungsfinder, Anleger-Strecke und eine Bildsprache, die das Zuhause zeigt, nicht das Exposé.",
  leistungen="Branding & Storytelling<br>Website & Wohnungsfinder<br>Broschüre, Exposés, Bauzaun<br>Performance Marketing",
  disz=[("Websites & Landingpages", "service-websites.html"), ("Performance Marketing", "service-performance-marketing.html"), ("Content Creation", "service-content-creation.html")],
  kap=dict(label="Zweites Kapitel, die Vermarktung",
           h="Vom Namen bis zum Kaufvertrag.",
           p1="Noma begann nicht mit einer Website, sondern mit einem Namen. Danach kamen Logo und Bildsprache, die Projektwebsite mit Wohnungsfinder und Grundrissen, eine Broschüre, Verkaufspläne, Exposés je Wohnung und der Bauzaun. Und die Meta-Kampagnen, die seit dem Verkaufsstart im März auf die Seite führen, fast ausschließlich mobil.",
           p2="<b>In den ersten elf Wochen kamen rund 70 Anfragen von 35 Interessenten über die Website, darunter sieben Anleger.</b> Fünf Monate nach Go-live waren vier Wohnungen verkauft. Dazwischen lag die unangenehmste Erkenntnis des Projekts: Die Seite lud am Telefon in 16 Sekunden. Der größte Conversion-Hebel war kein neues Sujet, sondern Ladezeit.",
           links=[("service-performance-marketing.html", "Performance Marketing"), ("service-content-creation.html", "Content Creation")])),
 dict(slug="case-web-trattner", key="trattner", name="Trattner & Söhne", url="https://www.trattner-soehne.at",
  branche="Immobilien, Makler-Traditionsbetrieb",
  line="Neue Website: Strategie, Struktur, Umsetzung.",
  story="Ein Traditionsbetrieb, der digital so souverän auftreten soll wie im persönlichen Gespräch: klare Objektsuche, ruhige Typografie und eine Struktur, die Suchende und Eigentümer getrennt abholt.",
  leistungen="Strategie & Struktur<br>Design & Copy<br>Umsetzung"),
 dict(slug="case-web-unio", key="unio", name="UNIO", url="https://www.unio.at",
  branche="PropTech, Venture",
  line="Venture-Partnerschaft: Marke, Website, Produkt.",
  story="Real Estate, endlich einfach: Für das Immobilien-Betriebssystem UNIO entstanden Marke, Website und Produkt-Oberflächen aus einem Guss, als Venture, an dem wir selbst beteiligt sind. Skin in the Game, wörtlich.",
  leistungen="Marke & Positionierung<br>Website & Produkt-Design<br>Film, Print & Beschilderung<br>Laufende Weiterentwicklung",
  disz=[("Websites & Landingpages", "service-websites.html"), ("Strategie & Funnel", "service-strategie.html"), ("Content Creation", "service-content-creation.html")],
  kap=dict(label="Zweites Kapitel, die Marke",
           h="Eine Kategorie braucht mehr als eine Website.",
           p1="Für UNIO haben wir in unter zwölf Monaten alles gebaut, was eine neue Kategorie sichtbar macht: Brand Guide mit Farben und Schriften, drei Storylines für Makler, Bauträger und Partner, einen Trailer, Pitch-Decks, Faltschilder, Banner, Karten und Plakate für Events, die Beschilderung für den Standort und die Website mit Lead-Routing an die richtigen Teams.",
           p2="<b>Dazu ein Ausschreibungs-Framework für Bauträger:</b> zwei Lose, Marketing und Vermarktung, sieben Ausschlusskriterien. Es macht aus einer Agenturauswahl eine Entscheidung mit Kriterien. Wir sitzen dabei auf beiden Seiten des Tisches, als Marketing-Engine von UNIO und als Beteiligte.",
           links=[("service-strategie.html", "Strategie & Funnel"), ("service-content-creation.html", "Content Creation")])),
 dict(slug="case-web-havenstone", key="havenstone", name="Havenstone", url="https://www.havenstone.at",
  branche="Real Estate, Development",
  line="Website für den Entwickler: From Vision to Reality.",
  story="Internationale Projekte brauchen einen Auftritt, der Größe zeigt, ohne laut zu werden: großes Bewegtbild, wenige Worte, klare Wege zu den Projekten.",
  leistungen="Strategie & Struktur<br>Design<br>Umsetzung<br>Signaturen, Vorlagen, Workspace",
  kap=dict(label="Zweites Kapitel, vier Wochen",
           h="Vier Partner, eine Meinung, vier Wochen.",
           p1="Vier Gründer mit vier Vorstellungen davon, wie Seriosität aussieht. Wir haben nicht diskutiert, sondern gezeigt: fünf Bildstile zur Auswahl, ein Bewegtbild im Header, wenige Worte. Vom Briefing bis zur Go-live-Freigabe vergingen vier Wochen.",
           p2="<b>Dazu alles, was ein neues Beratungshaus am ersten Tag braucht:</b> E-Mail-Signaturen, Präsentationsvorlage, LinkedIn-Design, Exposé-Vorlage für die Objekte und die Einrichtung des Arbeitsplatzes in der Cloud. Ein Auftritt, der von der Website bis zur Mail-Signatur dieselbe Sprache spricht."),
  quote=("Das Feedback des Teams zur Website ist durchweg positiv. Wir fühlen uns damit sehr wohl und möchten uns noch einmal herzlich für den persönlichen Einsatz in so kurzer Zeit bedanken.", "Robert Petrović, Partner und Co-Founder, Havenstone")),
 dict(slug="case-web-northpoint", key="northpoint", name="Northpoint Advisors", url="https://northpoint-advisors.com",
  branche="Finance, Advisory",
  line="Website für die Beratungsboutique: Kapital, Strategie, Immobilie.",
  story="Strategie, Struktur, Verantwortung: Der Auftritt übersetzt die Beratungsleistung in eine klare, vertrauensbildende Erzählung, mit ruhiger Bildwelt und präziser Sprache in zwei Sprachen.",
  leistungen="Strategie & Positionierung<br>Design & Copy<br>Umsetzung"),
 dict(slug="case-web-pharmacom", key="pharmacom", name="Pharmacom", url="https://www.pharmacom.at",
  branche="Pharma, B2B",
  line="Corporate Website: Direct to Pharmacy.",
  story="Ein erklärungsbedürftiges B2B-Modell, verständlich gemacht: Die Website führt Hersteller und Apotheken durch Prozess, Nutzen und Team, seriös und ohne Fachjargon-Wände.",
  leistungen="Strategie & Struktur<br>Design & Copy<br>Umsetzung<br>Fotoshooting",
  kap=dict(label="Zweites Kapitel, fünf Wochen",
           h="Angebot am Vormittag, Unterschrift am Nachmittag.",
           p1="Drei Stunden nach dem Angebot kam die Unterschrift zurück. Fünf Wochen später stand die Seite: sechs Seiten plus Blog und Jobs in zwei Sprachen, Anfrageformular, CMS, ein halber Drehtag für die Fotos und Screenrecordings der eigenen Software, damit das B2B-Modell sichtbar wird statt erklärt.",
           p2="<b>Aus dem Projekt wurde ein zweites:</b> Die Geschäftsführung brachte die Schwesterfirma DaPhi mit, deren Website wir direkt im Anschluss gebaut haben.",
           links=[("case-web-daphi.html", "Zum Schwesterprojekt DaPhi")]),
  quote=("Unterschrieben anbei. Wir freuen uns auf die Zusammenarbeit.", "Christoph Siegesleuthner, Geschäftsführung, Pharmacom, drei Stunden nach dem Angebot")),
 dict(slug="case-web-daphi", key="daphi", name="DaPhi", url="https://www.daphi.de",
  branche="IT-Dienstleistung, B2B",
  line="Neue Website: Sitemap, Wireframes, Service-Landingpages.",
  story="Vom Kick-off bis zum Go-live in einem strukturierten Sprint-Plan: Sitemap und Wireframes für Home und sieben Service-Landingpages, Screendesign in zwei Runden, Umsetzung mit CMS, danach Content und Launch.",
  leistungen="Strategie, Sitemap & Wireframes<br>Screendesign<br>Umsetzung mit CMS",
  kap=dict(label="Zweites Kapitel, der Sprint",
           h="Vom Kick-off zur Übergabe in zwölf Wochen.",
           p1="Kick-off Mitte November, Übergabe Mitte Februar: sechs Seiten, Blog und Karrierebereich in zwei Sprachen, gebaut in Webflow nach Wireframes und Screendesign in Figma. Der Kunde bekam einen Sprint-Plan mit Kalenderwochen statt einer Wunschliste.",
           p2="<b>Der Auftrag kam über einen Kunden:</b> Wer eine Website bei uns gebaut hat, empfiehlt uns weiter. DaPhi ist das Schwesterprojekt von Pharmacom, beide Auftritte entstanden nacheinander aus einer Hand.",
           links=[("case-web-pharmacom.html", "Zum Schwesterprojekt Pharmacom")]),
  quote=("Danke fürs schnelle Fixen! Ihr habt schon sehr viel für uns gemacht.", "Hendrik Walter, Projektleitung, DaPhi")),
 dict(slug="case-web-ib7", key="ib7", name="IB-7", url="https://ib-7.com",
  branche="Beauty, D2C",
  line="Website und Marke: Wo Jahrtausende auf den Moment treffen.",
  story="Antikes Wissen über Hautpflege trifft moderne Wissenschaft: Der Auftritt erzählt die Marke, führt zu den Produkten und trägt die Kampagnen, die wir parallel in Performance und Content fahren.",
  leistungen="Website & Markenauftritt<br>Content Creation<br>Performance Marketing",
  disz=[("Websites & Landingpages", "service-websites.html"), ("Content Creation", "service-content-creation.html"), ("Performance Marketing", "service-performance-marketing.html")],
  kap=dict(label="Zweites und drittes Kapitel",
           h="Content und Performance aus derselben Hand.",
           p1="Die Website ist der Ort, an dem alles zusammenläuft. Parallel produzieren wir den Content für Feed und Shop, von der Produktfotografie bis zum Bewegtbild, und steuern die Performance-Kampagnen, die den Traffic bringen.",
           p2="<b>Ein Team, eine Logik:</b> Wer die Seite baut, sitzt auch im Call, in dem die Kampagnenzahlen gelesen werden. Marke, Website, Content und Performance folgen so einer Linie, statt an drei Agenturen zu hängen."),
  voice=dict(label="Was der Kunde sagt",
             lead="Michael Rohrmeier, Gründer und CEO von IB-7, über die Zusammenarbeit mit ad.boutique: Marke, Website, Performance und Content aus einer Hand.",
             a="Michael Rohrmeier, Gründer und CEO, IB-7",
             video="assets/video/kundenstimme-ib7.mp4",
             note="Kein Dashboard, das niemand liest. Wir gehen die Zahlen gemeinsam durch, auch die, die nicht funktioniert haben.")),
 dict(slug="case-web-twistnsparkle", key="twistnsparkle", name="Twist'n Sparkle, isi", url="https://www.twistnsparkle.isi.com/en",
  branche="Consumer, Produkt-Kampagne",
  line="Produkt-Kampagnen-Site: Sparkle it your way.",
  story="Ein Produkt, ein Versprechen, eine Seite: Die Kampagnen-Site macht aus dem Twist'n Sparkle ein Erlebnis, von Benefits über How-to bis zu Rezepten, gebaut für Kampagnen-Traffic.",
  leistungen="Struktur & Story<br>Design<br>Umsetzung<br>Laufende Weiterentwicklung",
  disz=[("Websites & Landingpages", "service-websites.html"), ("Performance Marketing", "service-performance-marketing.html")],
  kap=dict(label="Zweites Kapitel, die Zahlen dahinter",
           h="Die Seite trägt die Kampagne. Die Kampagne trägt die Marke.",
           p1="Die Kampagnen-Site ist der Ort, auf den die Saison-Kampagnen der Marke führen. Am Black Friday lag der Return on Ad Spend bei 4,02, 75 Prozent über dem Benchmark des Kontos, die Awareness im Vorlauf kostete 0,99 Euro je tausend Kontakte statt 3,50.",
           p2="<b>Gebaut wurde die Seite gegen die Zeit:</b> vier Launch-Termine in drei Ländern, Content der Kreativagentur, der spät kam, und ein Pitch gegen eine zweite Agentur, den wir gewonnen haben. Die ganze Geschichte steht im Consumer-Brand-Case.",
           links=[("case-consumer-brand.html", "Zum Performance-Case"), ("service-performance-marketing.html", "Performance Marketing")]),
  quote=("Mit der Zusammenarbeit im Performance-Bereich war und bin ich sehr zufrieden, und auch die Ergebnisse können sich sehen lassen.", "Teamlead E-Commerce, isi")),
]

IMG = "assets/img"
def ex(p):
    return os.path.exists(p)

def page(c, nxt):
    k = c["key"]
    hero_img = "%s/web_%s_d.jpg" % (IMG, k)
    d_shots = [p for p in ["%s/web_%s_d1.jpg" % (IMG, k), "%s/web_%s_d2.jpg" % (IMG, k)] if ex(p)]
    subs = [p for p in ["%s/web_%s_ds0.jpg" % (IMG, k), "%s/web_%s_ds1.jpg" % (IMG, k), "%s/web_%s_ds2.jpg" % (IMG, k)] if ex(p)]
    mobs = [p for p in ["%s/web_%s_m0.jpg" % (IMG, k), "%s/web_%s_m1.jpg" % (IMG, k), "%s/web_%s_m2.jpg" % (IMG, k),
                        "%s/web_%s_ms0.jpg" % (IMG, k), "%s/web_%s_ms1.jpg" % (IMG, k)] if ex(p)]
    if not mobs and ex("%s/web_%s_m.jpg" % (IMG, k)):
        mobs = ["%s/web_%s_m.jpg" % (IMG, k)]

    stage = ""
    if d_shots:
        stage = """  <!-- STAGE -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: 0 0 clamp(110px,14vw,200px)">
    <div class="wrap">
      <div class="stage" data-fade><img loading="lazy" decoding="async" src="%s" alt="%s"></div>
    </div>
  </section>

""" % (d_shots[0], c["name"])

    phones = ""
    if len(mobs) >= 3:
        colA = mobs[0::2][:3]; colB = mobs[1::2][:3]
        def _col(items, speed):
            fr = "\n          ".join('<div class="phframe"><img loading="lazy" decoding="async" src="%s" alt=""></div>' % i for i in items)
            return '<div class="phcol" data-drift="%s">\n          %s\n        </div>' % (speed, fr)
        phones = """  <!-- MOBILE -->
  <section class="sec fg-light bg-paper phonesec" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap phwrap">
      <div class="phtxt">
        <div class="lchap" style="grid-template-columns:1fr;gap:18px">
          <div class="lh" data-lines><span class="rl"><span>Mobil zuerst gedacht.</span></span></div>
          <p class="lt3" data-fade>Der Auftritt, wie ihn die meisten Besucher sehen: am Telefon, Seite für Seite.</p>
        </div>
      </div>
      <div class="phcols">
        """ + _col(colA, "0.14") + """
        """ + _col(colB, "0.24") + """
      </div>
    </div>
  </section>

"""

    gal = ""
    gal_imgs = (subs + d_shots[1:])[:3]
    if gal_imgs:
        cells = []
        speeds = ["0.05", "0.11", "0.07"]
        for i, g in enumerate(gal_imgs):
            cells.append('<div data-drift="%s"%s><span data-scale style="display:block;overflow:hidden;border-radius:3px"><img loading="lazy" decoding="async" src="%s" alt=""></span></div>' % (
                speeds[i % 3], ' style="margin-top:44px"' if i == 1 else (' style="margin-top:14px"' if i == 2 else ""), g))
        gal = """  <!-- UNTERSEITEN -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:0;padding-bottom:clamp(160px,20vw,280px)">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(28px,3.4vw,48px)">Aus dem Projekt</span>
      <div class="cgal">
        """ + "\n        ".join(cells) + """
      </div>
    </div>
  </section>

"""

    # Weitere Kapitel: was ueber die Website hinaus fuer den Kunden laeuft, plus Kundenstimme.
    # Der Marker "KAPITEL: MEHR" ist die Einsetzstelle fuer die Content-Galerie aus _apply_content.py,
    # damit die Reihenfolge Website -> Content -> Performance-Text -> Kundenstimme -> Next entsteht.
    extra = ""
    if c.get("kap"):
        k = c["kap"]
        extra += """  <!-- KAPITEL: MEHR -->
  <section class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">%s</span>
        <div class="lh" data-lines><span class="rl"><span>%s</span></span></div>
      </div>
      <div data-stagger>
        <p class="lt3" data-fade>%s</p>
        <p class="lt3" data-fade>%s</p>
%s      </div>
    </div>
  </section>

""" % (k["label"], k["h"], k["p1"], k["p2"],
       ('        <div data-fade style="display:flex;gap:clamp(22px,3vw,44px);flex-wrap:wrap;margin-top:22px">\n' + "".join('          <a class="zalink" href="%s">%s</a>\n' % l for l in k["links"]) + '        </div>\n') if k.get("links") else "")
    if c.get("quote"):
        extra += """  <!-- WAS DER KUNDE SAGT -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap" style="max-width:980px">
      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(22px,3vw,40px)">Was der Kunde sagt</span>
      <p class="serif" data-fade style="font-size:clamp(24px,2.6vw,40px);line-height:1.3;letter-spacing:-0.01em">&bdquo;%s&ldquo;</p>
      <div data-fade style="margin-top:22px;font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--grey-dark)">%s</div>
    </div>
  </section>

""" % c["quote"]
    if c.get("voice"):
        v = c["voice"]
        extra += """  <!-- KAPITEL: KUNDENSTIMME -->
  <section class="sec fg-dark" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">
    <div class="wrap vsplit">
      <div class="vtxt">
        <span class="label" style="color:var(--champ)">%s</span>
        <p class="vq vq--lead" data-fade>%s</p>
        <div class="va" data-fade>%s</div>
        <p class="vnote" data-fade>%s</p>
      </div>
      <div class="vmedia vmedia--video" data-fade>
        <div class="pwiv">
          <video class="ivplayer" data-auto muted loop playsinline preload="none" width="640" height="1138" src="%s"></video>
          <button class="ivsound" type="button" aria-label="Ton einschalten"><span class="ivbars"><i></i><i></i><i></i></span><span class="ivlabel">Ton an</span></button>
        </div>
      </div>
    </div>
  </section>

""" % (v["label"], v["lead"], v["a"], v["note"], v["video"])

    nxt_href = nxt["slug"] + ".html"
    nxt_img = "%s/web_%s_d.jpg" % (IMG, nxt["key"])
    body = HEAD.format(title="Case, " + c["name"], bodybg="#0E0E10") + menu("work.html", back=True) + """<main>

  <!-- HERO: Vollbild-Screenshot -->
  <section class="chero" data-bg="#0E0E10" data-fg="light">
    <img src=\"""" + hero_img + """\" alt=\"""" + c["name"] + """\" style="object-position: top">
    <div class="hcap">
      <div class="cl" style="font-size:15px">""" + c["name"] + """ <span>""" + c["branche"] + """</span></div>
      <div class="dispn" style="--n:""" + str(len(c["line"])) + """">""" + c["line"] + """</div>
    </div>
    <div class="scrollhint">Scrollen</div>
  </section>

  <!-- INTRO -->
  <section class="sec fg-light cintro bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap grid">
      <div>
        <span class="label" style="color:var(--grey-dark)">""" + c["branche"] + """</span>
        <p class="serif" data-scrub style="margin-top:22px">""" + c["story"] + """</p>
        <div data-fade style="--i:2;margin-top:32px;display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn-i" href="mailto:hello@ad.boutique?subject=Website-Projekt">Ähnliches Projekt anfragen</a>
          <a class="btn btn-o" href=\"""" + c["url"] + """\" target="_blank" rel="noopener">Live ansehen ↗</a>
        </div>
      </div>
      <div class="cmeta" data-stagger>
        <div class="m" data-fade><div class="ml">Branche</div><div class="mv2">""" + c["branche"] + """</div></div>
        <div class="m" data-fade><div class="ml">Projekt</div><div class="mv2">Neue Website</div></div>
        <div class="m" data-fade><div class="ml">Leistungen</div><div class="mv2">""" + c["leistungen"] + """</div></div>
        <div class="m" data-fade><div class="ml">Leistungsseiten</div><div class="mv2">
          """ + "\n          ".join('<a href="%s">%s</a>' % (h, t) for t, h in c.get("disz", [("Websites & Landingpages", "service-websites.html")])) + """
        </div></div>
      </div>
    </div>
  </section>

""" + stage + phones + gal + extra + """  <!-- NEXT -->
  <section class="sec npro-sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-bottom:0;padding-top:clamp(60px,8vw,110px)">
    <div class="wrap">
      <div class="npbar2"><span>Nächste Website</span><a href="work.html">Alle ansehen</a></div>
      <a class="npro" href=\"""" + nxt_href + """\">
        <span>
          <span class="nptit">""" + nxt["name"] + """.</span>
          <span class="npsub2" style="display:block">""" + nxt["line"] + """</span>
          <span class="npgo">Case ansehen</span>
        </span>
        <span class="npim2" data-scale><img loading="lazy" decoding="async" src=\"""" + nxt_img + """\" alt=""></span>
      </a>
    </div>
  </section>

""" + FOOTER
    return body

if __name__ == "__main__":
    for i, c in enumerate(WEBCASES):
        nxt = WEBCASES[(i + 1) % len(WEBCASES)]
        open(c["slug"] + ".html", "w", encoding="utf-8").write(page(c, nxt))
        print("webcase", c["slug"])
    print("webcases done")

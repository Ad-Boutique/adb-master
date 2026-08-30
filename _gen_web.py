# Web-Case-Generator: 10 Homepage-Cases (neue Website inkl. Strategie), ohne erfundene KPIs
# Assets: web_<name>_d.jpg (Hero), web_<name>_d1/d2 (Scroll), web_<name>_ds0..2 (Unterseiten),
#         web_<name>_m0..m2 + web_<name>_ms0..1 (mobil). Galerien bauen sich aus dem, was existiert.
# -*- coding: utf-8 -*-
import os
from _gen import HEAD, FOOTER, menu

WEBCASES = [
 dict(slug="case-web-noma", key="noma", name="Noma Wien", url="https://www.noma.wien",
  branche="Real Estate · Projekt-Vermarktung",
  line="Projekt-Website mit Wohnungsfinder für 26 Eigentumswohnungen in 1030 Wien.",
  story="Ein Neubauprojekt am Prater brauchte einen Auftritt, der Ruhe ausstrahlt und trotzdem verkauft: klare Struktur, Wohnungsfinder, Anleger-Strecke und eine Bildsprache, die das Zuhause zeigt, nicht das Exposé.",
  leistungen="Strategie & Struktur<br>Design & Copy<br>Umsetzung & Wohnungsfinder"),
 dict(slug="case-web-funkhausliving", key="funkhausliving", name="funkhaus.living", url="https://funkhaus.living",
  branche="Real Estate · Projekt-Vermarktung",
  line="Projekt-Website für das Funkhaus: Living, Culture, History.",
  story="Ikonische Architektur, gelebte Kultur und das Echo der Geschichte: Die Projekt-Website erzählt das Funkhaus als Ort, nicht als Grundriss-Katalog, und führt trotzdem in wenigen Schritten zur Wohnung.",
  leistungen="Strategie & Storytelling<br>Design & Copy<br>Umsetzung & Wohnungsfinder"),
 dict(slug="case-web-trattner", key="trattner", name="Trattner & Söhne", url="https://www.trattner-soehne.at",
  branche="Immobilien · Makler-Traditionsbetrieb",
  line="Neue Website inklusive Strategie, Struktur und Umsetzung.",
  story="Ein Traditionsbetrieb, der digital so souverän auftreten soll wie im persönlichen Gespräch: klare Objektsuche, ruhige Typografie und eine Struktur, die Suchende und Eigentümer getrennt abholt.",
  leistungen="Strategie & Struktur<br>Design & Copy<br>Umsetzung"),
 dict(slug="case-web-unio", key="unio", name="UNIO", url="https://www.unio.at",
  branche="PropTech · Venture",
  line="Venture-Partnerschaft: Marke, Website und Produkt-Design.",
  story="Real Estate, endlich einfach: Für das Immobilien-Betriebssystem UNIO entstanden Marke, Website und Produkt-Oberflächen aus einem Guss, als Venture, an dem wir selbst beteiligt sind. Skin in the Game, wörtlich.",
  leistungen="Marke & Positionierung<br>Website & Produkt-Design<br>Laufende Weiterentwicklung"),
 dict(slug="case-web-havenstone", key="havenstone", name="Havenstone", url="https://www.havenstone.at",
  branche="Real Estate · Development",
  line="Website für den Projektentwickler: From Vision to Reality.",
  story="Internationale Projekte brauchen einen Auftritt, der Größe zeigt, ohne laut zu werden: großes Bewegtbild, wenige Worte, klare Wege zu den Projekten.",
  leistungen="Strategie & Struktur<br>Design<br>Umsetzung"),
 dict(slug="case-web-northpoint", key="northpoint", name="Northpoint Advisors", url="https://northpoint-advisors.com",
  branche="Finance · Advisory",
  line="Website für die Beratungsboutique an der Schnittstelle von Kapital, Strategie und Immobilie.",
  story="Strategie, Struktur, Verantwortung: Der Auftritt übersetzt die Beratungsleistung in eine klare, vertrauensbildende Erzählung, mit ruhiger Bildwelt und präziser Sprache in zwei Sprachen.",
  leistungen="Strategie & Positionierung<br>Design & Copy<br>Umsetzung"),
 dict(slug="case-web-pharmacom", key="pharmacom", name="Pharmacom", url="https://www.pharmacom.at",
  branche="Pharma · B2B",
  line="Corporate Website: Direct to Pharmacy.",
  story="Ein erklärungsbedürftiges B2B-Modell, verständlich gemacht: Die Website führt Hersteller und Apotheken durch Prozess, Nutzen und Team, seriös und ohne Fachjargon-Wände.",
  leistungen="Strategie & Struktur<br>Design & Copy<br>Umsetzung"),
 dict(slug="case-web-daphi", key="daphi", name="DaPhi", url="https://www.daphi.de",
  branche="IT-Dienstleistung · B2B",
  line="Neue Website inklusive Sitemap, Wireframes und Service-Landingpages.",
  story="Vom Kick-off bis zum Go-live in einem strukturierten Sprint-Plan: Sitemap und Wireframes für Home und sieben Service-Landingpages, Screendesign in zwei Runden, Umsetzung mit CMS, danach Content und Launch.",
  leistungen="Strategie, Sitemap & Wireframes<br>Screendesign<br>Umsetzung mit CMS"),
 dict(slug="case-web-ib7", key="ib7", name="IB-7", url="https://ib-7.com",
  branche="Beauty · D2C",
  line="Website und Markenauftritt: Wo Jahrtausende auf den Moment treffen.",
  story="Antikes Wissen über Hautpflege trifft moderne Wissenschaft: Der Auftritt erzählt die Marke, führt zu den Produkten und trägt die Kampagnen, die wir parallel in Performance und Content fahren.",
  leistungen="Website & Markenauftritt<br>Content Creation<br>Performance Marketing"),
 dict(slug="case-web-twistnsparkle", key="twistnsparkle", name="Twist'n Sparkle · isi", url="https://www.twistnsparkle.isi.com/en",
  branche="Consumer · Produkt-Kampagne",
  line="Produkt-Kampagnen-Site: Sparkle it your way.",
  story="Ein Produkt, ein Versprechen, eine Seite: Die Kampagnen-Site macht aus dem Twist'n Sparkle ein Erlebnis, von Benefits über How-to bis zu Rezepten, gebaut für Kampagnen-Traffic.",
  leistungen="Struktur & Story<br>Design<br>Umsetzung"),
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

    nxt_href = nxt["slug"] + ".html"
    nxt_img = "%s/web_%s_d.jpg" % (IMG, nxt["key"])
    body = HEAD.format(title="Case · " + c["name"], bodybg="#0E0E10") + menu("work.html") + """<main>

  <!-- HERO: Vollbild-Screenshot -->
  <section class="chero" data-bg="#0E0E10" data-fg="light">
    <img src=\"""" + hero_img + """\" alt=\"""" + c["name"] + """\" style="object-position: top">
    <div class="hcap">
      <div class="cl" style="font-size:15px">""" + c["name"] + """ <span>· """ + c["branche"] + """</span></div>
      <div class="serif" style="font-size:clamp(30px,3.8vw,60px);margin-top:10px;text-shadow:0 2px 24px rgba(0,0,0,0.45)">""" + c["line"] + """</div>
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
        <div class="m" data-fade><div class="ml">Leistung</div><div class="mv2"><a href="service-websites.html">Websites & Landingpages</a></div></div>
      </div>
    </div>
  </section>

""" + stage + phones + gal + """  <!-- NEXT -->
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

for i, c in enumerate(WEBCASES):
    nxt = WEBCASES[(i + 1) % len(WEBCASES)]
    open(c["slug"] + ".html", "w", encoding="utf-8").write(page(c, nxt))
    print("webcase", c["slug"])
print("webcases done")

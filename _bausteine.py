# -*- coding: utf-8 -*-
"""Bausteine der Case-Vorlagen. Jeder Baustein ist eine Funktion (Case, Baustein, Kontext) -> Markup einer Sektion.

Zwei Vorlagen, ein Rahmen:
  dossier  Performance-Cases (_gen.py):  Hero, Intro, Kennzahlen, [Bausteine], Next-Case
  web      Website-Cases (_gen_web.py):   Hero, Intro, Kennzahlen, [Bausteine], Next-Website
Die Bausteine dazwischen kommen in der Reihenfolge der Liste "bausteine" der Inhaltsdatei auf die Seite.
Felder und Beispiele: _intern/CMS-CASES.md. Das Markup ist das der bisherigen Generatoren, Zeichen fuer Zeichen;
die Nachlaeufe (_imgdim, _brand_inplace, _footer, _ui_markup, _headlines, _seo) setzen darauf auf."""
import json
import os
import re
import subprocess

from _cases import bausteine, board, leistungen, naechster, rahmen, teaser
from _kpi import board as kpi_board, mini as kpi_mini


def _links(ls):
    """Textlinks unter einem Kapitel (.zalink)."""
    if not ls:
        return ""
    return ('        <div data-fade style="display:flex;gap:clamp(22px,3vw,44px);flex-wrap:wrap;margin-top:22px">\n'
            + "".join('          <a class="zalink" href="%s">%s</a>\n' % (l["href"], l["text"]) for l in ls) + '        </div>\n')


def _zeilen(xs):
    return "".join('<span class="rl"><span>%s</span></span>' % x for x in xs)


# ================================================================ gemeinsame Bausteine

def zitat(c, b, ctx):
    """Kundenstimme als Zitat auf Papier."""
    return ('  <!-- WAS DER KUNDE SAGT -->\n'
            '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">\n'
            '    <div class="wrap" style="max-width:980px">\n'
            '      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(22px,3vw,40px)">Was der Kunde sagt</span>\n'
            '      <p class="serif" data-fade style="font-size:clamp(24px,2.6vw,40px);line-height:1.3;letter-spacing:-0.01em">&bdquo;%s&ldquo;</p>\n'
            '      <div data-fade style="margin-top:22px;font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--grey-dark)">%s</div>\n'
            '    </div>\n'
            '  </section>\n\n') % (b["text"], b["wer"])


def mobil(c, b, ctx):
    """Handy-Screens in zwei driftenden Spalten. Web-Vorlage: hoechstens drei je Spalte."""
    web = c["vorlage"] == "web"
    flat, seen = [], set()
    for x in b["bilder"]:
        if x not in seen:
            seen.add(x)
            flat.append(x)
    colA, colB = flat[0::2], flat[1::2]
    if web:
        colA, colB = colA[:3], colB[:3]
    alt = ("Website %s, mobile Ansicht" if web else "Sujet aus der Kampagne, %s") % c["meta"]["name"]

    def _col(items, speed):
        fr = "\n          ".join('<div class="phframe"><img loading="lazy" decoding="async" src="%s" alt="%s"></div>' % (i, alt) for i in items)
        return '<div class="phcol" data-drift="%s">\n          %s\n        </div>' % (speed, fr)
    return ("  <!-- MOBILE -->\n" if web else "  <!-- MOBILE: Screens ziehen vorbei -->\n") + """  <section class="sec fg-light bg-paper phonesec" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap phwrap">
      <div class="phtxt">
        <div class="lchap" style="grid-template-columns:1fr;gap:18px">
          <div class="lh" data-lines><span class="rl"><span>""" + b["headline"] + """</span></span></div>
          <p class="lt3" data-fade>""" + b["text"] + """</p>
        </div>
      </div>
      <div class="phcols">
        """ + _col(colA, "0.14") + """
        """ + _col(colB, "0.24") + """
      </div>
    </div>
  </section>

"""


# ---------------------------------------------------------------- Galerie "Aus dem Mandat" (schraege Collage, Referenzgroesse)
NCOL = 6
_DIMS = None


def _ratio(p):
    """Hoehe je Breiteneinheit, aus den echten Dateimassen (assets/imgdim.json, sonst sips)."""
    global _DIMS
    if _DIMS is None:
        _DIMS = json.load(open("assets/imgdim.json")) if os.path.exists("assets/imgdim.json") else {}
    if p.endswith(".mp4"):
        return 16 / 9.0
    if p in _DIMS and _DIMS[p]:
        return _DIMS[p][1] / float(_DIMS[p][0])
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p], capture_output=True, text=True).stdout
    mw = re.search(r"pixelWidth:\s*(\d+)", out)
    mh = re.search(r"pixelHeight:\s*(\d+)", out)
    if not (mw and mh):
        return 1.0
    _DIMS[p] = [int(mw.group(1)), int(mh.group(1))]
    return _DIMS[p][1] / float(_DIMS[p][0])


def galerie_html(medien, bg="#0E0E10", label="Aus dem Mandat"):
    """Sechs driftende Spalten, jedes Motiv in die gerade kuerzeste Spalte, hohe zuerst."""
    media = [m for m in medien if os.path.exists(m)]
    if not media:
        return ""
    # so oft wiederholen, dass jede der sechs Spalten den Rahmen ueberragt
    while len(media) < NCOL * 4:
        media = media + media
    media = media[:NCOL * 5]
    cols = [[] for _ in range(NCOL)]
    hs = [0.0] * NCOL
    for m, r in sorted(((m, _ratio(m)) for m in media), key=lambda x: -x[1]):
        i = hs.index(min(hs))
        cols[i].append(m)
        hs[i] += r + 0.055
    speeds = ["0.042", "0.068", "0.05", "0.075", "0.056", "0.072"]
    parts = []
    for i, col in enumerate(cols):
        if not col:
            continue
        items = []
        for m in col:
            if m.endswith(".mp4"):
                items.append('<video data-auto muted loop playsinline preload="none" src="%s"></video>' % m)
            else:
                items.append('<img loading="lazy" decoding="async" src="%s" alt="Material aus dem Mandat">' % m)
        parts.append('      <div class="cpcol" data-drift="%s">\n        %s\n      </div>' % (speeds[i], "\n        ".join(items)))
    return ('  <!-- CONTENT AUS DEM MANDAT -->\n'
            '  <section class="collage collage--tight" data-bg="%s" data-fg="light">\n'
            '    <div class="wrap" style="position:relative;z-index:2;margin-bottom:clamp(30px,4vw,60px)">\n'
            '      <span class="label" style="color:var(--champ)">%s</span>\n'
            '    </div>\n'
            '    <div class="cplane">\n%s\n    </div>\n  </section>\n\n') % (bg, label, "\n".join(parts))


def galerie(c, b, ctx):
    return galerie_html(b["medien"], b.get("hintergrund", "#0E0E10"), b.get("label", "Aus dem Mandat"))


# ================================================================ Vorlage dossier

def d_hero(c, ctx):
    m, h = c["meta"], c["hero"]
    world, sub = ctx["world"], h["headline"]
    kurz = m["branche"].split(",")[0].strip()
    if h.get("bild"):
        k = h.get("kennzahl")
        kpi = ('\n    <div class="hkpi"><div class="kv">%s</div><div class="kl">(%s)</div></div>' % (k["wert"], k.get("label", ""))) if k and k.get("wert") else ""
        hero = """<section class="chero" data-bg="%s" data-fg="light">
    <img src="%s" alt="%s">
    <div class="hcap">
      <div class="cl" style="font-size:15px">%s <span>%s</span></div>
      <h1 class="dispn" style="--n:%d">%s</h1>
    </div>%s
    <div class="scrollhint">Scrollen</div>
  </section>""" % (world, h["bild"], m["name"], m["name"], kurz, len(sub), sub, kpi)
    else:
        # Farbwelt-Hero ohne Kennzahl, die Zahl steht im Ergebnis
        hero = """<section class="chero" data-bg="%s" data-fg="light" style="background:%s;color:%s">
    <div class="hcap">
      <div class="cl" style="font-size:15px">%s <span style="opacity:.65">%s</span></div>
      <h1 class="dispn" style="--n:%d">%s</h1>
    </div>

    <div class="scrollhint">Scrollen</div>
  </section>""" % (world, world, m.get("farbwelt_text", "#EDF2EC"), m["name"], kurz, len(sub), sub)
    return "  <!-- HERO: Vollbild in der Case-Farbwelt -->\n  " + hero + "\n\n"


def d_intro(c, ctx):
    m, i = c["meta"], c["intro"]
    disz_links = "\n          ".join('<a href="%s">%s</a>' % (h, t) for t, h in leistungen(c))
    return """  <!-- INTRO auf Papier: Story links, Key Facts rechts -->
  <section class="sec fg-light cintro bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap grid">
      <div>
        <span class="label" style="color:var(--grey-dark)">""" + rahmen(c).replace("<br>", ", ") + """</span>
        <p class="serif" data-scrub style="margin-top:22px">""" + i["these"] + """</p>
        <p class="body" data-fade style="--i:1">""" + i["text"] + """</p>
        <div data-fade style="--i:2;margin-top:32px;display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn-i" href="mailto:hello@ad.boutique?subject=Projekt wie """ + m["name"] + """">Ähnliches Projekt anfragen</a>
          <a class="btn btn-o" href="work.html">Alle Cases</a>
        </div>
      </div>
      <div class="cmeta" data-stagger>
        <div class="m" data-fade><div class="ml">Branche</div><div class="mv2">""" + m["branche"] + """</div></div>
        <div class="m" data-fade><div class="ml">Zeitraum</div><div class="mv2">""" + m["zeitraum"] + """</div></div>
        <div class="m" data-fade><div class="ml">Kanäle</div><div class="mv2">""" + m["kanaele"] + """</div></div>
        <div class="m" data-fade><div class="ml">Ziel</div><div class="mv2">""" + m.get("ziel", "") + """</div></div>
        <div class="m" data-fade><div class="ml">Leistungen</div><div class="mv2">
          """ + disz_links + """
        </div></div>
      </div>
    </div>
  </section>

"""


def statement(c, b, ctx):
    """These in der Farbwelt, jede Zeile eine Zeile."""
    world = ctx["world"]
    stmt = "\n".join('        <span class="rl"><span>%s</span></span>' % x for x in b["zeilen"])
    return """  <!-- STATEMENT in der Farbwelt -->
  <section class="cstate fg-dark" data-bg=\"""" + world + """\" data-fg="light" style="--case-clr:""" + world + """">
    <div class="inner">
      <span class="label" style="color:var(--champ)">So denken wir</span>
      <h2 class="dispn" data-lines>
""" + stmt + """
      </h2>
    </div>
  </section>

"""


def perspektiven(c, b, ctx):
    """Fuenf Perspektiven: Titel links, Satz rechts."""
    rows = "\n".join('        <div class="lrow" data-fade><div class="ll">%s</div><div class="lt">%s</div></div>' % (z["titel"], z["text"]) for z in b["zeilen"])
    return """  <!-- FÜNF PERSPEKTIVEN -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(30px,4vw,50px)">Fünf Perspektiven</span>
      <div class="lens" data-stagger>
""" + rows + """
      </div>
    </div>
  </section>

"""


def ergebnis(c, b, ctx):
    """Zahlenreihe. Erscheint nur, wenn der Case kein Kennzahlen-Board hat (das Board ersetzt die Reihe)."""
    if ctx["has_kpi"] or not b.get("zahlen"):
        return ""
    nums = "\n".join('        <div class="n" data-fade><div class="l">%s</div><div class="v num serif">%s</div></div>' % (z["label"], z["wert"]) for z in b["zahlen"])
    return """  <!-- ERGEBNIS -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:0">
    <div class="wrap">
      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(30px,4vw,50px)">Ergebnis</span>
      <div class="cnums" data-stagger>
""" + nums + """
      </div>
      <p class="cfoot-note" data-fade>""" + b.get("fussnote", "") + """</p>
    </div>
  </section>

"""


def d_kapitel(c, b, ctx):
    """Weiteres Kapitel. Der Grund wechselt ab: erstes Kapitel creme, zweites papier, drittes creme."""
    i = ctx["kapitel"]
    ctx["kapitel"] += 1
    bg, bgcls = ("#EFE7D6", "bg-cream") if i % 2 == 0 else ("#F3EDE1", "bg-paper")
    nums = ""
    if b.get("zahlen"):
        # Kapitel-Zahlen in der Grammatik des KPI-Boards: kleine Karten statt Zahlenreihe
        nums = '    <div class="wrap">\n' + kpi_mini([(z["label"], z["wert"]) for z in b["zahlen"]], b.get("fussnote")) + '    </div>\n'
    return ('  <!-- KAPITEL: %s -->\n'
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
            '  </section>\n\n' % (b["label"].upper(), bgcls, bg, b["label"], _zeilen(b["headline"]), b["absatz1"], b["absatz2"], _links(b.get("links")), nums))


def learnings(c, b, ctx):
    """Learnings in der Farbwelt, Saetze mit Linien dazwischen."""
    world, xs = ctx["world"], b["saetze"]
    learn = "\n".join('        <p class="serif" data-fade style="font-size:clamp(20px,1.9vw,28px);padding:18px 0;border-top:1px solid var(--line-d)%s">%s</p>' % (
        (";border-bottom:1px solid var(--line-d)" if i == len(xs) - 1 else ""), t) for i, t in enumerate(xs))
    return """  <!-- LEARNINGS -->
  <section class="sec fg-dark" data-bg=\"""" + world + """\" data-fg="light" style="background:""" + world + """">
    <div class="wrap" style="max-width:900px">
      <span class="label" style="color:var(--champ);display:block;margin-bottom:26px">Learnings</span>
      <div data-stagger>
""" + learn + """
      </div>
    </div>
  </section>

"""


def d_naechster(c, ctx):
    n = naechster(c)
    t = teaser(n)
    nxt_name = " ".join(t["titel"])
    if t.get("bild"):
        nxt_media = '<img loading="lazy" decoding="async" src="%s" alt="Nächster Case: %s">' % (t["bild"], n["meta"]["name"])
    else:
        nm = n["meta"]
        k = (n.get("hero") or {}).get("kennzahl")
        nxt_media = '<span style="display:flex;align-items:flex-end;aspect-ratio:4/3;background:%s;color:%s;padding:24px;border-radius:3px"><span style="font-family:var(--f-disp);font-weight:680;font-size:clamp(40px,4vw,64px);font-variant-numeric:tabular-nums">%s</span></span>' % (
            nm.get("farbwelt", "#22382C"), nm.get("farbwelt_text", "#EDF2EC"), (k or {}).get("wert") or nm["name"])
    return """  <!-- NEXT CASE -->
  <section class="sec npro-sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-bottom:0">
    <div class="wrap">
      <div class="npbar2"><span>Nächster Case</span><a href="work.html">Alle ansehen</a></div>
      <a class="npro" href=\"""" + n["slug"] + """.html">
        <span>
          <span class="nptit">""" + nxt_name + """</span>
          <span class="npsub2" style="display:block">""" + t["zeile"] + """</span>
          <span class="npgo">Case ansehen</span>
        </span>
        <span class="npim2" data-scale>""" + nxt_media + """</span>
      </a>
    </div>
  </section>

"""


# ================================================================ Vorlage web

def w_hero(c, ctx):
    m, h = c["meta"], c["hero"]
    return """  <!-- HERO: Screenshot oben, Bildzeile darunter auf Schwarz (Text nie auf Gesichtern oder auf dem Text der Kundenseite) -->
  <section class="chero chero--shot" data-bg="#0E0E10" data-fg="light">
    <img src=\"""" + h["bild"] + """\" alt=\"""" + m["name"] + """\" style="object-position: top">
    <div class="hcap">
      <div class="cl" style="font-size:15px">""" + m["name"] + """ <span>""" + m["branche"] + """</span></div>
      <h1 class="dispn" style="--n:""" + str(len(h["headline"])) + """">""" + h["headline"] + """</h1>
    </div>
    <div class="scrollhint">Scrollen</div>
  </section>

"""


def w_intro(c, ctx):
    m = c["meta"]
    return """  <!-- INTRO -->
  <section class="sec fg-light cintro bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap grid">
      <div>
        <span class="label" style="color:var(--grey-dark)">""" + m["branche"] + """</span>
        <p class="serif" data-scrub style="margin-top:22px">""" + c["intro"]["text"] + """</p>
        <div data-fade style="--i:2;margin-top:32px;display:flex;gap:12px;flex-wrap:wrap">
          <a class="btn btn-i" href="mailto:hello@ad.boutique?subject=Website-Projekt">Ähnliches Projekt anfragen</a>
          <a class="btn btn-o" href=\"""" + m["url"] + """\" target="_blank" rel="noopener">Live ansehen ↗</a>
        </div>
      </div>
      <div class="cmeta" data-stagger>
        <div class="m" data-fade><div class="ml">Branche</div><div class="mv2">""" + m["branche"] + """</div></div>
        <div class="m" data-fade><div class="ml">Projekt</div><div class="mv2">Neue Website</div></div>
        <div class="m" data-fade><div class="ml">Leistungen</div><div class="mv2">""" + "<br>".join(m["umfang"]) + """</div></div>
        <div class="m" data-fade><div class="ml">Leistungsseiten</div><div class="mv2">
          """ + "\n          ".join('<a href="%s">%s</a>' % (h, t) for t, h in (leistungen(c) or [("Websites & Landingpages", "service-websites.html")])) + """
        </div></div>
      </div>
    </div>
  </section>

"""


def buehne(c, b, ctx):
    """Ein grosser Desktop-Screenshot auf Papier."""
    return """  <!-- STAGE -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: 0 0 clamp(110px,14vw,200px)">
    <div class="wrap">
      <div class="stage" data-fade><img loading="lazy" decoding="async" src="%s" alt="%s"></div>
    </div>
  </section>

""" % (b["bild"], c["meta"]["name"])


def unterseiten(c, b, ctx):
    """Bis zu drei Unterseiten versetzt nebeneinander."""
    cells = []
    speeds = ["0.05", "0.11", "0.07"]
    for i, g in enumerate(b["bilder"][:3]):
        cells.append('<div data-drift="%s"%s><span data-scale style="display:block;overflow:hidden;border-radius:3px"><img loading="lazy" decoding="async" src="%s" alt="Website %s, Unterseite"></span></div>' % (
            speeds[i % 3], ' style="margin-top:44px"' if i == 1 else (' style="margin-top:14px"' if i == 2 else ""), g, c["meta"]["name"]))
    return """  <!-- UNTERSEITEN -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:0;padding-bottom:clamp(160px,20vw,280px)">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(28px,3.4vw,48px)">""" + b.get("label", "Aus dem Projekt") + """</span>
      <div class="cgal">
        """ + "\n        ".join(cells) + """
      </div>
    </div>
  </section>

"""


def w_kapitel(c, b, ctx):
    """Was ueber die Website hinaus fuer den Kunden laeuft. Der Kommentar "KAPITEL: MEHR" ist die Einsetzstelle,
    an der aeltere Staende die Content-Galerie einsetzten."""
    return """  <!-- KAPITEL: MEHR -->
  <section class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">
    <div class="wrap lchap">
      <div>
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">%s</span>
        <div class="lh" data-lines>%s</div>
      </div>
      <div data-stagger>
        <p class="lt3" data-fade>%s</p>
        <p class="lt3" data-fade>%s</p>
%s      </div>
    </div>
  </section>

""" % (b["label"], _zeilen(b["headline"]), b["absatz1"], b["absatz2"], _links(b.get("links")))


def stimme(c, b, ctx):
    """Kundenstimme als Video im Hochformat, mit Ton-Knopf. Das Posterbild heisst wie das Video mit -poster.jpg."""
    return """  <!-- KAPITEL: KUNDENSTIMME -->
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
          <video class="ivplayer" data-auto muted loop playsinline preload="metadata" poster="%s" width="640" height="1138" src="%s"></video>
          <button class="ivsound" type="button" aria-label="Ton einschalten"><span class="ivbars"><i></i><i></i><i></i></span><span class="ivlabel">Ton an</span></button>
        </div>
      </div>
    </div>
  </section>

""" % (b["label"], b["text"], b["wer"], b["notiz"], b["video"].replace(".mp4", "-poster.jpg"), b["video"])


def w_naechster(c, ctx):
    n = naechster(c)
    return """  <!-- NEXT -->
  <section class="sec npro-sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-bottom:0;padding-top:clamp(60px,8vw,110px)">
    <div class="wrap">
      <div class="npbar2"><span>Nächste Website</span><a href="work.html">Alle ansehen</a></div>
      <a class="npro" href=\"""" + n["slug"] + """.html">
        <span>
          <span class="nptit">""" + n["meta"]["name"] + """.</span>
          <span class="npsub2" style="display:block">""" + n["hero"]["headline"] + """</span>
          <span class="npgo">Case ansehen</span>
        </span>
        <span class="npim2" data-scale><img loading="lazy" decoding="async" src=\"""" + n["hero"]["bild"] + """\" alt="Nächste Website: """ + n["meta"]["name"] + """"></span>
      </a>
    </div>
  </section>

"""


# ================================================================ Register und Seitenkoerper

VORLAGE = {
    "dossier": dict(hero=d_hero, intro=d_intro, naechster=d_naechster, bausteine=dict(
        statement=statement, perspektiven=perspektiven, ergebnis=ergebnis, kapitel=d_kapitel,
        zitat=zitat, mobil=mobil, learnings=learnings, galerie=galerie)),
    "web": dict(hero=w_hero, intro=w_intro, naechster=w_naechster, bausteine=dict(
        buehne=buehne, mobil=mobil, unterseiten=unterseiten, galerie=galerie, kapitel=w_kapitel,
        zitat=zitat, stimme=stimme)),
}


def koerper(c):
    """Alles zwischen <main> und dem Footer: Hero, Intro, Kennzahlen, Bausteine, Next."""
    v = VORLAGE[c["vorlage"]]
    b = board(c)
    ctx = dict(world=c["meta"].get("farbwelt", "#22382C"), has_kpi=b is not None, kapitel=0)
    out = v["hero"](c, ctx) + v["intro"](c, ctx)
    if b:
        # KPI-Board direkt nach dem Intro
        out += kpi_board(b)
    for x in bausteine(c):
        out += v["bausteine"][x["typ"]](c, x, ctx)
    return out + v["naechster"](c, ctx)

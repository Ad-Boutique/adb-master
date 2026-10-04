# -*- coding: utf-8 -*-
"""Vorlage der Leistungsseiten: nur Markup. Jede Sektion ist eine Funktion, die aus den Daten einer Leistung
(_content/services/<slug>.json, geladen von _leistungen.py) ihr HTML schreibt; render_service() setzt die Seite
in der Reihenfolge der Dramaturgie zusammen. Daten und Logik (Laden, FAQ-Reihenfolge, Querverweise auf Cases,
Schreiben, Nachlauf) stehen in _leistungen.py und _gen_services.py.

Schema der Seite (Dramaturgie v2, alle sechs Leistungen): Hero (Woerterbuch) -> Prozess-Schema -> Problem ->
Nutzen -> Bildband -> Zoom -> Visual -> Material aus dem Mandat -> Beweis-Kopf -> Stationen -> Kennzahlen ->
Punkt-Graphen -> Cases -> Kundenstimme -> Team -> Logos -> Fit -> Ablauf -> Detail-Raster -> FAQ -> Angebot -> CTA.
Die fruehere Dramaturgie v1 (Akkordeon, Differenzierung, Beleg-Paar, Content-Wand, Stoerer) bleibt als flow "v1"
verfuegbar, derzeit nutzt sie keine Seite."""
from _gen import HEAD, FOOTER, menu, logogrid
from _kpi import board as kpi_board, dotrows as kpi_dotrows


def _zeilen(xs, sep=""):
    """Headline-Zeilen als <span class="rl"> (eine Zeile je Eintrag)."""
    return sep.join('<span class="rl"><span>%s</span></span>' % x for x in xs)


def _link(l):
    return (l["href"], l["text"])


def _reihen(rows):
    """Balken-Zeilen der Datei (label, prozent, wert) in die Form, die _kpi.dotrows() zeichnet."""
    return [(r["label"], r["prozent"], r["wert"]) for r in rows]


def _wall(s):
    w = s.get("wall")
    cols = s.get("wall_cols", [])
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
                    else ('<img loading="lazy" decoding="async" src="%s" alt="Material aus laufenden Mandaten">' % m)
            cells.append('<span class="cwt %s">%s</span>' % (cls, inner))
        parts.append('        <div class="cwcol" data-drift="%s">\n          %s\n        </div>'
                     % (speeds[i % len(speeds)], "\n          ".join(cells)))
    head = _zeilen(w["h"])
    link = ('<a class="zalink" href="%s">%s</a>' % _link(w["link"])) if w.get("link") else ""
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


def _content_section(s, label="Aus laufenden Mandaten"):
    cols = s.get("content_cols", [])
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
                cells.append('<img loading="lazy" decoding="async" src="%s" alt="Material aus laufenden Mandaten">' % m)
        parts.append('      <div class="cpcol" data-drift="%s">\n        %s\n      </div>' % (speeds[i], "\n        ".join(cells)))
    return ('  <!-- CONTENT AUS DEM MANDAT -->\n'
            '  <section class="collage collage--tight" data-bg="#08080A" data-fg="light" style="background:#08080A">\n'
            '    <div class="wrap" style="position:relative;z-index:2;margin-bottom:clamp(30px,4vw,60px)">\n'
            '      <span class="label" style="color:var(--champ)">' + label + '</span>\n'
            '    </div>\n'
            '    <div class="cplane">\n%s\n    </div>\n  </section>\n\n') % ("\n".join(parts))


def _tell(s):
    t = s.get("tell")
    if not t:
        return ""
    steps = "\n        ".join(
        '<div class="ts%s" data-v="%s" data-l="%s">\n          <div class="tt">%s</div>\n          <p>%s</p>\n        </div>'
        % ((" on" if i == 0 else ""), st["wert"], st["label"], st["titel"], st["text"]) for i, st in enumerate(t["steps"]))
    first = t["steps"][0]
    # Steht der Beweis-Kopf direkt darueber, braucht es hier kein zweites Label
    lab = ('      <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(30px,3.6vw,52px)">'
           + t.get("label", "Ein Fall, nachgerechnet") + '</span>\n') if not t.get("nolabel") else ""
    pad = "clamp(20px,3vw,50px)" if t.get("nolabel") else "clamp(70px,9vw,140px)"
    head = ('  <!-- ERGEBNIS ALS STATIONEN (scrollgesteuert) -->\n'
            '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:' + pad + '">\n'
            '    <div class="wrap">\n' + lab)
    rest = ('      <div class="tell">\n'
            '        <div class="tsteps">\n        %s\n        </div>\n'
            '        <div class="tfix">\n'
            '          <div class="tv">%s</div>\n'
            '          <div class="tl">%s</div>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n  </section>\n\n') % (steps, first["wert"], first["label"])
    return head + rest


def _channels(s):
    c = s.get("channels")
    if not c:
        return ""
    # Balken sind Punktreihen: jede Zeile 25 Punkte, der Bestwert Lime (brand.js fuellt beim Ankommen)
    return ('      <div>\n'
            '        <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:20px">%s</span>\n'
            '%s\n'
            '        <p class="dotnote">%s</p>\n'
            '      </div>\n') % (c["label"], kpi_dotrows(_reihen(c["rows"])), c["note"])


def _quote(s):
    q = s.get("quote")
    if not q:
        return ""
    return ('      <div class="qbox" data-fade>\n'
            '        <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:18px">Eine Stimme</span>\n'
            '        <p class="qt">&bdquo;%s&ldquo;</p>\n'
            '        <div class="qa">%s</div>\n'
            '      </div>\n') % (q["text"], q["wer"])


def _fit(s):
    f = s.get("fit")
    if not f:
        return ""
    yes = "\n            ".join("<li>%s</li>" % x for x in f["yes"])
    no = "\n            ".join("<li>%s</li>" % x for x in f["no"])
    head = _zeilen(f["h"] if isinstance(f["h"], list) else [f["h"]])
    cap = ('      <div class="fitcap" data-fade>\n'
           '        <span class="fcnum">%s</span>\n'
           '        <span class="fctxt">%s</span>\n'
           '      </div>\n') % (f.get("cap_v", ""), f.get("cap_t", "")) if f.get("cap_t") and f.get("cap_v") else ""
    if s.get("flow") == "v2":
        # Zwei Karten, eine hell, eine dunkel: der Ja-Nein-Kontrast ist die Form, nicht zwei gleiche Listen
        yes2 = "\n            ".join('<li><i class="fdot"></i>%s</li>' % x for x in f["yes"])
        no2 = "\n            ".join('<li><i class="fdot fdot--no"></i>%s</li>' % x for x in f["no"])
        return ('  <!-- GEGENSEITIGE PRUEFUNG, ZWEI KARTEN -->\n'
                '  <section class="sec fg-light bg-paper fitsec" data-bg="#F3EDE1" data-fg="dark">\n'
                '    <div class="wrap">\n'
                '      <div class="fithead fithead--v2">\n'
                '        <div>\n'
                '          <div class="actring" aria-hidden="true"></div>\n'
                '          <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:clamp(16px,1.8vw,24px)">%s</span>\n'
                '          <h2 class="dispn fitH" data-lines>' + head + '</h2>\n'
                '        </div>\n'
                '        <p class="fitlead" data-fade>%s</p>\n'
                '      </div>\n'
                '      <div class="fitcards" data-stagger>\n'
                '        <div class="fcard fcard--yes" data-fade><div class="fh">%s</div>\n          <ul>\n            %s\n          </ul>\n        </div>\n'
                '        <div class="fcard fcard--no" data-fade><div class="fh">%s</div>\n          <ul>\n            %s\n          </ul>\n        </div>\n'
                '      </div>\n'
                '    </div>\n  </section>\n\n') % (f.get("label", "Bevor wir starten"), f["intro"],
           f.get("yes_h", "Wir passen zusammen, wenn"), yes2,
           f.get("no_h", "Wir sind die Falschen, wenn"), no2)
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
        '        </div>' % (r["wann"], r["titel"], r["text"])
        for r in n["rows"])
    return ('  <!-- WAS ALS NAECHSTES PASSIERT (dunkles Kapitel, Zeilen werden beim Scrollen aktiv) -->\n'
            '  <section class="sec fg-dark nextsec" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">\n'
            '    <div class="wrap">\n'
            '      <span class="label" style="color:var(--champ);display:block;margin-bottom:clamp(24px,3vw,40px)">Was als Nächstes passiert</span>\n'
            '      <h2 class="dispn" data-lines style="font-size:clamp(32px,3.8vw,62px);margin-bottom:clamp(36px,4.4vw,60px)"><span class="rl"><span>%s</span></span></h2>\n'
            '      <div class="oplist oplist--steps">\n        %s\n      </div>\n'
            '    </div>\n  </section>\n\n') % (n["h"], rows)


PROOF_HEAD = """  <!-- 06, PROOF 2: ERGEBNISSE -->
  <section id="beweis" class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">
    <div class="wrap" style="max-width:1100px">
      <div class="actring" aria-hidden="true" style="margin:0 auto 26px"></div>
      <span class="label" style="color:var(--champ-deep);display:block;text-align:center">{proof_label}</span>
      <h2 class="dispn" data-lines style="font-size:clamp(36px,4.6vw,78px);text-align:center;margin-top:22px">
        <span class="rl"><span>{h0}</span></span>
        <span class="rl"><span><i style="font-style:italic">{h1}</i></span></span>
      </h2>
{rest}
    </div>
  </section>

"""

SOL_ACC = """  <!-- 03, LÖSUNG: INTRO + AKKORDEON -->
  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(30px,4vw,60px)">
    <div class="wrap svc-split">
      <div class="intro">
        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:20px">{sol_label}</span>
        <p class="serif" data-scrub>{intro}</p>
      </div>
      <div class="acc">
        {acc}
      </div>
    </div>
  </section>

"""

DIFF_BLOCK = """  <!-- 04, WAS WIR ANDERS MACHEN (BiA-Split: links sticky, rechts Text) -->
  <section class="sec diffsec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">
    <div class="wrap">
      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(40px,5vw,70px)">Was wir anders machen</span>
      <div class="dgrid">
        <div class="dleft">
          <div class="dnum">01</div>
          <div class="dimg">
            {dimgs}
          </div>
        </div>
        <div class="dright">
          {dblocks}
        </div>
      </div>
    </div>
  </section>

"""


def _problem(s):
    """Akt 1: Spannung. Raster nach dem Vorbild functn: Trennlinie, Headline links, Text rechts."""
    p = s.get("problem")
    if not p or not p[0]:
        return ""
    head = _zeilen(s.get("problem_h", ["Das Problem"]))
    return ('  <!-- AKT 1: DAS PROBLEM -->\n'
            '  <section id="problem" class="dotzoom sec fg-dark kapsec kapsec--dark" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">\n'
            '    <div class="wrap">\n'
            '      <div class="lchap">\n'
            '        <div>\n'
            '          <div class="actring" aria-hidden="true"></div>\n'
            '          <span class="label" style="color:var(--champ);display:block;margin-bottom:16px">%s</span>\n'
            '          <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)">%s</h2>\n'
            '        </div>\n'
            '        <div data-stagger>\n'
            '          <p class="lt3" data-fade>%s</p>\n'
            '          <p class="lt3" data-fade>%s</p>\n'
            '        </div>\n'
            '      </div>\n'
            '    </div>\n  </section>\n\n') % (s.get("problem_label", "Die Ausgangslage"), head, p[0], p[1])


def _bene(s):
    """Akt 1: These plus sechs Nutzen-Kacheln, je ein Satz. Ersetzt die zweite Erklaerebene."""
    b = s.get("bene")
    if not b:
        return ""
    head = _zeilen(s.get("bene_h", ["Was Sie davon haben"]))
    cells = "\n        ".join(
        '<div class="bcell" data-fade><div class="bt">%s</div><p class="bd">%s</p></div>' % (x["titel"], x["text"]) for x in b)
    return ('  <!-- AKT 1: THESE UND NUTZEN -->\n'
            '  <section id="nutzen" class="sec fg-light bg-cream" data-bg="#EFE7D6" data-fg="dark">\n'
            '    <div class="wrap">\n'
            '      <div class="benehead">\n'
            '        <div>\n'
            '          <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">%s</span>\n'
            '          <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)">%s</h2>\n'
            '        </div>\n'
            '        <p class="serif benelead" data-scrub>%s</p>\n'
            '      </div>\n'
            '      <div class="benegrid" data-stagger>\n        %s\n      </div>\n'
            '    </div>\n  </section>\n\n') % (s.get("bene_label", "Was dabei herauskommt"), head, s["intro"], cells)


def _detail(s):
    """Akt 4: die Leistungstiefe als Raster aus vier Karten (Titel, ein Satz, vier Punkte).
    Am Telefon eine Reihe zum Wischen. Kein zweites Akkordeon vor der FAQ."""
    items = s.get("acc") or []
    if not items:
        return ""
    cells = []
    for i, a in enumerate(items):
        li = "\n              ".join("<li>%s</li>" % x for x in a["punkte"])
        cells.append('<div class="dcell" data-fade>\n            <span class="dnum">0%d</span>\n            <div class="dt">%s</div>\n            <p>%s</p>\n            <ul>\n              %s\n            </ul>\n          </div>' % (i + 1, a["titel"], a["text"], li))
    return ('  <!-- AKT 4: LEISTUNG IM DETAIL, VIER KARTEN -->\n'
            '  <section class="sec fg-light bg-cream detsec" data-bg="#EFE7D6" data-fg="dark">\n'
            '    <div class="wrap">\n'
            '      <div class="dethead">\n'
            '        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Im Detail</span>\n'
            '        <h2 class="dispn" data-lines style="font-size:clamp(28px,2.8vw,44px)">'
            '<span class="rl"><span>Was dazugehört,</span></span>'
            '<span class="rl"><span>wenn Sie es genau wissen wollen.</span></span></h2>\n'
            '      </div>\n'
            '      <div class="detgrid" data-stagger>\n          ' + "\n          ".join(cells) + '\n      </div>\n'
            '    </div>\n  </section>\n\n')


def _pmap(s):
    """Prozess-Schema am Anfang der Leistungsseite: was von Ihnen kommt, was wir tun, was Sie bekommen.
    Zwei SVGs aus denselben Daten: quer fuer den Desktop, hochkant fuers Telefon. Linien zeichnen sich
    beim Scrollen (master.js), Impulse laufen und die Verben im Kern wechseln als Schleife (SMIL)."""
    pm = s.get("pmap")
    if not pm:
        return ""
    slug = s["slug"].replace("service-", "")
    ins = pm["inputs"]                     # je Eingang: text (lang), kurz, von ("sie" | "wir")
    eng = pm["engine"]                     # title, loop=[...]
    out = pm["output"]                     # titel, text (| als Zeilenumbruch), tag
    touch = pm["touch"]
    words = eng["loop"]
    n = len(words)

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;")

    def loopwords(x, y, size, anchor="start"):
        parts = []
        for i, w in enumerate(words):
            t0, t1 = i / n, (i + 1) / n
            kt = "0;%.3f;%.3f;%.3f;%.3f;1" % (max(t0 - 0.03, 0), t0, max(t1 - 0.03, t0), min(t1, 1))
            parts.append('<text class="pw" x="%d" y="%d" font-size="%d" text-anchor="%s" opacity="0">%s'
                         '<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="%s" dur="%ds" repeatCount="indefinite"/></text>'
                         % (x, y, size, anchor, esc(w), kt, n * 2))
        return "".join(parts)

    def pulse(pid, dur, begin, r=3):
        return ('<circle class="pp" r="%s"><animateMotion dur="%ss" begin="%ss" repeatCount="indefinite"><mpath href="#%s"/></animateMotion></circle>'
                % (r, dur, begin, pid))

    def ring(cx, cy, r):
        return ('<g class="pring"><circle cx="%d" cy="%d" r="%d" class="pr1"/>'
                '<circle cx="%d" cy="%d" r="%d" class="pr2"><animateTransform attributeName="transform" type="rotate" from="0 %d %d" to="360 %d %d" dur="16s" repeatCount="indefinite"/></circle>'
                '<circle cx="%d" cy="%d" r="2.2" class="prd"/></g>' % (cx, cy, r, cx, cy, r + 5, cx, cy, cx, cy, cx, cy))

    # ---------- Desktop, quer ----------
    # Etiketten laenger als 24 Zeichen passen nicht in die Pille, dann gilt die Kurzform
    W, H = 1200, 600
    pw, ph, px0 = 250, 50, 20
    gap = 28
    tot = len(ins) * ph + (len(ins) - 1) * gap
    y0 = (H - tot) / 2
    bus = 340
    d = []
    cys = []
    for i, e in enumerate(ins):
        lang, kurz, who = e["text"], e["kurz"], e["von"]
        lab = lang if len(lang) <= 24 else kurz
        cy = y0 + ph / 2 + i * (ph + gap)
        cys.append(cy)
        d.append('<g class="pn" data-at="%.2f"><rect x="%d" y="%.1f" width="%d" height="%d" rx="%d" class="pill"/>'
                 '<circle cx="%d" cy="%.1f" r="4.5" class="dot dot-%s"/><text x="%d" y="%.1f" font-size="15.5" class="pt">%s</text></g>'
                 % (0.02 + i * 0.03, px0, cy - ph / 2, pw, ph, ph // 2, px0 + 22, cy, who, px0 + 38, cy + 5.5, esc(lab)))
    first, last = cys[0], cys[-1]
    for i, cy in enumerate(cys):
        pid = "d-%s-in%d" % (slug, i)
        if i == 0:
            path = "M%d,%.1f H%d a22,22 0 0 1 22,22" % (px0 + pw, cy, bus - 22)
        elif i == len(cys) - 1:
            path = "M%d,%.1f H%d a22,22 0 0 0 22,-22" % (px0 + pw, cy, bus - 22)
        else:
            path = "M%d,%.1f H%d" % (px0 + pw, cy, bus)
        d.append('<path id="%s" d="%s" class="pl" data-draw data-s="0.05" data-e="0.35"/>' % (pid, path))
    d.append('<path id="d-%s-bus" d="M%d,%.1f V%.1f" class="pl" data-draw data-s="0.2" data-e="0.42"/>' % (slug, bus, first + 22, last - 22))
    mid = (first + last) / 2
    ex, ew, eh = 420, 300, 220
    ey = mid - eh / 2
    d.append('<path id="d-%s-e" d="M%d,%.1f H%d" class="pl" data-draw data-s="0.4" data-e="0.55"/>' % (slug, bus, mid, ex))
    # Kern
    d.append('<g class="pn pcore" data-at="0.52"><rect x="%d" y="%.1f" width="%d" height="%d" rx="20" class="card"/>' % (ex, ey, ew, eh))
    d.append(ring(ex + 36, int(ey + 36), 10))
    d.append('<text x="%d" y="%.1f" font-size="14" class="pt pb">ad.boutique</text>' % (ex + 58, ey + 41))
    d.append('<rect x="%d" y="%.1f" width="44" height="22" rx="11" class="tagw"/><text x="%d" y="%.1f" font-size="10" text-anchor="middle" class="ptw">WIR</text>' % (ex + ew - 66, ey + 25, ex + ew - 44, ey + 40))
    d.append('<text x="%d" y="%.1f" font-size="17" class="pt pb">%s</text>' % (ex + 28, ey + 104, esc(eng["title"])))
    d.append('<path d="M%d,%.1f H%d" class="pl thin"/>' % (ex + 28, ey + 126, ex + ew - 28))
    d.append(loopwords(ex + 28, int(ey + 166), 20))
    d.append('<text x="%d" y="%.1f" font-size="10.5" text-anchor="end" class="pt pg">Schleife, jede Woche</text></g>' % (ex + ew - 28, ey + eh - 20))
    ox, ow, oh = 910, 280, 200
    oy = mid - oh / 2
    d.append('<path id="d-%s-o" d="M%d,%.1f H%d" class="pl" data-draw data-s="0.55" data-e="0.75"/>' % (slug, ex + ew, mid, ox))
    # Impulse liegen unter Pille und Karte, damit kein Punkt ueber Text laeuft (sichtbar erst mit Klasse live)
    d.append(pulse("d-%s-in1" % slug, 2.4, 0))
    d.append(pulse("d-%s-in4" % slug, 2.4, 1.1))
    d.append(pulse("d-%s-e" % slug, 1.6, 0.6))
    d.append(pulse("d-%s-o" % slug, 2.2, 1.4))
    # Beruehrungspunkt mit dem Kunden auf der Verbindung
    tx = (ex + ew + ox) / 2
    tw = 40 + len(touch) * 6.2
    d.append('<g class="pn ptouch" data-at="0.7"><rect x="%.1f" y="%.1f" width="%.1f" height="30" rx="15" class="pill dashed"/>'
             '<circle cx="%.1f" cy="%.1f" r="4" class="dot dot-sie"/><text x="%.1f" y="%.1f" font-size="11" class="pt">%s</text></g>'
             % (tx - tw / 2, mid - 15, tw, tx - tw / 2 + 15, mid, tx - tw / 2 + 27, mid + 4, esc(touch)))
    # Ergebnis
    sub_lines = out["text"].split("|")
    d.append('<g class="pn pout" data-at="0.78"><rect x="%d" y="%.1f" width="%d" height="%d" rx="20" class="card dashed"/>' % (ox, oy, ow, oh))
    d.append('<text x="%d" y="%.1f" font-size="16.5" class="pt pb">%s</text>' % (ox + 24, oy + 44, esc(out["titel"])))
    for j, ln in enumerate(sub_lines):
        d.append('<text x="%d" y="%.1f" font-size="13" class="pt pg">%s</text>' % (ox + 24, oy + 72 + j * 20, esc(ln.strip())))
    tgw = 40 + len(out["tag"]) * 6.2
    d.append('<rect x="%d" y="%.1f" width="%.1f" height="30" rx="15" class="pill"/><circle cx="%d" cy="%.1f" r="4" class="dot dot-sie"/>'
             '<text x="%d" y="%.1f" font-size="11" class="pt">%s</text></g>' % (ox + 24, oy + oh - 54, tgw, ox + 39, oy + oh - 39, ox + 51, oy + oh - 35, esc(out["tag"])))
    svg_d = '<svg class="pmap-d" viewBox="0 0 %d %d" aria-hidden="true">%s</svg>' % (W, H, "".join(d))

    # ---------- Telefon, hochkant ----------
    MW = 390
    mpw, mph, mgap, mx0 = 204, 40, 14, 14
    mbus = 258
    m = []
    mcys = []
    my0 = 16
    for i, e in enumerate(ins):
        kurz, who = e["kurz"], e["von"]
        cy = my0 + mph / 2 + i * (mph + mgap)
        mcys.append(cy)
        m.append('<g class="pn" data-at="%.2f"><rect x="%d" y="%.1f" width="%d" height="%d" rx="%d" class="pill"/>'
                 '<circle cx="%d" cy="%.1f" r="3.5" class="dot dot-%s"/><text x="%d" y="%.1f" font-size="12.5" class="pt">%s</text></g>'
                 % (0.02 + i * 0.03, mx0, cy - mph / 2, mpw, mph, mph // 2, mx0 + 18, cy, who, mx0 + 31, cy + 4.5, esc(kurz)))
    mfirst, mlast = mcys[0], mcys[-1]
    for i, cy in enumerate(mcys):
        pid = "m-%s-in%d" % (slug, i)
        if i == 0:
            path = "M%d,%.1f H%d a16,16 0 0 1 16,16" % (mx0 + mpw, cy, mbus - 16)
        else:
            path = "M%d,%.1f H%d" % (mx0 + mpw, cy, mbus)
        m.append('<path id="%s" d="%s" class="pl" data-draw data-s="0.05" data-e="0.35"/>' % (pid, path))
    mex, mey, mew, meh = 14, mlast + 46, MW - 28, 140
    m.append('<path id="m-%s-bus" d="M%d,%.1f V%.1f a16,16 0 0 1 -16,16 H%d a16,16 0 0 0 -16,16 V%d" class="pl" data-draw data-s="0.2" data-e="0.5"/>'
             % (slug, mbus, mfirst + 16, mey - 44, MW / 2 + 16, mey))
    m.append('<g class="pn pcore" data-at="0.5"><rect x="%d" y="%d" width="%d" height="%d" rx="16" class="card"/>' % (mex, mey, mew, meh))
    m.append(ring(mex + 28, mey + 28, 8))
    m.append('<text x="%d" y="%d" font-size="12" class="pt pb">ad.boutique</text>' % (mex + 46, mey + 32))
    m.append('<rect x="%d" y="%d" width="36" height="18" rx="9" class="tagw"/><text x="%d" y="%d" font-size="9" text-anchor="middle" class="ptw">WIR</text>' % (mex + mew - 50, mey + 19, mex + mew - 32, mey + 31.5))
    m.append('<text x="%d" y="%d" font-size="15" class="pt pb">%s</text>' % (mex + 20, mey + 74, esc(eng["title"])))
    m.append('<path d="M%d,%d H%d" class="pl thin"/>' % (mex + 20, mey + 90, mex + mew - 20))
    m.append(loopwords(mex + 20, mey + 118, 15))
    m.append('<text x="%d" y="%d" font-size="10" text-anchor="end" class="pt pg">Schleife, jede Woche</text></g>' % (mex + mew - 20, mey + 118))
    moy = mey + meh + 76
    m.append('<path id="m-%s-o" d="M%d,%d V%d" class="pl" data-draw data-s="0.55" data-e="0.75"/>' % (slug, MW // 2, mey + meh, moy))
    m.append(pulse("m-%s-in2" % slug, 2.2, 0, 2.6))
    m.append(pulse("m-%s-bus" % slug, 2.6, 0.8, 2.6))
    m.append(pulse("m-%s-o" % slug, 1.8, 1.2, 2.6))
    ttw = 40 + len(touch) * 6.0
    m.append('<g class="pn ptouch" data-at="0.7"><rect x="%.1f" y="%d" width="%.1f" height="28" rx="14" class="pill dashed"/>'
             '<circle cx="%.1f" cy="%d" r="3.5" class="dot dot-sie"/><text x="%.1f" y="%d" font-size="11" class="pt">%s</text></g>'
             % (MW / 2 - ttw / 2, mey + meh + 24, ttw, MW / 2 - ttw / 2 + 14, mey + meh + 38, MW / 2 - ttw / 2 + 25, mey + meh + 42, esc(touch)))
    moh = 150
    m.append('<g class="pn pout" data-at="0.78"><rect x="%d" y="%d" width="%d" height="%d" rx="16" class="card dashed"/>' % (mex, moy, mew, moh))
    m.append('<text x="%d" y="%d" font-size="14.5" class="pt pb">%s</text>' % (mex + 20, moy + 36, esc(out["titel"])))
    for j, ln in enumerate(sub_lines):
        m.append('<text x="%d" y="%d" font-size="12" class="pt pg">%s</text>' % (mex + 20, moy + 60 + j * 17, esc(ln.strip())))
    mtgw = 24 + len(out["tag"]) * 6.1
    m.append('<rect x="%d" y="%d" width="%.1f" height="28" rx="14" class="pill"/><circle cx="%d" cy="%d" r="3.5" class="dot dot-sie"/>'
             '<text x="%d" y="%d" font-size="11" class="pt">%s</text></g>' % (mex + 20, moy + moh - 46, mtgw, mex + 34, moy + moh - 32, mex + 45, moy + moh - 28, esc(out["tag"])))
    MH = moy + moh + 16
    svg_m = '<svg class="pmap-m" viewBox="0 0 %d %d" aria-hidden="true">%s</svg>' % (MW, MH, "".join(m))

    head = _zeilen(pm["h"])
    return ('  <!-- PROZESS-SCHEMA: was von Ihnen kommt, was wir tun, was Sie bekommen -->\n'
            '  <section class="sec fg-light bg-paper pmapsec" data-bg="#F3EDE1" data-fg="dark">\n'
            '    <div class="wrap">\n'
            '      <div class="lchap pmaphead">\n'
            '        <div>\n'
            '          <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">' + pm.get("label", "So läuft es") + '</span>\n'
            '          <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)">' + head + '</h2>\n'
            '        </div>\n'
            '        <p class="lt3" data-fade>' + pm["t"] + '</p>\n'
            '      </div>\n'
            '      <div class="pmap">\n        ' + svg_d + '\n        ' + svg_m + '\n'
            '        <div class="pmap-legend" data-fade><span><i class="dot-sie"></i>Kommt von Ihnen</span><span><i class="dot-wir"></i>Machen wir</span><span><i class="dot-out"></i>Bekommen Sie</span></div>\n'
            '      </div>\n'
            '    </div>\n  </section>\n\n')


def _dotline(s):
    """Arbeitsweise als Punktzeile unter dem Hero-Text, im Duktus des Boards ("strategie. creative. digital. growth.").
    Derzeit nicht eingebunden (der Woerterbuch-Hero hat keine Punktzeile), die Daten (dotline) bleiben in der Datei."""
    words = s.get("dotline") or [w.lower() for w in s.get("pmap", {}).get("engine", {}).get("loop", [])]
    if not words:
        return ""
    return '      <div class="dotline" data-fade style="--i:1">' + "".join("<span>%s</span>" % w for w in words) + "</div>\n"


def _dotfield(s):
    """Punktfeld im Hero: echte Einheiten, Lime-Anteil, antippbar zur Zahl.
    Derzeit nicht eingebunden (Woerterbuch-Hero), die Daten (dotfield) bleiben in der Datei."""
    f = s.get("dotfield")
    if not f:
        return ""
    return ('      <div class="dotfield-wrap" data-fade style="--i:3">\n'
            '        <canvas class="dotfield" data-total="%d" data-lime="%d" data-form="%s" aria-label="%d Punkte, %d davon in Lime"></canvas>\n'
            '        <p class="dotfield-cap">%s<span class="dothint">Antippen</span></p>\n'
            '      </div>\n') % (f["total"], f["lime"], f.get("form", str(f["lime"])), f["total"], f["lime"], f["cap"])


def _tline(s):
    """Zeitleiste im Ablauf: Tage oder Schritte als Punkte, Abschnitte aus data-seg."""
    t = s.get("tline")
    if not t:
        return ""
    leg = "".join('<span><i class="tl-%s"></i>%s</span>' % (x["code"], x["text"]) for x in t["legend"])
    return ('      <div class="tline" data-fade>\n'
            '        <div class="tldots" data-seg="%s" aria-label="%s"></div>\n'
            '        <div class="tllegend">%s</div>\n'
            '      </div>\n') % (t["seg"], t.get("aria", "Zeitleiste als Punkte"), leg)


def _dotsec(s):
    """Punkt-Graphen vor den Cases: jede Einheit ein Punkt."""
    d = s.get("dotsec")
    if not d:
        return ""
    rows = ""
    for block in d["blocks"]:
        rows += '        <div class="dotbars" data-fade>\n'
        for r in block["rows"]:
            rows += '          <div class="row%s"><span class="rl">%s</span><span class="dots" data-n="%d" data-on="%d"></span><span class="rv">%s</span></div>\n' % (
                " hi" if r["hervorgehoben"] else "", r["label"], r["punkte"], r["an"], r["wert"])
        rows += '        </div>\n        <p class="dotnote" data-fade>%s</p>\n' % block["note"]
    head = _zeilen(d["h"])
    return ('  <!-- PUNKT-GRAPHEN: jede Einheit ein Punkt -->\n'
            '  <section class="sec fg-light bg-paper dotsec" data-bg="#F3EDE1" data-fg="dark">\n'
            '    <div class="wrap lchap">\n'
            '      <div>\n'
            '        <span class="label" style="color:var(--champ-deep);display:block;margin-bottom:16px">Punkt für Punkt</span>\n'
            '        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)">' + head + '</h2>\n'
            '        <p class="lt3" data-fade style="margin-top:22px">' + d["t"] + '</p>\n'
            '      </div>\n'
            '      <div>\n' + rows + '      </div>\n'
            '    </div>\n  </section>\n\n')


def _svcband(s):
    """Bildband als Auflockerung zwischen zwei Textbloecken: laeuft von selbst, also auch am Telefon."""
    b = s.get("band")
    if not b:
        return ""
    items = "".join('<img loading="lazy" decoding="async" src="%s" alt="Material, das läuft: Sujet aus einem Mandat">' % x for x in b["imgs"])
    return ('  <!-- BILDBAND -->\n'
            '  <section class="svcband fg-dark" data-bg="#0E0E10" data-fg="light" style="background:#0E0E10">\n'
            '    <div class="wrap"><span class="label" style="color:var(--champ)">%s</span></div>\n'
            '    <div class="svcbandrow" data-speed="5">\n'
            '      <div class="svcbandtrack pwtrack">%s</div>\n'
            '      <div class="svcbandtrack pwtrack" aria-hidden="true">%s</div>\n'
            '    </div>\n  </section>\n\n') % (b.get("label", "Aus dem Studio"), items, items)


def _stoer(s):
    """Stoerer vor dem Angebot (Dramaturgie v1): ein Bild, ein Satz zur Risikoumkehr, dunkel gesetzt."""
    z = s.get("stoer")
    if not z:
        return ""
    pos = "left:clamp(24px,6vw,110px)" if z["side"] == "right" else "right:clamp(24px,6vw,110px)"
    ah = _zeilen(z["ah"])
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
    blink = ('        <a class="zalink" href="%s">%s</a>\n' % _link(b["link"])) if b.get("link") else ""
    solo = "" if s.get("tell") else " barsblock--solo"
    return ('      <div class="barsblock%s">\n'
            '        <span class="label bt">%s</span>\n'
            '%s\n'
            '        <p class="dotnote">%s</p>\n'
            '%s'
            '      </div>\n') % (solo, b["label"], kpi_dotrows(_reihen(b["rows"])), b["note"], blink)


def _crew(s):
    c = s.get("crew")
    if not c:
        return ""
    cells = "\n        ".join(
        '<div class="pcell" data-fade style="--i:%d">\n'
        '          <div class="pportrait" data-scale><img loading="lazy" decoding="async" src="%s" alt="%s"></div>\n'
        '          <div class="pname"><b>%s</b><span>%s</span></div>\n'
        '          <p class="prole">%s</p>\n'
        '        </div>' % (i, p["bild"], p["name"], p["name"], p["rolle"], p["text"])
        for i, p in enumerate(c["people"]))
    head = _zeilen(c["h"], "\n        ")
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
        media = ('      <div class="vmedia" data-fade><span data-scale><img loading="lazy" decoding="async" src="%s" alt="Kundenstimme"></span></div>\n'
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


def _more_cases(weitere):
    """Zeile "Auch mit dieser Leistung" unter den Cases: (href, titel) der weiteren Cases."""
    if not weitere:
        return ""
    return ('      <p class="morecases" data-fade><span>Auch mit dieser Leistung</span>'
            + "".join('<a href="%s">%s</a>' % (h, t) for h, t in weitere) + '</p>\n')


def _visual(s):
    """Visual vor dem Beweis: panels (Screens scrollen vorbei), phones (Telefone ziehen vorbei) oder stage (ein Bild)."""
    vd = s["visual"]
    vkind = vd["art"]
    if vkind == "panels":
        imgs = vd["imgs"]
        col1 = "\n          ".join('<img loading="lazy" decoding="async" src="%s" alt="Gebauter Auftritt aus einem Mandat">' % i for i in imgs[0::2])
        col2 = "\n          ".join('<img loading="lazy" decoding="async" src="%s" alt="Gebauter Auftritt aus einem Mandat">' % i for i in imgs[1::2])
        d1 = vd.get("d1") or {"titel": "Leistungen", "text": ""}
        d2 = vd.get("d2") or {"titel": "Ergebnis", "text": ""}
        return '''  <!-- PROOF, PANELS (Editorial, Screens scrollen vorbei) -->
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
       d1["titel"], d1["text"], d2["titel"], d2["text"],
       col1, col2)
    if vkind == "phones":
        screens = vd["phones"]
        if screens and isinstance(screens[0], list):
            screens = [x for grp in screens for x in grp]
        colA = screens[0::2]; colB = screens[1::2]

        def _pc(items, speed):
            def _pf(src):
                if src.endswith(".mp4"):
                    return '<div class="phframe"><video data-auto muted loop playsinline preload="none" src="%s"></video></div>' % src
                return '<div class="phframe"><img loading="lazy" decoding="async" src="%s" alt="Sujet aus einem Mandat, mobil"></div>' % src
            fr = "\n          ".join(_pf(i) for i in items)
            return '<div class="phcol" data-drift="%s">\n          %s\n        </div>' % (speed, fr)
        phh_lines = _zeilen(vd["h"] if isinstance(vd["h"], list) else [vd["h"]])
        return '''  <!-- PROOF, PHONES (Screens ziehen vorbei) -->
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
    return '''  <!-- PROOF, STAGE -->
  <section class="fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding: 0 0 clamp(110px,14vw,200px)">
    <div class="wrap">
      <div class="stage" data-fade><img loading="lazy" decoding="async" src="%s" alt="Aus dem Mandat"></div>
      <p data-fade style="font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--grey-dark);margin-top:16px">%s</p>
    </div>
  </section>

''' % (vd["img"], vd["cap"])


def _v1_loesung(s):
    """Dramaturgie v1: Intro mit Akkordeon, danach "Was wir anders machen" (Differenzierung mit Bildern)."""
    acc_items = []
    for a in s["acc"]:
        li = "\n              ".join("<li>%s</li>" % x for x in a["punkte"])
        acc_items.append('''<div class="aitem">
          <button class="ahead">%s <span class="plus">+</span></button>
          <div class="abody"><div class="abody-in">
            <p>%s</p>
            <ul>
              %s
            </ul>
          </div></div>
        </div>''' % (a["titel"], a["text"], li))
    acc = "\n        ".join(acc_items)
    dimgs = "\n            ".join(
        '<img loading="lazy" decoding="async" src="%s" alt="Aus der Agentur" class="%s">' % (x["bild"], "on" if i == 0 else "")
        for i, x in enumerate(s["diff"]))
    dblocks = "\n          ".join('''<div class="dblock" data-fade>
            <div class="pk2">%s, 0%d</div>
            <div class="ht2">%s</div>
            <p>%s</p>
          </div>''' % (x["kicker"], i + 1, x["titel"], x["text"]) for i, x in enumerate(s["diff"]))
    return SOL_ACC.format(sol_label=s.get("sol_label", "Die Lösung"), intro=s["intro"], acc=acc) + DIFF_BLOCK.format(dimgs=dimgs, dblocks=dblocks)


def _proofsplit(s, channels_sec, right_sec):
    """Dramaturgie v1: Beleg-Paar, zwei Rechnungen aus zwei Mandaten nebeneinander."""
    if not (s.get("channels") or right_sec):
        return ""
    ps = s.get("proofsplit") or {}
    ps_head = _zeilen(ps.get("h", ["Wo der Unterschied", "wirklich entsteht."]))
    out = ('  <!-- BELEG: ZWEI RECHNUNGEN AUS ZWEI MANDATEN -->\n'
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
    out += (channels_sec or "      <div></div>\n") + (right_sec or "      <div></div>\n")
    out += '      </div>\n    </div>\n  </section>\n\n'
    return out


def render_service(s, hero, faq, weitere, kennzahlen):
    """Die ganze Seite. hero: fertiges Markup des Woerterbuch-Heros, faq: Liste (frage, antwort) in der Reihenfolge
    der Seite, weitere: (href, titel) weiterer Cases mit dieser Leistung, kennzahlen: Board-Dict fuer _kpi.board()
    oder None."""
    z = s["zoom"]
    aside_pos = "left:clamp(24px,6vw,110px)" if z["side"] == "right" else "right:clamp(24px,6vw,110px)"
    nums_sec = ""
    if s.get("proof_nums"):
        nums_sec = ('      <div class="wnums" data-stagger style="justify-content:center;margin-top:clamp(30px,4vw,50px)">\n        %s\n      </div>\n'
                    % "\n        ".join('<div class="n" data-fade><div class="v num serif">%s</div><div class="l">%s</div></div>' % (x["wert"], x["label"]) for x in s["proof_nums"]))
    lead_sec = ""
    if s.get("proof_lead"):
        lead_sec = ('      <p data-fade style="font-family:var(--f-serif);font-size:clamp(17px,1.5vw,22px);line-height:1.6;color:var(--grey-dark);max-width:56ch;margin:clamp(26px,3vw,40px) auto 0;text-align:center">%s</p>\n'
                    % s["proof_lead"])
    visual = _visual(s)
    ops = "\n        ".join('''<a class="op" href="%s" data-fade>
          <span class="onum">0%d</span>
          <span><span class="otitle">%s</span></span>
          <span class="okpi"><span class="v">%s</span><span class="l">%s</span></span>
        </a>''' % (o["href"], i + 1, o["titel"], o["wert"], o["label"]) for i, o in enumerate(s["oplist"]))
    more = _more_cases(weitere)
    cases_sec = ("""  <!-- 07, CASES -->
  <section id="cases" class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark" style="padding-top:clamp(60px,7vw,100px)">
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
        </div>''' % (q["frage"], q["antwort"]) for q in faq)
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
    content_sec = _content_section(s, s.get("content_label", "Aus laufenden Mandaten"))
    content_before = content_sec if s.get("tell") else ""
    content_after = "" if s.get("tell") else content_sec
    zah = "\n          ".join('<span class="rl"><span>%s</span></span>' % x for x in z.get("ah", []))
    zalink = ('<a class="zalink" href="%s">%s</a>' % _link(z["alink"])) if z.get("alink") else ""
    tell_sec = _tell(s)
    channels_sec = _channels(s)
    quote_sec = _quote(s)
    bars_sec = _bars(s)
    pq_sec = "" if s.get("quote") else ('<p class="serif" data-fade style="font-size:clamp(17px,1.4vw,21px);color:var(--grey-dark);max-width:52ch;margin:clamp(30px,4vw,46px) auto 0;text-align:center">%s</p>' % s["proof_quote"])
    # Beleg-Paar: was rechts neben den Kanalzeilen steht
    bars_here = "" if (s.get("tell") and s.get("bars")) else bars_sec
    right_sec = bars_sec if (s.get("tell") and s.get("bars")) else quote_sec
    # Dramaturgie v2: Problem und Nutzen-Kacheln statt Akkordeon und zweiter Erklaerebene,
    # Beweis nur einmal (Stationen), keine zweite Grafikstrecke, keine Stimmungs-Bildwand.
    v2 = s.get("flow") == "v2"
    crew_sec = _crew(s)
    voice_sec = _voice(s)
    fit_sec = _fit(s)
    next_sec = _next(s) + ("" if v2 else _stoer(s))
    if v2:
        next_sec = next_sec.replace('      <div class="oplist oplist--steps">', _tline(s) + '      <div class="oplist oplist--steps">', 1)
        sol_sec = _pmap(s) + _problem(s) + _bene(s) + _svcband(s)
    else:
        sol_sec = _v1_loesung(s)
    deliver_sec = _deliver(s)
    trust_sec = _trust(s)

    # Dramaturgie v2: eine Grafik direkt unter dem Beweis-Kopf statt zwei in einer eigenen Strecke
    graphic_v2 = ('      <div class="proofone">\n' + channels_sec + '      </div>\n') if (v2 and s.get("v2_graphic") and channels_sec) else ""
    # Drei Mandate, drei Spruenge: nach den Stationen (ein Projekt in der Tiefe) die Breite, jede Karte fuehrt in ihren Case
    kpi_sec = kpi_board(kennzahlen, bg="cream") if kennzahlen else ""
    proof_head = PROOF_HEAD.format(
        proof_label=s.get("proof_label", "Ergebnisse"), h0=s["proof_h"][0], h1=s["proof_h"][1],
        rest=nums_sec + lead_sec + pq_sec + bars_here + graphic_v2)
    if v2:
        # Akt 2 Beweis: Karte zeigen, dann einmal beweisen, dann in die Cases weiterfuehren.
        # Akt 3 Vertrauen: erst die Kundenstimme, danach das Team.
        # Farbkette: nach zwei Papier-Bloecken (Kopf, Stationen) wechseln die Cases auf Creme.
        cases_sec = cases_sec.replace('bg-paper" data-bg="#F3EDE1"', 'bg-cream" data-bg="#EFE7D6"')
        # Echtes Mandatsmaterial bleibt im Beweisteil, wo es etwas belegt. Auf der ChatGPT-Seite
        # zeigt das Laufband schon dieselben Studiobilder, dort waere es eine Wiederholung.
        content_v2 = content_sec if s.get("v2_content") else ""
        mid_sec = (visual + content_v2 + proof_head + tell_sec + kpi_sec + _dotsec(s) + cases_sec
                   + voice_sec + crew_sec + logos_sec + fit_sec)
    else:
        mid_sec = (proof_head + tell_sec + kpi_sec + content_before + _proofsplit(s, channels_sec, right_sec) + visual + _wall(s)
                   + crew_sec + voice_sec + cases_sec + logos_sec + content_after + fit_sec)

    faq_sec = ('  <!-- 08, FAQ -->\n'
               '  <section class="sec fg-light bg-paper" data-bg="#F3EDE1" data-fg="dark">\n'
               '    <div class="wrap faq">\n'
               '      <div>\n'
               '        <h2 class="disp" data-lines style="text-transform:none;letter-spacing:-0.02em"><span class="rl"><span>Die ehrlichen</span></span><span class="rl"><span>Fragen.</span></span></h2>\n'
               '        <p class="fint" data-fade>Was uns vor dem Start wirklich gefragt wird, und was wir antworten.</p>\n'
               '      </div>\n'
               '      <div data-stagger>\n        ' + faqs + '\n      </div>\n'
               '    </div>\n  </section>\n\n')
    # v2: nach dem Fit erst der dunkle Ablauf, dann das Detail-Raster, dann die FAQ.
    # Drei Textbloecke gleicher Form hintereinander gibt es so nicht mehr.
    # Die ChatGPT-Seite bleibt so, wie sie freigegeben wurde: dort kein Detail-Raster.
    if v2:
        after_mid = next_sec + (_detail(s) if s.get("v2_content") else "") + faq_sec
    else:
        after_mid = faq_sec + next_sec
    page = HEAD.format(title=s["nav"], bodybg="#F3EDE1") + menu("index.html#leistungen") + '''<main class="apl">


  <!-- 01, HERO (Woerterbuch-Stil, Kundenfreigabe 3.10.2026) -->
''' + hero + '''
''' + sol_sec + '''  <!-- 05, PROOF 1: ZOOM -->
  <section class="zoomsec" data-side="''' + z["side"] + '''" data-bg="#F3EDE1" data-fg="dark">
    <div class="zsticky">
      <div class="zaside fg-light" style="''' + aside_pos + '''">
        <span class="label" style="color:var(--champ-deep)">''' + z.get("al", "Der Beweis") + '''</span>
        <h3 class="zah" data-lines>''' + zah + '''</h3>
        <p class="zasub">''' + z["aside"] + '''</p>
        ''' + zalink + '''
      </div>
      <div class="zmedia"><img src="''' + z["img"] + '''" alt="''' + z["zl"] + '''"></div>
      <div class="zcap">
        <span class="zl">''' + z["zl"] + '''</span>
        <div class="zt">''' + z["zt"] + '''</div>
      </div>
    </div>
  </section>

''' + mid_sec + after_mid + '''  <!-- 09, NO-BRAINER + RISIKOUMKEHR -->
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

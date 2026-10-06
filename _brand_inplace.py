# -*- coding: utf-8 -*-
"""Brand 2026 fuer handgebaute Seiten: Adobe-Fonts-Kit, site.css und site.js in den Kopf,
Seitenklasse, dazu auf Startseite und Agentur die Bausteine (Kapitel-Leiste, Punkt, Punktzeile,
Akt-Ringe, Punkt-Zoom). Mehrfach ausfuehrbar: was da ist, wird nicht doppelt eingesetzt.
Regel "brand" des Nachlaufs (_nachlauf.py), nach "poster", vor "footer". Einzeln aufrufbar: python3 _brand_inplace.py"""
import re

from _anker import einmal, sektion
from _kpi import board as kpi_board, mini as kpi_mini, HAND_KPI

SKIP = ("_qa_template.html",)


def cut_section(h, needle, what):
    """Schneidet die Sektion heraus, die den Anker enthaelt (vom oeffnenden <section bis </section>)."""
    a, b = sektion(h, needle, what)
    return h[:a] + h[b:]


def cnums_to_mini(h):
    """Zahlenreihen der Kapitel in kleine KPI-Karten drehen."""
    def one(m):
        nums = re.findall(r'<div class="l">(.*?)</div><div class="v num serif">(.*?)</div>', m.group(0))
        return kpi_mini(nums).rstrip("\n")
    return re.sub(r'<div class="cnums" data-stagger>.*?\n      </div>', one, h, flags=re.S)


TIGHT_DRIFT = ("0.042", "0.068", "0.05", "0.075", "0.056", "0.072")


def collage_tight(h):
    """Jede schraege Collage in der Referenzgroesse (BRAND-RULES 8): die dreispaltige .collage ohne --tight
    wird zur sechsspaltigen collage--tight wie in "Aus dem Mandat". Die Motive bleiben dieselben und laufen
    reihum durch sechs Spalten mit je fuenf Motiven, damit die Spalten oben und unten aus dem Bild laufen."""
    def one(m):
        items = re.findall(r"<(?:img|video)\b[^>]*>(?:</video>)?", m.group(2))
        if not items:
            return m.group(0)
        cols = []
        for c in range(6):
            pick = [items[(c * 2 + k) % len(items)] for k in range(5)]
            cols.append('      <div class="cpcol" data-drift="%s">\n        %s\n      </div>' % (TIGHT_DRIFT[c], "\n        ".join(pick)))
        return '<section class="collage collage--tight"%s>\n    <div class="cplane">\n%s\n    </div>\n  </section>' % (m.group(1), "\n".join(cols))
    return re.sub(r'<section class="collage"((?: [a-z-]+="[^"]*")*)>\s*<div class="cplane">(.*?)</div>\s*</section>', one, h, flags=re.S)


def funkhaus(h):
    """Original-Funkhaus: KPI-Board nach dem Intro, die alte Ergebnis-Zahlenreihe faellt weg.
    Das Board wird bei jedem Lauf aus der Inhaltsdatei _content/cases/case-premium-neubau.json neu gesetzt,
    damit Aenderungen an den Kennzahlen dort auch auf der handgebauten Seite ankommen."""
    h = collage_tight(h)
    if 'class="kpiboard"' in h:
        h = cut_section(h, 'class="kpiboard"', "Funkhaus Board")
    if 'class="kpiboard"' not in h:
        if '>Ergebnis</span>' in h:
            h = cut_section(h, '>Ergebnis</span>', "Funkhaus Ergebnis")
        h = rep(h, "  <!-- COLLAGE: Creatives", kpi_board(HAND_KPI["case-premium-neubau"]) + "  <!-- COLLAGE: Creatives", "Funkhaus Board")
    return cnums_to_mini(h)


def kommunalkredit(h):
    """Sommergespraeche: Produktion und Stimme als Board nach dem Intro, Kapitel-Zahlen als Mini-Karten."""
    # Board bei jedem Lauf neu aus _content/cases/case-kommunalkredit.json (wie beim Funkhaus)
    if 'class="kpiboard"' in h:
        h = cut_section(h, 'class="kpiboard"', "Kommunalkredit Board")
    if 'class="kpiboard"' not in h:
        h = rep(h, "  <!-- FILM: Recap", kpi_board(HAND_KPI["case-kommunalkredit"]) + "  <!-- FILM: Recap", "Kommunalkredit Board")
    return cnums_to_mini(h)


# Die Seiten laden ein Stylesheet und ein Script: assets/site.css und assets/site.js (gebuendelt von _css.py aus
# tokens.css, master.css, brand.css, brand-type/-ui/-layout/-motion/-keep.css bzw. brand.js und master.js).
# Aeltere Staende mit den Einzeldateien werden umgestellt; das Adobe-Fonts-Kit bleibt direkt hinter site.css.
TYPEKIT = '<link rel="stylesheet" href="https://use.typekit.net/udf8wjj.css">'
OLD_CSS = re.compile(r'\n?<link rel="stylesheet" href="assets/(?:site|master|brand(?:-[a-z]+)?)\.css\?v=(\d+)">')
OLD_JS = re.compile(r'\n?<script src="assets/(?:site|master|brand)\.js\?v=(\d+)" defer></script>')


def site_assets(h):
    """Alle Stylesheet- und Script-Verweise auf assets/ zu je einem Verweis zusammenfassen, an der Stelle des ersten.
    Mehrfach ausfuehrbar: ein schon umgestellter Kopf kommt unveraendert zurueck."""
    ms = list(OLD_CSS.finditer(h))
    if not ms:
        return h
    v = ms[0].group(1)
    h = h[:ms[0].start()] + "\x00CSS\x00" + h[ms[0].end():]
    h = OLD_CSS.sub("", h).replace("\n" + TYPEKIT, "").replace(TYPEKIT, "")
    h = h.replace("\x00CSS\x00", '\n<link rel="stylesheet" href="assets/site.css?v=%s">\n%s' % (v, TYPEKIT), 1)
    js = list(OLD_JS.finditer(h))
    if js:
        h = h[:js[0].start()] + "\x00JS\x00" + h[js[0].end():]
        h = OLD_JS.sub("", h)
        h = h.replace("\x00JS\x00", '\n<script src="assets/site.js?v=%s" defer></script>' % v, 1)
    return h


# Schrift-Hinweise (Technik B2): Verbindung zu Adobe Fonts frueh aufbauen (Kit-CSS plus Zaehl-CSS auf p.typekit.net),
# Satoshi vorladen, statt erst nach dem Lesen von site.css zu entdecken. Stehen direkt vor site.css, jede Zeile genau einmal.
FONT_HINTS = ('<link rel="preconnect" href="https://use.typekit.net" crossorigin>\n'
              '<link rel="preconnect" href="https://p.typekit.net" crossorigin>\n'
              '<link rel="preload" href="assets/fonts/Satoshi-Variable.woff2" as="font" type="font/woff2" crossorigin>\n')
FONT_HINT_RX = re.compile(r'<link rel="(?:preconnect" href="https://(?:use|p)\.typekit\.net"|preload" href="assets/fonts/[^"]+"[^>]*?) crossorigin>\n')


def font_hints(h):
    h = FONT_HINT_RX.sub("", h)
    m = re.search(r'<link rel="stylesheet" href="assets/site\.css', h)
    return h[:m.start()] + FONT_HINTS + h[m.start():] if m else h


def head(h):
    if "assets/site.css" in h or "brand.css" in h:
        return font_hints(site_assets(h))
    if not re.search(r'<link rel="stylesheet" href="assets/master\.css\?v=\d+">', h):
        return h
    h = site_assets(h)
    h = re.sub(r"<body([^>]*)>", lambda mm: ("<body%s class=\"brand\">" % mm.group(1)) if "class=" not in mm.group(1) else ("<body%s>" % mm.group(1).replace('class="', 'class="brand ')), h, count=1)
    return h


def rep(h, old, new, what):
    """Genau ein Treffer, sonst bricht der Build mit Zweck und Anker ab (_anker.AnkerFehlt)."""
    return einmal(h, old, new, what)


def strip_chapnav(h):
    """Kapitel-Leiste abgeschafft (24.9.2026): aus jeder Seite entfernen, auch aus aelteren Staenden."""
    return re.sub(r'\n?  <!-- KAPITEL-LEISTE[^\n]*\n  <nav class="chapnav".*?</nav>\n', '\n', h, flags=re.S)


def index(h):
    # der Hero-Punkt rechts oben unter dem Menue entfaellt (BRAND-RULES 6 und 10), auch aus aelteren Staenden
    h = h.replace('      <span class="bdot" aria-hidden="true"></span>\n', '')
    if 'class="dotline"' in h:
        return h
    h = rep(h, '<span class="rl"><span>Kein Zufall.</span></span>', '<span class="rl"><span><i>Kein Zufall.</i></span></span>', "Hero-Zeile")
    h = rep(h, '<section class="sec fg-light stats bg-paper"', '<section class="sec fg-light stats bg-paper dotzoom dotzoom--dark"', "Punkt-Zoom Zahlen")
    h = rep(h, "<main>", '<main class="apl">', "main")
    h = rep(h, '  <!-- 04, WORK-TEASER -->\n  <section class="sec fg-light bg-paper"', '  <!-- 04, WORK-TEASER -->\n  <section id="work" class="sec fg-light bg-paper"', "Work-ID")
    h = rep(h, '<section class="sec fg-light team-int bg-paper"', '<section id="team" class="sec fg-light team-int bg-paper"', "Team-ID")
    h = rep(h, 'Wir gewinnen nur, wenn Sie gewinnen.</p>\n      <div class="hbtns"',
            'Wir gewinnen nur, wenn Sie gewinnen.</p>\n      <div class="dotline" data-fade style="--i:1"><span>strategie</span><span>creative</span><span>digital</span><span>growth</span></div>\n      <div class="hbtns"', "Punktzeile")
    h = rep(h, '<span class="label">Wofür wir stehen</span>', '<div class="actring" aria-hidden="true"></div>\n      <span class="label">Wofür wir stehen</span>', "Ring These")
    h = rep(h, '<span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(30px,4vw,54px)">Reden wir</span>',
            '<div class="actring" aria-hidden="true"></div>\n      <span class="label" style="color:var(--grey-dark);display:block;margin-bottom:clamp(30px,4vw,54px)">Reden wir</span>', "Ring Kontakt")
    return h


def agentur(h):
    # kein dekorativer Lime-Punkt ueber der Headline (BRAND-RULES 6), auch aus aelteren Staenden
    h = h.replace('<span class="bdot" aria-hidden="true"></span>\n      <h1 class="dispn"', '<h1 class="dispn"')
    if 'id="zahlen"' in h:
        return h
    h = rep(h, "<main>", '<main class="apl">', "main")
    h = rep(h, '<section class="sec fg-light stats bg-paper"', '<section id="zahlen" class="sec fg-light stats bg-paper"', "Zahlen-ID")
    h = rep(h, '  <!-- 03, CAPABILITIES (Creme) -->\n  <section class="sec fg-light bg-cream"', '  <!-- 03, CAPABILITIES (Creme) -->\n  <section id="koennen" class="dotzoom sec fg-light bg-cream"', "Koennen-ID")
    h = rep(h, '<section class="sec fg-light ateam bg-paper"', '<section id="team" class="sec fg-light ateam bg-paper"', "Team-ID")
    h = rep(h, '  <!-- 05, JOIN / WORK (Vorlage: Join us, Work with us) -->\n  <section class="sec fg-light bg-paper"', '  <!-- 05, JOIN / WORK (Vorlage: Join us, Work with us) -->\n  <section id="jobs" class="sec fg-light bg-paper"', "Jobs-ID")
    h = rep(h, '<span class="rl"><span>auf Zahlen gebaut sind.</span></span>', '<span class="rl"><span><i>auf Zahlen gebaut sind.</i></span></span>', "Hero-Kursiv")
    h = rep(h, '<a class="alink" href="work.html" data-fade style="margin-top:30px">Die Beweise ansehen →</a>',
            '<div class="dotline" data-fade style="justify-content:flex-start;margin-top:22px"><span>strategen</span><span>kreative</span><span>performance-nerds</span></div>\n      <a class="alink" href="work.html" data-fade style="margin-top:30px">Die Beweise ansehen →</a>', "Punktzeile")
    h = rep(h, '<div><span class="label" style="color:var(--grey-dark)">Was wir können</span></div>',
            '<div><div class="actring" aria-hidden="true"></div><span class="label" style="color:var(--grey-dark)">Was wir können</span></div>', "Ring Koennen")
    h = rep(h, '<h2 class="dispn" data-lines>\n        <span class="rl"><span>Ein Team aus Strategen, Kreativen</span></span>',
            '<div class="actring" aria-hidden="true" style="margin:0 auto 26px"></div>\n      <h2 class="dispn" data-lines>\n        <span class="rl"><span>Ein Team aus Strategen, Kreativen</span></span>', "Ring Team")
    return h


# ---------- Layout-Abteilung: Raster und Abstaende (BRAND-RULES 3, 8) ----------
# Inline-Abstaende der Sektionen kommen aus vielen Generationen der Seiten (clamp mit vw).
# Hier werden sie auf die Tokens aus assets/brand-layout.css gezogen, damit gleiche Sektionstypen gleich sind:
#   0 bleibt 0, bis 60 px -> --sec-xs (48/32), bis 140 px -> --sec-s (64/48), darueber -> --sec (128/64).
# Ausnahme: Drift-Raster (Work, data-driftsc) behalten ihren Nachlauf-Puffer von 170 px zusaetzlich zu --sec.

def _pad_token(v):
    v = v.strip()
    if v.startswith("var(") or v.startswith("calc(var("):
        return v
    nums = [float(x) for x in re.findall(r"(-?\d+(?:\.\d+)?)px", v)]
    if not nums:
        return "0" if v.strip() in ("0", "0px") else v
    m = max(nums)
    if m <= 0:
        return "0"
    # feste Werte, die schon auf der 8er-Skala liegen, bleiben (z. B. 96 px Platz unter dem Logo auf Work)
    if len(nums) == 1 and "clamp" not in v and m in (8, 16, 24, 32, 48, 64, 96, 128):
        return "%dpx" % m
    if m <= 60:
        return "var(--sec-xs)"
    if m <= 140:
        return "var(--sec-s)"
    return "var(--sec)"


def _split_vals(v):
    """Teilt eine padding-Kurzschreibweise in Werte, ohne Klammern zu zerschneiden."""
    out, depth, cur = [], 0, ""
    for ch in v.strip():
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == " " and depth == 0:
            if cur:
                out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def _norm_style(style, drift=False):
    decls = [d for d in style.split(";") if d.strip()]
    out = []
    for d in decls:
        if ":" not in d:
            out.append(d)
            continue
        k, v = d.split(":", 1)
        key = k.strip()
        if key in ("padding-top", "padding-bottom"):
            t = _pad_token(v)
            out.append("%s:%s" % (key, t))
        elif key == "padding":
            vals = _split_vals(v)
            if len(vals) == 1:
                vals = [vals[0], "0", vals[0]]
            elif len(vals) == 2:
                vals = [vals[0], vals[1], vals[0]]
            top, side, bot = vals[0], vals[1], vals[2]
            if side.strip() not in ("0", "0px"):
                out.append(d)
                continue
            tb = _pad_token(bot)
            # Sektionen mit driftenden Spalten (Work): Abstand bleibt auf der Skala, der Puffer fuer die Drift
            # sitzt in brand-layout.css unter dem Raster (.wgridw). Aeltere Staende mit +170 werden zurueckgefuehrt.
            if tb.replace(" ", "") == "calc(var(--sec)+170px)":
                tb = "var(--sec)"
            out.append("padding:%s 0 %s" % (_pad_token(top), tb))
        else:
            out.append(d)
    return ";".join(x.strip() for x in out)


def layout(h, page=""):
    """Sektionsabstaende und Seitenrand auf die Tokens ziehen. Mehrfach ausfuehrbar (Tokens bleiben Tokens)."""
    def sec(m):
        tag = m.group(0)
        sm = re.search(r'style="([^"]*)"', tag)
        if not sm or "padding" not in sm.group(1):
            return tag
        i = h.find(tag)
        drift = "data-driftsc" in h[i:i + 800]
        return tag.replace(sm.group(0), 'style="%s"' % _norm_style(sm.group(1), drift))
    h = re.sub(r"<section\b[^>]*>", sec, h)
    # Text neben dem Zoom-Bild: Abstand zum Rand ist der Seitenrand
    h = h.replace("left:clamp(24px,6vw,110px)", "left:var(--gut)").replace("right:clamp(24px,6vw,110px)", "right:var(--gut)")
    # Work: das Raster nutzt den Seitenrand statt eines eigenen Randes
    h = h.replace(' style="width:min(1720px,calc(100% - 2 * clamp(20px,3.4vw,64px)))"', "")
    if page != "agentur.html":
        # Bilder im Container: Radius 20 statt 3 (Bildzeilen der Galerien und Karten)
        h = re.sub(r'(<span data-scale[^>]*style="display:block;overflow:hidden;)border-radius:3px', r"\1border-radius:var(--r-img)", h)
    return h


ZAEHLER = {"n": 0}


def seite(f, h):
    """Regel "brand": Kopf, Kapitel-Leiste raus, Bausteine je handgebauter Seite, Abstaende auf die Tokens."""
    # alte Testseiten hiessen *-brand.html; echte Cases wie case-consumer-brand.html gehoeren dazu
    if f in SKIP or (f.endswith("-brand.html") and not f.startswith("case-")):
        return h
    out = strip_chapnav(head(h))
    if f == "index.html":
        out = index(out)
        # das Wort im Menue-Punkt gilt seit 24.9.2026 ueberall (brand.css body.brand), die alte Klasse faellt weg
        out = out.replace('class="mword brand', 'class="brand', 1)
    elif f == "agentur.html":
        out = agentur(out)
    elif f == "case-premium-neubau.html":
        out = funkhaus(out)
    elif f == "case-kommunalkredit.html":
        out = kommunalkredit(out)
    out = layout(out, f)
    if out != h:
        ZAEHLER["n"] += 1
    return out


def bericht():
    return "Brand in %d Seiten eingesetzt" % ZAEHLER["n"]


if __name__ == "__main__":
    import _nachlauf
    _nachlauf.einzeln(seite)
    print(bericht())

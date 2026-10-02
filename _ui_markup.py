# -*- coding: utf-8 -*-
"""Markup-Vereinheitlichung fuer Farben und Komponenten (Regelwerk _intern/BRAND-RULES.md, Abschnitte 1, 5, 6).
Gehoert der Design-Abteilung. Reihenfolge: nach _footer.py, vor _headlines.py. Laeuft ueber alle Seiten.

Was dieser Schritt tut:
  1. Flaechen: jedes data-bg wird genau eine von Cream #F4F3EB, Black #101010, Lime #CDFF00
     (master.js faerbt damit beim Scrollen den Seitengrund). Alte Case-Farbwelten werden Schwarz.
  2. Farben im Markup: Literal-Farben in style-Attributen, <style>-Bloecken und SVG fill/stroke werden auf die
     Tokens abgebildet (hell -> Cream, dunkel -> Black, Lime -> #CDFF00, Transparenzen bleiben Transparenzen).
     Schwarz-Transparenzen (Schatten, Bildverlaeufe) bleiben unveraendert.
  3. Buttons: jedes Button-artige Element bekommt die Klasse "btn" und genau eine der acht Figma-Varianten
     (btn--primary, btn--secondary, btn--accent, btn--inverse, btn--outline-inverse, btn--soft-cream,
     btn--soft-black, btn--soft-lime), passend zum Untergrund (Cream, Schwarz, Lime, Foto).
     Hauptaktion und zweite Aktion werden je Untergrund gepaart wie in Figma 84:13.
  4. Labels (.label): steht direkt danach eine Headline oder ein Display-Satz, ist es ein verbotenes Eyebrow
     und bekommt "lbl-x" (brand-ui.css blendet es aus). Ebenso Labels auf Fotos (Collage "Aus dem Mandat"):
     ein Badge ohne Fuellung ist dort nicht lesbar. Sonst wird es ein Badge ("bdg"), ohne eigene Textfarbe.
  5. Case-Hero: die Kunden- und Branchenzeile (.hcap .cl) stand 10 px ueber der H1. Ihre zwei Teile werden
     zwei Badges (small.bdg); brand-ui.css stellt sie als Meta-Zeile unter die H1.
Mehrfach ausfuehrbar: eigene Klassen werden vor jeder Entscheidung entfernt und neu gesetzt, Farben sind nach dem
ersten Lauf bereits Tokens und bleiben es."""
import glob
import re
from html.parser import HTMLParser

SKIP = ("_qa_template.html",)

CREAM, INK, LIME = (244, 243, 235), (16, 16, 16), (205, 255, 0)
HEX = {CREAM: "#F4F3EB", INK: "#101010", LIME: "#CDFF00"}

# ------------------------------------------------------------------ Farben

COLOR_RX = re.compile(r"(?<![&\w])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b|rgba?\([^)]*\)")


def _parse(s):
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0
    p = [x for x in re.split(r"[\s,/]+", s[s.index("(") + 1:-1].strip()) if x]
    try:
        v = [float(x.rstrip("%")) for x in p]
    except ValueError:
        return None
    return v[0], v[1], v[2], (v[3] if len(v) > 3 else 1.0)


def token_for(r, g, b):
    """Naechster Token: Lime fuer gelbgruene Toene, sonst nach Helligkeit Cream oder Black."""
    if g > 200 and r > 150 and b < 140 and g - b > 80:
        return LIME
    return CREAM if (r + g + b) / 3 >= 140 else INK


def map_color(s):
    c = _parse(s)
    if not c:
        return s
    r, g, b, a = c
    if a == 0:
        return s
    if (r, g, b) == (0, 0, 0) and a < 1:
        return s  # Schatten und Bildverlaeufe
    t = token_for(r, g, b)
    if a >= 1:
        out = HEX[t]
    else:
        out = "rgba(%d,%d,%d,%s)" % (t[0], t[1], t[2], ("%.3f" % a).rstrip("0").rstrip("."))
    return s if out.lower() == s.lower() else out


def map_colors(text):
    return COLOR_RX.sub(lambda m: map_color(m.group(0)), text)


def fix_colors(h):
    # data-bg: genau drei Flaechen
    def bg(m):
        v = m.group(1).strip()
        c = _parse(v) if COLOR_RX.fullmatch(v) else None
        if not c:
            return m.group(0)
        return 'data-bg="%s"' % HEX[token_for(c[0], c[1], c[2])]
    h = re.sub(r'data-bg="([^"]*)"', bg, h)
    # style-Attribute, SVG fill/stroke/stop-color
    h = re.sub(r'(\sstyle=")([^"]*)(")', lambda m: m.group(1) + map_colors(m.group(2)) + m.group(3), h)
    h = re.sub(r"""(\s(?:fill|stroke|stop-color|color)=")([^"]*)(")""", lambda m: m.group(1) + map_colors(m.group(2)) + m.group(3), h)
    # <style>-Bloecke
    h = re.sub(r"(<style\b[^>]*>)(.*?)(</style>)", lambda m: m.group(1) + map_colors(m.group(2)) + m.group(3), h, flags=re.S)
    return h

# ------------------------------------------------------------------ Kontext je Element

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "path",
        "circle", "rect", "line", "polyline", "polygon", "stop", "use", "ellipse"}
# Klassen, deren Inhalt auf einem Foto oder Video liegt
PHOTO = {"chero", "hshow", "cstate", "collage", "wt", "ivid", "vmedia", "filmwrap", "pwiv", "ivframe", "tmed"}
# Link-Paare ohne eigene Klasse (Case-Fotowand, Panel-Scroll): Anfrage = Hauptaktion, alles andere = zweite Aktion
PAIRS = {"pwlinks", "pslinks"}
# Klassen heller Flaechen innerhalb dunkler Sektionen (Startseiten-Hero: rechte Haelfte Cream)
LIGHT = {"hpitch"}
# Klassen dunkler Flaechen ohne eigenes data-fg
DARK = {"fcard--no", "msheet", "tclr", "wclr", "panelscroll", "cwall", "ftr"}
HEADLINE_CLASSES = {"dispn", "disp", "lh", "zah", "pwh", "phh", "kh", "serif", "vq", "kquote", "cwh", "nptit"}


class Scan(HTMLParser):
    """Merkt sich fuer jedes Start-Tag die Position und den Untergrund (cream, dark, lime, photo)."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for ln in src.split("\n"):
            self.lines.append(self.lines[-1] + len(ln) + 1)
        self.stack = []
        self.tags = []  # (offset, tag, attrs, ground, Klassen des Elternelements)

    def ground(self):
        for tag, attrs in reversed(self.stack):
            cls = set((attrs.get("class") or "").split())
            if cls & LIGHT:
                return "cream"
            if cls & PHOTO:
                return "photo"
            if cls & DARK:
                return "dark"
            if attrs.get("data-bg", "").upper() == "#CDFF00":
                return "lime"
            fg = attrs.get("data-fg")
            if fg == "light":
                return "dark"
            if fg == "dark":
                return "cream"
            if "fg-dark" in cls:
                return "dark"
            if "fg-light" in cls:
                return "cream"
        return "cream"

    def parent_cls(self):
        return set((self.stack[-1][1].get("class") or "").split()) if self.stack else set()

    def handle_starttag(self, tag, attrs):
        a = dict((k, v or "") for k, v in attrs)
        off = self.lines[self.getpos()[0] - 1] + self.getpos()[1]
        pc = self.parent_cls()
        self.stack.append((tag, a))
        self.tags.append((off, tag, a, self.ground(), pc))
        if tag in VOID:
            self.stack.pop()

    def handle_startendtag(self, tag, attrs):
        a = dict((k, v or "") for k, v in attrs)
        off = self.lines[self.getpos()[0] - 1] + self.getpos()[1]
        pc = self.parent_cls()
        self.stack.append((tag, a))
        self.tags.append((off, tag, a, self.ground(), pc))
        self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

# ------------------------------------------------------------------ Buttons

MAIN = {"cream": "btn--primary", "lime": "btn--primary", "dark": "btn--inverse", "photo": "btn--inverse"}
SECOND = {"cream": "btn--soft-cream", "lime": "btn--soft-lime", "dark": "btn--soft-black", "photo": "btn--outline-inverse"}
VARIANTS = ("btn--primary", "btn--secondary", "btn--accent", "btn--inverse", "btn--outline-inverse",
            "btn--soft-cream", "btn--soft-black", "btn--soft-lime")
# Klasse -> Rolle. main = Hauptaktion, second = zweite Aktion, accent = Lime-Aktion auf hellem Grund, photo = immer Foto
ROLES = [("btn-i", "main"), ("btn-p", "main"), ("kbtn", "main"), ("btn-o", "second"), ("kback", "second"),
         ("alink", "second"), ("zalink", "second"), ("svc-back", "second"), ("ngo", "accent"), ("ivsound", "photo")]


def variant(cls, ground):
    for c, role in ROLES:
        if c in cls:
            if role == "main":
                return MAIN[ground]
            if role == "second":
                return SECOND[ground]
            if role == "accent":
                return "btn--accent" if ground in ("cream", "lime") else MAIN[ground]
            if role == "photo":
                return "btn--outline-inverse"
    return None


def set_class(tagsrc, fn):
    m = re.search(r'\sclass="([^"]*)"', tagsrc)
    if not m:
        return tagsrc
    cls = m.group(1).split()
    new = fn(cls)
    if new == cls:
        return tagsrc
    return tagsrc[:m.start(1)] + " ".join(new) + tagsrc[m.end(1):]


def fix_components(h):
    sc = Scan(h)
    sc.feed(h)
    sc.close()
    edits = []  # (start, end, neuer Tag-Text)
    for i, (off, tag, a, ground, pcls) in enumerate(sc.tags):
        cls = (a.get("class") or "").split()
        end = h.index(">", off) + 1
        src = h[off:end]
        # Link-Paare ohne Klasse: bekommen eine Rolle (Anfrage = Hauptaktion), danach wie alle Buttons
        if tag == "a" and (pcls & PAIRS) and not any(c for c, _ in ROLES if c in cls):
            role = "btn-i" if ("kontakt" in a.get("href", "") or "anfrage" in a.get("href", "")) else "btn-o"
            if 'class="' not in src:
                src = src[:2] + ' class=""' + src[2:]
            cls = cls + [role]
            src = set_class(src, lambda c, role=role: c + [role] if role not in c else c)
        if not cls:
            continue
        # Buttons (die Footer-Knoepfe der Layout-Abteilung tragen nur ihre Variante, keine Rolle, und bleiben)
        if tag in ("a", "button"):
            v = variant(cls, ground)
            if v:
                def fn(c, v=v):
                    c = [x for x in c if x not in VARIANTS]
                    if "btn" not in c:
                        c.append("btn")
                    c.append(v)
                    return c
                edits.append((off, end, set_class(src, fn)))
                continue
        # Labels: Eyebrow weg oder Badge
        if "label" in cls and "h1-seo" not in cls and tag in ("span", "p", "div"):
            close = h.find("</%s>" % tag, end)
            # naechstes Start-Tag nach dem Label-Ende
            j = i + 1
            while j < len(sc.tags) and sc.tags[j][0] < close:
                j += 1
            nxt = sc.tags[j] if j < len(sc.tags) else None
            eyebrow = False
            if nxt:
                ncls = set((nxt[2].get("class") or "").split())
                if nxt[1] in ("h1", "h2", "h3") or (ncls & HEADLINE_CLASSES):
                    eyebrow = True
                if nxt[1] == "p" and "serif" in ncls:
                    eyebrow = True
            if ground == "photo":
                eyebrow = True

            def fn(c, eyebrow=eyebrow):
                c = [x for x in c if x not in ("lbl-x", "bdg")]
                c.append("lbl-x" if eyebrow else "bdg")
                return c
            new = set_class(src, fn)
            if not eyebrow:
                # eigene Textfarbe (frueher Champagne/Lime) entfaellt, der Badge folgt dem Untergrund
                new = re.sub(r'(\sstyle=")([^"]*)(")',
                             lambda m: m.group(1) + re.sub(r"(?:^|;)\s*color\s*:[^;]*", "", m.group(2)).lstrip(";") + m.group(3), new)
                new = new.replace(' style=""', "")
            edits.append((off, end, new))
    for s, e, t in sorted(edits, reverse=True):
        h = h[:s] + t + h[e:]
    return h


HCAP_CL = re.compile(r'(<div class="hcap">\s*<div class="cl"[^>]*>)([^<]+?)\s*<span(?:\s+style="[^"]*")?>([^<]*)</span>\s*(</div>)')
# Stand aus frueheren Laeufen: die zwei Badges als span.bdg (brand-type.css setzt ".cl span" auf Satoshi Regular)
HCAP_CL_OLD = re.compile(r'(<div class="hcap">\s*<div class="cl"[^>]*>)<span class="bdg">([^<]*)</span> <span class="bdg">([^<]*)</span>(</div>)')


def fix_hero_meta(h):
    """Kunde und Branche im Case-Hero als zwei Badges. Element small statt span: die Schrift-Regel ".cl span"
    (Bildzeile, Satoshi Regular) trifft den Badge so nicht, er bleibt Satoshi Medium wie jeder Badge.
    Nach dem ersten Lauf beginnt .cl mit <small class="bdg">, beide Muster greifen dann nicht mehr."""
    fmt = lambda m: '%s<small class="bdg">%s</small> <small class="bdg">%s</small>%s' % (
        m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4))
    h = HCAP_CL_OLD.sub(fmt, h)
    return HCAP_CL.sub(fmt, h)


def apply(h):
    h = fix_colors(h)
    h = fix_hero_meta(h)
    h = fix_components(h)
    return h


def main():
    n = 0
    for f in sorted(glob.glob("*.html")):
        if f in SKIP:
            continue
        src = open(f, encoding="utf-8").read()
        out = apply(src)
        if out != src:
            open(f, "w", encoding="utf-8").write(out)
            n += 1
    print("ui_markup: %d Dateien angepasst" % n)


if __name__ == "__main__":
    main()

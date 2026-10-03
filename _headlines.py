# -*- coding: utf-8 -*-
"""Headline-Muster nach Figma (Rules / Typography 121:85, Rules / Amandine 122:85), Regelwerk _intern/BRAND-RULES.md Abschnitt 2.

Display-Headlines (eroeffnen eine Sektion, bei 1440 px mindestens 48 px) bekommen das H1-Muster:
  Zeile 1 Satoshi Bold, Zeile 2 Amandine Italic als eigene Zeile (genau eine Zeile auf Desktop).
Alle kleineren Ueberschriften (H2-Ebene, H3, Kartentitel, Akkordeon, FAQ, .kh, .lh, Next-Project-Titel) sind reines
Satoshi Bold. Vorhandene <i>/<em> darin setzt brand-type.css auf Satoshi, nicht kursiv.

Was dieser Schritt tut (laeuft nach den Generatoren und Buildern, vor _webp.py und _seo.py, ueber alle Seiten):
  1. entfernt die eigenen Marken des letzten Laufs: <i class="hs">, data-hd und die Variablen --hn/--h1n
  2. entscheidet je Headline, ob sie Display ist (Tabelle unten, gemessen am 30.09.2026 bei 1440 x 900)
  3. Display: setzt data-hd auf die Headline und markiert den Schlussteil als Amandine-Zeile.
     - von Hand gesetztes <i>/<em> am Ende bleibt die Amandine-Zeile (wird nicht ersetzt)
     - Headline mit Zeilen (.rl): die letzte Zeile, bei nur einer Zeile wird innerhalb geteilt
     - sonst: letzter Satz, Teil nach dem letzten Beistrich oder die letzten Woerter (bevorzugt ab einem
       Bindewort wie "die", "wenn", "zur"), nie die erste Zeile, nie die ganze Headline, hoechstens eine Zeile
     - --hn (Breite der Amandine-Zeile) und --h1n (laengste Satoshi-Zeile) gehen als Stil-Variable an die
       Headline, damit brand-type.css die Amandine-Zeile auf eine Zeile einpassen kann (Zeichenbreiten unten)
  4. Headlines, die zu kurz sind (unter drei Woertern), bleiben reines Satoshi.
  5. Grosse Zahlen (Amandine): data-nw und --nw (Breite des laengsten Werts in em, Amandine 400 normal) gehen an
     das Zahl-Element, damit brand-type.css die Zahl mobil auf eine Zeile in ihre Spalte einpassen kann.
     Werte einer Reihe (gleiche Klasse, gemeinsamer Rahmen bis drei Ebenen hoch) bekommen dieselbe Breite, damit
     sie gleich gross bleiben. Zaehl-Animationen: auch der Startwert (data-from) und Stationswerte (data-v) zaehlen.
  6. Platzhalter im Next-Project-Bild (.npim2) mit einem Namen statt einer Zahl bekommen data-npn (Satoshi Bold).
Mehrfach ausfuehrbar: alle eigenen Einsetzungen werden vor jedem Lauf entfernt."""
import glob
import html
import re
from html.parser import HTMLParser

SKIP = ("_qa_template.html", "case-web-funkhausliving.html")
# Klassen, die Headlines tragen koennen (div/span ohne h-Tag)
CLASSES = ("lh", "dispn", "disp", "phh", "zah", "pwh", "kh")
# bevorzugte Einstiegswoerter fuer die Amandine-Zeile (Schlussteil beginnt mit einem Bindewort oder Artikel)
SPLITWORDS = {"die", "der", "das", "den", "dem", "wenn", "wo", "wie", "was", "dass", "und", "statt", "als", "zur",
              "zum", "im", "in", "ins", "am", "an", "auf", "aus", "mit", "ohne", "bis", "vom", "von", "nicht", "ist",
              "sind", "fuer", "für", "ein", "eine", "einen", "unter", "über", "nach"}
MIN_DISPLAY = 48.0

# Zeichenbreiten in em, gemessen im Browser (WebKit, 30.09.2026) bei 100 px: Amandine Italic 400 und Satoshi Bold.
# Damit rechnet _headlines.py die Breite der Amandine-Zeile und der laengsten Satoshi-Zeile aus (--hn, --h1n).
W_AM = {
    " ": 0.26, "!": 0.25, "\"": 0.21, "%": 0.71, "&": 0.77, "'": 0.12, "(": 0.31, ")": 0.31, "+": 0.57,
    ",": 0.17, "-": 0.35, ".": 0.17, "/": 0.28, "0": 0.61, "1": 0.33, "2": 0.59, "3": 0.59, "4": 0.58, "5": 0.59,
    "6": 0.6, "7": 0.52, "8": 0.56, "9": 0.62, ":": 0.17, ";": 0.18, "?": 0.38, "A": 0.73, "B": 0.61, "C": 0.79,
    "D": 0.79, "E": 0.59, "F": 0.55, "G": 0.84, "H": 0.81, "I": 0.27, "J": 0.29, "K": 0.67, "L": 0.53, "M": 0.9,
    "N": 0.73, "O": 0.86, "P": 0.58, "Q": 0.88, "R": 0.64, "S": 0.57, "T": 0.57, "U": 0.76, "V": 0.69, "W": 1.09,
    "X": 0.7, "Y": 0.58, "Z": 0.63, "a": 0.59, "b": 0.57, "c": 0.47, "d": 0.59, "e": 0.49, "f": 0.33, "g": 0.49,
    "h": 0.6, "i": 0.26, "j": 0.25, "k": 0.55, "l": 0.25, "m": 0.95, "n": 0.6, "o": 0.56, "p": 0.58, "q": 0.56,
    "r": 0.41, "s": 0.4, "t": 0.31, "u": 0.59, "v": 0.48, "w": 0.8, "x": 0.48, "y": 0.6, "z": 0.51, "Ä": 0.73,
    "Ö": 0.86, "×": 0.46, "Ü": 0.76, "ß": 0.63, "ä": 0.59, "ö": 0.56, "ü": 0.59, "\u2013": 0.49, "’": 0.16, "“": 0.3,
    "„": 0.31, "€": 0.71
}
W_SB = {
    " ": 0.27, "!": 0.32, "\"": 0.43, "%": 0.96, "&": 0.74, "'": 0.24, "(": 0.31, ")": 0.31, "+": 0.66,
    ",": 0.29, "-": 0.45, ".": 0.29, "/": 0.41, "0": 0.7, "1": 0.4, "2": 0.59, "3": 0.57, "4": 0.65, "5": 0.6,
    "6": 0.62, "7": 0.54, "8": 0.64, "9": 0.62, ":": 0.31, ";": 0.31, "?": 0.55, "A": 0.68, "B": 0.65, "C": 0.76,
    "D": 0.74, "E": 0.59, "F": 0.57, "G": 0.78, "H": 0.74, "I": 0.29, "J": 0.55, "K": 0.67, "L": 0.54, "M": 0.88,
    "N": 0.76, "O": 0.79, "P": 0.64, "Q": 0.79, "R": 0.67, "S": 0.59, "T": 0.59, "U": 0.73, "V": 0.7, "W": 1.03,
    "X": 0.68, "Y": 0.64, "Z": 0.59, "a": 0.55, "b": 0.62, "c": 0.55, "d": 0.62, "e": 0.56, "f": 0.34, "g": 0.61,
    "h": 0.59, "i": 0.25, "j": 0.25, "k": 0.54, "l": 0.25, "m": 0.89, "n": 0.59, "o": 0.6, "p": 0.62, "q": 0.62,
    "r": 0.39, "s": 0.46, "t": 0.34, "u": 0.58, "v": 0.54, "w": 0.8, "x": 0.51, "y": 0.53, "z": 0.47, "Ä": 0.68,
    "Ö": 0.79, "×": 0.66, "Ü": 0.73, "ß": 0.59, "ä": 0.55, "ö": 0.6, "ü": 0.58, "\u2013": 0.98, "’": 0.28, "“": 0.48,
    "„": 0.48, "€": 0.62
}
# Amandine 400 normal (grosse Zahlen), gemessen wie oben (WebKit, 01.10.2026)
W_AN = {
    " ": 0.22, "!": 0.27, "%": 0.72, "+": 0.57, ",": 0.17, "-": 0.35, ".": 0.17, "/": 0.27, ":": 0.17, "×": 0.46,
    "€": 0.74, "$": 0.58, "0": 0.61, "1": 0.33, "2": 0.61, "3": 0.59, "4": 0.58, "5": 0.59, "6": 0.6, "7": 0.52,
    "8": 0.56, "9": 0.6, "−": 0.57, " ": 0.22, " ": 0.15, "M": 0.88, "i": 0.26, "o": 0.62, "T": 0.58,
    "s": 0.44, "d": 0.62, "k": 0.54, "K": 0.67, "a": 0.53, "e": 0.55, "n": 0.6, "r": 0.4, "t": 0.31, "x": 0.54
}
# Klassen grosser Zahlen (brand-type.css Abschnitt 8 entscheidet, welche davon Amandine sind)
NUMCLS = ("kto", "sv", "tv", "stnum", "big2", "fv", "dv", "bigno", "v")
NW_RESERVE = 1.04


def em_width(txt, table):
    return sum(table.get(c, 0.55) for c in txt)


def size_at_1440(style):
    """Liest eine Inline-Schriftgroesse (px oder clamp(a px, b vw, c px)) und rechnet sie auf 1440 px Breite um."""
    m = re.search(r"font-size:\s*clamp\(\s*([\d.]+)px\s*,\s*([\d.]+)vw\s*,\s*([\d.]+)px\s*\)", style or "")
    if m:
        lo, vw, hi = (float(x) for x in m.groups())
        return max(lo, min(hi, vw * 14.4))
    m = re.search(r"font-size:\s*([\d.]+)px", style or "")
    return float(m.group(1)) if m else None


def is_display(tag, cls, style, anc):
    """Display-Entscheidung nach gemessener Groesse bei 1440 px (Probe-Lauf 30.09.2026):
    h1 (Hero) 37 bis 109 px immer Display (Rolle H1 laut Regelwerk)
    .dispn 52 bis 66 px Display, ausser in .dethead (40) und .lchap (39), Inline-Groesse zaehlt zuerst
    .phh 55, .zah 52 bis 60 Display
    .disp 55 bis 63 px nur in .whead, .faq, .hpitch; ohne diesen Rahmen 24 px (keine Display)
    h2 ohne Klasse 63 bis 89 px in .help, .slp-cta, .whead, .faq
    .pwh 43, .kh 46, .lh 35, .otitle, .nptit (Name, nicht teilbar): nie Display"""
    if "sr-only" in cls:
        return False
    if tag == "h1":
        return True
    if any(c in cls for c in ("pwh", "kh", "lh")):
        return False
    s = size_at_1440(style)
    if s is not None:
        return s >= MIN_DISPLAY
    if "phh" in cls or "zah" in cls:
        return True
    if "dispn" in cls:
        return not ({"dethead", "lchap"} & anc)
    if "disp" in cls:
        return bool({"whead", "faq", "hpitch"} & anc)
    if tag == "h2" and not cls:
        return bool({"help", "slp-cta", "whead", "faq"} & anc)
    return False


class Ancestors(HTMLParser):
    """Merkt sich fuer jeden Start-Tag die Klassen aller offenen Vorfahren (Offset im Text als Schluessel)."""
    VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr", "area", "base", "col", "embed", "track"}

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.stack, self.found = [], {}
        self.lines = [0]
        for ln in text.split("\n"):
            self.lines.append(self.lines[-1] + len(ln) + 1)
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        ln, col = self.getpos()
        off = self.lines[ln - 1] + col
        anc = set()
        for _, c in self.stack:
            anc |= c
        self.found[off] = anc
        if tag not in self.VOID:
            cls = set((dict(attrs).get("class") or "").split())
            self.stack.append((tag, cls))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break


def plain(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s))).strip()


def pick_tail(words):
    """Index, ab dem der Schlussteil beginnt. Bevorzugt ein Bindewort, Schlussteil 2 Woerter bis 60 Prozent."""
    n = len(words)
    hi = max(2, int(n * 0.6 + 0.5))
    cands = [j for j in range(1, n - 1) if 2 <= n - j <= hi]
    good = [j for j in cands if words[j].lower().strip("„\"(") in SPLITWORDS]
    if good:
        return min(good, key=lambda j: abs((n - j) / n - 0.45))
    k = {3: 2, 4: 2, 5: 2, 6: 3, 7: 4}.get(n, max(3, int(round(n * 0.4))))
    return n - min(k, n - 1)


def split_text(body):
    """Teilt reinen Text (mit <br> erlaubt) in Satoshi-Teil und Amandine-Zeile. None, wenn zu kurz."""
    parts = [p for p in re.split(r"(?<=[.!?:])\s+|\s*<br\s*/?>\s*", body) if p.strip()]
    if len(parts) >= 2:
        tail = parts[-1]
        head = body[: body.rfind(tail)].rstrip()
        sep = "" if head.endswith(">") else " "
        return head + sep + '<i class="hs">' + tail + "</i>"
    words = body.split(" ")
    n = len(words)
    if n < 3:
        return None
    # Beistrich: der Teil nach dem letzten Beistrich, wenn er zwei Woerter bis 60 Prozent hat
    if "," in body:
        head, tail = body.rsplit(",", 1)
        tw = tail.strip().split(" ")
        if 2 <= len(tw) <= max(2, int(n * 0.6)):
            return head + ', <i class="hs">' + tail.strip() + "</i>"
    j = pick_tail(words)
    return " ".join(words[:j]) + ' <i class="hs">' + " ".join(words[j:]) + "</i>"


def hand_tail(inner):
    """Von Hand gesetztes <i>/<em> als Schlussteil: (Text der Zeile, Text davor) oder None."""
    tags = list(re.finditer(r"<(i|em)\b[^>]*>(.*?)</\1>", inner, re.S))
    if len(tags) != 1:
        return None
    t = tags[0]
    after = inner[t.end():]
    before = inner[:t.start()]
    if re.search(r"[^\s]", re.sub(r"</?span[^>]*>|<br\s*/?>", "", after)):
        return None
    if not re.search(r"\w", plain(re.sub(r'<span class="[^"]*h1-seo[^"]*"[^>]*>.*?</span>', "", before, flags=re.S))):
        return None
    return plain(t.group(2)), before


def lines_of(before):
    """Satoshi-Zeilen vor der Amandine-Zeile (Zeilen-Spans oder <br>), ohne SEO-Label."""
    before = re.sub(r'<span class="[^"]*h1-seo[^"]*"[^>]*>.*?</span>', "", before, flags=re.S)
    rls = re.findall(r'<span class="rl"><span>(.*?)</span></span>', before, re.S)
    if rls:
        return [plain(x) for x in rls if plain(x)]
    return [plain(x) for x in re.split(r"<br\s*/?>", before) if plain(x)]


def serifize(inner):
    """Liefert (neuer Inhalt, Text der Amandine-Zeile, Satoshi-Zeilen) oder None."""
    if "sr-only" in inner:
        return None
    ht = hand_tail(inner)
    if ht is not None:
        tail, before = ht
        return inner, tail, lines_of(before)
    if "<i" in inner or "<em" in inner:
        return None
    rls = list(re.finditer(r'(<span class="rl"><span>)(.*?)(</span></span>)', inner, re.S))
    if rls:
        last = rls[-1]
        txt = last.group(2)
        if "<" in txt or not re.search(r"\w", txt):
            return None
        if len(rls) > 1:
            # mehrere Zeilen: die letzte Zeile ganz. Bricht die vorletzte Zeile mitten im Satzteil um
            # ("... wiederholbar. Ueber" / "Projekte hinweg."), wandert der angebrochene Teil in die Amandine-Zeile.
            prev = rls[-2]
            ptxt = prev.group(2)
            move = ""
            if "<" not in ptxt and not re.search(r"[.,!?:;]\s*$", ptxt):
                m = re.search(r"[.,!?:;]\s+((?:[^\s.,!?:;]+\s+)?[^\s.,!?:;]+)\s*$", ptxt)
                if m:
                    move = m.group(1)
                else:
                    w = ptxt.split()
                    if len(w) >= 2 and w[-1].lower() in SPLITWORDS:
                        move = w[-1]
            if move:
                keep = ptxt[: ptxt.rfind(move)].rstrip()
                new = (inner[:prev.start(2)] + keep + inner[prev.end(2):last.start(2)]
                       + '<i class="hs">' + move + " " + txt + "</i>" + inner[last.end(2):])
            else:
                new = inner[:last.start(2)] + '<i class="hs">' + txt + "</i>" + inner[last.end(2):]
        else:
            # eine Zeile: innerhalb der Zeile teilen
            out = split_text(txt)
            if out is None:
                return None
            new = inner[:last.start(2)] + out + inner[last.end(2):]
    else:
        if re.search(r"<(?!br\b)[a-z]", inner):
            return None
        lead = re.match(r"^\s*", inner).group(0)
        trail = re.search(r"\s*$", inner).group(0)
        out = split_text(inner.strip())
        if out is None:
            return None
        new = lead + out + trail
    tail, before = hand_tail(new)
    return new, tail, lines_of(before)


def mark(attrs, tail, lines):
    """Setzt data-hd und die Einpass-Variablen in den Start-Tag.
    --hn: Breite der Amandine-Zeile in em / 0,5 (entspricht Zeichen zu je 0,5 em, tokens.css --am-cw)
    --h1n: Breite der laengsten Satoshi-Zeile in em / 0,56 (Case-Hero)"""
    hn = em_width(tail, W_AM) / 0.5
    h1n = max([em_width(x, W_SB) for x in lines] or [0.56]) / 0.56
    var = "--hn:%.1f;--h1n:%.1f" % (hn, h1n)
    m = re.search(r'style="([^"]*)"', attrs)
    if m:
        st = m.group(1).rstrip()
        st = (st + ";" if st and not st.endswith(";") else st) + var
        attrs = attrs[:m.start()] + 'style="' + st + '"' + attrs[m.end():]
    else:
        attrs += ' style="' + var + '"'
    return attrs + " data-hd"


def unmark(h):
    """Entfernt alle eigenen Marken des letzten Laufs."""
    h = re.sub(r'<i class="hs">(.*?)</i>', r"\1", h, flags=re.S)
    h = re.sub(r" data-hd(?=[\s>])", "", h)
    h = re.sub(r';?--hn:[\d.]+;--h1n:[\d.]+', "", h)
    h = re.sub(r" data-(?:nw|npn)(?=[\s>])", "", h)
    h = re.sub(r';?--nw:[\d.]+', "", h)
    h = h.replace(' style=""', "")
    return h


class Elements(HTMLParser):
    """Liste aller Elemente mit Offsets: [tag, attrs, start, ende des Start-Tags, Beginn des End-Tags, Eltern-Index]."""
    VOID = Ancestors.VOID

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.stack, self.els = [], []
        self.lines = [0]
        for ln in text.split("\n"):
            self.lines.append(self.lines[-1] + len(ln) + 1)
        self.feed(text)

    def off(self):
        ln, col = self.getpos()
        return self.lines[ln - 1] + col

    def handle_starttag(self, tag, attrs):
        o = self.off()
        par = self.stack[-1] if self.stack else -1
        self.els.append([tag, dict(attrs), o, o + len(self.get_starttag_text()), None, par])
        if tag not in self.VOID:
            self.stack.append(len(self.els) - 1)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.els[self.stack[i]][0] == tag:
                self.els[self.stack[i]][4] = self.off()
                del self.stack[i:]
                break


def fmt_de(v, dec):
    """Zahl wie die Zaehl-Animation (de-AT): Tausenderpunkt, Dezimalbeistrich."""
    s = "{:,.{d}f}".format(v, d=dec)
    return s.replace(",", "\u0001").replace(".", ",").replace("\u0001", ".")


def num_texts(a, inner, page_vs):
    """Alle Texte, die das Zahl-Element im Lauf zeigen kann (Endwert, Startwert, Stationen)."""
    out = [plain(inner)]
    # Zaehler: Case-KPIs (data-from/-to, -decimals, -prefix, -suffix) und Studie (data-to, -dec, -pre, -suf)
    dec = a.get("data-decimals") or a.get("data-dec") or "0"
    pre = a.get("data-prefix") or a.get("data-pre") or ""
    suf = a.get("data-suffix") or a.get("data-suf") or ""
    for key in ("data-from", "data-to"):
        if key in a:
            try:
                out.append(html.unescape(pre + fmt_de(float(a[key]), int(dec)) + suf))
            except ValueError:
                pass
    if "data-v0" in a:
        out += page_vs
    if "data-val" in a:
        # Studie: die Scrub-Ziffer schreibt "€ x,xx Mio." (bis 4,65), breiteste Ziffern als Annahme
        out.append("€ 0,00 Mio.")
    return [t for t in out if t]


def mark_numbers(h):
    """Setzt data-nw und --nw an grosse Zahlen und data-npn an Namen im Next-Project-Platzhalter."""
    els = Elements(h).els
    page_vs = [html.unescape(v) for v in re.findall(r'\bdata-v="([^"]*)"', h)]
    nums = {}
    for i, (tag, a, s, se, ce, par) in enumerate(els):
        cls = (a.get("class") or "").split()
        if ce is None or tag not in ("span", "div"):
            continue
        k = next((c for c in NUMCLS if c in cls), None)
        if k and "kto--txt" not in cls:
            inner = h[se:ce]
            if "<div" in inner:
                continue
            ts = num_texts(a, inner, page_vs)
            if ts:
                nums[i] = (k, max(em_width(t, W_AN) for t in ts))
    # Reihe: naechster Rahmen (bis drei Ebenen hoch), der mindestens zwei Zahlen derselben Klasse enthaelt
    def chain(i):
        c, p = [], els[i][5]
        while p >= 0 and len(c) < 3:
            c.append(p)
            p = els[p][5]
        return c
    chains = {i: chain(i) for i in nums}
    width = {}
    for i, (k, w) in nums.items():
        width[i] = w
        for anc in chains[i]:
            peers = [j for j in nums if j != i and nums[j][0] == k and anc in chains[j]]
            if peers:
                width[i] = max([w] + [nums[j][1] for j in peers])
                break
    ins = {}
    for i in nums:
        ins[i] = ("nw", width[i] * NW_RESERVE)
    # Next-Project-Platzhalter ohne Bild: Name (Buchstaben) statt Zahl
    for i, (tag, a, s, se, ce, par) in enumerate(els):
        if tag == "span" and "font-size" in (a.get("style") or "") and ce is not None and par >= 0:
            gp = els[par][5]
            if gp >= 0 and "npim2" in (els[gp][1].get("class") or "").split():
                if re.search(r"[A-Za-zÄÖÜäöüß]{3,}", plain(h[se:ce]).replace("Mio", "")):
                    ins[i] = ("npn", None)
    # von hinten einsetzen, damit die Offsets stimmen
    for i in sorted(ins, key=lambda j: els[j][2], reverse=True):
        kind, w = ins[i]
        s, se = els[i][2], els[i][3]
        st = h[s:se]
        if kind == "npn":
            st = st[:-1] + " data-npn>"
        else:
            var = "--nw:%.2f" % w
            m = re.search(r'style="([^"]*)"', st)
            if m:
                v = m.group(1).rstrip()
                v = (v + ";" if v and not v.endswith(";") else v) + var
                st = st[:m.start()] + 'style="' + v + '"' + st[m.end():]
            else:
                st = st[:-1] + ' style="' + var + '">'
            st = st[:-1] + " data-nw>"
        h = h[:s] + st + h[se:]
    return h, len([1 for k, _ in ins.values() if k == "nw"])


def process(h):
    anc = {}
    n = {"display": 0, "satoshi": 0}

    def repl(m, tag, attrs, inner):
        cls = re.search(r'class="([^"]*)"', attrs)
        cls = set(cls.group(1).split()) if cls else set()
        if tag in ("div", "span") and not (cls & set(CLASSES)):
            return m.group(0)
        st = re.search(r'style="([^"]*)"', attrs)
        if not is_display(tag, cls, st.group(1) if st else "", anc.get(m.start(), set())):
            n["satoshi"] += 1
            return m.group(0)
        res = serifize(inner)
        if res is None:
            n["satoshi"] += 1
            return m.group(0)
        new, tail, lines = res
        n["display"] += 1
        return "<%s%s>%s</%s>" % (tag, mark(attrs, tail, lines), new, tag)

    # Vorfahren je Durchgang neu lesen, weil der erste Durchgang die Offsets verschiebt
    anc = Ancestors(h).found
    h = re.sub(r"<(h1|h2|h3)(\b[^>]*)>(.*?)</\1>",
               lambda m: repl(m, m.group(1), m.group(2), m.group(3)), h, flags=re.S)
    anc = Ancestors(h).found
    h = re.sub(r'<(div)(\b[^>]*class="[^"]*\b(?:lh|dispn|disp|phh|zah|pwh|kh)\b[^"]*"[^>]*)>((?:(?!<div)[\s\S])*?)</div>',
               lambda m: repl(m, "div", m.group(2), m.group(3)), h)
    return h, n


def main():
    tot = {"display": 0, "satoshi": 0}
    nn = 0
    for f in sorted(glob.glob("*.html")):
        if f in SKIP:
            continue
        h0 = open(f, encoding="utf-8").read()
        h, n = process(unmark(h0))
        h, c = mark_numbers(h)
        nn += c
        for k in tot:
            tot[k] += n[k]
        if h != h0:
            open(f, "w", encoding="utf-8").write(h)
    print("Headlines: %d Display (Satoshi + Amandine-Zeile), %d reines Satoshi, %d grosse Zahlen eingepasst"
          % (tot["display"], tot["satoshi"], nn))


if __name__ == "__main__":
    main()

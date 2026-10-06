# -*- coding: utf-8 -*-
"""Ladeleistung fuer alle Seiten (Technik-Empfehlungen J1, J2, B1, B5). Mehrfach ausfuehrbar, schreibt nur bei
Aenderung. Regel "perf" des Nachlaufs (_nachlauf.py): nach "webp", vor "seo". Einzeln aufrufbar: python3 _perf.py

1. Videos (J1): jedes Video mit data-auto ausserhalb des Heros bekommt preload="none" und seine Quelle als data-src.
   master.js setzt src erst, wenn das Video sichtbar wird (vor play()). Im Hero (erste Sektion in <main> mit Klasse
   hero, ahero, svc-hero oder chero) behaelt nur das erste Video seine Quelle; die weiteren Folien des Hero-Sliders
   laedt master.js kurz vor ihrem Einsatz. Videos ohne data-auto (Film mit Abspielknopf, Scroll-Video) bleiben.
2. Menue-Vorschaubilder (J2): kleine Fassungen mit 300 px Breite unter assets/img/menu/ (aus den Originalen erzeugt),
   im Menue nur als data-src mit einem 1x1-Platzhalter. master.js laedt sie beim ersten Oeffnen des Menues oder schon
   bei mouseenter/focus auf den Menue-Knopf. Alt-Text leer (Dekoration, B5).
3. Bilder im ersten Bildschirm (B1): auf den Seiten in FIRST die ersten Bilder in <main> mit loading="eager",
   das groesste davon mit fetchpriority="high". Auf case-kommunalkredit.html die Fotostrecke (foto/e*) mit
   loading="lazy" (steht erst ab etwa 4.500 px Tiefe).
4. Kundenlogos der Startseite (B5): die Slots tragen die Bildmasse als data-wh, master.js setzt width/height.
Warnungen beginnen mit "  !" (sammelt _build.sh am Ende)."""
import os
import re

from PIL import Image

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SKIP = ("_qa_template.html",)
PIXEL = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
MENU_DIR = "assets/img/menu"
MENU_W = 300
HERO_RX = re.compile(r'<section\b[^>]*\bclass="[^"]*\b(?:hero|ahero|svc-hero|chero)\b[^"]*"')
# Seite -> Nummern der Bilder in <main> (Reihenfolge im HTML, ab 0), die im ersten Bildschirm stehen
# (gemessen 3.10.2026 bei 1440 x 900 und 390 x 844), und die Nummer des groessten am Telefon (fetchpriority="high").
# Aendert sich der Aufbau der Seite, die Liste neu messen (Messskript im Bericht der Technik-Umsetzung).
FIRST = {
    "agentur.html": ((0, 1, 2, 3, 4), 1),
    "work.html": ((0, 1, 2, 5), 1),   # 6, 10, 11 nur am Desktop angeschnitten: bleiben lazy (spart am Telefon gut 300 KB)
}
LAZY_FROM = {"case-kommunalkredit.html": re.compile(r'src="assets/case/kommunalkredit/foto/e\d+\.webp"')}

warn = []


# ---------------------------------------------------------------- 1. Videos
def attr_set(tag, name, value):
    """Attribut setzen oder ersetzen (Wert ohne Anfuehrungszeichen-Sonderfaelle)."""
    m = re.search(r'\s%s="[^"]*"' % re.escape(name), tag)
    if m:
        return tag[:m.start()] + ' %s="%s"' % (name, value) + tag[m.end():]
    return tag[:-1].rstrip() + ' %s="%s">' % (name, value)


def defer_video(tag):
    """src -> data-src, preload none. Schon umgestellte Tags kommen unveraendert zurueck."""
    m = re.search(r'\ssrc="([^"]+)"', tag)
    if m:
        tag = tag[:m.start()] + ' data-src="%s"' % m.group(1) + tag[m.end():]
    return attr_set(tag, "preload", "none")


def videos(h):
    mi = h.find("<main")
    if mi < 0:
        return h
    first = re.search(r"<section\b", h[mi:])
    hero_a = hero_b = -1
    if first:
        s = mi + first.start()
        if HERO_RX.match(h, s):
            hero_a = s
            hero_b = h.find("</section>", s)
    out, last, kept = [], 0, 0
    for m in re.finditer(r"<video\b[^>]*>", h):
        tag = m.group(0)
        if "data-auto" not in tag or m.start() < mi:
            continue
        if hero_a <= m.start() < hero_b and kept == 0:
            kept += 1
            continue
        new = defer_video(tag)
        if new != tag:
            out.append(h[last:m.start()] + new)
            last = m.end()
    out.append(h[last:])
    return "".join(out)


# ---------------------------------------------------------------- 2. Menue-Vorschaubilder
def menu_file(src):
    """assets/img/x.webp|jpg -> assets/img/menu/x.webp (erzeugt aus dem besten Original). Gibt (pfad, w, h) zurueck."""
    base = os.path.splitext(os.path.basename(src))[0]
    out = "%s/%s.webp" % (MENU_DIR, base)
    cands = [os.path.join("assets/img", base + ext) for ext in (".jpg", ".png", ".webp")]
    orig = next((c for c in cands if os.path.exists(c)), None)
    if not orig:
        warn.append("  ! Menue-Vorschau ohne Original: %s" % src)
        return None
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(orig):
        os.makedirs(MENU_DIR, exist_ok=True)
        im = Image.open(orig)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        if im.width > MENU_W:
            im = im.resize((MENU_W, round(im.height * MENU_W / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=80, method=6)
    with Image.open(out) as im:
        return out, im.width, im.height


def menu_tag(name, extra=""):
    """Fertiges Menue-Vorschaubild fuer _gen.py (Generator) und fuer die Umstellung handgebauter Seiten."""
    got = menu_file("assets/img/%s.jpg" % name)
    if not got:
        return '<img loading="lazy" decoding="async" src="assets/img/%s.jpg" alt=""%s>' % (name, extra)
    path, w, hh = got
    return '<img loading="lazy" decoding="async" src="%s" data-src="%s" alt=""%s width="%d" height="%d">' % (PIXEL, path, extra, w, hh)


def menu_img(tag):
    m = re.search(r'\ssrc="(assets/img/[^"/]+\.(?:webp|jpg|png))"', tag)
    if m:
        got = menu_file(m.group(1))
        if not got:
            return tag
        path, w, hh = got
        tag = tag[:m.start()] + ' src="%s" data-src="%s"' % (PIXEL, path) + tag[m.end():]
        tag = attr_set(attr_set(tag, "width", str(w)), "height", str(hh))
    return attr_set(tag, "alt", "")


def menu(h):
    def nav(m):
        return re.sub(r"<img\b[^>]*>", lambda x: menu_img(x.group(0)), m.group(0))
    return re.sub(r'<nav class="msheet".*?</nav>', nav, h, count=1, flags=re.S)


# ---------------------------------------------------------------- 3. Bilder im ersten Bildschirm, Fotostrecke lazy
def first_screen(f, h):
    idx, big = FIRST.get(f, ((), -1))
    if idx:
        mi = h.find("<main")
        tags = list(re.finditer(r"<img\b[^>]*>", h[mi:]))
        for k, m in reversed(list(enumerate(tags))):
            t = m.group(0)
            # alle anderen Bilder in <main> bleiben lazy (handgebaute Seiten behalten sonst einen alten eager-Stand)
            new = attr_set(t, "loading", "eager" if k in idx else "lazy")
            new = attr_set(new, "fetchpriority", "high") if k == big else re.sub(r'\sfetchpriority="[^"]*"', "", new)
            a, b = mi + m.start(), mi + m.end()
            h = h[:a] + new + h[b:]
    rx = LAZY_FROM.get(f)
    if rx:
        h = re.sub(r"<img\b[^>]*>", lambda m: attr_set(m.group(0), "loading", "lazy") if rx.search(m.group(0)) else m.group(0), h)
    return h


# ---------------------------------------------------------------- 4. Kundenlogos mit Massen
_logo_dims = {}


def logo_wh(name):
    if name not in _logo_dims:
        p = "assets/logos/%s.png" % name
        if os.path.exists(p):
            with Image.open(p) as im:
                _logo_dims[name] = "%dx%d" % im.size
        else:
            warn.append("  ! Logo fehlt: %s" % p)
            _logo_dims[name] = ""
    return _logo_dims[name]


def logos(h):
    def slot(m):
        tag = m.group(0)
        ns = re.search(r'data-set="([^"]*)"', tag)
        if not ns:
            return tag
        wh = ",".join(logo_wh(n) for n in ns.group(1).split(",") if n)
        return attr_set(tag, "data-wh", wh)
    return re.sub(r'<span class="lslot"[^>]*>', slot, h)


# ---------------------------------------------------------------- 5. Sprunglink "Zum Inhalt" (B5)
SKIPLINK = '<a class="skip" href="#inhalt">Zum Inhalt</a>'


def skiplink(h):
    if "<main" not in h:
        return h
    if SKIPLINK not in h:
        h = re.sub(r"(<body\b[^>]*>)", lambda m: m.group(1) + "\n" + SKIPLINK, h, count=1)
    m = re.search(r"<main\b[^>]*>", h)
    tag = m.group(0)
    if 'id="' not in tag:
        h = h[:m.start()] + tag[:-1] + ' id="inhalt" tabindex="-1">' + h[m.end():]
    elif 'id="inhalt"' not in tag:
        warn.append("  ! <main> hat eine eigene id, Sprunglink zeigt ins Leere")
    return h


ZAEHLER = {"n": 0}


def seite(f, h):
    """Regel "perf" des Nachlaufs (_nachlauf.py): Videos, Menuebilder, erster Bildschirm, Logos, Sprunglink."""
    if f in SKIP:
        return h
    if 'http-equiv="refresh"' in h:
        return h
    out = skiplink(logos(first_screen(f, menu(videos(h)))))
    if out != h:
        ZAEHLER["n"] += 1
    return out


def warnungen():
    """Gesammelte Warnungen, jede einmal. Leert die Liste."""
    zeilen = []
    for w in warn:
        if w not in zeilen:
            zeilen.append(w)
    del warn[:]
    return zeilen


def bericht():
    return "\n".join(warnungen() + ["Ladeleistung: %d Seiten angepasst" % ZAEHLER["n"]])


if __name__ == "__main__":
    import _nachlauf
    _nachlauf.einzeln(seite)
    print(bericht())

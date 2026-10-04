# Baut den Kunden-Content in Work-Kacheln (Vorschau-Medien aus assets/content.json) und in die handgebauten
# Case-Seiten (Galerie aus _content/cases/<slug>.json) ein.
# Regel "inhalt" des Nachlaufs (_nachlauf.py): seite(name, html) wirkt nur auf work.html und die handgebauten Cases,
# alle anderen Seiten kommen unveraendert zurueck. Einzeln aufrufbar: python3 _apply_content.py
# -*- coding: utf-8 -*-
import json, os, re

M = json.load(open("assets/content.json", encoding="utf-8"))

# ---------- 1) WORK: Preview-Medien in die Kacheln ----------
# Anker (Text in der Kachel) -> Case-Slug im Manifest. Mehrere Schreibweisen derselben Kachel sind erlaubt
# (z. B. mit &amp; und mit &): gewarnt wird nur, wenn keine davon auf der Seite steht.
TILE = {
    "Immobilien-Investment":     "case-immobilien-investment",
    "Crowdinvesting-Plattform":  "case-crowdinvesting",
    "Wohnbau, Floridsdorf":      "case-wohnbau-floridsdorf",
    "Dental-/Health-Marke":      "case-health-brand",
    "Premium-Consumer-Brand":    "case-consumer-brand",
    "Premium-Neubau, Wien":      "case-premium-neubau",
    "Noma Wien":                 "case-web-noma",
    "Trattner &amp; Söhne":      "case-web-trattner",
    "Trattner & Söhne":          "case-web-trattner",
    "Northpoint Advisors":       "case-web-northpoint",
    "Pharmacom":                 "case-web-pharmacom",
    "Havenstone":                "case-web-havenstone",
    "DaPhi":                     "case-web-daphi",
    "IB-7":                      "case-web-ib7",
    "Kommunalkredit":            "kommunalkredit",
    "Juwel Wien":                "juwel",
    "Hero Group":                "herogroup",
}

ZAEHLER = {"kacheln": 0, "galerien": 0}


def media_html(entry, alt):
    p = entry.get("prev")
    if not p:
        return None
    if entry.get("prev_kind") == "video":
        return ('<video data-auto muted loop playsinline preload="metadata" '
                'src="%s" aria-label="%s"></video>' % (p, alt))
    return '<img loading="lazy" decoding="async" src="%s" alt="%s">' % (p, alt)

def tile_bounds(s, start):
    depth, end = 0, None
    for mm in re.finditer(r'</?(a|div|span|img|video)\b[^>]*>', s[start:]):
        tag = mm.group(0)
        if tag.startswith('</'):
            depth -= 1
        elif not tag.endswith('/>') and mm.group(1) not in ('img',):
            depth += 1
        if depth == 0:
            end = start + mm.end()
            break
    return end


def kacheln(w):
    """Vorschau-Medien in die Kacheln von work.html."""
    changed = 0
    gefunden, fehlt = set(), []
    for anchor, slug in TILE.items():
        entry = M.get(slug)
        if not entry:
            continue
        new_media = media_html(entry, anchor)
        if not new_media:
            continue
        idx = w.find('<b>%s</b>' % anchor)
        if idx < 0:
            # Farbkachel: Anker im wclr-Label
            idx = w.find('>%s</b>' % anchor)
        if idx < 0:
            fehlt.append((anchor, slug))
            continue
        gefunden.add(slug)
        start = w.rfind('<a class="wt tile', 0, idx)
        d = w.rfind('<div class="wt tile', 0, idx)
        if d > start:
            start = d
        end = tile_bounds(w, start)
        if not end:
            print("  ! Work-Kachel ohne Ende:", anchor)
            continue
        block = w[start:end]
        # bestehendes Bild ersetzen, sonst Farbfläche durch Medium tauschen
        if '<img' in block and 'wclr' not in block:
            nb = re.sub(r'<img[^>]*>', new_media, block, count=1)
        else:
            nb = re.sub(r'<span class="wclr".*?</span>\s*(?=<span class="wpill"|<span class="wlab"|$)',
                        new_media, block, count=1, flags=re.S)
            if nb == block:
                continue
            if 'has-media' not in nb:
                nb = nb.replace('class="wt tile', 'class="wt tile has-media', 1)
            # Label ergänzen, falls die Farbkachel keins hatte
            if '<span class="wlab">' not in nb:
                label = anchor
                nb = nb.replace('</a>' if nb.startswith('<a') else '</div>',
                                '<span class="wlab"><b>%s</b></span>%s' % (label, '</a>' if nb.startswith('<a') else '</div>'))
        w = w[:start] + nb + w[end:]
        changed += 1
    for anchor, slug in fehlt:
        if slug not in gefunden:
            print("  ? kein Anker:", anchor)
    ZAEHLER["kacheln"] += changed
    return w


# ---------- 2) HANDGEBAUTE CASE-SEITEN: Content-Galerie ----------
# Die generierten Cases (Vorlagen dossier und web) setzen ihre Galerie selbst als Baustein "galerie" ein
# (_bausteine.py). Hier nur noch die handgebauten Seiten: Galerie aus dem Baustein "galerie" ihrer
# Inhaltsdatei _content/cases/<slug>.json, eingesetzt vor dem Next-Case.
from _cases import HAND, bausteine
from _bausteine import galerie_html

# Marker-Kommentare, vor denen die Galerie steht (der erste vorhandene gilt)
MARKER = ("  <!-- KAPITEL: MEHR -->", "  <!-- NEXT CASE -->", "  <!-- NEXT -->")


def film_html(entry, title, sub):
    if not entry.get("recap"):
        return ""
    return '''  <!-- FILM -->
  <section class="sec fg-dark" data-bg="#0A0A0A" data-fg="light" style="background:#0A0A0A">
    <div class="wrap" style="max-width:1240px">
      <span class="label" style="color:var(--champ);display:block;margin-bottom:clamp(26px,3vw,40px)">%s</span>
      <div class="filmwrap" data-fade>
        <video src="%s" preload="none" playsinline poster="%s"></video>
        <button class="fplay" aria-label="Film abspielen"><span>▶</span></button>
      </div>
      <div class="filmcap">
        <span>%s</span>
        <span>Ton beim Abspielen</span>
      </div>
    </div>
  </section>

''' % (title, entry["recap"], entry.get("prev_img_poster", ""), sub)


def galerie(case, s):
    """Galerie aus der Inhaltsdatei in die handgebaute Seite: alte Galerie heraus, neue vor den Next-Case."""
    gals = bausteine(case, "galerie")
    if not gals:
        return s
    g = gals[0]
    gal = galerie_html(g["medien"], g.get("hintergrund", "#0E0E10"), g.get("label", "Aus dem Mandat"))
    if not gal:
        return s
    # bestehende Galerie herausschneiden, damit sie neu verteilt wird
    if 'collage--tight' in s:
        a = s.find('  <!-- CONTENT AUS DEM MANDAT -->')
        if a < 0:
            a = s.rfind('<section class="collage collage--tight')
        b = s.find('</section>', s.find('collage--tight', a))
        if a >= 0 and b > a:
            s = s[:a] + s[b + len('</section>'):].lstrip('\n')
    # vor "NEXT" einsetzen
    for marker in MARKER:
        if marker in s:
            ZAEHLER["galerien"] += 1
            return s.replace(marker, gal + marker, 1)
    print("  ! %s: Galerie nicht eingesetzt, es fehlt ein Marker-Kommentar (%s)"
          % (case["seite"], " oder ".join(m.strip() for m in MARKER)))
    return s


def seite(name, h):
    """Regel "inhalt": Kacheln auf work.html, Galerie auf den handgebauten Case-Seiten."""
    if name == "work.html":
        return kacheln(h)
    for case in HAND:
        if case["seite"] == name:
            return galerie(case, h)
    return h


def bericht():
    return "Work-Kacheln mit Preview: %d, Case-Seiten mit Content-Galerie: %d" % (ZAEHLER["kacheln"], ZAEHLER["galerien"])


if __name__ == "__main__":
    import _nachlauf
    _nachlauf.einzeln(seite, [f for f in ["work.html"] + [c["seite"] for c in HAND] if os.path.exists(f)])
    print(bericht())

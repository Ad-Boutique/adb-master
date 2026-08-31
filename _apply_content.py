# Baut den Kunden-Content (assets/content.json) in Work-Kacheln und Case-Seiten ein.
# -*- coding: utf-8 -*-
import json, os, re, subprocess

# Bildmasse (Breite, Hoehe) je Datei, siehe assets/imgdim.json
DIMS = json.load(open("assets/imgdim.json")) if os.path.exists("assets/imgdim.json") else {}

M = json.load(open("assets/content.json", encoding="utf-8"))

# ---------- 1) WORK: Preview-Medien in die Kacheln ----------
# Anker (Text in der Kachel) -> Case-Slug im Manifest
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

w = open("work.html", encoding="utf-8").read()

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

changed = 0
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
        print("  ? kein Anker:", anchor)
        continue
    start = w.rfind('<a class="wt tile', 0, idx)
    d = w.rfind('<div class="wt tile', 0, idx)
    if d > start:
        start = d
    end = tile_bounds(w, start)
    if not end:
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

open("work.html", "w", encoding="utf-8").write(w)
print("Work-Kacheln mit Preview:", changed)


# ---------- 2) CASE-SEITEN: Intro-Medium + Content-Galerie ----------
NCOL = 6


def _ratio(p):
    """Hoehe je Breiteneinheit, aus den echten Dateimassen."""
    if p.endswith(".mp4"):
        return 16 / 9.0
    if p in DIMS and DIMS[p]:
        return DIMS[p][1] / float(DIMS[p][0])
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p],
                         capture_output=True, text=True).stdout
    mw = re.search(r"pixelWidth:\s*(\d+)", out)
    mh = re.search(r"pixelHeight:\s*(\d+)", out)
    if not (mw and mh):
        return 1.0
    DIMS[p] = [int(mw.group(1)), int(mh.group(1))]
    return DIMS[p][1] / float(DIMS[p][0])


def gallery_html(entry, title, bg="#0E0E10"):
    media = [im["src"] for im in entry.get("imgs", [])] + [v["src"] for v in entry.get("vids", [])]
    media = [m for m in media if os.path.exists(m)]
    if not media:
        return ""
    # so oft wiederholen, dass jede der sechs Spalten den Rahmen ueberragt
    while len(media) < NCOL * 4:
        media = media + media
    media = media[:NCOL * 5]
    # jedes Motiv in die gerade kuerzeste Spalte, hohe zuerst
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
                items.append('<img loading="lazy" decoding="async" src="%s" alt="">' % m)
        parts.append('      <div class="cpcol" data-drift="%s">\n        %s\n      </div>' % (speeds[i], "\n        ".join(items)))
    return ('  <!-- CONTENT AUS DEM MANDAT -->\n'
            '  <section class="collage collage--tight" data-bg="%s" data-fg="light">\n'
            '    <div class="wrap" style="position:relative;z-index:2;margin-bottom:clamp(30px,4vw,60px)">\n'
            '      <span class="label" style="color:var(--champ)">Aus dem Mandat</span>\n'
            '    </div>\n'
            '    <div class="cplane">\n%s\n    </div>\n  </section>\n\n') % (bg, "\n".join(parts))

CASE_BG = {
    "case-immobilien-investment": "#2E3A2F",
    "case-crowdinvesting": "#1C2530",
    "case-wohnbau-floridsdorf": "#33383E",
    "case-health-brand": "#1F3833",
    "case-consumer-brand": "#0E0E10",
    "case-premium-neubau": "#22382C",
}

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

CASE_FILES = {
    "case-immobilien-investment": "case-immobilien-investment.html",
    "case-crowdinvesting": "case-crowdinvesting.html",
    "case-wohnbau-floridsdorf": "case-wohnbau-floridsdorf.html",
    "case-health-brand": "case-health-brand.html",
    "case-consumer-brand": "case-consumer-brand.html",
    "case-premium-neubau": "case-premium-neubau.html",
    "case-web-noma": "case-web-noma.html",
    "case-web-trattner": "case-web-trattner.html",
    "case-web-northpoint": "case-web-northpoint.html",
    "case-web-pharmacom": "case-web-pharmacom.html",
    "case-web-havenstone": "case-web-havenstone.html",
    "case-web-daphi": "case-web-daphi.html",
    "case-web-ib7": "case-web-ib7.html",
}

added = 0
for slug, fname in CASE_FILES.items():
    entry = M.get(slug)
    if not entry or not os.path.exists(fname):
        continue
    s = open(fname, encoding="utf-8").read()
    gal = gallery_html(entry, slug, CASE_BG.get(slug, '#0E0E10'))
    if not gal:
        continue
    # bestehende Galerie herausschneiden, damit sie neu verteilt wird
    if 'collage--tight' in s:
        a = s.find('  <!-- CONTENT AUS DEM MANDAT -->')
        if a < 0:
            a = s.rfind('<section class="collage collage--tight')
        b = s.find('</section>', s.find('collage--tight', a))
        if a >= 0 and b > a:
            s = s[:a] + s[b + len('</section>'):].lstrip('\n')
    # vor "NEXT" einsetzen
    for marker in ("  <!-- NEXT CASE -->", "  <!-- NEXT -->"):
        if marker in s:
            s = s.replace(marker, gal + marker, 1)
            break
    else:
        continue
    open(fname, "w", encoding="utf-8").write(s)
    added += 1
print("Case-Seiten mit Content-Galerie:", added)

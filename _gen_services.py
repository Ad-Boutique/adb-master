# Leistungsseiten-Generator: baut die sechs Leistungsseiten service-*.html.
# Inhalte in _content/services/<slug>.json (Laden und Pruefen: _leistungen.py), Markup in _tpl_services.py,
# hier nur die Logik: FAQ-Reihenfolge, Querverweise auf die Cases, Kennzahlen, Schreiben.
# Anleitung fuer Inhalte: docs/CMS-LEISTUNGEN.md.
# -*- coding: utf-8 -*-
from _cases import PERFORMANCE, WEB, HAND, leistungen as case_leistungen
from _leistungen import SERVICES, faq_liste, kennzahlen
from _tpl_services import render_service

# Suchmaschinen-Teil je Leistung (Feld seo der Inhaltsdatei): Suchbegriff, Title, Description, Antwortabsatz, FAQ
SEO = {s["slug"]: s["seo"] for s in SERVICES}


# Leistungs-Hero im Woerterbuch-Stil (Kundenfreigabe 3.10.2026): ein Wort ueber die ganze Breite,
# darunter die Tags, dann die Definition mit Amandine-Woertern (<em>) und ein Foto ueber die volle Breite.
# Suchbegriff fuer die H1 steht unsichtbar im sr-only-Teil (SEO-Label), das Wort selbst ist dekorativ gross.
DHERO = {s["slug"]: s["dhero"] for s in SERVICES}


def _dhero(s):
    d = DHERO[s["slug"]]
    seo = SEO.get(s["slug"], {}).get("label") or s["nav"]
    tags = "".join('<span class="bdg">%s</span>' % t for t in s["tags"])
    text = d["text"].replace("<em>", '<em class="dh-am">')
    return ('''  <section class="dhero fg-light bg-paper" data-bg="#F4F3EB" data-fg="dark">
    <a class="svc-back" href="index.html#leistungen">← Alle Leistungen</a>
    <div class="dh-wrap">
      <h1 class="dh-word"><span class="dh-fit" aria-hidden="true">%s</span><span class="sr-only">%s</span></h1>
      <div class="dh-tags" data-fade>%s</div>
      <div class="dh-def" data-fade>
        <p class="dh-kicker">%s [Leistung]</p>
        <p class="dh-text">%s</p>
        <a class="alink" href="#anfrage">Direkt anfragen ↓</a>
      </div>
    </div>
    <figure class="dh-photo"><img src="%s" alt="%s" width="2400" height="1371" fetchpriority="high"></figure>
  </section>''') % (d["word"].upper(), seo, tags, d["kicker"], text, d["img"], d["alt"])


def _all_cases_for(slug):
    """(href, titel) aller Cases, die die Leistung <slug> als Leistung ausweisen (meta.leistungen der Inhaltsdateien
    _content/cases/*.json): erst die Dossiers, dann die Website-Cases, dann die handgebauten Seiten"""
    href = slug + ".html"
    out = []
    for c in PERFORMANCE:
        if c["vorlage"] == "handgebaut":
            continue
        if any(h == href for _, h in case_leistungen(c)):
            out.append((c["slug"] + ".html", c["meta"]["name"]))
    for c in WEB:
        if any(h == href for _, h in case_leistungen(c)):
            out.append((c["slug"] + ".html", c["meta"]["name"]))
    for c in HAND:
        if any(h == href for _, h in case_leistungen(c)):
            out.append((c["seite"], c["meta"]["name"]))
    return out


def weitere_cases(s):
    """Cases mit dieser Leistung, die nicht schon in der Liste "Ausgewaehlte Ergebnisse" (oplist) stehen.
    Meldet Cases der Liste, die die Leistung ihrerseits nicht verlinken."""
    listed = [o["href"] for o in s.get("oplist", [])]
    allc = _all_cases_for(s["slug"])
    for h in listed:
        if h not in {a for a, _ in allc}:
            print("  Hinweis: %s listet %s, aber der Case verlinkt die Leistung nicht" % (s["slug"], h))
    return [(h, t) for h, t in allc if h not in listed]


def seite(s):
    """Fertiges HTML der Leistungsseite (vor dem Nachlauf)."""
    return render_service(s, _dhero(s), faq_liste(s), weitere_cases(s), kennzahlen(s))


if __name__ == "__main__":
    # fertig(): die Nachlauf-Regeln (_nachlauf.py) laufen gleich beim Erzeugen, geschrieben wird die fertige Seite.
    # Die Vorschau-Variante service-performance-marketing-v3.html entsteht dabei mit (_nachlauf.ABLEITUNGEN).
    import _nachlauf
    for name in _nachlauf.fertig({s["slug"] + ".html": seite(s) for s in SERVICES}):
        print("service", name[:-5])
    print("services done")

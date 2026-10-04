# -*- coding: utf-8 -*-
"""Ein Footer fuer alle Seiten (Figma Website / Komponenten, Footer 84:69). Gehoert der Layout-Abteilung.
Ersetzt auf jeder Seite den kompletten <footer>...</footer> durch dasselbe Markup. Mehrfach ausfuehrbar:
der Footer wird bei jedem Lauf neu gesetzt, das Ergebnis ist immer gleich.
Die rechtliche Zeile traegt "© 2026 ad.boutique", _seo.py setzt danach Firmierung und Stand ein.
Styling: assets/brand-layout.css (Abschnitt Footer).
Regel "footer" des Nachlaufs (_nachlauf.py): nach "brand", vor "ui", "headlines" und "seo".
Einzeln aufrufbar (alle Seiten): python3 _footer.py"""
import re

SKIP = ("_qa_template.html", "case-web-funkhausliving.html")

FOOTER = '''  <footer class="ftr" data-bg="#101010" data-fg="light">
    <div class="wrap ftr-in">
      <div class="ftr-top">
        <div class="ftr-h"><span>We make</span> <i>attention perform.</i></div>
        <div class="ftr-btns">
          <a class="btn btn--inverse" href="kontakt.html">Projekt starten</a>
          <a class="btn btn--outline-inverse" href="work.html">Unsere Arbeit</a>
        </div>
      </div>
      <div class="ftr-rule" aria-hidden="true"></div>
      <div class="ftr-bot">
        <a class="ftr-mark" href="index.html">ad.boutique</a>
        <nav class="ftr-links" aria-label="Rechtliches und Social Media">
          <a href="https://www.ad.boutique/impressum" target="_blank" rel="noopener">Impressum</a>
          <a href="https://www.ad.boutique/datenschutz" target="_blank" rel="noopener">Datenschutz</a>
          <a href="#cookie-einstellungen" data-consent-open>Cookie-Einstellungen</a>
          <a href="https://www.instagram.com/ad.boutique.vienna/" target="_blank" rel="noopener">Instagram</a>
          <a href="https://www.linkedin.com/company/ad-boutique/" target="_blank" rel="noopener">LinkedIn</a>
        </nav>
        <span class="ftr-loc">Digitale Marketing Agentur Wien</span>
      </div>
      <p class="ftr-legal">© 2026 ad.boutique</p>
    </div>
  </footer>'''

RX = re.compile(r"[ \t]*<footer\b.*?</footer>", re.S)


def apply(h):
    """Setzt den einen Footer ein. Seiten ohne Footer bekommen ihn vor </main> bzw. </body>."""
    if RX.search(h):
        return RX.sub(lambda m: FOOTER, h, count=1)
    for end in ("</main>", "</body>"):
        if end in h:
            return h.replace(end, FOOTER + "\n\n" + end, 1)
    return h


ZAEHLER = {"n": 0}


def seite(f, h):
    """Regel "footer" des Nachlaufs (_nachlauf.py): der eine Footer, ausser auf SKIP-Seiten und Weiterleitungen."""
    if f in SKIP or (f.endswith("-brand.html") and not f.startswith("case-")):
        return h
    if 'http-equiv="refresh"' in h:
        return h
    out = apply(h)
    if out != h:
        ZAEHLER["n"] += 1
    elif not RX.search(out):
        print("  ! %s: Footer nicht gesetzt, weder <footer> noch </main> oder </body> gefunden" % f)
    return out


def bericht():
    return "Footer in %d Seiten gesetzt" % ZAEHLER["n"]


if __name__ == "__main__":
    import _nachlauf
    _nachlauf.einzeln(seite)
    print(bericht())

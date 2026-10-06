# -*- coding: utf-8 -*-
"""Nachlauf: die Regeln, die jede Seite nach dem Erzeugen durchlaeuft, an einer Stelle und in einer Reihenfolge.

Jede Regel ist eine Funktion seite(name, html) -> html in ihrem Modul (dort steht auch, welche Seiten sie auslaesst).
Die Reihenfolge steht nur hier in SCHRITTE. Zwei Wege fuehren hindurch:
  1. Generierte Seiten (_gen.py, _gen_web.py, _gen_services.py, _gen_kontakt.py): der Generator gibt sein HTML an
     fertig(), die Regeln laufen beim Erzeugen, geschrieben wird die fertige Seite. Kein Schritt fasst sie danach an.
  2. Handgebaute Seiten (index, work, agentur, studie, case-premium-neubau, case-kommunalkredit, Weiterleitungen):
     python3 _nachlauf.py (im Build nach den Generatoren) liest sie, wendet dieselben Regeln an und schreibt sie.
Abgeleitete Seiten (*-v3.html, Tabelle ABLEITUNGEN) entstehen nach der Regel "brand" aus ihrer Quelle und laufen
danach durch die restlichen Regeln. Am Ende des Nachlaufs: Bildmasse-Cache, sitemap.xml, robots.txt, llms.txt und die
Cache-Version in den Generatoren.

Alle Regeln sind mehrfach ausfuehrbar (handgebaute Seiten tragen das Ergebnis des letzten Laufs schon in sich).
Fehlt ein Anker fuer eine Einsetzung (_anker.py), bricht der Lauf mit Regel, Seite und Anker ab."""
import glob
import importlib
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import _apply_content
import _brand_inplace
import _bump
import _footer
import _headlines
import _imgdim
import _perf
import _poster
import _seo
import _ui_markup
import _webp
from _anker import AnkerFehlt

# (Name, Regel) in der verbindlichen Reihenfolge
SCHRITTE = (
    ("inhalt", _apply_content.seite),     # Work-Kacheln und Galerien der handgebauten Cases
    ("imgdim", _imgdim.seite),            # width/height an jedes Bild
    ("poster", _poster.seite),            # Posterbilder an Videos
    ("brand", _brand_inplace.seite),      # Kopf, Brand-Bausteine, Abstaende auf Tokens
    ("footer", _footer.seite),            # der eine Footer
    ("ui", _ui_markup.seite),             # Farben, Button-Varianten, Labels
    ("headlines", _headlines.seite),      # Satoshi- und Amandine-Teil, grosse Zahlen
    ("webp", _webp.seite),                # WebP-Pfade
    ("perf", _perf.seite),                # Videos, Menuebilder, erster Bildschirm, Logos, Sprunglink
    ("seo", _seo.seite),                  # Title, Description, Canonical, Open Graph, JSON-LD, H1, Footer-Stand
    ("version", _bump.seite),             # Cache-Version ?v=
)
NAMEN = [n for n, _ in SCHRITTE]

# Quelle -> (nach Regel, abgeleitete Seite, Modul mit ableiten(html))
ABLEITUNGEN = {
    "case-premium-neubau.html": ("brand", "case-premium-neubau-v3.html", "_build_funkhaus_v3"),
    "service-performance-marketing.html": ("brand", "service-performance-marketing-v3.html", "_build_performance_v3"),
}


def bearbeite(seiten, ab=None):
    """{name: html} -> {name: html} nach allen Regeln (ab: erste Regel, z. B. "footer"), inklusive abgeleiteter Seiten.
    Regel fuer Regel ueber alle Seiten, wie die frueheren Einzelschritte."""
    seiten = dict(seiten)
    start = NAMEN.index(ab) if ab else 0
    for schritt, regel in SCHRITTE[start:]:
        for name in sorted(seiten):
            try:
                seiten[name] = regel(name, seiten[name])
            except AnkerFehlt as e:
                raise AnkerFehlt("Regel %s, Seite %s: %s" % (schritt, name, e))
        for quelle, (nach, ziel, modul) in sorted(ABLEITUNGEN.items()):
            if nach == schritt and quelle in seiten:
                try:
                    seiten[ziel] = importlib.import_module(modul).ableiten(seiten[quelle])
                except AnkerFehlt as e:
                    raise AnkerFehlt("Ableitung %s aus %s: %s" % (ziel, quelle, e))
    return seiten


def schreibe(seiten):
    """Schreibt nur geaenderte Seiten. Gibt die Zahl der geschriebenen zurueck."""
    n = 0
    for name in sorted(seiten):
        alt = open(name, encoding="utf-8").read() if os.path.exists(name) else None
        if alt != seiten[name]:
            open(name, "w", encoding="utf-8").write(seiten[name])
            n += 1
    return n


def _melde():
    """Zaehlungen und Warnungen der Regeln (Warnzeilen beginnen mit "  !" oder "  ?", _build.sh sammelt sie)."""
    for modul in (_apply_content, _imgdim, _poster, _brand_inplace, _footer, _ui_markup, _headlines, _webp, _perf):
        print(modul.bericht())


def fertig(seiten):
    """Fuer die Generatoren: {name: html} durch alle Regeln, schreiben, Bildmasse-Cache sichern. Gibt die Namen zurueck."""
    try:
        out = bearbeite(seiten)
    except AnkerFehlt as e:
        raise SystemExit("FEHLER im Nachlauf: %s" % e)
    schreibe(out)
    _imgdim.speichern()
    for z in _poster.warnungen() + _perf.warnungen():
        print(z)
    return sorted(out)


def generierte_seiten():
    """Seiten, die ein Generator schreibt (und ihre Ableitungen). Alle anderen *.html sind handgebaut."""
    from _cases import PERFORMANCE, WEB
    from _leistungen import SERVICES
    out = {c["slug"] + ".html" for c in PERFORMANCE if c["vorlage"] == "dossier"}
    out |= {c["slug"] + ".html" for c in WEB}
    out |= {s["slug"] + ".html" for s in SERVICES}
    out.add("kontakt.html")    # _gen_kontakt.py
    for quelle, (_, ziel, _) in ABLEITUNGEN.items():
        if quelle in out:
            out.add(ziel)
    return out


def handgebaute_seiten():
    """Eingaben des Nachlaufs: alle *.html ausser den generierten und den abgeleiteten Seiten."""
    weg = generierte_seiten() | {ziel for _, ziel, _ in ABLEITUNGEN.values()}
    return [f for f in sorted(glob.glob("*.html")) if f not in weg]


def einzeln(regel, namen=None):
    """Eine Regel einzeln ueber Seiten (Standard: alle *.html), fuer den Aufruf eines Regel-Moduls von Hand."""
    namen = sorted(glob.glob("*.html")) if namen is None else namen
    n = 0
    for name in namen:
        h = open(name, encoding="utf-8").read()
        try:
            out = regel(name, h)
        except AnkerFehlt as e:
            raise SystemExit("FEHLER: Seite %s: %s" % (name, e))
        if out != h:
            open(name, "w", encoding="utf-8").write(out)
            n += 1
    return n


def main():
    _webp.convert()
    namen = handgebaute_seiten()
    seiten = {f: open(f, encoding="utf-8").read() for f in namen}
    try:
        out = bearbeite(seiten)
    except AnkerFehlt as e:
        raise SystemExit("FEHLER im Nachlauf: %s" % e)
    n = schreibe(out)
    _imgdim.speichern()
    sitemap = _seo.dateien()
    q = _bump.quellen()
    _melde()
    print(_seo.bericht(sitemap))
    print("Nachlauf: %d handgebaute Seiten, %d abgeleitet, %d geschrieben, v=%s%s"
          % (len(namen), len(out) - len(namen), n, _bump.version(), (", Generatoren %d" % q) if q else ""))


if __name__ == "__main__":
    main()

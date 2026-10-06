# Web-Case-Generator: Homepage-Cases (neue Website inkl. Strategie), ohne erfundene KPIs
# Inhalte in _content/cases/case-web-*.json (Vorlage "web"), Bausteine in _bausteine.py, Laden und Pruefen in _cases.py.
# Bildnamen der Website-Cases: web_<name>_d.jpg (Hero), web_<name>_d1/d2 (Buehne und Unterseiten), web_<name>_ds0..2
# (Unterseiten), web_<name>_m0..m2 + web_<name>_ms0..1 (mobil). Die Inhaltsdatei nennt die Bilder ausdruecklich.
# Anleitung fuer neue Cases: docs/CMS-CASES.md.
# -*- coding: utf-8 -*-
from _gen import HEAD, FOOTER, menu
from _cases import WEB
from _bausteine import koerper


def page(c):
    return (HEAD.format(title="Case, " + c["meta"]["name"], bodybg="#0E0E10") + menu("work.html", back=True)
            + "<main>\n\n" + koerper(c) + FOOTER)


if __name__ == "__main__":
    # fertig(): die Nachlauf-Regeln (_nachlauf.py) laufen gleich beim Erzeugen, geschrieben wird die fertige Seite
    import _nachlauf
    for name in _nachlauf.fertig({c["slug"] + ".html": page(c) for c in WEB}):
        print("webcase", name[:-5])
    print("webcases done")

# -*- coding: utf-8 -*-
"""Anker fuer Einsetzungen in fertiges HTML (handgebaute Seiten, Vorschau-Ableitungen *-v3.html).

Statt assert (faellt mit python -O weg und meldet nur ein Tupel) gibt es hier AnkerFehlt mit Zweck, Trefferzahl
und dem gesuchten Text. Der Nachlauf (_nachlauf.py) ergaenzt Regel und Seite, der Build bricht mit dieser Meldung ab.
Bevorzugt werden Marker-Kommentare (<!-- NEXT CASE -->) oder Struktur (id, Klasse) statt Fliesstext: ein geaenderter
Satz soll keine Einsetzung brechen."""


class AnkerFehlt(Exception):
    pass


def _kurz(s):
    s = s.strip().replace("\n", " ")
    return s if len(s) <= 70 else s[:67] + "..."


def einmal(h, alt, neu, was, anzahl=1):
    """Ersetzt alt durch neu; alt muss genau anzahl mal vorkommen."""
    n = h.count(alt)
    if n != anzahl:
        raise AnkerFehlt("%s: Anker %d mal gefunden, erwartet %d: %r" % (was, n, anzahl, _kurz(alt)))
    return h.replace(alt, neu)


def finde(h, anker, was, ab=0):
    """Position von anker ab ab, sonst AnkerFehlt."""
    i = h.find(anker, ab)
    if i < 0:
        raise AnkerFehlt("%s: Anker fehlt: %r" % (was, _kurz(anker)))
    return i


def sektion(h, anker, was):
    """(a, b) der Sektion, die anker enthaelt: vom einleitenden Kommentar bzw. "  <section" bis nach </section> und den
    folgenden Leerzeilen."""
    i = finde(h, anker, was)
    a = h.rfind("  <section", 0, i)
    if a < 0:
        raise AnkerFehlt("%s: keine <section> um den Anker %r" % (was, _kurz(anker)))
    b = finde(h, "</section>", was + " (Ende der Sektion)", i) + len("</section>")
    while b < len(h) and h[b] == "\n":
        b += 1
    # Kommentarzeile davor mitnehmen
    c = h.rfind("  <!--", 0, a)
    if c >= 0 and "\n" not in h[c:a].strip("\n"):
        a = c
    return a, b

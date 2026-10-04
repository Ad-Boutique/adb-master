# -*- coding: utf-8 -*-
"""Leistungs-CMS: liest die Inhaltsdateien _content/services/<slug>.json und prueft sie.

Eine Datei je Leistungsseite (analog zu den Cases in _content/cases, siehe _cases.py). Die Datei enthaelt alle Texte,
Zahlen und Bilder der Seite, dazu den Suchmaschinen-Teil (seo), den Woerterbuch-Hero (dhero) und das Kennzahlen-Board
(kennzahlen, geteilte Karten aus den Case-Dateien per ref). Das Markup steht in _tpl_services.py, gebaut wird mit
_gen_services.py, gelesen werden die Daten ausserdem von _seo.py (Title, Description, llms.txt).
Dateien, deren Name mit "_" beginnt, werden nicht gebaut. Felder und Anleitung: docs/CMS-LEISTUNGEN.md.

Pruefen ohne Bauen: python3 _leistungen.py"""
import glob
import json
import os

from _cases import Fehler, board as _board, NACH_SLUG as _CASES, HAND as _HAND

ORDNER = "_content/services"

DRAMATURGIEN = ("v2", "v1")
VISUAL = ("panels", "phones", "stage")

# Pflichtfelder je Dramaturgie (v2 ist die aller Seiten, v1 die fruehere mit Akkordeon und Differenzierung)
PFLICHT = ("slug", "reihenfolge", "nav", "flow", "seo", "dhero", "tags", "sub", "zoom", "visual", "proof_h",
           "oplist", "faq", "offer_h", "offer", "chips")
PFLICHT_V1 = ("h1", "intro", "acc", "diff")
SEO_FELDER = ("label", "title", "desc", "answer", "faq_first", "faq_last")
DHERO_FELDER = ("word", "kicker", "text", "img", "alt")
ZOOM_FELDER = ("side", "aside", "img", "zl", "zt")

# Listen aus Objekten: Feld -> Pflichtschluessel jedes Eintrags
EINTRAEGE = {
    "bene": ("titel", "text"),
    "acc": ("titel", "text", "punkte"),
    "diff": ("kicker", "titel", "text", "bild"),
    "oplist": ("href", "titel", "wert", "label"),
    "faq": ("frage", "antwort"),
    "proof_nums": ("wert", "label"),
}


def _lade(pfad):
    try:
        with open(pfad, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as e:
        raise Fehler("%s: kein gueltiges JSON (%s)" % (pfad, e))


def _pruefe(s, pfad):
    """Pflichtfelder und Typen. Meldet den ersten Fehler mit Dateiname und Feld."""
    def need(cond, msg):
        if not cond:
            raise Fehler("%s: %s" % (pfad, msg))
    need(isinstance(s, dict), "Datei muss ein Objekt sein")
    flow = s.get("flow")
    need(flow in DRAMATURGIEN, "flow muss eine von %s sein" % ", ".join(DRAMATURGIEN))
    for k in PFLICHT + (PFLICHT_V1 if flow == "v1" else ()):
        need(k in s, "Feld '%s' fehlt" % k)
    need(s["slug"] + ".json" == os.path.basename(pfad), "Dateiname muss <slug>.json sein (slug ist '%s')" % s["slug"])
    need(s["slug"].startswith("service-"), "slug beginnt mit 'service-'")
    need(isinstance(s["reihenfolge"], (int, float)), "reihenfolge muss eine Zahl sein")
    for k in SEO_FELDER:
        need(k in s["seo"], "seo.%s fehlt" % k)
    need(isinstance(s["seo"]["faq_first"], dict) and s["seo"]["faq_first"].get("frage") and "antwort" in s["seo"]["faq_first"],
         "seo.faq_first braucht frage und antwort")
    for i, q in enumerate(s["seo"]["faq_last"]):
        need(isinstance(q, dict) and q.get("frage") and "antwort" in q, "seo.faq_last[%d] braucht frage und antwort" % i)
    for k in DHERO_FELDER:
        need(s["dhero"].get(k), "dhero.%s fehlt" % k)
    for k in ZOOM_FELDER:
        need(k in s["zoom"], "zoom.%s fehlt" % k)
    need(s["zoom"]["side"] in ("left", "right"), "zoom.side muss left oder right sein")
    need(s["visual"].get("art") in VISUAL, "visual.art muss eine von %s sein" % ", ".join(VISUAL))
    need(isinstance(s["proof_h"], list) and len(s["proof_h"]) == 2, "proof_h braucht genau zwei Zeilen")
    need(isinstance(s["offer"], list) and len(s["offer"]) == 2, "offer braucht genau zwei Absaetze")
    need("quote" in s or "proof_quote" in s, "proof_quote fehlt (oder quote)")
    for feld, keys in EINTRAEGE.items():
        for i, e in enumerate(s.get(feld) or []):
            need(isinstance(e, dict), "%s[%d] muss ein Objekt sein" % (feld, i))
            for k in keys:
                need(k in e, "%s[%d]: Feld '%s' fehlt" % (feld, i, k))
    for i, o in enumerate(s["oplist"]):
        need(o["href"][:-5] in _CASES or any(c.get("seite") == o["href"] for c in _HAND),
             "oplist[%d]: Case '%s' gibt es nicht" % (i, o["href"]))
    k = s.get("kennzahlen")
    if k:
        for i, x in enumerate(k.get("karten", [])):
            need(x.get("ref"), "kennzahlen.karten[%d]: ref fehlt (Leistungsseiten nutzen geteilte Karten)" % i)


def lade_alle(ordner=ORDNER):
    out = []
    for p in sorted(glob.glob(os.path.join(ordner, "*.json"))):
        if os.path.basename(p).startswith("_"):
            continue
        s = _lade(p)
        _pruefe(s, p)
        out.append(s)
    slugs = [s["slug"] for s in out]
    doppelt = {x for x in slugs if slugs.count(x) > 1}
    if doppelt:
        raise Fehler("slug doppelt: %s" % ", ".join(sorted(doppelt)))
    out.sort(key=lambda s: (s["reihenfolge"], s["slug"]))
    return out


try:
    SERVICES = lade_alle()
except Fehler as _e:
    if __name__ == "__main__":
        raise SystemExit("FEHLER in den Leistungsdateien: %s" % _e)
    raise
NACH_SLUG = {s["slug"]: s for s in SERVICES}


def faq_liste(s):
    """FAQ der Seite: erst die Suchfrage seo.faq_first, dann die eigenen Fragen (ohne Dublette der ersten),
    dann seo.faq_last (ohne Fragen, die schon dastehen)."""
    seo = s["seo"]
    first = seo["faq_first"]
    eigene = s["faq"]
    return ([first] + [q for q in eigene if q["frage"] != first["frage"]]
            + [q for q in seo["faq_last"] if q["frage"] not in [x["frage"] for x in eigene]])


def kennzahlen(s):
    """Kennzahlen-Board als Dict fuer _kpi.board() (geteilte Karten aus den Case-Dateien) oder None."""
    return _board(s)


def fehlende_dateien(s):
    """Pfade unter assets/, die in der Datei stehen, aber nicht existieren."""
    out = []

    def walk(o):
        if isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str) and o.startswith("assets/") and not os.path.exists(o):
            out.append(o)
    walk(s)
    return out


if __name__ == "__main__":
    import sys
    try:
        for s in SERVICES:
            kennzahlen(s)
    except Fehler as e:
        raise SystemExit("FEHLER in den Leistungsdateien: %s" % e)
    for s in SERVICES:
        for p in fehlende_dateien(s):
            sys.stderr.write("Hinweis: %s nennt %s, die Datei fehlt\n" % (s["slug"], p))
    print("%d Leistungsdateien in Ordnung: %s" % (len(SERVICES), ", ".join(s["slug"][len("service-"):] for s in SERVICES)))

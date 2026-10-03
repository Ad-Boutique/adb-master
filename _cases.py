# -*- coding: utf-8 -*-
"""Case-CMS: liest die Inhaltsdateien _content/cases/<slug>.json und prueft sie.

Eine Datei je Case. Die Generatoren (_gen.py, _gen_web.py, _kpi.py, _apply_content.py, _gen_services.py, _seo.py)
lesen die Inhalte nur noch ueber dieses Modul. Dateien, deren Name mit "_" beginnt (z. B. _vorlage.json), werden
nicht gebaut. Anleitung, Felder und Baustein-Typen: docs/CMS-CASES.md.

Aufbau einer Datei (Vorlagen "dossier" und "web"): Rahmen aus meta, hero, intro, kennzahlen und naechster,
dazwischen die Liste bausteine, die in ihrer Reihenfolge auf die Seite kommt.
Vorlage "handgebaut": die Seite selbst ist handgebaut (Feld seite), die Datei liefert Meta, Teaser, Kennzahlen
und die Galerie.

Pruefen ohne Bauen: python3 _cases.py"""
import glob
import json
import os

ORDNER = "_content/cases"

VORLAGEN = ("dossier", "web", "handgebaut")
KETTEN = ("performance", "web", None)

# Baustein-Typen je Vorlage (Reihenfolge auf der Seite = Reihenfolge in "bausteine")
BAUSTEINE = {
    "dossier": ("statement", "perspektiven", "ergebnis", "kapitel", "zitat", "mobil", "learnings", "galerie"),
    "web": ("buehne", "mobil", "unterseiten", "galerie", "kapitel", "zitat", "stimme"),
    "handgebaut": ("galerie",),
}

# Pflichtfelder je Baustein-Typ
FELDER = {
    "statement": ("zeilen",), "perspektiven": ("zeilen",), "ergebnis": ("zahlen",),
    "kapitel": ("label", "headline", "absatz1", "absatz2"), "zitat": ("text", "wer"),
    "mobil": ("headline", "text", "bilder"), "learnings": ("saetze",), "galerie": ("medien",),
    "buehne": ("bild",), "unterseiten": ("bilder",), "stimme": ("label", "text", "wer", "video", "notiz"),
}

# Kartenarten des KPI-Boards: Name in der Datei -> Name im Markup (Klasse kpi--...)
ARTEN = {"sprung": "jump", "zaehler": "count", "text": "text", "medien": "media", "zitat": "quote"}


class Fehler(Exception):
    pass


def _lade(pfad):
    try:
        with open(pfad, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as e:
        raise Fehler("%s: kein gueltiges JSON (%s)" % (pfad, e))


def _pruefe(c, pfad):
    """Pflichtfelder und Typen. Meldet den ersten Fehler mit Dateiname, damit er schnell zu finden ist."""
    def need(cond, msg):
        if not cond:
            raise Fehler("%s: %s" % (pfad, msg))
    need(isinstance(c, dict), "Datei muss ein Objekt sein")
    for k in ("slug", "vorlage", "reihenfolge", "meta"):
        need(k in c, "Feld '%s' fehlt" % k)
    need(c["slug"] + ".json" == os.path.basename(pfad), "Dateiname muss <slug>.json sein (slug ist '%s')" % c["slug"])
    need(c["slug"].startswith("case-"), "slug beginnt mit 'case-'")
    need(c["vorlage"] in VORLAGEN, "vorlage muss eine von %s sein" % ", ".join(VORLAGEN))
    need(c.get("kette") in KETTEN, "kette muss 'performance', 'web' oder null sein")
    need(isinstance(c["reihenfolge"], (int, float)), "reihenfolge muss eine Zahl sein")
    m = c["meta"]
    need(m.get("name"), "meta.name fehlt")
    if c["vorlage"] == "dossier":
        for k in ("titel", "branche", "zeitraum", "kanaele", "leistungen"):
            need(k in m, "meta.%s fehlt" % k)
        need(c.get("hero", {}).get("headline"), "hero.headline fehlt")
        for k in ("these", "text"):
            need(c.get("intro", {}).get(k), "intro.%s fehlt" % k)
        need(c.get("kette") == "performance", "Vorlage dossier gehoert in die kette 'performance'")
    elif c["vorlage"] == "web":
        for k in ("branche", "url", "umfang", "leistungen"):
            need(k in m, "meta.%s fehlt" % k)
        need(c.get("hero", {}).get("headline") and c["hero"].get("bild"), "hero.headline und hero.bild fehlen")
        need(c.get("intro", {}).get("text"), "intro.text fehlt")
        need(c.get("kette") == "web", "Vorlage web gehoert in die kette 'web'")
    else:
        need(c.get("seite"), "Vorlage handgebaut braucht das Feld 'seite' (die handgebaute HTML-Datei)")
    erlaubt = BAUSTEINE[c["vorlage"]]
    for i, b in enumerate(c.get("bausteine", [])):
        need(isinstance(b, dict) and b.get("typ") in erlaubt,
             "bausteine[%d]: typ '%s' gibt es in der Vorlage %s nicht (erlaubt: %s)" % (i, b.get("typ") if isinstance(b, dict) else b, c["vorlage"], ", ".join(erlaubt)))
        for k in FELDER[b["typ"]]:
            need(k in b, "bausteine[%d] (%s): Feld '%s' fehlt" % (i, b["typ"], k))
    for i, k in enumerate((c.get("kennzahlen") or {}).get("karten", [])):
        if k.get("ref"):
            continue
        need(k.get("art") in ARTEN, "kennzahlen.karten[%d]: art muss eine von %s sein" % (i, ", ".join(ARTEN)))
        need(k.get("label"), "kennzahlen.karten[%d]: label fehlt" % i)


def lade_alle(ordner=ORDNER):
    out = []
    for p in sorted(glob.glob(os.path.join(ordner, "*.json"))):
        if os.path.basename(p).startswith("_"):
            continue
        c = _lade(p)
        if isinstance(c, dict) and not c.get("kette"):
            # leere Kette (z. B. "" aus dem Web-Editor) heisst: in keiner Kette
            c["kette"] = None
        _pruefe(c, p)
        out.append(c)
    slugs = [c["slug"] for c in out]
    doppelt = {s for s in slugs if slugs.count(s) > 1}
    if doppelt:
        raise Fehler("slug doppelt: %s" % ", ".join(sorted(doppelt)))
    out.sort(key=lambda c: (c["reihenfolge"], c["slug"]))
    return out


try:
    ALLE = lade_alle()
except Fehler as _e:
    if __name__ == "__main__":
        raise SystemExit("FEHLER in den Inhaltsdateien: %s" % _e)
    raise
NACH_SLUG = {c["slug"]: c for c in ALLE}


def kette(name):
    """Cases einer Kette in ihrer Reihenfolge (performance: Dossiers und Funkhaus, web: Website-Cases)."""
    return [c for c in ALLE if c.get("kette") == name]


PERFORMANCE = kette("performance")
WEB = kette("web")
HAND = [c for c in ALLE if c["vorlage"] == "handgebaut"]


def naechster(c):
    """Case fuer die Next-Kachel: Feld "naechster" (Slug) oder "auto" bzw. leer = der folgende Case der Kette."""
    n = c.get("naechster")
    if n and n != "auto":
        if n not in NACH_SLUG:
            raise Fehler("%s: naechster '%s' gibt es nicht" % (c["slug"], n))
        return NACH_SLUG[n]
    k = kette(c.get("kette"))
    return k[(k.index(c) + 1) % len(k)]


def teaser(c):
    """Was die Next-Kachel des Vorgaengers von diesem Case zeigt. Handgebaute Seiten tragen ein eigenes Feld teaser."""
    t = c.get("teaser")
    if t:
        return dict(titel=t["titel"], zeile=t["zeile"], bild=t.get("bild"))
    h = c.get("hero", {})
    return dict(titel=c["meta"].get("titel", [c["meta"]["name"]]), zeile=h.get("headline", ""), bild=h.get("bild"))


def leistungen(c):
    """[(Titel, Seite)] der Leistungsseiten, die der Case verlinkt."""
    return [(l["titel"], l["seite"]) for l in c["meta"].get("leistungen", [])]


def rahmen(c):
    """Branche, Zeitraum, Kanaele als die eine Zeile mit <br>, wie sie die Dossier-Vorlage zerlegt."""
    m = c["meta"]
    return "<br>".join((m["branche"], m["zeitraum"], m["kanaele"]))


def bausteine(c, typ=None):
    """Sichtbare Bausteine (ohne "ausgeblendet": true), optional nur ein Typ."""
    return [b for b in c.get("bausteine", []) if not b.get("ausgeblendet") and (typ is None or b["typ"] == typ)]


# ---------------------------------------------------------------- KPI-Karten
def _karte_intern(k):
    """Karte aus der Datei -> Karten-Dict, wie es _kpi.card() rendert."""
    d = {"kind": ARTEN[k["art"]], "l": k["label"]}
    if k.get("vorher"):
        d["frm"] = k["vorher"]
    if "wert" in k:
        d["to"] = k["wert"]
    if k.get("einheit"):
        d["unit"] = k["einheit"]
    if k.get("zaehlen"):
        z = k["zaehlen"]
        d["cnt"] = (z["von"], z["bis"], int(z.get("dezimalen", 0)), z.get("vor", ""), z.get("nach", ""))
    if k.get("badge"):
        d["pill"] = k["badge"]
    if "zitat" in k:
        d["q"] = k["zitat"]
        d["a"] = k.get("wer", "")
    if k.get("linie"):
        d["line"] = list(k["linie"])
    if k.get("reihen"):
        d["rows"] = [(r["label"], int(r["punkte"]), int(r["an"]), bool(r.get("hervorgehoben"))) for r in k["reihen"]]
    if k.get("waffel"):
        w = k["waffel"]
        d["waffle"] = (int(w["gesamt"]), int(w["wert"]), int(w["spalten"]))
    if k.get("stationen"):
        d["stations"] = list(k["stationen"])
    if k.get("bilder"):
        d["imgs"] = list(k["bilder"])
    if k.get("text"):
        d["cap"] = k["text"]
    if k.get("link") and k["link"].get("href"):
        d["link"] = (k["link"]["href"], k["link"]["text"])
    return d


def _karten_register():
    reg = {}
    for c in ALLE:
        for k in (c.get("kennzahlen") or {}).get("karten", []):
            if k.get("id"):
                if k["id"] in reg:
                    raise Fehler("%s: Karten-id '%s' gibt es schon" % (c["slug"], k["id"]))
                reg[k["id"]] = _karte_intern(k)
    return reg


KARTEN = _karten_register()


def karte(kid, link=None):
    """Geteilte Karte nach id (z. B. fuer Leistungsseiten), optional mit Link (href, text)."""
    if kid not in KARTEN:
        raise Fehler("Karten-id '%s' gibt es in keiner Case-Datei" % kid)
    d = dict(KARTEN[kid])
    if link:
        d["link"] = tuple(link)
    return d


def board(c):
    """KPI-Board eines Cases als Dict fuer _kpi.board(): h, cards, optional label und note. None ohne Kennzahlen."""
    k = c.get("kennzahlen")
    if not k or k.get("ausgeblendet"):
        return None
    cards = []
    for x in k["karten"]:
        if x.get("ref"):
            l = x.get("link") or {}
            cards.append(karte(x["ref"], (l["href"], l["text"]) if l.get("href") else None))
        else:
            cards.append(_karte_intern(x))
    b = dict(h=tuple(k.get("headline", ("Was besser wurde,", "in drei Zahlen."))), cards=cards)
    if k.get("label"):
        b["label"] = k["label"]
    if k.get("fussnote"):
        b["note"] = k["fussnote"]
    return b


def fehlende_dateien(c):
    """Pfade unter assets/, die in der Inhaltsdatei stehen, aber nicht existieren."""
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
    walk(c)
    return out


if __name__ == "__main__":
    import sys
    try:
        for c in ALLE:
            if c.get("kette"):
                naechster(c)
            board(c)
    except Fehler as e:
        raise SystemExit("FEHLER in den Inhaltsdateien: %s" % e)
    for c in ALLE:
        for p in fehlende_dateien(c):
            # kein Abbruch: Galerie, Bildstreifen und Unterseiten lassen fehlende Dateien aus
            sys.stderr.write("Hinweis: %s nennt %s, die Datei fehlt\n" % (c["slug"], p))
    print("%d Case-Dateien in Ordnung: %d Performance, %d Web, %d handgebaut" % (len(ALLE), len(PERFORMANCE), len(WEB), len(HAND)))

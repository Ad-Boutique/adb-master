# Traegt in alle <video>-Tags das passende Posterbild ein (<pfad>-poster.jpg), damit kein
# Video als Loch erscheint, solange es nicht laeuft. Regel "poster" des Nachlaufs (_nachlauf.py), nach "imgdim".
# Poster erzeugen: ./_tools/poster <video> <video ohne .mp4>-poster.jpg 0.8
# Einzeln aufrufbar (alle Seiten): python3 _poster.py
# -*- coding: utf-8 -*-
import os, re

ZAEHLER = {"tags": 0, "dateien": 0}
missing = set()


def seite(f, s):
    """Regel "poster": Posterbild an jedes Video mit vorhandener <pfad>-poster.jpg."""
    orig = s

    def fix(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+\.mp4)"', tag)
        if not src:
            return tag
        poster = src.group(1)[:-4] + "-poster.jpg"
        if not os.path.exists(poster):
            missing.add(src.group(1))
            return tag
        cur = re.search(r'\sposter="([^"]*)"', tag)
        if cur:
            if cur.group(1) == poster:
                return tag
            tag = tag.replace(cur.group(0), ' poster="%s"' % poster)
        else:
            tag = tag[:-1].rstrip() + ' poster="%s">' % poster
        ZAEHLER["tags"] += 1
        return tag

    s = re.sub(r"<video\b[^>]*>", fix, s)
    if s != orig:
        ZAEHLER["dateien"] += 1
    return s


def warnungen():
    """Videos ohne Posterbild als eine Warnzeile. Leert die Liste."""
    out = ["  ohne Posterbild: " + ", ".join(sorted(missing))] if missing else []
    missing.clear()
    return out


def bericht():
    return "\n".join(warnungen() + ["Video-Poster ergaenzt: %d Tags in %d Dateien" % (ZAEHLER["tags"], ZAEHLER["dateien"])])


if __name__ == "__main__":
    import _nachlauf
    _nachlauf.einzeln(seite)
    print(bericht())

# Setzt die Cache-Version ?v= in allen Seiten und Generatoren einheitlich (Technik B7).
# Die Nummer ist ein kurzer Inhalts-Hash von assets/site.css und assets/site.js (8 Ziffern, nur Ziffern, damit alle
# Muster mit \d+ in den anderen Schritten weiter greifen). Sie aendert sich nur, wenn sich CSS oder JS wirklich aendern:
# ein Build ohne Aenderung laesst die Seiten unberuehrt, wiederkehrende Besucher laden nichts neu.
# Regel "version" des Nachlaufs (_nachlauf.py), die letzte Regel; deshalb laeuft _css.py im Build vor den Generatoren.
# quellen() setzt dieselbe Nummer in die Generatoren (_gen*.py, Kopf in _gen.py).
# Einzeln aufrufbar (alle Seiten und Generatoren): python3 _bump.py [feste Nummer]
import glob, hashlib, re, sys

pat = re.compile(r'(?:site|master|brand(?:-[a-z]+)?)\.(css|js)\?v=(\d+)')
_V = []


def version():
    """Inhalts-Hash von site.css und site.js (oder die feste Nummer aus dem Aufruf)."""
    if not _V:
        if __name__ == "__main__" and len(sys.argv) > 1:
            _V.append(sys.argv[1])
        else:
            h = hashlib.sha1()
            for p in ("assets/site.css", "assets/site.js"):
                h.update(open(p, "rb").read())
            _V.append("%08d" % (int(h.hexdigest()[:12], 16) % 10 ** 8))
    return _V[0]


def seite(f, s):
    """Regel "version": ?v= an site.css und site.js (auch an aelteren Einzeldateien) auf die aktuelle Nummer."""
    new = version()
    return pat.sub(lambda m: "%s.%s?v=%s" % (m.group(0).split(".")[0], m.group(1), new), s)


def quellen():
    """Dieselbe Nummer in die Generatoren (_gen*.py). Gibt die Zahl der geaenderten Dateien zurueck."""
    n = 0
    for f in sorted(glob.glob("_gen*.py")):
        s = open(f, encoding="utf-8").read()
        out = seite(f, s)
        if out != s:
            open(f, "w", encoding="utf-8").write(out); n += 1
    return n


if __name__ == "__main__":
    files = sorted(set(glob.glob("*.html") + glob.glob("_gen*.py")))
    olds = sorted(set(m.group(2) for f in files for m in pat.finditer(open(f, encoding="utf-8").read())))
    n = 0
    for f in files:
        s = open(f, encoding="utf-8").read()
        out = seite(f, s)
        if out != s:
            open(f, "w", encoding="utf-8").write(out); n += 1
    print("v=%s -> v=%s in %d Dateien" % (",".join(olds) or "-", version(), n))

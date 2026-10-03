# Setzt die Cache-Version ?v= in allen Seiten und Generatoren einheitlich (Technik B7).
# Die Nummer ist ein kurzer Inhalts-Hash von assets/site.css und assets/site.js (8 Ziffern, nur Ziffern, damit alle
# Muster mit \d+ in den anderen Schritten weiter greifen). Sie aendert sich nur, wenn sich CSS oder JS wirklich aendern:
# ein Build ohne Aenderung laesst die Seiten unberuehrt, wiederkehrende Besucher laden nichts neu.
# Aufruf: python3 _bump.py [feste Nummer]
import glob, hashlib, re, sys

pat = re.compile(r'(?:site|master|brand(?:-[a-z]+)?)\.(css|js)\?v=(\d+)')
files = sorted(set(glob.glob("*.html") + glob.glob("_gen*.py")))
if len(sys.argv) > 1:
    new = sys.argv[1]
else:
    h = hashlib.sha1()
    for p in ("assets/site.css", "assets/site.js"):
        h.update(open(p, "rb").read())
    new = "%08d" % (int(h.hexdigest()[:12], 16) % 10 ** 8)
olds = sorted(set(m.group(2) for f in files for m in pat.finditer(open(f, encoding="utf-8").read())))
n = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    out = pat.sub(lambda m: "%s.%s?v=%s" % (m.group(0).split(".")[0], m.group(1), new), s)
    if out != s:
        open(f, "w", encoding="utf-8").write(out); n += 1
print("v=%s -> v=%s in %d Dateien" % (",".join(olds) or "-", new, n))

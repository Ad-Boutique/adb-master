# Hebt die Cache-Version in allen Seiten und Generatoren einheitlich an.
# Aufruf: python3 _bump.py [neue Nummer]  (ohne Argument: aktuelle + 1)
import glob, re, sys

pat = re.compile(r'master\.(css|js)\?v=(\d+)')
files = sorted(set(glob.glob("*.html") + glob.glob("_gen*.py")))
cur = max((int(m.group(2)) for f in files for m in pat.finditer(open(f, encoding="utf-8").read())), default=0)
new = int(sys.argv[1]) if len(sys.argv) > 1 else cur + 1
n = 0
for f in files:
    s = open(f, encoding="utf-8").read()
    out = pat.sub(lambda m: "master.%s?v=%d" % (m.group(1), new), s)
    if out != s:
        open(f, "w", encoding="utf-8").write(out); n += 1
print("v=%d -> v=%d in %d Dateien" % (cur, new, n))

# Vergleicht zwei Fingerabdruck-Ordner (_tools/fp.sh) und meldet Seiten mit Abweichungen.
# Aufruf: python3 _tools/fpdiff.py vorher/ nachher/ [max_zeilen]
import json, os, sys, difflib
a, b = sys.argv[1], sys.argv[2]; mx = int(sys.argv[3]) if len(sys.argv) > 3 else 6
import re
VOL = re.compile(r"\b(in|vis|on|lit|is-on|is-best|zdone|inview|active|playing|cur|loaded|mready|ready|done|show|shown|gone|mb-[a-z]+)\b")
def norm(line):
    # fluechtig: Klassen-Zustaende, Opazitaet (Index 24), Transform (Index 25), Lage auf 4 px gerundet
    f = line.split("\u00a6")
    if len(f) > 26:
        f[1] = " ".join(VOL.sub("", f[1]).split())
        for k in (2, 3, 4, 5):
            try: f[k] = str(round(int(f[k]) / 4) * 4)
            except ValueError: pass
        f[24] = f[25] = ""
    return "\u00a6".join(f)
bad = 0
for f in sorted(os.listdir(a)):
    pa, pb = os.path.join(a, f), os.path.join(b, f)
    if not os.path.exists(pb): print("FEHLT", f); bad += 1; continue
    try: ja, jb = json.load(open(pa)), json.load(open(pb))
    except Exception as e: print("LESEFEHLER", f, e); bad += 1; continue
    ia, ib = [norm(x) for x in ja["items"]], [norm(x) for x in jb["items"]]
    if ia == ib: continue
    bad += 1; d = [l for l in difflib.unified_diff(ia, ib, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    print("ABWEICHUNG %s: %d Zeilen" % (f, len(d)))
    for l in d[:mx]: print("   ", l[:260])
print("Seiten mit Abweichung:", bad)

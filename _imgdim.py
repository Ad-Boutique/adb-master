# Schreibt width/height in alle Bild-Tags, damit lazy geladene Bilder ihren
# Platz reservieren. Masse werden in assets/imgdim.json gecacht.
# Masse per PIL (frueher sips, nur macOS): laeuft so auch auf Linux (Vercel, GitHub Actions).
# Regel "imgdim" des Nachlaufs (_nachlauf.py): seite(name, html); speichern() schreibt den Cache.
# Einzeln aufrufbar (alle Seiten): python3 _imgdim.py
import os, re, json
from PIL import Image
CACHE = "assets/imgdim.json"
dims = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
ZAEHLER = {"n": 0}
def dim(p):
    if p in dims: return dims[p]
    if not os.path.exists(p): dims[p] = None; return None
    try:
        with Image.open(p) as im: dims[p] = [int(im.width), int(im.height)]
    except Exception:
        print("  ! Bildmasse nicht lesbar:", p); dims[p] = None
    return dims[p]
TAG, SRC = re.compile(r'<img\b[^>]*>'), re.compile(r'src="([^"]+)"')
def seite(f, s):
    """Regel "imgdim": width/height an jedes Bild ohne width (Seiten, deren Name mit _ beginnt, bleiben)."""
    if f.startswith("_"): return s
    parts=[]
    for m in TAG.finditer(s):
        t = m.group(0)
        if "width=" in t: continue
        ms = SRC.search(t)
        if not ms or ms.group(1).startswith(("data:","http")): continue
        d = dim(ms.group(1))
        if d: parts.append((m.start(), m.end(), t[:-1].rstrip()+' width="%d" height="%d">'%(d[0],d[1]))); ZAEHLER["n"]+=1
    for a,b,new in reversed(parts): s = s[:a]+new+s[b:]
    return s
def speichern():
    """Cache schreiben, wenn neue Masse dazugekommen sind."""
    old = open(CACHE).read() if os.path.exists(CACHE) else None
    new = json.dumps(dims)
    if new != old: open(CACHE,"w").write(new)
def bericht():
    return "Bildmasse ergaenzt: %d" % ZAEHLER["n"]
if __name__ == "__main__":
    import _nachlauf
    _nachlauf.einzeln(seite)
    speichern()
    print(bericht())

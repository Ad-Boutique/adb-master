# Schreibt width/height in alle Bild-Tags, damit lazy geladene Bilder ihren
# Platz reservieren. Masse werden in assets/imgdim.json gecacht.
import glob, os, re, subprocess, json
CACHE = "assets/imgdim.json"
dims = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def dim(p):
    if p in dims: return dims[p]
    if not os.path.exists(p): dims[p] = None; return None
    o = subprocess.run(["sips","-g","pixelWidth","-g","pixelHeight",p],capture_output=True,text=True).stdout
    mw, mh = re.search(r"pixelWidth:\s*(\d+)",o), re.search(r"pixelHeight:\s*(\d+)",o)
    dims[p] = [int(mw.group(1)),int(mh.group(1))] if mw and mh else None
    return dims[p]
TAG, SRC = re.compile(r'<img\b[^>]*>'), re.compile(r'src="([^"]+)"')
n = 0
for f in sorted(glob.glob("*.html")):
    if f.startswith("_"): continue
    s = open(f,encoding="utf-8").read(); parts=[]
    for m in TAG.finditer(s):
        t = m.group(0)
        if "width=" in t: continue
        ms = SRC.search(t)
        if not ms or ms.group(1).startswith(("data:","http")): continue
        d = dim(ms.group(1))
        if d: parts.append((m.start(), m.end(), t[:-1].rstrip()+' width="%d" height="%d">'%(d[0],d[1]))); n+=1
    for a,b,new in reversed(parts): s = s[:a]+new+s[b:]
    if parts: open(f,"w",encoding="utf-8").write(s)
json.dump(dims, open(CACHE,"w"))
print("Bildmasse ergaenzt:", n)

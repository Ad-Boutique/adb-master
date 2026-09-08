# Traegt in alle <video>-Tags das passende Posterbild ein (<pfad>-poster.jpg), damit kein
# Video als Loch erscheint, solange es nicht laeuft. Analog zu _imgdim.py als Nachlauf.
# Poster erzeugen: ./_tools/poster <video> <video ohne .mp4>-poster.jpg 0.8
# -*- coding: utf-8 -*-
import glob, os, re

changed_files = 0
changed_tags = 0
missing = set()

for f in sorted(glob.glob("*.html")):
    s = open(f, encoding="utf-8").read()
    orig = s

    def fix(m):
        global changed_tags
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
        changed_tags += 1
        return tag

    s = re.sub(r"<video\b[^>]*>", fix, s)
    if s != orig:
        open(f, "w", encoding="utf-8").write(s)
        changed_files += 1

print("Video-Poster ergaenzt: %d Tags in %d Dateien" % (changed_tags, changed_files))
if missing:
    print("  ohne Posterbild:", ", ".join(sorted(missing)))

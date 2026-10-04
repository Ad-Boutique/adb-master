# -*- coding: utf-8 -*-
"""Pruefschritt am Ende des Builds (Technik B7): jede Referenz auf assets/ in HTML, CSS und JS muss als Datei
existieren und darf nicht von .distignore ausgeschlossen sein. Fehler stehen als "  !"-Zeilen in der Ausgabe
(_build.sh sammelt sie am Ende). Dazu eine Zaehlung der Dateien unter assets/, die nirgends referenziert sind
(nur Info, die Liste mit python3 _check.py --liste). Schreibt nichts."""
import fnmatch
import glob
import os
import re
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SKIP = ("_qa_template.html",)
REF = re.compile(r"""(?:https://www\.ad\.boutique)?/?(assets/[^"'\s)?#<>]+)""")
CSS_URL = re.compile(r"""url\(\s*["']?([^"')]+)["']?\s*\)""")


def refs():
    out = {}
    for f in sorted(glob.glob("*.html")):
        if f in SKIP:
            continue
        h = open(f, encoding="utf-8").read()
        for m in REF.finditer(h):
            out.setdefault(m.group(1), set()).add(f)
        # Kundenlogos, die master.js aus data-set baut
        for m in re.finditer(r'class="lslot"[^>]*data-set="([^"]*)"', h):
            for n in filter(None, m.group(1).split(",")):
                out.setdefault("assets/logos/%s.png" % n, set()).add(f)
    for css in ("assets/site.css",):
        for m in CSS_URL.finditer(open(css, encoding="utf-8").read()):
            u = m.group(1)
            if u.startswith(("data:", "http", "#")):
                continue
            p = os.path.normpath(os.path.join(os.path.dirname(css), u.split("?")[0].split("#")[0]))
            out.setdefault(p, set()).add(css)
    for js in ("assets/site.js",):
        for m in re.finditer(r"""["'](assets/[^"'+]+\.[a-z0-9]+)["']""", open(js, encoding="utf-8").read()):
            out.setdefault(m.group(1), set()).add(js)
    return out


def ignore_rules():
    """Regeln aus .distignore (was nicht ausgeliefert wird; _dist.py nutzt dieselben)."""
    rules = []
    if os.path.exists(".distignore"):
        for ln in open(".distignore", encoding="utf-8"):
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                rules.append((ln.startswith("!"), ln.lstrip("!")))
    return rules


load_rules = ignore_rules


def _match(path, pat):
    pat = pat.rstrip("/")
    if "/" not in pat:
        # ohne Schraegstrich: trifft den Namen auf jeder Ebene und alles darunter
        return any(fnmatch.fnmatch(part, pat) for part in path.split("/"))
    rx = "^" + re.escape(pat.lstrip("/")).replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*").replace(r"\*", "[^/]*").replace(r"\?", "[^/]") + "(?:/.*)?$"
    return re.match(rx, path) is not None


def ignored(path, rules):
    hit = False
    for neg, pat in rules:
        if _match(path, pat):
            hit = not neg
    return hit


def main():
    r = refs()
    rules = ignore_rules()
    missing = sorted(p for p in r if not os.path.isfile(p))
    hidden = sorted(p for p in r if os.path.isfile(p) and ignored(p, rules))
    for p in missing:
        print("  ! Referenz ohne Datei: %s (in %s)" % (p, ", ".join(sorted(r[p])[:3])))
    for p in hidden:
        print("  ! Referenz von .distignore ausgeschlossen: %s (in %s)" % (p, ", ".join(sorted(r[p])[:3])))
    files = [p for p in glob.glob("assets/**/*", recursive=True) if os.path.isfile(p)]
    unref = sorted(p for p in files if p not in r and not p.endswith((".css", ".js", ".json")))
    shipped = [p for p in unref if not ignored(p, rules)]
    mb = sum(os.path.getsize(p) for p in shipped) / 1e6
    print("Pruefung: %d Referenzen, %d fehlen, %d ausgeschlossen. Unreferenziert unter assets/: %d Dateien, davon %d ausgeliefert (%.1f MB)"
          % (len(r), len(missing), len(hidden), len(unref), len(shipped), mb))
    if "--liste" in sys.argv:
        for p in shipped:
            print("    unreferenziert, ausgeliefert:", p)
    # Fehlende oder nicht ausgelieferte Referenzen brechen den Build und den GitHub-Check ab
    return 1 if (missing or hidden) else 0


if __name__ == "__main__":
    sys.exit(main())

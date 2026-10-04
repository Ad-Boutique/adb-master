# -*- coding: utf-8 -*-
"""Kopiert die auszuliefernden Dateien aus dem Build-Ordner in den Ausgabeordner (Standard: public/).
Was nicht ausgeliefert wird, steht in .distignore (gleiche Muster wie .gitignore: Ordnernamen,
*-Muster, ** fuer Unterordner, ! fuer Ausnahmen). Vercel liefert nur diesen Ordner aus
(vercel.json: outputDirectory), die GitHub-Pages-Vorschau ebenso (.github/workflows/pages.yml).
Aufruf (macht _build.sh): python3 _dist.py <ziel>"""
import os
import shutil
import sys

from _check import load_rules, ignored


def main():
    if len(sys.argv) < 2:
        print("Aufruf: python3 _dist.py <ziel>")
        return 2
    out = os.path.abspath(sys.argv[1])
    here = os.path.abspath(".")
    if out == here or here.startswith(out + os.sep):
        print("  ! Ziel darf nicht der Build-Ordner selbst sein: %s" % out)
        return 1
    rules = load_rules()
    if os.path.isdir(out):
        shutil.rmtree(out)
    n = size = 0
    for root, dirs, files in os.walk("."):
        rel_root = os.path.relpath(root, ".")
        rel_root = "" if rel_root == "." else rel_root.replace(os.sep, "/") + "/"
        # Ordner, die komplett ausgeschlossen sind, gar nicht erst betreten
        dirs[:] = sorted(d for d in dirs if d != ".git" and not ignored(rel_root + d, rules))
        for fn in sorted(files):
            rel = rel_root + fn
            if ignored(rel, rules):
                continue
            dst = os.path.join(out, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(rel, dst)
            n += 1
            size += os.path.getsize(rel)
    print("Ausgabe: %d Dateien, %.1f MB nach %s" % (n, size / 1e6, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())

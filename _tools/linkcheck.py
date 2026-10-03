# -*- coding: utf-8 -*-
"""Link- und HTML-Pruefung fuer alle ausgelieferten Seiten (GitHub-Check "links", laeuft auch lokal).
1. Jeder interne Link und jede eingebundene Datei (href, src, poster, srcset, data-src) muss existieren.
2. Strukturelemente (html, head, body, main, section, div, nav, header, footer, a, ul, ol, figure) muessen
   sauber geschlossen sein.
Externe Links (http, mailto, tel) werden nicht abgerufen. Aufruf: python3 _tools/linkcheck.py
Rueckgabe 1 bei Fehlern."""
import glob
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHECK = {"html", "head", "body", "main", "section", "div", "nav", "header", "footer", "a", "ul", "ol", "figure"}
ATTRS = ("href", "src", "poster", "data-src")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.stack, self.errors = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in ATTRS:
            if a.get(k):
                self.refs.append((self.getpos()[0], a[k]))
        for part in (a.get("srcset") or "").split(","):
            if part.strip():
                self.refs.append((self.getpos()[0], part.strip().split()[0]))
        if tag in CHECK:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag not in CHECK:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # Ende ohne passenden Anfang oder falsche Verschachtelung
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for t, line in self.stack[i + 1:]:
                    self.errors.append("Zeile %d: <%s> nicht geschlossen vor </%s>" % (line, t, tag))
                del self.stack[i:]
                return
        self.errors.append("Zeile %d: </%s> ohne Anfang" % (self.getpos()[0], tag))


def local_target(page, ref):
    if ref.startswith(("http:", "https:", "mailto:", "tel:", "javascript:", "data:", "#", "//", "{")):
        return None
    path = unquote(urlparse(ref).path)
    if not path:
        return None
    base = ROOT if path.startswith("/") else os.path.dirname(page)
    return os.path.normpath(os.path.join(base, path.lstrip("/")))


def main():
    pages = sorted(p for p in glob.glob(os.path.join(ROOT, "*.html")) if not os.path.basename(p).startswith("_"))
    broken, struct = [], []
    for p in pages:
        parser = Page()
        parser.feed(open(p, encoding="utf-8").read())
        name = os.path.basename(p)
        for line, ref in parser.refs:
            t = local_target(p, ref)
            if t and not os.path.exists(t):
                broken.append("%s Zeile %d: %s" % (name, line, ref))
        for t, line in parser.stack:
            if t not in ("html", "head", "body"):
                parser.errors.append("Zeile %d: <%s> bis Dateiende nicht geschlossen" % (line, t))
        struct += ["%s %s" % (name, e) for e in parser.errors]
    for b in broken:
        print("FEHLT  " + b)
    for s in struct:
        print("HTML   " + s)
    print("Linkpruefung: %d Seiten, %d fehlende Ziele, %d Strukturfehler" % (len(pages), len(broken), len(struct)))
    return 1 if broken or struct else 0


if __name__ == "__main__":
    sys.exit(main())

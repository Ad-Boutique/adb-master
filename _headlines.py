# -*- coding: utf-8 -*-
"""Headline-Regel Brand 2026 (Kundenentscheidung 28.9.2026): Jede Headline hat einen Teil in Satoshi und einen Teil
in der Serife (Amandine, kursiv). Dieser Schritt laeuft nach den Generatoren und Buildern, vor _webp.py und _seo.py,
ueber alle Seiten und setzt in jeder Headline ohne <i>-Anteil den Serifen-Teil:
  - Headline mit Zeilen (.rl): die letzte Zeile wird kursiv gesetzt
  - eine Zeile mit mehreren Saetzen: der letzte Satz
  - ein Satz mit Beistrich: der Teil nach dem letzten Beistrich (zwei bis 60 Prozent der Woerter)
  - ein Satz ohne Beistrich: die letzten Woerter (bis 5 Woerter: 2, bei 6: 3, bei 7: 4, sonst rund 40 Prozent), unter drei Woertern nichts
Betroffen: h1, h2, h3 sowie Elemente mit den Klassen lh, dispn, disp, phh, zah, pwh, kh. Nicht: .sr-only,
Headlines, die schon <i> oder <em> enthalten, und Headlines mit anderem Markup als Zeilen-Spans und <br>.
Mehrfach ausfuehrbar: eigene Einsetzungen tragen class="hs" und werden vor jedem Lauf entfernt."""
import glob
import re

SKIP = ("_qa_template.html", "studie-performance.html", "case-web-funkhausliving.html")
CLASSES = ("lh", "dispn", "disp", "phh", "zah", "pwh", "kh")


def split_text(body):
    """Teilt reinen Text (mit <br> erlaubt) in Satoshi-Teil und Serifen-Teil. None, wenn zu kurz."""
    parts = [p for p in re.split(r"(?<=[.!?:])\s+|\s*<br\s*/?>\s*", body) if p.strip()]
    if len(parts) >= 2:
        tail = parts[-1]
        head = body[: body.rfind(tail)].rstrip()
        sep = "" if head.endswith(">") else " "
        return head + sep + '<i class="hs">' + tail + "</i>"
    words = body.split(" ")
    n = len(words)
    if n < 3:
        return None
    # Beistrich: der Teil nach dem letzten Beistrich, wenn er zwei bis 60 Prozent der Woerter hat
    if "," in body:
        head, tail = body.rsplit(",", 1)
        tw = tail.strip().split(" ")
        if 2 <= len(tw) <= max(2, int(n * 0.6)):
            return head + ', <i class="hs">' + tail.strip() + "</i>"
    k = {3: 2, 4: 2, 5: 2, 6: 3, 7: 4}.get(n, max(3, int(round(n * 0.4))))
    if k >= n:
        k = n - 1
    return " ".join(words[:-k]) + ' <i class="hs">' + " ".join(words[-k:]) + "</i>"


def serifize(inner):
    if "<i" in inner or "<em" in inner or "sr-only" in inner:
        return None
    rls = list(re.finditer(r'(<span class="rl"><span>)(.*?)(</span></span>)', inner, re.S))
    if rls:
        last = rls[-1]
        txt = last.group(2)
        if "<" in txt or not re.search(r"\w", txt):
            return None
        # mehrere Zeilen: die letzte Zeile ganz; eine Zeile: innerhalb der Zeile teilen
        out = ('<i class="hs">' + txt + "</i>") if len(rls) > 1 else split_text(txt)
        if out is None:
            return None
        return inner[:last.start(2)] + out + inner[last.end(2):]
    if re.search(r"<(?!br\b)[a-z]", inner):
        return None
    lead = re.match(r"^\s*", inner).group(0)
    trail = re.search(r"\s*$", inner).group(0)
    out = split_text(inner.strip())
    return None if out is None else lead + out + trail


def process(h):
    n = 0

    def repl(tag, attrs, inner, whole):
        nonlocal n
        cls = re.search(r'class="([^"]*)"', attrs)
        cls = cls.group(1).split() if cls else []
        if "sr-only" in cls:
            return whole
        if tag == "div" and not any(c in CLASSES for c in cls):
            return whole
        out = serifize(inner)
        if out is None:
            return whole
        n += 1
        return "<%s%s>%s</%s>" % (tag, attrs, out, tag)

    # h1 bis h3 immer; div nur mit Headline-Klasse und ohne verschachteltes div
    h = re.sub(r"<(h1|h2|h3)(\b[^>]*)>(.*?)</\1>", lambda m: repl(m.group(1), m.group(2), m.group(3), m.group(0)), h, flags=re.S)
    h = re.sub(r'<div(\b[^>]*class="[^"]*\b(?:lh|dispn|disp|phh|zah|pwh|kh)\b[^"]*"[^>]*)>((?:(?!<div)[\s\S])*?)</div>',
               lambda m: repl("div", m.group(1), m.group(2), m.group(0)), h)
    return h, n


def main():
    total = 0
    for f in sorted(glob.glob("*.html")):
        if f in SKIP:
            continue
        h = open(f, encoding="utf-8").read()
        h = re.sub(r'<i class="hs">(.*?)</i>', r"\1", h, flags=re.S)
        h2, n = process(h)
        if n:
            open(f, "w", encoding="utf-8").write(h2)
            total += n
    print("Headlines mit Serifen-Anteil ergaenzt: %d" % total)


if __name__ == "__main__":
    main()

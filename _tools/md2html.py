# Kleiner Markdown-zu-HTML-Konverter fuer interne Dokumente (Ueberschriften, Absaetze,
# Listen, Tabellen, Fett, Links). Aufruf: md2html.py <ausgabe.html> <titel> <md1> [md2 ...]
import sys, re, html

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"(?<![\"'>])(https?://[^\s<)]+)", r'<a href="\1" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    return t

def convert(md):
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)", ln)
        if m:
            lvl = len(m.group(1)); out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl)); i += 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            rows = [r for r in rows if not all(re.match(r"^:?-{2,}:?$", c) for c in r)]
            if rows:
                out.append('<div class="tw"><table><thead><tr>' + "".join("<th>%s</th>" % inline(c) for c in rows[0]) + "</tr></thead><tbody>")
                for r in rows[1:]:
                    out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
                out.append("</tbody></table></div>")
            continue
        if re.match(r"^\s*[-*]\s+", ln):
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                out.append("<li>%s</li>" % inline(re.sub(r"^\s*[-*]\s+", "", lines[i]))); i += 1
            out.append("</ul>"); continue
        if re.match(r"^\s*\d+\.\s+", ln):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                out.append("<li>%s</li>" % inline(re.sub(r"^\s*\d+\.\s+", "", lines[i]))); i += 1
            out.append("</ol>"); continue
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("|", "#")) and not re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
    return "\n".join(out)

CSS = """
<style>
:root{--bg:#F3EDE1;--ink:#0E0E10;--grey:#5E5A52;--line:rgba(14,14,16,.14);--champ:#B89A63;--card:#FBF8F2}
body{background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,"Satoshi",system-ui,sans-serif;margin:0}
.wrap{max-width:1180px;margin:0 auto;padding:48px 28px 96px}
nav.toc{position:sticky;top:0;background:rgba(243,237,225,.96);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:12px 28px;display:flex;gap:18px;flex-wrap:wrap;font-size:12px;letter-spacing:.08em;text-transform:uppercase;z-index:5}
nav.toc a{color:var(--grey);text-decoration:none}nav.toc a:hover{color:var(--ink)}
h1{font-size:clamp(34px,5vw,60px);letter-spacing:-.03em;line-height:1.02;margin:0 0 18px}
h2{font-size:clamp(24px,2.6vw,34px);letter-spacing:-.02em;margin:64px 0 14px;padding-top:24px;border-top:1px solid var(--line)}
h3{font-size:18px;margin:34px 0 8px}
p{max-width:78ch;color:#2A2925}
b{color:var(--ink)}
a{color:var(--ink);text-decoration:underline;text-decoration-color:var(--champ)}
.tw{overflow-x:auto;margin:14px 0 22px;background:var(--card);border:1px solid var(--line);border-radius:4px}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:10px 12px;border-bottom:1px solid var(--line);vertical-align:top;text-align:left}
th{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grey);background:#EFE7D6;position:sticky;top:0}
td{min-width:120px}
ul,ol{max-width:80ch;color:#2A2925}li{margin:4px 0}
code{font-size:12.5px;background:#EFE7D6;padding:1px 5px;border-radius:3px}
.meta{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--grey);margin-bottom:26px}
section.doc{margin-top:40px}
@media (max-width:640px){.wrap{padding:28px 16px 72px}td{min-width:90px}}
</style>
"""

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def main():
    out, title, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    parts, toc = [], []
    for f in files:
        md = open(f, encoding="utf-8").read()
        first = next((l for l in md.split("\n") if l.startswith("# ")), "# " + f)[2:].strip()
        sid = slug(first)
        toc.append('<a href="#%s">%s</a>' % (sid, html.escape(first.replace("Recherche ", ""))))
        body = convert(md).replace("<h1>", '<h1 id="%s">' % sid, 1)
        parts.append('<section class="doc">%s</section>' % body)
    page = ("<title>%s</title>\n" % html.escape(title) + CSS +
            '<nav class="toc">' + "".join(toc) + "</nav>\n"
            '<div class="wrap"><div class="meta">Intern, vertraulich. Stand 7. September 2026</div>' + "\n".join(parts) + "</div>")
    open(out, "w", encoding="utf-8").write(page)
    print("html", out, len(page))

if __name__ == "__main__":
    main()

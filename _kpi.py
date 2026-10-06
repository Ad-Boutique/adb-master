# -*- coding: utf-8 -*-
"""KPI-Board "Auf einen Blick": ein Baustein fuer Cases, Web-Cases, handgebaute Seiten und Leistungen.

Drei Kartentypen, eine Grammatik (Label, grosse Zahl in Amandine, Badge in der Ecke, Punkt-Grafik, Satz):
  jump   Zahlen-Sprung: vorher durchgestrichen, nachher zaehlt hoch, Delta im Badge (.kpill, Figma 99:137)
  count  Produktion oder Volumen: eine Zahl zaehlt von null, jeder Punkt eine Einheit
  text   Qualitatives Ergebnis: kurzer Satz in Amandine, optional Stationen als Punktzeile
  quote  Kundenstimme als Ergebnis
  media  Die Arbeit selbst: drei Ausschnitte aus dem Projekt

Grafiken je Karte: line (Werte), rows (Punktreihen: Label, n, an, hervorgehoben), waffle (total, wert, spalten),
stations (Punktzeile), imgs (Streifen). Nur Zahlen, die auf der Seite oder im Reporting stehen.
Alle Punkt-Grafiken fuellen sich beim Ankommen (brand.js: .kpi, .dotgraph, .dotbars, .dotline).

Die Karten der Cases stehen in _content/cases/<slug>.json (Feld kennzahlen). Dort heissen die Arten sprung, zaehler,
text, medien und zitat und die Felder deutsch (label, vorher, wert, badge, reihen, waffel, ...); _cases.py uebersetzt
sie in die Kurzform, die card() hier rendert. Felder: docs/CMS-CASES.md, Abschnitt 5."""
import os

HTML_ARROW = '<span class="karrow" aria-hidden="true">&rarr;</span>'


def _q(s):
    return s.replace('"', "&quot;")


def card(c):
    kind = c.get("kind", "jump")
    # Kopfzeile: Label links, Pille rechts, beides im Fluss, damit lange Labels nicht unter die Pille laufen
    pill = ('<span class="kpill">%s</span>' % c["pill"]) if c.get("pill") else ""
    out = ['        <div class="kpi kpi--%s" data-fade>' % kind,
           '          <div class="khead"><span class="kl">%s</span>%s</div>' % (c["l"], pill)]
    if kind == "quote":
        out.append('          <p class="kquote">&bdquo;%s&ldquo;</p>' % c["q"])
        out.append('          <span class="kqa">%s</span>' % c["a"])
    else:
        vals = []
        if c.get("frm"):
            vals.append('<span class="kfrom">%s</span>%s' % (c["frm"], HTML_ARROW))
        attrs = ""
        cnt = c.get("cnt")
        if cnt:
            frm_v, to_v, dec = cnt[0], cnt[1], cnt[2]
            pre = cnt[3] if len(cnt) > 3 else ""
            suf = cnt[4] if len(cnt) > 4 else ""
            attrs = ' data-from="%s" data-to="%s" data-decimals="%d" data-prefix="%s" data-suffix="%s"' % (frm_v, to_v, dec, _q(pre), _q(suf))
        cls = "kto kto--txt" if kind in ("text", "media") else "kto"
        vals.append('<span class="%s"%s>%s</span>' % (cls, attrs, c["to"]))
        if c.get("unit"):
            vals.append('<span class="kunit">%s</span>' % c["unit"])
        out.append('          <div class="kvals">%s</div>' % "".join(vals))
    if c.get("line"):
        out.append('          <svg class="kline" viewBox="0 0 260 90" data-points="%s" aria-hidden="true"></svg>'
                   % ",".join(str(v) for v in c["line"]))
    if c.get("rows"):
        out.append('          <div class="kdots" aria-hidden="true">')
        for label, n, on, hi in c["rows"]:
            out.append('            <div class="row%s"><span class="rl">%s</span><span class="dots" data-n="%d" data-on="%d"></span></div>'
                       % (" hi" if hi else "", label, n, on))
        out.append('          </div>')
    if c.get("waffle"):
        total, value, cols = c["waffle"]
        out.append('          <div class="dotgraph kwaffle" data-total="%d" data-value="%d" style="--cols:%d" aria-hidden="true"></div>' % (total, value, cols))
    if c.get("stations"):
        out.append('          <div class="dotline kst" aria-hidden="true">%s</div>' % "".join("<span>%s</span>" % s for s in c["stations"]))
    if c.get("imgs"):
        imgs = [i for i in c["imgs"] if os.path.exists(i)][:3]
        if imgs:
            out.append('          <div class="kstrip">%s</div>' % "".join('<img loading="lazy" decoding="async" src="%s" alt="%s">' % (i, c["l"]) for i in imgs))
    if c.get("cap"):
        out.append('          <p class="kcap">%s</p>' % c["cap"])
    if c.get("link"):
        out.append('          <a class="zalink klink" href="%s">%s</a>' % c["link"])
    out.append('        </div>')
    return "\n".join(out)


def board(b, bg="paper", sec_id=None, style=None):
    """Sektion mit Label, Headline (zweite Zeile kursiv) und drei Karten."""
    label = b.get("label", "Auf einen Blick")
    h0, h1 = b.get("h", ("Was besser wurde,", "in drei Zahlen."))
    # Eine Cream-Flaeche fuer alle (BRAND-RULES Abschnitt 1): kein zweiter Cream-Ton mehr
    bgc = "#F4F3EB"
    note = ('      <p class="cfoot-note knote" data-fade>%s</p>\n' % b["note"]) if b.get("note") else ""
    st = style if style is not None else "padding-top:clamp(60px,7vw,110px);padding-bottom:clamp(50px,6vw,90px)"
    idattr = (' id="%s"' % sec_id) if sec_id else ""
    return ('  <!-- AUF EINEN BLICK: drei Karten, vorher, nachher, der Sprung im Badge -->\n'
            '  <section%s class="sec fg-light bg-%s kpisec" data-bg="%s" data-fg="dark" style="%s">\n'
            '    <div class="wrap">\n'
            '      <div class="kpihead">\n'
            '        <span class="label" style="display:block;margin-bottom:16px">%s</span>\n'
            '        <h2 class="dispn" data-lines style="font-size:clamp(30px,3.6vw,58px)"><span class="rl"><span>%s</span></span><span class="rl"><span><i>%s</i></span></span></h2>\n'
            '      </div>\n'
            '      <div class="kpiboard" data-stagger>\n%s\n      </div>\n'
            '%s'
            '    </div>\n'
            '  </section>\n\n') % (idattr, bg, bgc, st, label, h0, h1, "\n".join(card(c) for c in b["cards"]), note)


def mini(nums, note=None):
    """Kleine Zahlenkarten fuer Kapitel: dieselbe Grammatik wie das Board, ohne Grafik."""
    cards = "\n".join('        <div class="kpi kpi--mini" data-fade><span class="kl">%s</span><div class="kvals"><span class="kto">%s</span></div></div>'
                      % (l.strip("()"), v) for l, v in nums)
    out = '      <div class="kpiboard kpiboard--mini" data-stagger>\n%s\n      </div>\n' % cards
    if note:
        out += '      <p class="cfoot-note knote" data-fade>%s</p>\n' % note
    return out


def dotrows(rows, per=25):
    """Balken in Punktreihen: (Name, Prozent, Wert) -> 25 Punkte. Der Bestwert ist der eine hervorgehobene Wert (Lime auf Cream, BRAND-RULES Abschnitt 7)."""
    hi = max(range(len(rows)), key=lambda i: rows[i][1])
    out = ['        <div class="dotbars dotbars--ch" data-fade>']
    for i, (name, pct, val) in enumerate(rows):
        on = max(1, int(round(pct / 100.0 * per)))
        out.append('          <div class="row%s"><span class="rl">%s</span><span class="dots" data-n="%d" data-on="%d"></span><span class="rv">%s</span></div>'
                   % (" hi" if i == hi else "", name, per, on, val))
    out.append('        </div>')
    return "\n".join(out)


# ---------------------------------------------------------------- Daten
# Die Karten der Cases stehen in den Inhaltsdateien _content/cases/<slug>.json (Feld "kennzahlen"), siehe _cases.py
# und docs/CMS-CASES.md. Karten, die mehrfach gebraucht werden (Leistungsseiten, Web-Case Twist'n Sparkle),
# tragen dort eine id. Die Leistungsseiten holen sie in ihren Inhaltsdateien _content/services/<slug>.json
# (Feld kennzahlen, Karten als {"ref": "<id>", "link": ...}), siehe docs/CMS-LEISTUNGEN.md.
from _cases import HAND as _HAND, board as _case_board

# Handgebaute Seiten (_brand_inplace.py, _build_funkhaus_v3.py): Board aus der jeweiligen Inhaltsdatei
HAND_KPI = {c["slug"]: _case_board(c) for c in _HAND if c.get("kennzahlen")}

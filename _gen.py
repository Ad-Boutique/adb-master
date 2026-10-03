# Seiten-Generator der Case-Dossiers (Vorlage "dossier", Funkhaus bleibt handgebaut) und gemeinsamer Seitenrahmen
# (Kopf, Menue, Footer, Logos) fuer _gen_web.py, _gen_services.py und _gen_kontakt.py.
# Alle Zahlen aus uploads/AdBoutique_Referenzen_9Cases_Erweiterungsbriefing.md (bindend, anonymisiert)
# -*- coding: utf-8 -*-


HEAD = '''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} - ad.boutique Master</title>
<link rel="icon" type="image/svg+xml" href="favicon.svg">


<link rel="preconnect" href="https://use.typekit.net" crossorigin>
<link rel="preconnect" href="https://p.typekit.net" crossorigin>
<link rel="preload" href="assets/fonts/Satoshi-Variable.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v=41326722">
<link rel="stylesheet" href="https://use.typekit.net/udf8wjj.css">
<script src="assets/site.js?v=41326722" defer></script>
</head>
<body style="background-color:{bodybg}" class="on-light brand">

<div class="pt"><div class="ptw">ad<i>.</i>boutique</div></div>

<header class="chrome">
  <a href="index.html" class="logo">ad<i>.</i>boutique</a>
  <a href="kontakt.html" class="ctc">Kontakt</a>
</header>

'''

# Vorschaubilder im Menue: kleine Fassungen (300 px) aus assets/img/menu/, erst beim Oeffnen geladen (data-src, _perf.py, master.js)
from _perf import menu_tag as _mimg

MENU_ITEMS = [
    ("index.html", "Start", '''<span class="mv">
        <span class="half-d">''' + _mimg("funkhaus") + '''</span>
        <span class="half-p"></span>
        <span class="bars" style="left:56%;top:26%;width:34%"><i style="width:92%"></i><i style="width:76%"></i><i style="width:84%"></i><i style="width:30%;height:8px;margin-top:5px"></i></span>
      </span>'''),
    ("work.html", "Work", '''<span class="mv">
        <span class="grid4">
          <span>''' + _mimg("isi") + '''</span>
          <span>''' + _mimg("a_funk2") + '''</span>
          <span style="background:#1C2530"></span>
          <span>''' + _mimg("a_otta1") + '''</span>
        </span>
      </span>'''),
    ("index.html#leistungen", "Leistungen", '''<span class="mv" style="background:#F3EDE1">
        <span class="bars" style="left:8%;top:22%;width:40%"><i style="width:95%;height:9px"></i><i style="width:70%;height:9px"></i><i style="width:50%;margin-top:6px"></i><i style="width:26%;height:10px;margin-top:8px"></i></span>
        ''' + _mimg("isi", ' style="position:absolute;right:6%;top:18%;width:36%;height:64%;border-radius:2px"') + '''
      </span>'''),
    ("agentur.html", "Agentur", '''<span class="mv">
        <span class="grid4" style="grid-template-columns:1fr 1fr">
          <span>''' + _mimg("retreat-08") + '''</span>
          <span>''' + _mimg("retreat-01") + '''</span>
        </span>
      </span>'''),
    ("kontakt.html", "Kontakt", '''<span class="mv" style="background:#EFE7D6">
        <span class="bars" style="left:8%;top:24%;width:84%"><i style="width:70%;height:9px"></i><i style="width:100%;height:1px;opacity:.3;margin:7px 0"></i><i style="width:52%;height:9px"></i><i style="width:100%;height:1px;opacity:.3;margin:7px 0"></i><i style="width:44%;height:9px"></i></span>
      </span>'''),
]

BACKCIRCLE = """<a class="bkbtn" href="work.html" aria-label="Zurück zur Übersicht"><span class="bkar">&#8592;</span></a>
<svg class="bkorbit" viewBox="0 0 100 100" aria-hidden="true">
  <defs><path id="bkpath" d="M50,50 m-38,0 a38,38 0 1,1 76,0 a38,38 0 1,1 -76,0"/></defs>
  <text><textPath href="#bkpath" startOffset="2%">Übersicht</textPath></text>
</svg>
"""


def menu(active, back=False):
    rows = []
    for href, label, mv in MENU_ITEMS:
        act = " act" if href == active else ""
        rows.append('    <a class="mitem%s" href="%s">\n      <span class="mt">%s</span>\n      <span class="mthumb">%s</span>\n    </a>' % (act, href, label, mv))
    return (BACKCIRCLE if back else "") + '''<button class="mbtn" aria-label="Menü öffnen"></button>
<svg class="morbit" viewBox="0 0 124 124" aria-hidden="true">
  <defs><path id="mpath" d="M62,62 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs>
  <text class="t-open"><textPath href="#mpath" startOffset="2%">Menü</textPath></text>
  <text class="t-close"><textPath href="#mpath" startOffset="2%">Schließen</textPath></text>
</svg>
<div class="mdim"></div>
<nav class="msheet" aria-label="Hauptmenü">
  <div class="mrow">
''' + "\n".join(rows) + '''
  </div>
  <div class="mfoot">
    <span class="fl">ad.boutique Master-Preview</span>
    <span class="soc">
      <a href="https://www.instagram.com/ad.boutique.vienna/" target="_blank" rel="noopener">Instagram</a>
      <a href="https://www.linkedin.com/company/ad-boutique/" target="_blank" rel="noopener">LinkedIn</a>
    </span>
  </div>
</nav>

'''

# der eine Footer kommt aus _footer.py (Figma 84:69), damit Generator und Nachlauf dasselbe Markup setzen
from _footer import FOOTER as _FOOTER
FOOTER = _FOOTER + '''
</main>
</body>
</html>
'''

LOGO = lambda names: "\n      ".join(
    '<img loading="lazy" decoding="async" src="assets/logos/%s.png" alt="%s">' % (n, n) for n in names)


BRANCH_LOGOS = {
    "Finance": ["ifa", "conda", "raiffeisen"],
    "Real Estate": ["winegg", "funkhaus", "seeresidenz", "soravia", "rhomberg", "vonpoll"],
    "D2C / Retail": ["looops", "isi", "nordicspirit", "ilbosso", "kaisers", "jti"],
    "Consumer": ["isi", "looops", "nordicspirit", "jti", "ilbosso", "kaisers"],
    "E-Commerce": ["looops", "isi", "nordicspirit", "ilbosso", "kaisers", "jti"],
    "Energie": ["hagent", "robin", "fabrik1230"],
}
LOGO_TILE_BGS = [
    ("#FBF8F2", "lt"), ("#0E0E10", "dk"), ("#EFE7D6", "lt"), ("#22382C", "dk"),
    ("#E9D8BC", "lt"), ("#1C2530", "dk"), ("#FFFFFF", "lt"), ("#4A3328", "dk"),
]
def logogrid(names):
    names = list(names)
    slots = 8
    per = max(1, (len(names) + slots - 1) // slots)
    while len(names) < slots * per:
        names += names[: slots * per - len(names)]
    out = []
    for i in range(slots):
        bg, tone = LOGO_TILE_BGS[i]
        chunk = names[i * per:(i + 1) * per]
        out.append('<span class="lslot" data-set="%s"></span>' % ",".join(chunk))
    return "\n        ".join(out)

def logocycle(names, slots=3):
    names = list(names)
    per = max(1, (len(names) + slots - 1) // slots)
    out = []
    for i in range(0, len(names), per):
        out.append('<span class="lslot" data-set="%s"></span>' % ",".join(names[i:i+per]))
    return "\n        ".join(out)

# ============================================================
# CASES: Inhalte in _content/cases/<slug>.json (Vorlage "dossier"), Bausteine in _bausteine.py,
# Laden und Pruefen in _cases.py. Anleitung fuer neue Cases: _intern/CMS-CASES.md.
# Die Reihenfolge der Kette "performance" (Feld reihenfolge) ist die Staerke laut Briefing.
# ============================================================
from _cases import PERFORMANCE
from _bausteine import koerper


def case_page(c):
    world = c["meta"].get("farbwelt", "#22382C")
    return (HEAD.format(title="Case, " + c["meta"]["name"], bodybg=world) + menu("work.html", back=True)
            + "<main>\n\n" + koerper(c) + FOOTER)


if __name__ == "__main__":
    for c in PERFORMANCE:
        if c["vorlage"] != "dossier":
            continue
        open(c["slug"] + ".html", "w", encoding="utf-8").write(case_page(c))
        print("case", c["slug"])
    print("cases done")

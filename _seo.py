# -*- coding: utf-8 -*-
"""SEO-Schicht fuer den Master (Phase 0 des Masterplans, siehe _intern/SEO-MASTERPLAN.md).

Laeuft als vorletzter Schritt (vor _bump.py) ueber alle HTML-Seiten und setzt je Seite:
Title, Meta Description, Robots, Canonical, Open Graph, Twitter Card, JSON-LD (Organization,
WebSite, WebPage mit Breadcrumb, je nach Seitentyp Service oder Article), lang de-AT, die H1-Regel
(Suchbegriff als erste Zeile der H1 auf Startseite und Leistungsseiten, Hero-Zeile der Cases als H1),
den Stand im Footer und, im Live-Modus, GTM und Meta-Pixel. Dazu sitemap.xml, robots.txt, llms.txt.

Live-Schalter: Umgebungsvariable ADB_LIVE=1. Ohne Schalter bleibt alles noindex und robots sperrt,
damit die GitHub-Pages-Vorschau nicht als Dublette der Live-Seite indexiert wird. Im Live-Modus werden
ausserdem die internen Links auf die sauberen Pfade (vercel.json) umgeschrieben.

Mehrfach ausfuehrbar: der eingesetzte Block steht zwischen <!-- seo:start --> und <!-- seo:end -->."""
import datetime
import glob
import html as H
import json
import os
import re

from _gen import CASES
from _gen_web import WEBCASES
from _gen_services import SERVICES

LIVE = os.environ.get("ADB_LIVE") == "1"
BASE = "https://www.ad.boutique"
TODAY = datetime.date.today()
MONTHS = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
STAND = "%d. %s %d" % (TODAY.day, MONTHS[TODAY.month - 1], TODAY.year)
GTM = "GTM-KNJKF4D5"
PIXEL = "371950892334202"

# Referenzformulierung (Kapitel 3 des Masterplans): ueberall identisch verwenden
ORG_DESC = ("ad.boutique ist eine Performance-Marketing-Agentur in Wien. Die Agentur plant und steuert Kampagnen auf Meta, Google, "
            "TikTok, Pinterest und in ChatGPT, produziert die Creatives dafür (UGC, Foto, Film, Social Content) und baut die Landingpages "
            "und Websites, auf die sie führen. Schwerpunkte sind Immobilien und Wohnbau, Finance und Investment, Consumer und D2C sowie Health. "
            "Die Vergütung ist an messbare Ergebnisse gekoppelt.")
ORG = dict(name="ad.boutique", legal="Ad Boutique Agency GmbH", email="hello@ad.boutique", plz="1030", city="Wien", country="AT",
           same_as=["https://www.linkedin.com/company/ad-boutique/", "https://www.instagram.com/ad.boutique.vienna/"],
           logo=BASE + "/assets/img/og-default.jpg")
DEFAULT_OG = "assets/img/funkhaus.jpg"

NOINDEX = {"_qa_template.html", "studie-performance.html", "case-web-funkhausliving.html"}


def path_for(f):
    """Dateiname im Master -> sauberer Pfad auf der Live-Domain (Rewrites in vercel.json)."""
    special = {"index.html": "/", "work.html": "/referenzen", "agentur.html": "/agentur", "kontakt.html": "/kontakt",
               "service-strategie.html": "/services/digitale-strategie", "service-ecommerce.html": "/services/e-commerce"}
    if f in special:
        return special[f]
    if f.startswith("service-"):
        return "/services/" + f[len("service-"):-5]
    if f.startswith("case-"):
        return "/referenzen/" + f[len("case-"):-5]
    return "/" + f[:-5]


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def clip(s, n=155):
    s = strip_tags(s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "."


def first_sentence(s):
    s = strip_tags(s)
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return m.group(1) if m else s


# ---------------------------------------------------------------- Seitenregister: Title, Description, Typ
HAND = {
    "index.html": dict(title="Digitale Marketing Agentur Wien | ad.boutique",
                       desc="Performance-Marketing-Agentur in Wien: Meta, Google, TikTok, Pinterest und ChatGPT Ads, Creatives und Landingpages aus einer Hand. 26 Cases mit echten Zahlen.",
                       kind="home", h1label="Digitale Marketing Agentur Wien"),
    "work.html": dict(title="Referenzen: 26 Cases mit echten Zahlen | ad.boutique",
                      desc="26 Cases aus Immobilien, Finance, E-Commerce und Health, belegt mit Zahlen aus dem Reporting: Anfragen, Preis je Anfrage, ROAS, Umsatz.",
                      kind="collection"),
    "agentur.html": dict(title="Agentur: Team, Zahlen, Arbeitsweise | ad.boutique",
                         desc="Wer bei ad.boutique in Wien an Kampagnen, Creatives und Websites arbeitet, wie wir vergütet werden und warum Zahlen bei uns im Report stehen.",
                         kind="about"),
    "kontakt.html": dict(title="Anfrage: Performance Marketing Agentur Wien | ad.boutique",
                         desc="Anfrage in zwei Minuten, ehrliche Ersteinschätzung unter 24 Stunden, ein Gründer prüft. Der Einstieg ist ein Audit ohne Vertrag.",
                         kind="contact"),
    "case-premium-neubau.html": dict(title="Case: Premium-Neubau Wien, 489 Anfragen zu 11,77 Euro | ad.boutique",
                                     desc="489 Kaufinteressenten aus 5.755 Euro Spend, 11,77 Euro je Anfrage, Instant Form 6,97 statt 15,66 Euro über die Website. Ein Motiv trug 54 Prozent.",
                                     kind="case"),
    "case-premium-neubau-v3.html": dict(title="Vorschau v3: Premium-Neubau Wien | ad.boutique", desc="Vorschau-Variante, nicht indexiert.", kind="case"),
    "case-kommunalkredit.html": dict(title="Case: Kommunalkredit Sommergespräche, Film und Kampagne | ad.boutique",
                                     desc="Sommergespräche in Bad Aussee: Recap-Film, Dokumentation und 19 Social Clips aus drei Drehtagen, dazu Kampagnen auf LinkedIn und Google.",
                                     kind="case"),
    "service-performance-marketing-v3.html": dict(title="Vorschau v3: Performance Marketing | ad.boutique", desc="Vorschau-Variante, nicht indexiert.", kind="service"),
    "studie-performance.html": dict(title="Studie: Performance-Grafiken | ad.boutique", desc="Interne Studie, nicht indexiert.", kind="other"),
    "case-web-funkhausliving.html": dict(title="Weiterleitung | ad.boutique", desc="Weiterleitung.", kind="other"),
    "_qa_template.html": dict(title="QA | ad.boutique", desc="Intern.", kind="other"),
}


def registry():
    reg = dict(HAND)
    for c in CASES:
        f = c["slug"] + ".html"
        if c.get("handmade") or f in reg:
            continue
        big = (c.get("big") or "").strip()
        title = ("Case: %s, %s %s | ad.boutique" % (c["nav_title"], big, c.get("biglabel", ""))) if big else ("Case: %s | ad.boutique" % c["nav_title"])
        reg[f] = dict(title=title.replace("  ", " "), desc=clip(c["sub"] + " " + first_sentence(c["body"])), kind="case", name=c["nav_title"])
    for c in WEBCASES:
        f = c["slug"] + ".html"
        reg[f] = dict(title="%s: %s | ad.boutique" % (c["name"], c["line"]), desc=clip(c["story"]), kind="case", name=c["name"])
    for s in SERVICES:
        f = s["slug"] + ".html"
        seo = s.get("seo", {})
        reg[f] = dict(title=seo.get("title", s["nav"] + " Agentur Wien | ad.boutique"), desc=seo.get("desc", clip(s["sub"])),
                      kind="service", name=s["nav"], h1label=seo.get("label"), answer=seo.get("answer"))
    return reg


# ---------------------------------------------------------------- JSON-LD
def org_graph():
    return [
        {"@type": ["Organization", "ProfessionalService"], "@id": BASE + "/#org", "name": ORG["name"], "legalName": ORG["legal"],
         "url": BASE + "/", "logo": ORG["logo"], "image": ORG["logo"], "description": ORG_DESC, "email": ORG["email"],
         "address": {"@type": "PostalAddress", "postalCode": ORG["plz"], "addressLocality": ORG["city"], "addressCountry": ORG["country"]},
         "areaServed": ["Wien", "Österreich", "Deutschland"], "sameAs": ORG["same_as"],
         "knowsAbout": ["Performance Marketing", "Meta Ads", "Google Ads", "TikTok Ads", "Pinterest Ads", "ChatGPT Ads", "UGC", "Content Creation", "Landingpages", "Webflow", "Immobilienmarketing", "E-Commerce Growth"]},
        {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": ORG["name"], "inLanguage": "de-AT", "publisher": {"@id": BASE + "/#org"}},
    ]


def page_graph(f, r, url, og_image):
    kind = r["kind"]
    crumbs = [{"@type": "ListItem", "position": 1, "name": "Start", "item": BASE + "/"}]
    if kind == "service":
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Leistungen", "item": BASE + "/#leistungen"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": r.get("name", ""), "item": url})
    elif kind == "case":
        crumbs.append({"@type": "ListItem", "position": 2, "name": "Referenzen", "item": BASE + "/referenzen"})
        crumbs.append({"@type": "ListItem", "position": 3, "name": r.get("name", r["title"].split("|")[0].strip()), "item": url})
    elif kind != "home":
        crumbs.append({"@type": "ListItem", "position": 2, "name": r["title"].split(":")[0].split("|")[0].strip(), "item": url})
    page_type = {"home": "WebPage", "service": "WebPage", "case": "WebPage", "about": "AboutPage", "contact": "ContactPage", "collection": "CollectionPage"}.get(kind, "WebPage")
    g = [{"@type": page_type, "@id": url + "#page", "url": url, "name": r["title"].split(" | ")[0], "description": r["desc"], "inLanguage": "de-AT",
          "isPartOf": {"@id": BASE + "/#site"}, "about": {"@id": BASE + "/#org"}, "dateModified": TODAY.isoformat(),
          "primaryImageOfPage": {"@type": "ImageObject", "url": og_image},
          "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": crumbs}}]
    if kind == "service":
        g.append({"@type": "Service", "@id": url + "#service", "name": r.get("name", ""), "serviceType": r.get("h1label") or r.get("name", ""),
                  "provider": {"@id": BASE + "/#org"}, "areaServed": ["Wien", "Österreich"], "url": url,
                  "description": strip_tags(r.get("answer") or r["desc"])})
    elif kind == "case":
        g.append({"@type": "Article", "@id": url + "#article", "headline": r["title"].split(" | ")[0], "description": r["desc"], "url": url,
                  "image": og_image, "dateModified": TODAY.isoformat(), "inLanguage": "de-AT",
                  "author": {"@id": BASE + "/#org"}, "publisher": {"@id": BASE + "/#org"}, "mainEntityOfPage": {"@id": url + "#page"}})
    return g


# ---------------------------------------------------------------- Seite bearbeiten
def og_image_for(h):
    m = re.search(r'<img[^>]+src="(assets/[^"]+\.(?:jpg|webp|png))"', h) or re.search(r'poster="(assets/[^"]+\.(?:jpg|webp))"', h)
    p = m.group(1) if m else DEFAULT_OG
    jpg = re.sub(r"\.webp$", ".jpg", p)
    if os.path.exists(jpg):
        p = jpg
    return BASE + "/" + p


def apply(f, r, live):
    h = open(f, encoding="utf-8").read()
    orig = h
    h = re.sub(r"<!-- seo:start -->.*?<!-- seo:end -->\n?", "", h, flags=re.S)
    h = re.sub(r'\s*<meta name="robots" content="[^"]*">', "", h)
    h = re.sub(r'<html([^>]*)lang="[^"]*"', r'<html\1lang="de-AT"', h, count=1)
    indexable = live and f not in NOINDEX and not f.endswith("-v3.html")
    url = BASE + path_for(f)
    og = og_image_for(h)
    title = r["title"]
    r = dict(r, desc=clip(r["desc"], 158))
    h = re.sub(r"<title>.*?</title>", "<title>" + H.escape(title, quote=False) + "</title>", h, count=1, flags=re.S)
    graph = org_graph() + page_graph(f, r, url, og)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    block = ['<!-- seo:start -->',
             '<meta name="description" content="%s">' % H.escape(r["desc"], quote=True),
             '<meta name="robots" content="%s">' % ("index, follow, max-image-preview:large" if indexable else "noindex, nofollow"),
             '<link rel="canonical" href="%s">' % url,
             '<meta property="og:type" content="%s">' % ("article" if r["kind"] == "case" else "website"),
             '<meta property="og:site_name" content="ad.boutique">',
             '<meta property="og:locale" content="de_AT">',
             '<meta property="og:title" content="%s">' % H.escape(title.split(" | ")[0], quote=True),
             '<meta property="og:description" content="%s">' % H.escape(r["desc"], quote=True),
             '<meta property="og:url" content="%s">' % url,
             '<meta property="og:image" content="%s">' % og,
             '<meta name="twitter:card" content="summary_large_image">',
             '<script type="application/ld+json">%s</script>' % ld.replace("</", "<\\/")]
    if live:
        block.append("<!-- Google Tag Manager -->\n<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','%s');</script>\n<!-- End Google Tag Manager -->" % GTM)
        block.append("<!-- Meta Pixel -->\n<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','%s');fbq('track','PageView');</script>\n<!-- End Meta Pixel -->" % PIXEL)
    block.append('<!-- seo:end -->')
    anchor = re.search(r'<meta name="viewport"[^>]*>', h)
    if not anchor:
        return False
    h = h[:anchor.end()] + "\n" + "\n".join(block) + h[anchor.end():]
    if live and "<!-- GTM noscript -->" not in h:
        h = re.sub(r"(<body[^>]*>)", r'\1\n<!-- GTM noscript --><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' % GTM, h, count=1)

    # H1-Regel
    if r.get("h1label") and 'class="label h1-seo"' not in h:
        lab = H.escape(r["h1label"], quote=False)
        if f == "index.html":
            h = h.replace('<span class="label">Digitale Marketing Agentur, Wien</span>\n      <h1 class="disp" data-lines>',
                          '<h1 class="disp" data-lines>\n        <span class="label h1-seo">%s</span>' % lab, 1)
        else:
            h = re.sub(r'<span class="label slabel" data-fade>[^<]*</span>\n(\s*)<h1 data-lines>',
                       lambda m: '<h1 data-lines>\n%s  <span class="label slabel h1-seo" data-fade>%s</span>' % (m.group(1), lab), h, count=1)
    if "<h1" not in h:
        h = re.sub(r'<div class="dispn" style="--n:(\d+)">(.*?)</div>', r'<h1 class="dispn" style="--n:\1">\2</h1>', h, count=1)
    # Antwortabsatz unter dem Hero-Text der Leistungsseiten
    if r.get("answer") and 'class="sanswer"' not in h:
        h = re.sub(r'(<p class="ssub"[^>]*>.*?</p>\n)', lambda m: m.group(1) + '      <p class="sanswer" data-fade>%s</p>\n' % r["answer"], h, count=1, flags=re.S)
    # Menue-Vorschaubilder: kurzer Alt-Text statt leerem
    def _menu_alt(m):
        return re.sub(r'alt=""', 'alt="Menüvorschau"', m.group(0))
    h = re.sub(r'<nav class="msheet".*?</nav>', _menu_alt, h, count=1, flags=re.S)
    # restliche Bilder ohne Alt-Text: Projektname als Fallback
    pname = r.get("name") or r["title"].split(":")[0].split("|")[0].strip()
    h = re.sub(r'(<img\b[^>]*?)alt=""', lambda m: m.group(1) + 'alt="%s, Bild aus dem Projekt"' % H.escape(pname, quote=True), h)
    # Footer: Stand und Firmierung
    h = re.sub(r"© 2026 ad\.boutique[^<]*", "© 2026 %s, %s. Stand: %s" % (ORG["legal"], ORG["city"], STAND), h)
    if live:
        h = h.replace('<span class="fl">ad.boutique Master-Preview</span>', '<span class="fl">ad.boutique</span>')
        # interne Links auf die sauberen Pfade
        h = re.sub(r'href="([a-z0-9_-]+\.html)(#[^"]*)?"', lambda m: 'href="%s%s"' % (path_for(m.group(1)), m.group(2) or ""), h)
    if h != orig:
        open(f, "w", encoding="utf-8").write(h)
        return True
    return False


# ---------------------------------------------------------------- Dateien: sitemap, robots, llms.txt
def write_files(reg, live):
    pages = [f for f in sorted(glob.glob("*.html")) if f in reg and f not in NOINDEX and not f.endswith("-v3.html")]
    urls = "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (BASE + path_for(f), TODAY.isoformat()) for f in pages)
    open("sitemap.xml", "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    if live:
        bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User", "ClaudeBot", "Google-Extended", "CCBot"]
        rob = "# ad.boutique: Suche und KI-Systeme sind ausdruecklich willkommen\n" + "".join("User-agent: %s\nAllow: /\n\n" % b for b in bots)
        rob += "User-agent: *\nAllow: /\nDisallow: /_qa_template.html\nDisallow: /studie-performance.html\n\nSitemap: %s/sitemap.xml\n" % BASE
    else:
        rob = "# Master-Vorschau: nicht indexieren. Live-Fassung entsteht mit ADB_LIVE=1 (siehe _seo.py)\nUser-agent: *\nDisallow: /\n"
    open("robots.txt", "w", encoding="utf-8").write(rob)
    lines = ["# ad.boutique", "", "> " + ORG_DESC, "", "Standort: %s %s, Österreich. Kontakt: %s. Sprache der Seite: Deutsch (Sie-Form)." % (ORG["plz"], ORG["city"], ORG["email"]), "", "## Leistungen", ""]
    for s in SERVICES:
        lines.append("- [%s](%s%s): %s" % (s["nav"], BASE, path_for(s["slug"] + ".html"), strip_tags(s["sub"])))
    lines += ["", "## Referenzen (Zahlen aus dem Reporting, Kunden teils anonymisiert)", ""]
    for c in CASES:
        f = c["slug"] + ".html"
        if f in reg:
            lines.append("- [%s](%s%s): %s" % (c["nav_title"], BASE, path_for(f), strip_tags(reg[f]["desc"])))
    for c in WEBCASES:
        f = c["slug"] + ".html"
        lines.append("- [%s](%s%s): %s" % (c["name"], BASE, path_for(f), strip_tags(c["line"])))
    lines += ["", "## Weitere Seiten", "", "- [Agentur](%s/agentur)" % BASE, "- [Referenzen](%s/referenzen)" % BASE, "- [Anfrage](%s/kontakt)" % BASE, ""]
    open("llms.txt", "w", encoding="utf-8").write("\n".join(lines))
    return len(pages)


def main():
    reg = registry()
    n = 0
    for f in sorted(glob.glob("*.html")):
        if f not in reg:
            print("  ? keine SEO-Daten fuer", f)
            continue
        if apply(f, reg[f], LIVE):
            n += 1
    pages = write_files(reg, LIVE)
    print("SEO: %d Seiten bearbeitet, %d im Sitemap, Modus %s" % (n, pages, "LIVE" if LIVE else "Vorschau (noindex)"))


if __name__ == "__main__":
    main()

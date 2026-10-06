# adb-master: Website von ad.boutique

Statische Website der Digitalagentur ad.boutique (Wien). Das HTML wird von Python-Generatoren erzeugt; `sh _build.sh` baut die Seite nach `public/` (nicht in Git). Ausgeliefert wird über Vercel (Livegang vorbereitet) und als Vorschau über GitHub Pages, beides heute mit `noindex`.

Betreut von Daniel (`danielphadb`) und Florian (`florian-hoermann`) mit gleichen Rechten. **Arbeitsregeln für Menschen und Claude: [CLAUDE.md](CLAUDE.md).** Wer gerade woran arbeitet: [docs/STATUS.md](docs/STATUS.md). Plan bis zum Go-live: [docs/PLAN.md](docs/PLAN.md).

> Das Repo ist **öffentlich**. Interne Unterlagen (Log, SEO-Strategie, Recherchen, Audits) liegen im privaten Repo `Ad-Boutique/adb-intern`.

## Struktur

| Pfad | Was |
|---|---|
| `*.html` | nur die handgebauten Seiten (Startseite, Work, Agentur, Premium-Neubau, Kommunalkredit, Studie, Weiterleitung). Alle anderen Seiten entstehen beim Build in `public/` |
| `_content/cases/*.json` | Inhalt je Case (Texte, Zahlen, Bilder). Anleitung: [docs/CMS-CASES.md](docs/CMS-CASES.md) |
| `_content/services/*.json` | Inhalt je Leistungsseite (Texte, Zahlen, Bilder, SEO, Wörterbuch-Hero). Anleitung: [docs/CMS-LEISTUNGEN.md](docs/CMS-LEISTUNGEN.md) |
| `_*.py` | Build-Schritte (Prüfung, Generatoren, Vorlagen, Regeln des Nachlaufs), siehe unten |
| `assets/tokens.css` | alle Gestaltungswerte (Farben, Schrift, Abstände, Radien, Bewegung) |
| `assets/master.css`, `brand*.css` | Stylesheets je Bereich; `_css.py` bündelt sie zu `assets/site.css` (nie direkt bearbeiten) |
| `assets/brand.js`, `master.js` | Verhalten; gebündelt zu `assets/site.js` |
| `api/anfrage.js` | Vercel Function für das Kontaktformular (Versand über Resend) |
| `vercel.json`, `.distignore`, `.vercelignore` | Build, Routing, 301-Weiterleitungen, Header; `.distignore`: was nicht nach `public/` kommt; `.vercelignore`: was Vercel nicht hochlädt |
| `requirements.txt` | Python-Pakete des Builds (Pillow, feste Version) |
| `_tools/` | Prüfwerkzeuge: `linkcheck.py`, `qa2.js`, `stylefp.js`, `fp.sh`; Swift-Programme (nur Mac) für Screenshots und Posterbilder |
| `docs/` | Doku: Status, Plan, Versionen, Brand-Regeln, Design-System, Cases, GitHub-Einstellungen, Cloud-Anleitung |
| `.github/workflows/` | Prüfungen bei jedem PR (Build, Links, Secret-Scan), IndexNow nach Go-live |

## Bauen

Voraussetzung: Python 3 mit Pillow (`pip install -r requirements.txt`).

```bash
sh _build.sh
```

Der Build arbeitet in einer temporären Kopie des Repos und schreibt nur die auszuliefernden Dateien nach `public/` (nicht eingecheckt; was nicht ausgeliefert wird, steht in `.distignore`). **Das Repo selbst ändert sich beim Bauen nicht.** Erzeugte Seiten (22 Cases, 6 Leistungen, Kontakt, Impressum, Datenschutz, CSS/JS-Bündel, Sitemap) liegen deshalb nicht mehr in Git; Quellen sind `_content/` und die Generatoren. Handgebaute Seiten (Startseite, Work, Agentur, Premium-Neubau, Kommunalkredit) sind Quelle und bleiben eingecheckt.

Anderes Ziel, z. B. für eine lokale Vorschau:

```bash
sh _build.sh /tmp/adb-vorschau
```

Die Reihenfolge ist verbindlich und steht in `_build.sh`:

| # | Schritt | Aufgabe |
|---|---|---|
| 1 | `_cases.py` | prüft die Case-Dateien in `_content/cases` |
| 2 | `_leistungen.py` | prüft die Leistungsdateien in `_content/services` |
| 3 | `_css.py` | bündelt CSS und JS (vor den Generatoren, weil die Cache-Version ein Hash von `site.css` und `site.js` ist) |
| 4 | `_gen.py` | Performance-Cases aus `_content/cases` |
| 5 | `_gen_web.py` | Web-Cases |
| 6 | `_gen_services.py` | sechs Leistungsseiten aus `_content/services`, Markup in `_tpl_services.py`; dazu die Vorschau-Variante `service-performance-marketing-v3.html` |
| 7 | `_gen_kontakt.py` | Kontaktseite mit Anfrage-Funnel |
| 7a | `_gen_legal.py` | Impressum und Datenschutz |
| 8 | `_nachlauf.py` | dieselben Regeln für die handgebauten Seiten, Vorschau-Variante `case-premium-neubau-v3.html`, `sitemap.xml`, `robots.txt`, `llms.txt` |
| 9 | `_check.py` | jede `assets/`-Referenz existiert und wird ausgeliefert |
| 10 | `_dist.py` | kopiert die auszuliefernden Dateien nach `public/` |

Die Generatoren schreiben fertige Seiten: Sie geben ihr HTML an `_nachlauf.fertig()`, die Regeln laufen beim Erzeugen, kein späterer Schritt fasst die Seite noch an. Die handgebauten Seiten (Startseite, Work, Agentur, Studie, Premium-Neubau, Kommunalkredit, Weiterleitungen) durchlaufen dieselben Regeln in `_nachlauf.py`. Jede Regel steht genau einmal, als Funktion `seite(name, html)` in ihrem Modul; die Reihenfolge steht nur in `_nachlauf.py` (`SCHRITTE`):

| Regel | Modul | Aufgabe |
|---|---|---|
| `inhalt` | `_apply_content.py` | Vorschau-Medien der Work-Kacheln, Galerie der handgebauten Cases |
| `imgdim` | `_imgdim.py` | Breite und Höhe an jedes Bild (Cache `assets/imgdim.json`) |
| `poster` | `_poster.py` | Posterbilder an Videos |
| `brand` | `_brand_inplace.py` | Kopf, Brand-Bausteine der handgebauten Seiten, Abstände auf Tokens; danach entstehen die `*-v3.html` |
| `footer` | `_footer.py` | ein Footer für alle Seiten |
| `ui` | `_ui_markup.py` | Farben, Button-Varianten je Untergrund, Labels, alte Textlinks |
| `headlines` | `_headlines.py` | Satoshi- und Amandine-Teil der Headlines, große Zahlen |
| `webp` | `_webp.py` | WebP aus JPG (fehlende werden erzeugt), Pfade umschreiben |
| `perf` | `_perf.py` | Ladeleistung (Videos, Menübilder, Prioritäten, Sprunglink) |
| `seo` | `_seo.py` | Title, Description, Canonical, Open Graph, JSON-LD, H1-Regel, Footer-Stand |
| `version` | `_bump.py` | Cache-Version `?v=` als Inhalts-Hash |

Fehlt ein Anker für eine Einsetzung (Marker-Kommentar oder Struktur in einer handgebauten Seite oder einer `*-v3.html`), bricht der Build mit Regel, Seite und Anker ab (`_anker.py`). Jedes Regel-Modul lässt sich zur Fehlersuche einzeln aufrufen (`python3 _footer.py` bearbeitet alle Seiten), verbindlich ist der ganze Build.

Der Build zeigt je Schritt eine Zeile und am Ende alle Warnungen. `STRICT=1 sh _build.sh` bricht bei Warnungen ab. Zweimal hintereinander gebaut ergibt keine Unterschiede.

## Vorschau

**Lokal:** nach dem Build den Ordner mit einem einfachen Server öffnen, z. B. `python3 -m http.server 8743 --directory public`, dann `http://localhost:8743/?coach=0` (`coach=0` überspringt die Menü-Einführung).

**Cloud und PR:** Jeder Pull Request bekommt von Vercel automatisch einen Vorschau-Link. Anleitung für Claude-Cloud-Sitzungen: [docs/CLOUD-ANLEITUNG.md](docs/CLOUD-ANLEITUNG.md).

## Prüfen

```bash
python3 _tools/linkcheck.py public
```

Dazu je Seite die Darstellungsprüfung `_tools/qa2.js` (Overflow, Schriften, Overlays): auf dem Mac mit `_tools/probe <url> 1440 900 _tools/qa2.js`, in der Cloud mit `python3 _tools/pwprobe.py js <url> 1440 900 _tools/qa2.js`. In GitHub Actions laufen bei jedem PR der Build, `linkcheck.py`, `_check.py` und ein Secret-Scan; `qa2.js` läuft dort nicht.

## Deployment

- **Vercel baut die Seite selbst** (`vercel.json`: `installCommand` Pillow, `buildCommand` `sh _build.sh public`, `outputDirectory` `public`) und liefert nur `public/` aus. Funktionen in `api/` baut Vercel aus dem Projekt. Nur `main` geht live, jeder PR bekommt eine Vorschau.
- **GitHub-Pages-Vorschau** (https://ad-boutique.github.io/adb-master/) baut die Action `.github/workflows/pages.yml` bei jedem Push auf `main` (Settings, Pages, Source "GitHub Actions").
- **Live-Schalter:** `ADB_LIVE=1 sh _build.sh` gibt die Seiten für Suchmaschinen frei (index/follow, robots offen), schaltet saubere Pfade (`/referenzen/...`, `/services/...`) und lädt Google Tag Manager und Meta-Pixel erst nach Einwilligung. Beim Go-live in Vercel als Umgebungsvariable `ADB_LIVE=1` nur für Production setzen. Ohne Schalter bleibt alles `noindex`.
- Kontaktformular: in Vercel `RESEND_API_KEY` und `ANFRAGE_TO` setzen; ohne Endpunkt öffnet das Formular das Mailprogramm.

## Branches

- Niemals direkt auf `main`. Arbeit auf `daniel/...`, `florian/...`, `claude/...`, dann Pull Request; gemergt wird nur aktiv von Daniel oder Florian.
- Jede verworfene oder abgelöste Variante wird ein `archiv/JJJJ-MM-TT-name`-Branch mit Tag (nie löschen, nie mergen). Übersicht mit Screenshots: [docs/VERSIONEN.md](docs/VERSIONEN.md).
- Änderungen auf der Website: [CHANGELOG.md](CHANGELOG.md).

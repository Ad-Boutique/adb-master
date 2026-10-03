# adb-master: Website von ad.boutique

Statische Website der Digitalagentur ad.boutique (Wien). Das HTML wird von Python-Generatoren erzeugt und liegt fertig gebaut im Repo. Ausgeliefert wird über Vercel (Livegang vorbereitet) und als Vorschau über GitHub Pages, beides heute mit `noindex`.

Betreut von Daniel (`danielphadb`) und Florian (`florian-hoermann`) mit gleichen Rechten. **Arbeitsregeln für Menschen und Claude: [CLAUDE.md](CLAUDE.md).** Wer gerade woran arbeitet: [docs/STATUS.md](docs/STATUS.md). Plan bis zum Go-live: [docs/PLAN.md](docs/PLAN.md).

> Das Repo ist **öffentlich**. Interne Unterlagen (Log, SEO-Strategie, Recherchen, Audits) liegen im privaten Repo `Ad-Boutique/adb-intern`.

## Struktur

| Pfad | Was |
|---|---|
| `*.html` | gebaute Seiten: Startseite, Work, Agentur, Kontakt, 6 Leistungen, 24 Cases (2 davon handgebaut), Studie, 2 Vorschau-Varianten `*-v3.html` |
| `_content/cases/*.json` | Inhalt je Case (Texte, Zahlen, Bilder). Anleitung: [docs/CMS-CASES.md](docs/CMS-CASES.md) |
| `_*.py` | Build-Schritte (Generatoren und Nachbearbeitung), siehe unten |
| `assets/tokens.css` | alle Gestaltungswerte (Farben, Schrift, Abstände, Radien, Bewegung) |
| `assets/master.css`, `brand*.css` | Stylesheets je Bereich; `_css.py` bündelt sie zu `assets/site.css` (nie direkt bearbeiten) |
| `assets/brand.js`, `master.js` | Verhalten; gebündelt zu `assets/site.js` |
| `api/anfrage.js` | Vercel Function für das Kontaktformular (Versand über Resend) |
| `vercel.json`, `.vercelignore` | Routing, 301-Weiterleitungen, Header; was Vercel nicht ausliefert |
| `_tools/` | Prüfwerkzeuge: `linkcheck.py`, `qa2.js`, `stylefp.js`, `fp.sh`; Swift-Programme (nur Mac) für Screenshots und Posterbilder |
| `docs/` | Doku: Status, Plan, Versionen, Brand-Regeln, Design-System, Cases, GitHub-Einstellungen, Cloud-Anleitung |
| `.github/workflows/` | Prüfungen bei jedem PR (Build, Links, Secret-Scan), IndexNow nach Go-live |

## Bauen

Voraussetzung: Python 3 mit Pillow (`pip install pillow`). Auf dem Mac zusätzlich die Swift-Programme in `_tools/` (Posterbilder für neue Videos).

```bash
sh _build.sh
```

Mit Vorschau-Ordner (baut und kopiert danach dorthin):

```bash
sh _build.sh /tmp/adb-vorschau
```

Die Reihenfolge ist verbindlich und steht in `_build.sh`:

| # | Schritt | Aufgabe |
|---|---|---|
| 1 | `_cases.py` | prüft die Case-Dateien in `_content/cases` |
| 2 | `_gen.py` | Performance-Cases aus `_content` |
| 3 | `_gen_web.py` | Web-Cases |
| 4 | `_gen_services.py` | sechs Leistungsseiten (inkl. Wörterbuch-Hero) |
| 5 | `_gen_kontakt.py` | Kontaktseite mit Anfrage-Funnel |
| 6 | `_apply_content.py` | Bildmaterial in die Cases |
| 7 | `_imgdim.py` | Breite und Höhe an jedes Bild |
| 8 | `_poster.py` | Posterbilder an Videos |
| 9 | `_css.py` | bündelt CSS und JS |
| 10 | `_brand_inplace.py` | Kopf, Brand-Bausteine in handgebaute Seiten |
| 11 | `_build_funkhaus_v3.py` | Vorschau-Variante Funkhaus-Case |
| 12 | `_build_performance_v3.py` | Vorschau-Variante Performance |
| 13 | `_footer.py` | ein Footer für alle Seiten |
| 14 | `_ui_markup.py` | Button-Varianten je Untergrund, alte Textlinks |
| 15 | `_headlines.py` | Satoshi- und Amandine-Teil der Headlines |
| 16 | `_webp.py` | WebP aus JPG, Pfade umschreiben |
| 17 | `_perf.py` | Ladeleistung (Videos, Menübilder, Prioritäten) |
| 18 | `_seo.py` | Title, Description, Canonical, Open Graph, JSON-LD, Sitemap, robots, llms.txt |
| 19 | `_bump.py` | Cache-Version `?v=` als Inhalts-Hash |
| 20 | `_check.py` | jede `assets/`-Referenz existiert und wird ausgeliefert |

Der Build zeigt je Schritt eine Zeile und am Ende alle Warnungen. `STRICT=1 sh _build.sh` bricht bei Warnungen ab. Zweimal hintereinander gebaut ergibt keine Unterschiede.

## Vorschau

**Lokal:** nach dem Build den Ordner mit einem einfachen Server öffnen, z. B. `python3 -m http.server 8743 --directory /tmp/adb-vorschau`, dann `http://localhost:8743/?coach=0` (`coach=0` überspringt die Menü-Einführung).

**Cloud und PR:** Jeder Pull Request bekommt von Vercel automatisch einen Vorschau-Link. Anleitung für Claude-Cloud-Sitzungen: [docs/CLOUD-ANLEITUNG.md](docs/CLOUD-ANLEITUNG.md).

## Prüfen

```bash
python3 _tools/linkcheck.py
```

Dazu je Seite die Darstellungsprüfung `_tools/qa2.js` (Overflow, Schriften, Overlays): auf dem Mac mit `_tools/probe <url> 1440 900 _tools/qa2.js`, in der Cloud mit `python3 _tools/pwprobe.py js <url> 1440 900 _tools/qa2.js`. In GitHub Actions laufen bei jedem PR der Build, `linkcheck.py`, `_check.py` und ein Secret-Scan; `qa2.js` läuft dort nicht.

## Deployment

- Vercel baut nichts, es liefert die Dateien aus dem Repo aus. Nur `main` geht live, jeder PR bekommt eine Vorschau.
- **Live-Schalter:** `ADB_LIVE=1 python3 _seo.py` gibt die Seiten für Suchmaschinen frei (index/follow, robots offen), schaltet saubere Pfade (`/referenzen/...`, `/services/...`) und lädt Google Tag Manager und Meta-Pixel erst nach Einwilligung. Ohne Schalter bleibt alles `noindex`. Der Live-Modus schreibt Seiten dauerhaft um: nur auf dem Go-live-Branch ausführen.
- Kontaktformular: in Vercel `RESEND_API_KEY` und `ANFRAGE_TO` setzen; ohne Endpunkt öffnet das Formular das Mailprogramm.

## Branches

- Niemals direkt auf `main`. Arbeit auf `daniel/...`, `florian/...`, `claude/...`, dann Pull Request; gemergt wird nur aktiv von Daniel oder Florian.
- Jede verworfene oder abgelöste Variante wird ein `archiv/JJJJ-MM-TT-name`-Branch mit Tag (nie löschen, nie mergen). Übersicht mit Screenshots: [docs/VERSIONEN.md](docs/VERSIONEN.md).
- Änderungen auf der Website: [CHANGELOG.md](CHANGELOG.md).

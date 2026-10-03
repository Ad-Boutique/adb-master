# Projektplan Website ad.boutique

Stand 03.10.2026. **Entwurf zum Abstimmen zwischen Daniel und Florian.** Nichts davon wird ohne OK umgesetzt.

## 1. Bewertung des aktuellen Stands

**Was gut ist**
- Klares, verbindliches Design-System: Regelwerk aus Figma (`docs/BRAND-RULES.md`), alle Werte in einer Datei (`assets/tokens.css`), ein gebündeltes Stylesheet und Skript je Seite.
- Starkes SEO-Grundgerüst: Title, Description, Canonical, Open Graph, JSON-LD je Seitentyp, Sitemap, `llms.txt`, 301-Weiterleitungen für die alten Webflow-URLs vorbereitet.
- Build ist reproduzierbar (zweimal gebaut, null Unterschiede), alle Bilder als WebP mit festen Maßen (keine Layout-Sprünge).
- Cases als Inhaltsdateien (`_content/cases/*.json`) mit Prüfung, neue Cases ohne Code.
- Echte Zahlen aus Reportings, 24 Cases, sechs Leistungsseiten mit FAQ.

**Technische Schulden**
- 10 von 20 Build-Schritten schreiben fertiges HTML mit regulären Ausdrücken um, statt es aus Vorlagen zu erzeugen. Ändert jemand eine Zeile im Markup, kann ein Schritt still nicht mehr greifen.
- `_gen_services.py` hat rund 2.000 Zeilen und mischt Inhalt, Markup und Logik.
- Etwa ein Drittel der alten CSS-Regeln (`master.css`) trifft auf keiner Seite mehr etwas, viele Elemente werden zweimal gestylt.
- Zwei Vorschau-Varianten (`*-v3.html`) und eine Weiterleitungsseite liegen weiter im Repo.
- Rund 190 MB Medien direkt in Git, davon etwa 43 MB ungenutzt.

**Risiken**
- **Konflikte:** Jeder Build ändert rund 40 HTML-Dateien (Cache-Version, Menü, Datum). Arbeiten zwei Personen parallel, kollidieren diese Dateien fast immer.
- **Mac-Abhängigkeit:** Der Build läuft inzwischen überall (nur Python und Pillow). Die Prüf- und Screenshot-Werkzeuge sind noch Swift-Programme; Ersatz mit Playwright siehe `docs/CLOUD-ANLEITUNG.md`.
- **DSGVO:** Google Tag Manager und Meta-Pixel dürfen erst nach Einwilligung laden. Das Banner ist gebaut, muss aber vor dem Go-live geprüft und in der Datenschutzerklärung beschrieben werden (inkl. Adobe Fonts).
- **Öffentliches Repo:** Code, Case-Daten (auch ältere, ausgeblendete Ergebniszahlen in `_content`, z. B. beim Health-Case) und die Git-Historie sind für jeden lesbar. Der Health-Case steht außerdem schon in Sitemap und Work, obwohl seine Freigabe offen ist. Interne Unterlagen liegen deshalb im privaten Repo `adb-intern`.
- **Performance:** große Videos (bis 37 MB), keine responsiven Bildgrößen (`srcset`). Die schlimmsten Fälle sind behoben (Videos laden erst bei Bedarf), der Rest steht unten.
- **Barrierefreiheit:** Grundlagen umgesetzt (Sprunglink, Fokus, Menü), Alt-Texte sind teils sehr allgemein.
- **Wartbarkeit ohne CMS:** Texte außerhalb der Cases ändert nur, wer Python-Generatoren lesen kann.

**Was bis zum Go-live fehlt:** siehe Phase C und D.

## 2. Phasen und Aufgaben

Priorität: **A** muss vor Go-live, **B** bald danach, **C** später. Verantwortlich: Daniel, Florian oder offen.

### Phase A: Zusammenarbeit absichern (diese Woche)

| Aufgabe | Prio | Wer | Abhängig von | Status |
|---|---|---|---|---|
| Sicherung des lokalen Stands auf Branch, Archiv-Branches für alle Varianten | A | Daniel (Claude) | | erledigt, PR offen |
| Doku, Arbeitsregeln, Status-Log, Versionen | A | Daniel (Claude) | | PR offen |
| GitHub-Checks (Build, Links, Secret-Scan) | A | Daniel (Claude) | | PR offen |
| GitHub-Einstellungen nach Checkliste (`docs/GITHUB-EINSTELLUNGEN.md`) | A | Florian oder Daniel | Merge der PRs | offen |
| Claude-GitHub-App und Cloud-Umgebung | A | Daniel | Owner der Organisation | offen |
| Privates Repo `adb-intern` anlegen und befüllen | A | Daniel (Claude) | OK | vorbereitet |

### Phase B: Technik vor Go-live

| Aufgabe | Prio | Wer | Abhängig von | Status |
|---|---|---|---|---|
| Videos laden erst bei Bedarf, Menübilder klein, Ladeblende kürzer | A | | | umgesetzt, im PR |
| Cookie-Banner mit Einwilligung vor GTM und Pixel | A | | | umgesetzt, im PR, rechtliche Prüfung offen |
| Kontaktformular mit echtem Versand (Vercel Function, Resend) | A | Florian | Resend-Konto, Umgebungsvariablen `RESEND_API_KEY`, `ANFRAGE_TO` in Vercel | Code im PR |
| Sicherheits-Header, `.vercelignore`, Open-Graph-Bilder je Seite | A | | | umgesetzt, im PR |
| Adobe-Fonts-Kit auf Amandine reduzieren, "font-display: swap", Domain eintragen | A | Daniel | Adobe-Konto | offen |
| MP4 mit "faststart" neu verpacken (ändert kein Pixel) | B | offen | Entscheidung Git LFS | offen |
| Responsive Bildgrößen (`srcset`) | B | offen | Entscheidung Vercel-Build | offen |
| Tote CSS-Regeln abbauen | C | offen | | offen |

### Phase C: Inhalte und Freigaben

| Aufgabe | Prio | Wer | Status |
|---|---|---|---|
| Impressum und Datenschutz als eigene Seiten (Banner und Footer verlinken auf `www.ad.boutique/datenschutz` und `/impressum`, die nach der Domain-Umstellung 404 wären): **Blocker vor dem Live-Schalter** | A | Daniel | offen |
| Organisationsdaten im Schema: Adresse, Telefon, Gründungsjahr, Gründer | A | Daniel | offen |
| Freigaben Logowand (Soravia, Raiffeisen, Nordic Spirit) und Soravia-Kachel auf Work | A | Daniel | offen |
| Ad-Spend-Zahl auf der Startseite (16,7 oder 8,7 Mio. €) bestätigen | A | Daniel | offen |
| Blog-Artikel der Live-Seite (15 URLs) übernehmen oder weiterleiten | A | offen | offen |
| Portrait Fabi | B | Daniel | offen |
| Health-Case nur nach Freigabe | B | Daniel | offen |

### Phase D: Go-live

| Aufgabe | Prio | Wer | Abhängig von | Status |
|---|---|---|---|---|
| Domain `www.ad.boutique` auf Vercel umstellen | A | Florian | Phase B und C | offen |
| Live-Schalter `ADB_LIVE=1` (index/follow, robots offen, Tracking nach Einwilligung) | A | Florian | Domain | offen |
| 301-Weiterleitungen testen, Search Console und Bing Webmaster, IndexNow aktivieren | A | Florian | Live-Schalter | offen |

### Phase E: nach dem Go-live

| Aufgabe | Prio | Wer | Status |
|---|---|---|---|
| Antwortabsatz für Google und KI-Suchen auf den Leistungsseiten wieder sichtbar platzieren (mit dem Wörterbuch-Hero entfallen, steht noch im JSON-LD und in der ersten FAQ) | B | offen | offen |
| Content-Programm (zwölf Artikel, Benchmark-Report) laut SEO-Masterplan | B | offen | offen |
| Einträge in Agenturverzeichnissen | B | offen | offen |
| Generatoren entflechten (Vorlagen statt Nachbearbeitung) | C | offen | offen |
| Entscheidung CMS | C | Daniel und Florian | offen |

## 3. Offene Entscheidungen für Florian und Daniel

1. **Vercel baut die Seite, erzeugtes HTML liegt nicht mehr in Git.** Beseitigt die 40-Dateien-Konflikte und die Mac-Abhängigkeit beim Bauen. Voraussetzung: Build läuft unter Linux (Posterbilder per Python statt Swift). Empfehlung: ja, nach dem Go-live als eigenes Projekt.
2. **Archiv-Branches oder Archiv-Ordner.** Heute: Branches plus Tags (`archiv/*`), geschützt per Ruleset. Ordner würden den Stand von `main` aufblähen. Empfehlung: Branches beibehalten.
3. **Git LFS für Medien.** Spart Klon-Zeit, kostet ab 1 GB Speicher Geld und macht Vercel-Deploys etwas komplizierter. Alternative: Medien auf einem Speicher (z. B. Vercel Blob, Cloudflare R2) und nur Verweise im Repo. Empfehlung: erst entscheiden, wenn Videos neu verpackt werden.
4. **CMS mittelfristig.** Cases haben schon Inhaltsdateien; Decap CMS ist vorbereitet (im Repo `adb-intern`). Für Leistungsseiten und Startseite wäre zuerst Punkt 1 nötig. Empfehlung: Decap für Cases testen, sobald Vercel baut.
5. **Beispielseiten von Alexis und Martin** (einfache HTML-Dateien außerhalb des Repos). Vorschlag: Jede Beispielseite kommt als eigener Branch `claude/beispiel-<name>` mit der Datei unter `docs/beispiele/`; Claude überträgt sie dann in Bausteine des Design-Systems (Tokens, vorhandene Komponenten) und zeigt die Vorschau im PR.
6. **Repo öffentlich lassen** (entschieden 03.10.2026): Website-Repo bleibt öffentlich (Vercel Hobby, GitHub Pages und Rulesets kostenlos), Internes im privaten Repo `adb-intern`.

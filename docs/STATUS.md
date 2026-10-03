# Status

Wichtigste Datei für die Zusammenarbeit. Zu Beginn jeder Sitzung lesen, vor Arbeitsbeginn unter "Gerade in Arbeit" eintragen, am Ende einen Log-Eintrag oben ergänzen.

## Gerade in Arbeit

| Person | Branch | Seiten oder Dateien | Seit | Ziel |
|---|---|---|---|---|
| Daniel (Claude) | `daniel/setup-workflow` | Doku, Prüfungen, Build-Werkzeuge | 03.10.2026 | Sicherung und gemeinsamer Workflow, PRs zur Abnahme |

## Log

### 03.10.2026, Daniel (Claude), `daniel/sicherung-aktueller-stand` und `daniel/setup-workflow`

**Gemacht**
- Lokaler Stand seit dem 30.09. gesichert: Brand-Vereinheitlichung nach Figma (Regelwerk, Tokens, gebündeltes CSS/JS), Cases als Inhaltsdateien, alte Textlinks an drei Stellen, Kreis-Hover für Buttons, Wörterbuch-Hero auf allen Leistungsseiten, Portraits Leny und Philipp, Technik-Audit umgesetzt (Videos bei Bedarf, Menübilder, Ladeblende, Cookie-Banner, Formular-Endpunkt, Sicherheits-Header, SEO-Korrekturen, Barrierefreiheit, Build-Prüfungen).
- Archiv-Branches und Tags für alle Design-Stände seit dem 29.08. (`docs/VERSIONEN.md`).
- Interne Unterlagen ins private Repo `Ad-Boutique/adb-intern`.
- Doku: README, CLAUDE.md, STATUS, PLAN, VERSIONEN, CHANGELOG, GitHub-Einstellungen, Cloud-Anleitung. GitHub-Checks für Build, Links und Secret-Scan.
- Unabhängiger Review vor dem PR (separater Agent): keine kritischen Befunde. Behoben: Kundenlogos und Anfrage-Herkunft unter sauberen Live-Pfaden (`data-page` am body, Logo-Pfad relativ zu `site.js`), `_check.py` bricht bei fehlenden Referenzen ab, Cache nur für `site.css`/`site.js` unveränderlich, Formular-Endpunkt mit Herkunftsprüfung, Spam-Kennzeichnung statt stillem Verwerfen und 8 s Wartezeit, Footer-Stand nur mit Monat (Build über Tage gleich), Vorschau-Ziel des Builds nur unter /tmp, TruffleHog fest gepinnt, Doku-Pfade. Offen und in `docs/PLAN.md`: Mengenbegrenzung in Vercel, Datenschutz- und Impressum-Seiten vor dem Live-Schalter, Antwortabsatz auf den Leistungsseiten, Freigabe Health-Case. Gesehen, nicht geändert: Menü-Kreis und transparente Kopfzeile liegen beim Scrollen über Inhalt (gewolltes Gestaltungselement).
- Neuer Website-Stand vorab auf `main` vorgespult (Wunsch Daniel, 03.10.2026), alter Stand als `archiv/2026-09-30-vor-brand-vereinheitlichung` gesichert.

**Offen**
- PR `daniel/setup-workflow` prüfen und mergen (Daniel oder Florian, nach Sichtprüfung der Vercel-Vorschau).
- GitHub-Einstellungen nach `docs/GITHUB-EINSTELLUNGEN.md`.
- Inhalte und Freigaben laut `docs/PLAN.md`, Phase C.

**Nächster Schritt**
- Nach dem Merge: Rulesets setzen, dann arbeiten beide nur noch über Branches und PRs.

# CLAUDE.md: Arbeitsregeln für jede Claude-Sitzung

Gilt für jede Sitzung an diesem Repo, lokal und in der Cloud, für Daniel (`danielphadb`) und Florian (`florian-hoermann`). Beide haben gleiche Rechte.

## Zu Beginn jeder Sitzung

1. `docs/STATUS.md` und `docs/PLAN.md` lesen.
2. In `docs/STATUS.md` unter "Gerade in Arbeit" eintragen: Person, Branch, Seiten oder Dateien, seit wann, Ziel.
3. `git pull` auf `main`, dann eigenen Branch anlegen.

## Harte Regeln

1. **Niemals direkt auf `main` pushen, niemals `main` mergen.** Gearbeitet wird nur auf Branches, Änderungen kommen per Pull Request. Gemergt wird ausschließlich aktiv von Daniel oder Florian, nach Sichtprüfung der Vercel-Vorschau.
2. **Nichts löschen, nichts überschreiben, kein Force-Push, kein Rebase auf geteilten Branches.** Archiv-Branches (`archiv/*`) werden nie gelöscht und nie gemergt.
3. **Keine Geheimnisse ins Repo**: keine `.env`-Dateien, API-Keys, Tokens, Passwörter, privaten Kundendaten oder unanonymisierten Kundenzahlen. Vor jedem Commit einen Secret-Scan laufen lassen. Bei einem Fund sofort stoppen und fragen.
4. **Das Repo ist öffentlich.** Alles, was hier liegt, kann jeder lesen. Interne Unterlagen (Log, SEO-Strategie, Recherchen, Case-Inventar mit Zahlen, Audits) gehören ins private Repo `Ad-Boutique/adb-intern`, nicht hierher. Ausgeliefert wird nur `public/`, und dorthin kommt jede Datei des Repos, die nicht in `.distignore` steht: neue interne Dateien (Generatoren, Tools, Doku) dort ausschließen. `.vercelignore` regelt nur, was Vercel gar nicht erst hochlädt.
5. Vor jedem Schritt, der etwas auf GitHub verändert (Push, PR, Branch, Tag, Einstellungen), kurz zeigen, was passiert, und auf ein OK warten.
6. **Schreibstil**: In allen Texten, Dokumenten und Code-Kommentaren keine Geviertstriche oder Halbgeviertstriche, sondern Bindestrich, Komma, Doppelpunkt oder Klammer.
7. Echte Zahlen nur aus Reportings, Kunden anonymisiert, wo nicht freigegeben. Keine Preise und keine Vergütungsprozente auf der Website.

## Branches

- `daniel/...`, `florian/...`, `claude/...` für Arbeit
- `archiv/JJJJ-MM-TT-kurzname` plus gleichnamiges Tag für jede verworfene oder abgelöste Variante (siehe `docs/VERSIONEN.md`)

## Vor jedem Pull Request

1. Voller Build: `sh _build.sh` (baut nach `public/`, das Repo bleibt unverändert; siehe README).
2. `python3 _tools/linkcheck.py public` und Prüfung aller Seiten bei 1440 und 390 px (`_tools/qa2.js`, lokal mit `_tools/probe`, in der Cloud mit Playwright).
3. Unabhängiger Review durch einen separaten Review-Agenten, der den Code nicht geschrieben hat (`/code-review`, `/security-review`): Funktion, Darstellung Desktop und Handy, Sicherheit. Befunde beheben oder im PR begründen.
4. Die GitHub-Checks (Build, Links, Secret-Scan) müssen grün sein.

## Am Ende jeder Sitzung

- `docs/STATUS.md` aktualisieren (Log-Eintrag oben, "Gerade in Arbeit" bereinigen) und mitcommitten.
- Bei gemergten PRs: Zeile in `CHANGELOG.md`.
- Jede Antwort an Daniel endet mit drei Zeilen: `Fertig:`, `Du musst tun:`, `Als Nächstes:`.

## Wissen zum Projekt

- Design: `docs/BRAND-RULES.md` (verbindlich, aus Figma), `docs/DESIGN-SYSTEM.md` (wo welcher Wert steht). Werte nur in `assets/tokens.css`, nie in `assets/site.css` (wird erzeugt).
- Cases: `_content/cases/<slug>.json`, Anleitung `docs/CMS-CASES.md`.
- Alte Elemente der früheren Seite bleiben bewusst an festen Stellen (`assets/brand-keep.css`, Abschnitt 13 der Brand-Regeln).
- Prüfungen in versteckten Browser-Fenstern frieren CSS-Übergänge ein: für Farbmessungen Übergänge abschalten. URLs mit `?coach=0` laden, sonst läuft die Menü-Einführung.

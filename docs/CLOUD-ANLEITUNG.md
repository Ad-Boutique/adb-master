# Umstellung auf Claude-Cloud-Sitzungen

Für Daniel, so wie Florian schon arbeitet. Stand 03.10.2026.

## 1. Was ein Cloud-Container ist

Jede Sitzung läuft in einer frischen, abgeschotteten Umgebung in der Cloud. Zu Beginn holt sie das Repo von GitHub, am Ende ist alles weg, was nicht committet und gepusht wurde. **GitHub ist damit die einzige Wahrheit, nicht mehr der Mac.** Lokale Ordner wie `/tmp/adb-hero-variant` oder Kopien im Finder gibt es dort nicht.

## 2. Einrichten (einmal)

1. Auf https://claude.ai/code mit dem Firmen-Account anmelden.
2. GitHub verbinden: https://claude.ai/connect-github
3. Die Claude-GitHub-App muss für die Organisation Ad-Boutique installiert sein, mit Zugriff auf `adb-master` und `adb-intern`. Das macht ein Owner der Organisation (siehe `docs/GITHUB-EINSTELLUNGEN.md`, Abschnitt 5).

## 3. Umgebung anlegen

1. In claude.ai/code eine neue Umgebung anlegen und das Repo `Ad-Boutique/adb-master` auswählen.
2. Netzwerkzugriff: GitHub, Vercel (`vercel.com`, `*.vercel.app`), PyPI (`pypi.org`, `files.pythonhosted.org`) und die Playwright-Downloads (`playwright.azureedge.net`, `cdn.playwright.dev`) erlauben. Für Prüfungen der Seite zusätzlich `use.typekit.net` und `p.typekit.net`.
3. Setup-Skript eintragen:

   ```bash
   sh _tools/cloud-setup.sh
   ```

   Es installiert Pillow und Playwright (Chromium) und, falls möglich, ffmpeg.
4. Keine Geheimnisse in die Umgebung schreiben, die nicht gebraucht werden. Der Resend-Key gehört nach Vercel, nicht in die Claude-Umgebung.

### Was vom Mac in der Cloud nicht läuft, und der Ersatz

| Mac-Werkzeug | Wofür | Ersatz in der Cloud |
|---|---|---|
| `sips` (früher in `_imgdim.py`, `_bausteine.py`) | Bildmaße | ersetzt durch Pillow, läuft überall |
| `_tools/probe` (Swift) | JavaScript in der Seite auswerten, z. B. `qa2.js` | `python3 _tools/pwprobe.py js <url> 1440 900 _tools/qa2.js` |
| `_tools/scrollshot` (Swift) | Screenshots an Scrollpositionen | `python3 _tools/pwprobe.py shot <url> <prefix> 1440 900 0 900` |
| `_tools/poster` (Swift) | Posterbild aus neuem Video | `ffmpeg -ss 0.8 -i video.mp4 -frames:v 1 video-poster.jpg` |
| `_tools/aprobe`, `scrollprobe`, `dense`, `enc` | Spezialmessungen | bei Bedarf mit Playwright nachbauen |
| `_tools/fp.sh` (nutzt probe) | Stil-Fingerabdruck vor/nach | auf `pwprobe.py js` umstellen, wenn gebraucht |

Der Build selbst (`sh _build.sh`) braucht nur Python und Pillow und läuft in der Cloud wie auf dem Mac. Er läuft auch bei jedem PR in GitHub Actions auf Linux.

Vorschau in der Cloud: `sh _build.sh /tmp/vorschau`, dann `python3 -m http.server 8743 --directory /tmp/vorschau`. Für die Abnahme zählt der Vercel-Link im PR.

## 4. Arbeiten in der Cloud

1. Sitzung starten, Aufgabe beschreiben. Claude liest zuerst `CLAUDE.md`, `docs/STATUS.md` und `docs/PLAN.md`.
2. Claude arbeitet auf einem eigenen Branch (`claude/...` oder `daniel/...`), pusht und öffnet auf Wunsch einen Pull Request.
3. Die Vorschau prüfst du über den Vercel-Link im PR (Desktop und Handy).
4. Gemergt wird nur von dir oder Florian, aktiv mit "Squash and merge".
5. Funktioniert auch vom Handy und aus der Claude-Desktop-App.

## 5. Neue Gewohnheiten

- Keine Kopien und Varianten mehr in lokalen Ordnern. Jede Variante wird ein Branch; verworfene Varianten werden `archiv/...`-Branches mit Tag und eine Zeile in `docs/VERSIONEN.md`.
- Vor Arbeitsbeginn in `docs/STATUS.md` unter "Gerade in Arbeit" eintragen.
- Kleine PRs, schnell mergen. Wegen der vielen erzeugten HTML-Dateien kollidieren parallele PRs leicht: wer zuerst mergt, gewinnt; der andere holt `main` und baut neu (`sh _build.sh`), statt Konflikte in HTML-Dateien von Hand zu lösen.
- Interne Unterlagen ins private Repo `adb-intern`, nie ins öffentliche `adb-master`.

## 6. Lokal bleibt möglich

Wenn du doch auf dem Mac arbeitest, gelten dieselben Regeln: vor dem Start `git switch main && git pull`, dann eigenen Branch anlegen, nur dort arbeiten, am Ende pushen und PR öffnen. **Lokale Ordner erst aufräumen, wenn Florian bestätigt hat, dass alles auf GitHub angekommen ist.**

# GitHub-Einstellungen (von Hand, Daniel oder Florian)

Claude kann diese Einstellungen nicht selbst setzen. Reihenfolge einhalten: erst die PRs mergen, dann die Rulesets, sonst blockiert der Schutz die eigene Einrichtung.

Stand der Prüfung am 03.10.2026: Repo `Ad-Boutique/adb-master` ist **öffentlich**, Organisation im **Free**-Plan. Rulesets für öffentliche Repos sind im Free-Plan enthalten. Bleibt das Repo öffentlich (Entscheidung vom 03.10.2026), ist kein bezahlter Plan nötig.

## 1. Zugänge

- [ ] Organisation Ad-Boutique, Settings, People: Daniel (`danielphadb`) und Florian (`florian-hoermann`) sind Mitglieder.
- [ ] Repo `adb-master`, Settings, Collaborators and teams: beide mit Rolle **Admin**.
- [ ] Gleiches für das private Repo `adb-intern`.

## 2. Ruleset für `main`

Repo, Settings, Rules, Rulesets, New branch ruleset:

- [ ] Name: `main schützen`, Enforcement status: **Active**
- [ ] Target branches: **Include default branch**
- [ ] **Bypass list leer lassen** (keine Ausnahme für Admins)
- [ ] Restrict deletions
- [ ] Block force pushes
- [ ] Require a pull request before merging, Required approvals: **0** (Freigabe der anderen Person optional)
- [ ] Require status checks to pass: `build`, `links`, `secrets` (erscheinen nach dem ersten Lauf der Actions in der Auswahl), "Require branches to be up to date" an
- [ ] Require linear history (passt zu Squash and merge)

## 3. Ruleset für Archiv-Branches und -Tags

- [ ] Neues Branch-Ruleset `archiv schützen`, Target: Include by pattern `archiv/**`, Restrict deletions, Block force pushes, Restrict updates. Bypass leer.
- [ ] Neues Tag-Ruleset `archiv-tags schützen`, Target `archiv/**`, Restrict deletions, Restrict updates, Block force pushes.

## 4. Merge-Verhalten

Settings, General, Pull Requests:

- [ ] Nur **Allow squash merging** an, Merge commits und Rebase merging aus
- [ ] **Automatically delete head branches** an (betrifft `archiv/*` nicht, die sind durch das Ruleset geschützt)
- [ ] "Always suggest updating pull request branches" an

## 5. Actions und Apps

- [ ] Settings, Actions, General: Actions erlaubt, Workflow permissions "Read repository contents".
- [ ] Claude-GitHub-App für die Organisation installieren (https://github.com/apps/claude), Zugriff auf `adb-master` und `adb-intern`. Muss ein Owner der Organisation machen.
- [ ] Optional: automatischer Code-Review mit Claude auf jedem PR (in Claude Code mit `/install-github-app` einrichten).
- [ ] **Beim Merge des PR "Vercel baut selbst": Settings, Pages, Source auf "GitHub Actions" stellen** (sonst zeigt die Pages-Vorschau keine erzeugten Seiten mehr).
- [ ] Vercel-Integration prüfen: Jeder PR bekommt einen Vorschau-Link, nur `main` geht live. Die bestehende Verbindung bleibt unverändert. In den Vercel-Projekteinstellungen dürfen Build Command und Output Directory nicht überschrieben sein ("Override" aus), dann gilt `vercel.json`.

## 6. Später, beim Go-live

- [ ] IndexNow: einen Schlüssel erzeugen, die Datei `<schluessel>.txt` (Inhalt: der Schlüssel) im Repo-Root committen, damit Vercel sie ausliefert; dann Repository-Variable `ADB_LIVE=1` und Secret `INDEXNOW_KEY` setzen (aktiviert den IndexNow-Workflow).
- [ ] In Vercel: Umgebungsvariablen `RESEND_API_KEY` und `ANFRAGE_TO` für das Kontaktformular.
- [ ] In Vercel, Firewall: Mengenbegrenzung für `/api/anfrage` (z. B. 10 Anfragen je IP und Stunde), damit niemand das Postfach und das Resend-Kontingent flutet.

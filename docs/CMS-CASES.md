# Case-CMS: Cases als Inhaltsdateien

Stand 3.10.2026. Ein Case ist eine Datei `_content/cases/<slug>.json`. Die Vorlage baut daraus die Seite `<slug>.html` aus festen Bausteinen. Ein neuer Case entsteht durch Kopieren einer Datei und Befüllen. Kein Python anfassen.

## 1. Überblick

| Datei | Aufgabe |
|---|---|
| `_content/cases/<slug>.json` | Inhalt eines Cases: Meta, Hero, Intro, Kennzahlen, Bausteine, Next-Case, Bilder |
| `_content/cases/_vorlage.json` | Beispiel für einen Performance-Case (Vorlage `dossier`). Wird nicht gebaut (Name beginnt mit `_`) |
| `_content/cases/_vorlage-web.json` | Beispiel für einen Website-Case (Vorlage `web`). Wird nicht gebaut |
| `_cases.py` | Lädt und prüft alle Inhaltsdateien, Fehler nennen Datei und Feld. `python3 _cases.py` prüft ohne zu bauen |
| `_bausteine.py` | Die Bausteine (je Typ eine Funktion, die das Markup einer Sektion schreibt) und die beiden Vorlagen |
| `_gen.py` | Baut alle Cases der Vorlage `dossier`, dazu Kopf, Menü und Footer für alle Generatoren |
| `_gen_web.py` | Baut alle Cases der Vorlage `web` |
| `_kpi.py` | Zeichnet das Kennzahlen-Board. Die Leistungsseiten holen geteilte Karten per id aus den Case-Dateien |
| `_apply_content.py` | Vorschau-Medien der Work-Kacheln (`assets/content.json`) und die Galerie der handgebauten Seiten |
| `_gen_services.py`, `_leistungen.py`, `_seo.py` | lesen Name, Leistungen, Hero-Zeile und Intro der Cases (Querverweise, geteilte Karten, Title, Description, llms.txt). Leistungsseiten: [CMS-LEISTUNGEN.md](CMS-LEISTUNGEN.md) |
| `_nachlauf.py` | Regeln, die jede Seite nach dem Erzeugen durchläuft (Bildmaße, WebP, Footer, Headlines, SEO, ...). Generierte Cases bekommen sie beim Erzeugen, die handgebauten im Nachlauf |

Drei Vorlagen:

- `dossier`: Performance-Cases (13 Seiten, z. B. `case-d2c-lifestyle`). Kette `performance`.
- `web`: Website-Cases (9 Seiten, `case-web-*`). Kette `web`.
- `handgebaut`: Premium-Neubau (Funkhaus) und Kommunalkredit. Die Seite selbst bleibt handgebaut, die Datei liefert nur Daten (Abschnitt 8).

Seitenaufbau `dossier` und `web`: ein fester Rahmen und dazwischen die freie Liste `bausteine`.

```
Kopf, Menü
Hero          (Feld hero)
Intro         (Feld intro, Fakten aus meta)
Kennzahlen    (Feld kennzahlen, das Board "Auf einen Blick", optional)
Bausteine     (Liste bausteine, in genau dieser Reihenfolge)
Next-Case     (Feld naechster)
Footer
```

## 2. Neuen Case anlegen, Schritt für Schritt

1. Vorlage kopieren: `_content/cases/_vorlage.json` (Performance-Case) oder `_content/cases/_vorlage-web.json` (Website-Case) nach `_content/cases/case-<name>.json` kopieren. Der Dateiname ist der Slug plus `.json`, der Slug beginnt mit `case-` (Website-Cases mit `case-web-`), nur Kleinbuchstaben, Ziffern und Bindestriche. Er wird zur Adresse `<slug>.html` bzw. live `/referenzen/<name>`.
2. Im Kopf der Datei `slug` auf denselben Namen setzen.
3. `reihenfolge` setzen: Position in der Kette. Die bestehenden Cases stehen in Zehnerschritten (Performance 10 bis 140, Funkhaus 30, Web 210 bis 290), also passt jede Zahl dazwischen, z. B. 45 zwischen 40 und 50. Die Reihenfolge bestimmt auch die Reihenfolge in `llms.txt` und in "Auch mit dieser Leistung" auf den Leistungsseiten.
4. Next-Case verdrahten: `naechster` ist der Slug des Cases, auf den unten verlinkt wird, oder `auto` (der nächste in der Reihenfolge). Damit der neue Case selbst verlinkt wird, beim Vorgänger `naechster` auf den neuen Slug setzen. Die bestehenden Dateien nennen ihren Nachfolger ausdrücklich.
5. Bilder ablegen (Abschnitt 6) und die Pfade in die Datei schreiben.
6. Texte, Zahlen, Bausteine befüllen. Nicht gebrauchte Bausteine aus der Liste löschen, Reihenfolge nach Bedarf ändern. Nur Zahlen, die im Reporting stehen.
7. Prüfen: `python3 _cases.py`. Meldet Fehler mit Datei und Feld (z. B. `bausteine[3] (kapitel): Feld 'absatz2' fehlt`) und weist auf Bildpfade hin, deren Datei fehlt.
8. Bauen (Abschnitt 7) und in der Vorschau ansehen.
9. Außerhalb der Case-Datei, falls gewünscht: Kachel auf `work.html` und Verweise auf anderen Seiten sind weiterhin handgebaut, ebenso die Zahl "24 Cases" in den Texten.

Ein Case verschwindet, indem man die Datei löscht (und beim Vorgänger `naechster` anpasst). Die alte `case-*.html` bleibt liegen, bis man sie löscht.

## 3. Felder des Rahmens

Alle Texte dürfen einfaches HTML enthalten (`<b>`, `<em>`, `<br>`, `&amp;`). Ein Baustein mit `"ausgeblendet": true` bleibt in der Datei, erscheint aber nicht.

### Kopf (alle Vorlagen)

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `slug` | ja | gleich dem Dateinamen ohne `.json` |
| `vorlage` | ja | `dossier`, `web` oder `handgebaut` |
| `kette` | ja | `performance` (dossier, Funkhaus), `web` (web) oder `null` (in keiner Kette, Kommunalkredit) |
| `reihenfolge` | ja | Zahl, Position in der Kette |
| `naechster` | nein | Slug des Next-Case oder `auto` |

### meta, Vorlage dossier

| Feld | Bedeutung, wo es erscheint |
|---|---|
| `name` | Name des Cases: Seitentitel, Menü-Titel, Alt-Texte, Mail-Betreff, Title-Tag, Brotkrumen |
| `titel` | Liste von Zeilen, mit Leerzeichen verbunden der Titel in der Next-Kachel des Vorgängers |
| `ziel` | Fakt "Ziel" im Intro |
| `branche` | Fakt "Branche"; der Teil vor dem ersten Komma steht klein im Hero |
| `zeitraum` | Fakt "Zeitraum" |
| `kanaele` | Fakt "Kanäle" |
| `farbwelt` | Farbe von Seitenhintergrund, Statement und Learnings, Hero ohne Bild (Standard `#22382C`) |
| `farbwelt_text` | Textfarbe im Hero ohne Bild (Standard `#EDF2EC`) |
| `leistungen` | Liste `{titel, seite}`: Links im Fakt "Leistungen" und Querverweise auf den Leistungsseiten |

Die Zeile über der These im Intro ist `branche, zeitraum, kanaele`.

### meta, Vorlage web

| Feld | Bedeutung |
|---|---|
| `name` | Name des Kunden: Hero, Titel, Alt-Texte, Next-Kachel |
| `branche` | Hero, Label über dem Intro, Fakt "Branche" |
| `url` | Knopf "Live ansehen" |
| `umfang` | Liste von Zeilen im Fakt "Leistungen" (was wir gemacht haben) |
| `leistungen` | Liste `{titel, seite}`: Fakt "Leistungsseiten" und Querverweise |

### hero

| Feld | dossier | web |
|---|---|---|
| `headline` | H1 und Zeile in der Next-Kachel, Anfang der Meta Description | H1, Zeile in der Next-Kachel, Title-Tag |
| `bild` | Vollbild. Leer oder `null`: Hero in der Farbwelt ohne Bild | Screenshot der Website (Pflicht), auch Bild der Next-Kachel |
| `kennzahl` | `{wert, label}`: große Zahl im Hero mit Bild, im Title-Tag, in der Next-Kachel ohne Bild. `null` = keine | entfällt |

### intro

| Feld | dossier | web |
|---|---|---|
| `these` | großer Satz mit Scrub-Effekt, `<b>` markiert die Begriffe | entfällt |
| `text` | Absatz darunter, erster Satz geht in die Meta Description | der große Satz mit Scrub-Effekt, auch Meta Description |

### kennzahlen

Das Board "Auf einen Blick" direkt nach dem Intro. `null` oder weglassen = kein Board.

| Feld | Bedeutung |
|---|---|
| `label` | optional, Standard "Auf einen Blick" |
| `headline` | zwei Zeilen, die zweite kursiv. Üblich: "Was besser wurde, / in drei Zahlen.", "Was entstanden ist, / in drei Zahlen.", "Was das Projekt ausmacht, / in drei Punkten." |
| `karten` | drei Karten (Abschnitt 5) |
| `fussnote` | optional, Satz unter dem Board |

## 4. Baustein-Typen

Jeder Eintrag in `bausteine` hat `typ` und die Felder seines Typs. Die Prüfung kennt die Pflichtfelder.

### Vorlage dossier

| typ | Pflichtfelder | weitere Felder | Sektion |
|---|---|---|---|
| `statement` | `zeilen` (Liste) | | These in der Farbwelt, Label "So denken wir" |
| `perspektiven` | `zeilen` (Liste `{titel, text}`) | | "Fünf Perspektiven", üblich Effizienz, Zielgruppe, Message, Creative, Kanal |
| `ergebnis` | `zahlen` (Liste `{label, wert}`) | `fussnote`, `kurzfassung`, `ausgeblendet` | Zahlenreihe "Ergebnis". Erscheint nur, wenn der Case kein Kennzahlen-Board hat |
| `kapitel` | `label`, `headline` (Liste von Zeilen), `absatz1`, `absatz2` | `zahlen` (kleine Karten), `fussnote` (nur mit Zahlen), `links` (Liste `{href, text}`) | weiteres Kapitel. Der Grund wechselt selbst: erstes Kapitel creme, zweites papier, drittes creme |
| `zitat` | `text`, `wer` | | "Was der Kunde sagt". Anführungszeichen setzt die Vorlage |
| `mobil` | `headline`, `text`, `bilder` | | Handy-Screens in zwei driftenden Spalten, doppelte Bilder werden einmal gezeigt |
| `learnings` | `saetze` (Liste) | | Learnings in der Farbwelt |
| `galerie` | `medien` (Bilder und mp4) | `label` (Standard "Aus dem Mandat"), `hintergrund` (Standard `#0E0E10`) | schräge Collage in Referenzgröße, sechs Spalten. Fehlende Dateien fallen weg |

Übliche Reihenfolge: statement, perspektiven, ergebnis, kapitel, kapitel, zitat, mobil, learnings, galerie.

Zu `ergebnis`: Seit dem Kennzahlen-Board ersetzt das Board die Zahlenreihe. Bei allen bestehenden Cases steht der Baustein deshalb mit `"ausgeblendet": true` in der Datei; er bewahrt die alten Ergebniszahlen und die alten Ergebniszeilen (`kurzfassung`, wurde schon vorher nirgends ausgegeben). Die Fußnote der alten Reihe ist als `fussnote` ins Board gewandert.

### Vorlage web

| typ | Pflichtfelder | weitere Felder | Sektion |
|---|---|---|---|
| `buehne` | `bild` | | ein großer Desktop-Screenshot |
| `mobil` | `headline`, `text`, `bilder` | | wie oben, höchstens drei Screens je Spalte. Üblich: "Mobil zuerst gedacht." |
| `unterseiten` | `bilder` (bis zu drei) | `label` (Standard "Aus dem Projekt") | Unterseiten versetzt nebeneinander |
| `galerie` | `medien` | `label`, `hintergrund` | wie oben |
| `kapitel` | `label`, `headline` (eine Zeile, als Liste), `absatz1`, `absatz2` | `links` | "Zweites Kapitel" auf creme |
| `zitat` | `text`, `wer` | | wie oben |
| `stimme` | `label`, `text`, `wer`, `video`, `notiz` | | Kundenstimme als Video im Hochformat mit Ton-Knopf. Poster: gleicher Name mit `-poster.jpg` |

Übliche Reihenfolge: buehne, mobil, unterseiten, galerie, kapitel, zitat, stimme. Ohne Kapitel steht die Galerie am Schluss.

### Vorlage handgebaut

Nur `galerie`. Sie wird vor dem Next-Case der handgebauten Seite eingesetzt (`_apply_content.py`).

## 5. Kennzahlen-Karten

Grammatik: Label links oben, Badge rechts oben, große Zahl, eine Punkt-Grafik, ein Satz darunter.

| `art` | Inhalt |
|---|---|
| `sprung` | vorher (durchgestrichen) zu nachher, zählt hoch, Sprung im Badge |
| `zaehler` | eine Zahl zählt von null, jeder Punkt eine Einheit |
| `text` | kurzer Satz statt Zahl, optional Stationen als Punktzeile |
| `medien` | die Arbeit selbst: Bildstreifen mit bis zu drei Bildern |
| `zitat` | Kundenstimme als Ergebnis |

| Feld | Bedeutung |
|---|---|
| `label` | Pflicht, Überschrift der Karte |
| `badge` | Ecke rechts oben |
| `vorher` | nur `sprung`: der alte Wert |
| `wert` | die große Zahl bzw. der Satz (bei `text`, `medien`) |
| `einheit` | kleines Wort hinter der Zahl |
| `zaehlen` | `{von, bis, dezimalen, vor, nach}`: Hochzählen, z. B. `{"von": 0, "bis": 4.65, "dezimalen": 2, "vor": "€ ", "nach": " Mio."}` |
| `linie` | Liste von Werten: Punktlinie |
| `reihen` | Liste `{label, punkte, an, hervorgehoben}`: Punktreihen, genau eine Reihe hervorgehoben |
| `waffel` | `{gesamt, wert, spalten}`: Punktfeld, z. B. 100 Punkte, 54 gefüllt, 20 Spalten |
| `stationen` | Liste von Wörtern: Punktzeile |
| `bilder` | nur `medien`: Bildpfade, die ersten drei vorhandenen erscheinen |
| `zitat`, `wer` | nur `zitat` |
| `text` | Satz unter der Grafik, sagt, was ein Punkt bedeutet |
| `link` | `{href, text}`: Textlink unter der Karte |
| `id` | nur, wenn die Karte woanders wiederverwendet wird |

Eine Grafik je Karte (linie, reihen, waffel, stationen oder bilder).

Geteilte Karten: Eine Karte mit `id` kann in einem anderen Case als `{"ref": "<id>"}` stehen, optional mit `link`, und auf den Leistungsseiten im Feld `kennzahlen` ihrer Datei `_content/services/<slug>.json` ebenso als `{"ref": "<id>", "link": {...}}` (siehe [CMS-LEISTUNGEN.md](CMS-LEISTUNGEN.md)). Wer eine geteilte Karte ändert, ändert sie überall.

| id | steht in | wird außerdem gezeigt in |
|---|---|---|
| `consumer-roas` | case-consumer-brand | case-web-twistnsparkle, service-ecommerce |
| `consumer-cpm` | case-consumer-brand | case-web-twistnsparkle, service-strategie, service-chatgpt-ads |
| `crowd-roas` | case-crowdinvesting | service-performance-marketing, service-chatgpt-ads |
| `crowd-investor` | case-crowdinvesting | service-strategie |
| `d2c-umsatz` | case-d2c-lifestyle | service-ecommerce |
| `floridsdorf-strecke` | case-wohnbau-floridsdorf | service-performance-marketing |
| `funkhaus-cpl` | case-premium-neubau | service-performance-marketing |
| `funkhaus-motiv` | case-premium-neubau | service-content-creation |
| `havenstone-wochen` | case-web-havenstone | service-websites |
| `health-creator` | case-health-brand | service-content-creation |
| `invest-129` | case-immobilien-investment | service-strategie |
| `kk-clips` | case-kommunalkredit | service-content-creation |
| `noma-verkauft` | case-web-noma | service-websites |
| `nordic-orders` | case-nordic-spirit | service-ecommerce, service-chatgpt-ads |
| `pv-besucher` | case-photovoltaik | service-websites |
| `crowd-kapital`, `d2c-roas`, `d2c-budget`, `funkhaus-strecke` | ihr Case | (nur dort, id für spätere Wiederverwendung) |

## 6. Bilder: Pfade und Größen

Pfade stehen in der Datei immer ab `assets/` (z. B. `assets/case/case-neuer-case/g0.jpg`). JPG ablegen; WebP (Regel `webp`, `_webp.py`), Breite und Höhe (Regel `imgdim`, `_imgdim.py`, Cache `assets/imgdim.json`) und Video-Poster (Regel `poster`, `_poster.py`) setzt der Build beim Erzeugen der Seite. Fotos ohne Filter, kein Lime auf oder an Fotos (BRAND-RULES 1 und 8).

| Wo | Ordner, Name | Format, Größe der bestehenden Bilder |
|---|---|---|
| Hero dossier | `assets/prev/<slug>.jpg` oder `assets/case/<slug>/` | Vollbild, bestehend 1500 × 1000, 1500 × 843, 1200 × 1500, 1000 × 1500; Text steht auf der freien Seite, nie auf einem Gesicht (BRAND-RULES 3) |
| Hero web | `assets/img/web_<name>_d.jpg` | Screenshot 1600 × 1000, oben ausgerichtet |
| buehne | `assets/img/web_<name>_d1.jpg` | 1600 × 1000 |
| unterseiten | `assets/img/web_<name>_ds0.jpg` bis `_ds2.jpg`, sonst `_d2.jpg` | 1600 × 1000 |
| mobil (web) | `assets/img/web_<name>_m0.jpg` bis `_m2.jpg`, `_ms0.jpg`, `_ms1.jpg` | Handy-Screenshot 416 × 900 |
| mobil (dossier) | `assets/case/<slug>/` oder `assets/img/` | Sujets 9:16, 360 × 640 bis 843 × 1500 |
| galerie | `assets/case/<slug>/g0.jpg` ... und `v0.mp4` ... | Hochformat 843 × 1500 oder 1200 × 1500, quer 1500 × 1000; Videos mp4 16:9, ohne Ton; mindestens drei Motive, die Collage wiederholt sie bis sechs Spalten voll sind |
| Karte `medien` | wie mobil oder galerie | drei Bilder gleichen Formats |
| stimme | `assets/video/<name>.mp4` und `<name>-poster.jpg` | Hochformat 640 × 1138 |

Fehlende Dateien: Galerie und Bildstreifen der Karten lassen sie aus; Hero, Bühne, Mobil und Unterseiten zeigen dann ein leeres Bild. `python3 _cases.py` listet jeden Pfad, dessen Datei fehlt.

`assets/content.json` bleibt das Medien-Manifest für die Vorschau-Medien der Work-Kacheln (die Leistungsseiten lasen daraus früher eine Bildausrichtung, die nirgends verwendet wurde; seit dem Umbau der Leistungsseiten vom 4.10.2026 entfällt das). Die Galerien der Case-Seiten kommen seit dem Umbau aus den Case-Dateien (die Listen in `content.json` werden für die Case-Seiten nicht mehr gelesen).

## 7. Bauen und prüfen

```
cd /Users/daniel/Documents/Claudius/adb-master
python3 _cases.py                                  # nur prüfen
sh _build.sh /private/tmp/adb-master-preview       # ganze Kette, danach Vorschau auf http://localhost:8743
```

`_build.sh` prüft als ersten Schritt die Inhaltsdateien und bricht bei einem Fehler mit Datei und Feld ab. Der Build braucht nur Python und Pillow und läuft auf dem Mac, unter Linux und in der Cloud. Alle Schritte sind mehrfach ausführbar.

## 8. Handgebaute Cases: Prüfung und Entscheidung

Geprüft: `case-premium-neubau.html` (Funkhaus), `case-premium-neubau-v3.html` (Vorschau-Variante aus `_build_funkhaus_v3.py`), `case-kommunalkredit.html`.

Entscheidung: Die Seiten bleiben handgebaut. Ihre Daten stehen trotzdem in Inhaltsdateien (`case-premium-neubau.json`, `case-kommunalkredit.json`, Vorlage `handgebaut`) und steuern:

- das Kennzahlen-Board: wird seit diesem Umbau bei jedem Build aus der Datei neu gesetzt (`_brand_inplace.py`), vorher nur einmal eingesetzt und dann eingefroren. Das gilt auch für das Board der v3-Vorschau;
- die Galerie "Aus dem Mandat" (Funkhaus, Baustein `galerie`);
- den Teaser in der Next-Kachel des Vorgängers (Funkhaus, Feld `teaser`);
- Title und Description (`meta.seo`) und die Querverweise auf den Leistungsseiten (`meta.leistungen`);
- die geteilten Karten `funkhaus-*` und `kk-clips` auf den Leistungsseiten.

Warum nicht ganz in Bausteine: Die Seiten tragen zum einen Sektionen, die es nur einmal gibt, zum anderen sind sie über viele Stände direkt im HTML nachbearbeitet worden, mit Spuren, die kein Schritt der heutigen Kette mehr erzeugt.

Was für eine Überführung fehlen würde:

- Funkhaus: neue Bausteine für die Creative-Collage mit eigenem Alt-Text je Motiv, den Bild-Zoom-Übergang (`zoomsec`), das dunkle Kapitel mit Bild-Panel (`chapter`), die Bildreihe mit eigenen Abständen (`cgal` mit 60/24 px), die Website-Strecke (Kapitel mit externem Link, Desktop-Bühne, Mobil mit eigener H2 `phh`, Unterseiten "Aus dem Auftritt") sowie Varianten-Felder für Hero (kursiver Teil der H1, eigene Hero-Kennzahl, `object-position`), Statement (Hintergrundbild, dritte Zeile als Akzent) und Intro (eigener Mail-Betreff, eigener Link-Text).
- Kommunalkredit: Hero mit Vorschau-Film statt Bild und zweigeteilter H1, Film-Sektion "Recap" mit Ton auf Klick, Fotowand (`photowall`), dazu Varianten der Standard-Sektionen (Badges im Hero, Kapitel mit eingefrorenen Mini-Karten).
- v3: ist eine Vorschau-Variante mit eigenem, im Skript festgeschriebenem Hauptteil (Highlights-Stapel, Viewer, Stat-Groups, Kapitel-Leiste). Nicht im Menü, nicht indexiert.
- Für alle drei: Das heutige HTML ist der Endzustand nach Nachläufen, die es nicht mehr gibt (z. B. Alt-Texte "Case, Bild aus dem Projekt" aus einer früheren SEO-Regel, eine fest eingetragene Laufzeitklasse `inviewready`, eingefrorene Headline-Maße `--hn`). Ein Generator müsste diesen Endzustand Zeichen für Zeichen nachbauen, sonst weicht der Fingerabdruck ab.

Aufwand geschätzt: je Seite rund ein Arbeitstag inklusive Fingerabdruck-Abgleich, für rund zehn Bausteine, die jeweils nur einmal verwendet würden. Der Nutzen für das CMS (neue Cases anlegen) wäre gering, das Risiko einer sichtbaren Änderung hoch. Sinnvoll erst, wenn ein zweiter Case dieselben Sonderbausteine braucht (z. B. Film-Hero oder Fotowand); dann den Baustein in `_bausteine.py` ergänzen und die Seite in einem eigenen Schritt umstellen.

## 9. Web-Oberfläche (Decap CMS, vorbereitet, nicht aktiv)

`decap/config.yml` und `decap/index.html` im privaten Repo `adb-intern` beschreiben eine Oberfläche für die Case-Dateien: drei Sammlungen (Performance-Cases, Website-Cases, handgebaute Cases), dieselben Felder und Baustein-Typen wie oben, Bilder-Upload nach `assets/case/`, Änderungen als Pull Request (Editorial Workflow). Der Ordner liegt in `_intern/`: nicht im Git (`.gitignore`), nicht in der Vorschau (`_build.sh` schließt `_intern` aus), nicht ausgeliefert.

Was zum Aktivieren fehlt:

1. Login-Anbieter. Das GitHub-Backend braucht einen OAuth-Dienst, der den GitHub-Login für Decap abwickelt. Netlify Identity und Git Gateway gibt es nur auf Netlify; die Seite läuft auf GitHub Pages bzw. Vercel. Optionen: eine GitHub-OAuth-App plus ein kleiner OAuth-Proxy (z. B. als Vercel-Function oder Cloudflare Worker, fertige Vorlagen gibt es für Decap), oder ein gehosteter Dienst. Danach in `config.yml` `base_url` (heute Platzhalter `https://OAUTH-DIENST.example`) und gegebenenfalls `auth_endpoint` eintragen. Zugang bekommt, wer Schreibrechte auf `Ad-Boutique/adb-master` hat.
2. Ablage: `index.html` und `config.yml` nach `admin/` im Repo kopieren (ausgeliefert unter `/admin`), dort mit `noindex`.
3. Build nach dem Speichern: Decap schreibt nur die JSON-Dateien und Bilder. Die HTML-Seiten entstehen durch `_build.sh` (nur Python und Pillow, läuft auch in GitHub Actions). Entweder nach jeder Freigabe bauen und die Seiten committen, oder eine GitHub Action einrichten, die baut und committet.
4. Bild-Ordner je Case: Decap legt Uploads in `assets/case/` ab. Wer je Case einen Unterordner will, stellt `media_folder` der Sammlungen auf einen Pfad mit dem Slug um.
5. Decap schreibt die JSON-Dateien mit eigener Formatierung (alles ausgeklappt). Das ist für den Build gleichgültig.

## 10. Technische Hinweise zum Umbau (3.10.2026)

- Die Daten kamen aus `_gen.py` (CASES, EXTRA, SUBS), `_gen_web.py` (WEBCASES), `_kpi.py` (CASE_KPI, WEB_KPI, HAND_KPI und die Karten-Konstanten), `_apply_content.py` (CASE_FILES, CASE_BG und die Galerie-Listen aus `assets/content.json`), `_gen_services.py` (HAND_CASES) und `_seo.py` (Title und Description der handgebauten Cases). Alle diese Python-Daten sind entfernt, die Werte stehen unverändert in den Inhaltsdateien.
- Bildlisten der Website-Cases wurden vorher zur Laufzeit aus vorhandenen Dateinamen gesucht. Jetzt stehen sie ausdrücklich in der Datei (dieselben Dateien in derselben Reihenfolge).
- Die Galerie der generierten Cases setzt jetzt der Generator selbst als Baustein ein, nicht mehr `_apply_content.py` hinterher.
- Ergebnis-Abgleich: Alle 22 generierten Case-Seiten und alle übrigen Seiten, `sitemap.xml`, `robots.txt` und `llms.txt` sind nach dem Build Byte für Byte gleich wie vorher (bis auf die Cache-Version `?v=`, die `_bump.py` bei jedem Build hochzählt). Abweichungen gibt es nur auf `case-premium-neubau.html` und `case-kommunalkredit.html`, jeweils zwei unsichtbare Stellen, weil das Board jetzt neu gesetzt wird: der HTML-Kommentar über dem Board ("der Sprung im Badge" statt "in Lime") und ein Farbwert am Label "Auf einen Blick", das per `.brand .lbl-x { display: none }` ausgeblendet ist.
- Fingerabdruck: Die 22 generierten Cases und Premium-Neubau zeigen gegen den Stand nach dem Design-Umbau (`fp_design`) keine Abweichung. Kommunalkredit wurde zusätzlich alt gegen neu auf einem eigenen Server zweimal gemessen: Abweichungen nur in der laufenden Fotowand (`pwtrack`), die auch zwischen zwei Messungen derselben alten Seite wandert.


## Hinweis Ordnername (3.10.2026)

Der Ordner heißt `_content` mit Unterstrich. GitHub Pages veröffentlicht Ordner mit Unterstrich nicht, und `.vercelignore` schließt ihn für Vercel aus. So sind die Inhaltsdateien auf der Website nicht abrufbar. Achtung: Das GitHub-Repo selbst ist öffentlich, dort sind sie lesbar. Decap CMS muss beim Aktivieren auf `_content/cases` zeigen (steht so in `decap/config.yml` im privaten Repo `adb-intern`).

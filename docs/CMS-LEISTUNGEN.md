# Leistungs-CMS: Leistungsseiten als Inhaltsdateien

Stand 4.10.2026. Eine Leistungsseite ist eine Datei `_content/services/<slug>.json`. Der Generator baut daraus die Seite `<slug>.html` in der festen Dramaturgie der Leistungsseiten. Texte, Zahlen, Bilder, FAQ und der Suchmaschinen-Teil ändern sich in der Datei, ohne Python anzufassen. Aufbau und Prüfung folgen dem Case-CMS ([CMS-CASES.md](CMS-CASES.md)).

## 1. Überblick

| Datei | Aufgabe |
|---|---|
| `_content/services/<slug>.json` | Inhalt einer Leistungsseite: Hero, Prozess-Schema, Problem, Nutzen, Beweis, Cases, Team, Fit, Ablauf, FAQ, Angebot, dazu `seo`, `dhero` und `kennzahlen` |
| `_leistungen.py` | Lädt und prüft alle Dateien, Fehler nennen Datei und Feld. `python3 _leistungen.py` prüft ohne zu bauen und listet Bildpfade, deren Datei fehlt |
| `_tpl_services.py` | Die Vorlage: je Sektion eine Funktion, die ihr Markup schreibt, `render_service()` setzt die Seite zusammen. Nur Markup, keine Daten |
| `_gen_services.py` | Logik: FAQ-Reihenfolge, Querverweise auf die Cases, Kennzahlen-Board, Wörterbuch-Hero (`_dhero`), Schreiben über den Nachlauf |
| `_nachlauf.py` | Regeln, die jede Seite nach dem Erzeugen durchläuft (Bildmaße, Footer, Buttons, Headlines, WebP, Ladeleistung, SEO-Kopf, Cache-Version). Die Leistungsseiten bekommen sie beim Erzeugen |
| `_seo.py` | liest `seo`, `nav` und `sub` für Title, Description, JSON-LD und `llms.txt` |
| `_build_performance_v3.py` | leitet die Vorschau `service-performance-marketing-v3.html` aus der Performance-Seite ab (nach der Regel `brand`) |

Die sechs Seiten: `service-ecommerce` (10), `service-performance-marketing` (20), `service-content-creation` (30), `service-websites` (40), `service-strategie` (50), `service-chatgpt-ads` (60). Die Zahl ist `reihenfolge`.

## 2. Seitenaufbau (Dramaturgie v2, alle sechs Seiten)

```
Kopf, Menü
Wörterbuch-Hero        dhero, tags, seo.label
Prozess-Schema         pmap
Das Problem            problem_label, problem_h, problem
These und Nutzen       bene_label, bene_h, intro, bene
Bildband               band
Zoom                   zoom
Visual                 visual (panels, phones oder stage)
Material aus Mandaten  content_cols            nur mit v2_content
Beweis-Kopf            proof_label, proof_h, proof_lead, proof_quote, channels (nur mit v2_graphic)
Stationen              tell
Kennzahlen             kennzahlen (geteilte Karten aus den Case-Dateien)
Punkt-Graphen          dotsec                  optional
Ausgewählte Ergebnisse oplist, darunter automatisch "Auch mit dieser Leistung"
Was Kunden sagen       voice
Wer daran arbeitet     crew
Logos                  logos                   leer = keine Sektion
Fit                    fit
Was als Nächstes       steps_next, tline (optional, Zeitleiste)
Im Detail              acc                     nur mit v2_content
FAQ                    seo.faq_first, faq, seo.faq_last
Das Angebot            offer_h, offer, deliver
Anfrage                chips, trust
Footer
```

## 3. Text ändern, neue Leistung anlegen

Text ändern: die Datei öffnen, den Wert ändern, `python3 _leistungen.py`, dann `sh _build.sh`. Die Seite entsteht neu, alle Nachlauf-Regeln laufen mit.

Neue Leistung:

1. Eine bestehende Datei kopieren nach `_content/services/service-<name>.json` (Dateiname = Slug plus `.json`, Slug beginnt mit `service-`). Dateien, deren Name mit `_` beginnt, werden nicht gebaut.
2. `slug` auf denselben Namen setzen, `reihenfolge` wählen (Position in `llms.txt` und im Build).
3. Texte, Zahlen und Bilder befüllen. Nur Zahlen, die im Reporting stehen. Optionale Sektionen weglassen (Abschnitt 4).
4. Verlinkung von außen ist handgebaut: Kachel in `#leistungen` der Startseite, Menü, Footer. Die Cases verlinken die Leistung über `meta.leistungen` in ihrer Datei; nur dann erscheinen sie unter "Auch mit dieser Leistung".
5. Für saubere Pfade im Live-Modus: `path_for()` in `_seo.py` und `vercel.json` prüfen (`/services/<name>`).
6. `python3 _leistungen.py`, dann `sh _build.sh`, in der Vorschau ansehen.

## 4. Felder

Alle Texte dürfen einfaches HTML enthalten (`<b>`, `<em>`, `<i>`, `<br>`, `&amp;`). Listen von Zeilen (`*_h`, `h`) ergeben je Eintrag eine Headline-Zeile; die Teilung in Satoshi und Amandine setzt die Regel `headlines` danach selbst.

### Kopf

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `slug` | ja | gleich dem Dateinamen ohne `.json` |
| `reihenfolge` | ja | Zahl, Sortierung |
| `nav` | ja | Name der Leistung: Seitentitel vor dem SEO-Title, Name im JSON-LD und in `llms.txt`, Fallback für `seo.label` |
| `label` | nein | wird nicht angezeigt |
| `flow` | ja | `v2` (alle Seiten) oder `v1` (frühere Dramaturgie, Abschnitt 5) |
| `v2_content` | nein | `true`: Material-Collage aus `content_cols` und Detail-Raster aus `acc` erscheinen (bei ChatGPT Ads bewusst aus) |
| `v2_graphic` | nein | `true`: die Grafik `channels` steht direkt unter dem Beweis-Kopf |
| `tags` | ja | Badges unter dem großen Wort |
| `sub` | ja | ein Satz zur Leistung: `llms.txt`, Fallback der Description |

### seo, dhero

| Feld | Bedeutung |
|---|---|
| `seo.label` | Suchbegriff, z. B. "Performance Marketing Agentur Wien": unsichtbarer Teil der H1 im Hero, `serviceType` im JSON-LD |
| `seo.title`, `seo.desc` | Title und Meta Description (Description wird auf 158 Zeichen gekürzt) |
| `seo.answer` | Antwortabsatz für Suche und KI: steht im JSON-LD (Service), derzeit nicht sichtbar |
| `seo.faq_first` | `{frage, antwort}`: immer die erste Frage der FAQ |
| `seo.faq_last` | Liste `{frage, antwort}`: am Ende der FAQ, außer die Frage steht schon in `faq` |
| `dhero.word` | großes Wort über die ganze Breite (wird in Großbuchstaben gesetzt) |
| `dhero.kicker` | Zeile "<kicker> [Leistung]" |
| `dhero.text` | Definition; Wörter in `<em>` erscheinen in Amandine |
| `dhero.img`, `dhero.alt` | Foto über die volle Breite (2400 × 1371) und Alt-Text |

### Sektionen

| Feld | Bedeutung |
|---|---|
| `pmap` | Prozess-Schema: `label`, `h` (zwei Zeilen), `t`, `inputs` (Liste `{text, kurz, von}`; `von` ist `sie` oder `wir`; am Desktop steht `text`, wenn er höchstens 24 Zeichen hat, sonst `kurz`, am Telefon immer `kurz`), `engine` (`title`, `loop`: Wörter der Schleife), `touch` (Berührungspunkt mit dem Kunden), `output` (`titel`, `text` mit `|` als Zeilenumbruch, `tag`) |
| `problem_label`, `problem_h`, `problem` | Label, Headline-Zeilen und genau zwei Absätze; leerer erster Absatz = keine Sektion |
| `bene_label`, `bene_h`, `intro`, `bene` | Nutzen: Label, Headline, These (`intro`) und Kacheln `{titel, text}` (sechs) |
| `band` | Bildband: `label`, `imgs` (neun Bilder) |
| `zoom` | `img`, `side` (`left` oder `right`, der Textkasten steht gegenüber), `al` (Label), `ah` (Zeilen), `aside`, `alink` `{href, text}`, `zl` (Bildzeile, zugleich Alt-Text), `zt` |
| `visual` | `art`: `panels` (`label`, `h`, `t`, `d1` und `d2` je `{titel, text}`, `imgs`), `phones` (`h` als Zeilen, `t`, `phones`: Bilder oder `.mp4`) oder `stage` (`img`, `cap`) |
| `content_cols` | Material aus Mandaten: Liste von Spalten, je Spalte eine Liste von Bildern oder `.mp4` (bis sechs Spalten) |
| `proof_label`, `proof_h`, `proof_lead`, `proof_quote` | Beweis-Kopf: Label (Standard "Ergebnisse"), zwei Zeilen (die zweite kursiv), Lead, Satz darunter (entfällt, wenn `quote` gesetzt ist) |
| `proof_nums` | Zahlenreihe `{wert, label}` unter dem Kopf, derzeit überall leer |
| `channels` | Grafik als Punktreihen: `label`, `rows` (`{label, prozent, wert}`, der höchste Wert wird hervorgehoben), `note`; `link` wird nicht gezeigt |
| `tell` | Stationen: `steps` (`{wert, label, titel, text}`, vier), `nolabel` (`true`: kein eigenes Label, Standard), `label`; `h` und `t` werden derzeit nicht gezeigt |
| `kennzahlen` | Board: `headline` (zwei Zeilen), `karten`: geteilte Karten `{"ref": "<id>", "link": {"href", "text"}}` aus den Case-Dateien (Liste der ids: CMS-CASES.md, Abschnitt 5) |
| `dotsec` | Punkt-Graphen: `h`, `t`, `blocks` (je `rows` mit `{label, punkte, an, wert, hervorgehoben}` und `note`) |
| `oplist` | Ausgewählte Ergebnisse: `{href, titel, wert, label}`. `href` muss ein Case sein. Darunter folgen automatisch alle weiteren Cases, die die Leistung in `meta.leistungen` nennen |
| `voice` | `label`, `lead` (oder `q` als Zitat), `a` (wer), `note`, `video` (Poster: `<video>-poster.jpg`) oder `img` |
| `crew` | `label`, `h`, `t`, `people` (`{name, rolle, text, bild}`, vier) |
| `logos` | Namen der Logos in `assets/logos/<name>.png`, acht Plätze; leer = keine Sektion |
| `fit` | `label`, `h`, `intro`, `yes_h`, `yes`, `no_h`, `no` |
| `steps_next` | `h`, `rows` (`{wann, titel, text}`) |
| `tline` | Zeitleiste im Ablauf: `seg` (Abschnitte als Code und Anzahl, z. B. `h1 b9 g4 t28`), `aria`, `legend` (`{code, text}`) |
| `acc` | Im Detail: `{titel, text, punkte}` (vier Karten mit je vier Punkten) |
| `faq` | eigene Fragen `{frage, antwort}`; Reihenfolge auf der Seite: `seo.faq_first`, dann `faq`, dann `seo.faq_last` |
| `offer_h`, `offer`, `deliver` | Angebot: Headline, genau zwei Absätze, Liste "was Sie bekommen" |
| `chips`, `trust` | Auswahl im Anfrage-Block (wird in die Anfrage übernommen) und Badges darunter |
| `dotline`, `dotfield` | Punktzeile und Punktfeld des früheren Heros: bleiben in der Datei, werden derzeit nicht gezeigt |

## 5. Felder der Dramaturgie v1 (derzeit auf keiner Seite sichtbar)

Die frühere Dramaturgie (`flow: "v1"`) steht weiter in der Vorlage und ist mit den Dateien lauffähig. Ihre Felder bleiben deshalb in den Dateien: `h1`, `ital`, `sol_label` (Label vor dem Akkordeon), `acc` (dort als Akkordeon), `diff` (`{kicker, titel, text, bild}`, "Was wir anders machen"), `proofsplit` (`label`, `h`, `t`: Beleg-Paar), `bars` (zweite Grafik im Beleg-Paar, Felder wie `channels` plus `link`), `quote` (`{text, wer}`), `wall` und `wall_cols` (Content-Wand im Hochformat), `stoer` (Störer mit Risikoumkehr vor dem Angebot), `content_label`, `fit.cap_v` und `fit.cap_t`. `_leistungen.py` verlangt für `v1` zusätzlich `h1`, `intro`, `acc` und `diff`.

## 6. Bilder

Pfade stehen immer ab `assets/`. JPG ablegen; Breite und Höhe, WebP und Video-Poster setzt der Build beim Erzeugen (Regeln `imgdim`, `webp`, `poster`). Fotos ohne Filter, kein Lime auf oder an Fotos (BRAND-RULES 1 und 8). `python3 _leistungen.py` meldet Pfade, deren Datei fehlt.

## 7. Bauen und prüfen

```
python3 _leistungen.py                             # nur prüfen
sh _build.sh /private/tmp/adb-master-preview       # ganze Kette, danach Vorschau auf http://localhost:8743
```

Der Build bricht bei einem Fehler in einer Leistungsdatei mit Datei und Feld ab. Hinweise wie "service-strategie listet case-consumer-brand.html, aber der Case verlinkt die Leistung nicht" heißen: Der Case steht in `oplist`, nennt die Leistung aber nicht in seinem `meta.leistungen`.

## 8. Technische Hinweise zum Umbau (4.10.2026)

- Die Daten kamen aus `_gen_services.py` (`SERVICES`, `SEO`, `DHERO`, `STOER`, `SVC_COLS`, `SVC_WALL`) und `_kpi.py` (`SERVICE_KPI`). Sie stehen unverändert in den Dateien: Tupel wurden zu Objekten mit benannten Feldern, `SVC_COLS` heißt `content_cols`, `SVC_WALL` heißt `wall_cols`, `STOER` heißt `stoer`, `SERVICE_KPI` heißt `kennzahlen` (Karten per `ref` wie in den Case-Dateien).
- Die Umwandlung lief per Skript aus den alten Python-Daten. Ergebnis-Abgleich: Alle Seiten, `sitemap.xml`, `robots.txt`, `llms.txt`, `site.css`, `site.js` und `imgdim.json` sind nach dem Build Byte für Byte gleich wie vorher; die Dramaturgie v1 wurde zusätzlich für alle sechs Dateien alt gegen neu verglichen (gleich).
- Entfernt, weil ohne Wirkung: `logos_row()` (nirgends aufgerufen), `_heronum()` (kein Feld `heronum`, Ergebnis nie eingesetzt), `_chapnav()` (Kapitel-Leiste seit 24.9.2026 abgeschafft, gab nur noch "" zurück) und das Einlesen der Bildausrichtung aus `assets/content.json` (`_ORIENT`, nie verwendet).
- `_dhero` steht noch in `_gen_services.py` (gleicher Wortlaut wie vorher, damit parallele Änderungen am Hero sauber zusammenlaufen). Später kann er als Funktion nach `_tpl_services.py` wandern.

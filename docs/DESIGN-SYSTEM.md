# Master-Design: wo jeder Gestaltungswert liegt

Stand: 3.10.2026. Gilt fuer alle Seiten der Website. Die Marken-Regeln selbst stehen in `docs/BRAND-RULES.md`, diese Datei erklaert nur, wo die Werte im Code liegen und wie man sie aendert.

## Das Prinzip in drei Saetzen

1. Jeder Gestaltungswert (Farbe, Schrift, Groesse, Abstand, Radius, Schatten, Bewegung, Ebene) hat genau einen Namen und genau eine Quelle: `assets/tokens.css`.
2. Alle anderen Stylesheets verweisen nur auf diese Namen, zum Beispiel `border-radius: var(--r-img)` statt `border-radius: 16px`.
3. Der Browser laedt nur noch zwei Dateien: `assets/site.css` und `assets/site.js`. Beide werden beim Build aus den Einzeldateien erzeugt.

## Einen Wert aendern

Immer gleich: eine Zeile in `assets/tokens.css` aendern, dann den Build laufen lassen.

```
sh _build.sh /private/tmp/adb-master-preview
```

Beispiele:

| Was | Zeile in tokens.css | Wirkung |
|---|---|---|
| Radius aller Bilder und Karten | `--r-img: 16px;` | alle Bilder, Karten, Formularfelder, Kacheln |
| Radius der Collage-Bilder | `--r-col: 10px;` | nur die schraege Collage |
| Lime-Ton | `--lime: #CDFF00;` | Buttons, Menue-Knopf, Punkte, Graphen, Hover-Kreis |
| Cream-Ton | `--paper: #F4F3EB;` | Flaechen, Text auf Schwarz, alle Varianten davon |
| Seitenrand Desktop | `--gut: 64px;` (Mobile im Abschnitt 15) | Kopfzeile, Raster, Bildzeilen |
| Abstand oben und unten je Sektion | `--sec: 128px;` (Mobile 64 im Abschnitt 15) | alle Sektionen |
| Groesse des Menue-Knopfs | `--mbtn-size: 88px;` (Mobile 76) | Knopf, Wort im Knopf, Lage der Satelliten |
| Hover-Dauer | `--d-fast: 200ms;` | Buttons, Links, Chips (auch brand.js liest den Wert) |
| Kreisfarbe beim Hover eines Primary-Buttons | `--btn-primary-hv: var(--lime);` | nur Primary-Buttons |
| Schatten der Soft-Buttons | `--sh-soft: 0 4px 11px rgba(0,0,0,0.25);` | Soft Cream, Soft Lime, Menue-Knopf, Satelliten |

Wichtig: Transparenzen haben eigene Namen (`--ink-a16` heisst Schwarz mit 16 % Deckkraft, `--cream-a25` Cream mit 25 %). Sie sind fest in Zahlen geschrieben. Wer `--ink` aendert, muss die Stufen `--ink-a..` im Abschnitt 2 mit anpassen (gleiche Grundfarbe, gleiche Deckkraft).

## Was in tokens.css steht

| Abschnitt | Inhalt | Beispiele |
|---|---|---|
| 1 Farben | die fuenf Markenfarben und alte Namen, die darauf zeigen | `--ink`, `--paper`, `--lime`, `--stone`, `--ph` |
| 2 Transparenzstufen | Schwarz, Cream und Lime mit Deckkraft | `--ink-a06` bis `--ink-a92`, `--cream-a06` bis `--cream-a86` |
| 3 Linien und Grautoene | Linienfarben, Grautoene der Textfarbe | `--line-on-cream`, `--line-on-black`, `--line-badge`, `--grey` |
| 4 Schriften und Typo-Skala | Satoshi, Amandine, Groessen je Rolle | `--f-sans`, `--fs-h1`, `--fs-h2`, `--fs-ui`, `--fs-cap`, `--fs-logo` |
| 5 Zeilenhoehen | je Rolle | `--lh-head`, `--lh-body`, `--lh-ui` |
| 6 Abstaende | 8er-Skala und Rhythmus | `--sp-1` (8) bis `--sp-16` (128), `--gut`, `--sec`, `--h2b`, `--b2btn` |
| 7 Radien | Bilder, Collage, Pill, Kreis | `--r-img`, `--r-col`, `--r-pill`, `--r-round` |
| 8 Schatten | Soft-Buttons, Badge-Text, Kopfzeile ueber Fotos | `--sh-soft`, `--sh-soft-black`, `--sh-badge-text` |
| 9 Bewegung | eine Kurve, vier Dauern, Einblenden | `--e-out`, `--d-fast`, `--d-base`, `--d-slow`, `--d-chor`, `--fade-y`, `--stagger` |
| 10 Buttons | Masse und die acht Varianten | `--btn-fs`, `--btn-pad`, `--btn-soft-cream-bg`, `--btn-inverse-hv` |
| 11 Chips und Badges | Groesse und Innenabstand | `--chip-pad`, `--bdg-fs`, `--bdg-pad` |
| 12 Menue-Knopf | Knopf und Satelliten | `--mbtn-size`, `--mbtn-bottom`, `--sat-size`, `--sat-gap` |
| 13 Punkt-Graphen | Punktgroesse, Abstand, Farben | `--dot`, `--dot-gap`, `--g-on`, `--g-best`, `--g-line` |
| 14 z-Index-Ebenen | Reihenfolge von unten nach oben | `--z-chrome` (60) bis `--z-cur` (300) |
| 15 Mobile | was sich auf dem Telefon aendert | bis 767 px: Seitenrand 24, Sektion 64, Menue-Knopf 76; bis 720 px: Wortmarke 23 |
| 16 Varianten je Untergrund | Werte, die auf Schwarz oder Lime anders sind | `--grey` und `--line-l` auf dunklen Flaechen, Graph-Farben, Punktfeld |

Zu den Buttons: Je Variante gibt es sieben Namen. `bg` Flaeche, `fg` Text, `bd` Rand, `sh` Schatten, und fuer den Kreis-Hover `hv` Kreisfarbe, `hc` Textfarbe beim Hover, `hb` Randfarbe beim Hover. Eine Variante umfaerben heisst also: ihre Zeilen im Abschnitt 10 aendern.

Zu Abschnitt 16: `--grey`, `--grey-dark` und `--line-l` wechseln je Untergrund (Schwarz-Transparenz auf Cream, Cream-Transparenz auf Schwarz). Wer eine Linie braucht, die immer gleich aussieht, nimmt `--line-on-cream` oder `--line-on-black`.

## Welche Quelldatei wofuer zustaendig ist

Alle liegen in `assets/` und werden in genau dieser Reihenfolge zu `site.css` gebuendelt. Die Reihenfolge ist die Kaskade: spaetere Dateien gewinnen bei gleicher Spezifitaet.

| Datei | Zustaendig fuer |
|---|---|
| `tokens.css` | alle Werte (siehe oben), sonst nichts |
| `master.css` | Altbestand: Aufbau und Bausteine der Seite (Raster, Hero, Kacheln, Menue, Zoom, Fotowand). Nur :root, Pill-/Kreis-Radien und z-Index sind auf Token umgestellt. Am 4.10.2026 aufgeraeumt: Regeln ohne Treffer auf irgendeiner Seite und von den brand-Dateien vollstaendig ueberschriebene Altwerte sind entfernt (391 Regeln, site.css 17 % kleiner, Stil-Fingerabdruck ohne Abweichung). Stehen geblieben ist, was JavaScript setzt, was Inhalte jederzeit liefern koennen (z. B. blockquote, table) und die Button-Varianten des Design-Systems. |
| `brand.css` | Brand 2026, Grundschicht: der Punkt als Element (Cursor, Ladeblende, Punkt-Zoom, Punktzeilen, Coach, KPI-Karten) |
| `brand-type.css` | Typografie: welche Rolle welche Schrift, Groesse und Zeilenhoehe bekommt, Display-Headlines, grosse Zahlen |
| `brand-ui.css` | Design: Farben je Flaeche, Buttons, Textlinks, Badges, Chips, Menue-Knopf, Karten, Graphen |
| `brand-layout.css` | Layout: Raster, Seitenrand, Sektionsabstaende, Footer, Bildradien, Case-Hero |
| `brand-motion.css` | Bewegung: Dauern je Komponente, Einblenden, Hover, Kreis-Hover der Buttons, Reduced Motion |
| `brand-keep.css` | bewusst beibehaltene Elemente der alten Seite (BRAND-RULES Abschnitt 13), gewinnt als letzte Datei |

Scripts, gebuendelt zu `site.js`, jede Datei in eigenem Block:

| Datei | Zustaendig fuer |
|---|---|
| `brand.js` | laeuft zuerst: Ladeblende mit Punkt, Coach, Punkt-Graphen, Punkt-Zoom, Menue-Knopf nach Untergrund, Kreis-Hover. Liest Dauern und Kurve aus tokens.css. |
| `master.js` | Engine: Menue, Einblenden, Scroll-Effekte, Hero, Filter, Tile-Flip Work zu Case |

## Erzeugte Dateien: nie direkt bearbeiten

- `assets/site.css` und `assets/site.js` schreibt `_css.py`. Jede Aenderung darin ist beim naechsten Build weg.
- `_css.py` entfernt Kommentare und ueberfluessige Leerzeichen, laesst aber Reihenfolge, Strings und `url(...)` unangetastet. Die Kaskade bleibt gleich.
- Der Build (`_build.sh`) ruft `_css.py` vor den Generatoren auf, weil die Cache-Version `?v=` ein Inhalts-Hash von `site.css` und `site.js` ist und schon beim Erzeugen der Seiten feststehen muss. Die Regel "brand" (`_brand_inplace.py`) stellt aeltere Seitenkoepfe auf die zwei Dateien um, die Regel "version" (`_bump.py`) setzt die Cache-Version (aendert sich nur, wenn sich CSS oder JS aendern). Beide laufen fuer generierte Seiten beim Erzeugen und fuer handgebaute in `_nachlauf.py` (Reihenfolge der Regeln: README, Abschnitt Bauen).
- Jede Seite laedt im Kopf genau: `assets/site.css?v=N`, das Adobe-Fonts-Kit (`use.typekit.net/udf8wjj.css`) und `assets/site.js?v=N` (defer), davor Preconnect zu Typekit und Preload fuer Satoshi. Neue Seiten bekommen das ueber `HEAD` in `_gen.py`.
- Markup der Seiten: Cases in `_bausteine.py`, Leistungsseiten in `_tpl_services.py` (eine Funktion je Sektion), Inhalte in `_content/cases` und `_content/services`. Button-Varianten, Badges, Headline-Teilung und Abstands-Tokens setzen die Regeln "ui", "headlines" und "brand" einheitlich fuer alle Seiten, sie gehoeren nicht in die Vorlagen.

## Neue Werte und neue Bausteine

1. Gibt es den Wert schon als Token? Dann den Namen verwenden.
2. Wenn nicht: zuerst in `tokens.css` im passenden Abschnitt anlegen, mit kurzem Kommentar, dann in der zustaendigen Datei per `var(--name)` verwenden.
3. Werte, die nur fuer ein einziges Teil gelten (zum Beispiel die Lage eines einzelnen Punkts in einer Grafik), duerfen in der Bausteinregel stehen bleiben.
4. Farben nur aus Abschnitt 1 und 2. Kein Weiss, keine neuen Grau- oder Cream-Toene (BRAND-RULES Abschnitt 1).

## Pruefen nach einer Aenderung

- Build laufen lassen, Vorschau auf http://localhost:8743 ansehen.
- Fuer Umbauten ohne gewollte Aenderung: `sh _tools/fp.sh <ordner>` vorher und nachher, dann `python3 _tools/fpdiff.py <vorher> <nachher>`. Abweichungen ausser dem bekannten Rauschen (Hero-Zoom, wandernde Punkte auf Leistungsseiten, Work-Spalten) sind Fehler.

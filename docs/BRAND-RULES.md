# ad.boutique Brand-Regelwerk (Website)

Quelle: Figma-Datei `2S7tzOGpfn0qWfQ3wnhdiW`, Canvas "Design" (79:2268): Website / Komponenten (84:2), Rules / Badge (114:55), Rules / Typography (121:85), Rules / Amandine (122:85), Style 01 bis 12, Layouts (124:85), Brandbook (137:79).
Stand: 30.09.2026. Diese Datei ist verbindlich. Bei Widerspruch zu älteren Regeln (KONTEXT.md, brand.css-Kommentare, 28.9.-Headline-Regel) gilt diese Datei.

Ziel: 100 % einheitlich. Ein Element sieht überall gleich aus: ein Button-System, ein Badge, ein Chip, ein Footer, eine Collage-Größe, ein Graph-Stil.

---

## 1. Farben (Style 01)

| Token | Wert | Rolle |
|---|---|---|
| Cream | `#F4F3EB` | Hauptfläche, Text auf Schwarz |
| Black (Charcoal) | `#101010` | Text auf Cream, tragende Fläche |
| Lime | `#CDFF00` | Akzent: Aktionen, Highlights, Grafiken, reine Textflächen |
| Stone | `#B7B7B3` | nur Hintergrund hinter Mockups, nie Markenfläche |
| Bildplatzhalter | `#DEDDD4` | nur leere Bildcontainer |

Regeln:
- Kein Weiß, nirgends. Auf Schwarz sind Text und Buttons Cream.
- Verhältnis: Cream führt, Schwarz trägt, Lime akzentuiert.
- Erlaubte Paare: Schwarz auf Cream, Cream auf Schwarz, Schwarz auf Lime. Sonst nichts.
- Nie Lime-Text auf Schwarz, nie große Lime-Flächen auf Schwarz. Lime auf Schwarz nur als kleiner Status-Punkt.
- Nie Lime zusammen mit Fotos (keine Lime-Flächen, -Punkte, -Rahmen direkt an oder auf Fotos).
- Sektionsflächen sind genau eine von: Cream, Schwarz, Lime. Kein zweiter Cream-Ton (`#e9e8df` fällt weg), kein `#070708`, kein `#0f0f0f`.
- Linien: 1 px. Auf Cream `rgba(16,16,16,0.16)` (Badges 25 %), auf Schwarz `rgba(244,243,235,0.25)`.

## 2. Typografie (Rules / Typography, Rules / Amandine, Style 02, 03, 08)

Schriften: Satoshi (Bold 700, Medium 500, Regular 400) für alles. Amandine nur an genau zwei Stellen.

| Rolle | Schrift | Zeilenhöhe | Hinweis |
|---|---|---|---|
| H1 / Display (Hero, Vollbild-, Split-Sektionen) | Zeile 1 Satoshi Bold, Zeile 2 Amandine Italic | 110 % | Zeile 2 ist genau eine Zeile, der emotionale Teil |
| H2 | Satoshi Bold, nur | 110 % | Skala 1,55 zur nächsten Stufe |
| H3 | Satoshi Bold, nur | 110 % bis 120 % | |
| Body | Satoshi Regular | 140 % | |
| Buttons, Chips, Nav | Satoshi Medium 15 bis 17 px | 120 % | |
| Badges | Satoshi Medium 13 px (S 11 px) | normal | normale Schreibung, kein Versal |
| Große Zahlen ab 48 px (Stats, KPIs, Ergebnisse, Preise) | Amandine Medium | 110 % | Label darunter Satoshi Regular |

Abgrenzung H1 gegen H2 auf der Website: Eine Headline, die eine Sektion eröffnet und ab 1440 px Breite mindestens 48 px groß ist, gilt als Display und bekommt das H1-Muster (Satoshi-Zeile, dann Amandine-kursiv-Zeile auf eigener Zeile). Alles darunter (Zwischenüberschriften, Kartentitel, Akkordeon, FAQ, Kicker, Next-Project-Titel unter 48 px) ist Satoshi Bold ohne Amandine.

Nie Amandine für: den Markennamen ad.boutique (auch nicht im Logo, Footer-Wortmarke), die erste Zeile oder die ganze Headline, H2 und kleiner, einzelne Wörter im Fließtext, Buttons, Badges, Captions, Labels, kleine Zahlen im Text, Tabellen, Seitenzahlen.

Kundenzitate (`.vq`, `.kquote`, `.qbox p`) sind Satoshi (Medium oder Regular), nicht Amandine. Figma kennt keine Zitat-Ausnahme. Quelle Satoshi Regular.

Abstände: Headline zu Body 16 px (Web und Mobile). Body zu Buttons 48 px (Web), 32 px (Mobile).

Wortmarke: `ad.boutique`, Satoshi Bold, Kleinbuchstaben. Schutzraum mindestens die Höhe des "d". Der Punkt in der Wortmarke bleibt Satoshi.

## 3. Layout, Raster, Abstände (Style 04, 05, 06)

- Desktop-Format 1440 × 900, Seitenrand 64 px. Mobile 390 × 844, Seitenrand 24 px. Die Ränder sind fix je Format.
- 8-px-Skala: 8, 16, 24, 32, 48, 64, 96, 128. Abstände nur aus dieser Skala.
- Text steht auf der freien Seite, nie auf einem Gesicht.
- Vollformate (Full screen) haben keinen Radius.

## 4. Formen (Style 07, 10, 11)

- Buttons, Chips, Badges: immer Pill (`border-radius: 999px`).
- Karten und Bilder: Radius 16 px (Kundenentscheidung 3.10.2026, eine Spur kleiner als Figma 20; Token `--r-img`).
- Vollflächige Sektionen und Vollbild-Fotos: kein Radius.
- Alle Linien 1 px.
- Icons: Lucide, Strich 1,5, Textfarbe.

## 5. Komponenten (Website / Komponenten 84:2)

### Button (84:13)
Padding 16 px oben/unten, 24 px seitlich, Pill, Satoshi Medium 17 px, Zeilenhöhe 1,2.

| Variante | Fläche | Text | Rand/Schatten | Einsatz |
|---|---|---|---|---|
| Primary | `#101010` | Cream | keiner | Hauptaktion auf Cream |
| Secondary | transparent | Black | 1 px `#101010` | selten, auf Cream |
| Accent | Lime | Black | 1 px `#101010` | nur auf hellem Grund |
| Inverse | Cream | Black | keiner | Hauptaktion auf Schwarz |
| Outline Inverse | transparent | Cream | 1 px Cream | zweite Aktion auf Schwarz und auf Fotos |
| Soft Cream | `#F4F3EB` | Black | `0 4px 11px rgba(0,0,0,.25)` | zweite Aktion auf Cream |
| Soft Black | `#101010` | Cream | `0 4px 11px rgba(255,255,255,.14)` | zweite Aktion auf Schwarz |
| Soft Lime | Lime | Black | `0 4px 11px rgba(0,0,0,.25)` | zweite Aktion auf Lime |

Soft = exakt Seitenfarbe, sichtbar nur durch den Schatten. Nie Soft auf Fotos (dort Outline). Paarung: Primary + Soft Cream auf Cream, Inverse + Soft Black auf Schwarz, Primary + Soft Lime auf Lime, Primary/Inverse + Outline auf Fotos.
Hover: dezent (Schatten tiefer oder Fläche 6 % heller/dunkler), keine Farbwechsel in andere Markenfarben.

### Chip (84:21), für Filter und Auswahl
Padding 8 px / 24 px, Pill, Gap 8 px, Label Satoshi Medium 15 px, Zeichen Satoshi Regular 17 px.
Default: 1 px Rand `#101010`, Text Black, Zeichen "+". Selected: Fläche `#101010`, Text Cream, Zeichen "×". Kein Lime.

### Badge (99:137, Rules / Badge 114:55)
Keine Füllung, 1 px Rand mit 25 % Deckkraft (auf Cream/Lime `rgba(16,16,16,.25)`, auf Schwarz `rgba(244,243,235,.3)`), Satoshi Medium 13 px (S 11 px) in normaler Schreibung, Padding 8/16 (S 4/12), Pill. Soft Cream: Fläche Cream + `0 2px 6px rgba(0,0,0,.18)`, nur auf Cream. Kein Punkt, keine Lime-Füllung.
Platz: auf der Logo-Zeile (neben dem Logo oder zentriert darauf) oder in einer Ecke (rechter Rand der Textspalte, neben der Seitenzahl, Bildecke). Nie unter dem Logo, nie knapp über einer Headline. Unter dem Inhalt als Meta- oder Tag-Zeile mit 8 px Abstand.
Folge für die Website: Eyebrow-Labels direkt über Headlines (z. B. "Aus dem Mandat" in Lime) sind nicht erlaubt. Entweder weg oder als Badge in eine Ecke/Meta-Zeile.

### Navbar (84:35)
Wortmarke Satoshi Bold 25 px links, Aktion Primary "Projekt starten". Unsere Seite nutzt das schwebende Punkt-Menü (Figma: "floating menu, no header bar"), also keine Kopfleiste mit Fläche. Logo, Kontakt und Menü-Knopf schweben.

### Service Card (84:45)
1 px Rand `#101010`, Radius 16 (Token --r-img), Padding 32, Gap 16. Nummer Satoshi Regular 15 px, Titel Satoshi Bold 28,5 px, Text Satoshi Regular 16 px.

### Case Card (84:50)
Bild Radius 16 (Token --r-img) (Platzhalter `#DEDDD4`), darunter Gap 16: Chip (Branche), Kundenname Satoshi Bold 26,5 px, Ergebnis Satoshi Regular 18,5 px. Der Punkt (36 px, Schwarz) sitzt unten links im Bild als Marken-Akzent, nie Lime auf dem Foto.

### Stat (84:59)
Punktreihe (Daten-Punkte, der aktuelle/beste Wert gefüllt Lime oder Schwarz, der Rest Umriss oder Schwarz), darunter Wert Amandine Medium (ab 48 px auf der Website, Figma-Komponente 35 px), darunter Label Satoshi Regular 17 px. Gap 8.

### Footer (84:69), auf JEDER Seite identisch
Fläche `#101010`, Padding 96 oben, 48 unten, 64 seitlich (Mobile 24), Gap 64.
- Oben: links Headline im H1-Muster "We make" (Satoshi Bold) / "attention perform." (Amandine Italic), rechts zwei Buttons: Inverse "Projekt starten" (zu kontakt.html) und Outline Inverse "Unsere Arbeit" (zu work.html).
- Trennlinie 1 px `rgba(244,243,235,.25)`.
- Unten eine Zeile: Wortmarke `ad.boutique` Satoshi Bold 23 px links, Links Satoshi Regular 15 px mittig (Impressum, Datenschutz, Instagram, LinkedIn; Gap 32), rechts "Digitale Marketing Agentur Wien" Satoshi Regular 15 px.
- Rechtliche Zeile (Firmierung und Stand, von `_seo.py` gepflegt) darf klein darunter stehen, Satoshi Regular 13 px, Cream 60 %.
- Keine riesige Wortmarke (`.fword`) mehr, keine vierspaltigen Varianten, keine Seiten mit anderem Footer.

## 6. Punkt (Style 09)

- Signatur: ein kleiner Punkt pro Fläche, immer an derselben Stelle.
- Aufzählungspunkt: ersetzt Listenzeichen.
- Daten-Einheit: Graphen bestehen aus Punkten.
- Zustände: Punkt, Kontakt, Fokus, Target.
- Nie als große Dekoration. Keine dekorativen Lime-Punkte neben Headlines oder unter dem Menü (Startseite `.hpitch .bdot` fällt weg).

## 7. Daten und Graphen (Presentation / Tables and diagrams, Style 09)

- Diagramme aus Punkten. Aktueller oder bester Wert gefüllt, der Rest Umriss (1 px).
- Auf Cream: gefüllt = Schwarz oder Lime (Lime nur für den einen hervorgehobenen Wert), Umriss = Schwarz 1 px. Auf Schwarz: gefüllt = Cream, Umriss = Cream 1 px, Lime höchstens als ein kleiner Status-Punkt. Auf Lime: Schwarz gefüllt, Schwarz Umriss.
- Große Werte Amandine Medium, Achsen, Labels, Legenden Satoshi Regular 13 bis 15 px.
- Tabellen: Satoshi, 1-px-Linien, keine Füllflächen außer Cream/Schwarz/Lime.

## 8. Bilder (Style 12)

- Vollbild (ohne Radius), im Container mit Radius 16 (Token --r-img) oder als Kreis-Ausschnitt.
- Natürliches Licht, keine Filter. Keine Graustufen-Filter als Stilmittel (Ausnahme: bestehende Agentur-Collage darf bleiben, siehe 10).
- Kein Lime an Fotos.

### Schräge Collage (Referenz: Funkhaus-Case "Aus dem Mandat")
Einzige erlaubte Größe ist die Referenz `collage--tight` (sechs Spalten, `rotate(-7deg)`, Spaltenabstand `clamp(11px,1.3vw,20px)`, Höhe `clamp(620px,88vh,940px)`, Mobile 4 Spalten). Keine größere Variante (die dreispaltige `.collage` ohne `--tight` fällt weg). Bilder darin einheitlich Radius 10 px (Token `--r-col`, 3.10.2026), Schatten wie bisher.

## 9. Animation (Style 09, Brand-Punkt)

- Eine Bewegungssprache: der Punkt. Eintritt, Fokus-Ring, Wandern in den Menü-Kreis.
- Eine Easing-Kurve und eine Dauer-Skala für alles: `--e-out: cubic-bezier(.16,1,.3,1)`; Dauern 200 ms (Hover), 400 ms (Einblenden), 700 ms (Übergänge), 1200 ms (Choreografie).
- Einblenden überall gleich (gleicher Versatz, gleiche Dauer, gleiche Staffelung).
- Hover überall gleich je Komponententyp.
- Keine Lime-Glow-Effekte auf Schwarz, keine großen Lime-Flächen in Bewegung auf Schwarz.
- `prefers-reduced-motion` respektieren.
- Beibehalten: Coach (Variante 2 + 5), Tile-Flip Work zu Case und zurück, Ladeblende mit Punkt.

## 10. Seiten-Sonderregeln

- Agentur (agentur.html): Bilder und Bildaufbau bleiben wie sie sind. Nur Schriften, Farben, Buttons, Badges, Footer nach diesem Regelwerk.
- Work (work.html): die beiden Filter-Knöpfe links und rechts sehen identisch aus (gleiche Größe, Fläche, Rand, Schrift).
- Menü-Knopf unten Mitte: größer als heute (Richtwert 88 px Durchmesser Desktop, 76 px Mobile), Wort "Menü" im Punkt, Satoshi Medium.
- Startseite: der grüne Punkt rechts oben unter dem Menü-Knopf (`.hpitch .bdot`) entfällt.

## 11. Prüfliste für den Brand-Check

Farbe: nur die vier Tokens plus Transparenzen davon; kein Weiß; kein Lime-Text auf Schwarz; keine Lime-Fläche an Fotos; Sektionsflächen nur Cream/Schwarz/Lime.
Schrift: nur Satoshi und Amandine; Amandine nur als Zeile 2 von Display-Headlines und für Zahlen ab 48 px; Wortmarke Satoshi.
Form: Buttons/Chips/Badges Pill; Karten/Bilder Radius 16 (Token --r-img) (Collage 12); Linien 1 px.
Komponenten: jeder Button entspricht einer der acht Varianten; jedes Label über Headlines ist weg oder ein Badge; Chips nach 84:21; Footer identisch auf allen Seiten.
Layout: Seitenrand 64/24; Abstände aus der 8er-Skala; Headline zu Body 16 px; Body zu Buttons 48/32 px.
Collage: nur Referenzgröße.
Animation: eine Easing, eine Dauer-Skala, Reduced-Motion.


## 12. Button-Hover (3.10.2026)

Alle Buttons der acht Varianten: Beim Überfahren wächst ein Kreis von der Eintrittsstelle der Maus und füllt den Pill, beim Verlassen zieht er sich zur Austrittsstelle zurück (brand-motion.css, brand.js `btnPoint`). Kreisfarben: Primary Lime (Text Schwarz), Secondary, Accent, Soft Cream und Soft Lime Schwarz (Text Cream), Inverse Schwarz mit Cream-Rand (Text Cream), Outline Inverse und Soft Black Cream (Text Schwarz). Primary auf Lime-Fläche: Cream-Kreis. Ohne Hover-Geräte kein Kreis, bei reduzierter Bewegung ohne Animation.

## 13. Bewusst beibehaltene Elemente der alten Seite (Kundenentscheidung 3.10.2026)

Diese Elemente bleiben wie auf der alten Seite und gelten überall, auch wenn sie vom Figma-Regelwerk abweichen (assets/brand-keep.css, lädt als letzte Datei):

- Punktgrafiken (Punktfeld, Waffel, Punktreihen, Raster): gezählte Punkte Lime mit dunklem Ring, der Rest grau gefüllt. Bei Vergleichsreihen sind normale Reihen schwarz gefüllt, die hervorgehobene Reihe Lime. Auf Schwarz: Rest grau-transparent, gezählt Cream bzw. Lime ohne Ring. Hinweis "Antippen" in Versalien mit Lime-Punkt.
- Punktzeile (strategen, kreative, performance-nerds): Lime-Punkte mit dunklem Ring.
- Textlinks (`.alink`, `.zalink`, `.svc-back`, Link-Paare unter Fotowand und Panel): Versalien, Sperrung, Unterstrich, kein Pill. Nie in Lime, auf Schwarz in Cream.
- KPI-Kacheln der Startseite: immer Bild oben, darunter Name, Satz, Zahl und Label (keine Farbkachel mit Zahl im Bild).
- Startseite: der helle Kreis wächst rund über die dunkle Sektion darüber hinaus (`.zcircle`).

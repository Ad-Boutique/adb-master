# ad.boutique Brand 2026 · Designsystem

Exportierbares Paket aus dem aktuellen Stand der Website: `main` bei Commit `5d4ca3a` (Brand-Vereinheitlichung nach Figma, Kreis-Hover, Radius 16/10, Stand 3.10.2026). Quellen: `assets/tokens.css`, `brand-type.css`, `brand-ui.css`, `brand-layout.css`, `brand-motion.css`, `brand-keep.css`. Gedacht zum Anwenden im Agency Hub.

Online-Referenz mit Live-Vorschauen: https://claude.ai/artifact/WKH8NBDNbHKdf1Sf7SixA3

## Inhalt

| Datei | Zweck |
| --- | --- |
| `adb-fonts.css` | `@font-face` fuer Satoshi (Dateien in `fonts/`) |
| `adb-tokens.css` | alle Variablen `--adb-*`: Farben, Rollen fuer Cream und Schwarz, Typo-Skala, 8er-Abstaende, Radien, Schatten, Bewegung, Masse der Bedienelemente, Mobile-Werte |
| `adb-components.css` | 20 Komponenten mit Praefix `adb-` |
| `adb.js` | Kreis-Hover der Buttons, Einblenden (`data-fade`), Woerterbuch-Wort einpassen, Akkordeon |
| `tokens.json` | dieselben Tokens als Daten fuer Tools, Tailwind oder Figma |
| `components/*.md` | Richtlinien und HTML je Komponente |
| `index.html` | Showcase aller Komponenten, lokal im Browser oeffnen, mit Umschalter Cream/Schwarz |
| `fonts/` | Satoshi Variable (normal, kursiv) |

## Im Agency Hub einbinden

```html
<link rel="stylesheet" href="https://use.typekit.net/udf8wjj.css"> <!-- Amandine -->
<link rel="stylesheet" href="/designsystem/adb-fonts.css">
<link rel="stylesheet" href="/designsystem/adb-tokens.css">
<link rel="stylesheet" href="/designsystem/adb-components.css">

<body class="adb">
  <section class="adb-section"><div class="adb-wrap">
    <h1 class="adb-h1">Alle Kunden. <i>Ein Blick.</i></h1>
    <div class="adb-btns" style="margin-top:var(--adb-b2btn)">
      <a class="adb-btn adb-btn--primary" href="#">Projekt starten</a>
      <a class="adb-btn adb-btn--soft-cream" href="#">Alle Cases</a>
    </div>
  </div></section>
  <section class="adb-section adb-ink">...</section>
  <script src="/designsystem/adb.js"></script>
</body>
```

- Den Ordner `designsystem/` 1:1 in den Hub kopieren, die Pfade in `adb-fonts.css` sind relativ (`fonts/...`).
- **Amandine:** kommt aus dem Adobe-Fonts-Kit `udf8wjj`. Die Domain des Hubs im Kit freischalten (fonts.adobe.com, Web-Projekt, Domains), sonst faellt die Amandine-Zeile auf Georgia zurueck.
- **Untergrund:** Cream ist Standard. `class="adb-ink"` oder `data-theme="dark"` auf einem Bereich schaltet auf Schwarz.
- **Buttons:** Die Variante richtet sich nach dem Untergrund (siehe unten). Ohne `adb.js` waechst der Hover-Kreis aus der Mitte statt von der Maus.
- **Framework:** Die CSS-Dateien funktionieren ohne Build. In React/Vue global importieren und die Klassen verwenden, `adb.js` nach dem Rendern laden oder seine vier Funktionen nachbauen. Fuer Tailwind lassen sich die Variablen im `theme.extend` referenzieren, z. B. `colors: { lime: "var(--adb-lime)", ink: "var(--adb-ink)", paper: "var(--adb-paper)" }`, `borderRadius: { img: "var(--adb-r-img)" }`.

## Was sich gegenueber der ersten Version geaendert hat

- Farben: Lime ist jetzt `#CDFF00`, Schwarz `#101010`, Cream `#F4F3EB`. Kein zweiter Cream-Ton, kein Graphit mehr: Grautoene sind Transparenzen der Textfarbe.
- Schrift: Satoshi fuer alles in 700/500/400, keine Versalien, keine Sperrung. Amandine nur noch als zweite Headline-Zeile (0,88) und fuer grosse Zahlen. Reckless entfaellt.
- Buttons: Pill statt 2 px Ecke, acht Varianten, Kreis-Hover. Neue Komponenten: Badge, Footer, ServiceCard, CaseTile, FormField, DictionaryHero, Consent.
- Formen: Radius 16 fuer Bilder, Karten und Felder, Karten mit 1 px Rand statt Flaeche. Linien 1 px durchgezogen statt gepunktet.
- Entfallen: der grosse Hero-Punkt, Eyebrow-Labels ueber Headlines, Lime-Pillen in KPI-Karten, Graustufen-Fotos.

## Die wichtigsten Regeln

### Inhalt und Ton

- **Sie-Form**, direkt und nuechtern. Kurze Saetze, Zahlen statt Adjektive: "Mehr Umsatz. Kein Zufall.", "Wir gewinnen nur, wenn Sie gewinnen."
- **Zahlen sind Beweise.** Nur echte, belegte Werte, immer mit Kontext: "Vom Schnitt der ersten Kampagne zur ersten Welle."
- Zahlen im deutschen Format: `€ 11,77`, `€ 4,65 Mio.`, `−57 %`. Eine grosse Zahl bricht nie um.
- **Normale Schreibung, keine Sperrung.** Keine Versal-Headlines, keine gesperrten Labels. Ausnahmen nur fuer die beibehaltenen alten Textlinks und das Wort im Woerterbuch-Hero.
- **Kein Eyebrow** direkt ueber einer Headline. Was frueher Label war, wird Badge in Ecke oder Meta-Zeile, oder entfaellt.
- Keine Emoji, keine Ausrufezeichen, keine Gedankenstriche.
- Knoepfe sagen, was passiert: "Projekt starten", "Direkt anfragen", "Case ansehen".
- Der Footer spricht Englisch: "We make attention perform."

### Farbe

- Nur drei Markenfarben plus Transparenzen davon: `adb-paper` (Cream), `adb-ink` (Schwarz), `adb-lime`. `adb-stone` nur hinter Mockups, `adb-placeholder` nur in leeren Bildcontainern.
- Grund ist Cream (Farbwelt Cream). Dunkle Sektionen und der Footer sind Schwarz: `class="adb-ink"` oder `data-theme="dark"` schaltet `adb-bg`, `adb-fg`, `adb-fg-muted`, `adb-line` und die Graph-Farben um.
- Grautoene sind Transparenzen der Textfarbe: `adb-fg-muted` (64 %, 5,5:1) fuer Captions und Kartenlisten, `adb-fg-subtle` (50 %, 3,5:1) nur fuer durchgestrichene Vorher-Werte und Nebeninfo.
- **Lime** ist Aktion, Highlight, Grafik: Menue-Knopf auf Cream, Accent-Button, Kreis-Hover des Primary-Buttons, gezaehlte Punkte, Regler-Griff, Textmarkierung. **Nie** als Text auf Schwarz, **nie** an Fotos, auf Cream nie als Text. Auf Schwarz hoechstens als einzelner Status-Punkt.
- Linien sind immer 1 px und durchgezogen (`adb-line`). Gepunktete 2-px-Linien gibt es nicht mehr.

### Typografie

- **Satoshi fuer alles**, in drei Schnitten: Bold 700 (Headlines, Wortmarke, Akkordeon-Titel), Medium 500 (Buttons, Chips, Badges, Navigation, Zitate), Regular 400 (Fliesstext, Captions).
- **Amandine nur an zwei Stellen:** Zeile 2 einer Display-Headline (Italic, `amandine-line`) und grosse Zahlen ab 48 px (`number`). Das Adobe-Kit `udf8wjj` liefert Amandine 400 und 700; alle grossen Zahlen laufen in 400.
- **Display-Headline (ab 48 px):** Zeile 1 Satoshi Bold, Zeile 2 Amandine Italic als eigene Zeile, 0,88 der Satoshi-Groesse: `<h1 class="adb-h1">Mehr Umsatz. <i>Kein Zufall.</i></h1>`. Unter 48 px (`h2`, `h3`) reines Satoshi.
- Skala bei 1440 / 390 px: `h1` 80 / 39, `h1-xl` 110 / 44, `display` 62 / 34, `h2` 42 / 28, `h3` = h2 / 1,55, Fliesstext 17, UI 15, Caption 13, Zahl 56 / 40. Zeilenhoehen: Headlines 1,1, H3 1,2, Text 1,4, UI 1,2.
- Kundenzitate in Satoshi Medium, nicht kursiv. Kleine Zahlen in Text und Tabellen in Satoshi Medium.
- Die Wortmarke `ad.boutique` ist Satoshi Bold, der Punkt in derselben Farbe (kein Lime).

### Abstand und Layout

- 8er-Skala: `adb-sp-1` 8 bis `adb-sp-16` 128. Keine Werte ausserhalb der Skala.
- Seitenrand `adb-gut` 64 (mobil 24). Sektion oben und unten `adb-sec` 128 (mobil 64), kurz `adb-sec-s` 64, knapp 48.
- In Bloecken: Headline zu Text 16, Text zu Buttons 48 (mobil 32), Knopf-Paare 8 auseinander.
- Karten im Raster mit 16 px Abstand, Padding 32 (mobil 24).

### Formen, Linien, Schatten

- **Pill** (`adb-r-pill`) fuer alles Bedienbare: Buttons, Chips, Badges, Anfrage-Leiste.
- **Radius 16** (`adb-r-img`) fuer alles Gezeigte: Bilder im Container, Karten, Formularfelder, Banner. Bilder in der schraegen Collage 10. Vollbilder ohne Radius.
- Kreise (`adb-r-round`) nur fuer Punkte, Menue-Knopf und Satelliten.
- Karten: 1 px Rand in Textfarbe, keine Flaeche, kein Schatten. Die Nein-Karte ist eine schwarze Flaeche.
- Schatten nur fuer Soft-Buttons, Menue-Knopf und Satelliten (`adb-sh-soft`), dazu der Textschatten der Kopfzeile ueber Fotos.
- Fokus: Buttons 2 px Lime-Umriss mit 2 px Abstand, Links und Felder 2 px in Textfarbe.

### Bewegung

- **Eine Kurve:** `--adb-e-out` `cubic-bezier(.16, 1, .3, 1)`. Vier Dauern: 200 ms Hover, 400 ms Einblenden, 700 ms Uebergaenge, 1200 ms Choreografie.
- **Kreis-Hover der Buttons:** ein Kreis waechst von der Eintrittsstelle der Maus und fuellt den Knopf, 700 ms mit `--adb-e-btn`; die Schrift wechselt mit leichter Verzoegerung. Je Variante eine erlaubte Farbpaarung (siehe Button).
- Einblenden: 24 px Versatz, 400 ms, gestaffelt um 80 ms (`data-fade` mit `adb.js`).
- Links: nur Deckkraft (60 %). Karten: 3,5 % Schleier. Chips: 6 % Schleier.
- `prefers-reduced-motion` stellt alles sofort hin.

### Bildsprache

- Fotos ohne Filter (keine Graustufen mehr), ausser auf der Agentur-Seite.
- Text und Kennzahlen nie auf Gesichtern oder Kundenlogos. Lesbarkeit auf Fotos ueber Verlaeufe aus Schwarz-Transparenz.
- Kein Lime an Fotos: Badges, Kopfzeile und Zeiger sind dort Cream.

### Ikonografie

- Es gibt kein Icon-Set. Zeichen: Pfeile `→` `↓` `←`, "+" und "×" in Chips und Akkordeon.
- Punkte sind Zustand und Daten (10 px, Abstand 6 px), keine grosse Dekoration: der fruehere Hero-Punkt ist entfallen.
- Es gibt keine Logodatei: die Marke ist gesetzte Schrift (`adb-logo`, `adb-footer__mark`).

### Beibehaltene Elemente der alten Seite

Auf Kundenwunsch (3.10.2026) bleiben: die Punktgrafiken mit Lime-Punkten (`adb-dotgraph`, `adb-dotbars`), die Punktzeile (`adb-dotline`), die alten Versal-Textlinks an wenigen Stellen (`adb-keeplink`, `adb-back`) und die Agentur-CTAs in Amandine (`cta-amandine`).


## Nicht enthalten

- Die internen Regelwerk-Dokumente `_intern/BRAND-RULES.md` und `DESIGN-SYSTEM.md` (nicht im Repo). Dieses Paket ist aus den CSS-Dateien abgeleitet.
- Seiten-Choreografien aus `brand.js` (Ladeblende, Coach, Punkt-Zoom, Tile-Flip, Kopfzeilen-Messung, Cursor).
- Kundenlogos, Projektbilder und Portraits: das sind Inhalte, keine Marke.

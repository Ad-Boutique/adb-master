# ad.boutique Brand 2026 · Designsystem

Exportierbares Paket aus dem aktuellen Stand der Website (`assets/brand.css` ueber `assets/master.css`, alle Seiten mit `body.brand`, Stand 30.9.2026). Gedacht zum Anwenden im Agency Hub.

Online-Referenz mit Live-Vorschauen: https://claude.ai/artifact/WKH8NBDNbHKdf1Sf7SixA3

## Inhalt

| Datei | Zweck |
| --- | --- |
| `adb-fonts.css` | `@font-face` fuer Satoshi und Reckless (Dateien in `fonts/`) |
| `adb-tokens.css` | alle Variablen `--adb-*`: Palette, Rollen fuer Paper und Ink, Schrift, Abstaende, Radien, Schatten, Bewegung |
| `adb-components.css` | 17 Komponenten mit Praefix `adb-` |
| `tokens.json` | dieselben Tokens als Daten (Farben je Farbwelt, Schriftstile, Abstaende, Radien, Schatten) fuer Tools, Tailwind oder Figma |
| `components/*.md` | Richtlinien und HTML je Komponente |
| `index.html` | Showcase aller Komponenten, lokal im Browser oeffnen, mit Umschalter Paper/Ink |
| `fonts/` | Satoshi Variable (normal, kursiv), Reckless (Regular, Italic, Medium) |

## Im Agency Hub einbinden

```html
<link rel="stylesheet" href="https://use.typekit.net/udf8wjj.css"> <!-- Amandine -->
<link rel="stylesheet" href="/designsystem/adb-fonts.css">
<link rel="stylesheet" href="/designsystem/adb-tokens.css">
<link rel="stylesheet" href="/designsystem/adb-components.css">

<body class="adb">
  <section class="adb-section"><div class="adb-wrap">
    <span class="adb-label">Agency Hub</span>
    <h1 class="adb-h adb-h--section">Alle Kunden. <i>Ein Blick.</i></h1>
  </div></section>
  <section class="adb-section adb-ink">...</section>
</body>
```

- Den Ordner `designsystem/` 1:1 in den Hub kopieren, die Pfade in `adb-fonts.css` sind relativ (`fonts/...`).
- **Amandine:** kommt aus dem Adobe-Fonts-Kit `udf8wjj`. Die Domain des Hubs im Kit freischalten (fonts.adobe.com, Web-Projekt, Domains), sonst faellt die Serife auf Reckless zurueck.
- **Farbwelt:** hell ist Standard. `class="adb-ink"` oder `data-theme="dark"` auf einem Bereich schaltet auf dunkel.
- **Framework:** Die CSS-Dateien funktionieren ohne Build. In React/Vue einfach global importieren und die Klassen verwenden. Fuer Tailwind lassen sich die Variablen im `theme.extend` referenzieren, z. B. `colors: { lime: "var(--adb-lime)", ink: "var(--adb-ink)" }`.
- Interaktion (Akkordeon, Chips, Menue) liefert der Hub selbst. `index.html` zeigt ein minimales Beispiel.

## Die wichtigsten Regeln

### Inhalt und Ton

- **Sie-Form**, direkt und nuechtern. Kurze Saetze, Zahlen statt Adjektive: "Jeder Euro. Zurechenbar.", "Wir gewinnen nur, wenn Sie gewinnen."
- **Zahlen sind Beweise.** Nur echte, belegte Werte, immer mit Kontext in der Caption: "Vom Schnitt der ersten Kampagne zur ersten Welle."
- Zahlen im deutschen Format: `€ 11,77`, `1.385`, `−57 %` (Leerzeichen vor %, Euro-Zeichen vorne).
- Headlines in Satzform, nie in Versalien. Versal nur fuer `label`, `link` und kleine UI-Woerter wie "Menü".
- Keine Emoji, keine Ausrufezeichen, keine Gedankenstriche. Statt Strich: Komma, Doppelpunkt oder neuer Satz.
- Knoepfe sagen, was passiert: "Erstgespräch buchen", "Case ansehen", "Weiter".

### Farbe

- Grund ist `adb-paper` (Farbwelt Paper). Dunkle Sektionen nutzen die Farbwelt Ink: `class="adb-ink"` oder `data-theme="dark"` auf einem Bereich setzt `adb-bg`, `adb-fg`, `adb-fg-muted` und `adb-line` um.
- Komponenten nutzen nur die Rollen `adb-bg`, `adb-bg-alt`, `adb-surface`, `adb-fg`, `adb-fg-muted`, `adb-line`, `adb-line-dotted`. Palettenwerte (`adb-ink`, `adb-paper` ...) nur fuer Flaechen, die in beiden Welten gleich bleiben.
- **Lime ist Licht, kein Text.** `adb-lime` als Flaeche, Punkt, Ring oder Pille. Auf Paper nie als Schrift (Kontrast 1,1:1); dort bleibt der Akzent Ink. Fuer Akzent-Schrift `adb-accent-text` nehmen: Ink auf Paper, Lime auf Ink.
- Lime auf Paper bekommt immer eine 1px-Ink-Kontur (`adb-ring`), sonst verliert der Punkt seine Kante.
- Pro Ansicht wenig Lime: ein Punkt, eine Pille, ein aktiver Zustand. Lime gehoert zuerst dem Menue-Kreis.
- Kontraste: `adb-fg` auf `adb-bg` 17,2:1 in beiden Welten; `adb-fg-muted` 5,2:1 auf Paper, 4,7:1 auf Cream, 9,5:1 auf Ink. `adb-stone` auf Paper (1,8:1) nur fuer durchgestrichene Vorher-Werte.

### Typografie

- Zwei Stimmen: **Satoshi** (`--font-sans`) stellt fest, **Amandine kursiv** (`--font-serif`) antwortet einen Atemzug spaeter.
- **Headline-Regel:** Jede Headline hat einen Satoshi-Teil und einen Amandine-Teil. `<h1 class="adb-h adb-h--hero">Mehr Umsatz. <i>Kein Zufall.</i></h1>`. Der kursive Teil hat dieselbe Groesse, Gewicht 400.
- Jeder Absatz ist Satoshi (`body`, `lead`, `caption`). Die Serife ist fuer Zahlen (`number-xl`, `number-l`, `number-m`), Zitate (`quote`) und den kursiven Headline-Teil da, nie fuer Lesetext.
- Zahlen immer mit tabellarischen Ziffern (`adb-num`).
- Groessen der Website sind fluide. Die Styles nennen den Maximalwert, die `usage` den `clamp()`; `adb-components.css` setzt die fluiden Werte.
- Amandine kommt aus dem Adobe-Fonts-Kit `udf8wjj`. Wo es nicht geladen ist (z. B. in dieser Vorschau), greift Reckless als Ersatz. Satoshi und Reckless liegen als Dateien bei.

### Abstand und Layout

- Inhalt in `adb-wrap`: max. `adb-wrap-max` (1560px), Seitenrand `adb-gutter` fluide `clamp(26px, 6.4vw, 130px)`.
- Sektionen atmen: `adb-section` oben und unten `clamp(78px, 14vw, 210px)`.
- Stufen `adb-space-6` bis `adb-space-70` so verwenden, wie der Code sie nutzt: 6 zwischen Punkten, 14 von Punkt zu Text, 18 von Label zu Headline, 22 von Headline zu Text, 44 zwischen Bloecken.
- Karten im Raster mit `clamp(14px, 1.8vw, 28px)` Luecke, drei Spalten, unter 1000px eine.
- Lesetext max. 62 Zeichen breit.

### Formen, Linien, Schatten

- Fast eckig: Knoepfe `adb-radius-xs` (2px), Bilder `adb-radius-s` (3px), Karten `adb-radius-m` (4px). Rund ist nur, was ein Punkt ist: Kreise 50 %, Pillen `adb-radius-pill`.
- Linien: Haarlinie `adb-line` fuer Karten und Listen. **Der Punkt als Linie:** Trennlinien zwischen Fragen, Vergleichszeilen und Punktbalken sind 2px gepunktet in `adb-line-dotted`.
- Schatten nur fuer schwebende Kreise (`adb-shadow-float`, `adb-shadow-filter`). Karten haben Rand, keinen Schatten.
- Aktive Punkte bekommen den Lichthof `adb-halo-ring`.
- Fokus: 2px Umriss in `adb-fg`, 3px Abstand, in beiden Welten mind. 17:1.

### Bewegung

- Zwei Kurven: `--adb-e-out` `cubic-bezier(0.19, 1, 0.22, 1)` fuer alles, was ankommt (Hover, Einblenden), `--adb-e-snap` `cubic-bezier(0.76, 0, 0.24, 1)` fuer Oeffnen und Schliessen.
- Dauer 0,3 s fuer Farbe, 0,5 bis 0,6 s fuer Bewegung. Der Hero-Punkt pulsiert in 3,6 s.
- Knopf-Hover: 2px nach oben. Menue-Kreis: Skalierung 1.12.
- Die Punkte erzaehlen: Punktzeilen fuellen sich nacheinander, Ringe laufen beim Klick aus.
- `prefers-reduced-motion` schaltet Puls und Ringe ab.

### Bildsprache

- Eigene Bilder (Team, Buero, Stimmung) in Schwarzweiss: `adb-mono` (`grayscale(1) contrast(1.04)`), beim Hover farbig.
- Die Arbeit der Kunden bleibt farbig. Lime kommt nur als Spot dazu, nie als Filter.

### Ikonografie

- Es gibt kein Icon-Set. Statt Icons: Punkte (`adb-dot--s`), das Plus im Akkordeon, der Pfeil `→` als Zeichen.
- Die Marke ist gesetzte Schrift: `ad.boutique` in Satoshi 780 (`adb-wordmark`, `adb-logo`). Es gibt keine Bilddatei als Logo. Der Punkt im Namen ist auf Ink Lime, auf Paper Ink.


## Nicht enthalten

- Die alte Champagne-Palette aus `master.css` (`--champ #E9D8BC`, Reckless als Hauptserife). Sie ist durch das Brand 2026 ueberschrieben.
- Kundenlogos aus `assets/logos/` und Projektbilder: das sind Inhalte, keine Marke.
- Seiten-Choreografien aus `brand.js` (Coach, Punkt-Zoom, Ladeblende, Cursor). Sie sind an die Website gebunden; die Grundformen (Punkt, Ring, Puls) sind als Komponenten enthalten.

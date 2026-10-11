# Headline

Gruppe: Typografie

Headlines sind reines Satoshi Bold. Ab Display-Groesse (48 px) hat die Headline zwei Zeilen: Zeile 1 Satoshi Bold, Zeile 2 Amandine Italic in eigener Zeile, 0,88 so gross.

- `adb-h1` (Hero), `adb-h1--xl` (zentrierter Hero), `adb-display` (Sektionen, Splits): die zweite Zeile in `<i>`.
- `adb-h2` und `adb-h3` bleiben unter 48 px und haben keine Amandine-Zeile.
- Zeilenhoehe 1,1, normale Schreibung, keine Sperrung, nie Versal.
- Kein Eyebrow direkt ueber einer Headline. Ein Suchbegriff fuer SEO bleibt unsichtbar im H1.

```html
<div style="display:grid;gap:24px">
<h1 class="adb-h1">Mehr Umsatz. <i>Kein Zufall.</i></h1>
<h2 class="adb-h2">Die Beweise.</h2>
<h3 class="adb-h3">Strategie &amp; Funnel</h3>
</div>
```

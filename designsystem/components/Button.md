# Button

Gruppe: Aktionen

Button (Figma 84:13): Pill, Satoshi Medium 17 px, Padding 16/24. Beim Ueberfahren waechst ein Kreis von der Eintrittsstelle der Maus und fuellt den Knopf (700 ms).

- Auf Cream: `adb-btn--primary` (Hauptaktion), `adb-btn--soft-cream` (zweite Aktion), selten `--secondary`, `--accent` (Lime, nur auf hellem Grund).
- Auf Schwarz und Fotos: `adb-btn--inverse` (Hauptaktion), `adb-btn--outline-inverse` oder `--soft-black` (zweite Aktion).
- Auf Lime: `adb-btn--primary` und `--soft-lime`.
- Paare nebeneinander mit 8 px (`adb-btns`). `adb.js` laesst den Kreis der Maus folgen.
- Der Kreis ist nie Lime auf Schwarz.

```html
<div style="display:grid;gap:16px">
<div class="adb-btns"><a class="adb-btn adb-btn--primary" href="#">Projekt starten</a><a class="adb-btn adb-btn--soft-cream" href="#">Direkt anfragen ↓</a><a class="adb-btn adb-btn--secondary" href="#">Unsere Arbeit</a><a class="adb-btn adb-btn--accent" href="#">Weiter <i>→</i></a></div>
<div class="adb-ink adb-btns" style="padding:16px;border-radius:16px"><a class="adb-btn adb-btn--inverse" href="#">Projekt starten</a><a class="adb-btn adb-btn--outline-inverse" href="#">Unsere Arbeit</a><a class="adb-btn adb-btn--soft-black" href="#">Alle Cases</a></div>
</div>
```

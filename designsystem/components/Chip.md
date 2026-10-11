# Chip

Gruppe: Formular

Chip (Figma 84:21) fuer Filter und Auswahl: Rand in Textfarbe mit "+", gewaehlt gefuellt mit "×". Satoshi Medium 15 px, Padding 8/24. Kein Lime.

- `adb-chip`, gewaehlt `on` oder `aria-pressed="true"`. Ohne Zeichen: `adb-chip--plain`.
- Ueber Bildern (Work-Filter): `adb-chip--photo`, Schwarz mit Cream-Text, gewaehlt Cream.

```html
<div style="display:grid;gap:16px"><div class="adb-chips"><button class="adb-chip on" type="button">Meta Ads</button><button class="adb-chip" type="button">Google Ads</button><button class="adb-chip" type="button">Website</button></div>
<div class="adb-chips adb-ink" style="padding:16px;border-radius:16px"><button class="adb-chip adb-chip--photo on" type="button">Alle</button><button class="adb-chip adb-chip--photo" type="button">Performance</button><button class="adb-chip adb-chip--photo" type="button">Websites</button></div></div>
```

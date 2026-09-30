# Chip

Gruppe: Formular

Chip: zwei Arten. Filter-Chips sind Ink mit Paper-Wahl. Auswahl-Chips im Anfrageformular tragen einen Punkt, der sich Lime fuellt.

- `adb-chip` (aktiv: `on`), `adb-option` mit `<span class="o">` (gewaehlt: `sel`).

```html
<div style="display:grid;gap:18px">
<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="adb-chip on" type="button">Alle</button><button class="adb-chip" type="button">Performance</button><button class="adb-chip" type="button">Websites</button></div>
<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="adb-option sel" type="button"><span class="o"></span>Meta Ads</button><button class="adb-option" type="button"><span class="o"></span>Google Ads</button><button class="adb-option" type="button"><span class="o"></span>Website</button></div>
</div>
```

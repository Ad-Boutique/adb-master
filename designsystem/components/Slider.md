# Slider

Gruppe: Formular

Slider: 2px-Bahn, der Griff ist ein Lime-Punkt mit Ink-Rand und Lichthof.

- `input type="range" class="adb-range"`. Darueber Budget und Ergebnis in Amandine (`adb-num`), gerechnet mit einem echten Preis je Anfrage: jeder Punkt eine Anfrage.

```html
<div style="max-width:420px"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="adb-num" style="font-size:30px">€ 3.000</span><span style="font-size:13px;font-weight:700"><span class="adb-num" style="font-size:22px;margin-right:6px">300</span>Anfragen</span></div><input class="adb-range" id="budget" type="range" min="500" max="10000" value="3000" aria-label="Budget"></div>
```

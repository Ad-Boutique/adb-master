# FormField

Gruppe: Formular

FormField: Label 15 px Medium, Feld mit Radius 16, 1 px Rand 25 %, Innenabstand 16/24; im Fokus Rand in Textfarbe. Darunter der Budget-Regler: 1 px Bahn, Griff Lime mit 1 px Schwarz.

- `adb-field` > `label` + `input.adb-input`; `input type="range" class="adb-range"`.

```html
<div style="display:grid;gap:24px;max-width:420px"><div class="adb-field"><label for="mail">E-Mail</label><input class="adb-input" id="mail" type="email" placeholder="name@firma.at"></div>
<div><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="adb-num" style="font-size:40px">€ 3.000</span><span class="adb-small"><b>300</b> Anfragen</span></div><input class="adb-range" id="budget" type="range" min="500" max="10000" value="3000" aria-label="Budget"></div></div>
```

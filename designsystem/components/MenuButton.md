# MenuButton

Gruppe: Navigation

MenuButton: der Menue-Kreis, 64px Lime mit dem Wort "Menü" im Punkt, fix unten mittig.

- `adb-menu`, fix positioniert mit `adb-menu--fixed`. Offen (`aria-expanded="true"`) kehrt er sich um: Ink mit Lime-Schrift "Schließen".
- Lime gehoert dem Menue: andere schwebende Kreise (Filter) sind Paper mit Ink-Rand.

```html
<div style="display:flex;gap:26px;align-items:center;padding:18px"><button class="adb-menu" type="button" aria-expanded="false">Menü</button><button class="adb-menu" type="button" aria-expanded="true">Schließen</button></div>
```

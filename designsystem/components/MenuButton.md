# MenuButton

Gruppe: Navigation

MenuButton: der schwebende Kreis unten Mitte, 88 px (mobil 76), Wort "Menü" im Kreis, Satoshi Medium.

- `adb-menu`, fix mit `adb-menu--fixed`. Auf Cream Lime mit 1 px Schwarz, auf Schwarz und Fotos Cream (`adb-menu--on-dark` oder in `adb-ink`). Offen (`aria-expanded="true"`): Cream mit "Schließen".
- Satelliten `adb-sat` (Filter, Branche, Übersicht): 64 px, Cream, 1 px Schwarz; offen Schwarz, aktiver Filter mit zweitem Ring (`has`).

```html
<div style="display:flex;gap:24px;align-items:center;flex-wrap:wrap"><button class="adb-sat" type="button">Filter</button><button class="adb-menu" type="button" aria-expanded="false">Menü</button><button class="adb-sat has" type="button">Branche</button><span class="adb-ink" style="display:inline-flex;padding:12px;border-radius:999px"><button class="adb-menu" type="button" aria-expanded="true">Schließen</button></span></div>
```

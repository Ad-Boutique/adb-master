# TextLink

Gruppe: Aktionen

TextLink: Versal-Link mit Unterstreichung, die beim Hover auf volle Breite waechst.

- `adb-link`: freie Links ("Mehr erfahren"), Linie startet bei 35 %.
- `adb-link--line`: der Link zum Case, ueberall dieselbe Form, volle Linie. Auf Ink wird er beim Hover Lime.

```html
<div style="display:flex;gap:44px;flex-wrap:wrap"><a class="adb-link" href="#">Mehr erfahren <span aria-hidden="true">→</span></a><a class="adb-link adb-link--line" href="#">Case ansehen</a></div>
```

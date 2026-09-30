# Button

Gruppe: Aktionen

Button: fast eckig (2px), fett, ruhig. Beim Hover wird Ink zu Lime.

- `adb-btn adb-btn--ink` auf Paper, `adb-btn--paper` auf Ink, `adb-btn--outline` als zweite Aktion.
- `adb-btn--go`: der Punkt wird zum Knopf, Lime-Pille mit Ink-Ring. Nur fuer den einen Weiter- oder Absenden-Schritt eines Formulars.
- Beschriftung als Handlung: "Erstgespräch buchen", "Weiter".
- Pro Sichtfeld hoechstens ein gefuellter Knopf.

```html
<div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center">
<a class="adb-btn adb-btn--ink" href="#">Erstgespräch buchen</a>
<a class="adb-btn adb-btn--outline" href="#">Alle Cases</a>
<button class="adb-btn adb-btn--go" type="button">Weiter</button>
</div>
```

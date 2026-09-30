# KpiCard

Gruppe: Daten

KpiCard: vorher, nachher und die Verbesserung als Lime-Pille, auf einen Blick.

- Aufbau: `adb-kpi__head` (Label + `adb-kpi__pill`), `adb-kpi__vals` (`__from` durchgestrichen, Pfeil, `__to` in Amandine), `adb-kpi__cap`, optional `adb-link--line` zum Case.
- Mehrere Karten im `adb-kpigrid` (3 Spalten, unter 1000px eine).
- Nur echte, belegte Zahlen. Die Caption sagt, woher die Zahl kommt.

```html
<div class="adb-kpi" style="max-width:380px">
<div class="adb-kpi__head"><span class="adb-kpi__label">Preis je Anfrage</span><span class="adb-kpi__pill">−57 %</span></div>
<div class="adb-kpi__vals"><span class="adb-kpi__from">€ 11,77</span><span class="adb-kpi__arrow" aria-hidden="true">→</span><span class="adb-kpi__to">€ 5,00</span></div>
<p class="adb-kpi__cap">Vom Schnitt der ersten Kampagne zur ersten Welle.</p>
<a class="adb-link adb-link--line" href="#">Case ansehen</a>
</div>
```

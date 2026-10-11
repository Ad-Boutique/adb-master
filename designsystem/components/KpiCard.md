# KpiCard

Gruppe: Karten

KpiCard: vorher, nachher und die Verbesserung als Badge in der Kartenecke.

- `adb-card` mit `adb-kpi__head` (Label 15 px + `adb-badge`), `adb-kpi__vals` (`__from` Satoshi Medium durchgestrichen, Pfeil, `__to` Amandine in Zahlengroesse), `adb-kpi__cap` 13 px.
- Nur echte, belegte Zahlen. Die Caption sagt, woher die Zahl kommt.

```html
<div class="adb-card" style="max-width:380px">
<div class="adb-kpi__head"><span class="adb-kpi__label">Preis je Anfrage</span><span class="adb-badge">−57 %</span></div>
<div class="adb-kpi__vals"><span class="adb-kpi__from">€ 11,77</span><span class="adb-kpi__arrow" aria-hidden="true">→</span><span class="adb-kpi__to">€ 5,00</span></div>
<p class="adb-kpi__cap">Vom Schnitt der ersten Kampagne zur ersten Welle.</p>
<a class="adb-btn adb-btn--soft-cream" href="#" style="align-self:flex-start">Case ansehen</a>
</div>
```

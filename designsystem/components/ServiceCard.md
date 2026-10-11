# ServiceCard

Gruppe: Karten

ServiceCard (Figma 84:45): 1 px Rand in Textfarbe, Radius 16, Padding 32 (mobil 24), Gap 16. Dieselbe Karte traegt KPI, Fit, Prozess und Zitat.

- `adb-card adb-svc` mit `adb-svc__n` (Nummer), `adb-svc__t` (Titel 28,5 px Bold), Liste in `adb-fg-muted`, `adb-link` am Ende.
- Mehrere im Raster `adb-cards` mit 16 px Abstand. Keine Schatten, keine Flaeche.

```html
<div class="adb-cards">
<a class="adb-card adb-svc" href="#"><span class="adb-svc__n">01</span><span class="adb-svc__t">Strategie &amp; Funnel</span><ul><li>Funnel-Architektur</li><li>KPI-Logik &amp; Attribution</li><li>Positionierung</li></ul><span class="adb-link">Mehr dazu →</span></a>
<a class="adb-card adb-svc" href="#"><span class="adb-svc__n">02</span><span class="adb-svc__t">Performance Marketing</span><ul><li>Meta, Google, TikTok</li><li>Lead-Generierung</li><li>Creative-Testing</li></ul><span class="adb-link">Mehr dazu →</span></a>
</div>
```

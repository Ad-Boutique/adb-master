# DotGraph

Gruppe: Daten

DotGraph (beibehalten): jede Einheit ein Punkt (10 px, Abstand 6 px). In Punktgrafiken sind die gezaehlten Punkte Lime mit dunklem Ring, der Rest grau gefuellt. In Punktbalken sind gefuellte Punkte Schwarz, die hervorgehobene Reihe Lime.

- `adb-dotgraph` (Raster, `--cols`), `adb-dotbars` mit `.row` und `.row.hi`, aktive Punkte `class="on"`.
- Auf Schwarz: Lime ohne Ring, gefuellt Cream. Immer eine Legende in Worten.

```html
<div class="adb-dotbars">
<div class="row"><span class="rl">Website-Formular</span><span class="dots"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="rv">€ 58,05</span></div>
<div class="row hi"><span class="rl">Instant Form</span><span class="dots"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></span><span class="rv">€ 9,59</span></div>
</div><p class="adb-caption" style="margin:14px 0 0">Dieselbe Zielgruppe, zwei Wege zur Anfrage. Ein Punkt sind zwei Euro.</p>
```

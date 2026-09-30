# DotGraph

Gruppe: Daten

DotGraph: Daten sind Identitaet. Jede Einheit ein Punkt, der Lime-Anteil ist die Aussage.

- `adb-dotgraph` (Raster, Spalten per `--cols`) mit `<i>`, aktive Punkte `class="on"`.
- `adb-dotbars`: Zeilen zum Vergleichen, die hervorgehobene Zeile `row hi` bekommt Lime, die anderen Ink.
- Immer eine Legende in Worten: "Ein Punkt ist ein Euro."

```html
<div class="adb-dotbars">
<div class="row"><span class="rl">Website-Formular</span><span class="dots"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="rv">€ 58,05</span></div>
<div class="row hi"><span class="rl">Instant Form</span><span class="dots"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></span><span class="rv">€ 9,59</span></div>
</div><p class="adb-caption" style="margin-top:14px">Dieselbe Zielgruppe, zwei Wege zur Anfrage. Ein Punkt sind zwei Euro.</p>
```

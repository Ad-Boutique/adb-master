# FitCard

Gruppe: Inhalt

FitCard: "Wir passen zusammen, wenn" und "Wir sind die Falschen, wenn" nebeneinander. Die Ja-Karte ist Cream, die Nein-Karte Ink.

- `adb-fit adb-fit--yes` / `adb-fit--no`, darin `h4` und `ul` > `li` mit `<span class="d">`. Angetippte Aussagen `hit` fuellen den Punkt.

```html
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px">
<div class="adb-fit adb-fit--yes"><h4>Wir passen zusammen, wenn</h4><ul><li class="hit"><span class="d"></span>Es Kampagnen gibt, in denen das Material laufen soll</li><li><span class="d"></span>Laufende Produktion statt einmaliges Shooting</li></ul></div>
<div class="adb-fit adb-fit--no"><h4>Wir sind die Falschen, wenn</h4><ul><li><span class="d"></span>Das Material nur in die Mediathek soll</li><li><span class="d"></span>Nur Studio-Look, kein Available Light</li></ul></div>
</div>
```

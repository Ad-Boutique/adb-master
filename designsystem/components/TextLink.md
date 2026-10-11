# TextLink

Gruppe: Aktionen

TextLink: im Fliesstext und in Karten bleibt ein Link Text. Satoshi Medium, Textfarbe, 1 px Unterstrich, beim Hover 60 % Deckkraft.

- `adb-link`. Alle anderen Links sind Buttons.
- `adb-keeplink` und `adb-keeplink--line`: die alten Versal-Links mit wachsender Linie, nur an den freigegebenen Stellen (Agentur-CTAs, einzelne Leistungs-Links im Case). `adb-back` fuer "← Alle Leistungen".

```html
<div style="display:flex;gap:40px;flex-wrap:wrap;align-items:baseline"><a class="adb-link" href="#">Mehr dazu →</a><a class="adb-keeplink" href="#">Zum Team stoßen <span aria-hidden="true">→</span></a><a class="adb-keeplink adb-keeplink--line" href="#">Leistung: Landingpages</a><a class="adb-back" href="#">← Alle Leistungen</a></div>
```

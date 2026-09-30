# Headline

Gruppe: Typografie

Headline in zwei Stimmen: Satoshi stellt fest, Amandine kursiv antwortet.

**Regel (seit 28.9.2026):** Jede Headline hat einen Satoshi-Teil und einen Amandine-Teil. Den antwortenden Teil in `<i>` setzen, meist der letzte Satz oder die letzten Woerter.

- Klassen: `adb-h` plus Groesse `adb-h--hero`, `--xl`, `--section`, `--m`, `--s`.
- Farbe `adb-fg`. Kein Versalsatz, keine Farbe auf dem kursiven Teil.
- Darueber optional ein `adb-label` als Eyebrow (SEO-Suchbegriff der Seite).
- Nicht: zwei kursive Teile in einer Headline, Serife fuer ganze Absaetze.

```html
<div style="display:grid;gap:18px">
<span class="adb-label">Digitale Marketing Agentur Wien</span>
<h1 class="adb-h adb-h--hero">Mehr Umsatz. <i>Kein Zufall.</i></h1>
<h2 class="adb-h adb-h--m">Drei Projekte, <i>drei Sprünge.</i></h2>
</div>
```

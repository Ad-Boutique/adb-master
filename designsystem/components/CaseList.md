# CaseList

Gruppe: Inhalt

CaseList: nummerierte Liste von Cases oder Leistungen. Die Nummer traegt einen Punkt, der beim Hover Lime wird, der Titel unterstreicht sich.

- `adb-list` > `a.adb-list__row` mit `__num`, `__title`, `__kpi` (`.v` Zahl, `.l` Label).
- Die Nummer zaehlt echt (01, 02, 03), weil die Liste eine Reihenfolge hat.

```html
<div class="adb-list">
<a class="adb-list__row" href="#"><span class="adb-list__num">01</span><span><span class="adb-list__title">Premium-Neubau, Wien</span></span><span class="adb-list__kpi"><span class="v">489</span><span class="l">Leads</span></span></a>
<a class="adb-list__row" href="#"><span class="adb-list__num">02</span><span><span class="adb-list__title">Bauträger-Portfolio, Wien</span></span><span class="adb-list__kpi"><span class="v">€ 5,93</span><span class="l">CPL</span></span></a>
</div>
```

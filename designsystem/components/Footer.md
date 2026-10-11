# Footer

Gruppe: Navigation

Footer (Figma 84:69): auf jeder Seite gleich, immer Schwarz. Headline "We make" Satoshi Bold mit Amandine-Zeile "attention perform.", rechts zwei Knoepfe, darunter eine Linie, Wortmarke, Links und rechtliche Zeile.

- `adb-footer` mit `__top`, `__h`, `adb-btns`, `__rule`, `__bot`, `__mark`, `__links`, `__legal`.
- Knoepfe: `adb-btn--inverse` und `adb-btn--outline-inverse`.

```html
<footer class="adb-footer" style="padding:48px 24px 32px;border-radius:16px"><div class="adb-footer__in">
<div class="adb-footer__top"><div class="adb-footer__h" style="font-size:56px"><span>We make</span> <i>attention perform.</i></div><div class="adb-btns"><a class="adb-btn adb-btn--inverse" href="#">Projekt starten</a><a class="adb-btn adb-btn--outline-inverse" href="#">Unsere Arbeit</a></div></div>
<div class="adb-footer__rule"></div>
<div class="adb-footer__bot"><a class="adb-footer__mark" href="#">ad.boutique</a><nav class="adb-footer__links"><a href="#">Impressum</a><a href="#">Datenschutz</a><a href="#">Instagram</a><a href="#">LinkedIn</a></nav><span class="adb-footer__loc">Digitale Marketing Agentur Wien</span></div>
<p class="adb-footer__legal">© 2026 Ad Boutique Agency GmbH, Wien.</p>
</div></footer>
```

# Accordion

Gruppe: Inhalt

Accordion (FAQ): Frage Satoshi Bold, Plus dreht sich zum Kreuz, Antwort 15 px in `adb-fg-muted`. Linien 1 px durchgezogen (keine gepunkteten Linien mehr).

- `adb-faq__item` (offen: `open`), `button.adb-faq__q` mit `.plus`, `adb-faq__a` > `p`. `adb.js` schaltet um.

```html
<div>
<div class="adb-faq__item open"><button class="adb-faq__q" type="button" aria-expanded="true">Was ist UGC? <span class="plus">+</span></button><div class="adb-faq__a"><p>Videos und Bilder, die Creator im eigenen Stil drehen, nicht im Studio. Im Feed sieht das nicht nach Werbung aus.</p></div></div>
<div class="adb-faq__item"><button class="adb-faq__q" type="button" aria-expanded="false">Wir haben schon einen Fotografen. <span class="plus">+</span></button><div class="adb-faq__a"><p>Gut so. Wir ergänzen das System dahinter: Hooks, Testing, Winner-Selektion.</p></div></div>
</div>
```

# Consent

Gruppe: Seiten

Consent: Einwilligungs-Banner als schwarze Karte unten links (Radius 16), Text mit Link "Datenschutz", zwei gleichwertige Inverse-Knoepfe.

- `adb-consent` mit `p` und `adb-btns`. Fixe Lage unten links mit `var(--adb-gut)` Abstand; unter 1024 px ueber dem Menue-Knopf.

```html
<div class="adb-consent"><p>Darf ad.boutique messen? Mit Ihrer Zustimmung laden wir Google Tag Manager und das Meta-Pixel, um zu sehen, welche Kampagnen wirken. Ohne Zustimmung speichern wir nur Ihre Auswahl. <a href="#" style="color:inherit">Datenschutz</a></p><div class="adb-btns"><button class="adb-btn adb-btn--inverse" type="button">Alle akzeptieren</button><button class="adb-btn adb-btn--inverse" type="button">Nur notwendige</button></div></div>
```

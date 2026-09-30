# Dot

Gruppe: Marke

Dot: der Lime-Punkt, das Markenelement. Er steht fuer Aufmerksamkeit, Fokus und Ziel.

- `adb-dot`: grosser Punkt mit Puls und auslaufendem Ring (Hero, Ladeanimation). Einer pro Ansicht.
- `adb-dot--m`: 18px, `adb-dot--s`: 8px mit Ink-Ring, als Markierung vor Namen, Zahlen und Listenpunkten.
- Auf Paper braucht Lime immer den 1px-Ink-Ring (`adb-ring`), sonst verschwindet er.
- Respektiert `prefers-reduced-motion`.

```html
<div style="display:flex;gap:44px;align-items:center;padding:14px"><span class="adb-dot" aria-hidden="true"></span><span class="adb-dot adb-dot--m" aria-hidden="true"></span><span class="adb-dot adb-dot--s" aria-hidden="true"></span></div>
```

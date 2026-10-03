#!/bin/sh
# Ganze Build-Kette in der verbindlichen Reihenfolge. Aufruf: sh _build.sh [ziel-ordner-fuer-vorschau]
# Ohne Argument: baut nur im aktuellen Ordner. Mit Argument: danach rsync in den Vorschauordner.
# Erster Schritt _cases.py prueft die Inhaltsdateien _content/cases/*.json (Fehler nennen Datei und Feld).
# Ausgabe: je Schritt eine Zeile; Warnungen der Schritte (Zeilen mit "!" oder "?" am Anfang, "Hinweis", "fehlt",
# "ohne Posterbild") werden gesammelt und am Ende aufgelistet. STRICT=1 bricht bei Warnungen mit Fehler ab.
# Letzter Schritt _check.py: jede assets/-Referenz muss existieren und darf nicht von .vercelignore ausgeschlossen sein.
set -e
cd "$(dirname "$0")"
LOG=$(mktemp -t adbbuild); WARN=$(mktemp -t adbwarn)
trap 'rm -f "$LOG" "$WARN"' EXIT
for s in _cases.py _gen.py _gen_web.py _gen_services.py _gen_kontakt.py _apply_content.py _imgdim.py _poster.py \
         _css.py _brand_inplace.py _build_funkhaus_v3.py _build_performance_v3.py _footer.py _ui_markup.py _headlines.py _webp.py _perf.py _seo.py \
         _bump.py _check.py; do
  if ! python3 "$s" > "$LOG" 2>&1; then cat "$LOG"; echo "BUILD-FEHLER in $s"; exit 1; fi
  echo "  $s: $(tail -n 1 "$LOG" | cut -c1-140)"
  grep -E '^[[:space:]]*[!?]|Hinweis|fehlt|ohne Posterbild|fehlgeschlagen' "$LOG" | sed "s|^|$s: |" >> "$WARN" || true
done
if [ -s "$WARN" ]; then
  echo "Warnungen ($(wc -l < "$WARN" | tr -d ' ')):"; cat "$WARN"
  if [ "$STRICT" = "1" ]; then echo "STRICT=1: Abbruch wegen Warnungen"; exit 1; fi
else
  echo "Warnungen: keine"
fi
if [ -n "$1" ]; then rsync -a --delete --exclude .git --exclude .claude --exclude _intern ./ "$1"/; echo "Vorschau: $1"; fi

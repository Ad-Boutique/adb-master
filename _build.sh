#!/bin/sh
# Ganze Build-Kette in der verbindlichen Reihenfolge. Aufruf: sh _build.sh [ziel-ordner-fuer-vorschau]
# Ohne Argument: baut nur im aktuellen Ordner. Mit Argument: danach rsync in den Vorschauordner.
# Erst pruefen _cases.py und _leistungen.py die Inhaltsdateien _content/cases/*.json und _content/services/*.json
# (Fehler nennen Datei und Feld). _css.py buendelt CSS und JS vor den Generatoren, weil die Cache-Version (Regel
# "version") ein Hash dieser Dateien ist. Die Generatoren schreiben fertige Seiten: die Regeln des Nachlaufs laufen
# beim Erzeugen (_nachlauf.fertig). _nachlauf.py wendet dieselben Regeln in derselben Reihenfolge auf die
# handgebauten Seiten an und leitet die *-v3.html ab, dazu sitemap.xml, robots.txt, llms.txt.
# Ausgabe: je Schritt eine Zeile; Warnungen der Schritte (Zeilen mit "!" oder "?" am Anfang, "Hinweis", "fehlt",
# "ohne Posterbild") werden gesammelt und am Ende aufgelistet. STRICT=1 bricht bei Warnungen mit Fehler ab.
# Live-Fassung: ADB_LIVE=1 sh _build.sh (siehe _seo.py).
# Letzter Schritt _check.py: jede assets/-Referenz muss existieren und darf nicht von .vercelignore ausgeschlossen sein.
set -e
cd "$(dirname "$0")"
LOG=$(mktemp "${TMPDIR:-/tmp}/adbbuild.XXXXXX"); WARN=$(mktemp "${TMPDIR:-/tmp}/adbwarn.XXXXXX")  # Form fuer macOS und Linux
trap 'rm -f "$LOG" "$WARN"' EXIT
for s in _cases.py _leistungen.py _css.py _gen.py _gen_web.py _gen_services.py _gen_kontakt.py _gen_legal.py _nachlauf.py _check.py; do
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
if [ -n "$1" ]; then
  # rsync --delete loescht im Ziel: nur temporaere Vorschau-Ordner zulassen, damit ein Tippfehler nichts zerstoert
  case "$1" in
    /tmp/*|/private/tmp/*|"${TMPDIR%/}"/*) ;;
    *) echo "Vorschau-Ziel muss unter /tmp oder \$TMPDIR liegen: $1"; exit 1 ;;
  esac
  rsync -a --delete --exclude .git --exclude .claude --exclude _intern ./ "$1"/; echo "Vorschau: $1"
fi

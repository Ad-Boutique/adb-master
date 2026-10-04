#!/bin/sh
# Ganze Build-Kette in der verbindlichen Reihenfolge. Aufruf: sh _build.sh [ziel]
# Gebaut wird in einer temporaeren Kopie des Repos: das Repo selbst aendert sich beim Bauen nicht.
# Ins Ziel (Standard: public/ im Repo) kommen nur die auszuliefernden Dateien (_dist.py, Regeln in .distignore).
# Vercel baut mit demselben Befehl (vercel.json) und liefert public/ aus, ebenso die GitHub-Pages-Vorschau.
# Erst pruefen _cases.py und _leistungen.py die Inhaltsdateien _content/cases/*.json und _content/services/*.json
# (Fehler nennen Datei und Feld). _css.py buendelt CSS und JS vor den Generatoren, weil die Cache-Version (Regel
# "version") ein Hash dieser Dateien ist. Die Generatoren schreiben fertige Seiten: die Regeln des Nachlaufs laufen
# beim Erzeugen (_nachlauf.fertig). _nachlauf.py wendet dieselben Regeln in derselben Reihenfolge auf die
# handgebauten Seiten an und leitet die *-v3.html ab, dazu sitemap.xml, robots.txt, llms.txt.
# Ausgabe: je Schritt eine Zeile; Warnungen der Schritte (Zeilen mit "!" oder "?" am Anfang, "Hinweis", "fehlt",
# "ohne Posterbild") werden gesammelt und am Ende aufgelistet. STRICT=1 bricht bei Warnungen mit Fehler ab.
# Live-Fassung: ADB_LIVE=1 sh _build.sh (siehe _seo.py).
# _check.py: jede assets/-Referenz muss existieren und darf nicht von .distignore ausgeschlossen sein.
set -e
cd "$(dirname "$0")"
SRC=$(pwd)
OUT="${1:-public}"
case "$OUT" in /*) ;; *) OUT="$SRC/$OUT" ;; esac
# Das Ziel wird vor dem Kopieren geleert: nur public/ im Repo oder temporaere Ordner zulassen
case "$OUT" in
  "$SRC/public"|/tmp/*|/private/tmp/*|"${TMPDIR%/}"/*) ;;
  *) echo "Ziel muss public/ im Repo oder ein Ordner unter /tmp bzw. \$TMPDIR sein: $OUT"; exit 1 ;;
esac
TMP="${TMPDIR:-/tmp}"; TMP="${TMP%/}"
STAGE=$(mktemp -d "$TMP/adbstage.XXXXXX")
LOG=$(mktemp "$TMP/adbbuild.XXXXXX"); WARN=$(mktemp "$TMP/adbwarn.XXXXXX")  # Form fuer macOS und Linux
trap 'rm -rf "$STAGE" "$LOG" "$WARN"' EXIT
# Kopie ohne Git-Daten, Arbeitskopien und alte Ausgabe (tar statt rsync: gibt es auch im Vercel-Build)
tar --exclude=./.git --exclude=./.claude --exclude=./_intern --exclude=./public -cf - . | (cd "$STAGE" && tar -xf -)
cd "$STAGE"
export ADB_SRC="$SRC"   # _seo.py liest Aenderungsdaten aus dem Git des Repos
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
python3 _dist.py "$OUT"

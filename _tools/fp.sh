#!/bin/sh
# Stil-Fingerabdruecke aller Seiten (1440 und 390) nach $1 schreiben. Vorschauserver muss auf :8743 laufen und
# die Ausgabe von sh _build.sh ausliefern; die Seitenliste kommt aus public/ (erzeugte Seiten liegen nicht im Repo).
OUT="$1"; mkdir -p "$OUT"; cd "$(dirname "$0")/.."
for f in $(cd public && ls *.html | grep -v _qa_template | grep -v funkhausliving); do
  for W in 1440 390; do H=900; [ $W = 390 ] && H=844
    perl -e 'alarm 60; exec @ARGV' _tools/probe "http://localhost:8743/$f?coach=0&fp=$$" $W $H _tools/stylefp.js 4 > "$OUT/${f%.html}_$W.json" 2>/dev/null
  done
done
echo "fertig: $(ls "$OUT" | wc -l) Dateien"

#!/bin/sh
# Ganze Build-Kette in der verbindlichen Reihenfolge. Aufruf: sh _build.sh [ziel-ordner-fuer-vorschau]
# Ohne Argument: baut nur im aktuellen Ordner. Mit Argument: danach rsync in den Vorschauordner.
set -e
cd "$(dirname "$0")"
for s in _gen.py _gen_web.py _gen_services.py _gen_kontakt.py _apply_content.py _imgdim.py _poster.py \
         _brand_inplace.py _build_funkhaus_v3.py _build_performance_v3.py _footer.py _ui_markup.py _headlines.py _webp.py _seo.py; do
  python3 "$s" > /dev/null || { echo "BUILD-FEHLER in $s"; exit 1; }
done
python3 _bump.py
if [ -n "$1" ]; then rsync -a --delete --exclude .git --exclude _intern ./ "$1"/; echo "Vorschau: $1"; fi

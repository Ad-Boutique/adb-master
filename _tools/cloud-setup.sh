#!/bin/sh
# Setup-Skript fuer Claude-Cloud-Umgebungen (claude.ai/code): installiert, was Build und Pruefung brauchen.
# In den Umgebungseinstellungen als Setup-Skript eintragen: sh _tools/cloud-setup.sh
set -e
python3 -m pip install --quiet --upgrade pillow playwright
# Playwright ist in Claude-Cloud-Umgebungen meist vorinstalliert; sonst Browser nachladen
python3 -m playwright install chromium >/dev/null 2>&1 || python3 -m playwright install --with-deps chromium
# ffmpeg: nur fuer neue Videos (Posterbilder, faststart). Fehlt es, laeuft der Build trotzdem.
if ! command -v ffmpeg >/dev/null 2>&1; then
  (sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg) >/dev/null 2>&1 || echo "Hinweis: ffmpeg nicht installiert (nur fuer neue Videos noetig)"
fi
echo "Cloud-Setup fertig: $(python3 --version), Pillow $(python3 -c 'import PIL; print(PIL.__version__)')"

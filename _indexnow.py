# -*- coding: utf-8 -*-
"""IndexNow: meldet nach einem Deploy alle URLs aus sitemap.xml an Bing (und damit Copilot, Yahoo, DuckDuckGo).
Braucht die Umgebungsvariable INDEXNOW_KEY; die Schluesseldatei <key>.txt muss im Root liegen (einmalig anlegen).
Aufruf: INDEXNOW_KEY=... python3 _indexnow.py"""
import json
import os
import re
import sys
import urllib.request

key = os.environ.get("INDEXNOW_KEY")
if not key:
    print("INDEXNOW_KEY fehlt, nichts gemeldet")
    sys.exit(0)
if not os.path.exists(key + ".txt"):
    open(key + ".txt", "w").write(key)
sm = open("sitemap.xml", encoding="utf-8").read()
urls = re.findall(r"<loc>(.*?)</loc>", sm)
host = re.sub(r"^https?://", "", urls[0]).split("/")[0]
body = json.dumps({"host": host, "key": key, "keyLocation": "https://%s/%s.txt" % (host, key), "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/IndexNow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow:", r.status, len(urls), "URLs")

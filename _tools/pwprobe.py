# -*- coding: utf-8 -*-
"""Ersatz fuer die Mac-Programme probe und scrollshot (Swift), laeuft ueberall mit Playwright (Cloud, Linux).

  python3 _tools/pwprobe.py js   <url> <breite> <hoehe> <js-datei> [wartezeit]
      wertet das Skript aus und gibt das Ergebnis aus (wie _tools/probe, z. B. mit _tools/qa2.js)
  python3 _tools/pwprobe.py shot <url> <prefix> <breite> <hoehe> <y1> [y2 ...]
      Screenshots an Scrollpositionen nach <prefix>_<n>.jpg (wie _tools/scrollshot)

Umgebungsvariable PREJS: JavaScript, das vor den Screenshots laeuft (z. B. ein Banner schliessen).
Stand 03.10.2026: auf dem Mac nicht getestet (dort laufen die Swift-Programme); in der ersten Cloud-Sitzung pruefen."""
import os
import sys
import time

from playwright.sync_api import sync_playwright


def page_for(p, w, h):
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": int(w), "height": int(h)}, device_scale_factor=2)
    return browser, page


def run_js(url, w, h, js_file, wait="2.2"):
    js = open(js_file, encoding="utf-8").read()
    with sync_playwright() as p:
        browser, page = page_for(p, w, h)
        page.goto(url, wait_until="load", timeout=25000)
        time.sleep(float(wait))
        # Die Swift-Fassung wertet den letzten Ausdruck aus; Playwright braucht eine Funktion
        res = page.evaluate("() => eval(%r)" % js)
        print(res if isinstance(res, str) else repr(res))
        browser.close()


def shots(url, prefix, w, h, ys):
    with sync_playwright() as p:
        browser, page = page_for(p, w, h)
        page.goto(url, wait_until="load", timeout=25000)
        time.sleep(2.2)
        if os.environ.get("PREJS"):
            page.evaluate("() => { %s }" % os.environ["PREJS"])
            time.sleep(0.5)
        for i, y in enumerate(ys):
            page.evaluate("y => { window.scrollTo(0, y); window.dispatchEvent(new Event('scroll')); }", int(y))
            time.sleep(1.2)
            page.screenshot(path="%s_%d.jpg" % (prefix, i), type="jpeg", quality=80)
        browser.close()


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) >= 5 and a[0] == "js":
        run_js(*a[1:7])
    elif len(a) >= 6 and a[0] == "shot":
        shots(a[1], a[2], a[3], a[4], a[5:])
    else:
        print(__doc__)
        sys.exit(2)

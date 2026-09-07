(function () {
  var iss = [], W = document.documentElement.clientWidth;
  var secs = document.querySelectorAll("section").length;
  if (secs === 0) return "SEITE-LEER";
  if (document.documentElement.scrollWidth > W + 2) iss.push("OVERFLOW " + document.documentElement.scrollWidth + ">" + W);
  var broken = 0, flat = 0;
  document.querySelectorAll("img").forEach(function (im) {
    if (im.complete && im.naturalWidth === 0) broken++;
    var r = im.getBoundingClientRect(); if (r.width > 8 && r.height < 3) flat++; });
  if (broken) iss.push("BILD-FEHLT " + broken); if (flat) iss.push("BILD-FLACH " + flat);
  var empty = []; document.querySelectorAll("section").forEach(function (s, i) { if (s.getBoundingClientRect().height < 24) empty.push(i); });
  if (empty.length) iss.push("SEKTION-LEER " + empty.join(","));
  var wrong = []; document.querryAll && 0;
  document.querySelectorAll("h1,h2,.dispn,.phh,.cwh,.zah").forEach(function (el) {
    var cs = getComputedStyle(el); if (parseFloat(cs.fontSize) >= 30 && cs.fontFamily.indexOf("Satoshi") < 0) wrong.push(el.tagName + "/" + Math.round(parseFloat(cs.fontSize))); });
  if (wrong.length) iss.push("SERIF-HEADLINE " + wrong.slice(0, 3).join(" "));
  if (/case-/.test(location.pathname) && !document.querySelector(".bkbtn") && !document.querySelector('meta[http-equiv="refresh"]')) iss.push("ZURUECK-KREIS-FEHLT");
  var pt = document.querySelector(".pt"); if (pt && !pt.classList.contains("gone")) iss.push("OVERLAY-HAENGT");
  var mp = (document.body.innerText || "").split("·").length - 1; if (mp) iss.push("MITTELPUNKTE " + mp);
  var h = document.querySelector(".chero .hcap .dispn"); if (h && W > 720) { var lh = parseFloat(getComputedStyle(h).lineHeight); if (h.getBoundingClientRect().height > lh * 1.5) iss.push("HERO-ZEILE-UMBRUCH"); }
  return (iss.length ? iss.join(" ;; ") : "OK") + " [" + secs + " Sektionen]";
})();

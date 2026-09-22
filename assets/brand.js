/* ad.boutique Brand 2026, Test: der Punkt als Bewegung.
   Laden: Punkt erscheint, fokussiert, wandert in den Menue-Kreis.
   Verlassen: Menue-Kreis loest sich, wandert in die Mitte, die Blende faellt.
   Punkt-Graphen: jede Einheit ein Punkt, gefuellt beim Scrollen.
   Laeuft vor master.js und stellt ADB_ENTER / ADB_LEAVE bereit. */
(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var body = document.body;
  body.classList.add("brand");

  var dot = document.createElement("div");
  dot.className = "ptdot";
  dot.setAttribute("aria-hidden", "true");
  body.appendChild(dot);

  var SNAP = "cubic-bezier(0.76, 0, 0.24, 1)", OUT = "cubic-bezier(0.19, 1, 0.22, 1)";

  /* Wo sitzt der Menue-Kreis, relativ zur Bildschirmmitte, und wie gross ist er im Verhaeltnis zum Punkt */
  function target() {
    var b = document.querySelector(".mbtn");
    if (!b) return null;
    var r = b.getBoundingClientRect();
    return { x: r.left + r.width / 2 - window.innerWidth / 2, y: r.top + r.height / 2 - window.innerHeight / 2, s: r.width / 18 };
  }
  function at(t) { return "translate(" + t.x.toFixed(1) + "px," + t.y.toFixed(1) + "px) scale(" + t.s.toFixed(2) + ")"; }
  /* Protokoll der Choreografie, damit sie sich ohne Zuschauer pruefen laesst */
  var t0 = Date.now();
  window.__brandLog = [];
  function log(step) { window.__brandLog.push((Date.now() - t0) + "ms " + step); }

  window.ADB_ENTER = function (pt, done) {
    if (reduced) { pt.classList.add("gone"); body.classList.add("mready"); done(); return; }
    /* Punkt */
    dot.style.transition = "transform 0.45s " + OUT + ", opacity 0.3s ease";
    requestAnimationFrame(function () { dot.style.opacity = "1"; dot.style.transform = "scale(1)"; log("Punkt erscheint"); });
    /* Fokus: kurzer Atemzug, zwei Ringe */
    setTimeout(function () { dot.classList.add("pulse"); dot.style.transform = "scale(1.3)"; log("Fokus, Ringe"); }, 420);
    setTimeout(function () { dot.style.transform = "scale(1)"; }, 720);
    /* Ziel: die Seite kommt, der Punkt wandert in den Menue-Kreis */
    setTimeout(function () {
      done();
      pt.classList.add("gone");
      var t = target();
      if (t) { dot.style.transition = "transform 0.85s " + SNAP; dot.style.transform = at(t); log("wandert zum Menue " + at(t)); }
      setTimeout(function () {
        body.classList.add("mready");
        log("Menue-Kreis uebernimmt");
        dot.classList.remove("pulse");
        dot.style.transition = "opacity 0.25s ease";
        dot.style.opacity = "0";
        setTimeout(function () { dot.style.transition = "none"; dot.style.transform = "scale(0)"; }, 300);
      }, 880);
    }, 1050);
  };

  window.ADB_LEAVE = function (pt, href) {
    var t = target();
    body.classList.remove("mready");
    dot.classList.remove("pulse");
    dot.style.transition = "none";
    dot.style.opacity = "1";
    dot.style.transform = t ? at(t) : "scale(1)";
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        dot.style.transition = "transform 0.55s " + SNAP;
        dot.style.transform = "scale(1)";
        setTimeout(function () {
          dot.classList.add("pulse");
          pt.classList.remove("gone");
          pt.classList.add("enter");
          requestAnimationFrame(function () { pt.classList.add("cover"); });
        }, 480);
        setTimeout(function () { location.href = href; }, 1000);
        /* Netz: ist die Seite nach vier Sekunden noch da, geht alles wieder auf */
        setTimeout(function () {
          pt.classList.remove("cover", "enter"); pt.classList.add("gone");
          body.classList.add("mready"); dot.style.opacity = "0";
        }, 4500);
      });
    });
  };

  /* ---------- Punkt-Graphen ---------- */
  function build() {
    document.querySelectorAll(".dotgraph[data-total]").forEach(function (g) {
      if (g.children.length) return;
      var n = parseInt(g.getAttribute("data-total"), 10) || 100;
      var frag = document.createDocumentFragment();
      for (var i = 0; i < n; i++) frag.appendChild(document.createElement("i"));
      g.appendChild(frag);
    });
    document.querySelectorAll(".dotbars .dots[data-n]").forEach(function (d) {
      if (d.children.length) return;
      var n = parseInt(d.getAttribute("data-n"), 10) || 10;
      var frag = document.createDocumentFragment();
      for (var i = 0; i < n; i++) frag.appendChild(document.createElement("i"));
      d.appendChild(frag);
    });
  }
  function fill(el, count, step) {
    var dots = el.querySelectorAll("i");
    for (var i = 0; i < dots.length; i++) {
      (function (d, k) {
        if (k < count) setTimeout(function () { d.classList.add("on"); }, reduced ? 0 : k * step);
      })(dots[i], i);
    }
  }
  function arm() {
    var items = Array.prototype.slice.call(document.querySelectorAll(".dotgraph[data-value], .dotbars .dots[data-on]"));
    if (!items.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var count = parseInt(el.getAttribute("data-value") || el.getAttribute("data-on"), 10) || 0;
        fill(el, count, el.classList.contains("dotgraph") ? 22 : 40);
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -18% 0px" });
    items.forEach(function (el) { io.observe(el); });
  }
  build();
  arm();
})();

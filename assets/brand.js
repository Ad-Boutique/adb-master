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

  /* ---------- Favicon: Ring waehrend des Ladens, danach der Punkt ---------- */
  var ico = document.querySelector('link[rel="icon"]');
  function icon(kind) {
    var inner = kind === "ring"
      ? '<circle cx="32" cy="32" r="12" fill="none" stroke="#d7ff45" stroke-width="5"/>'
      : '<circle cx="32" cy="32" r="13" fill="#d7ff45"/><circle cx="32" cy="32" r="5" fill="#0f0f0f"/>';
    return "data:image/svg+xml," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0f0f0f"/>' + inner + '</svg>');
  }
  if (ico) {
    ico.setAttribute("href", icon("ring"));
    var icoWait = setInterval(function () { if (body.classList.contains("mready")) { ico.setAttribute("href", icon("dot")); clearInterval(icoWait); } }, 200);
  }

  /* ---------- Der Weiter-Knopf ist der Punkt am Ende: beim Druecken laufen die Ziel-Ringe ---------- */
  document.addEventListener("pointerdown", function (e) {
    var go = e.target.closest(".ngo");
    if (!go) return;
    go.classList.remove("fired");
    requestAnimationFrame(function () { go.classList.add("fired"); });
    setTimeout(function () { go.classList.remove("fired"); }, 800);
  });

  /* ---------- Punktfeld: echte Einheiten als Punkte. Beim Laden sammeln sie sich ins Raster,
       der Lime-Anteil steht in Leserichtung, am Desktop ziehen sie sich zum Cursor. ---------- */
  Array.prototype.slice.call(document.querySelectorAll("canvas.dotfield")).forEach(function (cv) {
    var total = parseInt(cv.getAttribute("data-total"), 10) || 100;
    var lime = parseInt(cv.getAttribute("data-lime"), 10) || 0;
    var ctx = cv.getContext("2d"), dots = [], W = 0, H = 0, dpr = Math.min(2, window.devicePixelRatio || 1);
    var mx = -9999, my = -9999, start = 0, seen = false, running = false, fine = window.matchMedia("(pointer: fine)").matches;
    function layout() {
      var r = cv.getBoundingClientRect(); W = r.width; H = r.height;
      if (!W || !H) return;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var cols = Math.max(4, Math.ceil(Math.sqrt(total * W / H))), rows = Math.ceil(total / cols);
      var gx = W / cols, gy = H / rows, rad = Math.max(2.4, Math.min(gx, gy) * 0.22);
      dots = [];
      for (var i = 0; i < total; i++) {
        var c = i % cols, rw = Math.floor(i / cols);
        dots.push({ x: gx * (c + 0.5), y: gy * (rw + 0.5), sx: W / 2 + (Math.random() - 0.5) * W * 1.8, sy: H / 2 + (Math.random() - 0.5) * H * 1.8, r: rad, lime: i < lime, d: Math.random() * 0.4 });
      }
    }
    function ease(t) { return 1 - Math.pow(1 - t, 3); }
    function frame(now) {
      if (!running) return;
      if (!start) start = now;
      var t = (now - start) / 1000;
      ctx.clearRect(0, 0, W, H);
      var settled = true;
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var p = reduced ? 1 : Math.max(0, Math.min(1, (t - d.d) / 1.1));
        if (p < 1) settled = false;
        var e = ease(p), x = d.sx + (d.x - d.sx) * e, y = d.sy + (d.y - d.sy) * e, r = d.r;
        if (fine && p >= 1) {
          var dx = mx - x, dy = my - y, dist = Math.sqrt(dx * dx + dy * dy), R = 150;
          if (dist < R) { var f = 1 - dist / R; x += dx / (dist || 1) * f * 12; y += dy / (dist || 1) * f * 12; r = d.r * (1 + f * 0.9); }
        }
        ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
        if (d.lime) { ctx.fillStyle = "#d7ff45"; ctx.fill(); ctx.lineWidth = 1; ctx.strokeStyle = "rgba(15,15,15,0.6)"; ctx.stroke(); }
        else { ctx.fillStyle = "rgba(15,15,15,0.16)"; ctx.fill(); }
      }
      /* nach dem Sammeln nur weiterzeichnen, wenn ein Cursor da ist, den es zu folgen gilt */
      if (!settled || (fine && mx > -9000)) requestAnimationFrame(frame); else running = false;
    }
    function wake() { if (!running) { running = true; requestAnimationFrame(frame); } }
    if (fine) {
      cv.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; wake(); });
      cv.addEventListener("pointerleave", function () { mx = -9999; my = -9999; wake(); });
    }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting && !seen) { seen = true; layout(); wake(); } });
    }, { rootMargin: "0px 0px -10% 0px" });
    io.observe(cv);
    window.addEventListener("resize", function () { if (seen) { layout(); start = 0; wake(); } });
  });

  /* ---------- Stationen: Punktzeile unter der grossen Zahl folgt der aktiven Station ---------- */
  var tellBoxes = Array.prototype.slice.call(document.querySelectorAll(".tell")).map(function (box) {
    var fix = box.querySelector(".tfix"), steps = box.querySelectorAll(".ts");
    if (!fix || !steps.length) return null;
    var row = document.createElement("div"); row.className = "tdots";
    for (var i = 0; i < steps.length; i++) row.appendChild(document.createElement("i"));
    fix.appendChild(row);
    return { steps: steps, dots: row.children, cur: -1 };
  }).filter(Boolean);

  /* ---------- Scroll-Fortschritt als Punkt auf gepunkteter Bahn ---------- */
  var prog = document.createElement("div"); prog.className = "sprog"; prog.setAttribute("aria-hidden", "true");
  var pdot = document.createElement("i"); prog.appendChild(pdot); body.appendChild(prog);

  /* ---------- Cursor-Zustaende: Fokus ueber Bildern, Target beim Klick (Expand ueber Links setzt master.js als cur-hov) ---------- */
  if (window.matchMedia("(pointer: fine)").matches) {
    document.addEventListener("pointerover", function (e) {
      body.classList.toggle("cur-media", !!e.target.closest("img, video, .phframe, .hlxmedia, .zmedia, .stage"));
    });
    document.addEventListener("pointerdown", function () {
      body.classList.remove("cur-tap");
      requestAnimationFrame(function () { body.classList.add("cur-tap"); });
      setTimeout(function () { body.classList.remove("cur-tap"); }, 600);
    });
  }

  /* ---------- Punkt-Zoom: Sektion oeffnet sich aus einem Punkt, gesteuert vom Scroll ---------- */
  var zooms = Array.prototype.slice.call(document.querySelectorAll(".dotzoom")).map(function (s) { return { el: s, p: -1 }; });
  function zoomTick() {
    zooms.forEach(function (z) {
      var r = z.el.getBoundingClientRect();
      var p = reduced ? 1 : Math.max(0, Math.min(1, (window.innerHeight * 0.95 - r.top) / (window.innerHeight * 0.62)));
      if (Math.abs(p - z.p) < 0.003) return;
      z.p = p;
      /* erst waechst der Punkt (0 bis 0,2), dann oeffnet sich aus ihm das Loch und der Punkt zieht sich zurueck */
      var zd = p < 0.2 ? p / 0.2 : Math.max(0, 1 - (p - 0.2) / 0.22);
      var zr = p < 0.2 ? 0 : (p - 0.2) / 0.8 * Math.hypot(r.width, r.height) * 0.62;
      z.el.style.setProperty("--zd", zd.toFixed(3));
      z.el.style.setProperty("--zr", zr.toFixed(0) + "px");
      z.el.classList.toggle("zdone", p >= 1);
    });
  }

  function brandTick() {
    zoomTick();
    tellBoxes.forEach(function (t) {
      var idx = -1;
      for (var i = 0; i < t.steps.length; i++) if (t.steps[i].classList.contains("on")) { idx = i; break; }
      if (idx === t.cur) return;
      t.cur = idx;
      for (var k = 0; k < t.dots.length; k++) t.dots[k].classList.toggle("on", k === idx);
    });
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.max(0, Math.min(1, window.pageYOffset / max)) : 0;
    pdot.style.transform = "translateY(" + (p * (prog.offsetHeight - 12)).toFixed(1) + "px)";
    requestAnimationFrame(brandTick);
  }
  requestAnimationFrame(brandTick);
})();

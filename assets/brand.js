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

  /* Alte Palette auf die neue mappen, bevor master.js die Hintergruende liest.
     Case-Farbwelten (Gruen, Slate usw.) bleiben, nur Papier, Creme und Schwarz wandern. */
  var BG = { "#F3EDE1": "#f4f3ec", "#EFE7D6": "#e9e8df", "#0A0A0A": "#0f0f0f", "#0E0E10": "#0f0f0f", "#070708": "#0f0f0f", "#08080A": "#0f0f0f", "#060607": "#0f0f0f" };
  var RGB = { "rgb(243, 237, 225)": "#f4f3ec", "rgb(239, 231, 214)": "#e9e8df", "rgb(10, 10, 10)": "#0f0f0f", "rgb(14, 14, 16)": "#0f0f0f", "rgb(7, 7, 8)": "#0f0f0f", "rgb(8, 8, 10)": "#0f0f0f" };
  Array.prototype.forEach.call(document.querySelectorAll("[data-bg]"), function (el) {
    var v = (el.getAttribute("data-bg") || "").toUpperCase();
    if (BG[v]) el.setAttribute("data-bg", BG[v]);
    var inl = el.style.backgroundColor;
    if (inl && RGB[inl]) el.style.backgroundColor = RGB[inl];
  });
  if (RGB[body.style.backgroundColor]) body.style.backgroundColor = RGB[body.style.backgroundColor];

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

  /* Beim Verlassen: eine Wolke aus Punkten sammelt sich zur Mitte, wo der Punkt wartet */
  function cloud() {
    if (reduced) return;
    var cv = document.createElement("canvas");
    cv.style.cssText = "position:fixed;inset:0;width:100%;height:100%;z-index:205;pointer-events:none";
    var dpr = Math.min(2, window.devicePixelRatio || 1), W = window.innerWidth, H = window.innerHeight;
    cv.width = W * dpr; cv.height = H * dpr; body.appendChild(cv);
    var c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0);
    var ps = [];
    for (var i = 0; i < 140; i++) {
      var ang = Math.random() * Math.PI * 2, rad = Math.max(W, H) * (0.35 + Math.random() * 0.6);
      ps.push({ x: W / 2 + Math.cos(ang) * rad, y: H / 2 + Math.sin(ang) * rad, r: 2 + Math.random() * 3.5, d: Math.random() * 0.25 });
    }
    var t0 = performance.now();
    (function draw(now) {
      var t = (now - t0) / 1000; c.clearRect(0, 0, W, H);
      var alive = false;
      ps.forEach(function (p) {
        var q = Math.max(0, Math.min(1, (t - p.d) / 0.6)); if (q < 1) alive = true;
        var e = q * q * (3 - 2 * q), x = p.x + (W / 2 - p.x) * e, y = p.y + (H / 2 - p.y) * e;
        c.beginPath(); c.arc(x, y, p.r * (1 - e * 0.6), 0, Math.PI * 2);
        c.fillStyle = "#d7ff45"; c.fill(); c.lineWidth = 1; c.strokeStyle = "rgba(15,15,15,0.7)"; c.stroke();
      });
      if (alive) requestAnimationFrame(draw); else setTimeout(function () { cv.remove(); }, 200);
    })(t0);
  }

  window.ADB_LEAVE = function (pt, href) {
    var t = target();
    body.classList.remove("mready");
    cloud();
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
    /* Antippen: die Lime-Punkte sammeln sich zur Zahl (data-form), zweites Antippen loest sie wieder */
    var formText = cv.getAttribute("data-form"), formed = false, form = 0, formT = 0;
    function targets() {
      if (!formText || !W) return;
      var oc = document.createElement("canvas"); oc.width = Math.round(W); oc.height = Math.round(H);
      var o = oc.getContext("2d");
      o.font = "400 " + Math.round(H * 0.92) + 'px "amandine", Georgia, serif';
      o.textAlign = "center"; o.textBaseline = "middle"; o.fillStyle = "#000";
      o.fillText(formText, W / 2, H / 2 + H * 0.04);
      var img = o.getImageData(0, 0, oc.width, oc.height).data, pts = [];
      for (var y = 0; y < oc.height; y += 3) for (var x = 0; x < oc.width; x += 3) if (img[(y * oc.width + x) * 4 + 3] > 128) pts.push([x, y]);
      var limeDots = dots.filter(function (d) { return d.lime; });
      if (!pts.length) return;
      pts.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
      for (var i = 0; i < limeDots.length; i++) { var k = Math.floor(i / limeDots.length * pts.length); limeDots[i].tx = pts[k][0]; limeDots[i].ty = pts[k][1]; }
    }
    if (formText) cv.addEventListener("click", function () { formed = !formed; formT = performance.now(); wake(); });
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
    /* Am Telefon gibt es keinen Cursor: dort sammeln sich die Punkte mit dem Scroll (vor und zurueck)
       und die Lime-Punkte atmen in einer langsamen Welle, solange das Feld im Bild ist */
    var coarse = !fine || /coarse/.test(location.search), inView = false;  /* ?coarse erzwingt den Telefon-Pfad fuer Pruefungen */
    function scrollP() {
      var r = cv.getBoundingClientRect(), vh = window.innerHeight;
      return Math.max(0, Math.min(1, (vh * 0.95 - r.top) / (vh * 0.55)));
    }
    function frame(now) {
      if (!running) return;
      if (!start) start = now;
      var t = (now - start) / 1000, sp = coarse ? scrollP() : 1;
      ctx.clearRect(0, 0, W, H);
      var settled = true;
      /* Formfortschritt: hin zur Zahl oder zurueck ins Raster, je 0,8 s */
      var target = formed ? 1 : 0, fdt = Math.min(1, (now - formT) / 800);
      var formNow = formed ? fdt : 1 - fdt;
      if (Math.abs(formNow - target) > 0.001) settled = false;
      form = formNow;
      var ef = ease(form);
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var p = reduced ? 1 : (coarse ? Math.max(0, Math.min(1, (sp * 1.4 - d.d) / 0.6)) : Math.max(0, Math.min(1, (t - d.d) / 1.1)));
        if (p < 1) settled = false;
        var e = ease(p), x = d.sx + (d.x - d.sx) * e, y = d.sy + (d.y - d.sy) * e, r = d.r;
        if (coarse && d.lime && p >= 1 && form === 0 && !reduced) { r = d.r * (1 + 0.32 * Math.sin(t * 1.6 + (d.x + d.y) / 55)); settled = false; }
        if (d.lime && d.tx != null && form > 0) { x += (d.tx - x) * ef; y += (d.ty - y) * ef; r = d.r * (1 + ef * 0.25); }
        if (fine && p >= 1 && form === 0) {
          var dx = mx - x, dy = my - y, dist = Math.sqrt(dx * dx + dy * dy), R = 150;
          if (dist < R) { var f = 1 - dist / R; x += dx / (dist || 1) * f * 12; y += dy / (dist || 1) * f * 12; r = d.r * (1 + f * 0.9); }
        }
        ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
        if (d.lime) { ctx.fillStyle = "#d7ff45"; ctx.fill(); ctx.lineWidth = 1; ctx.strokeStyle = "rgba(15,15,15,0.6)"; ctx.stroke(); }
        else { ctx.fillStyle = "rgba(15,15,15," + (0.16 * (1 - ef * 0.7)).toFixed(3) + ")"; ctx.fill(); }
      }
      /* nach dem Sammeln nur weiterzeichnen, wenn ein Cursor da ist oder das Feld am Telefon im Bild atmet */
      if ((!settled && (fine || inView)) || (fine && mx > -9000 && form === 0)) requestAnimationFrame(frame); else running = false;
    }
    function wake() { if (!running) { running = true; requestAnimationFrame(frame); } }
    if (fine) {
      cv.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; wake(); });
      cv.addEventListener("pointerleave", function () { mx = -9999; my = -9999; wake(); });
    }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        inView = x.isIntersecting;
        if (x.isIntersecting && !seen) { seen = true; layout(); targets(); }
        if (x.isIntersecting) wake();
      });
    }, { rootMargin: "0px 0px -10% 0px" });
    io.observe(cv);
    if (coarse) window.addEventListener("scroll", function () { if (inView) wake(); }, { passive: true });
    window.addEventListener("resize", function () { if (seen) { layout(); targets(); start = 0; wake(); } });
  });

  /* ---------- Budget-Regler: jeder Punkt eine Anfrage, gerechnet mit einem echten Preis je Anfrage ---------- */
  Array.prototype.slice.call(document.querySelectorAll(".rate")).forEach(function (box) {
    var cpl = parseFloat(box.getAttribute("data-cpl")) || 10, slider = box.querySelector(".rateslider"), grid = box.querySelector(".ratedots");
    var vEl = box.querySelector(".ratev"), nEl = box.querySelector(".raten");
    if (!slider || !grid) return;
    var maxN = Math.round(parseFloat(slider.max) / cpl);
    var frag = document.createDocumentFragment();
    for (var i = 0; i < maxN; i++) frag.appendChild(document.createElement("i"));
    grid.appendChild(frag);
    var cells = grid.children, cur = -1;
    function euro(v) { return "€ " + Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
    function render() {
      var v = parseFloat(slider.value), n = Math.round(v / cpl);
      vEl.textContent = euro(v);
      nEl.innerHTML = "<b>" + n + "</b>Anfragen";
      if (n === cur) return;
      cur = n;
      for (var k = 0; k < cells.length; k++) cells[k].classList.toggle("on", k < n);
    }
    slider.addEventListener("input", render);
    var io2 = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { render(); io2.unobserve(box); } }); }, { rootMargin: "0px 0px -15% 0px" });
    io2.observe(box);
  });

  /* ---------- Zeitleiste: 42 Tage als Punkte, gefuellt beim Ankommen ---------- */
  Array.prototype.slice.call(document.querySelectorAll(".tline .tldots")).forEach(function (row) {
    /* Segmente aus data-seg, z. B. "h1 b9 g4 t28": Klasse und Anzahl je Abschnitt */
    var seg = (row.getAttribute("data-seg") || "h1 b9 g4 t28").split(/\s+/);
    var frag = document.createDocumentFragment();
    seg.forEach(function (s) {
      var cls = s.charAt(0), n = parseInt(s.slice(1), 10) || 0;
      for (var i = 0; i < n; i++) { var d = document.createElement("i"); d.className = cls; frag.appendChild(d); }
    });
    row.appendChild(frag);
    var io3 = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (!x.isIntersecting) return;
        Array.prototype.forEach.call(row.children, function (d, k) { setTimeout(function () { d.classList.add("on"); }, reduced ? 0 : k * 45); });
        io3.unobserve(row);
      });
    }, { rootMargin: "0px 0px -15% 0px" });
    io3.observe(row);
  });

  /* ---------- Fit als Punktetest: Aussagen antippen, ein Satz antwortet ---------- */
  Array.prototype.slice.call(document.querySelectorAll(".fcard--yes")).forEach(function (card) {
    var items = Array.prototype.slice.call(card.querySelectorAll("li"));
    if (!items.length) return;
    var res = document.createElement("div"); res.className = "fitres";
    var dotsHtml = ""; for (var i = 0; i < items.length; i++) dotsHtml += "<i></i>";
    res.innerHTML = '<span class="frdots">' + dotsHtml + '</span><span class="frtxt">Tippen Sie an, was auf Sie zutrifft.</span>';
    card.appendChild(res);
    var frd = res.querySelectorAll(".frdots i"), txt = res.querySelector(".frtxt");
    function update() {
      var n = items.filter(function (li) { return li.classList.contains("hit"); }).length, all = items.length;
      for (var k = 0; k < frd.length; k++) frd[k].classList.toggle("on", k < n);
      if (n === 0) txt.innerHTML = "Tippen Sie an, was auf Sie zutrifft.";
      else if (n === all) txt.innerHTML = "<b>" + n + " von " + all + ".</b> Wir sollten sprechen.";
      else if (n >= all / 2) txt.innerHTML = "<b>" + n + " von " + all + ".</b> Das sieht nach einem Fit aus, der Rest klärt sich im Gespräch.";
      else txt.innerHTML = "<b>" + n + " von " + all + ".</b> Noch wenig Überschneidung. Ein Gespräch kostet trotzdem nichts.";
    }
    items.forEach(function (li) { li.addEventListener("click", function () { li.classList.toggle("hit"); update(); }); });
  });

  /* ---------- KPI-Sprung: Zahl zaehlt von vorher nach nachher, Linie zeichnet sich, Punkte springen ---------- */
  function fmt(v, dec) {
    var s = v.toFixed(dec).replace(".", ",");
    if (dec === 0) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return s;
  }
  Array.prototype.slice.call(document.querySelectorAll(".kpi")).forEach(function (k) {
    var to = k.querySelector(".kto"), line = k.querySelector(".kline");
    /* Linie aus data-points: Werte auf die Hoehe skaliert, Flaeche in Lime, letzter Punkt Lime */
    if (line) {
      var pts = (line.getAttribute("data-points") || "").split(",").map(parseFloat).filter(function (x) { return !isNaN(x); });
      if (pts.length > 1) {
        var W = 260, H = 90, pad = 10, mn = Math.min.apply(null, pts), mx = Math.max.apply(null, pts);
        var xs = pts.map(function (v, i) { return pad + i * (W - 2 * pad) / (pts.length - 1); });
        var ys = pts.map(function (v) { return pad + (mx - v) / ((mx - mn) || 1) * (H - 2 * pad - 14) + 6; });
        var d = xs.map(function (x, i) { return (i ? "L" : "M") + x.toFixed(1) + "," + ys[i].toFixed(1); }).join(" ");
        var area = d + " L" + xs[xs.length - 1].toFixed(1) + "," + (H - 2) + " L" + xs[0].toFixed(1) + "," + (H - 2) + " Z";
        var html = '<path class="kfill" d="' + area + '"/><path class="kpath" d="' + d + '"/>';
        xs.forEach(function (x, i) { html += '<circle class="kd' + (i === xs.length - 1 ? " end" : "") + '" cx="' + x.toFixed(1) + '" cy="' + ys[i].toFixed(1) + '" r="4.2"/>'; });
        html += '<text class="kv" x="' + xs[0].toFixed(1) + '" y="' + (ys[0] - 10).toFixed(1) + '" text-anchor="start">' + fmt(pts[0], 2) + '</text>';
        html += '<text class="kv" x="' + xs[xs.length - 1].toFixed(1) + '" y="' + (ys[ys.length - 1] + 18).toFixed(1) + '" text-anchor="end">' + fmt(pts[pts.length - 1], 2) + '</text>';
        line.innerHTML = html;
        var path = line.querySelector(".kpath"), L = path.getTotalLength();
        path.style.strokeDasharray = L + " " + L; path.style.strokeDashoffset = L;
        path.style.transition = "stroke-dashoffset 1.4s cubic-bezier(0.19, 1, 0.22, 1)";
        line.querySelectorAll(".kd").forEach(function (c, i) { c.style.transitionDelay = (0.25 + i * 0.16) + "s"; });
      }
    }
    var kd = k.querySelectorAll(".kdots .dots");
    kd.forEach(function (dts) { var n = parseInt(dts.getAttribute("data-n"), 10) || 0; for (var i = 0; i < n; i++) dts.appendChild(document.createElement("i")); });
    var ioK = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (!x.isIntersecting) return;
        ioK.unobserve(k);
        k.classList.add("lit");
        if (line) { var pth = line.querySelector(".kpath"); if (pth) pth.style.strokeDashoffset = 0; }
        kd.forEach(function (dts) { var on = parseInt(dts.getAttribute("data-on"), 10) || 0; Array.prototype.forEach.call(dts.children, function (d, i) { if (i < on) setTimeout(function () { d.classList.add("on"); }, reduced ? 0 : 200 + i * 30); }); });
        if (to && !reduced) {
          var from = parseFloat(to.getAttribute("data-from")), end = parseFloat(to.getAttribute("data-to"));
          var dec = parseInt(to.getAttribute("data-decimals"), 10) || 0, pre = to.getAttribute("data-prefix") || "", suf = to.getAttribute("data-suffix") || "";
          var t0 = performance.now();
          (function step(now) {
            var q = Math.min(1, (now - t0) / 1100), e = 1 - Math.pow(1 - q, 3);
            to.textContent = pre + fmt(from + (end - from) * e, dec) + suf;
            if (q < 1) requestAnimationFrame(step);
          })(t0);
        }
      });
    }, { rootMargin: "0px 0px -15% 0px" });
    ioK.observe(k);
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
  /* Kapitel-Marken auf der Bahn: die Ziele der Kapitel-Leiste, gelesen werden sie Lime */
  var marks = Array.prototype.slice.call(document.querySelectorAll(".chapnav a[href^='#']:not(.cn-cta)")).map(function (a) {
    var t = document.getElementById(a.getAttribute("href").slice(1));
    if (!t) return null;
    var b = document.createElement("b"); prog.appendChild(b);
    return { t: t, el: b, f: 0 };
  }).filter(Boolean);
  function placeMarks() {
    var max = document.documentElement.scrollHeight - window.innerHeight, h = prog.offsetHeight - 12;
    marks.forEach(function (m) {
      m.f = max > 0 ? Math.max(0, Math.min(1, (m.t.getBoundingClientRect().top + window.pageYOffset - window.innerHeight * 0.45) / max)) : 0;
      m.el.style.top = (m.f * h + 3).toFixed(1) + "px";
    });
  }
  setTimeout(placeMarks, 800);
  window.addEventListener("resize", placeMarks);

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

  /* ---------- Lime ist Licht: im Bildband bekommt das Bild in der Mitte seine Farbe zurueck.
       Am Desktop uebernimmt das der Hover, am Telefon wandert der Spot mit dem Band. ---------- */
  var bandImgs = Array.prototype.slice.call(document.querySelectorAll(".svcband img"));
  var bandLit = null, bandSec = document.querySelector(".svcband");
  function spotTick() {
    if (!bandImgs.length || !bandSec) return;
    var sr = bandSec.getBoundingClientRect();
    if (sr.bottom < 0 || sr.top > window.innerHeight) return;
    var cx = window.innerWidth / 2, best = null, bd = Infinity;
    for (var i = 0; i < bandImgs.length; i++) {
      var r = bandImgs[i].getBoundingClientRect();
      var d = Math.abs(r.left + r.width / 2 - cx);
      if (d < bd) { bd = d; best = bandImgs[i]; }
    }
    if (best !== bandLit) { if (bandLit) bandLit.classList.remove("lit"); if (best) best.classList.add("lit"); bandLit = best; }
  }

  /* ---------- Punktzeile im Hero: die Punkte fuellen sich nacheinander, sobald die Zeile im Bild ist ---------- */
  Array.prototype.slice.call(document.querySelectorAll(".dotline")).forEach(function (line) {
    var ioL = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (!x.isIntersecting) return;
        Array.prototype.forEach.call(line.children, function (sp, k) { setTimeout(function () { sp.classList.add("on"); }, reduced ? 0 : 300 + k * 220); });
        ioL.unobserve(line);
      });
    });
    ioL.observe(line);
  });

  function brandTick() {
    zoomTick();
    spotTick();
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
    marks.forEach(function (m) { m.el.classList.toggle("on", p >= m.f); });
    requestAnimationFrame(brandTick);
  }
  requestAnimationFrame(brandTick);
})();

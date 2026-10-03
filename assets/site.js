/* site.js: erzeugt von _css.py aus brand.js, master.js. Nicht bearbeiten, Quellen in assets/ aendern. */
/* ---------- brand.js ---------- */
;{
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

  /* Hintergruende: _ui_markup.py setzt data-bg schon auf die Tokens (Cream #F4F3EB, Black #101010), keine Umrechnung mehr im JS. */

  var dot = document.createElement("div");
  dot.className = "ptdot";
  dot.setAttribute("aria-hidden", "true");
  body.appendChild(dot);

  /* Eine Bewegungssprache: Kurve und Dauern kommen aus tokens.css (--e-out, --d-fast/base/slow/chor, --stagger).
     window.ADB_MOTION gibt sie an master.js weiter; eOut ist dieselbe Kurve fuer Bewegungen im Frame-Loop. */
  var M = (function () {
    var cs = getComputedStyle(document.documentElement);
    function ms(name, fb) { var v = (cs.getPropertyValue(name) || "").trim(), n = parseFloat(v); if (isNaN(n)) return fb; return /ms$/.test(v) ? n : (/s$/.test(v) ? n * 1000 : n); }
    var d = { fast: ms("--d-fast", 200), base: ms("--d-base", 400), slow: ms("--d-slow", 700), chor: ms("--d-chor", 1200), stagger: ms("--stagger", 80) };
    /* cubic-bezier(.16,1,.3,1) als Funktion: x(t) per Newton loesen, dann y(t) */
    var X1 = 0.16, Y1 = 1, X2 = 0.3, Y2 = 1;
    function bz(t, a, b) { return 3 * a * t * (1 - t) * (1 - t) + 3 * b * t * t * (1 - t) + t * t * t; }
    function dbz(t, a, b) { return 3 * a * (1 - t) * (1 - t) + 6 * (b - a) * t * (1 - t) + 3 * (1 - b) * t * t; }
    d.eOut = function (x) {
      if (x <= 0) return 0; if (x >= 1) return 1;
      var t = x;
      for (var i = 0; i < 8; i++) { var dx = bz(t, X1, X2) - x, der = dbz(t, X1, X2); if (Math.abs(dx) < 1e-5 || !der) break; t -= dx / der; }
      return bz(Math.max(0, Math.min(1, t)), Y1, Y2);
    };
    d.ease = "cubic-bezier(0.16, 1, 0.3, 1)";
    d.t = function (prop, dur) { return prop + " var(" + dur + ") var(--e-out)"; };
    return d;
  })();
  window.ADB_MOTION = M;

  /* Wo sitzt der Menue-Kreis, relativ zur Bildschirmmitte, und wie gross ist er im Verhaeltnis zum Punkt */
  function target() {
    var b = document.querySelector(".mbtn");
    if (!b) return null;
    var r = b.getBoundingClientRect();
    /* Groesse gemessen, nicht angenommen: Menue-Kreis (brand-ui.css --mbtn-size) geteilt durch den Punkt */
    return { x: r.left + r.width / 2 - window.innerWidth / 2, y: r.top + r.height / 2 - window.innerHeight / 2, s: r.width / (dot.offsetWidth || 18) };
  }
  function at(t) { return "translate(" + t.x.toFixed(1) + "px," + t.y.toFixed(1) + "px) scale(" + t.s.toFixed(2) + ")"; }
  /* Farbe des Menue-Kreises (brand-ui.css: Lime auf hellem Grund, Cream auf dunklem und auf Fotos), damit der Punkt nahtlos in ihm aufgeht */
  function mcolor() { var b = document.querySelector(".mbtn"); return b ? getComputedStyle(b).backgroundColor : ""; }
  /* Protokoll der Choreografie, damit sie sich ohne Zuschauer pruefen laesst */
  var t0 = Date.now();
  window.__brandLog = [];
  function log(step) { window.__brandLog.push((Date.now() - t0) + "ms " + step); }

  /* Work <-> Case: die Kachel-Expansion bleibt die Transition, in beide Richtungen, ohne Punkt und Wolke */
  var flipIn = false, unflip = null;
  try { flipIn = !!sessionStorage.getItem("adbflip"); } catch (e) {}
  try { unflip = JSON.parse(sessionStorage.getItem("adbunflip") || "null"); sessionStorage.removeItem("adbunflip"); } catch (e) {}
  /* alle Kacheln auf Work expandieren, auch Farb- und Videokacheln (master.js bindet a[data-flip] nach uns) */
  Array.prototype.forEach.call(document.querySelectorAll('a.wt.tile[href^="case-"]:not([data-flip])'), function (a) { a.setAttribute("data-flip", ""); });
  if (unflip) {
    var pt0 = document.querySelector(".pt");
    if (pt0) { pt0.style.transition = "none"; pt0.classList.add("gone"); }
    var tile = unflip.href ? document.querySelector('a.wt.tile[href="' + unflip.href + '"]') : null;
    if (tile && unflip.rect) {
      /* Deckel an der gemerkten Stelle, die Seite scrollt darunter so, dass die Kachel exakt dort liegt;
         Bilder laden nach, also nach load und kurz danach noch einmal ausrichten, erst dann blendet der Deckel aus */
      var lid = document.createElement("div"); lid.className = "flipx flipx--lid";
      var timg = tile.querySelector("img"), tvid = tile.querySelector("video"), tsrc = timg ? (timg.currentSrc || timg.src) : (tvid && tvid.poster ? tvid.poster : "");
      if (tsrc) lid.style.backgroundImage = "url('" + tsrc + "')"; else lid.style.background = getComputedStyle(tile.querySelector(".wclr") || tile).backgroundColor;
      lid.style.borderRadius = getComputedStyle(tile).borderRadius;
      lid.style.top = unflip.rect.top + "px"; lid.style.left = unflip.rect.left + "px"; lid.style.width = unflip.rect.width + "px"; lid.style.height = unflip.rect.height + "px";
      body.appendChild(lid);
      function align() { var tr = tile.getBoundingClientRect(); var dy = tr.top - unflip.rect.top; if (Math.abs(dy) > 0.5) window.scrollTo(0, Math.max(0, window.pageYOffset + dy)); }
      align();
      window.addEventListener("load", align);
      setTimeout(align, 250);
      setTimeout(function () { align(); lid.style.opacity = "0"; setTimeout(function () { lid.remove(); }, M.base + 100); }, M.slow);
    }
  }
  var bk = document.querySelector(".bkbtn");
  if (bk && !reduced) bk.addEventListener("click", function (e) {
    e.preventDefault(); e.stopPropagation();
    var href = bk.getAttribute("href") || "work.html", me = location.pathname.split("/").pop() || "index.html";
    var saved = null; try { saved = JSON.parse(sessionStorage.getItem("adbflipFrom") || "null"); } catch (err) {}
    var rect = (saved && saved.href === me && saved.rect) ? saved.rect : null;
    var hero = document.querySelector(".chero"), img = hero && hero.querySelector("img");
    var bg = document.createElement("div"); bg.className = "flipbg"; body.appendChild(bg);
    var x = document.createElement("div"); x.className = "flipx";
    if (img) x.style.backgroundImage = "url('" + (img.currentSrc || img.src) + "')"; else x.style.background = getComputedStyle(hero || body).backgroundColor;
    x.style.top = "0px"; x.style.left = "0px"; x.style.width = "100vw"; x.style.height = "100vh"; x.style.borderRadius = "0";
    body.appendChild(x);
    var W = window.innerWidth, H = window.innerHeight, cw = Math.min(420, W * 0.7), ch = cw * 0.75;
    var t = rect || { top: (H - ch) / 2, left: (W - cw) / 2, width: cw, height: ch };
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      bg.classList.add("on");
      x.style.top = t.top + "px"; x.style.left = t.left + "px"; x.style.width = t.width + "px"; x.style.height = t.height + "px"; x.style.borderRadius = (saved && saved.radius) || "20px";
      setTimeout(function () {
        try { sessionStorage.setItem("adbunflip", JSON.stringify({ href: me, rect: rect })); } catch (err) {}
        location.href = href;
      }, M.slow + 20);
    }); });
  });

  /* Lange Choreografie (Punkt, Fokus mit Ringen, dann die Seite) nur beim ersten Seitenaufruf je Sitzung,
     danach die kurze: der Punkt erscheint, die Seite kommt nach einer Hover-Einheit, der Punkt wandert in den Menue-Kreis. */
  var introSeen = false;
  try { introSeen = !!sessionStorage.getItem("adb_intro"); sessionStorage.setItem("adb_intro", "1"); } catch (e) {}
  window.ADB_ENTER = function (pt, done) {
    if (flipIn || unflip) { pt.classList.add("gone"); body.classList.add("mready"); done(); log("Kachel-Transition, kein Punkt"); return; }
    if (reduced) { pt.classList.add("gone"); body.classList.add("mready"); done(); setTimeout(coach, 500); return; }
    /* Punkt erscheint (Einblenden) */
    dot.style.transition = M.t("transform", "--d-base") + ", " + M.t("opacity", "--d-fast");
    /* Phase merken: ein verspaeteter Frame (Hintergrund-Tab drosselt requestAnimationFrame) darf den Punkt nicht wieder einschalten */
    var phase = "in";
    requestAnimationFrame(function () { if (phase !== "in") return; dot.style.opacity = "1"; dot.style.transform = "scale(1)"; log("Punkt erscheint"); });
    var reveal = introSeen ? M.fast : M.chor;
    if (!introSeen) {
      /* Fokus: kurzer Atemzug, zwei Ringe */
      setTimeout(function () { phase = "focus"; dot.style.opacity = "1"; dot.classList.add("pulse"); dot.style.transition = M.t("transform", "--d-fast"); dot.style.transform = "scale(1.3)"; log("Fokus, Ringe"); }, M.base);
      setTimeout(function () { dot.style.transform = "scale(1)"; }, M.base + M.fast);
    }
    /* Ziel: die Seite kommt, der Punkt wandert in den Menue-Kreis (Uebergang), Start nach einer Choreografie-Einheit (kurz: Hover-Einheit) */
    setTimeout(function () {
      phase = "go";
      done();
      pt.classList.add("gone");
      mbTick(true);
      var t = target();
      if (t) { dot.style.transition = M.t("transform", "--d-slow") + ", " + M.t("background-color", "--d-slow"); dot.style.transform = at(t); dot.style.backgroundColor = mcolor(); log("wandert zum Menue " + at(t)); }
      setTimeout(function () {
        body.classList.add("mready");
        log("Menue-Kreis uebernimmt");
        setTimeout(coach, M.base);
        dot.classList.remove("pulse");
        dot.style.transition = M.t("opacity", "--d-fast");
        dot.style.opacity = "0";
        setTimeout(function () { dot.style.transition = "none"; dot.style.transform = "scale(0)"; dot.style.backgroundColor = ""; }, M.fast + 50);
      }, M.slow);
    }, reveal);
  };

  /* Beim Verlassen: eine Wolke aus Punkten sammelt sich zur Mitte, wo der Punkt wartet (dur: Dauer bis zur Mitte in ms) */
  function cloud(dur) {
    dur = dur || M.slow;
    if (reduced) return;
    var cv = document.createElement("canvas");
    cv.style.cssText = "position:fixed;inset:0;width:100%;height:100%;z-index:205;pointer-events:none";
    var dpr = Math.min(2, window.devicePixelRatio || 1), W = window.innerWidth, H = window.innerHeight;
    cv.width = W * dpr; cv.height = H * dpr; body.appendChild(cv);
    var c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0);
    var ps = [];
    /* Punkte in Textfarbe der Flaeche, kein Lime in Bewegung (Abschnitt 9) */
    var ink = body.classList.contains("on-light"), fillC = ink ? "#101010" : "#F4F3EB";
    for (var i = 0; i < 140; i++) {
      var ang = Math.random() * Math.PI * 2, rad = Math.max(W, H) * (0.35 + Math.random() * 0.6);
      ps.push({ x: W / 2 + Math.cos(ang) * rad, y: H / 2 + Math.sin(ang) * rad, r: 2 + Math.random() * 3.5, d: Math.random() * 0.25 * dur / M.slow });
    }
    var t0 = performance.now();
    (function draw(now) {
      var t = (now - t0) / 1000; c.clearRect(0, 0, W, H);
      var alive = false;
      ps.forEach(function (p) {
        var q = Math.max(0, Math.min(1, (t - p.d) / (dur / 1000))); if (q < 1) alive = true;
        var e = M.eOut(q), x = p.x + (W / 2 - p.x) * e, y = p.y + (H / 2 - p.y) * e;
        c.beginPath(); c.arc(x, y, p.r * (1 - e * 0.6), 0, Math.PI * 2);
        c.fillStyle = fillC; c.fill();
      });
      if (alive) requestAnimationFrame(draw); else setTimeout(function () { cv.remove(); }, M.fast);
    })(t0);
  }

  /* ---------- Erster Besuch: der Menue-Kreis erklaert sich selbst, vier Choreografien zum Vergleich.
     ?coach=1 erzwingt, &cv=1..4 waehlt (1 Punkt zerfaellt in fuenf, 2 Kreis drueckt sich selbst und oeffnet das Menue, 3 Iris, 4 Wort schreibt sich, 5 Spur zum Menue-Knopf oben, 6 = 2 dann 5, Standard),
     &hold=1 haelt im sprechendsten Moment. Einmal je Browser (localStorage adb_coach), endet bei der ersten Handlung. ---------- */
  var COACH_DEFAULT = 6;
  function coach() {
    if (reduced) return;
    var q = location.search, force = /coach=1/.test(q), hold = /hold=1/.test(q);
    if (/coach=0/.test(q)) return; /* fuer Pruefungen und Screenshots: kein Coach */
    var mv = q.match(/[?&]cv=(\d)/), variant = mv ? parseInt(mv[1], 10) : COACH_DEFAULT;
    var mb = document.querySelector(".mbtn"), sheet = document.querySelector(".msheet");
    if (!mb || !sheet || body.classList.contains("menuopen")) return;
    /* offenes Einwilligungs-Banner (master.js): der Coach wartet, bis entschieden ist */
    if (window.ADB_CONSENT_OPEN) { document.addEventListener("adbconsent", function () { setTimeout(coach, M.slow); }, { once: true }); return; }
    /* Sperre je Browser, versioniert: wer eine aeltere Choreografie gesehen hat, sieht die aktuelle einmal */
    var KEY = "adb_coach_v" + variant;
    try { if (!force && localStorage.getItem(KEY)) return; localStorage.setItem(KEY, "1"); } catch (e) { if (!force) return; }
    var els = [], timers = [], over = false, y0 = window.pageYOffset;
    var STATES = ["menupeek", "menuopen", "mdemo", "mpress", "miris", "mwriting", "mblink", "mpop"];
    function mk(cls) { var el = document.createElement("div"); el.className = cls; el.setAttribute("aria-hidden", "true"); body.appendChild(el); els.push(el); return el; }
    function at(ms, fn) { timers.push(setTimeout(fn, ms)); }
    /* alles gemessen: Mitte und Radius des Menue-Kreises, egal wie gross brand-ui.css ihn macht */
    function center() { var r = mb.getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height }; }
    function ring(delay, pt, cls) {
      var c = pt || center(), r = mk("coach-ring" + (cls ? " " + cls : "")), s = c.w || 64;
      r.style.left = c.x + "px"; r.style.top = c.y + "px";
      r.style.width = s + "px"; r.style.height = s + "px"; r.style.margin = (-s / 2) + "px 0 0 " + (-s / 2) + "px";
      at(delay || 0, function () { r.classList.add("burst"); });
    }
    function words() {
      return Array.prototype.map.call(sheet.querySelectorAll(".mitem .mt"), function (e) { var r = e.getBoundingClientRect(); return { t: e.textContent.trim(), x: r.left + r.width / 2 }; }).slice(0, 5);
    }
    function end() {
      if (over) return; over = true;
      timers.forEach(clearTimeout);
      STATES.forEach(function (k) { body.classList.remove(k); });
      els.forEach(function (e) { e.style.transition = M.t("opacity", "--d-fast"); e.style.opacity = "0"; });
      setTimeout(function () { els.forEach(function (e) { e.remove(); }); }, M.fast + 50);
      window.removeEventListener("pointerdown", end, true); window.removeEventListener("keydown", end, true);
      window.removeEventListener("scroll", onScroll, true);
      log("Coach Ende");
    }
    function onScroll() { if (Math.abs(window.pageYOffset - y0) > 40) end(); }
    window.addEventListener("pointerdown", end, true); window.addEventListener("keydown", end, true);
    window.addEventListener("scroll", onScroll, true);
    log("Coach Variante " + variant);

    /* 1: der Punkt springt auf und entlaesst fuenf Punkte, die sich dorthin legen, wo die Reiter des Menues liegen; jeder traegt kurz sein Wort */
    function fan() {
      var ws = words(), c = center(), narrow = window.innerWidth < 760;
      var dots = ws.map(function (w) { var d = mk("cdot"); d.innerHTML = "<i></i><span>" + w.t + "</span>"; d.style.left = c.x + "px"; d.style.top = c.y + "px"; return d; });
      body.classList.add("mpop");
      at(220, function () {
        body.classList.remove("mpop");
        dots.forEach(function (d, i) {
          var tx, ty;
          if (narrow) { var a = Math.PI * (1.1 + 0.8 * i / (ws.length - 1)), rr = Math.max(132, c.w * 1.6); tx = Math.cos(a) * rr; ty = Math.sin(a) * rr + 20; }
          else { tx = ws[i].x - c.x; ty = -28; }
          d.style.transitionDelay = (i * M.stagger) + "ms"; d.classList.add("go"); d.style.transform = "translate(" + tx.toFixed(1) + "px," + ty.toFixed(1) + "px)";
        });
        log("Coach: fuenf Punkte fliegen");
      });
      at(1000, function () { dots.forEach(function (d) { d.classList.add("say"); }); log("Coach: Worte"); });
      if (!hold) {
        at(2700, function () { dots.forEach(function (d) { d.classList.remove("say"); d.style.transitionDelay = "0ms"; d.style.transform = "translate(0,0)"; }); });
        at(3400, function () { body.classList.add("mpop"); dots.forEach(function (d) { d.classList.remove("go"); }); });
        at(3620, function () { body.classList.remove("mpop"); });
        at(3800, end);
      }
    }
    /* Reihe des Menues weich scrollen (wenn nicht alle Reiter Platz haben) */
    function scrollRow(el, target, dur) {
      var from = el.scrollLeft, t0 = performance.now();
      (function step(now) {
        if (over) return;
        var q = Math.min(1, (now - t0) / dur), e = M.eOut(q);
        el.scrollLeft = from + (target - from) * e;
        if (q < 1) requestAnimationFrame(step);
      })(t0);
    }
    /* 2: der Kreis macht die Geste vor: drueckt sich, ein Ring, das ganze Menue oeffnet sich echt (body.menuopen, Vorschaubilder kommen wie beim Klick),
       die Reihe faehrt einmal nach rechts und zurueck, falls nicht alle Reiter Platz haben, zweiter Druck, zu. Gibt zurueck, wann das Menue wieder zu ist. */
    function openDemo(t) {
      Array.prototype.forEach.call(sheet.querySelectorAll("img[loading=lazy]"), function (im) { im.loading = "eager"; });
      /* Vorschaubilder kommen erst bei Bedarf (master.js, data-src): jetzt laden, bevor das Menue aufgeht */
      if (window.ADB_MENUIMG) window.ADB_MENUIMG();
      var mrow = sheet.querySelector(".mrow");
      at(t, function () { ring(0); body.classList.add("mpress"); });
      at(t + M.fast + 60, function () { body.classList.remove("mpress"); body.classList.add("menuopen"); body.classList.add("mdemo"); log("Coach: Menue offen"); });
      var t2 = t + 2900;
      var wide = mrow && mrow.scrollWidth > mrow.clientWidth + 8;
      if (wide) {
        at(t + 1300, function () { scrollRow(mrow, mrow.scrollWidth - mrow.clientWidth, M.chor + M.base); log("Coach: Reihe faehrt"); });
        at(t + 3100, function () { scrollRow(mrow, 0, M.chor); });
        t2 = t + 4400;
      }
      if (!hold) {
        at(t2, function () { ring(0); body.classList.add("mpress"); });
        at(t2 + M.fast + 60, function () { body.classList.remove("mpress"); body.classList.remove("menuopen"); body.classList.remove("mdemo"); log("Coach: Menue zu"); });
      }
      return t2 + 1000;
    }
    function press() { var tEnd = openDemo(0); if (!hold) at(tEnd, end); }
    /* 5: eine Spur aus Punkten laeuft vom Kreis zum Menue-Knopf rechts oben, ein Punkt reist mit, oben leuchtet es auf: beide Wege oeffnen dasselbe */
    function trail(t) {
      t = t || 0;
      var hm = document.querySelector(".chrome .hmenu i"); if (!hm) { fan(); return; }
      var c = center(), hr = hm.getBoundingClientRect(), h = { x: hr.left + hr.width / 2, y: hr.top + hr.height / 2 };
      var W = window.innerWidth, H = window.innerHeight, ns = "http://www.w3.org/2000/svg";
      var box = mk("ctrail"), svg = document.createElementNS(ns, "svg");
      svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("width", W); svg.setAttribute("height", H); box.appendChild(svg);
      var path = document.createElementNS(ns, "path");
      var dy = c.y - h.y;
      /* Start knapp ueber dem gemessenen Rand des Menue-Kreises */
      path.setAttribute("d", "M" + c.x + "," + (c.y - c.h / 2 - 8) + " C" + c.x + "," + (c.y - dy * 0.55) + " " + h.x + "," + (h.y + dy * 0.4) + " " + h.x + "," + (h.y + 22));
      path.setAttribute("fill", "none"); path.setAttribute("stroke", "none"); svg.appendChild(path);
      var L = path.getTotalLength(), n = Math.max(12, Math.floor(L / 16)), dots = [];
      for (var i = 0; i <= n; i++) {
        var pt = path.getPointAtLength(L * i / n), ci = document.createElementNS(ns, "circle");
        ci.setAttribute("cx", pt.x.toFixed(1)); ci.setAttribute("cy", pt.y.toFixed(1)); ci.setAttribute("r", "2.4"); ci.setAttribute("class", "td");
        svg.appendChild(ci); dots.push(ci);
      }
      var trv = document.createElementNS(ns, "circle"); trv.setAttribute("r", "6"); trv.setAttribute("class", "trv"); trv.setAttribute("opacity", "0"); svg.appendChild(trv);
      at(t, function () { ring(0); log("Coach: Spur startet"); });
      var dur = M.chor, step = dur / Math.max(1, dots.length);
      dots.forEach(function (d, i) { at(t + M.base + i * step * 0.8, function () { d.classList.add("on"); }); });
      at(t + M.base, function () {
        trv.setAttribute("opacity", "1"); var t0 = performance.now();
        (function step(now) {
          if (over) return;
          var q = Math.min(1, (now - t0) / dur), e = M.eOut(q), pt = path.getPointAtLength(L * e);
          trv.setAttribute("cx", pt.x.toFixed(1)); trv.setAttribute("cy", pt.y.toFixed(1));
          if (q < 1) requestAnimationFrame(step); else { trv.setAttribute("opacity", "0"); hm.classList.add("lit"); var hs = Math.max(24, hr.width * 3); ring(0, { x: h.x, y: h.y, w: hs, h: hs }, "small"); log("Coach: oben angekommen"); }
        })(t0);
      });
      if (!hold) {
        at(t + M.base + dur + 1200, function () { dots.forEach(function (d) { d.classList.remove("on"); }); hm.classList.remove("lit"); });
        at(t + M.base + dur + 1200 + M.slow, end);
      }
    }
    /* 6: Kombination: erst drueckt sich der Kreis und zeigt das Menue, dann laeuft die Spur zum zweiten Eingang oben */
    function combo() {
      var tEnd = openDemo(0);
      if (!hold) trail(tEnd + 200);
    }
    /* 3: Iris: der Kreis waechst auf das Dreifache, innen ein Ring aus fuenf Punkten, die Worte laufen in der Mitte durch */
    function iris() {
      var ws = words(), c = center(), ir = mk("iris");
      ir.style.left = c.x + "px"; ir.style.top = c.y + "px";
      ir.innerHTML = '<div class="iring">' + ws.map(function (w, i) { return '<i style="--a:' + (i * 72) + 'deg"></i>'; }).join("") + '</div><span class="iword"></span>';
      var word = ir.querySelector(".iword"), pins = ir.querySelectorAll(".iring i");
      body.classList.add("miris");
      at(450, function () { ir.classList.add("on"); log("Coach: Iris offen"); });
      ws.forEach(function (w, i) { at(700 + i * 520, function () { word.textContent = w.t; word.classList.remove("in"); void word.offsetWidth; word.classList.add("in"); pins[i].classList.add("lit"); }); });
      var done = 700 + ws.length * 520 + 400;
      if (!hold) {
        at(done, function () { ir.classList.remove("on"); body.classList.remove("miris"); });
        at(done + 800, end);
      }
    }
    /* 4: das Wort schreibt sich Buchstabe fuer Buchstabe in den Kreis, dann blinkt der Kern zweimal */
    function write() {
      var c = center(), wr = mk("mwrite");
      wr.style.left = c.x + "px"; wr.style.top = c.y + "px";
      wr.innerHTML = "Menü".split("").map(function (ch) { return "<b>" + ch + "</b>"; }).join("");
      ring(0); body.classList.add("mwriting");
      Array.prototype.forEach.call(wr.querySelectorAll("b"), function (bb, i) { at(500 + i * 150, function () { bb.classList.add("in"); }); });
      at(1100, function () { log("Coach: Wort steht"); });
      if (!hold) {
        at(2400, function () { wr.classList.add("out"); body.classList.remove("mwriting"); body.classList.add("mblink"); });
        at(3400, function () { body.classList.remove("mblink"); });
        at(3500, end);
      }
    }
    if (variant === 2) press(); else if (variant === 3) iris(); else if (variant === 4) write(); else if (variant === 5) trail(0); else if (variant === 6) combo(); else fan();
  }

  /* ---------- Leistungs-Hero: das Wort fuellt die Zeile exakt (Schriftgroesse an die Rahmenbreite) ---------- */
  (function () {
    var w = document.querySelector(".dhero .dh-word"); if (!w) return;
    var f = w.querySelector(".dh-fit"); if (!f) return;
    function fit() {
      f.style.display = "inline-block";
      w.style.setProperty("font-size", "100px", "important");
      var r = w.clientWidth / f.getBoundingClientRect().width;
      w.style.setProperty("font-size", (100 * r * 0.995).toFixed(2) + "px", "important");
      f.style.display = "";
    }
    fit();
    addEventListener("load", fit); addEventListener("resize", fit);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  })();

  /* ---------- Work: aktiver Filter (nicht Alle) markiert seinen Kreis ---------- */
  (function () {
    var pairs = [[".fbtn", ".fpop"], [".bbtn", ".bpop"]];
    function mark() {
      pairs.forEach(function (pr) {
        var b = document.querySelector(pr[0]), on = document.querySelector(pr[1] + " .fchip.on");
        if (b) b.classList.toggle("has", !!(on && (on.getAttribute("data-cat") || on.getAttribute("data-branche") || "").toLowerCase() !== "alle"));
      });
    }
    if (document.querySelector(".fbtn, .bbtn")) { document.addEventListener("click", function () { setTimeout(mark, 0); }); mark(); }
  })();

  /* ---------- Kopfzeile: gelernter Menue-Knopf rechts neben Kontakt, klickt den Punkt ---------- */
  (function () {
    var chrome = document.querySelector(".chrome"), ctc = chrome && chrome.querySelector(".ctc"), mb = document.querySelector(".mbtn");
    if (!chrome || !ctc || !mb) return;
    var wrap = document.createElement("div"); wrap.className = "chr";
    var btn = document.createElement("button"); btn.className = "hmenu"; btn.type = "button"; btn.setAttribute("aria-label", "Menü öffnen");
    btn.innerHTML = '<i aria-hidden="true"></i><span class="hm-open">Menü</span><span class="hm-close">Schließen</span>';
    btn.addEventListener("click", function () { mb.click(); });
    ctc.parentNode.insertBefore(wrap, ctc); wrap.appendChild(ctc); wrap.appendChild(btn);
  })();

  window.ADB_LEAVE = function (pt, href) {
    mbTick(true);
    var t = target();
    body.classList.remove("mready");
    /* Verlassen in einer Einblenden-Einheit (400 ms statt 1000): Punkt, Wolke und Blende laufen gleichzeitig */
    cloud(M.base);
    dot.classList.remove("pulse");
    dot.style.transition = "none";
    dot.style.opacity = "1";
    dot.style.transform = t ? at(t) : "scale(1)";
    dot.style.backgroundColor = mcolor();
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        /* der Menue-Kreis wird wieder Punkt und geht in die Mitte, die Blende faellt dabei */
        dot.style.transition = M.t("transform", "--d-base") + ", " + M.t("background-color", "--d-base");
        dot.style.transform = "scale(1)";
        dot.style.backgroundColor = "";
        dot.classList.add("pulse");
        pt.classList.remove("gone");
        pt.classList.add("enter");
        requestAnimationFrame(function () { pt.classList.add("cover"); });
        setTimeout(function () { location.href = href; }, M.base);
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
  /* Fuellung ueber Klassen, Farben in brand-motion.css: .is-on gefuellt, .is-best bester/aktueller Wert.
     best "last": nur der letzte gefuellte Punkt ist .is-best (der eine Lime-Punkt, Stat 84:59), "all" gibt es nicht mehr.
     (.on bleibt zusaetzlich gesetzt, damit aeltere Selektoren in brand.css/brand-ui.css weiter greifen).
     Die ganze Fuellung dauert hoechstens eine Choreografie-Einheit, egal wie viele Punkte. */
  function fill(el, count, best, delay) {
    var dots = el.querySelectorAll("i"), step = Math.min(40, M.chor / Math.max(1, count));
    for (var i = 0; i < dots.length; i++) {
      (function (d, k) {
        if (k < count) setTimeout(function () { d.classList.add("is-on", "on"); if (best === "last" && k === count - 1) d.classList.add("is-best"); }, reduced ? 0 : (delay || 0) + k * step);
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
        /* Punkt-Graph: der letzte gefuellte Punkt ist der Wert; Balken: die hervorgehobene Zeile (.hi) ist der beste Wert */
        var hiRow = el.closest(".row.hi");
        fill(el, count, el.classList.contains("dotgraph") ? "last" : (hiRow ? "last" : ""), 0);
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
      ? '<circle cx="32" cy="32" r="12" fill="none" stroke="#CDFF00" stroke-width="5"/>'
      : '<circle cx="32" cy="32" r="13" fill="#CDFF00"/><circle cx="32" cy="32" r="5" fill="#101010"/>';
    return "data:image/svg+xml," + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#101010"/>' + inner + '</svg>');
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
    setTimeout(function () { go.classList.remove("fired"); }, M.slow + M.stagger + 20);
  });

  /* ---------- Punktfeld: echte Einheiten als Punkte. Beim Laden sammeln sie sich ins Raster,
       der Lime-Anteil steht in Leserichtung, am Desktop ziehen sie sich zum Cursor. ---------- */
  Array.prototype.slice.call(document.querySelectorAll("canvas.dotfield")).forEach(function (cv) {
    var total = parseInt(cv.getAttribute("data-total"), 10) || 100;
    var lime = parseInt(cv.getAttribute("data-lime"), 10) || 0;
    var ctx = cv.getContext("2d"), dots = [], W = 0, H = 0, dpr = Math.min(2, window.devicePixelRatio || 1);
    /* Farben aus brand-motion.css (Abschnitt 7): Anteil gefuellt, der letzte Anteilspunkt ist der Wert, der Rest Umriss */
    var ccs = getComputedStyle(cv);
    /* Farben wie auf der alten Seite (Kundenentscheidung 3.10.2026, Werte in brand-keep.css): gezaehlt Lime mit Ring, Rest grau */
    var C_ON = (ccs.getPropertyValue("--g-on") || "").trim() || "#CDFF00", C_RING = (ccs.getPropertyValue("--g-ring") || "").trim() || "rgba(16,16,16,0.6)", C_OFF = (ccs.getPropertyValue("--g-off") || "").trim() || "rgba(16,16,16,0.16)";
    var mx = -9999, my = -9999, start = 0, seen = false, running = false, fine = window.matchMedia("(pointer: fine)").matches;
    /* Antippen: die Lime-Punkte sammeln sich zur Zahl (data-form), zweites Antippen loest sie wieder */
    var formText = cv.getAttribute("data-form"), formed = false, form = 0, formT = 0;
    function targets() {
      if (!formText || !W) return;
      var oc = document.createElement("canvas"); oc.width = Math.round(W); oc.height = Math.round(H);
      var o = oc.getContext("2d");
      o.font = "400 " + Math.round(H * 0.92) + 'px "amandine", Georgia, serif';
      o.textAlign = "center"; o.textBaseline = "middle"; o.fillStyle = "#101010";
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
        dots.push({ x: gx * (c + 0.5), y: gy * (rw + 0.5), sx: W / 2 + (Math.random() - 0.5) * W * 1.8, sy: H / 2 + (Math.random() - 0.5) * H * 1.8, r: rad, lime: i < lime, best: i === lime - 1, d: Math.random() * 0.4 });
      }
    }
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
      /* Formfortschritt: hin zur Zahl oder zurueck ins Raster, je ein Uebergang */
      var target = formed ? 1 : 0, fdt = Math.min(1, (now - formT) / M.slow);
      var formNow = formed ? fdt : 1 - fdt;
      if (Math.abs(formNow - target) > 0.001) settled = false;
      form = formNow;
      var ef = M.eOut(form);
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var p = reduced ? 1 : (coarse ? Math.max(0, Math.min(1, (sp * 1.4 - d.d) / 0.6)) : Math.max(0, Math.min(1, (t - d.d) / (M.chor / 1000))));
        if (p < 1) settled = false;
        var e = M.eOut(p), x = d.sx + (d.x - d.sx) * e, y = d.sy + (d.y - d.sy) * e, r = d.r;
        if (coarse && d.lime && p >= 1 && form === 0 && !reduced) { r = d.r * (1 + 0.32 * Math.sin(t * 1.6 + (d.x + d.y) / 55)); settled = false; }
        if (d.lime && d.tx != null && form > 0) { x += (d.tx - x) * ef; y += (d.ty - y) * ef; r = d.r * (1 + ef * 0.25); }
        if (fine && p >= 1 && form === 0) {
          var dx = mx - x, dy = my - y, dist = Math.sqrt(dx * dx + dy * dy), R = 150;
          if (dist < R) { var f = 1 - dist / R; x += dx / (dist || 1) * f * 12; y += dy / (dist || 1) * f * 12; r = d.r * (1 + f * 0.9); }
        }
        ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2);
        if (d.lime) { ctx.fillStyle = C_ON; ctx.fill(); ctx.lineWidth = 1; ctx.strokeStyle = C_RING; ctx.stroke(); }
        else { ctx.globalAlpha = 1 - ef * 0.7; ctx.fillStyle = C_OFF; ctx.fill(); ctx.globalAlpha = 1; }
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
      for (var k = 0; k < cells.length; k++) { cells[k].classList.toggle("is-on", k < n); cells[k].classList.toggle("on", k < n); cells[k].classList.toggle("is-best", k === n - 1); }
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
        var st = Math.min(80, M.chor / Math.max(1, row.children.length));
        Array.prototype.forEach.call(row.children, function (d, k) { setTimeout(function () { d.classList.add("is-on", "on"); if (d.classList.contains("e")) d.classList.add("is-best"); }, reduced ? 0 : k * st); });
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
        path.style.transition = M.t("stroke-dashoffset", "--d-chor");
        var kds = line.querySelectorAll(".kd"), kst = (M.chor - M.fast) / Math.max(1, kds.length);
        kds.forEach(function (c, i) { c.style.transitionDelay = Math.round(M.fast + i * kst) + "ms"; });
      }
    }
    var kd = k.querySelectorAll(".kdots .dots");
    kd.forEach(function (dts) { var n = parseInt(dts.getAttribute("data-n"), 10) || 0; for (var i = 0; i < n; i++) dts.appendChild(document.createElement("i")); });
    var ioK = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (!x.isIntersecting) return;
        ioK.unobserve(k);
        k.classList.add("lit");
        if (line) {
          var pth = line.querySelector(".kpath"); if (pth) pth.style.strokeDashoffset = 0;
          var kc = line.querySelectorAll(".kd");
          Array.prototype.forEach.call(kc, function (c, i) { c.classList.add(i === kc.length - 1 ? "is-best" : "is-on"); });
        }
        kd.forEach(function (dts) { var on = parseInt(dts.getAttribute("data-on"), 10) || 0; fill(dts, on, dts.closest(".row.hi") ? "last" : "", M.fast); });
        if (to && !reduced && to.hasAttribute("data-to")) {
          var from = parseFloat(to.getAttribute("data-from")), end = parseFloat(to.getAttribute("data-to"));
          var dec = parseInt(to.getAttribute("data-decimals"), 10) || 0, pre = to.getAttribute("data-prefix") || "", suf = to.getAttribute("data-suffix") || "";
          var t0 = performance.now();
          (function step(now) {
            var q = Math.min(1, (now - t0) / M.chor), e = M.eOut(q);
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
  var marks = Array.prototype.slice.call(document.querySelectorAll("main section[id]:not(#anfrage):not(#kontakt)")).map(function (t) {
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
      setTimeout(function () { body.classList.remove("cur-tap"); }, M.base + 100);
    });
  }

  /* ---------- Punkt-Zoom: Sektion oeffnet sich aus einem Punkt, gesteuert vom Scroll ---------- */
  var zooms = Array.prototype.slice.call(document.querySelectorAll(".dotzoom")).map(function (s) { return { el: s, p: -1 }; });
  function zoomTick() {
    zooms.forEach(function (z) {
      var r = z.el.getBoundingClientRect();
      var p = reduced ? 1 : Math.max(0, Math.min(1, (window.innerHeight * 0.95 - r.top) / (window.innerHeight * 0.62)));
      /* die Schrift-Kopie folgt dem Original auch, wenn der Kreis steht (Wort-Scrub schaltet nach) */
      if (z.k && z.k.style.display === "block" && z.k.innerHTML !== z.prev.innerHTML) z.k.innerHTML = z.prev.innerHTML;
      if (Math.abs(p - z.p) < 0.003) return;
      z.p = p;
      /* erst waechst der Punkt (0 bis 0,2), dann oeffnet sich aus ihm das Loch und der Punkt zieht sich zurueck */
      var zd = p < 0.2 ? p / 0.2 : Math.max(0, 1 - (p - 0.2) / 0.22);
      var zr = p < 0.2 ? 0 : (p - 0.2) / 0.8 * Math.hypot(r.width, r.height) * 0.62;
      z.el.style.setProperty("--zd", zd.toFixed(3));
      z.el.style.setProperty("--zr", zr.toFixed(0) + "px");
      z.el.classList.toggle("zdone", p >= 1);
      /* Kundenentscheidung 3.10.2026: der helle Kreis bleibt rund und waechst ueber die Sektion darueber hinaus.
         Innerhalb der Sektion zeigt das Loch im Deckel den Inhalt, oberhalb der Kante zeichnet .zcircle den Kreis weiter. */
      if (!z.c) {
        var zcs = getComputedStyle(z.el);
        z.c = document.createElement("span"); z.c.className = "zcircle"; z.c.setAttribute("aria-hidden", "true");
        z.bg = zcs.backgroundColor; z.el.appendChild(z.c);
        /* Schrift der Sektion darueber: wo der Kreis sie trifft, nimmt sie die Textfarbe der Kreis-Sektion an
           (Startseite: weisse Schrift wird schwarz). Dafuer liegt eine Kopie des Inhalts, auf den Kreis zugeschnitten, darueber. */
        var prev = z.el.previousElementSibling;
        if (prev && prev.tagName === "SECTION" && prev.firstElementChild) {
          /* gleiche Klassen wie die Sektion darueber, damit Schriftgroessen und Abstaende exakt passen (ohne data-bg) */
          z.prev = prev; z.k = document.createElement("div"); z.k.className = "zink " + prev.className; z.k.setAttribute("aria-hidden", "true");
          z.k.setAttribute("inert", ""); z.k.style.color = zcs.color; z.el.appendChild(z.k);
        }
      }
      var cy = r.height * 0.42, above = zr - cy;
      /* nur wo die Sektion es erlaubt (data-zover, Startseite); auf Unterseiten bleibt der Kreis in seiner Sektion */
      if (reduced || above <= 0 || !z.el.hasAttribute("data-zover")) { z.c.style.width = z.c.style.height = "0px"; if (z.k) z.k.style.display = "none"; }
      else {
        var d = 2 * zr; z.c.style.background = z.bg; z.c.style.width = z.c.style.height = d.toFixed(0) + "px"; z.c.style.clipPath = "inset(0 0 " + (zr + cy).toFixed(0) + "px 0)";
        if (z.k) {
          var pr = z.prev.getBoundingClientRect(), left = pr.left - r.left, top = pr.top - r.top;
          if (z.k.innerHTML !== z.prev.innerHTML) z.k.innerHTML = z.prev.innerHTML;
          z.k.style.display = "block"; z.k.style.left = left.toFixed(0) + "px"; z.k.style.top = top.toFixed(0) + "px";
          z.k.style.width = pr.width.toFixed(0) + "px"; z.k.style.height = pr.height.toFixed(0) + "px";
          z.k.style.padding = getComputedStyle(z.prev).padding;
          z.k.style.clipPath = "circle(" + zr.toFixed(0) + "px at " + (r.width / 2 - left).toFixed(0) + "px " + (cy - top).toFixed(0) + "px)";
        }
      }
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
        Array.prototype.forEach.call(line.children, function (sp, k) { setTimeout(function () { sp.classList.add("on"); }, reduced ? 0 : M.base + k * M.fast); });
        ioL.unobserve(line);
      });
    });
    ioL.observe(line);
  });

  /* ---------- Menue-Knopf: Untergrund messen (Abschnitt 1 und 9: Lime nie auf Schwarz, nie an Fotos).
       Je Frame (gedrosselt) 9 Punkte im Feld Knopf plus 40 px Rand: was liegt dort unter der festen UI?
       Genau eine Klasse am body: mb-photo (IMG, VIDEO, CANVAS, Hintergrundbild), mb-dark (dunkle Flaeche), sonst mb-light.
       Gemischt gilt Cream: ein Foto-Treffer macht mb-photo, ein dunkler Treffer mb-dark. Lime nur bei mb-light (brand-ui.css). ---------- */
  var mbEl = document.querySelector(".mbtn"), mbState = "", mbY = -1, mbT = 0, MB_PAD = 40;
  var uiCache = typeof WeakMap === "function" ? new WeakMap() : null;
  var MB_CLS = { light: "mb-light", dark: "mb-dark", photo: "mb-photo" };
  /* feste UI (Knopf, Satelliten, Kopfzeile, Blende, Cursor, Coach) ist nie Untergrund: alles mit position fixed in der Ahnenreihe */
  function isUi(el) {
    if (uiCache && uiCache.has(el)) return uiCache.get(el);
    var r = false, e = el;
    while (e && e !== body && e.nodeType === 1) { if (getComputedStyle(e).position === "fixed") { r = true; break; } e = e.parentElement; }
    if (uiCache) uiCache.set(el, r);
    return r;
  }
  function rgba(str) { var m = (str || "").match(/rgba?\(([^)]+)\)/); if (!m) return null; var p = m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; }
  function dark(c) { return (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]) / 255 < 0.45; }
  function media(el) { var t = el.tagName; return t === "IMG" || t === "VIDEO" || t === "CANVAS" || t === "PICTURE" || t === "image" || t === "IFRAME"; }
  /* wirksame Deckkraft: ein noch nicht eingeblendeter Vorfahre (data-fade, opacity 0) macht das Element unsichtbar */
  function faded(el) {
    for (var e = el; e && e !== body && e.nodeType === 1; e = e.parentElement) if (parseFloat(getComputedStyle(e).opacity) < 0.05) return true;
    return false;
  }
  function under(x, y) {
    var st = document.elementsFromPoint(x, y);
    for (var i = 0; i < st.length; i++) {
      var el = st[i];
      if (el === body || el === document.documentElement) break;
      if (isUi(el)) continue;
      var cs = getComputedStyle(el);
      if (cs.visibility === "hidden" || faded(el)) continue;
      if (media(el) || /url\(/.test(cs.backgroundImage)) return "photo";
      var c = rgba(cs.backgroundColor);
      if (c && c[3] > 0.5) return dark(c) ? "dark" : "light";
    }
    var bc = rgba(getComputedStyle(body).backgroundColor);
    return bc && bc[3] > 0.5 && dark(bc) ? "dark" : "light";
  }
  /* Fotos auch geometrisch: Medien, die das Feld schneiden (auch mit pointer-events none, die elementsFromPoint uebergeht) */
  var mbMedia = [], mbMediaT = 0;
  function photoNear(z) {
    var now = performance.now();
    if (now - mbMediaT > 2000) { mbMediaT = now; mbMedia = Array.prototype.slice.call(document.querySelectorAll("main img, main video, main canvas, main iframe, main picture")); }
    for (var i = 0; i < mbMedia.length; i++) {
      var m = mbMedia[i], r = m.getBoundingClientRect();
      if (!r.width || !r.height || r.right < z.l || r.left > z.r || r.bottom < z.t || r.top > z.b) continue;
      if (isUi(m)) continue;
      var e = m, vis = true;
      while (e && e !== body) { var cs = getComputedStyle(e); if (cs.visibility === "hidden" || cs.display === "none" || parseFloat(cs.opacity) < 0.05) { vis = false; break; } e = e.parentElement; }
      if (vis) return true;
    }
    return false;
  }
  function mbTick(force) {
    if (!mbEl) return;
    var now = performance.now(), y = window.pageYOffset;
    if (!force && y === mbY && now - mbT < 300) return;
    mbY = y; mbT = now;
    var r = mbEl.getBoundingClientRect(); if (!r.width) return;
    var W = window.innerWidth, H = window.innerHeight;
    var z = { l: Math.max(1, r.left - MB_PAD), r: Math.min(W - 2, r.right + MB_PAD), t: Math.max(1, r.top - MB_PAD), b: Math.min(H - 2, r.bottom + MB_PAD) };
    var mx = (z.l + z.r) / 2, my = (z.t + z.b) / 2;
    var pts = [[z.l, z.t], [z.r, z.t], [z.l, z.b], [z.r, z.b], [mx, z.t], [mx, z.b], [z.l, my], [z.r, my], [mx, my]];
    var seen = { light: 0, dark: 0, photo: 0 };
    for (var i = 0; i < pts.length; i++) seen[under(pts[i][0], pts[i][1])]++;
    var st = (seen.photo || photoNear(z)) ? "photo" : (seen.dark ? "dark" : "light");
    if (st === mbState) return;
    if (mbState) body.classList.remove(MB_CLS[mbState]);
    body.classList.add(MB_CLS[st]);
    mbState = st;
    window.__mbState = st;
  }
  /* Kopfzeile: jedes Element (Logo, Kontakt, Menue) misst seinen eigenen Untergrund an drei Punkten und traegt ihn als
     data-ug (light, dark, photo). brand-motion.css faerbt danach: Schwarz auf Cream und Lime, Cream auf Schwarz und Foto. */
  var chEls = Array.prototype.slice.call(document.querySelectorAll(".chrome .logo, .chrome .ctc, .chrome .hmenu")), chY = -1;
  function chTick(force) {
    var y = window.pageYOffset;
    if (!force && y === chY) return;
    chY = y;
    chEls.forEach(function (el) {
      var r = el.getBoundingClientRect(); if (!r.width) return;
      var my = r.top + r.height / 2, seen = { light: 0, dark: 0, photo: 0 };
      [r.left + 2, r.left + r.width / 2, r.right - 2].forEach(function (x) { seen[under(Math.max(1, x), Math.max(1, my))]++; });
      var st = seen.photo ? "photo" : (seen.dark >= 2 ? "dark" : (seen.light >= 2 ? "light" : "dark"));
      if (el.getAttribute("data-ug") !== st) el.setAttribute("data-ug", st);
    });
  }
  /* ohne Scroll aendert sich der Untergrund auch (Einblenden, Slider, Menue): spaetestens alle 500 ms neu messen.
     Technik B4: das Nachmessen laeuft nur, solange sich etwas tun kann, also bis UI_BUSY ms nach dem letzten Anlass
     (Laden, Scroll, Resize, Eingabe, Klassen- oder Farbwechsel am body, Folienwechsel), und nie im Hintergrund-Tab.
     Ohne Anlass bleibt der gemessene Zustand stehen, wie bisher auch: dann aendert sich unter dem Knopf nichts. */
  var uiT = 0, uiBusy = 0, uiIv = 0, UI_BUSY = 3000;
  function uiTick(force) {
    var now = performance.now(), again = force || (now < uiBusy && now - uiT > 500);
    if (again) uiT = now;
    else if (window.pageYOffset === mbY && window.pageYOffset === chY) return;
    mbTick(again); chTick(again);
  }
  function uiPoke(ms) {
    if (document.hidden) return;
    uiBusy = Math.max(uiBusy, performance.now() + (ms || UI_BUSY));
    if (!uiIv) uiIv = setInterval(function () {
      /* Sicherheitsnetz, falls Frames gedrosselt sind (Energiesparen): alle 500 ms nachmessen, solange Anlass besteht */
      if (document.hidden || performance.now() > uiBusy) { clearInterval(uiIv); uiIv = 0; return; }
      uiTick(true);
    }, 500);
  }
  uiTick(true);
  uiPoke(4000);
  window.ADB_MBTICK = uiTick;
  window.ADB_MBTICK_POKE = uiPoke;
  /* zusaetzlich am Scroll-Ereignis: gedrosselte Frames (Energiesparen) duerfen den Knopf nicht auf altem Untergrund lassen */
  window.addEventListener("scroll", function () { uiPoke(); uiTick(); }, { passive: true });
  window.addEventListener("resize", function () { uiPoke(); uiTick(true); });
  window.addEventListener("load", function () { uiPoke(); });
  window.addEventListener("pageshow", function () { uiPoke(); uiTick(true); });
  ["pointerdown", "keydown", "click", "touchstart"].forEach(function (ev) { document.addEventListener(ev, function () { uiPoke(); }, { passive: true, capture: true }); });
  document.addEventListener("visibilitychange", function () { if (!document.hidden) { uiPoke(); uiTick(true); } });
  /* Klassen am body (menuopen, loaded, on-light, Coach) und die Hintergrundfarbe (data-bg beim Scrollen) */
  if (window.MutationObserver) new MutationObserver(function () { uiPoke(); }).observe(body, { attributes: true, attributeFilter: ["class", "style"] });

  /* Buttons: Ein- und Austrittsstelle der Maus fuer den Kreis-Hover (brand-motion.css, --mx/--my) */
  function btnPoint(e) {
    var b = e.target && e.target.closest ? e.target.closest(".btn") : null;
    if (!b || (e.relatedTarget && b.contains(e.relatedTarget))) return;
    var r = b.getBoundingClientRect();
    b.style.setProperty("--mx", (e.clientX - r.left).toFixed(0) + "px");
    b.style.setProperty("--my", (e.clientY - r.top).toFixed(0) + "px");
  }
  document.addEventListener("pointerover", btnPoint, { passive: true });
  document.addEventListener("pointerout", btnPoint, { passive: true });

  function brandTick() {
    uiTick();
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
}
/* ---------- master.js ---------- */
;{
/* ad.boutique Master, Engine
   Cursor, Menue-Sheet, Reveals, Keyword-Scrub, Hero-Rotation,
   Hintergrund-Morph, Drift-Parallax, Filter-FLIP, Tile-Expansion,
   Page-Transitions. Kein Framework, keine Abhaengigkeiten. */
(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var docEl = document.documentElement;
  /* Bewegungswerte aus brand-motion.css, bereitgestellt von brand.js; Rueckfall auf dieselbe Skala */
  var MO = window.ADB_MOTION || { fast: 200, base: 400, slow: 700, chor: 1200, stagger: 80, ease: "cubic-bezier(0.16, 1, 0.3, 1)" };

  /* ---------- Spaete Quellen: Videos und Menue-Bilder tragen data-src (_perf.py), die Quelle kommt erst bei Bedarf ---------- */
  function vsrc(el) {
    var s = el.getAttribute("data-src");
    if (s) { el.removeAttribute("data-src"); el.setAttribute("src", s); }
    return el;
  }
  function vplay(v) { vsrc(v); var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  window.ADB_VSRC = vsrc;

  /* ---------- Page-Transition ---------- */
  var pt = document.querySelector(".pt");
  /* Kam die Navigation aus der Tile-Expansion, sofort ohne schwarze Blende starten */
  if (pt && sessionStorage.getItem("adbflip")) {
    sessionStorage.removeItem("adbflip");
    pt.style.transition = "none";
    pt.classList.add("gone");
    requestAnimationFrame(function () { pt.style.transition = ""; });
  }
  var entered = false;
  function enterPage() {
    if (entered) return;
    entered = true;
    /* Brand-Test: eine eigene Choreografie (Punkt wandert in den Menue-Kreis) darf uebernehmen */
    if (window.ADB_ENTER && pt) { window.ADB_ENTER(pt, function () { document.body.classList.add("loaded"); }); return; }
    document.body.classList.add("loaded");
    if (!pt) return;
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { pt.classList.add("gone"); });
    });
  }
  /* Start, sobald das HTML steht und ein Frame gezeichnet ist (nicht erst bei load: Bilder und Videos halten load auf) */
  function enterSoon() { requestAnimationFrame(function () { enterPage(); }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", enterSoon);
  else enterSoon();
  window.addEventListener("load", enterPage);
  setTimeout(enterPage, 600); /* Rueckfall, falls kein Frame kommt (Hintergrund-Tab) */

  function leaveTo(href) {
    if (reduced || !pt) { location.href = href; return; }
    if (window.ADB_LEAVE) { window.ADB_LEAVE(pt, href); return; }
    pt.classList.remove("gone");
    pt.classList.add("enter");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        pt.classList.add("cover");
        setTimeout(function () { location.href = href; }, 520);
        setTimeout(function () {
          /* Seite ist noch da: Blende wieder oeffnen statt schwarz stehen zu bleiben */
          pt.classList.remove("cover");
          setTimeout(function () { pt.classList.remove("enter"); pt.classList.add("gone"); }, 520);
        }, 4000);
      });
    });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href]");
    if (!a) return;
    var href = a.getAttribute("href");
    if (!href || href.indexOf("#") === 0 || a.target === "_blank" ||
        href.indexOf("http") === 0 || href.indexOf("mailto:") === 0) return;
    if (a.hasAttribute("data-flip")) return; /* Tile-Expansion regelt selbst */
    /* Sprung innerhalb derselben Seite (z. B. index.html#leistungen von der Startseite aus):
       kein Seitenwechsel, also keine Blende, sonst bleibt sie schwarz stehen */
    var url;
    try { url = new URL(href, location.href); } catch (err) { url = null; }
    if (url && url.hash && url.pathname === location.pathname) { closeMenu(); return; }
    e.preventDefault();
    closeMenu();
    leaveTo(href);
  });
  /* Sicherheitsnetz: Blende nie dauerhaft stehen lassen. Zurueck-Navigation aus dem
     Browser-Cache stellt die Seite mit geschlossener Blende wieder her; und wenn nach dem
     Klick kein Seitenwechsel passiert ist, geht die Blende wieder auf. */
  window.addEventListener("pageshow", function (e) {
    if (e.persisted && pt) {
      pt.style.transition = "none";
      pt.classList.remove("enter", "cover");
      pt.classList.add("gone");
      document.body.classList.add("loaded");
      requestAnimationFrame(function () { pt.style.transition = ""; });
    }
  });

  /* ---------- Cursor ---------- */
  if (window.matchMedia("(pointer: fine)").matches) {
    var cur = document.createElement("div");
    cur.className = "cur";
    document.body.appendChild(cur);
    var cx = -100, cy = -100, tx = -100, ty = -100, seen = false;
    document.addEventListener("mousemove", function (e) {
      tx = e.clientX; ty = e.clientY;
      if (!seen) { seen = true; cx = tx; cy = ty; }   /* erster Frame ohne Nachlauf */
    }, { passive: true });
    /* Position ueber die eigene translate-Eigenschaft: die Skalierung darf
       eine Transition haben, die Bewegung nicht, sonst daempft sie doppelt. */
    (function curLoop() {
      cx += (tx - cx) * 0.55; cy += (ty - cy) * 0.55;
      cur.style.translate = cx.toFixed(1) + "px " + cy.toFixed(1) + "px";
      requestAnimationFrame(curLoop);
    })();
    document.addEventListener("mouseover", function (e) {
      if (e.target.closest("a, button, [data-hover]")) document.body.classList.add("cur-hov");
    });
    document.addEventListener("mouseout", function (e) {
      if (e.target.closest("a, button, [data-hover]")) document.body.classList.remove("cur-hov");
    });
  }

  /* ---------- Menue ---------- */
  var mbtn = document.querySelector(".mbtn");
  var mdim = document.querySelector(".mdim");
  /* Vorschaubilder im Menue (J2): erst beim ersten Oeffnen oder wenn der Knopf angesteuert wird (Maus, Fokus, Antippen) */
  var menuImgs = false;
  function loadMenuImgs() {
    if (menuImgs) return;
    menuImgs = true;
    Array.prototype.forEach.call(document.querySelectorAll(".msheet img[data-src]"), vsrc);
  }
  window.ADB_MENUIMG = loadMenuImgs;
  function toggleMenu() { loadMenuImgs(); document.body.classList.toggle("menuopen"); }
  function closeMenu() { document.body.classList.remove("menuopen"); }
  if (mbtn) mbtn.addEventListener("click", function () {
    document.body.classList.remove("filteropen");
    toggleMenu();
  });
  ["mouseenter", "focus", "pointerdown", "touchstart"].forEach(function (ev) {
    if (mbtn) mbtn.addEventListener(ev, loadMenuImgs, { passive: true });
  });
  /* der Knopf in der Kopfzeile (brand.js .hmenu) entsteht vor diesem Script */
  document.addEventListener("mouseover", function (e) { if (e.target.closest && e.target.closest(".hmenu")) loadMenuImgs(); }, { passive: true });
  document.addEventListener("focusin", function (e) { if (e.target.closest && e.target.closest(".hmenu, .msheet")) loadMenuImgs(); });
  if (mdim) mdim.addEventListener("click", closeMenu);
  /* Barrierefreiheit (B5): geschlossenes Menue ist inert (nicht per Tab erreichbar, fuer Screenreader weg),
     die Knoepfe tragen aria-expanded und aria-controls. Folgt body.menuopen, egal wer es setzt (Klick, Esc, Coach). */
  var msheet = document.querySelector(".msheet");
  if (msheet) {
    if (!msheet.id) msheet.id = "hauptmenue";
    var syncMenuA11y = function () {
      var open = document.body.classList.contains("menuopen");
      if (open) msheet.removeAttribute("inert"); else msheet.setAttribute("inert", "");
      document.querySelectorAll(".mbtn, .chrome .hmenu").forEach(function (b) {
        b.setAttribute("aria-controls", msheet.id);
        b.setAttribute("aria-expanded", open ? "true" : "false");
        b.setAttribute("aria-label", open ? "Menü schließen" : "Menü öffnen");
      });
    };
    syncMenuA11y();
    new MutationObserver(syncMenuA11y).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeMenu(); document.body.classList.remove("filteropen"); document.body.classList.remove("branchopen"); }
  });

  /* Filter-Kreise (Work): links Leistung, rechts Branche */
  var fbtn = document.querySelector(".fbtn");
  if (fbtn) {
    fbtn.addEventListener("click", function () {
      closeMenu();
      document.body.classList.remove("branchopen");
      document.body.classList.toggle("filteropen");
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".fbtn, .fpop")) document.body.classList.remove("filteropen");
    });
  }
  var bbtn = document.querySelector(".bbtn");
  if (bbtn) {
    bbtn.addEventListener("click", function () {
      closeMenu();
      document.body.classList.remove("filteropen");
      document.body.classList.toggle("branchopen");
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".bbtn, .bpop")) document.body.classList.remove("branchopen");
    });
  }

  /* Drag-Scroll fuer die Vorschau-Zeile */
  var mrow = document.querySelector(".mrow");
  if (mrow) {
    var down = false, startX = 0, startL = 0, moved = 0;
    mrow.addEventListener("pointerdown", function (e) {
      down = true; moved = 0; startX = e.clientX; startL = mrow.scrollLeft;
    });
    window.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - startX; moved = Math.max(moved, Math.abs(dx));
      mrow.scrollLeft = startL - dx;
    });
    window.addEventListener("pointerup", function () { down = false; });
    mrow.addEventListener("click", function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
  }

  /* ---------- Reveals (einmalig) ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("inview"); io.unobserve(en.target); }
    });
  }, { threshold: 0.18, rootMargin: "0px 0px -6% 0px" });
  document.querySelectorAll("[data-fade], [data-scale], [data-lines]").forEach(function (el) {
    io.observe(el);
  });
  /* Stagger-Indizes fuer Zeilen + Gruppen */
  document.querySelectorAll("[data-lines]").forEach(function (el) {
    el.querySelectorAll(".rl > span").forEach(function (s, i) { s.style.setProperty("--i", i); });
  });
  document.querySelectorAll("[data-stagger]").forEach(function (grp) {
    grp.querySelectorAll("[data-fade]").forEach(function (el, i) { el.style.setProperty("--i", i); });
  });

  /* ---------- Keyword-Scrub ---------- */
  var scrubs = [];
  document.querySelectorAll("[data-scrub]").forEach(function (p) {
    (function wrapWords(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (ch) {
        if (ch.nodeType === 3) {
          var frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(function (tok) {
            if (/^\s+$/.test(tok) || tok === "") { frag.appendChild(document.createTextNode(tok)); return; }
            var s = document.createElement("span");
            s.className = "w"; s.textContent = tok;
            frag.appendChild(s);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1) wrapWords(ch);
      });
    })(p);
    scrubs.push({ el: p, words: p.querySelectorAll(".w") });
  });

  /* ---------- Hintergrund-Morph + Chrome-Modus ---------- */
  var bgsecs = Array.prototype.slice.call(document.querySelectorAll("[data-bg]"));
  var lastBg = null;

  /* ---------- Drift-Parallax ---------- */
  var drifts = Array.prototype.slice.call(document.querySelectorAll("[data-drift]")).map(function (el) {
    return { el: el, s: parseFloat(el.getAttribute("data-drift")) || 0.1 };
  });
  /* Scrollbasierter Spalten-Parallax (0 am Seitenanfang, Vorlage Work-Grid) */
  var driftsSc = Array.prototype.slice.call(document.querySelectorAll("[data-driftsc]")).map(function (el) {
    return { el: el, s: parseFloat(el.getAttribute("data-driftsc")) || 0.05, cur: 0 };
  });
  /* traege Nachlauf-Bewegung: Spalten gleiten langsam in ihre Ziellage (Vorlage) */
  if (driftsSc.length && !reduced) (function glide(t) {
    var y = window.scrollY;
    driftsSc.forEach(function (d, i) {
      d.cur += (Math.min(y * d.s, 170) - d.cur) * 0.05;
      /* dauerhafte, kaum merkliche Eigenbewegung je Spalte */
      var idle = Math.sin((t || 0) * 0.00028 + i * 2.3) * 10;
      d.el.style.transform = "translateY(" + (d.cur + idle).toFixed(2) + "px)";
    });
    requestAnimationFrame(glide);
  })();


  /* ---------- Bild-Zoom-Uebergang ---------- */
  var zsecs = Array.prototype.slice.call(document.querySelectorAll(".zoomsec")).map(function (sec) {
    var m = sec.querySelector(".zmedia");
    var el = m ? m.querySelector("img, video") : null;
    /* Seitenverhaeltnis aus den Attributen, damit es schon vor dem Laden stimmt */
    var w = el ? +(el.getAttribute("width") || el.naturalWidth || el.videoWidth || 0) : 0;
    var h = el ? +(el.getAttribute("height") || el.naturalHeight || el.videoHeight || 0) : 0;
    var vid = m ? m.querySelector("video[data-scrub]") : null;
    if (vid) { vid.pause(); vid.muted = true; }
    return { sec: sec, media: m, side: sec.getAttribute("data-side") || "right",
             ar: (w && h) ? h / w : 0.63, vid: vid };
  });
  function easeZ(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function zoomTick() {
    zsecs.forEach(function (z) {
      var r = z.sec.getBoundingClientRect();
      var span = r.height - vh;
      var p = Math.max(0, Math.min(1, -r.top / span));
      var e = reduced ? 1 : easeZ(p);
      /* Scrollgebundenes Video: der Fortschritt der Sektion ist die Zeitachse (Apple-Muster) */
      if (z.vid && z.vid.duration && !z.vid.seeking) {
        var tt = p * z.vid.duration;
        if (Math.abs(tt - z.vid.currentTime) > 0.04) z.vid.currentTime = tt;
      }
      if (window.innerWidth <= 860) {
        /* Am Telefon waechst die Karte auf voll Breite, die Hoehe folgt dem Bild.
           Kein Vollbild-Beschnitt, sonst ist von einem breiten Screenshot nichts zu lesen.
           Hochformat wird an der Hoehe gedeckelt, damit es in die Buehne passt. */
        var wp = (76 + 24 * e) / 100 * window.innerWidth;
        var hp = Math.min(wp * z.ar, vh * 0.6);
        wp = Math.min(wp, hp / z.ar);
        z.media.style.width = wp + "px";
        z.media.style.height = hp + "px";
        z.media.style.left = ((window.innerWidth - wp) / 2) + "px";
        z.media.style.top = (vh * 0.68 - hp / 2) + "px";
        z.media.style.borderRadius = (3 * (1 - e)) + "px";
        z.sec.classList.toggle("zdone", p > 0.82);
        return;
      }
      var w0 = 34, h0 = 46, l0 = z.side === "right" ? 58 : 8;
      var w = w0 + (100 - w0) * e;
      var h = h0 + (100 - h0) * e;
      var l = l0 * (1 - e);
      var t = (100 - h) / 2;
      z.media.style.width = w + "vw";
      z.media.style.height = h + "vh";
      z.media.style.left = l + "vw";
      z.media.style.top = t + "vh";
      z.media.style.borderRadius = (3 * (1 - e)) + "px";
      z.sec.classList.toggle("zdone", p > 0.82);
    });
  }

  /* ---------- Prozess-Pfad ---------- */
  var proc = document.querySelector(".procgrid");
  var pfill = null, pbase = null, plen = 0, pnodes = [];
  function buildProc() {
    if (!proc) return;
    var svg = proc.querySelector(".procsvg");
    if (!svg) return;
    var gr = proc.getBoundingClientRect();
    pnodes = Array.prototype.slice.call(proc.querySelectorAll(".pnode"));
    var pts = pnodes.map(function (n) {
      var r = n.getBoundingClientRect();
      return { x: r.left + r.width / 2 - gr.left, y: r.top + r.height / 2 - gr.top };
    });
    if (pts.length < 2) return;
    var d = "M " + pts[0].x + " 0 L " + pts[0].x + " " + pts[0].y;
    for (var i = 1; i < pts.length; i++) {
      var a = pts[i - 1], b = pts[i];
      var midY = (a.y + b.y) / 2, bend = (i % 2 ? -1 : 1) * Math.min(150, gr.width * 0.10);
      d += " C " + a.x + " " + midY + ", " + (b.x + bend) + " " + midY + ", " + b.x + " " + b.y;
    }
    d += " L " + pts[pts.length - 1].x + " " + gr.height;
    svg.setAttribute("viewBox", "0 0 " + gr.width + " " + gr.height);
    pbase = svg.querySelector(".pbase"); pfill = svg.querySelector(".pfill");
    pbase.setAttribute("d", d); pfill.setAttribute("d", d);
    plen = pfill.getTotalLength();
    pfill.style.strokeDasharray = plen;
    pfill.style.strokeDashoffset = plen;
  }
  window.addEventListener("load", buildProc);
  window.addEventListener("resize", buildProc);
  function procTick() {
    if (!proc || !pfill || !plen) return;
    var r = proc.getBoundingClientRect();
    var p = Math.max(0, Math.min(1, (vh * 0.7 - r.top) / r.height));
    pfill.style.strokeDashoffset = plen * (1 - p);
    pnodes.forEach(function (n) {
      var nr = n.getBoundingClientRect();
      var frac = (nr.top + nr.height / 2 - r.top) / r.height;
      n.classList.toggle("on", p >= frac - 0.02);
    });
  }

  /* ---------- Akkordeon ---------- */
  document.querySelectorAll(".acc .ahead, .faq .ahead").forEach(function (h) {
    h.addEventListener("click", function () {
      var item = h.parentElement;
      var body = item.querySelector(".abody");
      var open = item.classList.contains("open");
      item.parentElement.querySelectorAll(".aitem.open").forEach(function (o) {
        o.classList.remove("open");
        o.querySelector(".abody").style.maxHeight = "0px";
      });
      if (!open) {
        item.classList.add("open");
        body.style.maxHeight = body.scrollHeight + "px";
      }
    });
  });

  /* ---------- Anfrage-Mechanik ---------- */
  var needbar = document.querySelector(".needbar");
  if (needbar) {
    var nsel = needbar.querySelector(".nsel");
    var ngo = needbar.querySelector(".ngo");
    var opts = document.querySelectorAll(".needgrid .nopt");
    function syncNeed() {
      var picked = Array.prototype.slice.call(nsel.querySelectorAll(".schip")).map(function (c) { return c.getAttribute("data-v"); });
      needbar.classList.toggle("ready", picked.length > 0);
      opts.forEach(function (o) { o.classList.toggle("sel", picked.indexOf(o.getAttribute("data-v")) >= 0); });
      return picked;
    }
    opts.forEach(function (o) {
      o.addEventListener("click", function () {
        var v = o.getAttribute("data-v");
        var existing = nsel.querySelector('.schip[data-v="' + v + '"]');
        if (existing) { existing.remove(); syncNeed(); return; }
        var c = document.createElement("button");
        c.className = "schip"; c.setAttribute("data-v", v);
        c.innerHTML = v + " <i>×</i>";
        c.addEventListener("click", function () { c.remove(); syncNeed(); });
        nsel.appendChild(c);
        syncNeed();
      });
    });
    /* Auswahl und Herkunft wandern in den Anfrage-Funnel auf kontakt.html */
    ngo.addEventListener("click", function () {
      var picked = syncNeed();
      if (!picked.length) return;
      var slug = (location.pathname.split("/").pop() || "index.html").replace(/\.html$/, "");
      /* Ziel aus dem Kontakt-Link der Kopfzeile: live schreibt _seo.py ihn auf /kontakt um (saubere Pfade) */
      var ctcEl = document.querySelector(".chrome .ctc"), kurl = (ctcEl && ctcEl.getAttribute("href")) || "kontakt.html";
      location.href = kurl + "?w=" + encodeURIComponent(picked.join(",")) +
                      "&from=" + encodeURIComponent(slug);
    });
  }


  /* ---------- Horizontaler Prozess ---------- */
  var hproc = document.querySelector(".hproc");
  var htrack = hproc ? hproc.querySelector(".htrack") : null;
  var hfill = hproc ? hproc.querySelector(".hlinefill") : null;
  function hprocTick() {
    if (!hproc || !htrack || window.innerWidth <= 900) return;
    var r = hproc.getBoundingClientRect();
    var span = r.height - vh;
    var p = Math.max(0, Math.min(1, -r.top / span));
    var over = htrack.scrollWidth - window.innerWidth;
    htrack.style.transform = "translateX(" + (-p * Math.max(0, over)) + "px)";
    if (hfill) hfill.style.width = (p * 115) + "%";
    var cards = htrack.querySelectorAll(".hcard");
    cards.forEach(function (cd, i) {
      cd.classList.toggle("on", p >= (i + 0.35) / cards.length);
    });
  }


  /* ---------- Differenzierungs-Split (BiA-Muster) ---------- */
  var dsec = document.querySelector(".diffsec");
  if (dsec) {
    var dnum = dsec.querySelector(".dnum");
    var dimgs = dsec.querySelectorAll(".dimg img");
    var dblocks = dsec.querySelectorAll(".dblock");
    var dio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var idx = Array.prototype.indexOf.call(dblocks, en.target);
        if (idx < 0) return;
        if (dnum) dnum.textContent = "0" + (idx + 1);
        dimgs.forEach(function (im, i) { im.classList.toggle("on", i === idx); });
      });
    }, { rootMargin: "-42% 0px -42% 0px" });
    dblocks.forEach(function (b) { dio.observe(b); });
  }


  /* ---------- Logo-Zyklus ---------- */
  document.querySelectorAll(".logocycle").forEach(function (wall) {
    var slots = Array.prototype.slice.call(wall.querySelectorAll(".lslot"));
    slots.forEach(function (slot) {
      var names = (slot.getAttribute("data-set") || "").split(",").filter(Boolean);
      names.forEach(function (n, i) {
        var im = document.createElement("img");
        im.src = "assets/logos/" + n + ".png"; im.alt = n; im.loading = "lazy";
        if (i === 0) im.classList.add("on");
        slot.appendChild(im);
      });
      slot._idx = 0;
    });
    if (reduced) return;
    var turn = 0;
    setInterval(function () {
      if (document.hidden) return;   /* im Hintergrund-Tab steht der Wechsel (S3) */
      var slot = slots[turn % slots.length];
      turn++;
      var imgs = slot.querySelectorAll("img");
      if (imgs.length < 2) return;
      imgs[slot._idx].classList.remove("on");
      slot._idx = (slot._idx + 1) % imgs.length;
      imgs[slot._idx].classList.add("on");
    }, 2200);
  });

  /* ---------- generisches Drag-Scrollen (Service-Zeile) ---------- */
  document.querySelectorAll(".svcrow").forEach(function (row) {
    var down = false, sx = 0, sl = 0, mv = 0;
    row.addEventListener("pointerdown", function (e) { down = true; mv = 0; sx = e.clientX; sl = row.scrollLeft; });
    window.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - sx; mv = Math.max(mv, Math.abs(dx));
      row.scrollLeft = sl - dx;
    });
    window.addEventListener("pointerup", function () { down = false; });
    row.addEventListener("click", function (e) { if (mv > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
  });


  /* ---------- Footer-Wortmarke exakt einpassen ---------- */
  var fwordEl = document.querySelector(".fword div");
  if (fwordEl) {
    var fitWord = function () {
      var box = fwordEl.parentElement.getBoundingClientRect();
      fwordEl.style.fontSize = "";
      var base = parseFloat(getComputedStyle(fwordEl).fontSize);
      var w = fwordEl.scrollWidth;
      var avail = box.width - 8;
      if (w > avail) fwordEl.style.fontSize = Math.floor(base * (avail / w)) + "px";
    };
    fitWord();
    window.addEventListener("resize", fitWord);
    window.addEventListener("load", fitWord);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitWord);
  }


  /* ---------- Videos: nur im Viewport abspielen ----------
     Quelle erst beim Sichtbarwerden (data-src setzt _perf.py), bei reduzierter Bewegung kein Autoplay, das Poster bleibt.
     Folien des Hero-Sliders startet die Hero-Rotation selbst, nur die aktive Folie spielt. */
  var vids = document.querySelectorAll("video[data-auto]");
  if (vids.length) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) {
          if (reduced) return;
          var sl = v.closest(".hslide");
          if (sl && !sl.classList.contains("on")) return;
          vplay(v);
        }
        else v.pause();
      });
    }, { threshold: 0.15 });
    vids.forEach(function (v) { vio.observe(v); });
  }

  /* ---------- Eingebetteter Film: Ton auf Klick ---------- */
  document.querySelectorAll(".filmwrap").forEach(function (wrap) {
    var v = wrap.querySelector("video");
    var btn = wrap.querySelector(".fplay");
    if (!v || !btn) return;
    btn.addEventListener("click", function () {
      wrap.classList.add("playing");
      v.muted = false;
      v.controls = true;
      var p = v.play(); if (p && p.catch) p.catch(function () {});
    });
    v.addEventListener("pause", function () { if (v.currentTime === 0) wrap.classList.remove("playing"); });
  });


  /* ---------- Sticky-Zahl mit Stationen (scrollgetrieben) ---------- */
  var tells = Array.prototype.slice.call(document.querySelectorAll(".tell")).map(function (box) {
    var t = {
      box: box,
      tv: box.querySelector(".tv"),
      tl: box.querySelector(".tl"),
      steps: Array.prototype.slice.call(box.querySelectorAll(".ts")),
      /* optionale Chips direkt davor: zeigen die Station an und springen hin */
      nav: Array.prototype.slice.call((box.parentElement || box).querySelectorAll(".tellnav .hn")),
      cur: -1
    };
    t.nav.forEach(function (b, i) {
      b.addEventListener("click", function () {
        var target = t.steps[i];
        if (!target) return;
        var y = target.getBoundingClientRect().top + window.pageYOffset - vh * 0.5 + target.offsetHeight / 2;
        window.scrollTo({ top: y, behavior: reduced ? "auto" : "smooth" });
      });
    });
    return t;
  }).filter(function (t) { return t.tv && t.steps.length; });

  function tellTick() {
    tells.forEach(function (t) {
      var line = vh * 0.5, best = 0, bestD = Infinity;
      t.steps.forEach(function (st, i) {
        var r = st.getBoundingClientRect();
        var d = Math.abs((r.top + r.height / 2) - line);
        if (d < bestD) { bestD = d; best = i; }
      });
      if (best === t.cur) return;
      t.cur = best;
      t.steps.forEach(function (st, i) { st.classList.toggle("on", i === best); });
      t.nav.forEach(function (b, i) { b.classList.toggle("on", i === best); });
      var act = t.steps[best];
      t.tv.style.opacity = 0; t.tl.style.opacity = 0;
      setTimeout(function () {
        t.tv.textContent = act.getAttribute("data-v");
        t.tl.textContent = act.getAttribute("data-l");
        t.tv.style.opacity = 1; t.tl.style.opacity = 1;
      }, MO.fast);
    });
  }

  /* ---------- Highlights-Stapel: Medium steht, Karten ziehen vorbei, Tabnav zeigt an und springt ---------- */
  var stacks = Array.prototype.slice.call(document.querySelectorAll(".hlxgrid")).map(function (box) {
    var st = {
      steps: Array.prototype.slice.call(box.querySelectorAll(".hs")),
      media: Array.prototype.slice.call(box.querySelectorAll(".hlxmedia > *")),
      nav: Array.prototype.slice.call(box.querySelectorAll(".hlxnav .hn")),
      cur: -1
    };
    st.nav.forEach(function (b, i) {
      b.addEventListener("click", function () {
        var target = st.steps[i];
        if (!target) return;
        var y = target.getBoundingClientRect().top + window.pageYOffset - vh * 0.5 + target.offsetHeight / 2;
        window.scrollTo({ top: y, behavior: reduced ? "auto" : "smooth" });
      });
    });
    return st;
  }).filter(function (s) { return s.steps.length; });
  function stackTick() {
    stacks.forEach(function (s) {
      var line = vh * 0.5, best = 0, bestD = Infinity;
      s.steps.forEach(function (st, i) {
        var r = st.getBoundingClientRect();
        var d = Math.abs((r.top + r.height / 2) - line);
        if (d < bestD) { bestD = d; best = i; }
      });
      if (best === s.cur) return;
      s.cur = best;
      s.steps.forEach(function (st, i) { st.classList.toggle("on", i === best); });
      s.nav.forEach(function (b, i) { b.classList.toggle("on", i === best); });
      s.media.forEach(function (m, i) {
        var on = i === best;
        m.classList.toggle("on", on);
        if (m.tagName === "VIDEO") { if (on) { vplay(m); } else { m.pause(); } }
      });
    });
  }

  /* ---------- Kapitel-Leiste: erscheint nach dem Hero, zeigt das Kapitel, springt per Klick ---------- */
  var chap = document.querySelector(".chapnav");
  var chapLinks = chap ? Array.prototype.slice.call(chap.querySelectorAll("a[href^='#']")) : [];
  var chapTargets = chapLinks.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
  var chapHero = document.querySelector(".chero, .svc-hero");
  chapLinks.forEach(function (a, i) {
    a.addEventListener("click", function (ev) {
      var t = chapTargets[i];
      if (!t) return;
      ev.preventDefault();
      window.scrollTo({ top: t.getBoundingClientRect().top + window.pageYOffset - 40, behavior: reduced ? "auto" : "smooth" });
    });
  });
  function chapTick() {
    if (!chap) return;
    var showAt = chapHero ? chapHero.offsetHeight * 0.6 : 400;
    chap.classList.toggle("show", window.pageYOffset > showAt);
    /* der Kaufknopf springt zwar, wird aber nie als Kapitel markiert */
    var cur = -1;
    chapTargets.forEach(function (t, i) { if (t && !chapLinks[i].classList.contains("cn-cta") && t.getBoundingClientRect().top <= vh * 0.45) cur = i; });
    chapLinks.forEach(function (a, i) { if (!a.classList.contains("cn-cta")) a.classList.toggle("on", i === cur); });
    /* dunkle Pille auf dunklem Grund: body.on-light setzt der Hintergrund-Tracker weiter unten */
    chap.classList.toggle("dark", !document.body.classList.contains("on-light"));
  }

  /* ---------- Prozess-Schema: Linien zeichnen sich mit dem Scroll, Knoten leuchten auf, danach laufen die Impulse ---------- */
  var pmaps = Array.prototype.slice.call(document.querySelectorAll(".pmap")).map(function (box) {
    var paths = Array.prototype.slice.call(box.querySelectorAll("path[data-draw]")).map(function (p) {
      var L = 0;
      try { L = p.getTotalLength(); } catch (e) { L = 0; }
      p.style.strokeDasharray = L + " " + L;
      p.style.strokeDashoffset = L;
      return { el: p, L: L, s: parseFloat(p.getAttribute("data-s")), e: parseFloat(p.getAttribute("data-e")) };
    });
    if (reduced) {
      Array.prototype.slice.call(box.querySelectorAll("svg")).forEach(function (sv) { if (sv.pauseAnimations) sv.pauseAnimations(); });
    }
    return { box: box, paths: paths, nodes: Array.prototype.slice.call(box.querySelectorAll(".pn[data-at]")), p: -1 };
  });
  /* SVG-Animationen (animateMotion, animate) laufen nur im Bild (S3): ausserhalb pausiert, bei reduzierter Bewegung nie */
  if ("IntersectionObserver" in window) {
    var smil = Array.prototype.filter.call(document.querySelectorAll("main svg"), function (sv) {
      return sv.pauseAnimations && sv.querySelector("animateMotion, animate, animateTransform");
    });
    if (smil.length && !reduced) {
      var sio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) e.target.unpauseAnimations(); else e.target.pauseAnimations(); });
      }, { rootMargin: "100px 0px" });
      smil.forEach(function (sv) { sv.pauseAnimations(); sio.observe(sv); });
    }
  }
  function pmapTick() {
    pmaps.forEach(function (m) {
      var r = m.box.getBoundingClientRect();
      /* 0, wenn das Schema unten auftaucht, 1, wenn gut die Haelfte durch ist */
      var p = reduced ? 1 : Math.max(0, Math.min(1, (vh * 0.92 - r.top) / (r.height * 0.55 + vh * 0.4)));
      if (Math.abs(p - m.p) < 0.002) return;
      m.p = p;
      m.paths.forEach(function (x) {
        var q = Math.max(0, Math.min(1, (p - x.s) / (x.e - x.s)));
        x.el.style.strokeDashoffset = x.L * (1 - q);
      });
      m.nodes.forEach(function (n) { n.classList.toggle("on", p >= parseFloat(n.getAttribute("data-at"))); });
      m.box.classList.toggle("live", p > 0.97);
    });
  }

  /* ---------- Viewer: Chips wechseln Medium und Caption ---------- */
  document.querySelectorAll(".viewer").forEach(function (v) {
    var chips = Array.prototype.slice.call(v.querySelectorAll(".vchips .vc"));
    var media = Array.prototype.slice.call(v.querySelectorAll(".vstage img, .vstage video"));
    var caps = Array.prototype.slice.call(v.querySelectorAll(".vcaps .vcap"));
    chips.forEach(function (c, i) {
      c.addEventListener("click", function () {
        chips.forEach(function (x, j) { x.classList.toggle("on", j === i); });
        media.forEach(function (x, j) { x.classList.toggle("on", j === i); });
        caps.forEach(function (x, j) { x.classList.toggle("on", j === i); });
      });
    });
  });

  /* ---------- Kanal-Zeilen (scrollgetrieben) ---------- */
  var chrows = Array.prototype.slice.call(document.querySelectorAll(".chrow")).map(function (el) {
    return { el: el, done: false };
  });
  function chrowTick() {
    chrows.forEach(function (c) {
      if (c.done) return;
      var r = c.el.getBoundingClientRect();
      if (r.top > vh * 0.85 || r.bottom < 0) return;
      c.done = true;
      c.el.querySelectorAll(".cf").forEach(function (f, i) {
        setTimeout(function () { f.style.width = f.getAttribute("data-w") + "%"; }, i * MO.stagger);
      });
    });
  }


  /* ---------- Vorher/Nachher-Balken (scrollgetrieben) ---------- */
  var bacmps = Array.prototype.slice.call(document.querySelectorAll(".bacmp")).map(function (el) {
    return { el: el, done: false };
  });
  function bacmpTick() {
    bacmps.forEach(function (b) {
      if (b.done) return;
      var r = b.el.getBoundingClientRect();
      if (r.top > vh * 0.85 || r.bottom < 0) return;
      b.done = true;
      b.el.querySelectorAll(".bfill").forEach(function (f, i) {
        setTimeout(function () { f.style.width = f.getAttribute("data-w") + "%"; }, i * MO.stagger * 2);
      });
    });
  }

  /* ---------- Ablauf-Zeilen (scrollgetrieben, in beide Richtungen) ---------- */
  var steprows = Array.prototype.slice.call(document.querySelectorAll(".oplist--steps .op"));
  function stepsTick() {
    for (var i = 0; i < steprows.length; i++) {
      var r = steprows[i].getBoundingClientRect();
      steprows[i].classList.toggle("on", (r.top + r.height * 0.5) < vh * 0.74 && r.bottom > 0);
    }
  }

  /* ---------- Sicherheitsnetz fuer Einblendungen ----------
     Am Telefon wird mit Schwung gescrollt. Der IntersectionObserver kann dabei Elemente
     verpassen, die in einem Frame durchs Bild fliegen, und dann bleibt Text unsichtbar.
     Deshalb im Scroll-Loop synchron nachziehen: alles, was oben im Blick war, wird sichtbar. */
  var pending = Array.prototype.slice.call(document.querySelectorAll("[data-fade], [data-scale], [data-lines]"));
  function revealSafety() {
    for (var i = pending.length - 1; i >= 0; i--) {
      var el = pending[i];
      if (el.classList.contains("inview")) { pending.splice(i, 1); continue; }
      var r = el.getBoundingClientRect();
      /* im Blick oder schon vorbei: beides heisst sichtbar */
      if (r.top < vh * 0.94) { el.classList.add("inview"); pending.splice(i, 1); }
    }
  }

  /* ---------- Bildband: Tippen haelt es an, damit man am Telefon lesen und den Ton treffen kann ---------- */
  document.querySelectorAll(".pwstage").forEach(function (st) {
    st.addEventListener("click", function (e) {
      if (e.target.closest(".ivsound")) return;   /* der Ton-Knopf regelt sich selbst */
      st.classList.toggle("pwpaused");
    });
  });

  /* ---------- Bildband: Tempo in Prozent der Fensterbreite je Sekunde, Dauer aus der Bandbreite ---------- */
  var tracks = Array.prototype.slice.call(document.querySelectorAll(".pwtrack, .svcbandtrack"));
  function trackDur() {
    for (var i = 0; i < tracks.length; i++) {
      var t = tracks[i], sp = parseFloat(t.parentNode.getAttribute("data-speed") || "6");
      /* Am Telefon sind die Bilder kleiner: gleiches Tempo in vw wirkt dort zaeh */
      if (window.innerWidth <= 860) sp *= 2;
      var w = t.getBoundingClientRect().width;
      if (w > 0) t.style.setProperty("--dur", (w / (window.innerWidth * sp / 100)).toFixed(1) + "s");
    }
  }
  if (tracks.length) {
    trackDur();
    window.addEventListener("load", trackDur);
    window.addEventListener("resize", trackDur);
    document.querySelectorAll(".pwtrack img, .pwtrack video").forEach(function (m) {
      m.addEventListener("load", trackDur); m.addEventListener("loadedmetadata", trackDur);
    });
    setTimeout(trackDur, 900);
  }

  /* ---------- Nutzen-Kacheln: eine nach der anderen, gesteuert vom Scrollfortschritt der ganzen Wand.
       Ueber die Position der einzelnen Kachel kaemen am Desktop drei gleichzeitig, also eine Rasterreihe. ---------- */
  var begrids = Array.prototype.slice.call(document.querySelectorAll(".benegrid")).map(function (g) {
    return { grid: g, cells: Array.prototype.slice.call(g.querySelectorAll(".bcell")) };
  });
  function bcellTick() {
    for (var g = 0; g < begrids.length; g++) {
      var b = begrids[g], n = b.cells.length;
      if (!n) continue;
      var r = b.grid.getBoundingClientRect();
      /* 0, wenn die Wand die Leselinie erreicht, 1, wenn sie oben durch ist */
      var p = reduced ? 1 : (vh * 0.9 - r.top) / (r.height + vh * 0.62);
      for (var i = 0; i < n; i++) {
        b.cells[i].classList.toggle("on", p >= (i + 0.6) / (n + 0.6) * 0.86);
      }
    }
  }

  /* ---------- Scroll-Loop ---------- */
  var vh = window.innerHeight;
  window.addEventListener("resize", function () { vh = window.innerHeight; });
  function onScroll() {
    /* Scrub */
    scrubs.forEach(function (s) {
      var r = s.el.getBoundingClientRect();
      var prog = (vh * 0.86 - r.top) / (r.height + vh * 0.42);
      prog = Math.max(0, Math.min(1, prog));
      var n = Math.round(prog * s.words.length);
      for (var i = 0; i < s.words.length; i++) {
        s.words[i].classList.toggle("on", i < n);
      }
    });
    /* Hintergrund */
    var line = vh * 0.55, active = null;
    for (var i = 0; i < bgsecs.length; i++) {
      var r2 = bgsecs[i].getBoundingClientRect();
      if (r2.top <= line && r2.bottom > line) { active = bgsecs[i]; break; }
    }
    if (active && active !== lastBg) {
      lastBg = active;
      document.body.style.backgroundColor = active.getAttribute("data-bg");
      document.body.classList.toggle("on-light", active.getAttribute("data-fg") === "dark");
    }
    /* Drift */
    drifts.forEach(function (d) {
      var r3 = d.el.getBoundingClientRect(), t0 = d.t || 0;
      var top = r3.top - t0, bot = r3.bottom - t0;
      var delta = (top + r3.height / 2) - vh / 2;
      var t = delta * d.s * -1;
      /* nie ueber die eigene Sektion hinaus: mindestens 48 px Luft zur Kante (Kundenhinweis 3.10.2026) */
      var sec = d.sec !== undefined ? d.sec : (d.sec = d.el.classList.contains("phcol") ? d.el.closest("section") : null);
      if (sec) {
        var sr = sec.getBoundingClientRect(), gap = 48;
        t = Math.max(t, sr.top + gap - top);
        t = Math.min(t, sr.bottom - gap - bot);
      }
      d.t = t;
      d.el.style.transform = "translateY(" + t + "px)";
    });
    zoomTick();
    procTick();
    hprocTick();
    tellTick();
    stackTick();
    chapTick();
    pmapTick();
    chrowTick();
    bacmpTick();
    stepsTick();
    bcellTick();
    revealSafety();
    ticking = false;
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("load", onScroll);
  setTimeout(onScroll, 60);
  setTimeout(onScroll, 700);
  setTimeout(onScroll, 1600);

  /* ---------- Hero-Rotation ---------- */
  var show = document.querySelector(".hshow");
  if (show) {
    var slides = show.querySelectorAll(".hslide");
    var dots = show.querySelectorAll(".hdots i");
    var idx = 0, HOLD = 4200, PRE = 1500, preT = 0;
    show.style.setProperty("--hd", HOLD + "ms");
    function svid(i) { return slides[i] ? slides[i].querySelector("video") : null; }
    /* naechste Folie: Quelle kurz vor dem Einsatz setzen und puffern lassen */
    function preload(i) {
      var v = svid(i);
      if (v && v.getAttribute("data-src")) { vsrc(v); v.preload = "auto"; }
    }
    function go(n) {
      var prev = idx;
      slides[idx].classList.remove("on");
      if (dots[idx]) dots[idx].classList.remove("on");
      idx = n % slides.length;
      slides[idx].classList.add("on");
      if (dots[idx]) {
        dots[idx].classList.remove("on");
        void dots[idx].offsetWidth;
        dots[idx].classList.add("on");
      }
      var v = svid(idx), pv = svid(prev);
      var hr = show.getBoundingClientRect();
      if (v && !reduced && hr.bottom > 0 && hr.top < window.innerHeight) vplay(v);
      /* die alte Folie haelt erst nach der Ueberblendung an */
      if (pv && pv !== v) setTimeout(function () { if (!slides[prev].classList.contains("on")) pv.pause(); }, MO.chor);
      clearTimeout(preT);
      if (!reduced && slides.length > 1) preT = setTimeout(function () { preload((idx + 1) % slides.length); }, Math.max(0, HOLD - PRE));
      if (window.ADB_MBTICK_POKE) window.ADB_MBTICK_POKE();
    }
    go(0);
    /* im Hintergrund-Tab steht die Rotation (S3) */
    if (!reduced && slides.length > 1) setInterval(function () { if (!document.hidden) go(idx + 1); }, HOLD);
    dots.forEach(function (d, i) { d.addEventListener("click", function () { preload(i); go(i); }); });
  }

  /* ---------- Work-Filter (FLIP) ---------- */
  var chips = document.querySelectorAll(".fchip");
  if (chips.length) {
    var allTiles = Array.prototype.slice.call(document.querySelectorAll(".wgrid .tile, .wgridw .wt"));
    var sel = { cat: "alle", branche: "alle" };
    function tileMatches(t) {
      var cats = (t.getAttribute("data-cat") || "").split(" ");
      var brs = (t.getAttribute("data-branche") || "").split(" ");
      return (sel.cat === "alle" || cats.indexOf(sel.cat) >= 0) &&
             (sel.branche === "alle" || brs.indexOf(sel.branche) >= 0);
    }
    function applyFilter() {
      var first = new Map();
      allTiles.forEach(function (t) {
        if (!t.classList.contains("fout")) first.set(t, t.getBoundingClientRect());
      });
      allTiles.forEach(function (t) { t.classList.toggle("fout", !tileMatches(t)); });
      allTiles.forEach(function (t) {
        if (t.classList.contains("fout")) return;
        var f = first.get(t), l = t.getBoundingClientRect();
        if (!f) {
          /* neu dazukommende Kachel: dasselbe Einblenden wie ueberall */
          t.animate([{ opacity: 0, transform: "translateY(24px)" }, { opacity: 1, transform: "none" }],
            { duration: MO.base, easing: MO.ease });
          return;
        }
        var dx = f.left - l.left, dy = f.top - l.top;
        if (dx || dy) t.animate(
          [{ transform: "translate(" + dx + "px," + dy + "px)" }, { transform: "none" }],
          { duration: MO.slow, easing: MO.ease }
        );
      });
    }
    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        var inBranch = !!chip.closest(".bpop");
        var scope = inBranch ? chip.closest(".bpop") : chip.closest(".fpop");
        if (scope) {
          scope.querySelectorAll(".fchip").forEach(function (c) { c.classList.remove("on"); });
        }
        chip.classList.add("on");
        if (inBranch) sel.branche = chip.getAttribute("data-branche");
        else sel.cat = chip.getAttribute("data-cat");
        applyFilter();
      });
    });
  }

  /* ---------- Tile → Hero Expansion (FLIP zur Case-Seite) ---------- */
  document.querySelectorAll("a[data-flip]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      var href = a.getAttribute("href");
      if (reduced) { location.href = href; return; }
      var img = a.querySelector("img"), vid = a.querySelector("video");
      var r = a.getBoundingClientRect();
      var x = document.createElement("div");
      x.className = "flipx";
      var src = img ? (img.currentSrc || img.src) : (vid && vid.poster ? vid.poster : "");
      if (src) x.style.backgroundImage = "url('" + src + "')";
      else x.style.background = getComputedStyle(a.querySelector(".wclr") || a).backgroundColor;
      /* Rueckweg: die Case-Seite kennt so ihre Kachel und schrumpft dorthin zurueck */
      var rad = getComputedStyle(a).borderRadius;
      try { sessionStorage.setItem("adbflipFrom", JSON.stringify({ href: href, radius: rad, rect: { top: r.top, left: r.left, width: r.width, height: r.height } })); } catch (err) {}
      x.style.borderRadius = rad;
      x.style.top = r.top + "px"; x.style.left = r.left + "px";
      x.style.width = r.width + "px"; x.style.height = r.height + "px";
      document.body.appendChild(x);
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          x.style.top = "0px"; x.style.left = "0px";
          x.style.width = "100vw"; x.style.height = "100vh";
          x.style.borderRadius = "0";
          setTimeout(function () {
            sessionStorage.setItem("adbflip", "1");
            location.href = href;
          }, MO.slow);
        });
      });
    });
  });
})();

/* ============================================================
   Anfrage-Funnel auf kontakt.html
   Die Vorauswahl kommt per URL von der Leistungsseite mit.
   ============================================================ */
(function () {
  var root = document.querySelector(".ksec");
  if (!root) return;

  var steps = Array.prototype.slice.call(root.querySelectorAll(".kstep"));
  var progs = Array.prototype.slice.call(root.querySelectorAll(".kprog .kp"));
  var bar = root.querySelector(".kprog .kbar i");
  var chips = Array.prototype.slice.call(root.querySelectorAll(".kchip"));
  var opts = Array.prototype.slice.call(root.querySelectorAll(".kopt"));
  var free = root.querySelector("#kfree");
  var sumBody = root.querySelector(".ksumbody");
  var sendBtn = root.querySelector(".ksend");
  var nextBtns = Array.prototype.slice.call(root.querySelectorAll(".knext"));

  var SEITEN = {
    "service-performance-marketing": "Performance Marketing",
    "service-ecommerce": "E-Commerce Growth",
    "service-content-creation": "Content Creation",
    "service-websites": "Websites & Landingpages",
    "service-strategie": "Strategie & Funnel",
    "service-chatgpt-ads": "ChatGPT Ads",
    "work": "Work",
    "index": "Startseite"
  };

  /* ---- Vorauswahl aus der URL ---- */
  var q = new URLSearchParams(location.search);
  var pre = (q.get("w") || "").split(",").map(function (x) { return x.trim(); }).filter(Boolean);
  pre.forEach(function (v) {
    var hit = chips.filter(function (c) { return c.getAttribute("data-v").toLowerCase() === v.toLowerCase(); })[0];
    if (hit) { hit.classList.add("sel"); return; }
    /* unbekannter Wunsch: als eigener Chip anhaengen, damit nichts verloren geht */
    var box = root.querySelector(".kchips");
    if (!box) return;
    var b = document.createElement("button");
    b.className = "kchip sel"; b.type = "button"; b.setAttribute("data-v", v);
    b.innerHTML = v + ' <span class="kx">+</span>';
    box.appendChild(b); chips.push(b);
    b.addEventListener("click", onChip);
  });
  var from = q.get("from");
  if (from && SEITEN[from]) {
    var fb = root.querySelector(".kfrom");
    if (fb) { fb.querySelector(".kfromname").textContent = SEITEN[from]; fb.hidden = false; }
  }

  /* ---- Auswahl ---- */
  function onChip() { this.classList.toggle("sel"); sync(); }
  chips.forEach(function (c) { c.addEventListener("click", onChip); });
  opts.forEach(function (o) {
    o.addEventListener("click", function () {
      var grp = o.getAttribute("data-g");
      root.querySelectorAll('.kopt[data-g="' + grp + '"]').forEach(function (x) {
        if (x !== o) x.classList.remove("sel");
      });
      o.classList.toggle("sel");
      sync();
    });
  });
  if (free) free.addEventListener("input", sync);

  function picked() { return chips.filter(function (c) { return c.classList.contains("sel"); })
                                  .map(function (c) { return c.getAttribute("data-v"); }); }
  function val(id) { var e = root.querySelector(id); return e ? e.value.trim() : ""; }
  function opt(g) { var e = root.querySelector('.kopt[data-g="' + g + '"].sel'); return e ? e.getAttribute("data-v") : ""; }

  function sync() {
    var ok = picked().length > 0 || val("#kfree").length > 2;
    nextBtns.forEach(function (b) { if (b.getAttribute("data-to") === "2") b.disabled = !ok; });
    if (sendBtn) sendBtn.disabled = !/.+@.+\..+/.test(val("#kmail"));
    if (!sumBody) return;
    var w = picked(); var extra = val("#kfree");
    /* Eingaben nur als Text einsetzen (textContent), nie als HTML */
    var lines = [];
    lines.push(["Womit:", w.length ? w.join(", ") + (extra ? ", " + extra : "") : null, extra]);
    var firm = val("#kfirm"), goal = val("#kgoal"), b = opt("budget"), wn = opt("when");
    if (firm) lines.push(["Projekt:", firm]);
    if (goal) lines.push(["Ziel:", goal]);
    if (b) lines.push(["Mediabudget:", b]);
    if (wn) lines.push(["Zeitpunkt:", wn]);
    var nm = val("#kname"), ml = val("#kmail"), ph = val("#kphone");
    if (nm || ml || ph) lines.push(["Kontakt:", [nm, ml, ph].filter(Boolean).join(", ")]);
    sumBody.textContent = "";
    lines.forEach(function (ln, i) {
      if (i) sumBody.appendChild(document.createElement("br"));
      var bb = document.createElement("b"); bb.textContent = ln[0];
      sumBody.appendChild(bb);
      sumBody.appendChild(document.createTextNode(" "));
      if (ln[1] === null) {
        /* noch keine Auswahl: Platzhalter wie bisher, ein frei getippter Wunsch steht dahinter */
        var em = document.createElement("span"); em.className = "kempty"; em.textContent = "noch offen";
        sumBody.appendChild(em);
        if (ln[2]) sumBody.appendChild(document.createTextNode(", " + ln[2]));
      } else sumBody.appendChild(document.createTextNode(ln[1]));
    });
  }
  root.querySelectorAll(".kinput").forEach(function (i) { i.addEventListener("input", sync); });

  /* ---- Schrittwechsel ---- */
  function go(n, quiet) {
    steps.forEach(function (s) { s.classList.toggle("on", s.getAttribute("data-s") === String(n)); });
    progs.forEach(function (p) {
      var v = parseInt(p.getAttribute("data-s"), 10);
      p.classList.toggle("on", v === n);
      p.classList.toggle("done", v < n);
    });
    if (bar) bar.style.width = Math.min(100, n * 33.4) + "%";
    if (quiet) return;                       /* beim Start nicht scrollen */
    var anchor = root.querySelector(".kprog");
    var top = (anchor || root).getBoundingClientRect().top + window.scrollY - 110;
    window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
  }
  root.querySelectorAll(".knext, .kback").forEach(function (b) {
    b.addEventListener("click", function () { go(parseInt(b.getAttribute("data-to"), 10)); });
  });

  /* ---- Absenden ----
     Zuerst POST an /api/anfrage (Vercel Function, Versand ueber Resend). Antwortet der Endpunkt nicht mit ok
     (Fehler, keine Konfiguration, GitHub-Pages-Vorschau ohne Endpunkt), oeffnet sich wie bisher das Mailprogramm.
     Danach ein dataLayer-Ereignis "lead" (nur wenn GTM nach Einwilligung geladen ist). */
  var sending = false;
  function leadEvent(via) {
    if (window.dataLayer && window.__adbTrack) window.dataLayer.push({ event: "lead", lead_via: via, lead_from: (from && SEITEN[from]) || "" });
  }
  function mailto() {
    var w = picked(); var extra = val("#kfree");
    var subject = "Anfrage: " + (w.length ? w.join(", ") : (extra || "Projekt"));
    var t = [];
    t.push("Hallo ad.boutique,");
    t.push("");
    t.push("wir brauchen Unterstuetzung bei: " + (w.length ? w.join(", ") : "") + (extra ? (w.length ? ", " : "") + extra : ""));
    if (val("#kfirm")) t.push("Unternehmen/Projekt: " + val("#kfirm"));
    if (val("#kgoal")) t.push("Was sich aendern soll: " + val("#kgoal"));
    if (opt("budget")) t.push("Monatliches Mediabudget: " + opt("budget"));
    if (opt("when")) t.push("Zeitpunkt: " + opt("when"));
    if (from && SEITEN[from]) t.push("Gekommen ueber: " + SEITEN[from]);
    t.push("");
    t.push([val("#kname"), val("#kmail"), val("#kphone")].filter(Boolean).join(", "));
    location.href = "mailto:hello@ad.boutique?subject=" + encodeURIComponent(subject) +
                    "&body=" + encodeURIComponent(t.join("\n"));
    leadEvent("mailto");
    setTimeout(function () { go(4); }, 400);
  }
  function sent() {
    /* Bestaetigung fuer den Versand ueber den Endpunkt: Texte stehen im Markup (data-ok-h, data-ok-t, _gen_kontakt.py) */
    var done = root.querySelector('.kstep[data-s="4"]');
    if (done && done.getAttribute("data-ok-h")) {
      var hh = done.querySelector(".kh"), tt = done.querySelector(".kt");
      if (hh) hh.textContent = done.getAttribute("data-ok-h");
      if (tt) tt.textContent = done.getAttribute("data-ok-t") || "";
    }
    leadEvent("api");
    go(4);
  }
  if (sendBtn) sendBtn.addEventListener("click", function () {
    if (sending) return;
    var w = picked(); var extra = val("#kfree");
    var data = {
      wahl: (w.length ? w.join(", ") : "") + (extra ? (w.length ? ", " : "") + extra : ""),
      projekt: val("#kfirm"), ziel: val("#kgoal"), budget: opt("budget"), zeitpunkt: opt("when"),
      herkunft: (from && SEITEN[from]) || "", name: val("#kname"), mail: val("#kmail"), telefon: val("#kphone"),
      website: val("#kweb")
    };
    if (!window.fetch || location.protocol === "file:") { mailto(); return; }
    sending = true; sendBtn.disabled = true;
    var ctl = window.AbortController ? new AbortController() : null;
    /* kurz halten: das Mailprogramm darf der Browser nur kurz nach dem Klick oeffnen (Nutzergeste) */
    var to = setTimeout(function () { if (ctl) ctl.abort(); }, 4000);
    fetch("/api/anfrage", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { return r.ok ? r.json() : { ok: false }; })
      .catch(function () { return { ok: false }; })
      .then(function (res) {
        clearTimeout(to); sending = false; sync();
        if (res && res.ok) sent(); else mailto();
      });
  });

  sync();
  go(1, true);
})();

/* ============================================================
   Interview im Hochformat: laeuft stumm, Ton per Klick
   ============================================================ */
(function () {
  var frame = document.querySelector(".pwiv") || document.querySelector(".ivframe");
  if (!frame) return;
  var v = frame.querySelector(".ivplayer");
  var btn = frame.querySelector(".ivsound");
  var lab = btn ? btn.querySelector(".ivlabel") : null;
  if (!v || !btn) return;

  btn.addEventListener("click", function () {
    var an = v.muted;
    if (an) {
      /* andere Tonquellen auf der Seite zuerst stumm schalten */
      document.querySelectorAll("video").forEach(function (o) {
        if (o !== v && !o.muted) { o.muted = true; o.pause(); }
      });
      document.querySelectorAll(".filmwrap.playing").forEach(function (w) { w.classList.remove("playing"); });
      v.muted = false;
      if (window.ADB_VSRC) window.ADB_VSRC(v);
      v.play().catch(function () {});
    } else {
      v.muted = true;
    }
    frame.classList.toggle("sound", !v.muted);
    btn.setAttribute("aria-label", v.muted ? "Ton einschalten" : "Ton ausschalten");
    if (lab) lab.textContent = v.muted ? "Ton an" : "Ton aus";
    /* laeuft das Interview in einem Bildband, haelt das Band beim Zuhoeren an */
    var st = frame.closest(".pwstage");
    if (st) st.classList.toggle("pwpaused", !v.muted);
  });

  /* laeuft das Video aus dem Bild, geht der Ton wieder aus */
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting && !v.muted) {
          v.muted = true;
          frame.classList.remove("sound");
          if (lab) lab.textContent = "Ton an";
        }
      });
    }, { threshold: 0.25 }).observe(frame);
  }
})();

/* ============================================================
   Einwilligung (J4): schlankes Banner unten links, zwei gleichwertige Knoepfe.
   Live (window.ADB_TRACK kommt aus dem Kopf, gesetzt von _seo.py mit ADB_LIVE=1): erscheint, solange keine Wahl
   gespeichert ist. Vorschau: nur mit ?consent=1. Erneut oeffnen: Footer-Link "Cookie-Einstellungen" (data-consent-open).
   Wahl in localStorage "adb_consent": "all" laedt GTM und Meta-Pixel (ADB_TRACK), "necessary" laedt nichts.
   ============================================================ */
(function () {
  var KEY = "adb_consent";
  var live = typeof window.ADB_TRACK === "function";
  var stored = null;
  try { stored = localStorage.getItem(KEY); } catch (e) {}
  var box = null, opener = null;

  function build() {
    box = document.createElement("div");
    box.className = "consent";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "false");
    box.setAttribute("aria-labelledby", "consent-t");
    var p = document.createElement("p");
    p.className = "consent-t"; p.id = "consent-t";
    p.appendChild(document.createTextNode("Darf ad.boutique messen? Mit Ihrer Zustimmung laden wir Google Tag Manager und das Meta-Pixel, um zu sehen, welche Kampagnen wirken. Ohne Zustimmung speichern wir nur Ihre Auswahl. "));
    var a = document.createElement("a");
    a.href = "https://www.ad.boutique/datenschutz"; a.target = "_blank"; a.rel = "noopener"; a.textContent = "Datenschutz";
    p.appendChild(a);
    var row = document.createElement("div");
    row.className = "consent-b";
    [["all", "Alle akzeptieren"], ["necessary", "Nur notwendige"]].forEach(function (b) {
      var btn = document.createElement("button");
      btn.type = "button"; btn.className = "btn btn--inverse"; btn.setAttribute("data-consent", b[0]); btn.textContent = b[1];
      btn.addEventListener("click", function () { decide(b[0]); });
      row.appendChild(btn);
    });
    box.appendChild(p); box.appendChild(row);
    document.body.appendChild(box);
  }
  function open(focus) {
    if (!box) build();
    box.classList.add("on");
    window.ADB_CONSENT_OPEN = true;
    if (focus) { var f = box.querySelector("button"); if (f) f.focus(); }
  }
  function close() {
    if (!box) return;
    box.classList.remove("on");
    window.ADB_CONSENT_OPEN = false;
    try { document.dispatchEvent(new CustomEvent("adbconsent")); } catch (e) {}
    if (opener && opener.focus) opener.focus();
    opener = null;
  }
  function decide(v) {
    try { localStorage.setItem(KEY, v); localStorage.setItem(KEY + "_t", new Date().toISOString().slice(0, 10)); } catch (e) {}
    if (v === "all" && window.ADB_TRACK) window.ADB_TRACK();
    if (v !== "all" && stored === "all" && window.ADB_UNTRACK) window.ADB_UNTRACK();
    stored = v;
    close();
  }
  document.addEventListener("click", function (e) {
    var t = e.target.closest && e.target.closest("[data-consent-open]");
    if (!t) return;
    e.preventDefault();
    opener = t;
    open(true);
  });
  if ((live && !stored) || /[?&]consent=1(&|$)/.test(location.search)) {
    /* erst nach der Ladeblende, damit es nicht hinter ihr aufgeht */
    var show = function () { open(false); };
    if (document.body.classList.contains("loaded")) show();
    else {
      var mo = new MutationObserver(function () { if (document.body.classList.contains("loaded")) { mo.disconnect(); show(); } });
      mo.observe(document.body, { attributes: true, attributeFilter: ["class"] });
    }
  }
})();
}

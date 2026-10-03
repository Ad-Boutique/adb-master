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
    /* Vergleich ueber den aufgeloesten Pfad: gilt fuer case-x.html (Vorschau) und /referenzen/x (live) */
    var same = false; try { same = !!saved && new URL(saved.href, location.href).pathname === location.pathname; } catch (err) {}
    var rect = (same || (saved && saved.href === me)) && saved.rect ? saved.rect : null;
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

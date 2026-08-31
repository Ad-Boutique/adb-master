/* ad.boutique Master · Engine
   Cursor, Menue-Sheet, Reveals, Keyword-Scrub, Hero-Rotation,
   Hintergrund-Morph, Drift-Parallax, Filter-FLIP, Tile-Expansion,
   Page-Transitions. Kein Framework, keine Abhaengigkeiten. */
(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var docEl = document.documentElement;

  /* ---------- Page-Transition ---------- */
  var pt = document.querySelector(".pt");
  /* Kam die Navigation aus der Tile-Expansion, sofort ohne schwarze Blende starten */
  if (pt && sessionStorage.getItem("adbflip")) {
    sessionStorage.removeItem("adbflip");
    pt.style.transition = "none";
    pt.classList.add("gone");
    requestAnimationFrame(function () { pt.style.transition = ""; });
  }
  function enterPage() {
    document.body.classList.add("loaded");
    if (!pt) return;
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { pt.classList.add("gone"); });
    });
  }
  window.addEventListener("load", enterPage);
  setTimeout(enterPage, 1400); /* Fallback, falls load haengt */

  function leaveTo(href) {
    if (reduced || !pt) { location.href = href; return; }
    pt.classList.remove("gone");
    pt.classList.add("enter");
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        pt.classList.add("cover");
        setTimeout(function () { location.href = href; }, 520);
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
    e.preventDefault();
    closeMenu();
    leaveTo(href);
  });

  /* ---------- Cursor ---------- */
  if (window.matchMedia("(pointer: fine)").matches) {
    var cur = document.createElement("div");
    cur.className = "cur";
    document.body.appendChild(cur);
    var cx = -100, cy = -100, tx = -100, ty = -100;
    document.addEventListener("mousemove", function (e) { tx = e.clientX; ty = e.clientY; });
    (function curLoop() {
      cx += (tx - cx) * 0.22; cy += (ty - cy) * 0.22;
      cur.style.transform = "translate(" + cx + "px," + cy + "px)" +
        (document.body.classList.contains("cur-hov") ? " scale(1.9)" : "");
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
  function toggleMenu() { document.body.classList.toggle("menuopen"); }
  function closeMenu() { document.body.classList.remove("menuopen"); }
  if (mbtn) mbtn.addEventListener("click", function () {
    document.body.classList.remove("filteropen");
    toggleMenu();
  });
  if (mdim) mdim.addEventListener("click", closeMenu);
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
    return { sec: sec, media: sec.querySelector(".zmedia"), side: sec.getAttribute("data-side") || "right" };
  });
  function easeZ(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
  function zoomTick() {
    zsecs.forEach(function (z) {
      var r = z.sec.getBoundingClientRect();
      var span = r.height - vh;
      var p = Math.max(0, Math.min(1, -r.top / span));
      var e = reduced ? 1 : easeZ(p);
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
  document.querySelectorAll(".acc .ahead").forEach(function (h) {
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
    ngo.addEventListener("click", function () {
      var picked = syncNeed();
      if (!picked.length) return;
      var subject = encodeURIComponent("Anfrage: " + picked.join(", "));
      var body = encodeURIComponent("Hallo ad.boutique,\n\nwir brauchen Unterstützung bei: " + picked.join(", ") + ".\n\nUnser Shop/Projekt: \nMonatsumsatz (ca.): \nZiel: ");
      location.href = "mailto:hello@ad.boutique?subject=" + subject + "&body=" + body;
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


  /* ---------- Videos: nur im Viewport abspielen ---------- */
  var vids = document.querySelectorAll("video[data-auto]");
  if (vids.length) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
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
      var r3 = d.el.getBoundingClientRect();
      var delta = (r3.top + r3.height / 2) - vh / 2;
      d.el.style.transform = "translateY(" + (delta * d.s * -1) + "px)";
    });
    zoomTick();
    procTick();
    hprocTick();
    ticking = false;
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("load", onScroll);
  setTimeout(onScroll, 60);

  /* ---------- Hero-Rotation ---------- */
  var show = document.querySelector(".hshow");
  if (show) {
    var slides = show.querySelectorAll(".hslide");
    var dots = show.querySelectorAll(".hdots i");
    var idx = 0, HOLD = 4200;
    show.style.setProperty("--hd", HOLD + "ms");
    function go(n) {
      slides[idx].classList.remove("on");
      if (dots[idx]) dots[idx].classList.remove("on");
      idx = n % slides.length;
      slides[idx].classList.add("on");
      if (dots[idx]) {
        dots[idx].classList.remove("on");
        void dots[idx].offsetWidth;
        dots[idx].classList.add("on");
      }
    }
    go(0);
    if (!reduced && slides.length > 1) setInterval(function () { go(idx + 1); }, HOLD);
    dots.forEach(function (d, i) { d.addEventListener("click", function () { go(i); }); });
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
          t.animate([{ opacity: 0, transform: "translateY(20px)" }, { opacity: 1, transform: "none" }],
            { duration: 500, easing: "cubic-bezier(0.19,1,0.22,1)" });
          return;
        }
        var dx = f.left - l.left, dy = f.top - l.top;
        if (dx || dy) t.animate(
          [{ transform: "translate(" + dx + "px," + dy + "px)" }, { transform: "none" }],
          { duration: 600, easing: "cubic-bezier(0.76,0,0.24,1)" }
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
      var img = a.querySelector("img");
      var r = (img || a).getBoundingClientRect();
      var x = document.createElement("div");
      x.className = "flipx";
      x.style.backgroundImage = "url('" + (img ? img.currentSrc || img.src : "") + "')";
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
          }, 700);
        });
      });
    });
  });
})();

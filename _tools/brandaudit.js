// Brand-Audit nach _intern/BRAND-RULES.md. Laeuft als Rumpf einer async-Funktion:
//   _tools/aprobe "<url>?coach=0" 1440 900 _tools/brandaudit.js 3 240
// Gibt JSON zurueck: je Pruefgruppe eine Liste von Befunden (gruppiert nach Ursache) plus Messwerte.
// Optionen ueber window.BA_OPT vor dem Lauf (z. B. {scan:false} ohne Scroll-Durchlauf).
const OPT = Object.assign({ scan: true, step: 0.6, pause: 650 }, window.BA_OPT || {});
const sl = (ms) => new Promise((r) => setTimeout(r, ms));
const W = document.documentElement.clientWidth, H = innerHeight, MOB = W < 768, DESK = W >= 1400;
const PAGE = location.pathname.split("/").pop() || "index.html";
const out = { page: PAGE, w: W, findings: {}, info: {} };
// Schutz: wenn ein eigenes Stylesheet nicht geladen ist (z. B. Server unter Last), ist jede Messung wertlos
// unter Last kommen Stylesheets verspaetet an: bis zu 12 s warten, bevor abgebrochen wird
for (let k = 0; k < 24; k++) {
  const a0 = document.querySelector("a.btn");
  const ok = /satoshi/i.test(getComputedStyle(document.body).fontFamily) && !(a0 && getComputedStyle(a0).color === "rgb(0, 0, 238)") && Array.from(document.querySelectorAll('link[rel="stylesheet"]')).filter((l) => /\/assets\//.test(l.href)).every((l) => { try { return l.sheet && l.sheet.cssRules.length > 0; } catch (e) { return false; } });
  if (ok) break; await sl(500);
}
{
  const bad = [];
  for (const l of document.querySelectorAll('link[rel="stylesheet"]')) {
    if (!/\/assets\//.test(l.href)) continue;
    let n = -1; try { n = l.sheet ? l.sheet.cssRules.length : -1; } catch (e) { n = -1; }
    if (n < 1) bad.push(l.href.split("/").pop());
  }
  // zweite Absicherung: Grundregeln aus master.css muessen greifen (sonst Browser-Standard: Linkblau, graue Knoepfe)
  if (!/satoshi/i.test(getComputedStyle(document.body).fontFamily)) bad.push("body-ohne-Satoshi");
  const a0 = document.querySelector("a.btn"); if (a0 && getComputedStyle(a0).color === "rgb(0, 0, 238)") bad.push("btn-linkblau");
  if (bad.length) return JSON.stringify({ page: PAGE, w: W, abort: "CSS-NICHT-GELADEN " + bad.join(","), findings: {}, info: {} });
}
function add(key, el, msg) {
  const f = (out.findings[key] = out.findings[key] || { n: 0, samples: [] });
  f.n++;
  const s = (el ? sel(el) + " " : "") + (msg || "");
  if (f.samples.length < 8 && !f.samples.includes(s)) f.samples.push(s);
}
function info(key, v) { (out.info[key] = out.info[key] || []).push(v); }
function sel(el) {
  if (!el || !el.tagName) return String(el);
  const one = (e) => e.tagName.toLowerCase() + (e.id ? "#" + e.id : "") + (e.classList && e.classList.length ? "." + Array.from(e.classList).slice(0, 3).join(".") : "");
  let s = one(el), p = el.parentElement, k = 0;
  while (p && k < 2 && p !== document.body) { s = one(p) + ">" + s; p = p.parentElement; k++; }
  return s;
}
// ---------- Farben ----------
const TOK = { cream: [244, 243, 235], black: [16, 16, 16], lime: [205, 255, 0], stone: [183, 183, 179], ph: [222, 221, 212] };
function cols(str) {
  const r = [], re = /rgba?\(([^)]+)\)/g; let m;
  while ((m = re.exec(str || ""))) {
    const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(parseFloat);
    r.push({ r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1, s: m[0] });
  }
  return r;
}
function tokOf(c) {
  for (const k in TOK) { const t = TOK[k]; if (Math.abs(c.r - t[0]) <= 2 && Math.abs(c.g - t[1]) <= 2 && Math.abs(c.b - t[2]) <= 2) return k; }
  return null;
}
const isLime = (c) => c && c.a > 0.3 && tokOf(c) === "lime";
function judge(c, prop) {
  if (c.a === 0) return "ok";
  const t = tokOf(c);
  if (t) return "ok";
  if (c.r >= 250 && c.g >= 250 && c.b >= 250) return /shadow/.test(prop) && c.a <= 0.2 ? "ok" : "white";
  if (c.r === 0 && c.g === 0 && c.b === 0 && /shadow|gradient/.test(prop) && c.a < 1) return "ok";
  return "foreign";
}
function vis(el) {
  const r = el.getBoundingClientRect();
  if (r.width < 1 || r.height < 1) return false;
  if (el.checkVisibility) return el.checkVisibility({ opacityProperty: true, visibilityProperty: true });
  const cs = getComputedStyle(el);
  return cs.visibility !== "hidden" && cs.display !== "none" && parseFloat(cs.opacity) > 0;
}
function ownText(el) {
  for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) return n.textContent.trim();
  return "";
}
function bgOf(el) {
  let e = el;
  while (e && e.nodeType === 1) {
    const c = cols(getComputedStyle(e).backgroundColor)[0];
    if (c && c.a > 0.5) return c;
    e = e.parentElement;
  }
  const d = el.closest && el.closest("[data-bg]");
  if (d) { const h = d.getAttribute("data-bg").replace("#", ""); return { r: parseInt(h.substr(0, 2), 16), g: parseInt(h.substr(2, 2), 16), b: parseInt(h.substr(4, 2), 16), a: 1 }; }
  return cols(getComputedStyle(document.body).backgroundColor)[0];
}
const SKIP = new Set(["SCRIPT", "STYLE", "META", "LINK", "NOSCRIPT", "TEMPLATE", "HEAD", "TITLE", "BR", "SOURCE", "TRACK"]);
const ALL = Array.from(document.querySelectorAll("body *")).filter((e) => !SKIP.has(e.tagName) && !e.closest(".h1-seo"));
// ---------- Bewegung ----------
const DUR = [0, 0.2, 0.4, 0.7, 1.2];
const EASE = /cubic-bezier\(0\.16, 1, 0\.3, 1\)/;
const LIN_OK = ".pwtrack, .svcbandtrack, .hdots, .hdots *, .pwtrack *, .svcbandtrack *";
const secs = (s) => s.split(",").map((v) => (v.trim().endsWith("ms") ? parseFloat(v) / 1000 : parseFloat(v)));
for (const el of ALL) {
  for (const ps of ["", "::before", "::after"]) {
    const cs = getComputedStyle(el, ps || null);
    if (ps && (cs.content === "none" || cs.content === "normal")) continue;
    const d = secs(cs.transitionDuration), tf = cs.transitionTimingFunction.split(/,(?![^(]*\))/).map((s) => s.trim()), pr = cs.transitionProperty.split(",").map((s) => s.trim());
    d.forEach((v, i) => {
      if (!(v > 0)) return;
      const t = tf[i % tf.length];
      if (!DUR.some((x) => Math.abs(x - v) < 0.001)) add("TRANSITION-DAUER", el, ps + " " + pr[i % pr.length] + " " + v + "s");
      if (!EASE.test(t) && !(t === "linear" && el.matches(LIN_OK))) add("TRANSITION-KURVE", el, ps + " " + pr[i % pr.length] + " " + t);
    });
    if (cs.animationName && cs.animationName !== "none") {
      const ad = secs(cs.animationDuration), at = cs.animationTimingFunction.split(/,(?![^(]*\))/).map((s) => s.trim()), an = cs.animationName.split(",");
      ad.forEach((v, i) => {
        if (!(v > 0)) return; const t = at[i % at.length];
        if (!DUR.some((x) => Math.abs(x - v) < 0.001) && !el.matches(LIN_OK)) add("ANIMATION-DAUER", el, ps + " " + an[i] + " " + v + "s");
        if (!EASE.test(t) && !(t === "linear" && el.matches(LIN_OK))) add("ANIMATION-KURVE", el, ps + " " + an[i] + " " + t);
        if (cs.animationIterationCount.split(",")[i % cs.animationIterationCount.split(",").length].trim() === "infinite" && !el.matches(LIN_OK)) add("ANIMATION-ENDLOS", el, ps + " " + an[i]);
      });
    }
  }
}
let rm = false; try { for (const s of document.styleSheets) { try { for (const r of s.cssRules) if (r.media && /prefers-reduced-motion/.test(r.media.mediaText)) rm = true; } catch (e) {} } } catch (e) {}
if (!rm) add("KEIN-REDUCED-MOTION", null);

// ---------- Einfrieren: erst Bewegung messen (oben), dann alle Uebergaenge abschalten ----------
// Das unsichtbare WebKit-Fenster spielt Uebergaenge nicht ab (currentTime 0). Ohne Einfrieren misst man Zwischenstaende.
// Vorher einmal ganz durchscrollen, damit Einblendungen (IntersectionObserver) ausgeloest sind.
function freeze() { for (const an of document.getAnimations()) { try { if (an.effect && an.effect.getComputedTiming().iterations !== Infinity) an.finish(); } catch (e) {} } }
// Das Probe-Fenster drosselt requestAnimationFrame stark: Scroll-Loops (on-light, Untergrund, Scrub) laufen dann nicht.
// Ersatz ueber setTimeout, damit die Seite so reagiert wie im sichtbaren Browser.
if (OPT.rafShim !== false) window.requestAnimationFrame = (cb) => setTimeout(() => cb(performance.now()), 16);
const scrollTo2 = (y) => { window.scrollTo(0, y); window.dispatchEvent(new Event("scroll")); };
if (OPT.freeze !== false) {
  const st = document.createElement("style"); st.id = "_ba_freeze";
  st.textContent = "*:not(#_z),*:not(#_z)::before,*:not(#_z)::after{transition:none!important}";
  if (OPT.scan) { const mx = document.documentElement.scrollHeight - H; for (let y = 0; y <= mx + 1; y += Math.round(H * 0.5)) { scrollTo2(Math.min(y, mx)); await sl(260); } }
  document.head.appendChild(st); freeze();
  scrollTo2(0); await sl(500); freeze(); if (window.ADB_MBTICK) window.ADB_MBTICK(true);
}
const V = ALL.filter(vis);
out.info.count = { all: ALL.length, visible: V.length };
const docRect = (el) => { const r = el.getBoundingClientRect(); return { l: r.left + scrollX, t: r.top + scrollY, r: r.right + scrollX, b: r.bottom + scrollY, w: r.width, h: r.height }; };
const blended = (el) => { let e = el; while (e && e !== document.body) { if (getComputedStyle(e).mixBlendMode !== "normal") return true; e = e.parentElement; } return false; };
const isFixed = (el) => { let e = el; while (e && e !== document.body) { const p = getComputedStyle(e).position; if (p === "fixed" || p === "sticky") return true; e = e.parentElement; } return false; };

// Fotos (fuer Lime-an-Foto)
const PHOTOS = V.filter((e) => {
  const r = e.getBoundingClientRect(); if (r.width < 80 || r.height < 80) return false;
  if (e.tagName === "IMG") return !/\.svg|logo/i.test(e.currentSrc || e.src);
  if (e.tagName === "VIDEO") return true;
  return /url\(/.test(getComputedStyle(e).backgroundImage) && !/\.svg/.test(getComputedStyle(e).backgroundImage);
}).map((e) => ({ e, r: docRect(e), fx: isFixed(e) }));
const near = (a, b, d) => a.l - d < b.r && a.r + d > b.l && a.t - d < b.b && a.b + d > b.t;

function colorPass(el, cs, pseudo) {
  const tag = pseudo ? sel(el) + pseudo : sel(el);
  const txt = pseudo ? (cs.content && cs.content !== "none" && cs.content !== "normal" && cs.content.replace(/["']/g, "").trim()) : ownText(el);
  const props = [];
  if (txt || el instanceof SVGTextElement) props.push(["color", cs.color]);
  props.push(["background-color", cs.backgroundColor]);
  for (const s of ["Top", "Right", "Bottom", "Left"]) if (parseFloat(cs["border" + s + "Width"]) > 0 && cs["border" + s + "Style"] !== "none") props.push(["border-color", cs["border" + s + "Color"]]);
  if (cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0) props.push(["outline", cs.outlineColor]);
  if (cs.boxShadow && cs.boxShadow !== "none") props.push(["box-shadow", cs.boxShadow]);
  if (/gradient/.test(cs.backgroundImage)) props.push(["gradient", cs.backgroundImage]);
  if (el instanceof SVGElement && !pseudo && el.tagName !== "svg" && el.tagName !== "g") {
    if (cs.fill && cs.fill !== "none") props.push(["fill", cs.fill]);
    if (cs.stroke && cs.stroke !== "none") props.push(["stroke", cs.stroke]);
  }
  if (txt && cs.textShadow && cs.textShadow !== "none") props.push(["text-shadow", cs.textShadow]);
  let lime = false;
  for (const [p, v] of props) for (const c of cols(v)) {
    const j = judge(c, p);
    if (j === "white") add("FARBE-WEISS", null, tag + " " + p + " " + c.s);
    else if (j === "foreign") add("FARBE-FREMD", null, tag + " " + p + " " + c.s);
    if (isLime(c) && p !== "box-shadow" && p !== "text-shadow") lime = true;
    if (tokOf(c) === "stone" && c.a > 0.3) add("FARBE-STONE-NUTZUNG", null, tag + " " + p);
  }
  return { lime, txt };
}

for (const el of V) {
  const cs = getComputedStyle(el);
  const res = colorPass(el, cs, "");
  let lime = res.lime;
  for (const ps of ["::before", "::after"]) {
    const pc = getComputedStyle(el, ps);
    if (pc.content && pc.content !== "none" && pc.content !== "normal" && pc.display !== "none") { const r2 = colorPass(el, pc, ps); if (r2.lime) lime = true; }
  }
  const r = el.getBoundingClientRect();
  // Lime-Text
  const tc = cols(cs.color)[0];
  if (res.txt && isLime(tc)) {
    const b = bgOf(el.parentElement || el); add(tokOf(b) === "black" ? "LIME-TEXT-AUF-SCHWARZ" : "LIME-TEXT", el, "'" + res.txt.slice(0, 30) + "' auf " + (b && b.s ? b.s : JSON.stringify(b)));
  }
  // grosse Lime-Flaeche auf Schwarz
  const bc = cols(cs.backgroundColor)[0];
  if (isLime(bc) && r.width > 48 && r.height > 48) {
    const b = bgOf(el.parentElement); if (b && tokOf(b) === "black" && !isFixed(el)) add("LIME-FLAECHE-AUF-SCHWARZ", el, Math.round(r.width) + "x" + Math.round(r.height));
    info("limeFlaechen", sel(el) + " " + Math.round(r.width) + "x" + Math.round(r.height));
  }
  // Lime an Fotos (statische Elemente)
  if (lime && !isFixed(el)) {
    const a = docRect(el);
    const ph = PHOTOS.find((p) => !p.fx && p.e !== el && !p.e.contains(el) && near(a, p.r, 40));
    if (ph) add("LIME-AN-FOTO", el, "neben " + sel(ph.e));
  }
  // Graustufen- und andere Filter
  if (cs.filter && cs.filter !== "none" && /grayscale|sepia|saturate|brightness|contrast/.test(cs.filter) && PAGE !== "agentur.html") add("BILD-FILTER", el, cs.filter);
  // Linien
  for (const s of ["Top", "Right", "Bottom", "Left"]) {
    const bw = parseFloat(cs["border" + s + "Width"]), st = cs["border" + s + "Style"];
    if (bw > 0 && st !== "none" && st !== "hidden") {
      if (Math.abs(bw - 1) > 0.05 && !el.closest(".phframe")) add("LINIE-NICHT-1PX", el, "border-" + s.toLowerCase() + " " + bw + "px");
      if (st === "dotted" || st === "dashed") add("LINIE-GESTRICHELT", el, st);
    }
  }
  if (r.height > 1.5 && r.height <= 3 && r.width > 40 && bc && bc.a > 0 && el.children.length === 0 && !ownText(el)) add("LINIE-ALS-FLAECHE-NICHT-1PX", el, Math.round(r.width) + "x" + r.height.toFixed(1));
}

// Text-Paare
for (const el of V) {
  const t = ownText(el); if (!t) continue;
  // feste/klebende Ebenen und Elemente mit mix-blend-mode werden im Scroll-Durchlauf bzw. gar nicht ueber Vorfahren bewertet
  if (isFixed(el) || blended(el)) continue;
  const cs = getComputedStyle(el), c = cols(cs.color)[0]; if (!c || c.a < 0.3) continue;
  const b = bgOf(el), tt = tokOf(c), bt = b && tokOf(b);
  if (!tt || !bt) continue;
  const ok = (tt === "black" && (bt === "cream" || bt === "lime" || bt === "stone" || bt === "ph")) || (tt === "cream" && bt === "black");
  if (!ok) {
    // Text ueber Foto/Bild-Ebene (Ueberlagerung) ist nicht ueber Vorfahren bestimmbar: dann nur melden, wenn kein Foto in der Naehe
    const a = docRect(el); const overPhoto = PHOTOS.some((p) => near(a, p.r, 0));
    if (!overPhoto) add("FARBPAAR-UNERLAUBT", el, tt + " auf " + bt + " '" + t.slice(0, 24) + "'");
  }
}
// Sektionsflaechen
document.querySelectorAll("[data-bg]").forEach((s) => { const v = s.getAttribute("data-bg").toUpperCase(); if (!["#F4F3EB", "#101010", "#CDFF00"].includes(v)) add("SEKTION-DATA-BG", s, v); });
V.filter((e) => e.tagName === "SECTION" || e.tagName === "FOOTER").forEach((s) => { const c = cols(getComputedStyle(s).backgroundColor)[0]; if (c && c.a > 0 && !["cream", "black", "lime"].includes(tokOf(c))) add("SEKTION-FLAECHE", s, c.s); if (c && c.a > 0 && c.a < 0.99) add("SEKTION-FLAECHE-TRANSPARENT", s, c.s); });

// ---------- Graphen: Lime nur fuer den einen hervorgehobenen Wert, auf Schwarz hoechstens ein kleiner Status-Punkt ----------
for (const g of V.filter((e) => e.matches(".dotbars .row, .kdots .row, .dotgraph, .ratedots, .tldots, .kline"))) {
  const dots = Array.from(g.querySelectorAll("i, circle, .kd")).filter(vis);
  const lime = dots.filter((d) => { const c = getComputedStyle(d); return isLime(cols(c.backgroundColor)[0]) || isLime(cols(c.fill)[0]); });
  const b = bgOf(g);
  if (lime.length > 1) add("GRAPH-MEHR-ALS-EIN-LIME", g, lime.length + " Lime-Punkte von " + dots.length + " auf " + (tokOf(b) || (b && b.s)));
  if (lime.length && tokOf(b) === "black") { const r = lime[0].getBoundingClientRect(); if (r.width > 12 || lime.length > 1) add("GRAPH-LIME-AUF-SCHWARZ", g, lime.length + "x " + Math.round(r.width) + "px"); }
  info("graphLime", sel(g).slice(-30) + " " + lime.length + "/" + dots.length);
}
// ---------- Schrift ----------
const fams = {}, weights = {};
const NUMRE = /^[+\-−~≈<>]?\s?[€$]?\s?\d[\d.,\s]*\s?(%|x|×|€|k|K|Mio\.?|Mrd\.?|Tsd\.?|h|s|m²|m|Wochen|Tage|°)?\s?[+]?$/;
function fam(cs) { return cs.fontFamily.split(",")[0].replace(/["']/g, "").trim().toLowerCase(); }
for (const el of V) {
  const t = ownText(el); const cs = getComputedStyle(el);
  let ptxt = "";
  for (const ps of ["::before", "::after"]) { const pc = getComputedStyle(el, ps); if (pc.content && /^["'].*\S.*["']$/.test(pc.content)) ptxt = pc.content; }
  if (!t && !ptxt) continue;
  const f = fam(cs), fs = parseFloat(cs.fontSize), fw = cs.fontWeight;
  fams[f] = (fams[f] || 0) + 1; weights[fw] = (weights[fw] || 0) + 1;
  if (f !== "satoshi" && f !== "amandine") add("SCHRIFT-FREMD", el, f + " '" + (t || ptxt).slice(0, 20) + "'");
  if (!["400", "500", "700"].includes(fw)) add("SCHNITT-FREMD", el, fw + " (" + f + ")");
  if (cs.fontStyle !== "normal" && f !== "amandine") add("SATOSHI-KURSIV", el, "'" + t.slice(0, 20) + "'");
  if (cs.textTransform !== "none") add("VERSALIEN", el, cs.textTransform);
  if (cs.letterSpacing !== "normal" && Math.abs(parseFloat(cs.letterSpacing)) > 0.01) add("LAUFWEITE", el, cs.letterSpacing);
  if (t && /^[A-ZÄÖÜ0-9 .,&\-]{4,}$/.test(t) && /[A-Z]{3}/.test(t) && fs < 20) add("VERSAL-TEXT-IM-MARKUP", el, "'" + t.slice(0, 24) + "'");
  const isNum = NUMRE.test(t);
  if (f === "amandine") {
    const hd = el.closest("[data-hd], .ftr-h") || (el.classList.contains("am") ? el.parentElement : null);
    if (hd && !isNum) {
      const hfs = parseFloat(getComputedStyle(hd).fontSize);
      if (DESK && hfs < 47.5) add("AMANDINE-HEADLINE-UNTER-48", hd, Math.round(hfs) + "px '" + hd.textContent.trim().slice(0, 30) + "'");
      if (cs.fontStyle !== "italic") add("AMANDINE-ZEILE-NICHT-KURSIV", el);
      const full = hd.textContent.replace(/\s+/g, " ").trim(), mine = el.textContent.replace(/\s+/g, " ").trim(), idx = full.lastIndexOf(mine);
      if (idx <= 0) add("AMANDINE-ERSTE-ZEILE-ODER-GANZE", hd, "'" + full.slice(0, 40) + "'");
      else if (full.slice(idx + mine.length).replace(/[.!?\s]/g, "").length > 0) add("AMANDINE-NICHT-LETZTE-ZEILE", hd, "'" + full.slice(0, 50) + "'");
      const r = el.getBoundingClientRect(), lh = parseFloat(cs.lineHeight) || fs * 1.1;
      if (!MOB && r.height > lh * 1.5) add("AMANDINE-ZEILE-UMBRUCH", hd, Math.round(r.height / lh) + " Zeilen '" + mine.slice(0, 30) + "'");
      const ratio = fs / hfs;
      if (!MOB && (ratio < 0.84 || ratio > 0.92)) add("AMANDINE-SKALA-ABWEICHUNG", hd, "Amandine " + Math.round(fs) + "px zu Satoshi " + Math.round(hfs) + "px (" + ratio.toFixed(2) + ", Soll 0,88) '" + mine.slice(0, 26) + "'");
      // Mobil: die Amandine-Zeile soll nicht staerker als 0,72 schrumpfen
      if (MOB && ratio < 0.7) add("AMANDINE-SKALA-MOBIL", hd, ratio.toFixed(2) + " '" + mine.slice(0, 26) + "'");
    } else if (isNum || NUMRE.test(el.textContent.trim())) {
      if (DESK && fs < 47.5) add("AMANDINE-ZAHL-UNTER-48", el, Math.round(fs) + "px '" + el.textContent.trim().slice(0, 16) + "'");
      if (cs.fontStyle !== "normal") add("AMANDINE-ZAHL-KURSIV", el);
    } else add("AMANDINE-AUSSERHALB-REGEL", el, Math.round(fs) + "px '" + (t || el.textContent).trim().slice(0, 30) + "'");
  } else if (DESK && fs >= 47.5) {
    if (isNum) add("GROSSE-ZAHL-NICHT-AMANDINE", el, Math.round(fs) + "px '" + t.slice(0, 16) + "'");
    else {
      const hd = el.closest("[data-hd], .ftr-h");
      if (!hd) add("DISPLAY-OHNE-AMANDINE-MUSTER", el, Math.round(fs) + "px '" + el.textContent.trim().slice(0, 40) + "'");
      else if (!Array.from(hd.querySelectorAll("*")).some((x) => fam(getComputedStyle(x)) === "amandine")) add("DISPLAY-OHNE-AMANDINE-MUSTER", hd, "data-hd ohne Amandine '" + hd.textContent.trim().slice(0, 40) + "'");
    }
  }
  // Zeilenhoehen
  const lh = parseFloat(cs.lineHeight);
  if (lh && fs) {
    const k = lh / fs;
    if (el.matches("p, li") && !el.closest("[data-hd], h1, h2, h3, .btn, .chip, nav, footer .ftr-bot") && fs <= 24 && (k < 1.33 || k > 1.47)) add("FLIESSTEXT-ZEILENHOEHE", el, fs + "/" + lh.toFixed(1) + " = " + k.toFixed(2));
    if (el.matches("h1, h2, [data-hd]") && (k < 1.05 || k > 1.25)) add("HEADLINE-ZEILENHOEHE", el, k.toFixed(2));
  }
  if (el.matches("p") && !el.closest("footer, .btn, .kpi, .tile, .wt, figcaption") && fs < 20) info("pSize", Math.round(fs));
}
out.info.fams = fams; out.info.weights = weights;
out.info.fontsLoaded = Array.from(document.fonts).map((f) => f.family.replace(/["']/g, "") + " " + f.weight + " " + f.style + " " + f.status).filter((v, i, a) => a.indexOf(v) === i);
if (!document.fonts.check("italic 400 40px amandine")) add("AMANDINE-NICHT-GELADEN", null, "document.fonts.check false");
// Wortmarke
document.querySelectorAll(".logo, .ftr-mark, .wordmark, .fword, .ptw").forEach((e) => {
  if (!vis(e) && !e.classList.contains("ptw")) return;
  const cs = getComputedStyle(e);
  info("wortmarke", sel(e) + " " + fam(cs) + " " + cs.fontWeight + " " + cs.fontSize + " '" + e.textContent.trim() + "'");
  if (fam(cs) !== "satoshi" || cs.fontWeight !== "700") add("WORTMARKE-SCHRIFT", e, fam(cs) + " " + cs.fontWeight);
  e.querySelectorAll("*").forEach((k) => { const c = getComputedStyle(k); if (fam(c) !== "satoshi" || c.fontStyle !== "normal") add("WORTMARKE-SCHRIFT", k, fam(c) + " " + c.fontStyle); });
  if (e.matches(".fword")) add("FWORD-VORHANDEN", e);
  const fs = parseFloat(cs.fontSize);
  if (e.matches(".chrome .logo, .logo") && !MOB && (fs < 22.5 || fs > 25.5)) add("WORTMARKE-GROESSE", e, fs + "px (Figma Navbar 25, Footer 23)");
  if (e.matches(".ftr-mark") && (fs < 22.5 || fs > 23.5)) add("WORTMARKE-GROESSE", e, fs + "px (Figma Footer 23)");
});

// ---------- Komponenten ----------
const px = (v) => parseFloat(v) || 0;
const pill = (el, cs) => { const r = el.getBoundingClientRect(); return px(cs.borderTopLeftRadius) >= Math.min(r.height, r.width) / 2 - 1; };
const SPEC = {
  "btn--primary": ["black", "cream", "black", "none"], "btn--secondary": [null, "black", "black", "none"], "btn--accent": ["lime", "black", "black", "none"],
  "btn--inverse": ["cream", "black", "cream", "none"], "btn--outline-inverse": [null, "cream", "cream", "none"], "btn--soft-cream": ["cream", "black", "cream", "dark"],
  "btn--soft-black": ["black", "cream", "black", "light"], "btn--soft-lime": ["lime", "black", "lime", "dark"],
};
const BTNS = V.filter((e) => e.classList.contains("btn"));
out.info.buttons = BTNS.length;
for (const b of BTNS) {
  const cs = getComputedStyle(b), r = b.getBoundingClientRect();
  const vars = Array.from(b.classList).filter((c) => /^btn--/.test(c));
  if (vars.length !== 1) { add("BUTTON-VARIANTE-ANZAHL", b, vars.join(",") || "keine"); continue; }
  if (!pill(b, cs)) add("BUTTON-NICHT-PILL", b, cs.borderTopLeftRadius);
  const pv = px(cs.paddingTop) + px(cs.borderTopWidth), ph = px(cs.paddingLeft) + px(cs.borderLeftWidth);
  if (Math.abs(pv - 16) > 0.6 || Math.abs(ph - 24) > 0.6) add("BUTTON-PADDING", b, pv + "/" + ph);
  if (Math.abs(px(cs.fontSize) - 17) > 0.3) add("BUTTON-SCHRIFTGROESSE", b, cs.fontSize);
  if (cs.fontWeight !== "500") add("BUTTON-SCHNITT", b, cs.fontWeight);
  if (Math.abs(px(cs.lineHeight) / px(cs.fontSize) - 1.2) > 0.03) add("BUTTON-ZEILENHOEHE", b, cs.lineHeight);
  if (Math.abs(r.height - 52.4) > 1.5) add("BUTTON-HOEHE", b, r.height.toFixed(1) + "px (Soll 16+20,4+16)");
  const sp = SPEC[vars[0]]; if (!sp) { add("BUTTON-VARIANTE-UNBEKANNT", b, vars[0]); continue; }
  const bg = cols(cs.backgroundColor)[0], fg = cols(cs.color)[0], bo = cols(cs.borderTopColor)[0];
  if (sp[0] ? tokOf(bg) !== sp[0] || bg.a < 0.99 : bg.a > 0.01) add("BUTTON-FLAECHE-FALSCH", b, vars[0] + " " + bg.s);
  if (tokOf(fg) !== sp[1]) add("BUTTON-TEXT-FALSCH", b, vars[0] + " " + fg.s);
  if (sp[2] && (px(cs.borderTopWidth) > 0) && tokOf(bo) !== sp[2] && bo.a > 0.01) add("BUTTON-RAND-FALSCH", b, vars[0] + " " + bo.s);
  const sh = cs.boxShadow;
  if (sp[3] === "none" && sh !== "none" && !/inset/.test(sh)) add("BUTTON-SCHATTEN-FALSCH", b, vars[0] + " " + sh);
  if (sp[3] !== "none" && (sh === "none" || !/4px 11px/.test(sh))) add("BUTTON-SCHATTEN-FALSCH", b, vars[0] + " " + sh);
  if (fam(cs) !== "satoshi") add("BUTTON-SCHRIFT", b, fam(cs));
}
// Knopf-artige Elemente ausserhalb des Systems
for (const e of V) {
  if (e.classList.contains("btn") || !(e.tagName === "A" || e.tagName === "BUTTON")) continue;
  if (e.closest(".chrome, .msheet, .mitem, nav.ftr-links, .ftr-bot") || e.matches(".mbtn, .fbtn, .bbtn, .bkbtn, .fchip, .kchip, .kopt, .nopt, .hn, .vc, .schip, .chip, .ahead, .wt, .tile, .see, .npgo")) continue;
  const cs = getComputedStyle(e), r = e.getBoundingClientRect();
  const filled = cols(cs.backgroundColor)[0].a > 0.05 || px(cs.borderTopWidth) > 0;
  if (filled && r.height >= 28 && r.height <= 90 && r.width > r.height && px(cs.borderTopLeftRadius) > 4 && (ownText(e) || e.textContent.trim())) add("KNOPF-OHNE-SYSTEM", e, Math.round(r.width) + "x" + Math.round(r.height) + " r" + cs.borderTopLeftRadius + " '" + e.textContent.trim().slice(0, 24) + "'");
}
// Chips
for (const c of V.filter((e) => e.matches(".kchip, .kopt, .needgrid .nopt, .hlxnav .hn, .vchips .vc, .fpop .fchip, .bpop .fchip, .needbar .nsel .schip, .chip"))) {
  const cs = getComputedStyle(c);
  if (MOB && c.matches(".apl .hlxnav .hn")) continue;
  if (!pill(c, cs)) add("CHIP-NICHT-PILL", c, cs.borderTopLeftRadius);
  const pv = px(cs.paddingTop) + px(cs.borderTopWidth), ph = px(cs.paddingLeft) + px(cs.borderLeftWidth);
  if (Math.abs(pv - 8) > 0.6 || Math.abs(ph - 24) > 0.6) add("CHIP-PADDING", c, pv + "/" + ph);
  if (Math.abs(px(cs.fontSize) - 15) > 0.3) add("CHIP-SCHRIFTGROESSE", c, cs.fontSize);
  if (cs.fontWeight !== "500") add("CHIP-SCHNITT", c, cs.fontWeight);
  const bg = cols(cs.backgroundColor)[0]; if (isLime(bg) || isLime(cols(cs.borderTopColor)[0]) || isLime(cols(cs.color)[0])) add("CHIP-LIME", c);
  if (Math.abs(px(cs.borderTopWidth) - 1) > 0.05) add("CHIP-RAND", c, cs.borderTopWidth);
}
// Badges und Eyebrows
const HEADS = V.filter((e) => e.matches("h1, h2, h3, [data-hd], .disp, .dispn, .kh"));
function aboveHeadline(el) {
  const r = el.getBoundingClientRect();
  for (const h of HEADS) {
    if (h.contains(el)) continue;
    const hr = h.getBoundingClientRect(); const gap = hr.top - r.bottom;
    if (gap >= -2 && gap <= 56 && r.left < hr.right && r.right > hr.left) return [h, Math.round(gap)];
  }
  return null;
}
for (const b of V.filter((e) => e.matches(".bdg, .kpi .kpill, .ktrust span, .svc-hero .tags span, .wt .wpill, .tile .badge, .badge"))) {
  const cs = getComputedStyle(b);
  if (!pill(b, cs)) add("BADGE-NICHT-PILL", b, cs.borderTopLeftRadius);
  const fs = px(cs.fontSize); if (Math.abs(fs - 13) > 0.3 && Math.abs(fs - 11) > 0.3) add("BADGE-SCHRIFTGROESSE", b, cs.fontSize);
  if (cs.fontWeight !== "500") add("BADGE-SCHNITT", b, cs.fontWeight);
  const pv = px(cs.paddingTop) + px(cs.borderTopWidth), ph = px(cs.paddingLeft) + px(cs.borderLeftWidth);
  if (!((Math.abs(pv - 8) < 0.6 && Math.abs(ph - 16) < 0.6) || (Math.abs(pv - 4) < 0.6 && Math.abs(ph - 12) < 0.6))) add("BADGE-PADDING", b, pv + "/" + ph);
  const bg = cols(cs.backgroundColor)[0]; if (bg.a > 0.01) add("BADGE-MIT-FUELLUNG", b, bg.s + (cs.backdropFilter && cs.backdropFilter !== "none" ? " + " + cs.backdropFilter : ""));
  const bo = cols(cs.borderTopColor)[0]; if (bo && (bo.a < 0.2 || bo.a > 0.35)) add("BADGE-RAND-DECKKRAFT", b, bo.s);
  if (isLime(cols(cs.color)[0]) || isLime(bo)) add("BADGE-LIME", b);
  const ah = aboveHeadline(b); if (ah) add("BADGE-UEBER-HEADLINE", b, ah[1] + "px ueber " + sel(ah[0]));
}
for (const l of V.filter((e) => e.matches(".label, .slabel, .eyebrow, .kicker, .lbl, .cl, .sticky-l") && !e.matches(".bdg"))) {
  const ah = aboveHeadline(l); if (ah) add("EYEBROW-UEBER-HEADLINE", l, "'" + l.textContent.trim().slice(0, 24) + "' " + ah[1] + "px ueber " + sel(ah[0]));
  else info("labelsSichtbar", sel(l) + " '" + l.textContent.trim().slice(0, 24) + "'");
}
// Allgemein: kleine Texte direkt ueber Headlines (Eyebrow ohne bekannte Klasse)
for (const e of V) {
  const t = ownText(e); if (!t || t.length > 40) continue;
  const cs = getComputedStyle(e); if (px(cs.fontSize) > 16 || e.closest("h1,h2,h3,[data-hd],.btn,.chrome,.msheet,.bdg,.badge,.lbl-x,.label,.slabel,nav")) continue;
  const ah = aboveHeadline(e); if (ah && px(getComputedStyle(ah[0]).fontSize) >= 28) add("KLEINTEXT-UEBER-HEADLINE", e, "'" + t.slice(0, 24) + "' " + ah[1] + "px ueber " + sel(ah[0]));
}
// Karten
for (const c of V.filter((e) => e.matches(".svcard, .kpiboard .kpi, .dcell, .fcard, .pcard, .hproc .hcard, .proofcase .ptile, .qcard"))) {
  const cs = getComputedStyle(c);
  if (Math.abs(px(cs.borderTopLeftRadius) - 20) > 0.5) add("KARTE-RADIUS", c, cs.borderTopLeftRadius);
  if (Math.abs(px(cs.borderTopWidth) - 1) > 0.05) add("KARTE-RAND", c, cs.borderTopWidth);
  const p = px(cs.paddingTop), want = MOB ? 24 : 32;
  if (Math.abs(p - want) > 0.6 || Math.abs(px(cs.paddingLeft) - want) > 0.6) add("KARTE-PADDING", c, cs.paddingTop + " " + cs.paddingLeft + " (Soll " + want + ")");
}
// Service Card Typo
for (const c of V.filter((e) => e.matches(".svcard"))) {
  const st = c.querySelector(".st"), sn = c.querySelector(".sn"), li = c.querySelector("li, p");
  if (st) { const s = getComputedStyle(st); if (Math.abs(px(s.fontSize) - 28.5) > 0.6 && !MOB) add("SERVICECARD-TITEL", st, s.fontSize + " (Soll 28,5)"); }
  if (sn) { const s = getComputedStyle(sn); if (Math.abs(px(s.fontSize) - 15) > 0.3) add("SERVICECARD-NUMMER", sn, s.fontSize); }
  if (li) { const s = getComputedStyle(li); if (Math.abs(px(s.fontSize) - 16) > 0.3) add("SERVICECARD-TEXT", li, s.fontSize + " (Soll 16)"); }
}
// Radien allgemein (Flaechen mit Radius, keine Pills)
for (const e of V) {
  const cs = getComputedStyle(e), rr = px(cs.borderTopLeftRadius); if (rr <= 0.5) continue;
  const r = e.getBoundingClientRect(); if (r.width < 100 || r.height < 70) continue;
  if (rr >= Math.min(r.width, r.height) / 2 - 1) continue; // Pill oder Kreis
  if (cs.borderTopLeftRadius.includes("%")) continue;
  const inCollage = !!e.closest(".collage");
  const want = inCollage ? 12 : 20;
  if (Math.abs(rr - want) > 0.5 && !e.closest(".phframe") && !e.matches(".phframe")) add("RADIUS-FREMD", e, cs.borderTopLeftRadius + " (Soll " + want + ")");
}
// Bilder: Container Radius 20, Vollbild 0, Collage 12
function clipRadius(img) {
  let e = img, k = 0, best = px(getComputedStyle(img).borderTopLeftRadius), src = img;
  const ir = img.getBoundingClientRect();
  while (e.parentElement && k < 5) {
    e = e.parentElement; k++;
    const cs = getComputedStyle(e), r = e.getBoundingClientRect();
    if (r.width > ir.width * 1.25 + 4 || r.height > ir.height * 1.25 + 4) break;
    if ((cs.overflow !== "visible" || cs.clipPath !== "none") && px(cs.borderTopLeftRadius) > best) { best = px(cs.borderTopLeftRadius); src = e; }
  }
  return [best, src];
}
for (const im of V.filter((e) => e.tagName === "IMG" || e.tagName === "VIDEO" || e.tagName === "PICTURE")) {
  if (im.tagName === "PICTURE") continue;
  const r = im.getBoundingClientRect(); if (r.width < 60 || r.height < 60) continue;
  if (im.tagName === "IMG" && /\.svg|logo/i.test(im.currentSrc || im.src)) continue;
  if (im.closest(".phframe, .mthumb, .msheet, .cur, .pt")) continue;
  const [rad, src] = clipRadius(im);
  const full = r.width >= W - 2 || (r.width >= W * 0.9 && r.height >= H * 0.7);
  const circle = rad >= Math.min(r.width, r.height) / 2 - 1;
  if (circle) continue;
  if (im.closest(".collage")) { if (Math.abs(rad - 12) > 0.5) add("COLLAGE-BILD-RADIUS", im, rad + "px"); continue; }
  if (full) { if (rad > 0.5) add("VOLLBILD-MIT-RADIUS", im, rad + "px"); continue; }
  // Bilder, die eine Sektion fuellen (Hero, Statement-Hintergrund), zaehlen als Vollformat
  const sec = im.closest("section, header, .chero, .hshow"); if (sec) { const sr = sec.getBoundingClientRect(); if (r.width >= sr.width - 2 && sr.width >= W - 2) { if (rad > 0.5) add("VOLLBILD-MIT-RADIUS", im, rad + "px"); continue; } }
  if (Math.abs(rad - 20) > 0.5) add("BILD-RADIUS", im, rad + "px " + Math.round(r.width) + "x" + Math.round(r.height) + " via " + sel(src));
}

// ---------- Footer ----------
const html = await fetch(location.pathname, { cache: "no-store" }).then((r) => r.text()).catch(() => "");
const fm = html.match(/<footer[\s\S]*?<\/footer>/g) || [];
function hash(s) { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(16); }
out.footer = { count: fm.length, hash: fm.length ? hash(fm[0].replace(/Stand:[^<]*/g, "").replace(/\?v=\d+/g, "").replace(/\s+/g, " ")) : null };
const ft = document.querySelector("footer");
if (fm.length !== 1) add("FOOTER-ANZAHL", null, fm.length + " footer");
if (ft) {
  const cs = getComputedStyle(ft), inn = ft.querySelector(".ftr-in") || ft;
  const ci = getComputedStyle(inn);
  const fr = ft.getBoundingClientRect();
  const m = (q) => { const e = ft.querySelector(q); if (!e) return null; const c = getComputedStyle(e), r = e.getBoundingClientRect(); return { fam: fam(c), fs: px(c.fontSize), fw: c.fontWeight, fst: c.fontStyle, col: c.color, l: Math.round(r.left), r: Math.round(r.right), t: Math.round(r.top - fr.top), b: Math.round(r.bottom - fr.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const btns = Array.from(ft.querySelectorAll(".btn")).map((b) => b.className + "|" + b.getAttribute("href") + "|" + b.textContent.trim());
  const links = Array.from(ft.querySelectorAll(".ftr-links a"));
  const gaps = links.slice(1).map((a, i) => Math.round(a.getBoundingClientRect().left - links[i].getBoundingClientRect().right));
  out.footer.m = {
    bg: cs.backgroundColor, pad: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(" "), innerPad: [ci.paddingTop, ci.paddingRight, ci.paddingBottom, ci.paddingLeft].join(" "),
    contentLeft: Math.round((inn.getBoundingClientRect().left + px(ci.paddingLeft))), h1: m(".ftr-h"), h1span: m(".ftr-h > span"), h1i: m(".ftr-h > i"), btns, top: m(".ftr-top"), rule: m(".ftr-rule"), ruleBg: ft.querySelector(".ftr-rule") ? getComputedStyle(ft.querySelector(".ftr-rule")).backgroundColor + "/" + getComputedStyle(ft.querySelector(".ftr-rule")).borderTopColor : null,
    bot: m(".ftr-bot"), mark: m(".ftr-mark"), links: links.map((a) => a.textContent.trim() + " " + getComputedStyle(a).fontSize + " " + getComputedStyle(a).fontWeight).join(" / "), linkGaps: gaps, loc: m(".ftr-loc"), legal: m(".ftr-legal"), height: Math.round(fr.height),
    gapTopRule: ft.querySelector(".ftr-rule") && ft.querySelector(".ftr-top") ? Math.round(ft.querySelector(".ftr-rule").getBoundingClientRect().top - ft.querySelector(".ftr-top").getBoundingClientRect().bottom) : null,
    gapRuleBot: ft.querySelector(".ftr-rule") && ft.querySelector(".ftr-bot") ? Math.round(ft.querySelector(".ftr-bot").getBoundingClientRect().top - ft.querySelector(".ftr-rule").getBoundingClientRect().bottom) : null,
  };
}
// ---------- Collage ----------
out.collage = Array.from(document.querySelectorAll(".collage")).map((c) => {
  const cs = getComputedStyle(c), r = c.getBoundingClientRect(), pl = c.querySelector(".cplane");
  const colsE = Array.from(c.querySelectorAll(".cpcol")).filter((x) => getComputedStyle(x).display !== "none");
  const im = c.querySelector(".cpcol img");
  return { cls: c.className, h: Math.round(r.height), plane: pl ? getComputedStyle(pl).transform : null, cols: colsE.length, colW: colsE.length ? Math.round(colsE[0].getBoundingClientRect().width * 10) / 10 : null, colWcss: colsE.length ? colsE[0].offsetWidth : null, planeW: pl ? pl.offsetWidth : null, planeH: pl ? pl.offsetHeight : null, gap: pl ? getComputedStyle(pl).columnGap : null, imgR: im ? getComputedStyle(im).borderTopLeftRadius : null, imgShadow: im ? getComputedStyle(im).boxShadow : null, drift: colsE.map((x) => x.getAttribute("data-drift")).join(",") };
});
// ---------- Layout: Seitenrand, Overflow, Abstaende ----------
const gut = MOB ? 24 : 64;
for (const w of V.filter((e) => e.classList.contains("wrap"))) {
  const cs = getComputedStyle(w), r = w.getBoundingClientRect();
  const L = Math.round(r.left + px(cs.paddingLeft)), R = Math.round(W - (r.right - px(cs.paddingRight)));
  if (r.width < W * 0.6) continue;
  if (L < gut - 1 || R < gut - 1 || Math.abs(L - R) > 2) add("SEITENRAND", w, "links " + L + " rechts " + R + " (Soll " + gut + ")");
  else if (L > gut + 1) info("schmaleSpalte", sel(w) + " " + L);
}
if (document.documentElement.scrollWidth > W + 2) add("OVERFLOW", null, document.documentElement.scrollWidth + ">" + W);
const SCALE = [0, 8, 16, 24, 32, 48, 64, 96, 128];
for (const s of V.filter((e) => e.tagName === "SECTION" || e.tagName === "FOOTER")) {
  const cs = getComputedStyle(s);
  for (const p of ["paddingTop", "paddingBottom"]) { const v = Math.round(px(cs[p])); if (!SCALE.includes(v)) add("ABSTAND-AUSSER-SKALA", s, p + " " + v + "px"); }
}
// Headline zu Body, Body zu Buttons
for (const h of V.filter((e) => e.matches("h1, h2, [data-hd]"))) {
  let n = h.nextElementSibling; while (n && !vis(n)) n = n.nextElementSibling;
  if (!n || !n.matches("p, .lead, .sub, .ssub")) continue;
  const g = Math.round(n.getBoundingClientRect().top - h.getBoundingClientRect().bottom);
  if (Math.abs(g - 16) > 2) add("ABSTAND-HEADLINE-BODY", h, g + "px (Soll 16)");
}
for (const b of BTNS) {
  let grp = b.parentElement && b.parentElement.querySelectorAll(":scope > .btn").length > 1 ? b.parentElement : b;
  if (grp !== b && grp.querySelector(".btn") !== b) continue;
  let p = grp.previousElementSibling; while (p && !vis(p)) p = p.previousElementSibling;
  if (!p || !p.matches("p, .lead, .sub, .ssub")) continue;
  const g = Math.round(grp.getBoundingClientRect().top - p.getBoundingClientRect().bottom), want = MOB ? 32 : 48;
  if (Math.abs(g - want) > 2) add("ABSTAND-BODY-BUTTON", grp, g + "px (Soll " + want + ")");
}
// ---------- Menue-Knopf, Startseiten-Punkt, Work-Filter ----------
const mb = document.querySelector(".mbtn");
if (mb) {
  const cs = getComputedStyle(mb), r = mb.getBoundingClientRect(), pb = getComputedStyle(mb, "::before");
  out.mbtn = { w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10, cx: Math.round(r.left + r.width / 2), bottom: Math.round(H - r.bottom), bg: cs.backgroundColor, border: cs.borderTopColor, display: cs.display, ai: cs.alignItems, jc: cs.justifyContent, before: { content: pb.content, fam: fam(pb), fw: pb.fontWeight, fs: pb.fontSize, w: pb.width, h: pb.height, pos: pb.position, disp: pb.display, inset: pb.top + " " + pb.left } };
  const want = MOB ? 76 : 88; if (Math.abs(r.width - want) > 1 || Math.abs(r.height - want) > 1) add("MENUEKNOPF-GROESSE", mb, r.width + "x" + r.height + " (Soll " + want + ")");
  if (!/Men/.test(pb.content)) add("MENUEKNOPF-WORT", mb, pb.content);
  if (fam(pb) !== "satoshi" || pb.fontWeight !== "500") add("MENUEKNOPF-SCHRIFT", mb, fam(pb) + " " + pb.fontWeight);
  if (Math.abs(r.left + r.width / 2 - W / 2) > 1.5) add("MENUEKNOPF-NICHT-MITTIG", mb, Math.round(r.left + r.width / 2) + " statt " + W / 2);
}
const bd = document.querySelector(".hpitch .bdot"); if (bd && vis(bd)) add("STARTSEITE-BDOT-SICHTBAR", bd); out.info.bdotInDom = !!bd;
const fb = document.querySelector(".fbtn"), bb = document.querySelector(".bbtn");
if (fb && bb) {
  const IGN = /^(left|right|margin-left|margin-right|inset|inset-inline|inset-inline-start|inset-inline-end|margin-inline|margin-inline-start|margin-inline-end|translate|content|-webkit-margin-start|-webkit-margin-end|transform-origin|perspective-origin|grid-area|order|view-transition-name|anchor-name)$/;
  const diff = [];
  for (const ps of ["", "::before", "::after"]) {
    const a = getComputedStyle(fb, ps || null), b = getComputedStyle(bb, ps || null);
    for (let i = 0; i < a.length; i++) { const k = a[i]; if (IGN.test(k)) continue; const x = a.getPropertyValue(k), y = b.getPropertyValue(k); if (x !== y && !(ps && /width|height|block-size|inline-size/.test(k) && false)) diff.push((ps || "") + k + ": " + x + " | " + y); }
  }
  const ra = fb.getBoundingClientRect(), rb = bb.getBoundingClientRect();
  out.workFilter = { fbtn: [ra.width, ra.height, Math.round(ra.left), Math.round(H - ra.bottom)], bbtn: [rb.width, rb.height, Math.round(rb.left), Math.round(H - rb.bottom)], diff: diff.slice(0, 30), symmetric: Math.round(W / 2 - ra.right) + " / " + Math.round(rb.left - W / 2) };
  if (diff.length) add("WORK-FILTER-UNGLEICH", null, diff.length + " Eigenschaften: " + diff.slice(0, 4).join("; "));
  if (Math.abs(ra.width - rb.width) > 0.5 || Math.abs(ra.bottom - rb.bottom) > 0.5) add("WORK-FILTER-UNGLEICH", null, "Groesse/Lage " + JSON.stringify(out.workFilter));
  if (Math.abs((W / 2 - ra.right) - (rb.left - W / 2)) > 1.5) add("WORK-FILTER-ASYMMETRISCH", null, out.workFilter.symmetric);
  const pops = Array.from(document.querySelectorAll(".fpop .fchip, .bpop .fchip")).filter(vis); if (pops.length) add("WORK-FILTERCHIPS-OHNE-KLICK-SICHTBAR", pops[0], pops.length + " Chips");
}
// ---------- Scroll-Durchlauf: Menue-Knopf, Knoepfe nach Untergrund, feste Elemente an Fotos ----------
function under(x, y, skip) {
  const st = document.elementsFromPoint(x, y);
  for (const e of st) {
    if (skip.some((s) => s.contains(e) || e.contains(s) && false)) continue;
    if (e.closest(".mbtn, .fbtn, .bbtn, .bkbtn, .chrome, .cur, .sprog, .chapnav, .fpop, .bpop, .coach, .pt")) continue;
    if (e.tagName === "IMG" || e.tagName === "VIDEO" || e.tagName === "CANVAS" && e.getBoundingClientRect().width > 200) return { k: "photo", e };
    const cs = getComputedStyle(e);
    if (/url\(/.test(cs.backgroundImage)) return { k: "photo", e };
    const c = cols(cs.backgroundColor)[0];
    if (c && c.a > 0.5) return { k: tokOf(c) || c.s, e };
  }
  const c = cols(getComputedStyle(document.body).backgroundColor)[0]; return { k: tokOf(c) || c.s, e: document.body };
}
const BOK = { cream: ["btn--primary", "btn--secondary", "btn--accent", "btn--soft-cream"], ph: ["btn--primary", "btn--secondary", "btn--accent", "btn--soft-cream"], stone: ["btn--primary", "btn--secondary", "btn--accent", "btn--soft-cream"], black: ["btn--inverse", "btn--outline-inverse", "btn--soft-black"], lime: ["btn--primary", "btn--soft-lime"], photo: ["btn--primary", "btn--inverse", "btn--outline-inverse"] };
if (OPT.scan) {
  const seen = new Set(); const mbLog = [];
  const max = document.documentElement.scrollHeight - H;
  for (let y = 0; y <= max + 1; y += Math.round(H * OPT.step)) {
    scrollTo2(Math.min(y, max)); await sl(OPT.pause);
    for (const b of BTNS) {
      if (seen.has(b)) continue; const r = b.getBoundingClientRect();
      if (r.top < 60 || r.bottom > H - 140 || r.width < 1 || !vis(b)) continue;
      seen.add(b);
      const pts = [[r.left + 2, r.top + r.height / 2], [r.right - 2, r.top + r.height / 2], [r.left + r.width / 2, r.top - 3], [r.left + r.width / 2, r.bottom + 3]];
      const us = pts.map((p) => under(p[0], p[1], [b]).k); const u = us.includes("photo") ? "photo" : us[0];
      const v = Array.from(b.classList).find((c) => /^btn--/.test(c));
      if (BOK[u] && !BOK[u].includes(v)) add("BUTTON-VARIANTE-UNTERGRUND", b, v + " auf " + u + " '" + b.textContent.trim().slice(0, 20) + "'");
      if (!BOK[u]) add("BUTTON-UNTERGRUND-UNBEKANNT", b, u);
      info("btnSurf", v + "@" + u);
    }
    freeze(); if (window.ADB_MBTICK) window.ADB_MBTICK(true);
    // Kopfzeile (Logo, Kontakt, Menue) muss sich vom Untergrund abheben
    for (const ce of document.querySelectorAll(".chrome .logo, .chrome .ctc, .chrome .hmenu")) {
      if (!vis(ce)) continue; const r = ce.getBoundingClientRect(); const c = cols(getComputedStyle(ce).color)[0];
      const u = under(r.left + r.width / 2, r.top + r.height / 2, [ce]); const ct = tokOf(c);
      if ((ct === "cream" && (u.k === "cream" || u.k === "ph" || u.k === "lime")) || (ct === "black" && u.k === "black")) add("KOPFZEILE-UNSICHTBAR", ce, "y=" + Math.round(scrollY) + " " + ct + " auf " + u.k + " (" + sel(u.e).slice(-40) + ")");
    }
    if (mb && vis(mb)) {
      const r = mb.getBoundingClientRect(), c = cols(getComputedStyle(mb).backgroundColor)[0];
      const pts = [[r.left - 4, r.top + r.height / 2], [r.right + 4, r.top + r.height / 2], [r.left + r.width / 2, r.top - 4], [r.left + r.width / 2, r.bottom + 2]];
      const us = pts.map((p) => under(p[0], p[1], [mb]));
      const kinds = us.map((u) => u.k);
      if (isLime(c)) {
        if (kinds.includes("black")) add("MENUEKNOPF-LIME-AUF-SCHWARZ", null, "y=" + Math.round(scrollY) + " neben " + sel(us[kinds.indexOf("black")].e));
        // Foto innerhalb von 40 px um den Knopf
        const ex = { l: r.left - 40, t: r.top - 40, r: r.right + 40, b: r.bottom + 40 };
        const ph = PHOTOS.find((p) => { const q = p.e.getBoundingClientRect(); return vis(p.e) && q.left < ex.r && q.right > ex.l && q.top < ex.b && q.bottom > ex.t; });
        if (ph || kinds.includes("photo")) add("MENUEKNOPF-LIME-AN-FOTO", null, "y=" + Math.round(scrollY) + " " + sel(ph ? ph.e : us[kinds.indexOf("photo")].e));
      }
      if (tokOf(c) === "cream" && kinds.filter((k) => k === "cream").length >= 3) add("MENUEKNOPF-CREAM-AUF-CREAM", null, "y=" + Math.round(scrollY) + " " + kinds.join(","));
      if (tokOf(c) === "black" && kinds.filter((k) => k === "black").length >= 3) add("MENUEKNOPF-SCHWARZ-AUF-SCHWARZ", null, "y=" + Math.round(scrollY));
      mbLog.push(Math.round(scrollY) + ":" + (tokOf(c) || c.s) + "/" + kinds.join(","));
    }
  }
  out.info.mbLog = mbLog.slice(0, 80);
  window.scrollTo(0, 0);
}
// ---------- qa2 und JS-Fehler ----------
try { const q = await fetch("_tools/qa2.js", { cache: "no-store" }).then((r) => r.text()); out.qa2 = String((0, eval)(q)); } catch (e) { out.qa2 = "qa2 nicht ladbar: " + e; }
out.errs = (window.__errs || []).slice(0, 10);
if (out.errs.length) add("JS-FEHLER", null, out.errs.join(" | "));
return JSON.stringify(out);

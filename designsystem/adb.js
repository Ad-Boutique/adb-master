/* ad.boutique Brand 2026 · Verhalten (optional, ohne Abhaengigkeiten)
   1 Kreis-Hover: der Kreis waechst von der Eintrittsstelle der Maus und zieht sich zur Austrittsstelle zurueck
   2 Einblenden: Elemente mit data-fade bekommen .in, sobald sie sichtbar werden (Versatz 24 px, 400 ms)
   3 Woerterbuch-Hero: das Wort (.adb-dhero__word) fuellt genau die Zeile
   4 Akkordeon: .adb-faq__q oeffnet und schliesst sein .adb-faq__item */
(function () {
  function pos(e) {
    var b = e.currentTarget, r = b.getBoundingClientRect();
    b.style.setProperty("--mx", (e.clientX - r.left) + "px");
    b.style.setProperty("--my", (e.clientY - r.top) + "px");
  }
  function fit() {
    document.querySelectorAll(".adb-dhero__word").forEach(function (w) {
      w.style.setProperty("--fit", "100px");
      var box = w.parentNode.clientWidth, cur = w.scrollWidth;
      if (cur) w.style.setProperty("--fit", (100 * box / cur) + "px");
    });
  }
  function init() {
    document.querySelectorAll(".adb-btn").forEach(function (b) {
      b.addEventListener("pointerenter", pos);
      b.addEventListener("pointerleave", pos);
    });
    var fades = document.querySelectorAll("[data-fade]");
    if ("IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (en) {
        en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } });
      }, { rootMargin: "0px 0px -10% 0px" });
      fades.forEach(function (el) { io.observe(el); });
    } else fades.forEach(function (el) { el.classList.add("in"); });
    document.querySelectorAll(".adb-faq__q").forEach(function (q) {
      q.addEventListener("click", function () {
        var open = q.parentNode.classList.toggle("open");
        q.setAttribute("aria-expanded", open);
      });
    });
    fit();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    window.addEventListener("resize", fit);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();

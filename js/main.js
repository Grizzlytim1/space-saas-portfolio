/* Обрій — page behaviour */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- toast ---------- */
  const toastEl = $("[data-toast]");
  let tt;
  const toast = (t) => { toastEl.textContent = t; toastEl.classList.add("is-on"); clearTimeout(tt); tt = setTimeout(() => toastEl.classList.remove("is-on"), 2600); };
  $$("[data-soon]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); toast("Ця сторінка ще в розробці — Обрій поки концепт для портфоліо."); }));

  /* ---------- starfield ---------- */
  const cv = $("[data-stars]"), cx = cv.getContext("2d");
  let stars = [], sw = 0, sh = 0, dpr = 1, raf;
  function sizeStars() {
    dpr = Math.min(2, devicePixelRatio || 1);
    sw = cv.offsetWidth; sh = cv.offsetHeight;
    cv.width = sw * dpr; cv.height = sh * dpr;
    const n = Math.round(sw * sh / 5200);
    stars = Array.from({ length: n }, () => ({ x: Math.random() * sw, y: Math.random() * sh, r: Math.random() * 1.1 + 0.2, p: Math.random() * 6.28, s: 0.4 + Math.random() * 1.4, v: 0.02 + Math.random() * 0.08 }));
    drawStars(0);
  }
  function drawStars(t) {
    cx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cx.clearRect(0, 0, sw, sh);
    for (const s of stars) {
      const a = 0.25 + 0.75 * Math.abs(Math.sin(s.p + t / 1000 * s.s));
      if (!reduce) { s.y -= s.v; if (s.y < -2) s.y = sh + 2; }
      cx.globalAlpha = a; cx.fillStyle = s.r > 1.1 ? "#e9ffb0" : "#fff";
      cx.beginPath(); cx.arc(s.x, s.y, s.r, 0, 6.283); cx.fill();
    }
  }
  const loop = (t) => { drawStars(t); raf = requestAnimationFrame(loop); };
  sizeStars();
  if (!reduce) {
    new IntersectionObserver(([en]) => { cancelAnimationFrame(raf); if (en.isIntersecting) raf = requestAnimationFrame(loop); }).observe(cv);
  }
  addEventListener("resize", sizeStars);

  /* ---------- nav: solid after scroll, hides while scrolling down ---------- */
  const nav = $("[data-nav]");
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    nav.classList.toggle("is-solid", y > 30);
    nav.classList.toggle("is-hidden", y > 400 && y > lastY && mnav.hidden);
    lastY = y;
  };
  addEventListener("scroll", onScroll, { passive: true });

  /* ---------- mobile nav ---------- */
  const burger = $("[data-burger]"), mnav = $("#mnav");
  const setM = (open) => { mnav.hidden = !open; burger.setAttribute("aria-expanded", String(open)); burger.setAttribute("aria-label", open ? "Закрити меню" : "Відкрити меню"); };
  burger.addEventListener("click", () => setM(mnav.hidden));
  $$("#mnav a, #mnav button").forEach((a) => a.addEventListener("click", () => setM(false)));
  matchMedia("(min-width: 861px)").addEventListener("change", (e) => e.matches && setM(false));
  onScroll();

  /* ---------- reveal ---------- */
  const io = "IntersectionObserver" in window ? new IntersectionObserver((ents) => ents.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
  }), { rootMargin: "0px 0px -6% 0px" }) : null;
  $$(".reveal").forEach((el) => (io ? io.observe(el) : el.classList.add("is-in")));

  /* ---------- rolling-digit counters ---------- */
  $$("[data-odo]").forEach((el) => {
    const digits = el.dataset.odo.split("");
    el.innerHTML = digits.map(() => `<span class="odo__d">${"0123456789".split("").map((d) => `<span>${d}</span>`).join("")}</span>`).join("");
    el.setAttribute("aria-label", el.dataset.odo);
    const cols = $$(".odo__d", el);
    const run = () => cols.forEach((c, i) => { c.style.transitionDelay = `${i * 0.15}s`; c.style.transform = `translateY(-${+digits[i]}em)`; });
    if (reduce || !io) { cols.forEach((c) => (c.style.transition = "none")); run(); return; }
    const o = new IntersectionObserver(([en]) => { if (en.isIntersecting) { o.disconnect(); run(); } }, { threshold: 0.5 });
    o.observe(el);
  });

  /* ---------- logo marquee (content duplicated once) ---------- */
  const logos = $("[data-logos]");
  logos.insertAdjacentHTML("beforeend", logos.innerHTML.replace(/<span class="lg/g, '<span aria-hidden="true" class="lg'));

  /* ---------- fixed-size editor mock scaled to its column ---------- */
  $$("[data-scaler]").forEach((box) => {
    const w = +box.dataset.w, h = +box.dataset.h;
    const fit = () => { const s = box.clientWidth / w; box.style.setProperty("--s", s); box.style.height = h * s + "px"; };
    fit(); new ResizeObserver(fit).observe(box);
  });

  /* ---------- tabs (ARIA, arrow keys) ---------- */
  const tabs = $$("[data-tabs] [role=tab]");
  const select = (t, focus) => {
    tabs.forEach((b) => { const on = b === t; b.setAttribute("aria-selected", String(on)); b.tabIndex = on ? 0 : -1; $("#" + b.getAttribute("aria-controls")).hidden = !on; });
    if (focus) t.focus();
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => select(t));
    t.addEventListener("keydown", (e) => {
      const k = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (k) { e.preventDefault(); select(tabs[(i + k + tabs.length) % tabs.length], true); }
      if (e.key === "Home") { e.preventDefault(); select(tabs[0], true); }
      if (e.key === "End") { e.preventDefault(); select(tabs[tabs.length - 1], true); }
    });
  });

  /* ---------- testimonial slider ---------- */
  const slider = $("[data-slider]");
  const pics = $$(".slider__photos img", slider), quotes = $$(".rv", slider);
  let cur = 0, auto;
  const go = (n) => {
    cur = (n + quotes.length) % quotes.length;
    pics.forEach((p, i) => p.classList.toggle("is-on", i === cur));
    quotes.forEach((q, i) => { q.classList.toggle("is-on", i === cur); q.setAttribute("aria-hidden", String(i !== cur)); });
  };
  const restart = () => { clearInterval(auto); if (!reduce) auto = setInterval(() => go(cur + 1), 7000); };
  $("[data-prev]", slider).addEventListener("click", () => { go(cur - 1); restart(); });
  $("[data-next]", slider).addEventListener("click", () => { go(cur + 1); restart(); });
  let sx = null;
  slider.addEventListener("touchstart", (e) => { sx = e.touches[0].clientX; }, { passive: true });
  slider.addEventListener("touchend", (e) => { if (sx === null) return; const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) { go(cur + (dx < 0 ? 1 : -1)); restart(); } sx = null; });
  slider.addEventListener("mouseenter", () => clearInterval(auto));
  slider.addEventListener("mouseleave", restart);
  go(0); restart();

  /* ---------- FAQ accordion (one open at a time) ---------- */
  const qas = $$("[data-faq] .qa");
  qas.forEach((qa) => {
    const b = $("button", qa), a = $(".qa__a", qa);
    b.addEventListener("click", () => {
      const open = !qa.classList.contains("is-open");
      qas.forEach((o) => { o.classList.remove("is-open"); $("button", o).setAttribute("aria-expanded", "false"); $(".qa__a", o).hidden = true; });
      if (open) { qa.classList.add("is-open"); b.setAttribute("aria-expanded", "true"); a.hidden = false; }
    });
  });

  /* ---------- contact modal ---------- */
  const modal = $("[data-modal]"), box = $(".modal__box", modal), form = $("[data-form]", modal), done = $("[data-done]", modal), err = $("[data-err]", modal);
  let opener = null;
  const openM = (from) => { opener = from; modal.hidden = false; document.documentElement.classList.add("no-scroll"); form.hidden = false; done.hidden = true; setTimeout(() => form.elements.namedItem("name").focus(), 50); };
  const closeM = () => { modal.hidden = true; document.documentElement.classList.remove("no-scroll"); if (opener) opener.focus({ preventScroll: true }); };
  $$("[data-contact]").forEach((b) => b.addEventListener("click", () => openM(b)));
  $$("[data-close]", modal).forEach((b) => b.addEventListener("click", closeM));
  modal.addEventListener("click", (e) => { if (e.target === modal) closeM(); });
  document.addEventListener("keydown", (e) => {
    if (modal.hidden) return;
    if (e.key === "Escape") closeM();
    if (e.key === "Tab") {
      const f = $$("button, input, select, textarea", box).filter((x) => x.offsetParent);
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const f = (n) => form.elements.namedItem(n);
    const rules = [["name", (v) => v.trim().length >= 2, "Вкажіть ім'я."], ["email", (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()), "Перевірте email."], ["size", (v) => !!v, "Оберіть розмір команди."]];
    const msgs = []; let first = null;
    rules.forEach(([n, ok, m]) => { const bad = !ok(f(n).value); f(n).setAttribute("aria-invalid", String(bad)); if (bad) { msgs.push(m); first = first || f(n); } });
    err.textContent = msgs.join(" ");
    if (first) { first.focus(); return; }
    $("[data-done-text]", modal).textContent = `${f("name").value.trim()}, доступ на 14 днів надіслали на ${f("email").value.trim()}. Менеджер зв'яжеться, щоб допомогти з налаштуванням. (Це демо для портфоліо — листи не надсилаються.)`;
    form.reset(); form.hidden = true; done.hidden = false; $("button", done).focus();
  });
})();

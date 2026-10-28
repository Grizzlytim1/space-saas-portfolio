/* Space — behaviour shared by all pages (each block runs only if its markup exists) */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- toast ---------- */
  const toastEl = $("[data-toast]");
  let tt;
  const toast = (t) => { toastEl.textContent = t; toastEl.classList.add("is-on"); clearTimeout(tt); tt = setTimeout(() => toastEl.classList.remove("is-on"), 2600); };
  $$("[data-soon]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); toast("Ця сторінка ще в розробці — Space поки концепт для портфоліо."); }));

  /* ---------- starfield ---------- */
  const cv = $("[data-stars]");
  if (cv) {
    const cx = cv.getContext("2d");
    let stars = [], sw = 0, sh = 0, dpr = 1, raf;
    const drawStars = (t) => {
      cx.setTransform(dpr, 0, 0, dpr, 0, 0);
      cx.clearRect(0, 0, sw, sh);
      for (const s of stars) {
        if (!reduce) { s.y -= s.v; if (s.y < -2) s.y = sh + 2; }
        cx.globalAlpha = 0.25 + 0.75 * Math.abs(Math.sin(s.p + t / 1000 * s.s));
        cx.fillStyle = s.r > 1.1 ? "#e9ffb0" : "#fff";
        cx.beginPath(); cx.arc(s.x, s.y, s.r, 0, 6.283); cx.fill();
      }
    };
    const sizeStars = () => {
      dpr = Math.min(2, devicePixelRatio || 1);
      sw = cv.offsetWidth; sh = cv.offsetHeight;
      cv.width = sw * dpr; cv.height = sh * dpr;
      stars = Array.from({ length: Math.round(sw * sh / 5200) }, () => ({ x: Math.random() * sw, y: Math.random() * sh, r: Math.random() * 1.1 + 0.2, p: Math.random() * 6.28, s: 0.4 + Math.random() * 1.4, v: 0.02 + Math.random() * 0.08 }));
      drawStars(0);
    };
    const loop = (t) => { drawStars(t); raf = requestAnimationFrame(loop); };
    sizeStars();
    if (!reduce) new IntersectionObserver(([en]) => { cancelAnimationFrame(raf); if (en.isIntersecting) raf = requestAnimationFrame(loop); }).observe(cv);
    addEventListener("resize", sizeStars);
  }

  /* ---------- nav: solid after scroll, hides while scrolling down; burger on phones ---------- */
  const nav = $("[data-nav]"), burger = $("[data-burger]"), mnav = $("#mnav");
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    nav.classList.toggle("is-solid", y > 30);
    nav.classList.toggle("is-hidden", y > 400 && y > lastY && mnav.hidden);
    lastY = y;
  };
  addEventListener("scroll", onScroll, { passive: true });
  const setM = (open) => { mnav.hidden = !open; burger.setAttribute("aria-expanded", String(open)); burger.setAttribute("aria-label", open ? "Закрити меню" : "Відкрити меню"); };
  burger.addEventListener("click", () => setM(mnav.hidden));
  $$("#mnav a").forEach((a) => a.addEventListener("click", () => setM(false)));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !mnav.hidden) { setM(false); burger.focus(); } });
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
  $$("[data-logos]").forEach((l) => l.insertAdjacentHTML("beforeend", l.innerHTML.replace(/<span class="lg/g, '<span aria-hidden="true" class="lg')));

  /* ---------- fixed-size mock scaled to its column ---------- */
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
  if (slider) {
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
  }

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

  /* ---------- about: history timeline ---------- */
  const tl = $("[data-timeline]");
  if (tl) {
    const yb = $$("[data-year]", tl), yc = $$("[data-ycard]", tl), bar = $("[data-tl-bar]", tl);
    const pick = (i, focus) => {
      yb.forEach((b, k) => { b.setAttribute("aria-selected", String(k === i)); b.tabIndex = k === i ? 0 : -1; b.classList.toggle("is-past", k <= i); });
      yc.forEach((c, k) => c.classList.toggle("is-on", k === i));
      bar.style.transform = `scaleX(${yb.length > 1 ? i / (yb.length - 1) : 1})`;
      if (focus) yb[i].focus();
    };
    yb.forEach((b, i) => {
      b.addEventListener("click", () => pick(i));
      b.addEventListener("keydown", (e) => { const k = { ArrowRight: 1, ArrowLeft: -1 }[e.key]; if (k) { e.preventDefault(); pick(Math.max(0, Math.min(yb.length - 1, i + k)), true); } });
    });
    pick(yb.length - 1);
  }

  /* ---------- pricing: monthly / yearly toggle (no prices, only billing note) ---------- */
  const bill = $("[data-bill-toggle]");
  if (bill) {
    const btns = $$("[data-period]", bill);
    const setP = (p) => {
      btns.forEach((b) => b.setAttribute("aria-checked", String(b.dataset.period === p)));
      $$("[data-bill]").forEach((s) => { s.textContent = p === "year" ? "Річна оплата · знижка 20% до будь-якої пропозиції" : "Щомісячна оплата · підберемо під ваш обсяг"; });
      document.body.dataset.billing = p;
    };
    btns.forEach((b) => b.addEventListener("click", () => setP(b.dataset.period)));
    bill.addEventListener("keydown", (e) => { if (["ArrowLeft", "ArrowRight"].includes(e.key)) { e.preventDefault(); const n = btns.find((b) => b.getAttribute("aria-checked") === "false"); setP(n.dataset.period); n.focus(); } });
    setP("month");
  }

  /* ---------- form validation (modal + contact page) ---------- */
  const emailOk = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim());
  function validate(form, rules) {
    const f = (n) => form.elements.namedItem(n), err = $("[data-err]", form);
    const msgs = []; let first = null;
    rules.forEach(([n, ok, m]) => { const el = f(n); if (!el) return; const bad = !ok(el.value); el.setAttribute("aria-invalid", String(bad)); if (bad) { msgs.push(m); first = first || el; } });
    err.textContent = msgs.join(" ");
    if (first) first.focus();
    return !first;
  }

  /* contact modal (opened by every "Почати / Дізнатися ціну" button) */
  const modal = $("[data-modal]");
  const box = $(".modal__box", modal), mform = $("[data-form]", modal), mdone = $("[data-done]", modal), mtitle = $("#m-title", modal);
  let opener = null, plan = "";
  const openM = (from) => {
    opener = from; plan = from.dataset.plan || "";
    mtitle.textContent = plan ? `Тариф «${plan}»: дізнайтеся ціну` : "Почнімо роботу зі Space";
    modal.hidden = false; document.documentElement.classList.add("no-scroll"); mform.hidden = false; mdone.hidden = true;
    setTimeout(() => mform.elements.namedItem("name").focus(), 50);
  };
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
  mform.addEventListener("submit", (e) => {
    e.preventDefault();
    const ok = validate(mform, [["name", (v) => v.trim().length >= 2, "Вкажіть ім'я."], ["email", emailOk, "Перевірте email."], ["size", (v) => !!v, "Оберіть розмір команди."]]);
    if (!ok) return;
    const f = (n) => mform.elements.namedItem(n).value.trim();
    $("[data-done-text]", modal).textContent = plan
      ? `Демо: ${f("name")}, так виглядала б заявка на тариф «${plan}». Насправді нічого не оформлено, гроші не списано, лист на ${f("email")} не надіслано.`
      : `Демо: ${f("name")}, так виглядала б реєстрація. Насправді акаунт не створено й лист на ${f("email")} не надіслано.`;
    mform.reset(); mform.hidden = true; mdone.hidden = false; $("button", mdone).focus();
  });

  /* contact page form */
  const pform = $('[data-form="page"]');
  if (pform) {
    const wrap = pform.parentElement, pdone = $("[data-done]", wrap);
    pform.addEventListener("submit", (e) => {
      e.preventDefault();
      const ok = validate(pform, [
        ["name", (v) => v.trim().length >= 2, "Вкажіть ім'я."],
        ["phone", (v) => { const p = v.replace(/[\s()-]/g, ""); return !p || /^\+?380\d{9}$/.test(p) || /^0\d{9}$/.test(p); }, "Телефон у форматі +380 XX XXX XX XX (або залиште порожнім)."],
        ["email", emailOk, "Перевірте email."],
        ["size", (v) => !!v, "Оберіть тему."],
        ["msg", (v) => v.trim().length >= 10, "Напишіть хоча б кілька слів."],
      ]);
      if (!ok) return;
      const f = (n) => pform.elements.namedItem(n).value.trim();
      $("[data-done-text]", wrap).textContent = `Демо: ${f("name")}, повідомлення нікуди не надіслано — це концепт для портфоліо, відповіді не буде.`;
      pform.reset(); pform.hidden = true; pdone.hidden = false; $("[data-reset]", wrap).focus();
    });
    $("[data-reset]", wrap).addEventListener("click", () => { pdone.hidden = true; pform.hidden = false; pform.elements.namedItem("name").focus(); });
  }
})();

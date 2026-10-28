"""Playwright checks for the Space site (5 pages).  Run:  python tests/test_site.py"""
import os
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SHOTS = ROOT / "tests" / "screenshots"
PORT = 8794
URL = f"http://localhost:{PORT}/"
results = []


def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("  ok  " if cond else "  FAIL") + f"  {name}" + (f"  — {detail}" if detail and not cond else ""))


def run():
    SHOTS.mkdir(parents=True, exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT)], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for w, h in [(1440, 900), (768, 1024), (375, 812)]:
                print(f"\n— viewport {w}×{h}")
                page = browser.new_page(viewport={"width": w, "height": h}, locale="uk-UA")
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.on("console", lambda m: m.type == "error" and errors.append(m.text))
                page.goto(URL + "features.html", wait_until="networkidle")
                page.add_style_tag(content="html{scroll-behavior:auto!important}")
                page.evaluate("async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); }")
                page.wait_for_timeout(500)
                check(f"{w}: no JS errors", not errors, "; ".join(errors))
                sw = page.evaluate("document.documentElement.scrollWidth")
                check(f"{w}: no horizontal overflow", sw <= w, f"scrollWidth {sw}")
                broken = page.evaluate("[...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src)")
                check(f"{w}: images load", not broken, ", ".join(broken))
                check(f"{w}: Inter loaded (Cyrillic)", page.evaluate("document.fonts.check('600 40px Inter', 'Простір')"))
                missing = page.evaluate("[...document.querySelectorAll('a[href^=\"#\"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1 && !document.querySelector(h))")
                check(f"{w}: anchors have targets", not missing, ", ".join(missing))
                check(f"{w}: stars canvas drawn", page.evaluate("(() => { const c = document.querySelector('[data-stars]'); const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 64) if (d[i]) n++; return n > 20; })()"))
                page.screenshot(path=str(SHOTS / f"hero-{w}.png"))

                # navigation
                if w > 860:
                    page.evaluate("scrollTo(0, 1500)"); page.wait_for_timeout(100)
                    page.evaluate("scrollTo(0, 2200)"); page.wait_for_timeout(500)
                    check(f"{w}: nav hides while scrolling down", "is-hidden" in page.get_attribute("[data-nav]", "class"))
                    page.evaluate("scrollTo(0, 1900)"); page.wait_for_timeout(500)
                    cls = page.get_attribute("[data-nav]", "class")
                    check(f"{w}: nav returns (solid) on scroll up", "is-hidden" not in cls and "is-solid" in cls)
                else:
                    page.click("[data-burger]")
                    check(f"{w}: burger opens mobile nav", page.is_visible("#mnav") and page.get_attribute("[data-burger]", "aria-expanded") == "true")
                    check(f"{w}: mobile nav lists 5 pages", page.locator("#mnav a[href$='.html']").count() == 6)
                    page.click("[data-burger]")
                    check(f"{w}: burger closes menu", page.is_hidden("#mnav"))

                # counters
                page.locator(".stat").first.scroll_into_view_if_needed()
                page.wait_for_timeout(2400)
                ty = page.evaluate("[...document.querySelectorAll('[data-odo=\"98\"] .odo__d')].map(d => d.style.transform)")
                check(f"{w}: rolling counter reaches 98", ty == ["translateY(-9em)", "translateY(-8em)"], str(ty))
                check(f"{w}: logo marquee duplicated", page.locator("[data-logos] .lg").count() == 14)

                # editor mock scales to its column
                sc = page.evaluate("(() => { const b = document.querySelector('[data-scaler]'), e = b.firstElementChild.getBoundingClientRect(); return [Math.round(e.width), Math.round(b.clientWidth)]; })()")
                check(f"{w}: editor mock fits its column", abs(sc[0] - sc[1]) <= 2, str(sc))

                # tabs
                page.locator("#t-team").scroll_into_view_if_needed()
                page.click("#t-team")
                check(f"{w}: tab shows its panel", page.is_visible("#p-team") and page.is_hidden("#p-assets"))
                page.focus("#t-team"); page.keyboard.press("ArrowRight")
                check(f"{w}: arrow key moves to next tab", page.get_attribute("#t-money", "aria-selected") == "true" and page.is_visible("#p-money"))
                page.keyboard.press("Home")
                check(f"{w}: Home key returns to first tab", page.is_visible("#p-assets"))

                # slider
                page.locator("[data-slider]").scroll_into_view_if_needed()
                page.click("[data-next]")
                page.wait_for_timeout(700)
                on = page.evaluate("[...document.querySelectorAll('.rv')].findIndex(r => r.classList.contains('is-on'))")
                pic = page.evaluate("[...document.querySelectorAll('.slider__photos img')].findIndex(r => r.classList.contains('is-on'))")
                check(f"{w}: next shows 2nd review and photo", on == 1 and pic == 1)
                page.click("[data-prev]"); page.click("[data-prev]")
                check(f"{w}: prev wraps to last review", page.evaluate("[...document.querySelectorAll('.rv')].findIndex(r => r.classList.contains('is-on'))") == 2)

                # faq
                page.locator("#q3").scroll_into_view_if_needed()
                page.click("#q3")
                check(f"{w}: FAQ opens clicked item", page.is_visible("#a3") and page.get_attribute("#q3", "aria-expanded") == "true")
                check(f"{w}: FAQ closes the others", page.is_hidden("#a1"))
                page.click("#q3")
                check(f"{w}: FAQ item toggles closed", page.is_hidden("#a3"))

                # contact modal
                page.locator(".cta [data-contact]").scroll_into_view_if_needed()
                page.click(".cta [data-contact]")
                page.wait_for_timeout(200)
                check(f"{w}: modal opens with focus in form", page.is_visible("[data-modal]") and page.evaluate("document.activeElement.name") == "name")
                page.click("[data-form] button[type=submit]")
                err = page.inner_text("[data-err]")
                check(f"{w}: empty form rejected", "ім'я" in err.lower() and "email" in err.lower(), err)
                page.fill("[data-form] input[name=name]", "Олена")
                page.fill("[data-form] input[name=email]", "olena@")
                page.select_option("[data-form] select[name=size]", "2–10 людей")
                page.click("[data-form] button[type=submit]")
                check(f"{w}: bad email rejected", page.get_attribute("[data-form] input[name=email]", "aria-invalid") == "true")
                page.fill("[data-form] input[name=email]", "olena@company.ua")
                page.click("[data-form] button[type=submit]")
                check(f"{w}: success message shown", page.is_visible("[data-done]") and "olena@company.ua" in page.inner_text("[data-done]"))
                page.screenshot(path=str(SHOTS / f"modal-{w}.png"))
                page.keyboard.press("Escape")
                check(f"{w}: Escape closes modal", page.is_hidden("[data-modal]"))
                page.locator("[data-soon] >> nth=0").scroll_into_view_if_needed()
                page.click("[data-soon] >> nth=0")
                check(f"{w}: placeholder links show a toast", "розробці" in page.inner_text("[data-toast]"))
                check(f"{w}: placeholder phone", "+380 00 000 00 00" in page.inner_text("footer"))
                page.close()
                # ---------- other pages ----------
                for path in ["index.html", "about.html", "pricing.html", "contact.html"]:
                    errs = []
                    pg = browser.new_page(viewport={"width": w, "height": h}, locale="uk-UA")
                    pg.on("pageerror", lambda e: errs.append(str(e)))
                    pg.on("console", lambda m: m.type == "error" and errs.append(m.text))
                    pg.goto(URL + path, wait_until="networkidle")
                    pg.add_style_tag(content="html{scroll-behavior:auto!important}")
                    check(f"{w} {path}: no JS errors", not errs, "; ".join(errs))
                    sw = pg.evaluate("document.documentElement.scrollWidth")
                    check(f"{w} {path}: no horizontal overflow", sw <= w, f"scrollWidth {sw}")
                    check(f"{w} {path}: images load", not pg.evaluate("[...document.images].filter(i => (i.loading !== 'lazy' || i.getBoundingClientRect().top < innerHeight) && (!i.complete || !i.naturalWidth)).length"))
                    check(f"{w} {path}: one h1 + current nav item", pg.locator("h1").count() == 1 and pg.get_attribute(".nav__links a[aria-current=page]", "href") == path)
                    if path == "index.html" and w > 860:
                        pg.click(".nav__links a[href='pricing.html']")
                        pg.wait_for_load_state()
                        check(f"{w}: nav link opens pricing page", pg.url.endswith("pricing.html"))
                        pg.click(".nav__cta")
                        pg.wait_for_load_state()
                        check(f"{w}: 'Зв'язатися' opens contact page", pg.url.endswith("contact.html"))
                    if path == "about.html":
                        pg.locator("[data-year='1']").scroll_into_view_if_needed()
                        pg.click("[data-year='1']")
                        pg.wait_for_timeout(600)
                        check(f"{w} about: timeline shows chosen year", pg.locator("[data-ycard='1']").is_visible() and "2021" in pg.inner_text(".tl__card.is-on"))
                        check(f"{w} about: 10 team members", pg.locator(".person").count() == 10)
                    if path == "pricing.html":
                        check(f"{w} pricing: 3 plans, no numeric prices", pg.locator(".plan").count() == 3 and "₴" not in pg.inner_text(".plans") and "$" not in pg.inner_text(".plans"))
                        pg.click("[data-period='year']")
                        check(f"{w} pricing: yearly toggle updates billing note", "Річна" in pg.inner_text(".plan [data-bill]") and pg.get_attribute("[data-period='year']", "aria-checked") == "true")
                        pg.locator(".plan--pop [data-contact]").scroll_into_view_if_needed()
                        pg.click(".plan--pop [data-contact]")
                        pg.wait_for_timeout(200)
                        check(f"{w} pricing: plan button opens modal for that plan", pg.is_visible("[data-modal]") and "Бізнес" in pg.inner_text("#m-title"))
                        pg.fill("[data-form] input[name=name]", "Ігор")
                        pg.fill("[data-form] input[name=email]", "igor@shop.ua")
                        pg.select_option("[data-form] select[name=size]", "11–50 людей")
                        pg.click("[data-form] button[type=submit]")
                        check(f"{w} pricing: request confirmed for plan", "«Бізнес»" in pg.inner_text("[data-done]"))
                        pg.keyboard.press("Escape")
                        check(f"{w} pricing: comparison table has 9 rows", pg.locator(".compare__table tbody tr").count() == 9)
                    if path == "contact.html":
                        f = "[data-form=page]"
                        pg.click(f + " button[type=submit]")
                        check(f"{w} contact: empty form rejected", pg.get_attribute(f + " input[name=email]", "aria-invalid") == "true" and pg.inner_text(f + " [data-err]") != "")
                        pg.fill(f + " input[name=name]", "Марта")
                        pg.fill(f + " input[name=phone]", "123")
                        pg.fill(f + " input[name=email]", "marta@agency.ua")
                        pg.select_option(f + " select[name=size]", "Демонстрація продукту")
                        pg.fill(f + " textarea[name=msg]", "Хочемо демо для трьох ФОП і ТОВ.")
                        pg.click(f + " button[type=submit]")
                        check(f"{w} contact: bad phone rejected", pg.get_attribute(f + " input[name=phone]", "aria-invalid") == "true")
                        pg.fill(f + " input[name=phone]", "+380 50 123 45 67")
                        pg.click(f + " button[type=submit]")
                        check(f"{w} contact: message confirmed", pg.locator(".cform [data-done]").is_visible() and "Демо" in pg.inner_text(".cform [data-done]"))
                        pg.screenshot(path=str(SHOTS / f"contact-{w}.png"))
                    pg.close()

            browser.close()
    finally:
        srv.terminate()
    failed = [n for n, ok in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(run())

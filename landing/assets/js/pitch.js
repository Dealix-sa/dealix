/* Dealix Pitch Deck — standalone renderer.
 * Loads pitch-content.json, renders bilingual slides, and drives
 * deck/scroll modes, keyboard navigation, language toggle and PDF export.
 * No dependencies.
 */
(function () {
  "use strict";

  var DATA_URL = "/assets/data/pitch-content.json";

  var state = {
    data: null,
    lang: "ar",
    mode: "deck",
    index: 0
  };

  var els = {};

  /* ── helpers ──────────────────────────────────────────────────── */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function ui(key) {
    return state.data.ui[state.lang][key];
  }
  function isRTL() {
    return state.lang === "ar";
  }

  /* ── block renderers ──────────────────────────────────────────── */
  function renderKpis(b) {
    var grid = el("div", "pitch-kpis");
    b.items.forEach(function (it) {
      var c = el("div", "pitch-kpi");
      c.appendChild(el("div", "pitch-kpi__num", it.num));
      c.appendChild(el("div", "pitch-kpi__label", it.label));
      if (it.note) c.appendChild(el("div", "pitch-kpi__note", it.note));
      grid.appendChild(c);
    });
    return grid;
  }

  function renderCards(b) {
    var grid = el("div", "pitch-cards" + (b.tone === "danger" ? " pitch-cards--danger" : ""));
    b.items.forEach(function (it) {
      var c = el("div", "pitch-card");
      if (it.icon) c.appendChild(el("div", "pitch-card__icon", it.icon));
      var head = el("div", "pitch-card__head");
      head.appendChild(el("h3", "pitch-card__title", it.title));
      if (it.stat) head.appendChild(el("span", "pitch-card__stat", it.stat));
      c.appendChild(head);
      c.appendChild(el("p", "pitch-card__desc", it.desc));
      grid.appendChild(c);
    });
    return grid;
  }

  function renderFlow(b) {
    var grid = el("div", "pitch-flow");
    b.items.forEach(function (it, i) {
      var s = el("div", "pitch-flow__step");
      s.appendChild(el("div", "pitch-flow__icon", it.icon));
      s.appendChild(el("h3", "pitch-flow__title", it.title));
      s.appendChild(el("p", "pitch-flow__desc", it.desc));
      grid.appendChild(s);
      if (i < b.items.length - 1) grid.appendChild(el("div", "pitch-flow__arrow", "→"));
    });
    return grid;
  }

  function renderSteps(b) {
    var grid = el("div", "pitch-steps");
    b.items.forEach(function (it) {
      var s = el("div", "pitch-step");
      s.appendChild(el("span", "pitch-step__n", it.n));
      s.appendChild(el("h3", "pitch-step__title", it.title));
      s.appendChild(el("p", "pitch-step__desc", it.desc));
      grid.appendChild(s);
    });
    return grid;
  }

  function renderTable(b) {
    var wrap = el("div", "pitch-table-wrap");
    var t = el("table", "pitch-table");
    var thead = el("thead");
    var hr = el("tr");
    b.head.forEach(function (h, i) {
      var th = el("th", i === b.highlight ? "is-highlight" : null, h);
      hr.appendChild(th);
    });
    thead.appendChild(hr);
    t.appendChild(thead);
    var tbody = el("tbody");
    b.rows.forEach(function (row) {
      var tr = el("tr");
      row.forEach(function (cell, i) {
        tr.appendChild(el("td", i === b.highlight ? "is-highlight" : null, cell));
      });
      tbody.appendChild(tr);
    });
    t.appendChild(tbody);
    wrap.appendChild(t);
    return wrap;
  }

  function renderBars(b) {
    var box = el("div", "pitch-bars");
    b.items.forEach(function (it) {
      var row = el("div", "pitch-bar-row");
      row.appendChild(el("div", "pitch-bar-row__label", it.label));
      var track = el("div", "pitch-bar-row__track");
      track.appendChild(makeBar("before", it.before, it.beforePct));
      track.appendChild(makeBar("after", it.after, it.afterPct));
      row.appendChild(track);
      box.appendChild(row);
    });
    return box;
  }
  function makeBar(kind, val, pct) {
    var bar = el("div", "pitch-bar pitch-bar--" + kind);
    bar.appendChild(el("span", "pitch-bar__tag", kind === "before"
      ? (state.lang === "ar" ? "قبل" : "Before")
      : (state.lang === "ar" ? "بعد" : "After")));
    var meter = el("div", "pitch-bar__meter");
    meter.setAttribute("data-w", Math.max(2, pct) + "%");
    meter.style.width = "0%";
    bar.appendChild(meter);
    bar.appendChild(el("span", "pitch-bar__val", val));
    return bar;
  }

  function renderRoi(b) {
    var grid = el("div", "pitch-roi");
    b.cols.forEach(function (col) {
      var c = el("div", "pitch-roi__col pitch-roi__col--" + (col.tone || "ok"));
      c.appendChild(el("div", "pitch-roi__label", col.label));
      var v = el("div", "pitch-roi__value", col.value);
      c.appendChild(v);
      c.appendChild(el("div", "pitch-roi__unit", b.unit));
      var mt = el("div", "pitch-roi__meter-track");
      var m = el("div", "pitch-roi__meter");
      m.setAttribute("data-w", Math.max(3, col.pct) + "%");
      m.style.width = "0%";
      mt.appendChild(m);
      c.appendChild(mt);
      if (col.items) {
        var ul = el("ul", "pitch-roi__items");
        col.items.forEach(function (x) { ul.appendChild(el("li", null, x)); });
        c.appendChild(ul);
      }
      grid.appendChild(c);
    });
    if (b.delta) {
      var d = el("div", "pitch-roi__delta");
      d.appendChild(el("span", "pitch-roi__delta-label", b.delta.label));
      d.appendChild(el("span", "pitch-roi__delta-value", b.delta.value));
      grid.appendChild(d);
    }
    return grid;
  }

  function renderGates(b) {
    var grid = el("div", "pitch-gates");
    b.items.forEach(function (it) {
      var g = el("div", "pitch-gate");
      g.appendChild(el("span", "pitch-gate__lock", "🔒"));
      var body = el("div", "pitch-gate__body");
      body.appendChild(el("span", "pitch-gate__code", it.code));
      body.appendChild(el("span", "pitch-gate__label", it.label));
      g.appendChild(body);
      grid.appendChild(g);
    });
    return grid;
  }

  function renderPricing(b) {
    var grid = el("div", "pitch-pricing");
    b.items.forEach(function (it) {
      var c = el("div", "pitch-price" + (it.featured ? " pitch-price--featured" : ""));
      if (it.badge) c.appendChild(el("span", "pitch-price__badge", it.badge));
      c.appendChild(el("span", "pitch-price__tier", it.tier));
      c.appendChild(el("h3", "pitch-price__name", it.name));
      var p = el("div", "pitch-price__price", it.price);
      if (it.period) p.appendChild(el("span", "pitch-price__period", it.period));
      c.appendChild(p);
      var ul = el("ul", "pitch-price__list");
      it.items.forEach(function (x) { ul.appendChild(el("li", null, x)); });
      c.appendChild(ul);
      grid.appendChild(c);
    });
    return grid;
  }

  function renderBullets(b) {
    var box = el("div", "pitch-bullets");
    if (b.title) box.appendChild(el("h3", "pitch-bullets__title", b.title));
    var ul = el("ul", "pitch-bullets__list");
    b.items.forEach(function (x) { ul.appendChild(el("li", null, x)); });
    box.appendChild(ul);
    return box;
  }

  function renderNote(b) {
    return el("div", "pitch-note", b.text);
  }

  var BLOCKS = {
    kpis: renderKpis,
    cards: renderCards,
    flow: renderFlow,
    steps: renderSteps,
    table: renderTable,
    bars: renderBars,
    roi: renderRoi,
    gates: renderGates,
    pricing: renderPricing,
    bullets: renderBullets,
    note: renderNote
  };

  /* ── slide renderers ──────────────────────────────────────────── */
  function renderSlide(slide) {
    var c = slide[state.lang];
    var sec = el("section", "pitch-slide");
    sec.id = "slide-" + slide.id;
    sec.setAttribute("aria-roledescription", "slide");

    if (slide.layout === "cover") {
      sec.className += " pitch-slide--cover";
      sec.appendChild(el("div", "pitch-cover__kicker", c.kicker));
      sec.appendChild(el("h1", "pitch-cover__title", c.title));
      sec.appendChild(el("h2", "pitch-cover__headline", c.headline));
      sec.appendChild(el("p", "pitch-cover__subtitle", c.subtitle));
      sec.appendChild(el("div", "pitch-cover__meta", c.meta));
      var tags = el("div", "pitch-cover__tags");
      (c.tags || []).forEach(function (t) { tags.appendChild(el("span", "pitch-cover__tag", t)); });
      sec.appendChild(tags);
      return sec;
    }

    if (c.eyebrow) sec.appendChild(el("span", "pitch-eyebrow", c.eyebrow));
    sec.appendChild(el("h2", "pitch-title", c.title));
    if (c.subtitle) sec.appendChild(el("p", "pitch-subtitle", c.subtitle));

    if (slide.layout === "cta") {
      sec.className += " pitch-slide--cta";
      var btns = el("div", "pitch-cta__buttons");
      (c.buttons || []).forEach(function (btn) {
        var a = el("a", "pitch-cta__btn" + (btn.primary ? " pitch-cta__btn--primary" : ""), btn.label);
        a.href = btn.href;
        btns.appendChild(a);
      });
      sec.appendChild(btns);
      if (c.contact) sec.appendChild(el("div", "pitch-cta__contact", c.contact));
      return sec;
    }

    var body = el("div", "pitch-slide__body");
    (c.blocks || []).forEach(function (b) {
      var fn = BLOCKS[b.type];
      if (fn) body.appendChild(fn(b));
    });
    sec.appendChild(body);
    return sec;
  }

  /* ── full render ──────────────────────────────────────────────── */
  function render() {
    var doc = document.documentElement;
    doc.lang = state.lang;
    doc.dir = isRTL() ? "rtl" : "ltr";
    document.title = state.lang === "ar"
      ? "Dealix — العرض التقديمي"
      : "Dealix — Pitch Deck";

    els.stage.innerHTML = "";
    state.data.slides.forEach(function (slide, i) {
      var node = renderSlide(slide);
      node.setAttribute("data-i", i);
      els.stage.appendChild(node);
    });

    els.langBtn.textContent = ui("lang");
    els.pdfBtn.lastChild.textContent = " " + ui("pdf");
    els.prevBtn.setAttribute("aria-label", ui("prev"));
    els.nextBtn.setAttribute("aria-label", ui("next"));
    els.deckSeg.textContent = ui("deck");
    els.scrollSeg.textContent = ui("scroll");
    els.hint.textContent = ui("scroll_hint");

    buildDots();
    applyMode();
    goTo(state.index, true);
    syncUrl();
  }

  function buildDots() {
    els.dots.innerHTML = "";
    state.data.slides.forEach(function (slide, i) {
      var d = el("button", "pitch__dot");
      d.type = "button";
      d.setAttribute("aria-label", (i + 1) + " " + ui("of") + " " + state.data.slides.length);
      d.addEventListener("click", function () { goTo(i); });
      els.dots.appendChild(d);
    });
  }

  function applyMode() {
    els.root.setAttribute("data-mode", state.mode);
    els.deckSeg.setAttribute("aria-pressed", String(state.mode === "deck"));
    els.scrollSeg.setAttribute("aria-pressed", String(state.mode === "scroll"));
  }

  function slideEls() {
    return els.stage.querySelectorAll(".pitch-slide");
  }

  function goTo(i, force) {
    var total = state.data.slides.length;
    i = Math.max(0, Math.min(total - 1, i));
    if (i === state.index && !force) {
      if (state.mode === "deck") return;
    }
    state.index = i;
    var slides = slideEls();
    slides.forEach(function (s, idx) {
      s.classList.toggle("is-active", idx === i);
    });
    var dots = els.dots.querySelectorAll(".pitch__dot");
    dots.forEach(function (d, idx) {
      d.classList.toggle("is-active", idx === i);
    });
    els.counter.textContent = (i + 1) + " / " + total;
    els.progressFill.style.width = ((i + 1) / total * 100) + "%";
    els.prevBtn.disabled = i === 0;
    els.nextBtn.disabled = i === total - 1;

    if (state.mode === "deck") {
      animateMeters(slides[i]);
      window.scrollTo({ top: 0, behavior: force ? "auto" : "smooth" });
    } else {
      slides[i].scrollIntoView({ behavior: force ? "auto" : "smooth", block: "start" });
    }
    syncUrl();
  }

  function animateMeters(slide) {
    if (!slide) return;
    var meters = slide.querySelectorAll("[data-w]");
    meters.forEach(function (m) { m.style.width = "0%"; });
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        meters.forEach(function (m) { m.style.width = m.getAttribute("data-w"); });
      });
    });
  }

  function setMode(mode) {
    state.mode = mode;
    applyMode();
    if (mode === "deck") {
      goTo(state.index, true);
    } else {
      slideEls().forEach(function (s) {
        animateMeters(s);
      });
    }
    syncUrl();
  }

  function syncUrl() {
    var q = "?lang=" + state.lang + "&mode=" + state.mode +
      (state.mode === "deck" ? "&s=" + (state.index + 1) : "");
    history.replaceState(null, "", q);
  }

  /* ── controls shell ───────────────────────────────────────────── */
  function buildShell() {
    var root = el("div", "pitch");
    root.setAttribute("data-mode", "deck");

    var bar = el("div", "pitch__bar");
    var brand = el("div", "pitch__brand");
    brand.appendChild(el("span", "pitch__brand-dot"));
    brand.appendChild(el("span", null, "Dealix"));
    bar.appendChild(brand);
    bar.appendChild(el("div", "pitch__spacer"));

    var seg = el("div", "pitch__seg");
    els.deckSeg = el("button", null, "Slides");
    els.deckSeg.type = "button";
    els.scrollSeg = el("button", null, "Scroll");
    els.scrollSeg.type = "button";
    els.deckSeg.addEventListener("click", function () { setMode("deck"); });
    els.scrollSeg.addEventListener("click", function () { setMode("scroll"); });
    seg.appendChild(els.deckSeg);
    seg.appendChild(els.scrollSeg);
    bar.appendChild(seg);

    var controls = el("div", "pitch__controls");
    els.langBtn = el("button", "pitch__btn", "English");
    els.langBtn.type = "button";
    els.langBtn.addEventListener("click", toggleLang);
    controls.appendChild(els.langBtn);

    els.pdfBtn = el("button", "pitch__btn pitch__btn--primary");
    els.pdfBtn.type = "button";
    els.pdfBtn.appendChild(el("span", null, "↓"));
    els.pdfBtn.appendChild(document.createTextNode(" Export PDF"));
    els.pdfBtn.addEventListener("click", exportPdf);
    controls.appendChild(els.pdfBtn);
    bar.appendChild(controls);
    root.appendChild(bar);

    var progress = el("div", "pitch__progress");
    els.progressFill = el("div", "pitch__progress-fill");
    progress.appendChild(els.progressFill);
    root.appendChild(progress);

    els.stage = el("div", "pitch__stage");
    root.appendChild(els.stage);

    els.hint = el("div", "pitch__scroll-hint", "");
    root.appendChild(els.hint);

    var nav = el("div", "pitch__nav");
    els.prevBtn = navBtn("prev");
    els.dots = el("div", "pitch__dots");
    els.counter = el("div", "pitch__counter", "1 / 1");
    els.nextBtn = navBtn("next");
    els.prevBtn.addEventListener("click", function () { goTo(state.index - 1); });
    els.nextBtn.addEventListener("click", function () { goTo(state.index + 1); });
    nav.appendChild(els.prevBtn);
    nav.appendChild(els.dots);
    nav.appendChild(els.counter);
    nav.appendChild(els.nextBtn);
    root.appendChild(nav);

    els.root = root;
    document.getElementById("pitch-root").appendChild(root);
  }

  function navBtn(dir) {
    var b = el("button", "pitch__nav-btn");
    b.type = "button";
    b.innerHTML = dir === "prev"
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>';
    return b;
  }

  function toggleLang() {
    state.lang = state.lang === "ar" ? "en" : "ar";
    render();
  }

  function exportPdf() {
    var prevMode = state.mode;
    window.print();
    // restore is automatic; print CSS shows all slides regardless of mode
    void prevMode;
  }

  /* ── keyboard ─────────────────────────────────────────────────── */
  function onKey(e) {
    if (state.mode !== "deck") return;
    var fwd = isRTL() ? "ArrowLeft" : "ArrowRight";
    var back = isRTL() ? "ArrowRight" : "ArrowLeft";
    if (e.key === fwd || e.key === " " || e.key === "PageDown") {
      e.preventDefault();
      goTo(state.index + 1);
    } else if (e.key === back || e.key === "PageUp") {
      e.preventDefault();
      goTo(state.index - 1);
    } else if (e.key === "Home") {
      e.preventDefault();
      goTo(0);
    } else if (e.key === "End") {
      e.preventDefault();
      goTo(state.data.slides.length - 1);
    }
  }

  /* ── init ─────────────────────────────────────────────────────── */
  function readUrl() {
    var p = new URLSearchParams(location.search);
    if (p.get("lang") === "en" || p.get("lang") === "ar") state.lang = p.get("lang");
    if (p.get("mode") === "scroll" || p.get("mode") === "deck") state.mode = p.get("mode");
    var s = parseInt(p.get("s"), 10);
    if (!isNaN(s) && s > 0) state.index = s - 1;
  }

  function init() {
    readUrl();
    buildShell();
    fetch(DATA_URL)
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        state.data = data;
        if (state.index >= data.slides.length) state.index = 0;
        render();
        document.addEventListener("keydown", onKey);
      })
      .catch(function (err) {
        els.stage.appendChild(el("p", "pitch-note",
          "تعذّر تحميل محتوى العرض / Failed to load presentation content: " + err.message));
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

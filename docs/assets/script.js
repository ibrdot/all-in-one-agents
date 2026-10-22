/* all-in-one-agents — vanilla ES6, no libraries */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var hasIO = "IntersectionObserver" in window;

  /* ---------- scroll reveal: add .in-view once, then stop observing ---------- */
  var revealEls = document.querySelectorAll(".reveal");

  if (reduceMotion || !hasIO) {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  } else {
    // apply immediately — gating content visibility on requestAnimationFrame
    // leaves sections permanently hidden where rAF is stalled
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          observer.unobserve(entry.target);
          entry.target.classList.add("in-view");
        }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });

    revealEls.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- one rAF-throttled scroll handler: topbar blur + progress bar ---------- */
  var nav = document.getElementById("site-nav");
  var progress = document.querySelector(".scroll-progress");
  var scrollTick = false;

  function onScroll() {
    if (nav) nav.classList.toggle("scrolled", window.scrollY > 8);
    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var ratio = max > 0 ? Math.min(window.scrollY / max, 1) : 0;
      progress.style.transform = "scaleX(" + ratio + ")";
    }
  }
  window.addEventListener("scroll", function () {
    if (!scrollTick) {
      scrollTick = true;
      requestAnimationFrame(function () { scrollTick = false; onScroll(); });
    }
  }, { passive: true });
  onScroll();

  /* ---------- rail scrollspy: highlight the section in view ---------- */
  var spyLinks = Array.prototype.slice.call(
    document.querySelectorAll('.rail-nav a[href^="#"]')
  );
  if (spyLinks.length && hasIO) {
    var linkFor = {};
    spyLinks.forEach(function (a) { linkFor[a.getAttribute("href").slice(1)] = a; });

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var link = linkFor[entry.target.id];
        if (!link) return;
        if (entry.isIntersecting) {
          spyLinks.forEach(function (a) { a.classList.remove("active"); });
          link.classList.add("active");
        }
      });
    }, { rootMargin: "-30% 0px -55% 0px" });

    ["loop", "solves", "features", "install", "structure"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el);
    });
  }

  /* ---------- copy to clipboard (with legacy fallback) ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy") ? resolve() : reject(new Error("execCommand failed"));
      } catch (err) {
        reject(err);
      } finally {
        document.body.removeChild(ta);
      }
    });
  }

  var copyBtn = document.getElementById("copy-install");
  if (copyBtn) {
    var resetTimer = null;
    copyBtn.addEventListener("click", function () {
      var codeEl = document.getElementById("install-cmd");
      // dataset.copy holds the prompt-free command text (prompts are visual only)
      var text = (codeEl.dataset && codeEl.dataset.copy) ? codeEl.dataset.copy : codeEl.innerText;
      copyText(text).then(function () {
        copyBtn.textContent = "copied!";
        copyBtn.classList.add("copied");
        clearTimeout(resetTimer);
        resetTimer = setTimeout(function () {
          copyBtn.textContent = "copy";
          copyBtn.classList.remove("copied");
        }, 2000);
      });
    });
  }

  /* ---------- mobile nav: toggle, focus trap, escape, click-outside ---------- */
  var toggle = document.getElementById("nav-toggle");
  var menu = document.getElementById("nav-menu");

  function menuLinks() {
    return Array.prototype.slice.call(menu.querySelectorAll("a"));
  }

  function openMenu() {
    toggle.setAttribute("aria-expanded", "true");
    menu.hidden = false;
    document.body.classList.add("menu-open");
    var links = menuLinks();
    if (links.length) links[0].focus();
  }

  function closeMenu(returnFocus) {
    toggle.setAttribute("aria-expanded", "false");
    menu.hidden = true;
    document.body.classList.remove("menu-open");
    if (returnFocus) toggle.focus();
  }

  function isOpen() {
    return toggle.getAttribute("aria-expanded") === "true";
  }

  toggle.addEventListener("click", function () {
    isOpen() ? closeMenu(false) : openMenu();
  });

  document.addEventListener("keydown", function (e) {
    if (!isOpen()) return;

    if (e.key === "Escape") {
      closeMenu(true);
      return;
    }

    // keep Tab cycling inside toggle + menu while open
    if (e.key === "Tab") {
      var focusables = [toggle].concat(menuLinks());
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      var active = document.activeElement;

      if (focusables.indexOf(active) === -1) {
        e.preventDefault();
        first.focus();
      } else if (e.shiftKey && active === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && active === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });

  document.addEventListener("click", function (e) {
    if (isOpen() && !menu.contains(e.target) && !toggle.contains(e.target)) {
      closeMenu(false);
    }
  });

  // close after navigating to an anchor
  menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) closeMenu(false);
  });

  // leaving the mobile breakpoint while open -> reset state
  window.matchMedia("(min-width: 1100px)").addEventListener("change", function (e) {
    if (e.matches && isOpen()) closeMenu(false);
  });

  /* ---------- custom terminal cursor: accent dot + lagging ring ---------- */
  var dot = document.querySelector(".cursor-dot");
  var ring = document.querySelector(".cursor-ring");
  var glow = document.querySelector(".mouse-glow");

  if (finePointer && !reduceMotion && dot && ring) {
    var tx = -100, ty = -100, rx = -100, ry = -100, shown = false;

    document.addEventListener("mousemove", function (e) {
      tx = e.clientX;
      ty = e.clientY;
      if (glow) {
        glow.style.setProperty("--mx", tx + "px");
        glow.style.setProperty("--my", ty + "px");
        glow.classList.add("is-on");
      }
      if (!shown) {
        shown = true;
        rx = tx; ry = ty;
        dot.classList.add("cursor-visible");
        ring.classList.add("cursor-visible");
      }
    }, { passive: true });

    // spotlight position inside hovered cells/stages
    document.addEventListener("mousemove", function (e) {
      var cell = e.target.closest && e.target.closest(".bento-cell, .stage");
      if (!cell) return;
      var r = cell.getBoundingClientRect();
      cell.style.setProperty("--cx", (e.clientX - r.left) + "px");
      cell.style.setProperty("--cy", (e.clientY - r.top) + "px");
    }, { passive: true });

    document.addEventListener("mouseover", function (e) {
      ring.classList.toggle(
        "cursor-hover",
        !!(e.target.closest && e.target.closest("a, button"))
      );
    }, { passive: true });

    document.documentElement.addEventListener("mouseleave", function () {
      shown = false;
      dot.classList.remove("cursor-visible");
      ring.classList.remove("cursor-visible");
    });

    (function cursorLoop() {
      rx += (tx - rx) * 0.16;
      ry += (ty - ry) * 0.16;
      dot.style.transform = "translate3d(" + (tx - 4) + "px," + (ty - 4) + "px,0)";
      var half = ring.offsetWidth / 2;
      ring.style.transform = "translate3d(" + (rx - half) + "px," + (ry - half) + "px,0)";
      requestAnimationFrame(cursorLoop);
    })();
  }

  /* ---------- hero eyebrow typewriter ---------- */
  var eyebrow = document.getElementById("hero-eyebrow");
  if (eyebrow && !reduceMotion) {
    var finalHTML = eyebrow.innerHTML;
    var plain = eyebrow.textContent;
    eyebrow.textContent = "";
    var tw = 0;
    var twTimer = setInterval(function () {
      tw++;
      eyebrow.textContent = plain.slice(0, tw);
      if (tw >= plain.length) {
        clearInterval(twTimer);
        eyebrow.innerHTML = finalHTML;
      }
    }, 26);
  }

  /* ---------- stats count-up when scrolled into view ---------- */
  var statNums = Array.prototype.slice.call(document.querySelectorAll(".stat-num"));
  if (statNums.length && !reduceMotion && hasIO) {
    var statObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        statObserver.unobserve(entry.target);
        var el = entry.target;
        var target = parseInt(el.textContent, 10) || 0;
        var start = null;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / 1200, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased);
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    statNums.forEach(function (el) { statObserver.observe(el); });
  }

  /* ---------- terminal typing when the hero terminal is visible ---------- */
  var codeEl = document.getElementById("install-cmd");
  var terminal = document.querySelector(".terminal");
  var cmdLines = [
    { t: "git clone https://github.com/ibrorg/all-in-one-agents.git" },
    { t: "cd all-in-one-agents" },
    { t: "./install.sh claude --dry-run   ", c: "# preview" },
    { t: "./install.sh claude             ", c: "# install" }
  ];

  if (codeEl) {
    // prompt-free text for the copy button (prompts are typed visually only)
    codeEl.dataset.copy = cmdLines.map(function (l) { return l.t + (l.c ? l.c : ""); }).join("\n");
  }

  if (codeEl && terminal && !reduceMotion && hasIO) {
    var termObserver = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      termObserver.disconnect();

      codeEl.textContent = "";
      var caret = document.createElement("span");
      caret.className = "type-caret";
      caret.textContent = "▌";
      codeEl.appendChild(caret);

      var li = 0, ch = 0;
      var lineNode;

      function startLine() {
        var prompt = document.createElement("span");
        prompt.className = "prompt";
        prompt.textContent = "$ ";
        caret.before(prompt);
        lineNode = document.createTextNode("");
        caret.before(lineNode);
      }
      startLine();

      function tick() {
        var line = cmdLines[li];
        ch++;
        lineNode.data = line.t.slice(0, ch);
        if (ch < line.t.length) {
          setTimeout(tick, 14 + Math.random() * 22);
          return;
        }
        if (line.c) {
          var comment = document.createElement("span");
          comment.className = "comment";
          comment.textContent = line.c;
          caret.before(comment);
        }
        if (li >= cmdLines.length - 1) {
          caret.remove();
          return;
        }
        caret.before(document.createTextNode("\n"));
        li++;
        ch = 0;
        startLine();
        setTimeout(tick, 140);
      }
      tick();
    }, { threshold: 0.3 });
    termObserver.observe(terminal);
  }

  /* ---------- JS-driven smooth anchor scrolling ----------
     Native CSS/API smooth scrolling is cancelled instantly by some
     embedded webviews, so anchor clicks are tweened manually. */
  function smoothScrollTo(targetY, duration) {
    var startY = window.scrollY;
    var delta = targetY - startY;
    if (delta === 0) return;
    var start = null, done = false;
    function ease(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
    function frame(ts) {
      if (done) return;
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      window.scrollTo(0, Math.round(startY + delta * ease(p)));
      if (p < 1) requestAnimationFrame(frame);
      else done = true;
    }
    requestAnimationFrame(frame);
    // if rAF is stalled (embedded webviews, some power-save modes), jump
    setTimeout(function () {
      if (!done && start === null) { done = true; window.scrollTo(0, targetY); }
    }, 140);
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute("href").slice(1);
    if (!id) return;
    var target = document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    // 80px offset mirrors section[id] scroll-margin-top
    var top = Math.max(target.getBoundingClientRect().top + window.scrollY - 80, 0);
    if (reduceMotion) {
      window.scrollTo(0, top);
    } else {
      smoothScrollTo(top, 600);
    }
    history.pushState(null, "", "#" + id);
    // move focus to the section for keyboard/AT users without scrolling again
    target.setAttribute("tabindex", "-1");
    target.focus({ preventScroll: true });
  });
})();

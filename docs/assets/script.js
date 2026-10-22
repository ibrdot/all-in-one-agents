/* all-in-one-agents — vanilla ES6, no libraries */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- scroll reveal: add .in-view once, then stop observing ---------- */
  var revealEls = document.querySelectorAll(".reveal");

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in-view"); });
  } else {
    var scheduled = false;
    var pending = [];

    function flush() {
      scheduled = false;
      pending.forEach(function (el) { el.classList.add("in-view"); });
      pending = [];
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          observer.unobserve(entry.target);
          pending.push(entry.target);
        }
      });
      // batch class writes into one animation frame
      if (pending.length && !scheduled) {
        scheduled = true;
        requestAnimationFrame(flush);
      }
    }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });

    revealEls.forEach(function (el) { observer.observe(el); });
  }

  /* ---------- sticky nav blur after scrolling ---------- */
  var nav = document.getElementById("site-nav");

  function onScroll() {
    nav.classList.toggle("scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

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
      var text = document.getElementById("install-cmd").innerText;
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
    var links = menuLinks();
    if (links.length) links[0].focus();
  }

  function closeMenu(returnFocus) {
    toggle.setAttribute("aria-expanded", "false");
    menu.hidden = true;
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

  // leaving mobile breakpoint while open -> reset state
  window.matchMedia("(min-width: 768px)").addEventListener("change", function (e) {
    if (e.matches && isOpen()) closeMenu(false);
  });
})();

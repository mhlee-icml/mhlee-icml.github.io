/* Progressive enhancements: all content remains available without JavaScript. */
(() => {
  "use strict";
  document.documentElement.classList.add("js");
  const menuButton = document.querySelector(".nav-toggle");
  const menu = document.querySelector("#site-nav");
  if (menuButton && menu) {
    const closeMenu = () => {
      menu.classList.remove("is-open");
      menuButton.setAttribute("aria-expanded", "false");
    };
    menuButton.addEventListener("click", () => {
      const expanded = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!expanded));
      menu.classList.toggle("is-open", !expanded);
    });
    menu.addEventListener("click", event => {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && menu.classList.contains("is-open")) {
        closeMenu();
        menuButton.focus();
      }
    });
    const desktop = window.matchMedia("(min-width: 1021px)");
    desktop.addEventListener("change", event => {
      if (event.matches) closeMenu();
    });
  }

  const carousel = document.querySelector("[data-carousel]");
  if (carousel) {
    const viewport = carousel.querySelector("[data-carousel-viewport]");
    const track = carousel.querySelector("[data-carousel-track]");
    const slides = Array.from(carousel.querySelectorAll("[data-carousel-slide]"));
    const controls = carousel.querySelector("[data-carousel-controls]");
    const toggle = carousel.querySelector("[data-carousel-toggle]");
    const previous = carousel.querySelector("[data-carousel-prev]");
    const next = carousel.querySelector("[data-carousel-next]");
    const dots = Array.from(carousel.querySelectorAll("[data-carousel-go]"));
    const count = carousel.querySelector("[data-carousel-count]");
    const status = carousel.querySelector("[data-carousel-status]");

    if (viewport && track && slides.length > 1 && controls && toggle) {
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
      const hoverCapability = window.matchMedia("(hover: hover)");
      const focusableSelector = "a[href], button, input, select, textarea, [tabindex], [contenteditable='true'], audio[controls], video[controls], iframe";
      const focusableElements = slides.map(slide => Array.from(slide.querySelectorAll(focusableSelector)));
      const originalTabindex = new Map(focusableElements.flat().map(element => [element, element.getAttribute("tabindex")]));
      let index = 0;
      let userPaused = reducedMotion.matches;
      let hovered = hoverCapability.matches && carousel.matches(":hover");
      let focusWithin = carousel.contains(document.activeElement);
      let playWithToggleFocus = false;
      let inView = true;
      let timer = null;
      let touch = null;
      let touching = false;
      let suppressClickUntil = 0;

      const schedule = () => {
        window.clearTimeout(timer);
        timer = null;
        const focusAllowsPlayback = !focusWithin || (playWithToggleFocus && document.activeElement === toggle);
        if (!userPaused && !hovered && focusAllowsPlayback && !touching && !document.hidden && inView) {
          timer = window.setTimeout(() => show(index + 1), 5000);
        }
      };

      const render = (manual = false) => {
        // Keep focus visible when arrow keys or a swipe leave a focused slide.
        if (slides.some((slide, slideIndex) => slideIndex !== index && slide.contains(document.activeElement))) {
          viewport.focus({ preventScroll: true });
        }
        slides.forEach((slide, slideIndex) => {
          const active = slideIndex === index;
          slide.setAttribute("aria-hidden", String(!active));
          slide.inert = !active;
          slide.toggleAttribute("inert", !active);
          focusableElements[slideIndex].forEach(element => {
            const original = originalTabindex.get(element);
            if (!active) element.setAttribute("tabindex", "-1");
            else if (original === null) element.removeAttribute("tabindex");
            else element.setAttribute("tabindex", original);
          });
        });
        track.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach(dot => dot.setAttribute("aria-pressed", String(Number(dot.dataset.carouselGo) === index)));
        if (count) count.textContent = `${String(index + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
        if (manual && status) {
          status.textContent = `Slide ${index + 1} of ${slides.length}: ${slides[index].dataset.carouselTitle || "Research project"}`;
        }
      };

      const show = (requestedIndex, manual = false) => {
        index = (requestedIndex + slides.length) % slides.length;
        render(manual);
        schedule();
      };

      const syncToggle = () => {
        toggle.textContent = userPaused ? "Play" : "Pause";
        toggle.setAttribute("aria-label", userPaused ? "Play slideshow" : "Pause slideshow");
      };

      previous?.addEventListener("click", () => show(index - 1, true));
      next?.addEventListener("click", () => show(index + 1, true));
      dots.forEach(dot => {
        dot.addEventListener("click", () => {
          const requestedIndex = Number(dot.dataset.carouselGo);
          if (Number.isInteger(requestedIndex) && requestedIndex >= 0 && requestedIndex < slides.length) show(requestedIndex, true);
        });
      });
      toggle.addEventListener("click", () => {
        userPaused = !userPaused;
        playWithToggleFocus = !userPaused && document.activeElement === toggle;
        syncToggle();
        schedule();
      });
      carousel.addEventListener("mouseenter", () => { hovered = hoverCapability.matches; schedule(); });
      carousel.addEventListener("mouseleave", () => { hovered = false; schedule(); });
      hoverCapability.addEventListener("change", event => {
        hovered = event.matches && carousel.matches(":hover");
        schedule();
      });
      carousel.addEventListener("focusin", event => {
        focusWithin = true;
        if (event.target !== toggle) playWithToggleFocus = false;
        schedule();
      });
      carousel.addEventListener("focusout", event => {
        focusWithin = carousel.contains(event.relatedTarget);
        if (event.relatedTarget !== toggle) playWithToggleFocus = false;
        schedule();
      });
      carousel.addEventListener("keydown", event => {
        if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.target.closest("input, textarea, select, [contenteditable='true']")) return;
        if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
          event.preventDefault();
          show(index + (event.key === "ArrowRight" ? 1 : -1), true);
        }
      });
      document.addEventListener("visibilitychange", schedule);
      reducedMotion.addEventListener("change", event => {
        if (event.matches) {
          userPaused = true;
          syncToggle();
          schedule();
        }
      });

      viewport.addEventListener("touchstart", event => {
        touching = event.touches.length > 0;
        touch = event.touches.length === 1 ? {
          x: event.touches[0].clientX,
          y: event.touches[0].clientY,
          scrolling: false
        } : null;
        schedule();
      }, { passive: true });
      viewport.addEventListener("touchmove", event => {
        if (!touch || event.touches.length !== 1) { touch = null; return; }
        const dx = event.touches[0].clientX - touch.x;
        const dy = event.touches[0].clientY - touch.y;
        if (Math.abs(dy) > 12 && Math.abs(dy) > Math.abs(dx)) touch.scrolling = true;
      }, { passive: true });
      viewport.addEventListener("touchend", event => {
        touching = event.touches.length > 0;
        if (touch && !touching && event.changedTouches.length) {
          const dx = event.changedTouches[0].clientX - touch.x;
          const dy = event.changedTouches[0].clientY - touch.y;
          if (!touch.scrolling && Math.abs(dx) >= 48 && Math.abs(dx) > Math.abs(dy) * 1.3) {
            suppressClickUntil = Date.now() + 400;
            show(index + (dx < 0 ? 1 : -1), true);
          }
        }
        touch = null;
        schedule();
      }, { passive: true });
      viewport.addEventListener("touchcancel", () => { touch = null; touching = false; schedule(); }, { passive: true });
      viewport.addEventListener("click", event => {
        if (Date.now() < suppressClickUntil) {
          event.preventDefault();
          event.stopPropagation();
        }
      }, true);

      if ("IntersectionObserver" in window) {
        const observer = new window.IntersectionObserver(entries => {
          inView = entries[0].isIntersecting;
          schedule();
        }, { threshold: 0.05 });
        observer.observe(carousel);
      }
      track.setAttribute("aria-live", "off");
      carousel.classList.add("is-ready");
      controls.hidden = false;
      syncToggle();
      render();
      schedule();
    }
  }

  const search = document.querySelector("#publication-search, .publication-tools .search-input");
  const publications = document.querySelector(".publication-list");
  if (!search || !publications) return;
  const groups = Array.from(publications.querySelectorAll("details"));
  const originalOpenState = new Map(groups.map(group => [group, group.open]));
  const listItems = Array.from(publications.querySelectorAll("li")).filter(item => !item.querySelector("li"));
  const countedItems = groups.length ? listItems.filter(item => item.closest("details")) : listItems;
  const count = document.querySelector(".publication-count");
  const empty = document.querySelector(".empty-results");
  const searchableText = new Map(listItems.map(item => [item, item.textContent.toLocaleLowerCase()]));

  const filterPublications = () => {
    const query = search.value.trim().toLocaleLowerCase();
    const words = query.split(/\s+/).filter(Boolean);
    for (const item of listItems) {
      item.hidden = !words.every(word => searchableText.get(item).includes(word));
    }
    for (const group of groups) {
      const visible = Array.from(group.querySelectorAll("li")).some(item => !item.hidden);
      group.hidden = !visible;
      group.open = query ? visible : originalOpenState.get(group);
    }
    const total = countedItems.filter(item => !item.hidden).length;
    if (count) count.textContent = query ? `${total} of ${countedItems.length} publications` : `${countedItems.length} publications`;
    if (empty) empty.hidden = total !== 0;
  };
  search.addEventListener("input", filterPublications);
  search.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      search.value = "";
      filterPublications();
    }
  });
  filterPublications();
})();

// Dependency-free behavior checks for the carousel. This exercises lab.js in
// a small DOM/event fixture with a deterministic clock, not a real browser.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import vm from "node:vm";

const source = readFileSync(new URL("../assets/js/lab.js", import.meta.url), "utf8");

class Element {
  constructor(dataset = {}, focusable = false) {
    this.dataset = dataset;
    this.focusable = focusable;
    this.attributes = new Map();
    this.listeners = new Map();
    this.children = [];
    this.style = {};
    this.textContent = "";
    this.hidden = false;
    const classes = new Set();
    this.classList = { add: value => classes.add(value), contains: value => classes.has(value) };
  }
  append(...children) { children.forEach(child => { child.parent = this; this.children.push(child); }); }
  contains(node) { return !!node && (node === this || this.children.some(child => child.contains(node))); }
  getAttribute(name) { return this.attributes.get(name) ?? null; }
  setAttribute(name, value) { this.attributes.set(name, String(value)); }
  removeAttribute(name) { this.attributes.delete(name); }
  toggleAttribute(name, force) { if (force) this.setAttribute(name, ""); else this.removeAttribute(name); }
  matches(selector) { return selector === ":hover" ? !!this.hovered : false; }
  closest() { return this.editable ? this : null; }
  querySelector(selector) { return this.querySelectorAll(selector)[0] ?? null; }
  querySelectorAll(selector) {
    const all = this.children.flatMap(child => [child, ...child.querySelectorAll("*")]);
    if (selector === "*") return all;
    const dataMatch = selector.match(/^\[data-([\w-]+)\]$/);
    if (dataMatch) {
      const key = dataMatch[1].replace(/-([a-z])/g, (_, char) => char.toUpperCase());
      return all.filter(child => key in child.dataset);
    }
    if (selector.startsWith("a[href]")) return all.filter(child => child.focusable);
    return [];
  }
  addEventListener(type, callback) {
    if (!this.listeners.has(type)) this.listeners.set(type, []);
    this.listeners.get(type).push(callback);
  }
  fire(type, values = {}) {
    const event = {
      target: this, defaultPrevented: false, propagationStopped: false,
      preventDefault() { this.defaultPrevented = true; },
      stopPropagation() { this.propagationStopped = true; }, ...values
    };
    for (const callback of this.listeners.get(type) || []) callback(event);
    return event;
  }
}

function fixture({ reduced = false, complete = true, hover = true, titles = ["ERP-42", "Mobile Manipulator", "Smart Stroller"] } = {}) {
  const document = new Element();
  document.documentElement = new Element();
  document.activeElement = new Element();
  document.hidden = false;
  const root = new Element({ carousel: "" });
  const viewport = new Element({ carouselViewport: "" });
  const track = new Element({ carouselTrack: "" });
  const slides = titles.map(title => new Element({ carouselSlide: "", carouselTitle: title }));
  const links = slides.map(() => new Element({}, true));
  links[0].setAttribute("tabindex", "0");
  slides.forEach((slide, i) => slide.append(links[i]));
  track.append(...slides);
  viewport.append(track);
  const controls = new Element({ carouselControls: "" });
  controls.hidden = true;
  const previous = new Element({ carouselPrev: "" }, true);
  const next = new Element({ carouselNext: "" }, true);
  const toggle = new Element({ carouselToggle: "" }, true);
  const dots = slides.map((_, i) => new Element({ carouselGo: String(i) }, true));
  const count = new Element({ carouselCount: "" });
  const status = new Element({ carouselStatus: "" });
  controls.append(previous, next, toggle, ...dots, count);
  root.append(viewport, controls, status);
  if (!complete) delete track.dataset.carouselTrack;
  document.append(root);
  let now = 0;
  let sequence = 0;
  const timers = new Map();
  const motion = new Element();
  motion.matches = reduced;
  const hoverCapability = new Element();
  hoverCapability.matches = hover;
  let observer;
  const window = {
    matchMedia: query => query.includes("reduced-motion") ? motion : hoverCapability,
    setTimeout(callback, delay) { const id = ++sequence; timers.set(id, { callback, due: now + delay }); return id; },
    clearTimeout(id) { timers.delete(id); },
    IntersectionObserver: class {
      constructor(callback) { this.callback = callback; observer = this; }
      observe() {}
    }
  };
  const focus = element => {
    const old = document.activeElement;
    document.activeElement = element;
    if (root.contains(old)) root.fire("focusout", { target: old, relatedTarget: element });
    if (root.contains(element)) root.fire("focusin", { target: element, relatedTarget: old });
  };
  viewport.focus = () => focus(viewport);
  vm.runInNewContext(source, { document, window, Date: { now: () => now } }, { filename: "lab.js" });
  return {
    root, viewport, track, slides, links, controls, previous, next, toggle, dots, count, status, document, motion, focus,
    timers: () => timers.size,
    visible(value) { observer.callback([{ isIntersecting: value }]); },
    advance(milliseconds) {
      const target = now + milliseconds;
      while (true) {
        const pending = [...timers].filter(([, timer]) => timer.due <= target).sort((a, b) => a[1].due - b[1].due)[0];
        if (!pending) break;
        const [id, timer] = pending;
        timers.delete(id);
        now = timer.due;
        timer.callback();
      }
      now = target;
    }
  };
}

const activeIndex = test => test.slides.findIndex(slide => slide.getAttribute("aria-hidden") === "false");
const test = fixture();
assert.equal(test.controls.hidden, false);
assert.equal(test.root.classList.contains("is-ready"), true);
assert.equal(test.count.textContent, "01 / 03");
assert.equal(test.timers(), 1);
assert.equal(test.links[1].getAttribute("tabindex"), "-1");
assert.equal(test.slides[1].inert, true);
test.advance(4999);
assert.equal(activeIndex(test), 0);
test.advance(1);
assert.equal(activeIndex(test), 1);
assert.equal(test.track.style.transform, "translateX(-100%)");
assert.equal(test.status.textContent, "", "autoplay must not announce changes");
test.advance(10000);
assert.equal(activeIndex(test), 0, "autoplay wraps to the first slide");
assert.equal(test.links[0].getAttribute("tabindex"), "0", "original tabindex is restored");
test.previous.fire("click");
assert.equal(activeIndex(test), 2, "previous wraps to the final slide");
assert.match(test.status.textContent, /Smart Stroller/);
test.dots[1].fire("click");
assert.equal(activeIndex(test), 1);
assert.equal(test.dots[1].getAttribute("aria-pressed"), "true");
assert.equal(test.links[1].getAttribute("tabindex"), null, "native link focusability is restored");

for (const [pause, resume] of [
  [() => test.root.fire("mouseenter"), () => test.root.fire("mouseleave")],
  [() => test.focus(test.next), () => test.focus(new Element())],
  [() => { test.document.hidden = true; test.document.fire("visibilitychange"); }, () => { test.document.hidden = false; test.document.fire("visibilitychange"); }],
  [() => test.visible(false), () => test.visible(true)]
]) {
  pause();
  assert.equal(test.timers(), 0);
  const before = activeIndex(test);
  test.advance(10000);
  assert.equal(activeIndex(test), before);
  resume();
  assert.equal(test.timers(), 1);
}

test.toggle.fire("click");
assert.equal(test.toggle.textContent, "Play");
test.root.fire("mouseenter");
test.root.fire("mouseleave");
test.visible(false);
test.visible(true);
assert.equal(test.timers(), 0, "explicit pause survives transient pauses");
test.toggle.fire("click");
assert.equal(test.timers(), 1);
test.focus(test.links[1]);
const key = test.root.fire("keydown", { target: test.links[1], key: "ArrowRight" });
assert.equal(key.defaultPrevented, true);
assert.equal(activeIndex(test), 2);
assert.equal(test.document.activeElement, test.viewport, "focus must not remain in an inactive slide");
assert.equal(test.timers(), 0);

test.viewport.fire("touchstart", { touches: [{ clientX: 200, clientY: 10 }] });
test.viewport.fire("touchmove", { touches: [{ clientX: 190, clientY: 120 }] });
test.viewport.fire("touchend", { touches: [], changedTouches: [{ clientX: 20, clientY: 140 }] });
assert.equal(activeIndex(test), 2, "vertical scrolling must not change slides");
test.viewport.fire("touchstart", { touches: [{ clientX: 200, clientY: 10 }] });
test.viewport.fire("touchend", { touches: [], changedTouches: [{ clientX: 100, clientY: 15 }] });
assert.equal(activeIndex(test), 0, "horizontal swipe advances and wraps");
assert.equal(test.viewport.fire("click").defaultPrevented, true, "swiping must not accidentally open a link");
test.advance(401);
assert.equal(test.viewport.fire("click").defaultPrevented, false);

const reduced = fixture({ reduced: true });
assert.equal(reduced.timers(), 0);
assert.equal(reduced.toggle.textContent, "Play");
reduced.next.fire("click");
assert.equal(activeIndex(reduced), 1, "manual navigation still works with reduced motion");
reduced.focus(reduced.toggle);
reduced.toggle.fire("click");
assert.equal(reduced.timers(), 1, "explicit Play can opt into motion while the toggle retains focus");
reduced.focus(reduced.next);
assert.equal(reduced.timers(), 0, "moving focus elsewhere in the carousel stops playback again");
reduced.focus(new Element());
assert.equal(reduced.timers(), 1);
reduced.motion.fire("change", { matches: true });
assert.equal(reduced.timers(), 0);
assert.equal(reduced.toggle.textContent, "Play");

const mobile = fixture({ hover: false });
mobile.root.fire("mouseenter");
assert.equal(mobile.timers(), 1, "synthetic hover on a touchscreen must not stop autoplay permanently");
mobile.viewport.fire("touchstart", { touches: [{ clientX: 200, clientY: 20 }] });
assert.equal(mobile.timers(), 0, "autoplay pauses while a finger is down");
mobile.advance(10000);
assert.equal(activeIndex(mobile), 0);
mobile.viewport.fire("touchend", { touches: [], changedTouches: [{ clientX: 100, clientY: 20 }] });
assert.equal(activeIndex(mobile), 1);
assert.equal(mobile.timers(), 1);
mobile.viewport.fire("touchstart", { touches: [{ clientX: 200, clientY: 20 }] });
mobile.viewport.fire("touchcancel");
assert.equal(mobile.timers(), 1, "cancelled gestures resume the timer");

const incomplete = fixture({ complete: false });
assert.equal(incomplete.root.classList.contains("is-ready"), false);
assert.equal(incomplete.controls.hidden, true);
assert.equal(incomplete.slides[1].getAttribute("aria-hidden"), null, "incomplete markup keeps the static fallback visible");

const five = fixture({ titles: ["ERP-42", "Mobile Manipulator", "Smart Stroller", "Quadruped Robot", "Drone Platform"] });
assert.equal(five.count.textContent, "01 / 05");
five.dots[3].fire("click");
assert.equal(activeIndex(five), 3);
assert.equal(five.count.textContent, "04 / 05");
assert.equal(five.dots[3].getAttribute("aria-pressed"), "true");
assert.match(five.status.textContent, /Quadruped Robot/);
five.dots[4].fire("click");
assert.equal(activeIndex(five), 4);
assert.equal(five.count.textContent, "05 / 05");
assert.equal(five.dots[4].getAttribute("aria-pressed"), "true");
assert.match(five.status.textContent, /Drone Platform/);
five.next.fire("click");
assert.equal(activeIndex(five), 0, "next wraps from the fifth slide to the first");
five.previous.fire("click");
assert.equal(activeIndex(five), 4, "previous wraps from the first slide to the fifth");
five.dots[0].fire("click");
for (const expectedIndex of [1, 2, 3, 4, 0]) {
  five.advance(5000);
  assert.equal(activeIndex(five), expectedIndex, "autoplay visits all five slides before wrapping");
}
assert.equal(five.count.textContent, "01 / 05");
console.log("Carousel behavior checks passed: autoplay, wrapping, controls, focus, motion preference, visibility, swipe, fallback, five-slide navigation.");

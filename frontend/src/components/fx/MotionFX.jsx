"use client";

import { useEffect } from "react";

const TILT = ".stat-card, .hover-lift, .action-card";
const RIPPLE = ".btn, .chip";
const MAX_TILT = 8;

// Global interaction layer: card spotlight + tilt, click ripples and scroll reveal.
// Works by event delegation, so no component needs to opt in.
export default function MotionFX() {
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    let hovered = null;
    let lastMove = null;
    let raf = 0;

    const applyMove = () => {
      raf = 0;
      const card = lastMove.target.closest?.(".card") || null;
      if (hovered && hovered !== card) {
        hovered.style.removeProperty("--rx");
        hovered.style.removeProperty("--ry");
      }
      hovered = card;
      if (!card) return;
      const rect = card.getBoundingClientRect();
      const x = lastMove.clientX - rect.left;
      const y = lastMove.clientY - rect.top;
      card.style.setProperty("--mx", `${x}px`);
      card.style.setProperty("--my", `${y}px`);
      if (card.matches(TILT)) {
        card.style.setProperty("--ry", `${(x / rect.width - 0.5) * MAX_TILT}deg`);
        card.style.setProperty("--rx", `${(0.5 - y / rect.height) * MAX_TILT}deg`);
      }
    };
    const onMove = (e) => {
      lastMove = e;
      if (!raf) raf = requestAnimationFrame(applyMove);
    };

    const onDown = (e) => {
      const el = e.target.closest?.(RIPPLE);
      if (!el || el.disabled) return;
      const rect = el.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height) * 2;
      const ripple = document.createElement("span");
      ripple.className = "fx-ripple";
      ripple.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - rect.left - size / 2}px;top:${e.clientY - rect.top - size / 2}px`;
      el.appendChild(ripple);
      ripple.addEventListener("animationend", () => ripple.remove());
    };

    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          entry.target.classList.add("fx-in");
          io.unobserve(entry.target);
        }
      },
      { rootMargin: "0px 0px -40px 0px" },
    );
    // Only cards that start below the fold get the reveal; visible ones keep their own entrance
    let tagQueued = false;
    const tagCards = () => {
      tagQueued = false;
      document.querySelectorAll(".card:not([data-fx])").forEach((el) => {
        el.dataset.fx = "1";
        if (el.getBoundingClientRect().top > window.innerHeight) {
          el.classList.add("fx-reveal");
          io.observe(el);
        }
      });
    };
    const queueTag = () => {
      if (tagQueued) return;
      tagQueued = true;
      requestAnimationFrame(tagCards);
    };
    const mo = new MutationObserver(queueTag);
    mo.observe(document.body, { childList: true, subtree: true });
    queueTag();

    const onAnimationEnd = (e) => {
      if (e.animationName === "fxRise") e.target.classList.remove("fx-reveal", "fx-in");
    };

    document.addEventListener("pointermove", onMove, { passive: true });
    document.addEventListener("pointerdown", onDown);
    document.addEventListener("animationend", onAnimationEnd);
    return () => {
      cancelAnimationFrame(raf);
      io.disconnect();
      mo.disconnect();
      document.removeEventListener("pointermove", onMove);
      document.removeEventListener("pointerdown", onDown);
      document.removeEventListener("animationend", onAnimationEnd);
    };
  }, []);

  return null;
}

"use client";

import { useEffect, useState } from "react";

import { CsIcon } from "./CsIcon";

const STORAGE_KEY = "arasaac-theme";

export function CsThemeToggle() {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    const preferred =
      stored === "dark" ||
      (stored === null && window.matchMedia("(prefers-color-scheme: dark)").matches);
    document.documentElement.dataset.theme = preferred ? "dark" : "light";
    const update = window.setTimeout(() => setDark(preferred), 0);
    return () => window.clearTimeout(update);
  }, []);

  function toggleTheme() {
    const next = !dark;
    setDark(next);
    const theme = next ? "dark" : "light";
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem(STORAGE_KEY, theme);
  }

  return (
    <button
      aria-pressed={dark}
      className="cs-button secondary cs-theme-toggle"
      onClick={toggleTheme}
      type="button"
    >
      <CsIcon name={dark ? "sun" : "moon"} />
      {dark ? "Usar tema claro" : "Usar tema oscuro"}
    </button>
  );
}

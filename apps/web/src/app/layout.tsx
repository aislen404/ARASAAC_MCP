import type { Metadata } from "next";
import type { ReactNode } from "react";
import Script from "next/script";

import "./styles.css";

export const metadata: Metadata = {
  title: "ARASAAC Social MCP Platform",
  description:
    "Creación guiada de materiales accesibles con pictogramas reales de ARASAAC.",
};

const themeScript = `
try {
  const stored = localStorage.getItem("arasaac-theme");
  const preferred =
    stored === "dark" ||
    (stored === null && window.matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.dataset.theme = preferred ? "dark" : "light";
} catch (e) {}
`;

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <head>
        <Script id="theme-init" strategy="beforeInteractive">
          {themeScript}
        </Script>
      </head>
      <body>{children}</body>
    </html>
  );
}

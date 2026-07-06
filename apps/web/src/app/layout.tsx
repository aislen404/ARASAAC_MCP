import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./styles.css";

export const metadata: Metadata = {
  title: "ARASAAC Social MCP Platform",
  description:
    "Creación guiada de materiales accesibles con pictogramas reales de ARASAAC.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}

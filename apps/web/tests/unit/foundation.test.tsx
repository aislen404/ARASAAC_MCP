import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import RootLayout, { metadata } from "../../src/app/layout";
import Home from "../../src/app/page";

describe("Convergencia Serena home", () => {
  it("renders the guided product shell and governed workflow", () => {
    const markup = renderToStaticMarkup(<Home />);

    expect(markup).toContain("Crear con claridad. Revisar con criterio.");
    expect(markup).toContain("Revisión humana obligatoria");
    expect(markup).toContain("Cinco fases, una decisión humana");
    expect(markup).toContain('aria-current="step"');
    expect(markup).toContain("WCAG 2.2 AA");
    expect(markup).toContain("Configura el material");
    expect(markup).toContain("Vista previa editable");
    expect(markup).toContain("Revisión y exportación");
    expect(markup).toContain("Sergio Palao");
  });

  it("provides Spanish document metadata and semantic content", () => {
    const markup = renderToStaticMarkup(
      <RootLayout>
        <Home />
      </RootLayout>,
    );

    expect(markup).toContain('<html lang="es">');
    expect(markup).toContain("<main ");
    expect(markup).toContain("<h1");
    expect(metadata.title).toBe("ARASAAC Social MCP Platform");
  });
});

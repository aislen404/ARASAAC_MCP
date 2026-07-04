import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import RootLayout, { metadata } from "../../src/app/layout";
import Home from "../../src/app/page";

describe("MVP-0 status page", () => {
  it("renders project status and every approved limit", () => {
    const markup = renderToStaticMarkup(<Home />);

    expect(markup).toContain("ARASAAC Social MCP Platform");
    expect(markup).toContain("Revisión humana obligatoria");
    expect(markup).toContain("Configura el material");
    expect(markup).toContain("Vista previa editable");
    expect(markup).toContain("Revisión y exportación");
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

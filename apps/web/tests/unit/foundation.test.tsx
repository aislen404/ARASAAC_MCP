import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";

import RootLayout, { metadata } from "../../src/app/layout";
import Home from "../../src/app/page";

describe("MVP-0 status page", () => {
  it("renders project status and every approved limit", () => {
    const markup = renderToStaticMarkup(<Home />);

    expect(markup).toContain("ARASAAC Social MCP Platform");
    expect(markup).toContain("Base técnica disponible");
    expect(markup).toContain("Sin integración ni consultas a ARASAAC");
    expect(markup).toContain("Sin generación o exportación de materiales");
    expect(markup).toContain("Sin autenticación ni datos personales");
    expect(markup).toContain("Servidor MCP deshabilitado y sin tools");
  });

  it("provides Spanish document metadata and semantic content", () => {
    const markup = renderToStaticMarkup(
      <RootLayout>
        <Home />
      </RootLayout>,
    );

    expect(markup).toContain('<html lang="es">');
    expect(markup).toContain("<main>");
    expect(markup).toContain("<h1");
    expect(metadata.title).toBe("ARASAAC Social MCP Platform");
  });
});

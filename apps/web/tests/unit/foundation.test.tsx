import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import RootLayout, { metadata } from "../../src/app/layout";
import Home from "../../src/app/page";

describe("Convergencia Serena home", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({ matches: false }),
    );
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        available: false,
        provider: "disabled",
        reason: "La capa IA está desactivada.",
        generates_pictograms: false,
        requires_human_selection: true,
        stores_input: false,
      }),
    }));
  });

  it("renders the guided product shell and governed workflow", () => {
    render(<Home />);

    expect(screen.getByRole("heading", { level: 1, name: "Crear con claridad. Revisar con criterio." })).toBeTruthy();
    expect(screen.getAllByText("Revisión humana obligatoria").length).toBeGreaterThan(0);
    expect(screen.getByRole("heading", { name: "Cinco fases, una decisión humana" })).toBeTruthy();
    expect(screen.getByRole("listitem", { current: "step" }).textContent).toContain("Definir necesidad");
    expect(screen.getByText("WCAG 2.2 AA")).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Configura el material" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Vista previa editable" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Revisión y exportación" })).toBeTruthy();
    expect(screen.getAllByText(/Sergio Palao/).length).toBeGreaterThan(0);
  });

  it("provides Spanish document metadata", () => {
    expect(metadata.title).toBe("ARASAAC Social MCP Platform");
    render(
      <RootLayout>
        <Home />
      </RootLayout>,
    );
    expect(document.documentElement.getAttribute("lang")).toBe("es");
  });
});

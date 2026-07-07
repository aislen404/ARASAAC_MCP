import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { ConvergenciaSerenaApp } from "../../src/components/convergencia-serena/ConvergenciaSerenaApp";
import { MaterialBuilderProvider } from "../../src/features/material-builder/builder-context";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

describe("ConvergenciaSerenaApp", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          available: false,
          provider: "disabled",
          model: null,
          reason: "IA deshabilitada en pruebas.",
          generates_pictograms: false,
          requires_human_selection: true,
          stores_input: false,
        }),
    }));
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({ matches: false }),
    );
  });

  it("exposes skip link, shell zones and single main landmark", () => {
    render(
      <MaterialFlowProvider>
        <MaterialBuilderProvider>
          <ConvergenciaSerenaApp builder={<p>Builder de prueba</p>} />
        </MaterialBuilderProvider>
      </MaterialFlowProvider>,
    );

    const skip = screen.getByRole("link", { name: "Saltar al contenido principal" });
    expect(skip.getAttribute("href")).toBe("#cs-main");
    expect(screen.getAllByRole("main")).toHaveLength(1);
    expect(screen.getByText("Builder de prueba")).toBeTruthy();
    expect(document.querySelector('[data-cs="header"]')).toBeTruthy();
    expect(document.querySelector('[data-cs="side-rail"]')).toBeTruthy();
    expect(document.querySelector('[data-cs="guided-workspace"]')).toBeTruthy();
    expect(document.querySelector('[data-cs="context-help"]')).toBeTruthy();
    expect(document.querySelector('[data-cs="bottom-strip"]')).toBeTruthy();
    expect(screen.getByText(/Sergio Palao/)).toBeTruthy();
  });
});

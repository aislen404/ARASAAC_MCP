import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { AppShell } from "../../src/components/app-shell";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

describe("AppShell", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({ matches: false }),
    );
  });

  it("exposes skip link and single main landmark", () => {
    render(
      <MaterialFlowProvider>
        <AppShell>
          <p>Contenido de prueba</p>
        </AppShell>
      </MaterialFlowProvider>,
    );

    const skip = screen.getByRole("link", { name: "Saltar al contenido principal" });
    expect(skip.getAttribute("href")).toBe("#main-content");
    expect(screen.getAllByRole("main")).toHaveLength(1);
    expect(screen.getByText("Contenido de prueba")).toBeTruthy();
  });
});

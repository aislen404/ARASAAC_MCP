import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import RootLayout, { metadata } from "../../src/app/layout";
import Home from "../../src/app/page";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

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

  it("renders the workspace welcome entry point", () => {
    render(<Home />);

    expect(
      screen.getByRole("heading", {
        level: 1,
        name: "Guarda tu enlace. Si lo pierdes, perderás el acceso.",
      }),
    ).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Crear workspace" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Abrir workspace existente" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Crear workspace" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "Abrir workspace existente" })).toBeTruthy();
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

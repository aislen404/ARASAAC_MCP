import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { CsContinueCard } from "../../src/components/convergencia-serena/CsContinueCard";
import { MaterialBuilderProvider } from "../../src/features/material-builder/builder-context";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

describe("CsContinueCard", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: true,
      json: () =>
        Promise.resolve({
          available: false,
          provider: "disabled",
          model: null,
          reason: "IA deshabilitada.",
          generates_pictograms: false,
          requires_human_selection: true,
          stores_input: false,
        }),
    }));
  });

  it("shows empty draft state and navigates to builder", async () => {
    const user = userEvent.setup();
    const builder = document.createElement("section");
    builder.id = "cs-builder";
    document.body.append(builder);
    const titleInput = document.createElement("input");
    titleInput.id = "material-title";
    document.body.append(titleInput);
    const scrollIntoView = vi.fn();
    builder.scrollIntoView = scrollIntoView;
    const focus = vi.spyOn(titleInput, "focus");

    render(
      <MaterialFlowProvider>
        <MaterialBuilderProvider>
          <CsContinueCard />
        </MaterialBuilderProvider>
      </MaterialFlowProvider>,
    );

    expect(screen.getByText("Sin borrador activo")).toBeTruthy();
    expect(screen.getByText("0 de 5 pasos completados")).toBeTruthy();
    await user.click(screen.getByRole("button", { name: /Ir al área de trabajo/i }));
    expect(scrollIntoView).toHaveBeenCalled();
    await vi.waitFor(() => expect(focus).toHaveBeenCalled());
  });
});

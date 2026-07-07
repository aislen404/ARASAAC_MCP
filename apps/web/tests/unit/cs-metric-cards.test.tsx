import { render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { CsMetricCards } from "../../src/components/convergencia-serena/CsMetricCards";
import { MaterialBuilderProvider } from "../../src/features/material-builder/builder-context";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

describe("CsMetricCards", () => {
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

  it("shows honest empty metrics at start", () => {
    render(
      <MaterialFlowProvider>
        <MaterialBuilderProvider>
          <CsMetricCards />
        </MaterialBuilderProvider>
      </MaterialFlowProvider>,
    );

    expect(screen.getByText("0%")).toBeTruthy();
    expect(screen.getByText("0 completados · 1 en curso · 4 pendientes")).toBeTruthy();
    expect(screen.getAllByText("0")).toHaveLength(3);
  });
});

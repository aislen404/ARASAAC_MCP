import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { GuidedFlow } from "../../src/components/guided-flow";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

describe("GuidedFlow", () => {
  it("marks the first phase as active by default", () => {
    render(
      <MaterialFlowProvider>
        <GuidedFlow />
      </MaterialFlowProvider>,
    );
    const current = screen.getByRole("listitem", { current: "step" });
    expect(current.textContent).toContain("Definir necesidad");
    expect(document.querySelector(".progressLabel")?.textContent).toContain(
      "definir necesidad",
    );
  });
});

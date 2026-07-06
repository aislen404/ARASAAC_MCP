import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CsWorkflowStepper } from "../../src/components/convergencia-serena/CsWorkflowStepper";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

describe("CsWorkflowStepper", () => {
  it("marks the first phase as active by default", () => {
    render(
      <MaterialFlowProvider>
        <CsWorkflowStepper />
      </MaterialFlowProvider>,
    );
    const current = screen.getByRole("listitem", { current: "step" });
    expect(current.textContent).toContain("Definir necesidad");
  });
});

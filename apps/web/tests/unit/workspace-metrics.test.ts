import { describe, expect, it } from "vitest";

import {
  computeWorkspaceMetrics,
  formatProgressSummary,
} from "../../src/components/convergencia-serena/workspace-metrics";

describe("computeWorkspaceMetrics", () => {
  it("returns honest zeros at initial phase", () => {
    const metrics = computeWorkspaceMetrics({ phase: 0, items: [], material: null });

    expect(metrics).toEqual({
      completedSteps: 0,
      inProgressSteps: 1,
      pendingSteps: 4,
      progressPercent: 0,
      totalItems: 0,
      pendingReview: 0,
      correctItems: 0,
    });
    expect(formatProgressSummary(metrics)).toBe("0 completados · 1 en curso · 4 pendientes");
  });

  it("reflects progress when items exist", () => {
    const metrics = computeWorkspaceMetrics({
      phase: 2,
      items: [{ key: "a", text: "Paso", pictogram: null as never }],
      material: null,
    });

    expect(metrics.progressPercent).toBe(40);
    expect(metrics.totalItems).toBe(1);
  });

  it("counts pending review for draft materials", () => {
    const metrics = computeWorkspaceMetrics({
      phase: 3,
      items: [],
      material: {
        material_id: "m1",
        title: "Borrador",
        status: "draft",
        type: "agenda",
      } as never,
    });

    expect(metrics.pendingReview).toBe(1);
  });
});

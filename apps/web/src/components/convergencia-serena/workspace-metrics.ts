import type { FlowPhase } from "../../features/material-builder/flow-context";
import type { Material, SelectedItem } from "../../features/material-builder/types";

const WORKFLOW_STEP_COUNT = 5;

export type WorkspaceMetrics = {
  completedSteps: number;
  inProgressSteps: number;
  pendingSteps: number;
  progressPercent: number;
  totalItems: number;
  pendingReview: number;
  correctItems: number;
};

export function computeWorkspaceMetrics(input: {
  phase: FlowPhase;
  items: SelectedItem[];
  material: Material | null;
}): WorkspaceMetrics {
  const completedSteps = input.phase;
  const inProgressSteps = input.phase < WORKFLOW_STEP_COUNT ? 1 : 0;
  const pendingSteps = Math.max(0, WORKFLOW_STEP_COUNT - input.phase - 1);
  const progressPercent = Math.round((input.phase / WORKFLOW_STEP_COUNT) * 100);
  const totalItems = input.items.length;
  const pendingReview =
    input.material?.status === "draft" || input.material?.status === "rejected" ? 1 : 0;
  const correctItems = input.items.filter((item) => item.pictogram).length;

  return {
    completedSteps,
    inProgressSteps,
    pendingSteps,
    progressPercent,
    totalItems,
    pendingReview,
    correctItems,
  };
}

export function formatProgressSummary(metrics: WorkspaceMetrics): string {
  return `${metrics.completedSteps} completados · ${metrics.inProgressSteps} en curso · ${metrics.pendingSteps} pendiente${metrics.pendingSteps === 1 ? "" : "s"}`;
}

export { WORKFLOW_STEP_COUNT };

import type { MaterialStatus } from "./types";

const STATUS_LABELS: Record<MaterialStatus, string> = {
  draft: "Borrador",
  in_review: "En revisión",
  approved: "Aprobado",
  rejected: "Rechazado",
};

export function formatMaterialStatus(
  status: MaterialStatus | null | undefined,
): string {
  if (!status) return "Sin borrador";
  return STATUS_LABELS[status];
}

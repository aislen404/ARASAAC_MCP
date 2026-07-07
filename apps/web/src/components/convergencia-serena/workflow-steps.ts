export const workflowSteps = [
  ["Definir necesidad", "Describe un escenario genérico y sin datos personales."],
  ["Explorar pictogramas", "Consulta exclusivamente candidatos reales de ARASAAC."],
  ["Organizar material", "Selecciona, ordena y ajusta cada elemento."],
  ["Validar accesibilidad", "Comprueba claridad, secuencia y atribución."],
  ["Revisar y compartir", "Una persona debe aprobar antes de exportar."],
] as const;

export const workflowStepIcons = [
  "target",
  "search",
  "folder",
  "shield",
  "plane",
] as const;

export const phaseLabels = ["Pendiente", "En curso", "Completada"] as const;

export type PhaseLabel = (typeof phaseLabels)[number];

export function phaseStatus(index: number, active: number): PhaseLabel {
  if (index < active) return "Completada";
  if (index === active) return "En curso";
  return "Pendiente";
}

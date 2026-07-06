import type { FlowPhase } from "../../features/material-builder/flow-context";
import { workflowSteps } from "./workflow-steps";

export type WorkspaceSuggestion = {
  illustration: string;
  title: string;
  description: string;
  href: string;
};

const suggestionTemplates: WorkspaceSuggestion[] = [
  {
    illustration: "suggest-search.svg",
    title: "Definir tu necesidad",
    description: "Describe un escenario genérico sin datos personales.",
    href: "#crear",
  },
  {
    illustration: "suggest-collections.svg",
    title: "Explorar pictogramas",
    description: "Busca candidatos reales de ARASAAC manualmente.",
    href: "#crear",
  },
  {
    illustration: "suggest-accessibility.svg",
    title: "Validar accesibilidad",
    description: "Comprueba claridad, secuencia y atribución.",
    href: "#cs-review",
  },
  {
    illustration: "suggest-guides.svg",
    title: "Revisar y compartir",
    description: "Una persona debe aprobar antes de exportar.",
    href: "#cs-review",
  },
];

export function buildWorkspaceSuggestions(phase: FlowPhase): WorkspaceSuggestion[] {
  const nextStepIndex = Math.min(phase, workflowSteps.length - 1);
  const prioritized = [
    {
      ...suggestionTemplates[nextStepIndex],
      title: workflowSteps[nextStepIndex][0],
      description: workflowSteps[nextStepIndex][1],
      href: nextStepIndex <= 1 ? "#crear" : nextStepIndex === 2 ? "#cs-builder" : "#cs-review",
    },
    suggestionTemplates[1],
    suggestionTemplates[2],
    suggestionTemplates[3],
  ];

  const seen = new Set<string>();
  return prioritized.filter((item) => {
    const key = `${item.title}-${item.href}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

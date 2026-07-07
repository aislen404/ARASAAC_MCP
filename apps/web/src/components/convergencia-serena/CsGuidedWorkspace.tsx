"use client";

import type { ReactNode } from "react";

import { useMaterialFlow } from "../../features/material-builder/flow-context";
import { CsContinueCard } from "./CsContinueCard";
import { CsMetricCards } from "./CsMetricCards";
import { CsSuggestionStrip } from "./CsSuggestionStrip";
import { CsWorkflowStepper } from "./CsWorkflowStepper";
import { workflowSteps } from "./workflow-steps";

export function CsGuidedWorkspace({ builder }: Readonly<{ builder: ReactNode }>) {
  const { phase } = useMaterialFlow();
  const activeTitle = workflowSteps[phase][0];

  return (
    <section className="cs-main-card" data-cs="guided-workspace">
      <div className="cs-hero-card">
        <p className="cs-eyebrow">Convergencia Serena</p>
        <h1 className="cs-title-display">Crear con claridad. Revisar con criterio.</h1>
        <p className="cs-lead">
          Un espacio guiado para preparar materiales accesibles con pictogramas reales de ARASAAC
          y control humano en cada decisión.
        </p>
      </div>
      <div className="cs-main-inner">
        <div className="cs-chip-row" style={{ justifyContent: "space-between" }}>
          <div>
            <p className="cs-eyebrow">Asistente guiado</p>
            <h2 className="cs-h2">Cinco fases, una decisión humana</h2>
          </div>
          <span className="cs-chip">Fase activa: {activeTitle.toLowerCase()}</span>
        </div>
        <CsWorkflowStepper />
        <div className="cs-section">
          <CsMetricCards />
          <div className="cs-section">
            <CsContinueCard />
          </div>
        </div>
        <section aria-labelledby="cs-builder-title" className="cs-section" id="cs-builder">
          <p className="cs-eyebrow">Área de trabajo</p>
          <h2 className="cs-h2" id="cs-builder-title">
            Continúa con tu material
          </h2>
          <p className="cs-lead">
            La IA, si está habilitada, solo propone texto. Tú eliges cada pictograma y una persona
            revisa el resultado final.
          </p>
          {builder}
        </section>
        <div className="cs-section">
          <CsSuggestionStrip />
        </div>
      </div>
    </section>
  );
}

"use client";

import { useMaterialBuilderContext } from "../../features/material-builder/builder-context";
import { useMaterialFlow } from "../../features/material-builder/flow-context";
import { CsIcon } from "./CsIcon";
import { WORKFLOW_STEP_COUNT } from "./workspace-metrics";

function continueToBuilder() {
  const builder = document.getElementById("cs-builder");
  builder?.scrollIntoView({ behavior: "smooth", block: "start" });
  const titleInput = document.getElementById("material-title");
  if (titleInput instanceof HTMLElement) {
    window.setTimeout(() => titleInput.focus(), 300);
  }
}

export function CsContinueCard() {
  const { phase } = useMaterialFlow();
  const { title, material } = useMaterialBuilderContext();
  const draftTitle = material?.title?.trim() || title.trim();
  const hasDraft = draftTitle.length > 0;

  return (
    <article className="cs-metric-card" data-cs="continue-card">
      <h3>Continuar donde lo dejaste</h3>
      <img
        alt=""
        className="cs-theme-illustration-light"
        height={160}
        src="/convergencia-serena/illustrations/landscape-light.svg"
        width={280}
      />
      <img
        alt=""
        className="cs-theme-illustration-dark"
        height={160}
        src="/convergencia-serena/illustrations/landscape-dark.svg"
        width={280}
      />
      <p>
        <strong>{hasDraft ? `Borrador: ${draftTitle}` : "Sin borrador activo"}</strong>
        <br />
        {phase} de {WORKFLOW_STEP_COUNT} pasos completados
      </p>
      <button className="cs-button secondary" onClick={continueToBuilder} type="button">
        <CsIcon name="route" /> {hasDraft ? "Continuar" : "Ir al área de trabajo"}
      </button>
    </article>
  );
}

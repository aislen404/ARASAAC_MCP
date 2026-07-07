"use client";

import { useMaterialBuilderContext } from "../../features/material-builder/builder-context";
import { useMaterialFlow } from "../../features/material-builder/flow-context";
import {
  computeWorkspaceMetrics,
  formatProgressSummary,
} from "./workspace-metrics";

export function CsMetricCards() {
  const { phase } = useMaterialFlow();
  const { items, material } = useMaterialBuilderContext();
  const metrics = computeWorkspaceMetrics({ phase, items, material });

  return (
    <section aria-label="Métricas del flujo" className="cs-metric-row" data-cs="metric-row">
      <article className="cs-metric-card">
        <h3>Progreso del flujo guiado</h3>
        <div
          className="cs-progress-donut"
          style={{
            background: `conic-gradient(var(--cs-accent) 0 ${metrics.progressPercent}%, color-mix(in srgb, var(--cs-border) 50%, transparent) ${metrics.progressPercent}% 100%)`,
          }}
        >
          <span>{metrics.progressPercent}%</span>
        </div>
        <p className="cs-metric-label">{formatProgressSummary(metrics)}</p>
      </article>
      <article className="cs-metric-card">
        <h3>Validación de la colección</h3>
        <div className="cs-three-col">
          <p className="cs-stat-block">
            <span className="cs-metric-value">{metrics.totalItems}</span>
            <span className="cs-metric-label">Elementos totales</span>
          </p>
          <p className="cs-stat-block">
            <span className="cs-metric-value">{metrics.pendingReview}</span>
            <span className="cs-metric-label">Por revisar</span>
          </p>
          <p className="cs-stat-block">
            <span className="cs-metric-value">{metrics.correctItems}</span>
            <span className="cs-metric-label">Correctos</span>
          </p>
        </div>
      </article>
    </section>
  );
}

"use client";

import type { useMaterialBuilder } from "./use-material-builder";

type Builder = ReturnType<typeof useMaterialBuilder>;

const severityLabel: Record<string, string> = {
  blocker: "Bloqueo",
  warning: "Aviso",
  ok: "Correcto",
};

export function ValidationPanel({
  builder,
  embedded = false,
}: Readonly<{ builder: Builder; embedded?: boolean }>) {
  const { material, validationReport, busy, runValidation } = builder;

  const summary = validationReport
    ? `${validationReport.blocker_count} bloqueos, ${validationReport.warning_count} avisos y ${validationReport.ok_count} comprobaciones correctas.`
    : "Ejecuta la validación antes de enviar el material a revisión.";

  return (
    <section
      aria-labelledby="validation-heading"
      className={embedded ? "cs-panel cs-builder-panel validationPanel" : "panel validationPanel"}
      id="cs-validation"
    >
      <p className={embedded ? "cs-eyebrow" : "stepLabel"}>Paso 3</p>
      <h2 id="validation-heading">Validación del material</h2>
      <p
        aria-live={validationReport?.is_blocking ? "assertive" : "polite"}
        className={embedded ? "cs-ai-feedback" : "message"}
        role="status"
      >
        {summary}
      </p>
      <button
        className={embedded ? "cs-button" : undefined}
        disabled={busy || !material}
        onClick={runValidation}
        type="button"
      >
        Validar material
      </button>
      {validationReport ? (
        <div
          aria-labelledby="validation-findings-heading"
          className="validationFindings"
          role="group"
        >
          <h3 id="validation-findings-heading">Resultados</h3>
          <ul>
            {validationReport.findings.map((finding) => (
              <li key={`${finding.code}-${finding.field ?? "general"}`}>
                <strong>{severityLabel[finding.severity]}:</strong> {finding.message}
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
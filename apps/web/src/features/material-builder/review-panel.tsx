"use client";

import { formatMaterialStatus } from "./status-labels";
import type { useMaterialBuilder } from "./use-material-builder";

type Builder = ReturnType<typeof useMaterialBuilder>;

export function ReviewPanel({
  builder,
  embedded = false,
}: Readonly<{ builder: Builder; embedded?: boolean }>) {
  const { material, message, busy, submitReview, decide, download } = builder;

  return (
    <section
      aria-labelledby="review-heading"
      className={embedded ? "cs-panel cs-builder-panel reviewPanel" : "panel reviewPanel"}
      id="cs-review"
    >
      <p className={embedded ? "cs-eyebrow" : "stepLabel"}>Paso 3</p>
      <h2 id="review-heading">Revisión y exportación</h2>
      <p
        aria-live="polite"
        className={embedded ? "cs-ai-feedback" : "message"}
        role="status"
      >
        {message}
      </p>
      <p>
        Estado: <strong>{formatMaterialStatus(material?.status)}</strong>
      </p>
      <div className="reviewActions">
        <button
          className={embedded ? "cs-button" : undefined}
          disabled={busy || material?.status !== "draft"}
          onClick={submitReview}
          type="button"
        >
          Enviar a revisión
        </button>
        <button
          className={embedded ? "cs-button" : undefined}
          disabled={busy || material?.status !== "in_review"}
          onClick={() => decide("approved")}
          type="button"
        >
          Aprobar tras revisión humana
        </button>
        <button
          className={embedded ? "cs-button secondary" : undefined}
          disabled={busy || material?.status !== "in_review"}
          onClick={() => decide("rejected")}
          type="button"
        >
          Rechazar
        </button>
        <button
          className={embedded ? "cs-button secondary" : undefined}
          disabled={busy || material?.status !== "approved"}
          onClick={() => download("html")}
          type="button"
        >
          Exportar HTML
        </button>
        <button
          className={embedded ? "cs-button secondary" : undefined}
          disabled={busy || material?.status !== "approved"}
          onClick={() => download("pdf")}
          type="button"
        >
          Exportar PDF
        </button>
        <button
          className={embedded ? "cs-button secondary" : undefined}
          disabled={busy || material?.status !== "approved"}
          onClick={() => download("docx")}
          type="button"
        >
          Exportar DOCX
        </button>
        <button
          className={embedded ? "cs-button secondary" : undefined}
          disabled={busy || material?.status !== "approved"}
          onClick={() => download("pptx")}
          type="button"
        >
          Exportar PPTX
        </button>
        <button
          className={embedded ? "cs-button secondary" : undefined}
          disabled={busy || material?.status !== "approved"}
          onClick={() => download("zip")}
          type="button"
        >
          Exportar ZIP
        </button>
      </div>
    </section>
  );
}

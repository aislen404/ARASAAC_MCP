"use client";

import { useEffect, useMemo, useRef, useState } from "react";

import type { Workspace } from "./types";

export function WorkspaceCreatedDialog({
  workspace,
  onContinue,
}: Readonly<{ workspace: Workspace; onContinue: () => void }>) {
  const [confirmed, setConfirmed] = useState(false);
  const [feedback, setFeedback] = useState("");
  const confirmRef = useRef<HTMLInputElement | null>(null);
  const workspaceUrl = useMemo(
    () => `${window.location.origin}/w/${workspace.slug}/mis-materiales`,
    [workspace.slug],
  );

  useEffect(() => {
    confirmRef.current?.focus();
  }, []);

  async function copyLink() {
    await navigator.clipboard.writeText(workspaceUrl);
    setFeedback("Enlace copiado.");
  }

  function downloadLink() {
    const blob = new Blob([workspaceUrl], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `workspace-${workspace.slug}.txt`;
    link.click();
    URL.revokeObjectURL(link.href);
    setFeedback("Enlace descargado.");
  }

  return (
    <div
      aria-labelledby="workspace-created-title"
      aria-modal="true"
      className="workspaceDialogBackdrop"
      role="dialog"
    >
      <div className="workspaceDialogCard">
        <p aria-live="assertive" className="workspaceWarning" role="alert">
          Este enlace no se puede recuperar si lo pierdes.
        </p>
        <h2 id="workspace-created-title">Workspace creado</h2>
        <p>Guarda este enlace antes de continuar.</p>
        <label htmlFor="workspace-link">Enlace del workspace</label>
        <input id="workspace-link" readOnly value={workspaceUrl} />
        <div className="workspaceDialogActions">
          <button onClick={copyLink} type="button">
            Copiar enlace
          </button>
          <button onClick={downloadLink} type="button">
            Descargar enlace .txt
          </button>
        </div>
        <label className="checkLabel">
          <input
            checked={confirmed}
            ref={confirmRef}
            onChange={(event) => setConfirmed(event.target.checked)}
            type="checkbox"
          />
          He guardado mi enlace
        </label>
        <p aria-live="polite" className="workspaceFeedback" role="status">
          {feedback || "Marca la casilla para continuar."}
        </p>
        <button aria-disabled={!confirmed} disabled={!confirmed} onClick={onContinue} type="button">
          Ir a mi workspace
        </button>
        {!confirmed ? (
          <p className="workspaceReason">Debes confirmar que has guardado el enlace.</p>
        ) : null}
      </div>
    </div>
  );
}
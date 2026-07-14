"use client";

import { useState } from "react";

import { useWorkspace } from "./workspace-context";

export function WorkspaceHeader() {
  const { workspace, workspaceUrl } = useWorkspace();
  const [message, setMessage] = useState("");

  async function copyLink() {
    await navigator.clipboard.writeText(workspaceUrl);
    setMessage("Enlace copiado.");
    window.setTimeout(() => setMessage(""), 1600);
  }

  return (
    <section aria-label="Workspace actual" className="workspaceHeader">
      <div>
        <p className="workspaceLabel">Workspace actual</p>
        <h1>{workspace.display_name?.trim() || "Mis materiales"}</h1>
        <p className="workspaceSlug">
          Slug: <strong>{workspace.slug}</strong>
        </p>
      </div>
      <div className="workspaceHeaderActions">
        <button onClick={copyLink} type="button">
          Copiar enlace
        </button>
        <p aria-live="polite" className="workspaceFeedback" role="status">
          {message || "Guarda este enlace: no se puede recuperar si lo pierdes."}
        </p>
      </div>
    </section>
  );
}
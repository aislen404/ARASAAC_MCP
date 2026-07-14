"use client";

import { useState } from "react";

import { updateWorkspace } from "./api";

export function WorkspaceSettingsForm({
  slug,
  initialDisplayName,
}: Readonly<{ slug: string; initialDisplayName: string | null }>) {
  const [displayName, setDisplayName] = useState(initialDisplayName ?? "");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSave() {
    setBusy(true);
    try {
      const response = await updateWorkspace(slug, displayName.trim() || null);
      setDisplayName(response.workspace.display_name ?? "");
      setMessage("Nombre visible actualizado.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "No se pudo actualizar.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="workspacePanel">
      <p className="eyebrow">Ajustes</p>
      <h2>Nombre visible del workspace</h2>
      <label htmlFor="workspace-display-name-settings">Nombre visible</label>
      <input
        id="workspace-display-name-settings"
        maxLength={120}
        onChange={(event) => setDisplayName(event.target.value)}
        value={displayName}
      />
      <button disabled={busy} onClick={handleSave} type="button">
        Guardar nombre visible
      </button>
      <p aria-live="polite" className="message" role="status">
        {message || "No uses nombres personales ni datos sensibles."}
      </p>
    </section>
  );
}
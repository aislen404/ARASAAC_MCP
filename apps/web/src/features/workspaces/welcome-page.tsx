"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { createWorkspace, getWorkspace } from "./api";
import { WorkspaceCreatedDialog } from "./workspace-created-dialog";
import type { Workspace } from "./types";

function extractSlug(value: string): string {
  const trimmed = value.trim();
  if (!trimmed) return "";
  if (!trimmed.includes("/")) return trimmed;
  try {
    const url = new URL(trimmed);
    const parts = url.pathname.split("/").filter(Boolean);
    const index = parts.indexOf("w");
    return index >= 0 ? (parts[index + 1] ?? "") : parts.at(-1) ?? "";
  } catch {
    return trimmed;
  }
}

export function WelcomePage() {
  const router = useRouter();
  const [displayName, setDisplayName] = useState("");
  const [openValue, setOpenValue] = useState("");
  const [message, setMessage] = useState("");
  const [workspace, setWorkspace] = useState<Workspace | null>(null);
  const [busy, setBusy] = useState(false);

  async function handleCreate() {
    setBusy(true);
    try {
      const response = await createWorkspace(displayName.trim() || undefined);
      setWorkspace(response.workspace);
      setMessage("");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "No se pudo crear el workspace.");
    } finally {
      setBusy(false);
    }
  }

  async function handleOpen() {
    const slug = extractSlug(openValue);
    if (!slug) {
      setMessage("Introduce un slug o un enlace completo.");
      return;
    }
    setBusy(true);
    try {
      await getWorkspace(slug);
      router.push(`/w/${slug}/mis-materiales`);
    } catch {
      setMessage("Este enlace no existe o ha sido eliminado. Verifica el enlace.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="welcomeMain" id="main-content">
      <section className="welcomeCard">
        <p className="eyebrow">Workspace seguro</p>
        <h1>Guarda tu enlace. Si lo pierdes, perderás el acceso.</h1>
        <p className="helpText">
          Crea un workspace nuevo o abre uno existente con su slug o URL completa.
        </p>
        <div className="welcomeActions">
          <section aria-labelledby="create-workspace-title" className="welcomePanel">
            <h2 id="create-workspace-title">Crear workspace</h2>
            <label htmlFor="workspace-display-name">Nombre visible opcional</label>
            <input
              id="workspace-display-name"
              maxLength={120}
              onChange={(event) => setDisplayName(event.target.value)}
              placeholder="Ej.: Centro comunitario"
              value={displayName}
            />
            <button disabled={busy} onClick={handleCreate} type="button">
              Crear workspace
            </button>
          </section>
          <section aria-labelledby="open-workspace-title" className="welcomePanel">
            <h2 id="open-workspace-title">Abrir workspace existente</h2>
            <label htmlFor="workspace-link-input">Slug o enlace completo</label>
            <input
              id="workspace-link-input"
              onChange={(event) => setOpenValue(event.target.value)}
              placeholder="lince-sereno-sendero o https://..."
              value={openValue}
            />
            <button disabled={busy} onClick={handleOpen} type="button">
              Abrir workspace existente
            </button>
          </section>
        </div>
        <p aria-live="polite" className="message" role="status">
          {message || "No guardamos tu enlace por ti."}
        </p>
      </section>
      {workspace ? (
        <WorkspaceCreatedDialog
          onContinue={() => router.push(`/w/${workspace.slug}/mis-materiales`)}
          workspace={workspace}
        />
      ) : null}
    </main>
  );
}
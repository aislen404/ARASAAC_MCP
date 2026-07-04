"use client";

import { FormEvent, useState } from "react";

type Pictogram = {
  pictogram_id: number;
  label: string;
  source_url: string;
  origin: "ARASAAC";
  author: "Sergio Palao";
  owner: "Gobierno de Aragón";
  license: "CC BY-NC-SA";
  retrieved_at: string;
};

type SelectedItem = {
  key: string;
  text: string;
  pictogram: Pictogram;
};

type Material = {
  material_id: string;
  title: string;
  material_type: "visual_agenda" | "communication_board";
  status: "draft" | "in_review" | "approved" | "rejected";
  attribution_text: string;
};

type SearchResponse = {
  candidates: Pictogram[];
  requires_human_selection: true;
};

type MaterialResponse = {
  material: Material;
};

type ExportResponse = {
  filename: string;
  media_type: string;
  content_base64: string;
};

const API_URL = "/backend";

export function MaterialBuilder() {
  const [type, setType] = useState<"agenda" | "board">("agenda");
  const [title, setTitle] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Pictogram[]>([]);
  const [items, setItems] = useState<SelectedItem[]>([]);
  const [material, setMaterial] = useState<Material | null>(null);
  const [message, setMessage] = useState("Prepara un borrador sin datos personales.");
  const [busy, setBusy] = useState(false);

  async function search(event: FormEvent) {
    event.preventDefault();
    await run(async () => {
      const response = await api<SearchResponse>("/api/pictograms/search", {
        method: "POST",
        body: JSON.stringify({ query, limit: 12 }),
      });
      setResults(response.candidates);
      setMessage(
        `${response.candidates.length} candidatos encontrados. Elige manualmente.`,
      );
    });
  }

  function selectPictogram(pictogram: Pictogram) {
    setItems((current) => [
      ...current,
      {
        key: crypto.randomUUID(),
        text: pictogram.label,
        pictogram,
      },
    ]);
    setMessage(`“${pictogram.label}” añadido a la vista previa.`);
  }

  function updateText(key: string, text: string) {
    setItems((current) =>
      current.map((item) => (item.key === key ? { ...item, text } : item)),
    );
  }

  function move(key: string, offset: -1 | 1) {
    setItems((current) => {
      const index = current.findIndex((item) => item.key === key);
      const target = index + offset;
      if (index < 0 || target < 0 || target >= current.length) return current;
      const copy = [...current];
      [copy[index], copy[target]] = [copy[target], copy[index]];
      return copy;
    });
  }

  function remove(key: string) {
    setItems((current) => current.filter((item) => item.key !== key));
  }

  async function createMaterial() {
    const minimum = type === "agenda" ? 1 : 2;
    if (!title.trim() || items.length < minimum) {
      setMessage(
        type === "agenda"
          ? "Añade un título y al menos un paso."
          : "Añade un título y al menos dos celdas.",
      );
      return;
    }
    await run(async () => {
      const collection = items.map(({ text, pictogram }) => ({ text, pictogram }));
      const path = type === "agenda" ? "/api/materials/agendas" : "/api/materials/boards";
      const body =
        type === "agenda"
          ? { title: title.trim(), steps: collection }
          : { title: title.trim(), cells: collection };
      const response = await api<MaterialResponse>(path, {
        method: "POST",
        body: JSON.stringify(body),
      });
      setMaterial(response.material);
      setMessage("Borrador creado. Revisa la vista previa antes de enviarlo.");
    });
  }

  async function submitReview() {
    if (!material) return;
    await run(async () => {
      const response = await api<MaterialResponse>(
        `/api/materials/${material.material_id}/submit`,
        { method: "POST" },
      );
      setMaterial(response.material);
      setMessage("Material enviado a revisión humana.");
    });
  }

  async function decide(outcome: "approved" | "rejected") {
    if (!material) return;
    await run(async () => {
      const response = await api<MaterialResponse>(
        `/api/materials/${material.material_id}/review`,
        {
          method: "POST",
          body: JSON.stringify({
            outcome,
            human_confirmed: true,
            note:
              outcome === "approved"
                ? "Revisión humana completada desde la Web App."
                : "La revisión humana solicita cambios.",
          }),
        },
      );
      setMaterial(response.material);
      setMessage(
        outcome === "approved"
          ? "Material aprobado. Ya se puede exportar."
          : "Material rechazado. Debe corregirse antes de exportar.",
      );
    });
  }

  async function download(format: "html" | "pdf") {
    if (!material) return;
    await run(async () => {
      const response = await api<ExportResponse>(
        `/api/materials/${material.material_id}/export?format=${format}`,
      );
      const bytes = Uint8Array.from(atob(response.content_base64), (value) =>
        value.charCodeAt(0),
      );
      const blob = new Blob([bytes], { type: response.media_type });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = response.filename;
      link.click();
      URL.revokeObjectURL(link.href);
      setMessage(`Exportación ${format.toUpperCase()} preparada.`);
    });
  }

  async function run(action: () => Promise<void>) {
    setBusy(true);
    try {
      await action();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Error inesperado.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="workspace">
      <section aria-labelledby="create-heading" className="panel">
        <p className="stepLabel">Paso 1</p>
        <h2 id="create-heading">Configura el material</h2>
        <fieldset>
          <legend>Tipo de material</legend>
          <label>
            <input
              checked={type === "agenda"}
              name="material-type"
              onChange={() => setType("agenda")}
              type="radio"
            />
            Agenda visual
          </label>
          <label>
            <input
              checked={type === "board"}
              name="material-type"
              onChange={() => setType("board")}
              type="radio"
            />
            Tablero de comunicación
          </label>
        </fieldset>
        <label htmlFor="material-title">Título genérico, sin nombres personales</label>
        <input
          id="material-title"
          maxLength={120}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="Ej.: Rutina de entrada"
          value={title}
        />

        <form onSubmit={search}>
          <label htmlFor="pictogram-query">Buscar pictogramas reales ARASAAC</label>
          <div className="inlineForm">
            <input
              id="pictogram-query"
              maxLength={120}
              onChange={(event) => setQuery(event.target.value)}
              required
              value={query}
            />
            <button disabled={busy} type="submit">
              Buscar
            </button>
          </div>
        </form>
        <p className="helpText">
          No introduzcas nombres, diagnósticos ni información personal.
        </p>
        <div aria-label="Resultados de búsqueda" className="results" role="region">
          {results.map((pictogram) => (
            <article className="resultCard" key={pictogram.pictogram_id}>
              {/* Native img preserves the original ARASAAC asset URL. */}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                alt={pictogram.label}
                height="112"
                src={pictogram.source_url}
                width="112"
              />
              <p>{pictogram.label}</p>
              <button
                onClick={() => selectPictogram(pictogram)}
                type="button"
              >
                Seleccionar {pictogram.label}
              </button>
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="preview-heading" className="panel previewPanel">
        <p className="stepLabel">Paso 2</p>
        <h2 id="preview-heading">Vista previa editable</h2>
        {items.length === 0 ? (
          <p>Aún no has seleccionado pictogramas.</p>
        ) : (
          <ol className="previewList">
            {items.map((item, index) => (
              <li className="previewItem" key={item.key}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  alt={item.pictogram.label}
                  height="128"
                  src={item.pictogram.source_url}
                  width="128"
                />
                <label htmlFor={`text-${item.key}`}>Texto del elemento {index + 1}</label>
                <input
                  id={`text-${item.key}`}
                  maxLength={240}
                  onChange={(event) => updateText(item.key, event.target.value)}
                  value={item.text}
                />
                <div className="itemActions">
                  <button
                    disabled={index === 0}
                    onClick={() => move(item.key, -1)}
                    type="button"
                  >
                    Subir
                  </button>
                  <button
                    disabled={index === items.length - 1}
                    onClick={() => move(item.key, 1)}
                    type="button"
                  >
                    Bajar
                  </button>
                  <button onClick={() => remove(item.key)} type="button">
                    Eliminar
                  </button>
                </div>
              </li>
            ))}
          </ol>
        )}
        <aside className="attribution">
          Pictogramas: Sergio Palao. Origen: ARASAAC. Propietario: Gobierno de
          Aragón. Licencia: CC BY-NC-SA.
        </aside>
        <button disabled={busy || material !== null} onClick={createMaterial} type="button">
          Crear borrador
        </button>
      </section>

      <section aria-labelledby="review-heading" className="panel reviewPanel">
        <p className="stepLabel">Paso 3</p>
        <h2 id="review-heading">Revisión y exportación</h2>
        <p aria-live="polite" className="message" role="status">
          {message}
        </p>
        <p>
          Estado: <strong>{material?.status ?? "sin borrador"}</strong>
        </p>
        <div className="reviewActions">
          <button
            disabled={busy || material?.status !== "draft"}
            onClick={submitReview}
            type="button"
          >
            Enviar a revisión
          </button>
          <button
            disabled={busy || material?.status !== "in_review"}
            onClick={() => decide("approved")}
            type="button"
          >
            Aprobar tras revisión humana
          </button>
          <button
            disabled={busy || material?.status !== "in_review"}
            onClick={() => decide("rejected")}
            type="button"
          >
            Rechazar
          </button>
          <button
            disabled={busy || material?.status !== "approved"}
            onClick={() => download("html")}
            type="button"
          >
            Exportar HTML
          </button>
          <button
            disabled={busy || material?.status !== "approved"}
            onClick={() => download("pdf")}
            type="button"
          >
            Exportar PDF
          </button>
        </div>
      </section>
    </div>
  );
}

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null;
    throw new Error(body?.detail ?? `Error HTTP ${response.status}.`);
  }
  return (await response.json()) as T;
}

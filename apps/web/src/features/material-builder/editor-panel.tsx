"use client";

import type { useMaterialBuilder } from "./use-material-builder";

type Builder = ReturnType<typeof useMaterialBuilder>;

export function EditorPanel({
  builder,
  embedded = false,
}: Readonly<{ builder: Builder; embedded?: boolean }>) {
  const { type, items, material, message, busy, updateText, move, remove, createMaterial } =
    builder;

  const previewClass =
    type === "signage"
      ? "previewList previewListHorizontal"
      : type === "story"
        ? "previewList previewListStory"
        : "previewList";

  return (
    <section
      aria-labelledby="preview-heading"
      className={embedded ? "cs-panel cs-builder-panel previewPanel" : "panel previewPanel"}
    >
      <p className={embedded ? "cs-eyebrow" : "stepLabel"}>Paso 2</p>
      <h2 id="preview-heading">Vista previa editable</h2>
      {items.length === 0 ? (
        <p>Aún no has seleccionado pictogramas.</p>
      ) : (
        <ol className={previewClass}>
          {items.map((item, index) => (
            <li className="previewItem" key={item.key}>
              {type === "story" ? (
                <span aria-hidden="true" className="storyNumber">
                  {index + 1}
                </span>
              ) : null}
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                alt={item.pictogram.label}
                height="128"
                src={item.pictogram.source_url}
                width="128"
              />
              <label htmlFor={`text-${item.key}`}>Texto del elemento {index + 1}</label>
              <input
                className={embedded ? "cs-input" : undefined}
                id={`text-${item.key}`}
                maxLength={240}
                onChange={(event) => updateText(item.key, event.target.value)}
                value={item.text}
              />
              <div className="itemActions">
                <button
                  className={embedded ? "cs-button secondary" : undefined}
                  disabled={index === 0}
                  onClick={() => move(item.key, -1)}
                  type="button"
                >
                  Subir
                </button>
                <button
                  className={embedded ? "cs-button secondary" : undefined}
                  disabled={index === items.length - 1}
                  onClick={() => move(item.key, 1)}
                  type="button"
                >
                  Bajar
                </button>
                <button
                  className={embedded ? "cs-button secondary" : undefined}
                  onClick={() => remove(item.key)} type="button">
                  Eliminar
                </button>
              </div>
            </li>
          ))}
        </ol>
      )}
      <div className="attribution" role="note">
        Pictogramas: Sergio Palao. Origen: ARASAAC. Propietario: Gobierno de Aragón. Licencia:
        CC BY-NC-SA.
      </div>
      <p
        aria-live="polite"
        className={embedded ? "cs-ai-feedback" : "message"}
        role="status"
      >
        {message}
      </p>
      <button
        className={embedded ? "cs-button" : undefined}
        disabled={busy || material !== null}
        onClick={createMaterial}
        type="button"
      >
        Crear borrador
      </button>
    </section>
  );
}

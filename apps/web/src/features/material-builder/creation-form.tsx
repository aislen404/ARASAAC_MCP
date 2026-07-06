"use client";

import type { useMaterialBuilder } from "./use-material-builder";

type Builder = ReturnType<typeof useMaterialBuilder>;

function panelClass(embedded: boolean) {
  return embedded ? "cs-panel cs-builder-panel" : "panel";
}

function stepClass(embedded: boolean) {
  return embedded ? "cs-eyebrow" : "stepLabel";
}

function inputClass(embedded: boolean) {
  return embedded ? "cs-input" : undefined;
}

function buttonClass(embedded: boolean) {
  return embedded ? "cs-button" : undefined;
}

export function CreationForm({
  builder,
  embedded = false,
}: Readonly<{ builder: Builder; embedded?: boolean }>) {
  const {
    type,
    setType,
    title,
    setTitle,
    query,
    setQuery,
    results,
    aiStatus,
    aiObjective,
    setAIObjective,
    aiItemCount,
    setAIItemCount,
    privacyConfirmed,
    setPrivacyConfirmed,
    aiPlan,
    busy,
    message,
    generateAIPlan,
    search,
    selectPictogram,
  } = builder;

  const minimumItems =
    type === "agenda" || type === "story" || type === "document" ? 1 : 2;

  const aiStatusClass = embedded
    ? aiStatus === null
      ? "cs-ai-status loading"
      : aiStatus.available
        ? "cs-ai-status available"
        : "cs-ai-status unavailable"
    : aiStatus?.available
      ? "aiAvailable"
      : "aiUnavailable";

  const aiStatusLabel =
    aiStatus === null
      ? "Comprobando conexión con el servidor…"
      : aiStatus.available
        ? `Disponible · ${aiStatus.model}`
        : "No configurada";

  return (
    <section aria-labelledby="create-heading" className={panelClass(embedded)} id="crear">
      <p className={stepClass(embedded)}>Paso 1</p>
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
        <label>
          <input
            checked={type === "document"}
            name="material-type"
            onChange={() => setType("document")}
            type="radio"
          />
          Lectura fácil
        </label>
        <label>
          <input
            checked={type === "story"}
            name="material-type"
            onChange={() => setType("story")}
            type="radio"
          />
          Historia social
        </label>
        <label>
          <input
            checked={type === "signage"}
            name="material-type"
            onChange={() => setType("signage")}
            type="radio"
          />
          Señalética
        </label>
      </fieldset>
      <label className={embedded ? "cs-field" : undefined} htmlFor="material-title">
        Título genérico, sin nombres personales
      </label>
      <input
        className={inputClass(embedded)}
        id="material-title"
        maxLength={120}
        onChange={(event) => setTitle(event.target.value)}
        placeholder="Ej.: Rutina de entrada"
        value={title}
      />

      <section aria-labelledby="ai-assistant-heading" className="aiAssistant">
        <div className="aiAssistantHeader">
          <div>
            <p className={stepClass(embedded)}>Asistente opcional</p>
            <h3 id="ai-assistant-heading">Proponer estructura con IA</h3>
          </div>
          <p aria-live="polite" className={aiStatusClass}>
            {aiStatusLabel}
          </p>
        </div>
        <p>
          La IA solo propone texto y búsquedas. No genera pictogramas, no decide por ti y no
          crea el material.
        </p>
        {aiStatus && !aiStatus.available ? (
          <p className="helpText">
            El flujo manual sigue disponible. {aiStatus.reason}{" "}
            <a href="/backend/api/ai/status" rel="noopener noreferrer" target="_blank">
              Ver estado del servidor
            </a>
          </p>
        ) : null}
        {embedded ? (
          <p aria-live="polite" className="cs-ai-feedback" role="status">
            {message}
          </p>
        ) : null}
        <label className={embedded ? "cs-field" : undefined} htmlFor="ai-objective">
          Situación genérica, sin nombres ni diagnósticos
        </label>
        <textarea
          className={embedded ? "cs-textarea" : undefined}
          id="ai-objective"
          maxLength={500}
          onChange={(event) => setAIObjective(event.target.value)}
          placeholder="Ej.: Preparar una visita genérica a la biblioteca"
          rows={3}
          value={aiObjective}
        />
        <label className={embedded ? "cs-field" : undefined} htmlFor="ai-item-count">
          Número de conceptos
        </label>
        <input
          className={inputClass(embedded)}
          id="ai-item-count"
          max={12}
          min={minimumItems}
          onChange={(event) => setAIItemCount(event.target.value)}
          type="number"
          value={aiItemCount}
        />
        <label className="checkLabel">
          <input
            checked={privacyConfirmed}
            onChange={(event) => setPrivacyConfirmed(event.target.checked)}
            type="checkbox"
          />
          Confirmo que el texto es genérico y no contiene datos personales, contacto,
          diagnósticos ni información sensible.
        </label>
        <button
          className={buttonClass(embedded)}
          disabled={
            busy ||
            !privacyConfirmed ||
            aiObjective.trim().length < 10 ||
            aiStatus?.available === false
          }
          onClick={generateAIPlan}
          type="button"
        >
          {busy ? "Generando propuesta…" : "Generar propuesta textual"}
        </button>

        {aiPlan ? (
          <div aria-label="Propuesta de IA" className="aiPlan" role="region">
            <p>
              <strong>Resumen:</strong> {aiPlan.summary}
            </p>
            <p className="helpText">{aiPlan.warning}</p>
            <ol>
              {aiPlan.items.map((plannedItem, itemIndex) => (
                <li key={`${plannedItem.search_term}-${itemIndex}`}>
                  <h4>{plannedItem.text}</h4>
                  <p className="searchTerm">
                    Búsqueda ARASAAC: “{plannedItem.search_term}”
                  </p>
                  {plannedItem.candidates.length === 0 ? (
                    <p>Sin candidatos. Usa la búsqueda manual.</p>
                  ) : (
                    <div className="aiCandidates">
                      {plannedItem.candidates.map((pictogram) => (
                        <article
                          className="resultCard"
                          key={`${itemIndex}-${pictogram.pictogram_id}`}
                        >
                          {/* eslint-disable-next-line @next/next/no-img-element */}
                          <img
                            alt={pictogram.label}
                            height="96"
                            src={pictogram.source_url}
                            width="96"
                          />
                          <p>{pictogram.label}</p>
                          <button
                            className={buttonClass(embedded)}
                            onClick={() => selectPictogram(pictogram, plannedItem.text)}
                            type="button"
                          >
                            Elegir {pictogram.label} para {plannedItem.text}
                          </button>
                        </article>
                      ))}
                    </div>
                  )}
                </li>
              ))}
            </ol>
            <p className="aiTrace">
              Propuesta textual: {aiPlan.provider} · {aiPlan.model}. Pictogramas: resultados
              reales ARASAAC.
            </p>
          </div>
        ) : null}
      </section>

      <form onSubmit={search}>
        <label className={embedded ? "cs-field" : undefined} htmlFor="pictogram-query">
          Buscar pictogramas reales ARASAAC manualmente
        </label>
        <div className="inlineForm">
          <input
            className={inputClass(embedded)}
            id="pictogram-query"
            maxLength={120}
            onChange={(event) => setQuery(event.target.value)}
            required
            value={query}
          />
          <button className={buttonClass(embedded)} disabled={busy} type="submit">
            Buscar
          </button>
        </div>
      </form>
      <p className="helpText">No introduzcas nombres, diagnósticos ni información personal.</p>
      <div aria-label="Resultados de búsqueda" className="results" role="region">
        {results.map((pictogram) => (
          <article className="resultCard" key={pictogram.pictogram_id}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              alt={pictogram.label}
              height="112"
              src={pictogram.source_url}
              width="112"
            />
            <p>{pictogram.label}</p>
            <button
              className={buttonClass(embedded)}
              onClick={() => selectPictogram(pictogram)}
              type="button"
            >
              Seleccionar {pictogram.label}
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}

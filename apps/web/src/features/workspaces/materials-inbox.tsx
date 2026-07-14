"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";

import { listWorkspaceMaterials } from "./api";
import { useWorkspace } from "./workspace-context";
import type { WorkspaceMaterial } from "./types";

const PAGE_SIZE = 20;

function formatStatus(status: WorkspaceMaterial["status"]): string {
  return {
    draft: "Borrador · editable",
    in_review: "En revisión · bloqueado",
    approved: "Aprobado · listo para descargar",
    rejected: "Rechazado · requiere cambios",
  }[status];
}

export function MaterialsInbox() {
  const { workspace } = useWorkspace();
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [statuses, setStatuses] = useState<string[]>([]);
  const [items, setItems] = useState<WorkspaceMaterial[]>([]);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [message, setMessage] = useState("");
  const firstResultRef = useRef<HTMLAnchorElement | null>(null);

  const requestKey = `${workspace.slug}|${debouncedQuery}|${statuses.join(",")}|${offset}`;

  useEffect(() => {
    const id = window.setTimeout(() => setDebouncedQuery(query), 250);
    return () => window.clearTimeout(id);
  }, [query]);

  useEffect(() => {
    listWorkspaceMaterials(workspace.slug, {
      q: debouncedQuery || undefined,
      status: statuses.length > 0 ? statuses.join(",") : undefined,
      limit: PAGE_SIZE,
      offset,
    })
      .then((response) => {
        setItems(response.materials);
        setTotal(response.total);
        setMessage("");
      })
      .catch((error) => {
        setItems([]);
        setTotal(0);
        setMessage(error instanceof Error ? error.message : "No se pudo cargar la bandeja.");
      });
  }, [workspace.slug, debouncedQuery, statuses, offset]);

  useEffect(() => {
    if (items.length > 0) {
      firstResultRef.current?.focus();
    }
  }, [requestKey, items]);

  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const currentPage = Math.floor(offset / PAGE_SIZE) + 1;

  function toggleStatus(status: string) {
    setOffset(0);
    setStatuses((current) =>
      current.includes(status) ? current.filter((value) => value !== status) : [...current, status],
    );
  }

  const emptyMessage = useMemo(() => {
    if (query || statuses.length > 0) {
      return "No hay resultados para los filtros actuales.";
    }
    return "Aún no has creado ningún material.";
  }, [query, statuses]);

  return (
    <section className="workspacePanel">
      <div className="workspacePanelHeader">
        <div>
          <p className="eyebrow">Mis materiales</p>
          <h2>Bandeja del workspace</h2>
        </div>
        <Link className="workspaceLinkButton" href={`/w/${workspace.slug}/nuevo`}>
          Crear el primero
        </Link>
      </div>
      <fieldset>
        <legend>Filtrar por estado</legend>
        {[
          ["draft", "Borrador"],
          ["in_review", "En revisión"],
          ["approved", "Aprobado"],
          ["rejected", "Rechazado"],
        ].map(([value, label]) => (
          <label key={value}>
            <input
              checked={statuses.includes(value)}
              onChange={() => toggleStatus(value)}
              type="checkbox"
            />
            {label}
          </label>
        ))}
      </fieldset>
      <label htmlFor="workspace-search">Buscar por título</label>
      <input id="workspace-search" onChange={(event) => setQuery(event.target.value)} value={query} />
      <p aria-live="polite" className="helpText" role="status">
        {message || `Total: ${total}`}
      </p>
      {items.length === 0 ? (
        <div className="workspaceEmptyState">
          <p>{emptyMessage}</p>
          <Link className="workspaceLinkButton" href={`/w/${workspace.slug}/nuevo`}>
            Crear el primero
          </Link>
        </div>
      ) : (
        <ul className="workspaceList">
          {items.map((item, index) => (
            <li className="workspaceListItem" key={item.material_id}>
              <div>
                <h3>{item.title}</h3>
                <p>{formatStatus(item.status)}</p>
                <p title={new Date(item.updated_at).toLocaleString()}>
                  Actualizado: {new Date(item.updated_at).toLocaleString()}
                </p>
              </div>
              <div className="workspaceItemActions">
                <Link
                  href={`/w/${workspace.slug}/material/${item.material_id}`}
                  ref={index === 0 ? firstResultRef : undefined}
                >
                  {item.status === "approved" ? "Ver" : "Retomar"}
                </Link>
                <Link href={`/w/${workspace.slug}/material/${item.material_id}#audit`}>
                  Ver auditoría
                </Link>
                {item.status === "approved" ? (
                  <Link href={`/w/${workspace.slug}/material/${item.material_id}#downloads`}>
                    Descargar
                  </Link>
                ) : null}
              </div>
            </li>
          ))}
        </ul>
      )}
      <nav aria-label="Paginación de materiales" className="workspacePagination">
        <button
          disabled={currentPage <= 1}
          onClick={() => setOffset(Math.max(0, offset - PAGE_SIZE))}
          type="button"
        >
          Anterior
        </button>
        <span>
          Página {currentPage} de {pages} · {total} materiales
        </span>
        <button
          disabled={currentPage >= pages}
          onClick={() => setOffset(offset + PAGE_SIZE)}
          type="button"
        >
          Siguiente
        </button>
      </nav>
    </section>
  );
}
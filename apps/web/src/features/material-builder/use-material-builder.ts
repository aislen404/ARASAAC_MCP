"use client";

import { FormEvent, useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { api, buildWorkspacePath, validateMaterial } from "./api";
import { computeFlowPhase, useMaterialFlow } from "./flow-context";
import type {
  AIPlanResponse,
  AIStatus,
  ExportResponse,
  Material,
  MaterialBuilderType,
  MaterialResponse,
  Pictogram,
  SearchResponse,
  SelectedItem,
  ValidationReport,
} from "./types";

export function useMaterialBuilder() {
  const params = useParams<{ slug?: string }>();
  const slug = typeof params?.slug === "string" ? params.slug : "";
  const { setPhase } = useMaterialFlow();
  const [type, setType] = useState<MaterialBuilderType>("agenda");
  const [title, setTitle] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Pictogram[]>([]);
  const [aiStatus, setAIStatus] = useState<AIStatus | null>(null);
  const [aiObjective, setAIObjective] = useState("");
  const [aiItemCount, setAIItemCount] = useState("6");
  const [privacyConfirmed, setPrivacyConfirmed] = useState(false);
  const [aiPlan, setAIPlan] = useState<AIPlanResponse | null>(null);
  const [items, setItems] = useState<SelectedItem[]>([]);
  const [material, setMaterial] = useState<Material | null>(null);
  const [validationReport, setValidationReport] = useState<ValidationReport | null>(null);
  const [message, setMessage] = useState("Prepara un borrador sin datos personales.");
  const [busy, setBusy] = useState(false);

  function loadMaterial(source: Material) {
    setMaterial(source);
    setTitle(source.title);

    const payload = source.payload;
    if (!payload || typeof payload !== "object") {
      setItems([]);
      return;
    }

    const entries = [
      "steps",
      "cells",
      "sections",
      "scenes",
      "signs",
    ].flatMap((key) => {
      const value = payload[key as keyof typeof payload];
      return Array.isArray(value) ? value : [];
    });

    setItems(
      entries.flatMap((entry) => {
        if (!entry || typeof entry !== "object") return [];
        const candidate = entry as {
          text?: unknown;
          pictogram?: unknown;
        };
        const pictogram = candidate.pictogram;
        if (!pictogram || typeof pictogram !== "object") return [];
        const typedPictogram = pictogram as Pictogram;
        if (
          typeof typedPictogram.pictogram_id !== "number" ||
          typeof typedPictogram.label !== "string" ||
          typeof typedPictogram.source_url !== "string"
        ) {
          return [];
        }
        return [
          {
            key: crypto.randomUUID(),
            text:
              typeof candidate.text === "string" && candidate.text.trim().length > 0
                ? candidate.text
                : typedPictogram.label,
            pictogram: typedPictogram,
          },
        ];
      }),
    );

    const typeByMaterial = {
      visual_agenda: "agenda",
      communication_board: "board",
      accessible_document: "document",
      social_story: "story",
      signage: "signage",
    } as const;
    setType(typeByMaterial[source.material_type]);
  }

  useEffect(() => {
    setPhase(
      computeFlowPhase({
        hasSearchResults: results.length > 0,
        itemCount: items.length,
        materialStatus: material?.status ?? null,
      }),
    );
  }, [results.length, items.length, material?.status, setPhase]);

  useEffect(() => {
    let active = true;
    api<AIStatus>("/api/ai/status")
      .then((status) => {
        if (active) setAIStatus(status);
      })
      .catch(() => {
        if (active) {
          setAIStatus({
            available: false,
            provider: "unavailable",
            model: null,
            reason: "No se pudo consultar el estado de la IA.",
            generates_pictograms: false,
            requires_human_selection: true,
            stores_input: false,
          });
        }
      });
    return () => {
      active = false;
    };
  }, []);

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

  async function generateAIPlan() {
    if (!privacyConfirmed || aiObjective.trim().length < 10) {
      setMessage(
        "Describe un escenario genérico de al menos 10 caracteres y confirma que no contiene datos personales.",
      );
      return;
    }
    await run(async () => {
      const minimum = type === "agenda" || type === "story" ? 1 : 2;
      const requestedCount = Math.min(
        12,
        Math.max(minimum, Number.parseInt(aiItemCount, 10) || minimum),
      );
      const materialTypeMap = {
        agenda: "visual_agenda",
        board: "communication_board",
        document: "accessible_document",
        story: "social_story",
        signage: "signage",
      } as const;
      const response = await api<AIPlanResponse>("/api/ai/plan", {
        method: "POST",
        body: JSON.stringify({
          material_type: materialTypeMap[type],
          objective: aiObjective.trim(),
          item_count: requestedCount,
          locale: "es",
          no_personal_data_confirmed: true,
        }),
      });
      setAIPlan(response);
      setMessage(
        `La IA propuso ${response.items.length} conceptos. Revisa el texto y elige manualmente cada pictograma.`,
      );
    });
  }

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

  function selectPictogram(pictogram: Pictogram, text = pictogram.label) {
    setItems((current) => [
      ...current,
      { key: crypto.randomUUID(), text, pictogram },
    ]);
    setMessage(`“${text}” añadido a la vista previa para revisión.`);
  }

  function updateText(key: string, text: string) {
    if (material?.status === "approved") return;
    setItems((current) =>
      current.map((item) => (item.key === key ? { ...item, text } : item)),
    );
  }

  function move(key: string, offset: -1 | 1) {
    if (material?.status === "approved") return;
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
    if (material?.status === "approved") return;
    setItems((current) => current.filter((item) => item.key !== key));
  }

  async function createMaterial() {
    const minimum =
      type === "agenda" || type === "story" || type === "document" ? 1 : 2;
    if (!title.trim() || items.length < minimum) {
      setMessage(
        minimum === 1
          ? "Añade un título y al menos un elemento."
          : "Añade un título y al menos dos celdas.",
      );
      return;
    }
    await run(async () => {
      const collection = items.map(({ text, pictogram }) => ({ text, pictogram }));
      const pathByType = {
        agenda: "/materials/agendas",
        board: "/materials/boards",
        document: "/materials/documents",
        story: "/materials/stories",
        signage: "/materials/signage",
      } as const;
      const bodyByType = {
        agenda: { title: title.trim(), steps: collection },
        board: { title: title.trim(), cells: collection },
        document: { title: title.trim(), sections: collection },
        story: { title: title.trim(), scenes: collection },
        signage: { title: title.trim(), signs: collection },
      } as const;
      const response = await api<MaterialResponse>(buildWorkspacePath(slug, pathByType[type]), {
        method: "POST",
        body: JSON.stringify(bodyByType[type]),
      });
      setMaterial(response.material);
      setValidationReport(null);
      setMessage("Borrador creado. Revisa la vista previa antes de enviarlo.");
    });
  }

  async function runValidation() {
    if (!material) return;

    const currentVersion = material.version ?? 0;
    if (validationReport && validationReport.material_version === currentVersion) {
      setMessage(
        validationReport.is_blocking
          ? "La validación sigue bloqueando la revisión. Corrige los findings antes de continuar."
          : "Validación ya actualizada para esta versión del material.",
      );
      return;
    }

    await run(async () => {
      const report = await validateMaterial(
        buildWorkspacePath(slug, `/materials/${material.material_id}/validate`),
      );
      setValidationReport(report);
      setMessage(
        report.is_blocking
          ? "La validación ha detectado bloqueos. Revísalos antes de enviar a revisión."
          : report.warning_count > 0
            ? "Validación completada con avisos. Puedes continuar tras revisarlos."
            : "Validación completada sin incidencias bloqueantes.",
      );
    });
  }

  async function submitReview() {
    if (!material) return;
    if (validationReport?.is_blocking) {
      setMessage("No puedes enviar a revisión mientras existan bloqueos de validación.");
      return;
    }
    await run(async () => {
      const response = await api<MaterialResponse>(
        buildWorkspacePath(slug, `/materials/${material.material_id}/submit`),
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
        buildWorkspacePath(slug, `/materials/${material.material_id}/review`),
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

  async function download(format: "html" | "pdf" | "docx" | "pptx" | "zip") {
    if (!material) return;
    await run(async () => {
      const response = await api<ExportResponse>(
        `${buildWorkspacePath(slug, `/materials/${material.material_id}/export`)}?format=${format}`,
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

  return {
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
    items,
    material,
    validationReport,
    message,
    busy,
    isReadOnly: material?.status === "approved",
    loadMaterial,
    generateAIPlan,
    search,
    selectPictogram,
    updateText,
    move,
    remove,
    createMaterial,
    runValidation,
    submitReview,
    decide,
    download,
  };
}

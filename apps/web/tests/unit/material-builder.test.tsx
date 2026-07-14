import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { MaterialBuilder } from "../../src/app/material-builder";
import { MaterialBuilderProvider } from "../../src/features/material-builder/builder-context";
import { MaterialFlowProvider } from "../../src/features/material-builder/flow-context";

function renderBuilder() {
  return render(
    <MaterialFlowProvider>
      <MaterialBuilderProvider>
        <MaterialBuilder />
      </MaterialBuilderProvider>
    </MaterialFlowProvider>,
  );
}

const pictogram = {
  pictogram_id: 6964,
  label: "casa",
  source_url: "https://static.arasaac.org/pictograms/6964/6964_300.png",
  origin: "ARASAAC",
  author: "Sergio Palao",
  owner: "Gobierno de Aragón",
  license: "CC BY-NC-SA",
  retrieved_at: "2026-07-04T00:00:00Z",
};

const aiStatus = {
  available: true,
  provider: "openai",
  model: "gpt-5.4-mini",
  reason: null,
  generates_pictograms: false,
  requires_human_selection: true,
  stores_input: false,
};

function response(body: unknown, ok = true, status = 200) {
  return Promise.resolve({
    ok,
    status,
    json: () => Promise.resolve(body),
  } as Response);
}

describe("guided material flow", () => {
  beforeEach(() => {
    let id = 0;
    vi.stubGlobal("crypto", { randomUUID: () => `selected-${++id}` });
    vi.stubGlobal("fetch", vi.fn());
    vi.stubGlobal("atob", (value: string) => Buffer.from(value, "base64").toString("binary"));
    vi.stubGlobal("URL", {
      createObjectURL: () => "blob:export",
      revokeObjectURL: vi.fn(),
    });
    HTMLAnchorElement.prototype.click = vi.fn();
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("searches, selects, creates, reviews, and exports an agenda", async () => {
    let status = "draft";
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation((input) => {
      const url = String(input);
      if (url.endsWith("/api/ai/status")) {
        return response(aiStatus);
      }
      if (url.endsWith("/api/pictograms/search")) {
        return response({ candidates: [pictogram], requires_human_selection: true });
      }
      if (url.endsWith("/api/materials/agendas")) {
        return response({ material: material(status) }, true, 201);
      }
      if (url.endsWith("/submit")) {
        status = "in_review";
        return response({ material: material(status) });
      }
      if (url.endsWith("/review")) {
        status = "approved";
        return response({ material: material(status) });
      }
      if (url.includes("/export?format=html")) {
        return response({
          filename: "material.html",
          media_type: "text/html",
          content_base64: btoa("<html></html>"),
        });
      }
      throw new Error(`Unexpected request: ${url}`);
    });

    const user = userEvent.setup();
    renderBuilder();
    await user.type(
      screen.getByLabelText("Título genérico, sin nombres personales"),
      "Rutina de entrada",
    );
    await user.type(
      screen.getByLabelText("Buscar pictogramas reales ARASAAC manualmente"),
      "casa",
    );
    await user.click(screen.getByRole("button", { name: "Buscar" }));
    await user.click(
      await screen.findByRole("button", { name: "Seleccionar casa" }),
    );
    await user.clear(screen.getByLabelText("Texto del elemento 1"));
    await user.type(screen.getByLabelText("Texto del elemento 1"), "Llegar");
    await user.click(screen.getByRole("button", { name: "Crear borrador" }));
    await waitFor(() => expect(screen.getByText("Borrador")).toBeTruthy());
    await user.click(screen.getByRole("button", { name: "Enviar a revisión" }));
    await user.click(
      screen.getByRole("button", { name: "Aprobar tras revisión humana" }),
    );
    await user.click(screen.getByRole("button", { name: "Exportar HTML" }));

    await waitFor(() =>
      expect(
        screen
          .getAllByRole("status")
          .some((element) => element.textContent?.includes("preparada")),
      ).toBe(true),
    );
  });

  it("supports board selection, reordering, removal, and validation messages", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation((input) =>
      String(input).endsWith("/api/ai/status")
        ? response(aiStatus)
        : response({ candidates: [pictogram], requires_human_selection: true }),
    );
    const user = userEvent.setup();
    renderBuilder();

    await user.click(screen.getByLabelText("Tablero de comunicación"));
    await user.click(screen.getByRole("button", { name: "Crear borrador" }));
    expect(
      screen
        .getAllByRole("status")
        .some((element) => element.textContent?.includes("dos celdas")),
    ).toBe(true);

    await user.type(
      screen.getByLabelText("Buscar pictogramas reales ARASAAC manualmente"),
      "casa",
    );
    await user.click(screen.getByRole("button", { name: "Buscar" }));
    const select = await screen.findByRole("button", { name: "Seleccionar casa" });
    await user.click(select);
    await user.click(select);
    await user.click(screen.getAllByRole("button", { name: "Subir" })[1]);
    await user.click(screen.getAllByRole("button", { name: "Eliminar" })[0]);
    expect(screen.getAllByLabelText(/Texto del elemento/)).toHaveLength(1);
  });

  it("shows a visible and semantic selected state for chosen pictograms", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation((input) =>
      String(input).endsWith("/api/ai/status")
        ? response(aiStatus)
        : response({ candidates: [pictogram], requires_human_selection: true }),
    );
    const user = userEvent.setup();
    renderBuilder();

    await user.type(
      screen.getByLabelText("Buscar pictogramas reales ARASAAC manualmente"),
      "casa",
    );
    await user.click(screen.getByRole("button", { name: "Buscar" }));

    const select = await screen.findByRole("button", { name: "Seleccionar casa" });
    expect(select.getAttribute("aria-pressed")).toBe("false");

    await user.click(select);

    expect(
      await screen.findByRole("button", { name: "casa seleccionado" }),
    ).toBeTruthy();
    expect(screen.getByText("Seleccionado en la vista previa")).toBeTruthy();
  });

  it("keeps work and announces controlled API failures", async () => {
    vi.mocked(fetch).mockImplementation((input) =>
      String(input).endsWith("/api/ai/status")
        ? response(aiStatus)
        : response({ detail: "Servicio ARASAAC no disponible." }, false, 502),
    );
    const user = userEvent.setup();
    renderBuilder();

    await user.type(
      screen.getByLabelText("Buscar pictogramas reales ARASAAC manualmente"),
      "casa",
    );
    await user.click(screen.getByRole("button", { name: "Buscar" }));

    await waitFor(() =>
      expect(
        screen
          .getAllByRole("status")
          .some((element) => element.textContent?.includes("no disponible")),
      ).toBe(true),
    );
    expect(
      (
        screen.getByLabelText(
          "Buscar pictogramas reales ARASAAC manualmente",
        ) as HTMLInputElement
      ).value,
    ).toBe("casa");
  });

  it("uses an AI text plan but requires explicit ARASAAC selection", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation((input) => {
      const url = String(input);
      if (url.endsWith("/api/ai/status")) return response(aiStatus);
      if (url.endsWith("/api/ai/plan")) {
        return response({
          summary: "Visita genérica",
          items: [
            {
              text: "Entrar",
              search_term: "biblioteca",
              candidates: [pictogram],
            },
          ],
          provider: "openai",
          model: "gpt-5.4-mini",
          requires_human_selection: true,
          creates_material: false,
          stores_input: false,
          warning: "Revisión humana obligatoria.",
        });
      }
      throw new Error(`Unexpected request: ${url}`);
    });
    const user = userEvent.setup();
    renderBuilder();

    await waitFor(() => expect(screen.getByText(/Disponible/)).toBeTruthy());
    await user.type(
      screen.getByLabelText("Situación genérica, sin nombres ni diagnósticos"),
      "Preparar una visita genérica a la biblioteca",
    );
    await user.click(
      screen.getByLabelText(/Confirmo que el texto es genérico/),
    );
    await user.clear(screen.getByLabelText("Número de conceptos"));
    await user.type(screen.getByLabelText("Número de conceptos"), "1");
    await user.click(
      screen.getByRole("button", { name: "Generar propuesta textual" }),
    );

    expect(await screen.findByText("Visita genérica")).toBeTruthy();
    expect(screen.queryAllByLabelText(/Texto del elemento/)).toHaveLength(0);
    await user.click(
      screen.getByRole("button", { name: "Elegir casa para Entrar" }),
    );
    expect(
      (screen.getByLabelText("Texto del elemento 1") as HTMLInputElement).value,
    ).toBe("Entrar");

    const planCall = fetchMock.mock.calls.find(([input]) =>
      String(input).endsWith("/api/ai/plan"),
    );
    expect(JSON.parse(String(planCall?.[1]?.body))).toMatchObject({
      no_personal_data_confirmed: true,
      item_count: 1,
    });
  });

  it("keeps the manual flow available when AI status cannot be loaded", async () => {
    vi.mocked(fetch).mockRejectedValue(new Error("status unavailable"));

    renderBuilder();

    expect(
      await screen.findByText("No se pudo consultar el estado de la IA.", {
        exact: false,
      }),
    ).toBeTruthy();
    expect(
      (
        screen.getByRole("button", {
          name: "Generar propuesta textual",
        }) as HTMLButtonElement
      ).disabled,
    ).toBe(true);
    expect(
      (
        screen.getByLabelText(
          "Buscar pictogramas reales ARASAAC manualmente",
        ) as HTMLInputElement
      ).disabled,
    ).toBe(false);
  });

  it("shows AI feedback in embedded creation form", async () => {
    vi.mocked(fetch).mockImplementation((input) =>
      String(input).endsWith("/api/ai/status")
        ? response(aiStatus)
        : response({ detail: "Servicio no disponible." }, false, 502),
    );
    const user = userEvent.setup();
    render(
      <MaterialFlowProvider>
        <MaterialBuilderProvider>
          <MaterialBuilder embedded />
        </MaterialBuilderProvider>
      </MaterialFlowProvider>,
    );

    await screen.findByText(/Disponible · gpt-5.4-mini/);
    await user.type(
      screen.getByLabelText("Situación genérica, sin nombres ni diagnósticos"),
      "Visita genérica a un museo sin nombres",
    );
    await user.click(screen.getByLabelText(/Confirmo que el texto es genérico/i));
    await user.click(screen.getByRole("button", { name: "Generar propuesta textual" }));

    await waitFor(() =>
      expect(
        screen
          .getAllByRole("status")
          .some((element) => element.textContent?.includes("Servicio no disponible")),
      ).toBe(true),
    );
  });

  it("shows visible draft feedback in embedded mode after creating a draft", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation((input) => {
      const url = String(input);
      if (url.endsWith("/api/ai/status")) {
        return response(aiStatus);
      }
      if (url.endsWith("/api/pictograms/search")) {
        return response({ candidates: [pictogram], requires_human_selection: true });
      }
      if (url.endsWith("/api/materials/agendas")) {
        return response({ material: material("draft") }, true, 201);
      }
      throw new Error(`Unexpected request: ${url}`);
    });

    const user = userEvent.setup();
    render(
      <MaterialFlowProvider>
        <MaterialBuilderProvider>
          <MaterialBuilder embedded />
        </MaterialBuilderProvider>
      </MaterialFlowProvider>,
    );

    await screen.findByText(/Disponible · gpt-5.4-mini/);
    await user.type(
      screen.getByLabelText("Título genérico, sin nombres personales"),
      "Rutina de entrada",
    );
    await user.type(
      screen.getByLabelText("Buscar pictogramas reales ARASAAC manualmente"),
      "casa",
    );
    await user.click(screen.getByRole("button", { name: "Buscar" }));
    await user.click(await screen.findByRole("button", { name: "Seleccionar casa" }));
    await user.click(screen.getByRole("button", { name: "Crear borrador" }));

    await waitFor(() => {
      expect(screen.getAllByText("Borrador creado. Revisa la vista previa antes de enviarlo.")).toHaveLength(3);
    });
    expect(screen.getByText("Borrador")).toBeTruthy();
    expect(
      (screen.getByRole("button", { name: "Enviar a revisión" }) as HTMLButtonElement).disabled,
    ).toBe(false);
  });

  it("blocks review when validation reports blocker findings and reuses cached version", async () => {
    const status = "draft";
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation((input) => {
      const url = String(input);
      if (url.endsWith("/api/ai/status")) {
        return response(aiStatus);
      }
      if (url.endsWith("/api/pictograms/search")) {
        return response({ candidates: [pictogram], requires_human_selection: true });
      }
      if (url.endsWith("/api/materials/agendas")) {
        return response({ material: material(status, 3) }, true, 201);
      }
      if (url.endsWith("/validate")) {
        return response({
          material_id: material(status, 3).material_id,
          material_version: 3,
          findings: [
            {
              code: "no_personal_data",
              severity: "blocker",
              message: "Se ha detectado un posible dato personal.",
              field: "items[0].text",
            },
          ],
          blocker_count: 1,
          warning_count: 0,
          ok_count: 2,
          is_blocking: true,
        });
      }
      throw new Error(`Unexpected request: ${url}`);
    });

    const user = userEvent.setup();
    renderBuilder();
    await user.type(
      screen.getByLabelText("Título genérico, sin nombres personales"),
      "Rutina de entrada",
    );
    await user.type(
      screen.getByLabelText("Buscar pictogramas reales ARASAAC manualmente"),
      "casa",
    );
    await user.click(screen.getByRole("button", { name: "Buscar" }));
    await user.click(await screen.findByRole("button", { name: "Seleccionar casa" }));
    await user.click(screen.getByRole("button", { name: "Crear borrador" }));

    await user.click(screen.getByRole("button", { name: "Validar material" }));
    expect(await screen.findByText(/Se ha detectado un posible dato personal/)).toBeTruthy();

    await user.click(screen.getByRole("button", { name: "Enviar a revisión" }));

    await waitFor(() =>
      expect(
        screen
          .getAllByRole("status")
          .some((element) =>
            element.textContent?.includes("No puedes enviar a revisión mientras existan bloqueos"),
          ),
      ).toBe(true),
    );

    await user.click(screen.getByRole("button", { name: "Validar material" }));
    expect(fetchMock.mock.calls.filter(([input]) => String(input).endsWith("/validate"))).toHaveLength(1);
  });
});

function material(status: string, version = 1) {
  return {
    material_id: "00000000-0000-4000-8000-000000000001",
    title: "Rutina de entrada",
    material_type: "visual_agenda",
    status,
    attribution_text: "Atribución ARASAAC",
    version,
  };
}

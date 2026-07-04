import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { MaterialBuilder } from "../../src/app/material-builder";

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
    render(<MaterialBuilder />);
    await user.type(
      screen.getByLabelText("Título genérico, sin nombres personales"),
      "Rutina de entrada",
    );
    await user.type(screen.getByLabelText("Buscar pictogramas reales ARASAAC"), "casa");
    await user.click(screen.getByRole("button", { name: "Buscar" }));
    await user.click(
      await screen.findByRole("button", { name: "Seleccionar casa" }),
    );
    await user.clear(screen.getByLabelText("Texto del elemento 1"));
    await user.type(screen.getByLabelText("Texto del elemento 1"), "Llegar");
    await user.click(screen.getByRole("button", { name: "Crear borrador" }));
    await waitFor(() => expect(screen.getByText("draft")).toBeTruthy());
    await user.click(screen.getByRole("button", { name: "Enviar a revisión" }));
    await user.click(
      screen.getByRole("button", { name: "Aprobar tras revisión humana" }),
    );
    await user.click(screen.getByRole("button", { name: "Exportar HTML" }));

    await waitFor(() =>
      expect(screen.getByRole("status").textContent).toContain("preparada"),
    );
  });

  it("supports board selection, reordering, removal, and validation messages", async () => {
    const fetchMock = vi.mocked(fetch);
    fetchMock.mockImplementation(() =>
      response({ candidates: [pictogram], requires_human_selection: true }),
    );
    const user = userEvent.setup();
    render(<MaterialBuilder />);

    await user.click(screen.getByLabelText("Tablero de comunicación"));
    await user.click(screen.getByRole("button", { name: "Crear borrador" }));
    expect(screen.getByRole("status").textContent).toContain("dos celdas");

    await user.type(screen.getByLabelText("Buscar pictogramas reales ARASAAC"), "casa");
    await user.click(screen.getByRole("button", { name: "Buscar" }));
    const select = await screen.findByRole("button", { name: "Seleccionar casa" });
    await user.click(select);
    await user.click(select);
    await user.click(screen.getAllByRole("button", { name: "Subir" })[1]);
    await user.click(screen.getAllByRole("button", { name: "Eliminar" })[0]);
    expect(screen.getAllByLabelText(/Texto del elemento/)).toHaveLength(1);
  });

  it("keeps work and announces controlled API failures", async () => {
    vi.mocked(fetch).mockImplementation(() =>
      response({ detail: "Servicio ARASAAC no disponible." }, false, 502),
    );
    const user = userEvent.setup();
    render(<MaterialBuilder />);

    await user.type(screen.getByLabelText("Buscar pictogramas reales ARASAAC"), "casa");
    await user.click(screen.getByRole("button", { name: "Buscar" }));

    await waitFor(() =>
      expect(screen.getByRole("status").textContent).toContain("no disponible"),
    );
    expect(
      (screen.getByLabelText("Buscar pictogramas reales ARASAAC") as HTMLInputElement)
        .value,
    ).toBe("casa");
  });
});

function material(status: string) {
  return {
    material_id: "00000000-0000-4000-8000-000000000001",
    title: "Rutina de entrada",
    material_type: "visual_agenda",
    status,
    attribution_text: "Atribución ARASAAC",
  };
}

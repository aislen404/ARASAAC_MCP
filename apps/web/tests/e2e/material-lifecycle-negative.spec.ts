import { expect, test } from "@playwright/test";

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

async function createAgenda(request: import("@playwright/test").APIRequestContext) {
  const created = await request.post("http://127.0.0.1:8100/api/materials/agendas", {
    data: {
      title: "Agenda de prueba negativa",
      steps: [{ text: "Llegar", pictogram }],
    },
  });
  expect(created.status()).toBe(201);
  const body = await created.json();
  return body.material.material_id as string;
}

test.describe("REV-003: transiciones inválidas y ciclo de rechazo", () => {
  test("aprobar sin enviar a revisión devuelve 409 y no cambia el estado", async ({
    request,
  }) => {
    const materialId = await createAgenda(request);
    const response = await request.post(
      `http://127.0.0.1:8100/api/materials/${materialId}/review`,
      { data: { outcome: "approved", human_confirmed: true, note: "Intento inválido." } },
    );
    expect(response.status()).toBe(409);

    const material = await request.get(
      `http://127.0.0.1:8100/api/materials/${materialId}`,
    );
    expect((await material.json()).material.status).toBe("draft");
  });

  test("rechazar y reenviar permite aprobar en un segundo intento", async ({
    request,
  }) => {
    const materialId = await createAgenda(request);
    await request.post(`http://127.0.0.1:8100/api/materials/${materialId}/submit`);

    const rejected = await request.post(
      `http://127.0.0.1:8100/api/materials/${materialId}/review`,
      { data: { outcome: "rejected", human_confirmed: true, note: "Requiere cambios." } },
    );
    expect(rejected.status()).toBe(200);
    expect((await rejected.json()).material.status).toBe("rejected");

    const resubmit = await request.post(
      `http://127.0.0.1:8100/api/materials/${materialId}/submit`,
    );
    expect(resubmit.status()).toBe(200);
    expect((await resubmit.json()).material.status).toBe("in_review");

    const approved = await request.post(
      `http://127.0.0.1:8100/api/materials/${materialId}/review`,
      { data: { outcome: "approved", human_confirmed: true, note: "Ahora sí." } },
    );
    expect(approved.status()).toBe(200);
    expect((await approved.json()).material.status).toBe("approved");
  });
});

test.describe("EXP-001: exportación bloqueada antes de aprobación", () => {
  for (const format of ["html", "pdf", "docx", "pptx", "zip"] as const) {
    test(`formato ${format} devuelve 409 en borrador sin aprobar`, async ({
      request,
    }) => {
      const materialId = await createAgenda(request);
      const response = await request.get(
        `http://127.0.0.1:8100/api/materials/${materialId}/export?format=${format}`,
      );
      expect(response.status()).toBe(409);
    });
  }

  test("botones de exportación permanecen deshabilitados en la interfaz hasta aprobar", async ({
    page,
  }) => {
    await page.route("**/backend/api/pictograms/search", async (route) => {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({ candidates: [pictogram], requires_human_selection: true }),
      });
    });
    await page.goto("/");
    await page.getByLabel("Título genérico, sin nombres personales").fill("Rutina UAT");
    await page
      .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
      .fill("casa");
    await page.getByRole("button", { name: "Buscar" }).click();
    await page.getByRole("button", { name: "Seleccionar casa" }).click();
    await page.getByLabel("Texto del elemento 1").fill("Llegar");
    await page.getByRole("button", { name: "Crear borrador" }).click();
    await expect(page.getByText("draft", { exact: true })).toBeVisible();

    for (const label of [
      "Exportar HTML",
      "Exportar PDF",
      "Exportar DOCX",
      "Exportar PPTX",
      "Exportar ZIP",
    ]) {
      await expect(page.getByRole("button", { name: label })).toBeDisabled();
    }
  });
});

test.describe("MAT-002: límites del tablero de comunicación", () => {
  function cellsPayload(count: number) {
    return Array.from({ length: count }, (_, index) => ({
      text: `Celda ${index + 1}`,
      pictogram,
    }));
  }

  test("acepta el máximo de 24 celdas", async ({ request }) => {
    const response = await request.post("http://127.0.0.1:8100/api/materials/boards", {
      data: { title: "Tablero máximo", cells: cellsPayload(24) },
    });
    expect(response.status()).toBe(201);
  });

  test("rechaza 25 celdas con 422", async ({ request }) => {
    const response = await request.post("http://127.0.0.1:8100/api/materials/boards", {
      data: { title: "Tablero excedido", cells: cellsPayload(25) },
    });
    expect(response.status()).toBe(422);
  });

  test("rechaza una sola celda con 422 (mínimo dos)", async ({ request }) => {
    const response = await request.post("http://127.0.0.1:8100/api/materials/boards", {
      data: { title: "Tablero incompleto", cells: cellsPayload(1) },
    });
    expect(response.status()).toBe(422);
  });
});

test.describe("DB-002 / esquema cerrado: payload corrupto o con campos extra", () => {
  test("rechaza campos adicionales no declarados", async ({ request }) => {
    const response = await request.post("http://127.0.0.1:8100/api/materials/agendas", {
      data: {
        title: "Agenda con campo extra",
        steps: [{ text: "Llegar", pictogram }],
        unexpected_field: "no debería aceptarse",
      },
    });
    expect(response.status()).toBe(422);
  });

  test("rechaza pictograma sin licencia obligatoria", async ({ request }) => {
    const response = await request.post("http://127.0.0.1:8100/api/materials/agendas", {
      data: {
        title: "Agenda con pictograma inválido",
        steps: [
          {
            text: "Llegar",
            pictogram: { ...pictogram, license: "CC0" },
          },
        ],
      },
    });
    expect(response.status()).toBe(422);
  });
});

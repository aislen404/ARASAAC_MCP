import { expect, test } from "@playwright/test";

const API = "http://127.0.0.1:8100/api/ai/plan";

function basePayload(overrides: Record<string, unknown> = {}) {
  return {
    material_type: "visual_agenda",
    objective: "Preparar una visita genérica a la biblioteca del barrio",
    item_count: 3,
    locale: "es",
    no_personal_data_confirmed: true,
    ...overrides,
  };
}

test.describe("AI-003/004/005/006: la API rechaza entradas no gobernadas antes del proveedor", () => {
  test("campos adicionales no declarados devuelven 422 (schema cerrado)", async ({
    request,
  }) => {
    const response = await request.post(API, {
      data: basePayload({ extra_field: "no permitido" }),
    });
    expect(response.status()).toBe(422);
  });

  test("email en el objetivo devuelve 422 antes de llamar al proveedor", async ({
    request,
  }) => {
    const response = await request.post(
      API,
      { data: basePayload({ objective: "Escribir a persona@example.com sobre la rutina" }) },
    );
    expect(response.status()).toBe(422);
  });

  test("teléfono en el objetivo devuelve 422", async ({ request }) => {
    const response = await request.post(API, {
      data: basePayload({ objective: "Llamar al 611 222 333 antes de salir de casa" }),
    });
    expect(response.status()).toBe(422);
  });

  test("DNI/NIE en el objetivo devuelve 422", async ({ request }) => {
    const response = await request.post(API, {
      data: basePayload({ objective: "Documento 12345678Z necesario para la actividad" }),
    });
    expect(response.status()).toBe(422);
  });

  test("URL en el objetivo devuelve 422", async ({ request }) => {
    const response = await request.post(API, {
      data: basePayload({ objective: "Revisar https://ejemplo.com antes de la visita" }),
    });
    expect(response.status()).toBe(422);
  });

  test("lenguaje diagnóstico devuelve 422", async ({ request }) => {
    const response = await request.post(API, {
      data: basePayload({
        objective: "Adaptar la rutina porque tiene un diagnóstico de autismo severo",
      }),
    });
    expect(response.status()).toBe(422);
  });

  test("sin confirmación explícita de privacidad devuelve 422", async ({ request }) => {
    const response = await request.post(API, {
      data: basePayload({ no_personal_data_confirmed: false }),
    });
    expect(response.status()).toBe(422);
  });

  test("cantidad de conceptos fuera de rango devuelve 422", async ({ request }) => {
    const response = await request.post(API, { data: basePayload({ item_count: 20 }) });
    expect(response.status()).toBe(422);
  });

  test("tablero con un solo concepto devuelve 422 (mínimo dos)", async ({ request }) => {
    const response = await request.post(API, {
      data: basePayload({ material_type: "communication_board", item_count: 1 }),
    });
    expect(response.status()).toBe(422);
  });
});

test.describe("AI-009/010: degradación controlada del proveedor en la interfaz", () => {
  test("proveedor no disponible: el formulario bloquea la generación y ofrece flujo manual", async ({
    page,
  }) => {
    await page.route("**/backend/api/ai/status", async (route) => {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          available: false,
          provider: "disabled",
          model: null,
          reason: "La capa IA está desactivada.",
          generates_pictograms: false,
          requires_human_selection: true,
          stores_input: false,
        }),
      });
    });
    await page.goto("/");

    await expect(page.getByText("No configurada")).toBeVisible();
    await expect(
      page.getByRole("button", { name: "Generar propuesta textual" }),
    ).toBeDisabled();
    await expect(page.getByText(/El flujo manual sigue disponible/)).toBeVisible();

    // El flujo manual debe seguir siendo completamente utilizable sin IA.
    await page
      .getByLabel("Título genérico, sin nombres personales")
      .fill("Rutina manual sin IA");
    await expect(
      page.getByLabel("Buscar pictogramas reales ARASAAC manualmente"),
    ).toBeEnabled();
  });

  test("error transitorio del proveedor (504) se informa sin crear material", async ({
    page,
  }) => {
    await page.route("**/backend/api/ai/status", async (route) => {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          available: true,
          provider: "openai",
          model: "gpt-5.4-mini",
          reason: null,
          generates_pictograms: false,
          requires_human_selection: true,
          stores_input: false,
        }),
      });
    });
    await page.route("**/backend/api/ai/plan", async (route) => {
      await route.fulfill({
        status: 504,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Tiempo de espera agotado con el proveedor." }),
      });
    });
    await page.goto("/");

    await page
      .getByLabel("Situación genérica, sin nombres ni diagnósticos")
      .fill("Preparar una visita genérica a la biblioteca");
    await page.getByLabel(/Confirmo que el texto es genérico/).check();
    await page.getByRole("button", { name: "Generar propuesta textual" }).click();

    await expect(page.getByText("Tiempo de espera agotado con el proveedor.")).toBeVisible();
    await expect(page.getByRole("region", { name: "Propuesta de IA" })).toHaveCount(0);
  });

  test("plan IA con cero candidatos exige búsqueda manual (sin auto-selección)", async ({
    page,
  }) => {
    await page.route("**/backend/api/ai/status", async (route) => {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          available: true,
          provider: "openai",
          model: "gpt-5.4-mini",
          reason: null,
          generates_pictograms: false,
          requires_human_selection: true,
          stores_input: false,
        }),
      });
    });
    await page.route("**/backend/api/ai/plan", async (route) => {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          summary: "Concepto sin candidatos oficiales",
          items: [{ text: "Concepto raro", search_term: "xyzzy123", candidates: [] }],
          provider: "openai",
          model: "gpt-5.4-mini",
          requires_human_selection: true,
          creates_material: false,
          stores_input: false,
          warning: "Revisa y selecciona manualmente.",
        }),
      });
    });
    await page.goto("/");

    await page
      .getByLabel("Situación genérica, sin nombres ni diagnósticos")
      .fill("Preparar una visita genérica a la biblioteca");
    await page.getByLabel(/Confirmo que el texto es genérico/).check();
    await page.getByRole("button", { name: "Generar propuesta textual" }).click();

    await expect(page.getByText("Sin candidatos. Usa la búsqueda manual.")).toBeVisible();
    await expect(page.getByLabel(/Texto del elemento/)).toHaveCount(0);
  });
});

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

test("MVP-001: creates, reviews, approves, and exports an agenda", async ({
  page,
}) => {
  await page.route("**/backend/api/pictograms/search", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        query: "casa",
        locale: "es",
        candidates: [pictogram],
        requires_human_selection: true,
      }),
    });
  });
  await page.goto("/");

  await page
    .getByLabel("Título genérico, sin nombres personales")
    .fill("Rutina de entrada");
  await page
    .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
    .fill("casa");
  await page.getByRole("button", { name: "Buscar" }).click();
  await page.getByRole("button", { name: "Seleccionar casa" }).click();
  await page.getByLabel("Texto del elemento 1").fill("Llegar");
  await page.getByRole("button", { name: "Crear borrador" }).click();
  await expect(page.getByText("draft", { exact: true })).toBeVisible();

  await expect(page.getByRole("button", { name: "Exportar HTML" })).toBeDisabled();
  await page.getByRole("button", { name: "Enviar a revisión" }).click();
  await expect(page.getByText("in_review", { exact: true })).toBeVisible();
  await page
    .getByRole("button", { name: "Aprobar tras revisión humana" })
    .click();
  await expect(page.getByText("approved", { exact: true })).toBeVisible();

  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("button", { name: "Exportar HTML" }).click();
  const download = await downloadPromise;
  expect(download.suggestedFilename()).toMatch(/\.html$/);
});

test("MVP-002: board requires two human-selected cells", async ({ page }) => {
  await page.route("**/backend/api/pictograms/search", async (route) => {
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        candidates: [pictogram],
        requires_human_selection: true,
      }),
    });
  });
  await page.goto("/");
  await page.getByLabel("Tablero de comunicación").check();
  await page.getByRole("button", { name: "Crear borrador" }).click();
  await expect(page.getByRole("status")).toContainText("dos celdas");
});

test("AI-001: AI proposes text and a human selects the real pictogram", async ({
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
    const payload = route.request().postDataJSON();
    expect(payload.no_personal_data_confirmed).toBe(true);
    await route.fulfill({
      contentType: "application/json",
      body: JSON.stringify({
        summary: "Visita genérica a la biblioteca",
        items: [
          {
            text: "Entrar",
            search_term: "entrada",
            candidates: [pictogram],
          },
        ],
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
  await page.getByLabel("Número de conceptos").fill("1");
  await page.getByRole("button", { name: "Generar propuesta textual" }).click();

  await expect(
    page
      .getByRole("region", { name: "Propuesta de IA" })
      .locator("p")
      .filter({ hasText: "Visita genérica a la biblioteca" })
      .first(),
  ).toContainText("Visita genérica a la biblioteca");
  await expect(page.getByLabel(/Texto del elemento/)).toHaveCount(0);
  await page.getByRole("button", { name: "Elegir casa para Entrar" }).click();
  await expect(page.getByLabel("Texto del elemento 1")).toHaveValue("Entrar");
  await expect(page.getByText(/resultados reales ARASAAC/)).toBeVisible();
});

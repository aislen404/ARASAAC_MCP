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
  await page.getByLabel("Buscar pictogramas reales ARASAAC").fill("casa");
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

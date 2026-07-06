import { expect, test } from "@playwright/test";

const pictogramA = {
  pictogram_id: 6964,
  label: "casa",
  source_url: "https://static.arasaac.org/pictograms/6964/6964_300.png",
  origin: "ARASAAC",
  author: "Sergio Palao",
  owner: "Gobierno de Aragón",
  license: "CC BY-NC-SA",
  retrieved_at: "2026-07-04T00:00:00Z",
};

const pictogramB = {
  ...pictogramA,
  pictogram_id: 2280,
  label: "adiós",
  source_url: "https://static.arasaac.org/pictograms/2280/2280_300.png",
};

test.describe("Tipos de material sin cobertura previa (lectura fácil, historia, señalética)", () => {
  test.beforeEach(async ({ page }) => {
    let call = 0;
    await page.route("**/backend/api/pictograms/search", async (route) => {
      call += 1;
      const candidate = call === 1 ? pictogramA : pictogramB;
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({ candidates: [candidate], requires_human_selection: true }),
      });
    });
  });

  test("lectura fácil (documento): un elemento es suficiente", async ({ page }) => {
    await page.goto("/");
    await page.getByLabel("Lectura fácil").check();
    await page
      .getByLabel("Título genérico, sin nombres personales")
      .fill("Guía de lectura fácil");
    await page
      .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
      .fill("casa");
    await page.getByRole("button", { name: "Buscar" }).click();
    await page.getByRole("button", { name: "Seleccionar casa" }).click();
    await page.getByLabel("Texto del elemento 1").fill("Primer paso");
    await page.getByRole("button", { name: "Crear borrador" }).click();
    await expect(page.getByText("draft", { exact: true })).toBeVisible();
  });

  test("historia social: un elemento es suficiente y numera las escenas", async ({
    page,
  }) => {
    await page.goto("/");
    await page.getByLabel("Historia social").check();
    await page
      .getByLabel("Título genérico, sin nombres personales")
      .fill("Historia social genérica");
    await page
      .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
      .fill("casa");
    await page.getByRole("button", { name: "Buscar" }).click();
    await page.getByRole("button", { name: "Seleccionar casa" }).click();
    await page.getByLabel("Texto del elemento 1").fill("Escena inicial");
    await page.getByRole("button", { name: "Crear borrador" }).click();
    await expect(page.getByText("draft", { exact: true })).toBeVisible();
  });

  test("señalética: exige al menos dos elementos", async ({ page }) => {
    await page.goto("/");
    await page.getByLabel("Señalética").check();
    await page
      .getByLabel("Título genérico, sin nombres personales")
      .fill("Señalética de sala");
    await page
      .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
      .fill("casa");
    await page.getByRole("button", { name: "Buscar" }).click();
    await page.getByRole("button", { name: "Seleccionar casa" }).click();
    await page.getByLabel("Texto del elemento 1").fill("Entrada");
    await page.getByRole("button", { name: "Crear borrador" }).click();
    await expect(page.getByRole("status")).toContainText("dos celdas");

    await page
      .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
      .fill("adiós");
    await page.getByRole("button", { name: "Buscar" }).click();
    await page.getByRole("button", { name: "Seleccionar adiós" }).click();
    await page.getByLabel("Texto del elemento 2").fill("Salida");
    await page.getByRole("button", { name: "Crear borrador" }).click();
    await expect(page.getByText("draft", { exact: true })).toBeVisible();
  });
});

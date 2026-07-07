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

test.describe("WEB-004 extendido: flujo completo operable solo con teclado", () => {
  test("crear, enviar y aprobar una agenda sin usar el ratón", async ({ page }) => {
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

    const title = page.getByLabel("Título genérico, sin nombres personales");
    await title.focus();
    await page.keyboard.type("Rutina accesible por teclado");
    await expect(title).toHaveValue("Rutina accesible por teclado");

    const search = page.getByLabel("Buscar pictogramas reales ARASAAC manualmente");
    await search.focus();
    await page.keyboard.type("casa");
    await page.getByRole("button", { name: "Buscar" }).focus();
    await page.keyboard.press("Enter");

    const selectButton = page.getByRole("button", { name: "Seleccionar casa" });
    await expect(selectButton).toBeVisible();
    await selectButton.focus();
    await expect(selectButton).toBeFocused();
    await page.keyboard.press("Enter");

    const itemText = page.getByLabel("Texto del elemento 1");
    await itemText.focus();
    await page.keyboard.type("Llegar a casa");

    const createButton = page.getByRole("button", { name: "Crear borrador" });
    await createButton.focus();
    await expect(createButton).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page.getByText("Borrador", { exact: true })).toBeVisible();

    const submitButton = page.getByRole("button", { name: "Enviar a revisión" });
    await submitButton.focus();
    await page.keyboard.press("Enter");
    await expect(page.getByText("En revisión", { exact: true })).toBeVisible();

    const approveButton = page.getByRole("button", {
      name: "Aprobar tras revisión humana",
    });
    await approveButton.focus();
    await expect(approveButton).toBeFocused();
    await page.keyboard.press("Enter");
    await expect(page.getByText("Aprobado", { exact: true })).toBeVisible();

    const exportButton = page.getByRole("button", { name: "Exportar HTML" });
    await exportButton.focus();
    await expect(exportButton).toBeFocused();
    await expect(exportButton).toBeEnabled();
  });

  test("el toggle de tema es operable con Enter y con Espacio", async ({ page }) => {
    await page.goto("/");
    const toggle = page.getByRole("button", { name: "Usar tema oscuro" });
    await toggle.focus();
    await page.keyboard.press("Enter");
    await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");

    const lightToggle = page.getByRole("button", { name: "Usar tema claro" });
    await lightToggle.focus();
    await page.keyboard.press(" ");
    await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  });
});

test.describe("WEB-006 extendido: la tarea se completa, no solo se ve, en tablet", () => {
  test("busca, selecciona y crea un borrador a 768px de ancho", async ({ page }) => {
    await page.route("**/backend/api/pictograms/search", async (route) => {
      await route.fulfill({
        contentType: "application/json",
        body: JSON.stringify({
          candidates: [pictogram],
          requires_human_selection: true,
        }),
      });
    });
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto("/");

    await page
      .getByLabel("Título genérico, sin nombres personales")
      .fill("Rutina en tablet");
    await page
      .getByLabel("Buscar pictogramas reales ARASAAC manualmente")
      .fill("casa");
    const searchField = page.getByLabel("Buscar pictogramas reales ARASAAC manualmente");
    await searchField.press("Enter");
    await page.getByRole("button", { name: "Seleccionar casa" }).click();
    await page.getByLabel("Texto del elemento 1").fill("Llegar");
    await page.getByRole("button", { name: "Crear borrador" }).click();
    await expect(page.getByText("Borrador", { exact: true })).toBeVisible();

    const dimensions = await page.evaluate(() => ({
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
    }));
    expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth);
  });
});

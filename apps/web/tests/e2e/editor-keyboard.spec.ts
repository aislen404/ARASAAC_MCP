import { expect, test } from "@playwright/test";

test("WEB-010: editor reorder buttons are keyboard reachable", async ({ page }) => {
  await page.goto("/");

  await page.getByLabel("Título genérico, sin nombres personales").fill("Rutina genérica");
  await page.getByLabel("Buscar pictogramas reales ARASAAC manualmente").fill("casa");
  await page.getByRole("button", { name: "Buscar" }).click();

  const selectButtons = page.getByRole("button", { name: /^Seleccionar / });
  await expect(selectButtons.first()).toBeVisible({ timeout: 120_000 });
  await selectButtons.first().click();
  await selectButtons.nth(1).click();

  const moveDown = page.getByRole("button", { name: "Bajar" }).first();
  await moveDown.focus();
  await expect(moveDown).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByLabel("Texto del elemento 1")).toBeVisible();
});

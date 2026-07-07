import { expect, test } from "@playwright/test";

test.describe("Convergencia Serena honest state", () => {
  test("shows zero progress and honest continue state on load", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByText("0%")).toBeVisible();
    await expect(page.getByText("0 completados · 1 en curso · 4 pendientes")).toBeVisible();
    await expect(page.getByText("Sin borrador activo")).toBeVisible();
  });

  test("ver todas link targets suggestions section not builder", async ({ page }) => {
    await page.goto("/");
    const verTodas = page.getByRole("link", { name: "Ver todas →" });
    await expect(verTodas).toHaveAttribute("href", "#cs-suggestions");
  });

  test("continue button scrolls to builder area", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("button", { name: /Ir al área de trabajo/i }).click();
    await expect(page.locator("#cs-builder")).toBeInViewport();
  });
});

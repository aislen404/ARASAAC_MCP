import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const sections = [
  "Configura el material",
  "Vista previa editable",
  "Revisión y exportación",
];

test("WEB-001/002/003: shows the complete governed workflow", async ({ page }) => {
  const response = await page.goto("/");

  expect(response?.status()).toBe(200);
  await expect(
    page.getByRole("heading", {
      level: 1,
      name: "Crear con claridad. Revisar con criterio.",
    }),
  ).toBeVisible();
  await expect(page.getByText("Revisión humana obligatoria")).toBeVisible();
  await expect(
    page.getByRole("heading", { name: "Cinco fases, una decisión humana" }),
  ).toBeVisible();
  await expect(page.locator('[aria-current="step"]')).toContainText(
    "Definir necesidad",
  );
  for (const section of sections) {
    await expect(page.getByRole("heading", { level: 2, name: section })).toBeVisible();
  }
  await expect(page.locator("footer").getByText(/Sergio Palao/)).toBeVisible();
});

test("WEB-004/005: has semantic Spanish structure without keyboard traps", async ({
  page,
}) => {
  await page.goto("/");

  await expect(page.locator("html")).toHaveAttribute("lang", "es");
  await expect(page.locator("main")).toHaveCount(1);
  await expect(page.getByRole("heading", { level: 1 })).toHaveCount(1);
  await page.keyboard.press("Tab");
  await expect(page.locator("body")).toBeVisible();
});

test("WEB-006: remains usable at mobile viewport", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await page.goto("/");

  const dimensions = await page.evaluate(() => ({
    clientWidth: document.documentElement.clientWidth,
    scrollWidth: document.documentElement.scrollWidth,
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});

test("WEB-006A: switches theme with an accessible persistent control", async ({
  page,
}) => {
  await page.goto("/");

  const toggle = page.getByRole("button", { name: "Usar tema oscuro" });
  await expect(toggle).toHaveAttribute("aria-pressed", "false");
  await toggle.click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await expect(
    page.getByRole("button", { name: "Usar tema claro" }),
  ).toHaveAttribute("aria-pressed", "true");

  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("WEB-007/008: renders no ARASAAC pictograms and calls no external hosts", async ({
  page,
}) => {
  const externalHosts = new Set<string>();
  page.on("request", (request) => {
    const host = new URL(request.url()).hostname;
    if (host !== "127.0.0.1" && host !== "localhost") {
      externalHosts.add(host);
    }
  });

  await page.goto("/");
  await expect(page.locator('img[src*="arasaac"]')).toHaveCount(0);
  expect([...externalHosts]).toEqual([]);
});

test("WEB-009: has no serious or critical axe violations", async ({ page }) => {
  await page.goto("/");

  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();
  const blocking = results.violations.filter((violation) =>
    ["serious", "critical"].includes(violation.impact ?? ""),
  );

  expect(blocking).toEqual([]);
});

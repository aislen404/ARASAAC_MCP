import { expect, test } from "@playwright/test";

const limits = [
  "Sin integración ni consultas a ARASAAC",
  "Sin generación o exportación de materiales",
  "Sin autenticación ni datos personales",
  "Servidor MCP deshabilitado y sin tools",
];

test("WEB-001/002/003: shows MVP-0 status and approved limits", async ({ page }) => {
  const response = await page.goto("/");

  expect(response?.status()).toBe(200);
  await expect(
    page.getByRole("heading", { level: 1, name: "ARASAAC Social MCP Platform" }),
  ).toBeVisible();
  await expect(page.getByText("Base técnica disponible")).toBeVisible();
  for (const limit of limits) {
    await expect(page.getByRole("listitem").filter({ hasText: limit })).toBeVisible();
  }
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

test("WEB-007/008: renders no pictograms and calls no external hosts", async ({
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
  await expect(page.locator("img, svg, canvas")).toHaveCount(0);
  expect([...externalHosts]).toEqual([]);
});

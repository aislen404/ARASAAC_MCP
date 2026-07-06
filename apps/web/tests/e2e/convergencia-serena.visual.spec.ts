import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const shellSelectors = [
  '[data-cs="app"]',
  '[data-cs="header"]',
  '[data-cs="side-rail"]',
  '[data-cs="guided-workspace"]',
  '[data-cs="workflow-stepper"]',
  '[data-cs="metric-row"]',
  '[data-cs="continue-card"]',
  '[data-cs="context-help"]',
  '[data-cs="bottom-strip"]',
];

async function assertShellZones(page: import("@playwright/test").Page) {
  for (const selector of shellSelectors) {
    await expect(page.locator(selector)).toBeVisible();
  }
}

test.describe("Convergencia Serena visual shell", () => {
  test("desktop light structure", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/");
    await assertShellZones(page);
    await expect(page).toHaveScreenshot("home-light-desktop.png", { fullPage: true });
  });

  test("desktop dark structure", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/");
    await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
    await assertShellZones(page);
    await expect(page).toHaveScreenshot("home-dark-desktop.png", { fullPage: true });
  });

  test("tablet light structure", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto("/");
    await assertShellZones(page);
    await expect(page).toHaveScreenshot("home-light-tablet.png", { fullPage: true });
  });

  test("tablet dark structure", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto("/");
    await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
    await assertShellZones(page);
    await expect(page).toHaveScreenshot("home-dark-tablet.png", { fullPage: true });
  });

  test("mobile light structure", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/");
    await assertShellZones(page);
    await expect(page).toHaveScreenshot("home-light-mobile.png", { fullPage: true });
  });

  test("mobile dark structure", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/");
    await page.evaluate(() => document.documentElement.setAttribute("data-theme", "dark"));
    await assertShellZones(page);
    await expect(page).toHaveScreenshot("home-dark-mobile.png", { fullPage: true });
  });

  test("mobile has no horizontal overflow", async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto("/");
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth > window.innerWidth,
    );
    expect(overflow).toBe(false);
  });

  test("has no serious or critical axe violations", async ({ page }) => {
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto("/");

    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
      .analyze();
    const blocking = results.violations.filter((violation) =>
      ["serious", "critical"].includes(violation.impact ?? ""),
    );

    expect(blocking).toEqual([]);
  });
});

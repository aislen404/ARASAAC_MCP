import { expect, test } from "@playwright/test";

const assets = [
  "/convergencia-serena/brand/monogram.svg",
  "/convergencia-serena/icons/search.svg",
  "/convergencia-serena/icons/shield.svg",
  "/convergencia-serena/illustrations/helper-light.svg",
  "/convergencia-serena/patterns/botanical-corner.svg",
];

test("required Convergencia Serena assets are served", async ({ request }) => {
  for (const asset of assets) {
    const response = await request.get(asset);
    expect(response.ok(), asset).toBeTruthy();
    expect(response.headers()["content-type"] ?? "").toContain("svg");
  }
});

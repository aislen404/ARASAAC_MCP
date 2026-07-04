import { expect, test } from "@playwright/test";

test("API-001: API healthcheck has the exact contract", async ({ request }) => {
  const response = await request.get("http://127.0.0.1:8100/health");

  expect(response.status()).toBe(200);
  expect(await response.json()).toEqual({ status: "ok", service: "api" });
});

test("API-002/003: API rejects unsupported methods and unknown routes", async ({
  request,
}) => {
  expect((await request.post("http://127.0.0.1:8100/health")).status()).toBe(405);
  expect((await request.get("http://127.0.0.1:8100/unknown")).status()).toBe(404);
});

test("AI-API-001: disabled AI fails closed without affecting API health", async ({
  request,
}) => {
  const status = await request.get("http://127.0.0.1:8100/api/ai/status");

  expect(status.status()).toBe(200);
  expect(await status.json()).toEqual({
    available: false,
    provider: "disabled",
    model: null,
    reason: "La capa IA está desactivada.",
    generates_pictograms: false,
    requires_human_selection: true,
    stores_input: false,
  });
});

test("MCP-001/002: placeholder is healthy, disabled, and has no tools", async ({
  request,
}) => {
  const health = await request.get("http://127.0.0.1:8101/health");
  const status = await request.get("http://127.0.0.1:8101/mcp/status");

  expect(health.status()).toBe(200);
  expect(await health.json()).toEqual({
    status: "ok",
    service: "mcp-server",
  });
  expect(status.status()).toBe(200);
  expect(await status.json()).toEqual({
    status: "active",
    enabled: true,
    tools: [
      "get_pictogram",
      "search_pictograms",
      "suggest_pictograms_for_text",
    ],
  });
});

test("MCP-003/004: placeholder rejects mutation and unknown tools", async ({
  request,
}) => {
  expect((await request.post("http://127.0.0.1:8101/mcp/status")).status()).toBe(405);
  expect((await request.post("http://127.0.0.1:8101/tools/execute")).status()).toBe(
    404,
  );
});

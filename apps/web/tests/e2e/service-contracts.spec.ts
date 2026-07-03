import { expect, test } from "@playwright/test";

test("API-001: API healthcheck has the exact contract", async ({ request }) => {
  const response = await request.get("http://127.0.0.1:8000/health");

  expect(response.status()).toBe(200);
  expect(await response.json()).toEqual({ status: "ok", service: "api" });
});

test("API-002/003: API rejects unsupported methods and unknown routes", async ({
  request,
}) => {
  expect((await request.post("http://127.0.0.1:8000/health")).status()).toBe(405);
  expect((await request.get("http://127.0.0.1:8000/unknown")).status()).toBe(404);
});

test("MCP-001/002: placeholder is healthy, disabled, and has no tools", async ({
  request,
}) => {
  const health = await request.get("http://127.0.0.1:8001/health");
  const status = await request.get("http://127.0.0.1:8001/mcp/status");

  expect(health.status()).toBe(200);
  expect(await health.json()).toEqual({
    status: "ok",
    service: "mcp-placeholder",
  });
  expect(status.status()).toBe(200);
  expect(await status.json()).toEqual({
    status: "placeholder",
    enabled: false,
    tools: [],
  });
});

test("MCP-003/004: placeholder rejects mutation and unknown tools", async ({
  request,
}) => {
  expect((await request.post("http://127.0.0.1:8001/mcp/status")).status()).toBe(405);
  expect((await request.post("http://127.0.0.1:8001/tools/execute")).status()).toBe(
    404,
  );
});

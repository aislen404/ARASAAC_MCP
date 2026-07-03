import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

test("status page states the MVP-0 limits", async () => {
  const page = await readFile(new URL("../src/app/page.tsx", import.meta.url), "utf8");

  assert.match(page, /Project foundation/);
  assert.match(page, /Sin integración ni consultas a ARASAAC/);
  assert.match(page, /Servidor MCP deshabilitado y sin tools/);
});

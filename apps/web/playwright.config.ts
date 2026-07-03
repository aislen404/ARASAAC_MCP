import { defineConfig, devices } from "@playwright/test";
import path from "node:path";

const repositoryRoot = path.resolve(process.cwd(), "../..");

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: true,
  retries: 1,
  workers: 4,
  reporter: [["line"], ["html", { open: "never" }]],
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "retain-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: [
    {
      command:
        ".venv/bin/uvicorn arasaac_platform.main:app --app-dir services/api/src --host 127.0.0.1 --port 8000",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command:
        ".venv/bin/uvicorn safe_mcp.main:app --app-dir services/mcp/src --host 127.0.0.1 --port 8001",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:8001/health",
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command:
        "npm --prefix apps/web run build:clean && npm --prefix apps/web run start -- --hostname 127.0.0.1",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:3000",
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],
});

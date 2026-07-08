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
    baseURL: "http://127.0.0.1:3100",
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
        ".venv/bin/uvicorn arasaac_platform.main:app --app-dir services/api/src --host 127.0.0.1 --port 8100",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:8100/health",
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command:
        ".venv/bin/uvicorn safe_mcp.main:app --app-dir services/mcp/src --host 127.0.0.1 --port 8101",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:8101/health",
      reuseExistingServer: false,
      timeout: 120_000,
    },
    {
      command:
        "API_INTERNAL_URL=http://127.0.0.1:8100 npm --prefix apps/web run build:clean && API_INTERNAL_URL=http://127.0.0.1:8100 npm --prefix apps/web run start -- --hostname 127.0.0.1 --port 3100",
      cwd: repositoryRoot,
      url: "http://127.0.0.1:3100",
      reuseExistingServer: false,
      timeout: 300_000,
    },
  ],
});

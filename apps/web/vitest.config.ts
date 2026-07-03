import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    include: ["tests/unit/**/*.test.tsx"],
    coverage: {
      provider: "v8",
      include: ["src/app/**/*.{ts,tsx}"],
      reporter: ["text", "json-summary"],
      reportsDirectory: "../../coverage/frontend",
      thresholds: {
        branches: 75,
        functions: 75,
        lines: 75,
        statements: 75,
      },
    },
  },
});

import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["tests/unit/**/*.test.tsx"],
    coverage: {
      provider: "v8",
      include: ["src/app/**/*.{ts,tsx}", "src/components/**/*.{ts,tsx}", "src/features/**/*.{ts,tsx}"],
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

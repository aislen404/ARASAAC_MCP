# Design — 0019-testing-quality-gates

GitHub Actions instala Python/Node/Chromium y ejecuta OpenSpec, cobertura ≥75%,
lint, tipos, build y Playwright. La integración live ARASAAC permanece opt-in para
no convertir disponibilidad externa en flakiness del CI.

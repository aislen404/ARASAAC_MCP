# Plan Playwright visual

## Capturas obligatorias

- `home-light-desktop.png` — 1440×1000.
- `home-dark-desktop.png` — 1440×1000.
- `home-light-tablet.png` — 768×1024.
- `home-dark-tablet.png` — 768×1024.
- `home-light-mobile.png` — 390×844.
- `home-dark-mobile.png` — 390×844.

## Selectores obligatorios

```text
[data-cs="app"]
[data-cs="header"]
[data-cs="side-rail"]
[data-cs="guided-workspace"]
[data-cs="workflow-stepper"]
[data-cs="metric-row"]
[data-cs="continue-card"]
[data-cs="context-help"]
[data-cs="bottom-strip"]
```

## Tolerancias

- Screenshot diff ≤ 0.08 para cambios menores.
- Cero `serious` o `critical` en axe.
- `document.documentElement.scrollWidth <= window.innerWidth` en móvil.

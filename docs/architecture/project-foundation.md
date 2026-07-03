# Project foundation

MVP-0 separa tres procesos sin estado: web, API y placeholder MCP. No comparten
base de datos ni contratos de dominio porque esta unidad solo valida el arranque.

El placeholder MCP no es todavía un servidor MCP funcional. Su único propósito es
reservar el límite de servicio y hacer explícita una allowlist vacía. Cualquier
tool futura requiere su propia OpenSpec, schema estricto, tests y revisión.

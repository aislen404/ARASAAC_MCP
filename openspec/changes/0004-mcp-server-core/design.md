# Design — 0004-mcp-server-core

Se usa `mcp>=1.27,<2`, rama estable del SDK oficial. FastMCP genera input/output
schemas desde modelos tipados. El registro de tools es estático y comprobado por
tests; no existe carga dinámica ni eval.

El proceso stdio escribe protocolo en stdout y logs en stderr. El endpoint HTTP
de estado permanece separado y solo informa de la allowlist.

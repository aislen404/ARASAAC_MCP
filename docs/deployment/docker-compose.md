# Despliegue local con Docker Compose

## Inicio y parada

```bash
make start
make stop
```

Servicios: PostgreSQL 17, API, MCP status y Web App. El volumen
`postgres_data` conserva materiales y auditoría tras `make stop`.

La IA está desactivada por defecto. Para activarla, crea `.env` desde
`.env.example` y configura Azure Foundry (`AI_PROVIDER=azure`,
`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY`) u OpenAI directo
(`AI_PROVIDER=openai`, `OPENAI_API_KEY`). Vuelve a ejecutar `make start`. La clave
se inyecta en el contenedor API en runtime, no en la imagen ni en el navegador.

## Verificación

```bash
docker compose config --quiet
docker compose ps
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/api/ai/status
curl --fail http://localhost:8001/health
curl --fail http://localhost:3000
```

## Datos

`make reset-data` elimina deliberadamente el volumen local. Para una copia simple:

```bash
docker compose exec db pg_dump -U arasaac arasaac_mvp > arasaac_mvp.sql
```

El fichero resultante puede contener materiales operativos y no debe subirse al
repositorio.

No captures ni publiques la salida completa de `docker compose config` cuando
hay una clave real interpolada. Usa `docker compose config --quiet` para validar
la sintaxis sin imprimir configuración.

## Resolución de problemas

Si la construcción queda detenida en `load metadata for docker.io`, comprueba la
conectividad/autenticación de Docker Hub y repite `make start`. En la validación
del 2026-07-04, Docker Desktop arrancó correctamente pero Docker Hub no devolvió
los metadatos de las imágenes base; `docker compose config` y el contrato de
persistencia SQL sí se validaron.

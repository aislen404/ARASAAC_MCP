FROM python:3.12-slim

WORKDIR /app
COPY services/api ./services/api
COPY services/mcp ./services/mcp
RUN pip install --no-cache-dir ./services/api ./services/mcp

EXPOSE 8001
CMD ["uvicorn", "safe_mcp.main:app", "--host", "0.0.0.0", "--port", "8001"]

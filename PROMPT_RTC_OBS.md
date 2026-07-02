# Prompt 1 - Agregar metrica de observabilidad

Actua como especialista en observabilidad para una API FastAPI del Simulador Mundial 2026.

Objetivo:
- Exponer metricas Prometheus sin romper el endpoint existente `GET /metrics/dashboard`.
- Medir requests HTTP por metodo, path y status.
- Medir latencia HTTP, especialmente `POST /simulator/run`.
- Medir ejecuciones de simulacion por estado.
- Agregar un contador para incidentes sinteticos activados por variable de entorno.
- Dejar la app lista para Prometheus + Grafana con `docker compose up`.

Contexto tecnico:
- La API usa FastAPI, SQLAlchemy y SQLite.
- El endpoint funcional de dashboard vive bajo `/metrics/dashboard`.
- El endpoint de scraping debe usar otro path, por ejemplo `/prometheus`.

Criterios de aceptacion:
- `GET /prometheus` devuelve formato Prometheus.
- Prometheus scrapea la app.
- Grafana abre en `http://localhost:3000` con datasource y dashboard provisionados.
- La variable `SIMULATOR_INCIDENT_MODE=true` genera un pico visible de latencia/incidentes.

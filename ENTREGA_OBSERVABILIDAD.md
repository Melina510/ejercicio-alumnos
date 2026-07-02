# Entrega Observabilidad - Simulador Mundial 2026

## Resumen

Se instrumento el Simulador Mundial 2026 con metricas Prometheus y un dashboard Grafana provisionado por Docker Compose.

La stack incluye:

- API FastAPI en `http://localhost:8000`.
- Metricas Prometheus en `http://localhost:8000/prometheus`.
- Prometheus en `http://localhost:9090`.
- Grafana en `http://localhost:3000` con usuario `admin` y password `admin`.

## Como levantar

```bash
docker compose up --build
```

Luego abrir Grafana:

```text
http://localhost:3000
```

Dashboard:

```text
Mundial 2026 / Mundial 2026 Observability
```

## Metricas agregadas

- `worldcup_http_requests_total`: requests por metodo, path y status.
- `worldcup_http_request_duration_seconds`: latencia HTTP.
- `worldcup_simulation_runs_total`: simulaciones por estado.
- `worldcup_simulation_duration_seconds`: duracion de simulaciones.
- `worldcup_incidents_total`: incidentes sinteticos activados.

## Incidente plantado

El incidente se activa con:

```yaml
SIMULATOR_INCIDENT_MODE: "true"
```

Cuando queda activo, `POST /simulator/run` agrega una demora artificial de 3 segundos y aumenta:

```text
worldcup_incidents_total{type="slow_simulation"}
```

## Diagnostico

La causa raiz es una variable de entorno de incidente habilitada en el runtime:

```text
SIMULATOR_INCIDENT_MODE=true
```

Esto ejecuta una rama de codigo que incrementa el contador de incidentes y fuerza `time.sleep(3)` antes de simular.

## Fix aplicado

El `docker-compose.yml` queda corregido con:

```yaml
SIMULATOR_INCIDENT_MODE: "false"
```

## Verificacion realizada

Fecha de verificacion: 2026-07-02.

La stack se levanto correctamente con:

```bash
docker compose up --build -d
```

Contenedores verificados:

```text
worldcup-api        Up   0.0.0.0:8000->8000/tcp
worldcup-prometheus Up   0.0.0.0:9090->9090/tcp
worldcup-grafana    Up   0.0.0.0:3000->3000/tcp
```

Checks realizados:

- `GET http://localhost:8000/prometheus` devolvio `200 OK`.
- `POST http://localhost:8000/simulator/run` devolvio `200 OK`.
- `GET http://localhost:3000/api/health` devolvio `200 OK` con database `ok`.
- Prometheus consulto `up{job="worldcup-api"}` y devolvio valor `1`.
- Grafana mostro el folder `Mundial 2026` y el dashboard provisionado.

Tambien se agrego `.dockerignore` para evitar subir `.venv`, caches, reportes y base SQLite al contexto Docker. La build paso de enviar aproximadamente 306 MB a 6.7 KB de contexto.

## Pasos para demostrar en clase

1. Levantar la stack con `docker compose up --build`.
2. Abrir Grafana en `http://localhost:3000`.
3. Entrar con usuario `admin` y password `admin`.
4. Abrir el dashboard `Mundial 2026 / Mundial 2026 Observability`.
5. Ejecutar una simulacion:

```bash
curl -X POST http://localhost:8000/simulator/run
```

6. Verificar que:
   - `API up` esta en `1`.
   - `Simulation runs` aumenta en `success`.
   - `Incidents` no aumenta.
   - `p95 latency /simulator/run` vuelve a valores bajos.

## Archivos entregados

- `Dockerfile`: imagen de la API FastAPI.
- `docker-compose.yml`: levanta API, Prometheus y Grafana.
- `prometheus.yml`: configura el scraping de `/prometheus`.
- `grafana/provisioning/datasources/prometheus.yml`: datasource Prometheus.
- `grafana/provisioning/dashboards/worldcup.yml`: provisioning del dashboard.
- `grafana/dashboards/worldcup-observability.json`: dashboard de Grafana.
- `observability.py`: metricas Prometheus y middleware HTTP.
- `PROMPT_RTC_OBS.md`: prompt para agregar metricas.
- `PROMPT_RTC_OBS_INCIDENTE.md`: prompt para diagnosticar el incidente.

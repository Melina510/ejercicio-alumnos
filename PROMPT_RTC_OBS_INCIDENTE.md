# Prompt 2 - Diagnosticar incidente de observabilidad

Actua como SRE. Te paso los sintomas de Grafana, logs y stacktrace del Simulador Mundial 2026.

Sintomas:
- En Grafana sube `worldcup_incidents_total{type="slow_simulation"}`.
- El panel `p95 latency /simulator/run` salta aproximadamente a 3 segundos.
- La API sigue respondiendo, pero `POST /simulator/run` queda lenta.

Logs relevantes:

```text
SIMULATOR_INCIDENT_MODE=true
worldcup_incidents_total{type="slow_simulation"} aumenta
worldcup_simulation_duration_seconds_bucket muestra observaciones en buckets altos
```

Codigo sospechoso:

```python
if incident_mode_enabled():
    INCIDENTS.labels("slow_simulation").inc()
    time.sleep(3)
```

Pedido:
- Identifica la causa raiz.
- Propone el fix minimo.
- Indica como verificar que Grafana vuelve a verde.

Respuesta esperada:
- Causa raiz: la variable `SIMULATOR_INCIDENT_MODE` quedo activada y fuerza una demora artificial en cada simulacion.
- Fix: volver `SIMULATOR_INCIDENT_MODE=false` en `docker-compose.yml` o quitar la variable del entorno productivo.
- Verificacion: recrear la app, ejecutar simulaciones, confirmar que el contador de incidentes no aumenta y que p95 baja.

# SESION_INTERACTIVA - QA Clase 5

## Prompt RTC completado

```text
[ROL]
Sos un QA Engineer Senior especializado en testing de APIs FastAPI con pytest y TestClient.

Tenes cargado como contexto el archivo QA.md del Simulador Mundial 2026. Usalo como fuente de verdad para endpoints, reglas de negocio, quality gates, contratos de respuesta y herramientas permitidas.

[TAREA]
Trabaja en modo plan para disenar una estrategia de QA sobre este objetivo:

Quiero testear: POST /simulator/run.
Me preocupa: que el campeon no coincida con el ganador de la final.

Antes de generar codigo o modificar archivos:
1. Haceme las preguntas necesarias para cerrar alcance.
2. Revisa los tests existentes para evitar duplicar cobertura.
3. Proponeme un plan de prueba.
4. Espera mi aprobacion explicita.

No generes codigo todavia.
No modifiques archivos todavia.
No ejecutes comandos todavia.
No apliques el plan hasta que yo diga exactamente: "aplica el plan".
```

Nota: durante la conversacion aparecio `http://localhost:8000`, pero se corrigio el alcance: esa URL queda para el smoke frontend de Parte 3. Para Parte 1 y Parte 2 el objetivo formal es `POST /simulator/run`.

## Preguntas del agente y respuestas

| Pregunta | Respuesta |
|---|---|
| Queres validar solo esa regla critica, o tambien reglas cercanas como estructura de respuesta, total de partidos y eliminacion sin empates? | No. Solo la regla critica del campeon. |
| La DB de test deberia arrancar vacia para comprobar la autogeneracion de 32 equipos/jugadores? | Si. |
| Queres que los tests sean solo backend con pytest + TestClient, o tambien dejar previsto algo para frontend/Playwright sobre como se muestra el campeon? | Si, dejar previsto algo para frontend/Playwright. |

## Plan mostrado por el agente

Alcance confirmado:

- Backend: testear `POST /simulator/run`.
- Riesgo principal: `champion` debe coincidir con `final.winner`.
- DB de test: iniciar limpia usando la fixture `client`.
- Frontend: dejar previsto un chequeo manual/Playwright para `#championResult`.
- Reporteria: generar evidencia con Allure.

Casos propuestos:

| ID | Caso | Objetivo | Resultado esperado |
|---|---|---|---|
| SIM-CHAMP-001 | Champion coincide con ganador de final | Validar que el contrato principal de la simulacion sea consistente | `response["champion"] == response["final"]["winner"]` |
| SIM-CHAMP-002 | Simulacion desde DB vacia mantiene consistencia del campeon | Validar el riesgo con autogeneracion de datos | Status 200, `champion` no nulo y `champion == final.winner` |
| SIM-CHAMP-003 | Ganador de final pertenece a los finalistas | Evitar un ganador imposible en la final | `final.winner` pertenece a `{final.home_team, final.away_team}` |
| DASH-CHAMP-001 | Dashboard refleja el campeon de la simulacion | Validar consistencia entre simulacion y metricas | `dashboard.champion == simulation.champion == final.winner` |
| FE-CHAMP-001 | Campeon visible en UI | Dejar previsto smoke frontend | `#championResult` visible y no vacio |

Tests existentes revisados:

- `tests/test_simulator.py` ya cubre estructura de respuesta, conteos, grupos, eliminatoria, autogeneracion y varias reglas de negocio.
- Ya existe cobertura similar para `champion == final.winner`; no se duplica dentro del mismo archivo.
- Para cumplir la consigna, se crea `tests/test_qa_clase5.py` como archivo nuevo y focalizado.

Archivos a crear o modificar:

- Crear `tests/test_qa_clase5.py`.
- Completar `SESION_INTERACTIVA.md`.
- Crear `SMOKE_TEST_REPORT.md`.
- Crear `QA_REPORT.md`.
- Usar `allure-results/` y `allure-report.html` como evidencia generada.

Comandos de ejecucion:

```bash
pytest tests/test_qa_clase5.py -v --alluredir=allure-results
python generate_allure_report.py
```

Criterio GO / NO-GO:

- GO si `tests/test_qa_clase5.py` pasa completo y Allure genera evidencia.
- GO con observaciones si los tests backend pasan pero el smoke frontend queda pendiente de ejecucion manual.
- NO-GO si falla algun test critico relacionado con `champion`, `final.winner` o dashboard.

## Decision

Decision del alumno: `go` / aplica el plan.

## Codigo pytest generado

Archivo creado:

```text
tests/test_qa_clase5.py
```

Contenido principal:

```python
def test_qa_clase5_empty_db_champion_equals_final_winner(client):
    ...

def test_qa_clase5_final_winner_is_one_of_finalists(client):
    ...

def test_qa_clase5_dashboard_champion_matches_simulation(client):
    ...
```

Los tests usan `pytest`, `TestClient` y anotaciones Allure (`allure.epic`, `allure.feature`, `allure.story`, `allure.title`, `allure.severity`, `allure.step`).

## Evidencia Allure

Comando planificado y ejecutado:

```bash
pytest tests/test_qa_clase5.py tests/e2e -v --alluredir=allure-results --clean-alluredir
PYTHONIOENCODING=utf-8 python generate_allure_report.py
```

Resultado de pytest:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.0.3, pluggy-1.6.0
plugins: allure-pytest-2.16.0, anyio-4.13.0, base-url-2.1.0, cov-7.1.0, playwright-0.8.0
collecting ... collected 13 items

tests/test_qa_clase5.py::test_qa_clase5_empty_db_champion_equals_final_winner PASSED [  7%]
tests/test_qa_clase5.py::test_qa_clase5_final_winner_is_one_of_finalists PASSED [ 15%]
tests/test_qa_clase5.py::test_qa_clase5_dashboard_champion_matches_simulation PASSED [ 23%]
tests/e2e/test_api_integration.py::test_e2e_06_crud_teams_api PASSED [ 30%]
tests/e2e/test_api_integration.py::test_e2e_07_crud_players_api PASSED [ 38%]
tests/e2e/test_api_integration.py::test_e2e_08_reject_duplicate_team_code PASSED [ 46%]
tests/e2e/test_api_integration.py::test_e2e_09_reject_invalid_player_position PASSED [ 53%]
tests/e2e/test_api_integration.py::test_e2e_10_champion_equals_final_winner PASSED [ 61%]
tests/e2e/test_frontend_e2e.py::test_e2e_01_app_loads PASSED [ 69%]
tests/e2e/test_frontend_e2e.py::test_e2e_02_simulator_button_triggers_api PASSED [ 76%]
tests/e2e/test_frontend_e2e.py::test_e2e_03_champion_displays_correctly PASSED [ 84%]
tests/e2e/test_frontend_e2e.py::test_e2e_04_dashboard_displays_metrics PASSED [ 92%]
tests/e2e/test_frontend_e2e.py::test_e2e_05_bracket_structure_correct PASSED [100%]

======================== 13 passed, 1 warning in 4.71s ========================
```

Resultado de Allure:

```text
Reporte generado: allure-report.html
Pruebas Pasadas: 13
Pruebas Fallidas: 0
Total: 13
```

Evidencia esperada:

- `allure-results/`
- `allure-report.html`

Nota: en Windows se uso `PYTHONIOENCODING=utf-8` para evitar un error de encoding al imprimir iconos desde `generate_allure_report.py`.

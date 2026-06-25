# QA_REPORT - Simulador Mundial 2026

## Resumen

- Objetivo testeado: `POST /simulator/run`
- Riesgo principal: que `champion` no coincida con `final.winner`
- Herramientas: `pytest`, `TestClient`, `allure-pytest`
- Reporteria: `allure-results/` y `allure-report.html`

## Resultado de tests automatizados

| Suite | Archivo | Resultado |
|---|---|---|
| QA Clase 5 | `tests/test_qa_clase5.py` | 3 passed, 0 failed |
| E2E / API existente | `tests/e2e` | 10 passed, 0 failed |

Casos cubiertos:

| ID | Caso | Estado esperado |
|---|---|---|
| SIM-CHAMP-002 | DB vacia: champion coincide con final.winner | Verde |
| SIM-CHAMP-003 | final.winner pertenece a los finalistas | Verde |
| DASH-CHAMP-001 | Dashboard refleja el campeon de la simulacion | Verde |

## Resultado smoke frontend

Archivo: `SMOKE_TEST_REPORT.md`

Estado: GO con observaciones.

La suite automatizada `tests/e2e` valido carga del frontend por HTML, simulacion, dashboard, bracket y consistencia del campeon. Quedan como observaciones las validaciones estrictamente visuales/manuales: spinner, click real del boton y responsive mobile en navegador.

## Evidencia Allure

Comandos:

```bash
pytest tests/test_qa_clase5.py tests/e2e -v --alluredir=allure-results --clean-alluredir
PYTHONIOENCODING=utf-8 python generate_allure_report.py
```

Evidencia:

- `allure-results/`
- `allure-report.html`

## Riesgos residuales

- El backend queda cubierto para la regla critica del campeon.
- El frontend queda cubierto parcialmente por automatizacion con `TestClient`.
- La conclusion puede pasar a GO completo cuando spinner, click real y responsive mobile se validen manualmente en navegador.

## Analisis estatico y SonarQube

Fecha de ejecucion: 2026-06-18.

Comandos ejecutados:

```powershell
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest --cov=. --cov-report=xml
.\.venv\Scripts\pysonar.exe --sonar-host-url=http://localhost:9000 --sonar-project-key=simulador-mundial --sonar-project-name="Simulador Mundial" --sonar-python-coverage-report-paths=coverage.xml
```

Resultados:

| Herramienta | Resultado |
|---|---|
| Ruff | 15 hallazgos |
| Pytest + coverage | 82 passed, 0 failed |
| SonarQube | Analysis successful |
| Quality Gate actual | OK |
| Coverage SonarQube | 86.5% |
| Bugs | 0 |
| Vulnerabilities | 0 |
| Code smells | 24 |
| Duplicated lines density | 0.0% |
| NCLOC | 767 |

Dashboard SonarQube:

```text
http://localhost:9000/dashboard?id=simulador-mundial
```

Quality Gate recomendado para produccion:

| Metrica | Umbral |
|---|---|
| Bugs | 0 |
| Vulnerabilities | 0 |
| Coverage | >= 80% |
| Duplicated lines density | <= 3% |
| Code smells | <= 20 |
| Tests automatizados | 100% passing |

Nota: el token usado permite consultar SonarQube, pero no crear/asignar Quality Gates desde API (`actions.create=false`). Por eso el Quality Gate recomendado queda documentado como criterio de evaluacion.

### Priorizacion RTC de hallazgos

| Prioridad | Hallazgo | Riesgo | Accion propuesta |
|---|---|---|---|
| P1 | `services/simulator_service.py`: variable `y` sin uso en validacion de simulacion | Puede ocultar logica incompleta sobre jugadores requeridos | Eliminar la variable o reemplazarla por validacion explicita de jugadores si corresponde a la regla de negocio |
| P1 | SonarQube: 24 code smells vs umbral recomendado <= 20 | El proyecto queda con deuda tecnica superior al umbral productivo | Atacar primero smells vinculados a simulacion y servicios |
| P2 | Imports sin uso en servicios y tests | Ruido, menor mantenibilidad, posible confusion al revisar dependencias | Remover imports con `ruff check . --fix` y revisar los cambios |
| P2 | `schemas/team.py`: import a mitad del modulo (`E402`) | Orden de imports fragil; puede esconder dependencia circular | Reordenar schema o documentar/aislar el `model_rebuild()` si la dependencia circular es necesaria |
| P3 | f-strings sin placeholders | Estilo innecesario, sin impacto funcional | Quitar prefijo `f` |

Conclusion de produccion:

GO con observaciones. Los tests pasan y SonarQube no reporta bugs ni vulnerabilidades, con cobertura mayor al 80%. Antes de considerar GO pleno, conviene bajar code smells a <= 20 y limpiar Ruff.

## Conclusion

GO con observaciones.

Motivo: los tests automatizados planificados y la suite e2e existente quedaron en verde con evidencia Allure. La observacion es que todavia quedan validaciones visuales/manuales del frontend que requieren navegador real.

## Output pytest

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

## Output Allure

```text
Reporte generado: allure-report.html
Pruebas Pasadas: 13
Pruebas Fallidas: 0
Total: 13
```

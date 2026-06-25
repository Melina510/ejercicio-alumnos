import allure
from fastapi.testclient import TestClient


@allure.epic("QA Clase 5")
@allure.feature("Simulador Mundial 2026")
@allure.story("Champion debe coincidir con final.winner")
@allure.title("DB vacia: champion coincide con el ganador de la final")
@allure.severity(allure.severity_level.CRITICAL)
def test_qa_clase5_empty_db_champion_equals_final_winner(client: TestClient):
    with allure.step("Verificar que la DB de test inicia sin equipos"):
        teams_res = client.get("/teams/")
        assert teams_res.status_code == 200
        assert teams_res.json() == []

    with allure.step("Ejecutar POST /simulator/run"):
        sim_res = client.post("/simulator/run")
        assert sim_res.status_code == 200
        data = sim_res.json()

    with allure.step("Validar que champion coincide con final.winner"):
        assert data["champion"] is not None
        assert data["final"]["winner"] == data["champion"]


@allure.epic("QA Clase 5")
@allure.feature("Simulador Mundial 2026")
@allure.story("Final debe tener un ganador valido")
@allure.title("El ganador de la final pertenece a los finalistas")
@allure.severity(allure.severity_level.CRITICAL)
def test_qa_clase5_final_winner_is_one_of_finalists(client: TestClient):
    with allure.step("Ejecutar POST /simulator/run"):
        sim_res = client.post("/simulator/run")
        assert sim_res.status_code == 200
        data = sim_res.json()

    with allure.step("Validar que final.winner sea home_team o away_team"):
        final = data["final"]
        assert final["winner"] in {final["home_team"], final["away_team"]}


@allure.epic("QA Clase 5")
@allure.feature("Dashboard de metricas")
@allure.story("Dashboard refleja el campeon de la simulacion")
@allure.title("Dashboard champion coincide con simulation champion y final.winner")
@allure.severity(allure.severity_level.CRITICAL)
def test_qa_clase5_dashboard_champion_matches_simulation(client: TestClient):
    with allure.step("Ejecutar POST /simulator/run"):
        sim_res = client.post("/simulator/run")
        assert sim_res.status_code == 200
        sim_data = sim_res.json()

    with allure.step("Consultar GET /metrics/dashboard"):
        dashboard_res = client.get("/metrics/dashboard")
        assert dashboard_res.status_code == 200
        dashboard_data = dashboard_res.json()

    with allure.step("Validar consistencia de campeon entre simulacion, final y dashboard"):
        assert sim_data["champion"] == sim_data["final"]["winner"]
        assert dashboard_data["champion"] == sim_data["champion"]

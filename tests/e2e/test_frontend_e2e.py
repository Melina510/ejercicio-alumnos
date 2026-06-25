from fastapi.testclient import TestClient


# E2E-01: App carga sin errores
def test_e2e_01_app_loads(client: TestClient):
    """Verificar que el frontend se carga sin errores"""
    res = client.get("/")
    assert res.status_code == 200
    assert "DOCTYPE html" in res.text or "html" in res.text


# E2E-02: Botón simular dispara POST /simulator/run
def test_e2e_02_simulator_button_triggers_api(client: TestClient, prepopulated_db):
    """Verificar que simulación se ejecuta correctamente"""
    client, _ = prepopulated_db
    
    res = client.post("/simulator/run")
    assert res.status_code == 200
    
    data = res.json()
    assert "champion" in data
    assert "final" in data
    assert "groups" in data


# E2E-03: Campeón se muestra correctamente en DOM
def test_e2e_03_champion_displays_correctly(client: TestClient, prepopulated_db):
    """Verificar que campeón se renderiza y es consistente"""
    client, _ = prepopulated_db
    
    # Ejecutar simulación
    sim_res = client.post("/simulator/run")
    sim_data = sim_res.json()
    champion_name = sim_data["champion"]
    
    # Obtener métricas del dashboard
    dash_res = client.get("/metrics/dashboard")
    assert dash_res.status_code == 200
    
    dash_data = dash_res.json()
    assert dash_data["champion"] == champion_name
    
    # Verificar que campeón coincide con ganador de final
    assert champion_name == sim_data["final"]["winner"]


# E2E-04: Dashboard muestra métricas
def test_e2e_04_dashboard_displays_metrics(client: TestClient, prepopulated_db):
    """Verificar que dashboard se renderiza con datos correctos"""
    client, _ = prepopulated_db
    
    # Ejecutar simulación
    client.post("/simulator/run")
    
    # Obtener dashboard
    res = client.get("/metrics/dashboard")
    assert res.status_code == 200
    
    data = res.json()
    assert "champion" in data
    assert "top_scorer" in data
    assert "avg_goals_per_match" in data
    assert "total_goals" in data
    assert "total_matches" in data
    
    # Validar estructura de top_scorer
    ts = data["top_scorer"]
    assert "player_name" in ts
    assert "team_name" in ts
    assert "goals" in ts
    
    # Validar conteos
    assert data["total_matches"] == 64  # 48 grupos + 16 eliminatoria (8+4+2+1+1)
    assert isinstance(data["avg_goals_per_match"], (int, float))
    assert data["total_goals"] > 0


# E2E-05: Bracket muestra resultados correctamente
def test_e2e_05_bracket_structure_correct(client: TestClient, prepopulated_db):
    """Verificar que bracket eliminatorio tiene estructura correcta"""
    client, _ = prepopulated_db
    
    res = client.post("/simulator/run")
    assert res.status_code == 200
    
    data = res.json()
    
    # Validar estructura eliminatoria
    assert len(data["round_of_16"]) == 8  # 8 partidos
    assert len(data["quarterfinals"]) == 4  # 4 partidos
    assert len(data["semifinals"]) == 2  # 2 partidos
    assert "final" in data and data["final"] is not None  # 1 partido
    
    # Cada partido debe tener resultado
    for match in data["round_of_16"] + data["quarterfinals"] + data["semifinals"]:
        assert "home_team" in match
        assert "away_team" in match
        assert "home_goals" in match
        assert "away_goals" in match
        assert "winner" in match

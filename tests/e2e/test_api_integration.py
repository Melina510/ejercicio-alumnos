from fastapi.testclient import TestClient


# E2E-06: CRUD Equipos funciona vía API
def test_e2e_06_crud_teams_api(client: TestClient):
    """Crear equipo + verificar en lista"""
    # POST: Crear equipo
    res = client.post("/teams/", json={
        "name": "Test Team",
        "code": "TST"
    })
    assert res.status_code == 201
    team = res.json()
    assert team["name"] == "Test Team"
    assert team["code"] == "TST"
    
    # GET: Verificar en lista
    res = client.get("/teams/")
    assert res.status_code == 200
    teams = res.json()
    assert any(t["id"] == team["id"] for t in teams)


# E2E-07: CRUD Jugadores funciona vía API
def test_e2e_07_crud_players_api(client: TestClient):
    """Crear jugador + verificar en equipo"""
    # Crear equipo primero
    team_res = client.post("/teams/", json={
        "name": "Test Team",
        "code": "TST"
    })
    team = team_res.json()
    
    # POST: Crear jugador
    res = client.post("/players/", json={
        "name": "Test Player",
        "position": "FW",
        "team_id": team["id"]
    })
    assert res.status_code == 201
    player = res.json()
    assert player["name"] == "Test Player"
    assert player["position"] == "FW"
    
    # GET: Verificar en equipo
    res = client.get(f"/teams/{team['id']}")
    assert res.status_code == 200
    team_data = res.json()
    assert any(p["id"] == player["id"] for p in team_data.get("players", []))


# E2E-08: Rechazo - código equipo duplicado
def test_e2e_08_reject_duplicate_team_code(client: TestClient):
    """Validar 409 si se intenta crear código duplicado"""
    # Crear primer equipo
    res1 = client.post("/teams/", json={
        "name": "Team A",
        "code": "TAA"
    })
    assert res1.status_code == 201
    
    # Intentar crear segundo con mismo código
    res2 = client.post("/teams/", json={
        "name": "Team B",
        "code": "TAA"
    })
    assert res2.status_code == 409


# E2E-09: Rechazo - posición jugador inválida
def test_e2e_09_reject_invalid_player_position(client: TestClient):
    """Validar 400 si posición ∉ {GK, DF, MF, FW}"""
    # Crear equipo
    team_res = client.post("/teams/", json={
        "name": "Test Team",
        "code": "TST"
    })
    team = team_res.json()
    
    # Intentar crear jugador con posición inválida
    res = client.post("/players/", json={
        "name": "Test Player",
        "position": "XYZ",  # Posición inválida
        "team_id": team["id"]
    })
    assert res.status_code == 400


# E2E-10: Consistency - campeón = ganador final
def test_e2e_10_champion_equals_final_winner(client: TestClient, prepopulated_db):
    """Validar que champion == final.winner"""
    client, _ = prepopulated_db
    
    # Ejecutar simulación
    sim_res = client.post("/simulator/run")
    assert sim_res.status_code == 200
    
    sim_data = sim_res.json()
    champion = sim_data["champion"]
    final_winner = sim_data["final"]["winner"]
    
    # Validación crítica: campeón = ganador de final
    assert champion == final_winner, \
        f"Champion '{champion}' != Final Winner '{final_winner}'"
    
    # Verificar consistencia con dashboard
    dashboard_res = client.get("/metrics/dashboard")
    assert dashboard_res.status_code == 200
    
    dashboard_data = dashboard_res.json()
    assert dashboard_data["champion"] == champion

import pytest
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app
from fastapi.testclient import TestClient

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def base_url():
    """Base URL para los tests E2E"""
    return "http://localhost:8000"


@pytest.fixture()
def client():
    """TestClient con DB en memoria prepoblada"""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides.clear()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def prepopulated_db(client: TestClient):
    """Prepobla DB con 32 equipos + 3 jugadores cada uno"""
    teams = []
    groups = ["A", "B", "C", "D", "E", "F", "G", "H"]
    team_idx = 0
    
    for group in groups:
        for i in range(4):
            team_idx += 1
            team_name = f"Team {team_idx}"
            team_code = f"T{team_idx:02d}"
            
            # Crear equipo
            res = client.post("/teams/", json={"name": team_name, "code": team_code})
            assert res.status_code == 201
            team = res.json()
            teams.append(team)
            
            # Crear 3 jugadores
            positions = ["GK", "DF", "MF"]
            for j, pos in enumerate(positions):
                res = client.post("/players/", json={
                    "name": f"Player {j+1} of {team_name}",
                    "position": pos,
                    "team_id": team["id"],
                })
                assert res.status_code == 201
    
    return client, teams


@pytest.fixture()
def http_client():
    """Cliente HTTP para hacer requests directos (Playwright simulado)"""
    return httpx.AsyncClient(base_url="http://localhost:8000")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from observability import PrometheusMiddleware, metrics_response
from routers import users_router, teams_router, players_router, simulator_router, metrics_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mundial 2026 - Simulator API")
app.add_middleware(PrometheusMiddleware)

app.include_router(users_router)
app.include_router(teams_router)
app.include_router(players_router)
app.include_router(simulator_router)
app.include_router(metrics_router)


@app.get("/prometheus", include_in_schema=False)
def prometheus_metrics():
    return metrics_response()


app.mount("/", StaticFiles(directory="static", html=True), name="static")

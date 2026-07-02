import time

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from observability import INCIDENTS, SIMULATION_LATENCY, SIMULATION_RUNS, incident_mode_enabled
from services.simulator_service import SimulatorService
from schemas.simulator import SimulatorResponse

router = APIRouter(prefix="/simulator", tags=["Simulator"])


@router.post("/run", response_model=SimulatorResponse)
def run_simulation(db: Session = Depends(get_db)):
    start = time.perf_counter()
    service = SimulatorService(db)
    try:
        if incident_mode_enabled():
            INCIDENTS.labels("slow_simulation").inc()
            time.sleep(3)

        response = service.run()
        SIMULATION_RUNS.labels("success").inc()
        return response
    except Exception:
        SIMULATION_RUNS.labels("error").inc()
        raise
    finally:
        SIMULATION_LATENCY.observe(time.perf_counter() - start)

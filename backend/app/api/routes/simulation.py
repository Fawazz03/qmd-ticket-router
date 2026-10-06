import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.database import SessionLocal
from app.repositories.routing_state_repository import reset_routing_states
from app.repositories.ticket_repository import reset_simulation_tickets
from app.services.simulation_scheduler import run_simulation
from app.services.simulation_service import (
    configure_simulation,
    get_simulation_state,
    start_simulation,
    stop_simulation,
)


router = APIRouter(
    prefix="/api/simulation",
    tags=["simulation"],
)


class SimulationConfig(BaseModel):
    batch_size: int
    interval_seconds: int


@router.post("/configure")
def configure(
    config: SimulationConfig,
):
    try:
        state = configure_simulation(
            batch_size=config.batch_size,
            interval_seconds=config.interval_seconds,
        )

        return {
            "batch_size": state.batch_size,
            "interval_seconds": state.interval_seconds,
            "running": state.running,
        }

    except ValueError as error:
        return {
            "error": str(error),
        }


@router.post("/start")
async def start():
    state = start_simulation()

    asyncio.create_task(
        run_simulation()
    )

    return {
        "batch_size": state.batch_size,
        "interval_seconds": state.interval_seconds,
        "running": state.running,
    }


@router.post("/stop")
def stop():
    state = stop_simulation()

    return {
        "batch_size": state.batch_size,
        "interval_seconds": state.interval_seconds,
        "running": state.running,
    }


@router.post("/reset")
def reset():
    stop_simulation()

    db = SessionLocal()

    try:
        reset_ticket_count = reset_simulation_tickets(db)
        reset_routing_state_count = reset_routing_states(db)

        return {
            "message": "Simulation reset successfully.",
            "tickets_reset": reset_ticket_count,
            "routing_states_reset": reset_routing_state_count,
            "running": False,
        }

    finally:
        db.close()


@router.get("")
def get_state():
    state = get_simulation_state()

    return {
        "batch_size": state.batch_size,
        "interval_seconds": state.interval_seconds,
        "running": state.running,
    }
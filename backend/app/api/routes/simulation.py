import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

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


@router.get("")
def get_state():
    state = get_simulation_state()

    return {
        "batch_size": state.batch_size,
        "interval_seconds": state.interval_seconds,
        "running": state.running,
    }
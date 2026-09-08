from dataclasses import dataclass


@dataclass
class SimulationState:
    batch_size: int = 1
    interval_seconds: int = 5
    running: bool = False


simulation_state = SimulationState()


def configure_simulation(
    batch_size: int,
    interval_seconds: int,
) -> SimulationState:
    if batch_size < 1:
        raise ValueError("Batch size must be at least 1.")

    if interval_seconds < 1:
        raise ValueError("Interval must be at least 1 second.")

    simulation_state.batch_size = batch_size
    simulation_state.interval_seconds = interval_seconds

    return simulation_state


def start_simulation() -> SimulationState:
    simulation_state.running = True
    return simulation_state


def stop_simulation() -> SimulationState:
    simulation_state.running = False
    return simulation_state


def get_simulation_state() -> SimulationState:
    return simulation_state
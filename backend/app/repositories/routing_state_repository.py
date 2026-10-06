from sqlalchemy.orm import Session

from app.models.routing_state import RoutingState


def get_routing_state(
    db: Session,
    queue: str,
    pool: str,
) -> RoutingState | None:
    return (
        db.query(RoutingState)
        .filter(
            RoutingState.queue == queue,
            RoutingState.pool == pool,
        )
        .first()
    )


def get_or_create_routing_state(
    db: Session,
    queue: str,
    pool: str,
) -> RoutingState:
    state = get_routing_state(
        db,
        queue,
        pool,
    )

    if state:
        return state

    state = RoutingState(
        queue=queue,
        pool=pool,
        last_assigned_employee_id=None,
    )

    db.add(state)
    db.commit()
    db.refresh(state)

    return state


def update_last_assigned_employee(
    db: Session,
    state: RoutingState,
    employee_id: int,
) -> RoutingState:
    state.last_assigned_employee_id = employee_id

    db.commit()
    db.refresh(state)

    return state


def reset_routing_states(
    db: Session,
) -> int:
    updated_count = (
        db.query(RoutingState)
        .update(
            {
                RoutingState.last_assigned_employee_id: None,
            },
            synchronize_session=False,
        )
    )

    db.commit()

    return updated_count
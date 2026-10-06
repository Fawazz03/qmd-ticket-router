from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.models.ticket import Ticket


def create_tickets(
    db: Session,
    tickets: list[dict],
) -> list[Ticket]:
    new_tickets = [
        Ticket(**ticket)
        for ticket in tickets
    ]

    db.add_all(new_tickets)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    for ticket in new_tickets:
        db.refresh(ticket)

    return new_tickets


def get_all_tickets(
    db: Session,
    status: str | None = None,
) -> list[Ticket]:
    query = (
        db.query(Ticket)
        .options(
            joinedload(Ticket.assigned_employee)
        )
    )

    if status:
        query = query.filter(
            Ticket.status == status
        )

    return (
        query
        .order_by(Ticket.id)
        .all()
    )


def get_backlog_tickets(
    db: Session,
) -> list[Ticket]:
    return (
        db.query(Ticket)
        .filter(
            Ticket.status == "backlog"
        )
        .order_by(Ticket.id)
        .all()
    )


def reset_simulation_tickets(
    db: Session,
) -> int:
    updated_count = (
        db.query(Ticket)
        .filter(
            Ticket.status.in_(["active", "assigned"])
        )
        .update(
            {
                Ticket.status: "backlog",
                Ticket.assigned_employee_id: None,
                Ticket.assigned_at: None,
                Ticket.arrived_at: None,
            },
            synchronize_session=False,
        )
    )

    db.commit()

    return updated_count
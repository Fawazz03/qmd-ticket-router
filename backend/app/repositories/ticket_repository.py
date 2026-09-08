from sqlalchemy.orm import Session

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
    db.commit()

    for ticket in new_tickets:
        db.refresh(ticket)

    return new_tickets


def get_all_tickets(db: Session) -> list[Ticket]:
    return (
        db.query(Ticket)
        .order_by(Ticket.id)
        .all()
    )


def get_backlog_tickets(db: Session) -> list[Ticket]:
    return (
        db.query(Ticket)
        .filter(
            Ticket.status == "backlog"
        )
        .order_by(Ticket.id)
        .all()
    )
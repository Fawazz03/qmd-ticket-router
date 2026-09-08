import asyncio
from datetime import datetime

from app.core.database import SessionLocal
from app.repositories.ticket_repository import get_backlog_tickets
from app.services.routing_service import route_ticket
from app.services.simulation_service import get_simulation_state


async def run_simulation():
    """
    Run the ticket simulation.

    Each cycle:
    1. Read the current simulation settings.
    2. Take the configured number of backlog tickets.
    3. Mark them as active.
    4. Route each ticket.
    5. Wait for the configured interval.
    6. Repeat until stopped or backlog is empty.
    """

    while True:
        state = get_simulation_state()

        if not state.running:
            break

        db = SessionLocal()

        try:
            backlog_tickets = get_backlog_tickets(db)

            if not backlog_tickets:
                break

            batch = backlog_tickets[:state.batch_size]

            for ticket in batch:
                ticket.status = "active"
                ticket.arrived_at = datetime.now()

                db.commit()
                db.refresh(ticket)

                route_ticket(
                    db,
                    ticket,
                )

        finally:
            db.close()

        await asyncio.sleep(state.interval_seconds)
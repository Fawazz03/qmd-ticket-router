from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories import ticket_repository
from app.schemas.ticket import (
    TicketOut,
    TicketUploadResult,
)
from app.utils.excel_parser import parse_ticket_excel


def upload_tickets(
    db: Session,
    file: UploadFile,
) -> TicketUploadResult:
    tickets = parse_ticket_excel(file)

    created_tickets = ticket_repository.create_tickets(
        db,
        tickets,
    )

    return TicketUploadResult(
        total_tickets=len(created_tickets),
        backlog_count=sum(
            1
            for ticket in created_tickets
            if ticket.status == "backlog"
        ),
    )


def list_tickets(
    db: Session,
    status: str | None = None,
) -> list[TicketOut]:
    tickets = ticket_repository.get_all_tickets(
        db,
        status,
    )

    result = []

    for ticket in tickets:
        out = TicketOut.model_validate(ticket)

        out.assigned_employee_name = (
            ticket.assigned_employee.name
            if ticket.assigned_employee
            else None
        )

        result.append(out)

    return result
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.ticket_repository import create_tickets, get_all_tickets
from app.schemas.ticket import TicketUploadResult
from app.utils.excel_parser import parse_ticket_excel


def upload_tickets(
    db: Session,
    file: UploadFile,
) -> TicketUploadResult:
    tickets = parse_ticket_excel(file)

    created_tickets = create_tickets(
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


def list_tickets(db: Session):
    return get_all_tickets(db)
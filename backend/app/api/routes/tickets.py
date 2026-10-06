from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ticket import (
    TicketOut,
    TicketUploadResult,
)
from app.services import ticket_service


router = APIRouter(
    prefix="/api/tickets",
    tags=["tickets"],
)


@router.post(
    "/upload",
    response_model=TicketUploadResult,
)
def upload_tickets(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    try:
        return ticket_service.upload_tickets(
            db,
            file,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail=(
                "One or more tickets already exist. "
                "Please remove duplicate ticket numbers "
                "from the Excel file and try again."
            ),
        )


@router.get(
    "",
    response_model=list[TicketOut],
)
def get_tickets(
    status: str | None = None,
    db: Session = Depends(get_db),
):
    return ticket_service.list_tickets(
        db,
        status,
    )
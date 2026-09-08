from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.employee import EmployeeOut, RosterUploadResult
from app.services import roster_service


router = APIRouter(
    prefix="/api/roster",
    tags=["roster"],
)


@router.post(
    "/upload",
    response_model=RosterUploadResult,
)
def upload_roster(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return roster_service.upload_roster(db, file)


@router.get(
    "",
    response_model=list[EmployeeOut],
)
def get_roster(
    db: Session = Depends(get_db),
):
    return roster_service.list_roster(db)
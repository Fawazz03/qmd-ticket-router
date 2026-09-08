from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.employee_repository import (
    get_all_employees,
    replace_roster,
)
from app.schemas.employee import RosterUploadResult
from app.utils.excel_parser import parse_roster_excel


def upload_roster(
    db: Session,
    file: UploadFile,
) -> RosterUploadResult:
    parsed = parse_roster_excel(file)

    employees = replace_roster(db, parsed)

    return RosterUploadResult(
        total_employees=len(employees),
        agents=sum(
            1 for employee in employees if employee.role == "agent"
        ),
        leads=sum(
            1 for employee in employees if employee.role == "lead"
        ),
        queue=employees[0].queue if employees else "Gen IT",
    )


def list_roster(db: Session):
    return get_all_employees(db)
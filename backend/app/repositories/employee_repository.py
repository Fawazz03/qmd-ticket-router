from sqlalchemy.orm import Session

from app.models.employee import Employee


def replace_roster(
    db: Session,
    employees: list[dict],
) -> list[Employee]:
    db.query(Employee).delete()
    db.flush()

    new_employees = [
        Employee(**employee)
        for employee in employees
    ]

    db.add_all(new_employees)
    db.commit()

    for employee in new_employees:
        db.refresh(employee)

    return new_employees


def get_all_employees(
    db: Session,
) -> list[Employee]:
    return db.query(Employee).all()


def get_employees_by_role_and_queue(
    db: Session,
    role: str,
    queue: str,
) -> list[Employee]:
    return (
        db.query(Employee)
        .filter(
            Employee.role == role,
            Employee.queue == queue,
        )
        .order_by(Employee.id)
        .all()
    )
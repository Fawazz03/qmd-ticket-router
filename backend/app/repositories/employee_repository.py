from sqlalchemy.orm import Session

from app.models.employee import Employee


def replace_roster(
    db: Session,
    employees: list[dict],
) -> list[Employee]:
    # Preserve existing employees for assignment history.
    # They become inactive when a new roster is uploaded.
    db.query(Employee).update(
        {
            Employee.is_active: False,
        },
        synchronize_session=False,
    )

    new_employees = [
        Employee(
            **employee,
            is_active=True,
        )
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
    return (
        db.query(Employee)
        .filter(Employee.is_active.is_(True))
        .all()
    )


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
            Employee.is_active.is_(True),
        )
        .order_by(Employee.id)
        .all()
    )
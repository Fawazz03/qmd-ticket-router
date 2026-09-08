from datetime import datetime

from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.models.ticket import Ticket
from app.repositories.employee_repository import (
    get_all_employees,
    get_employees_by_role_and_queue,
)
from app.repositories.routing_state_repository import (
    get_or_create_routing_state,
    update_last_assigned_employee,
)
from app.routing.engine import (
    EligibleEmployee,
    get_eligible_employees,
    next_in_round_robin,
    select_pool,
)


def route_ticket(
    db: Session,
    ticket: Ticket,
) -> Assignment | None:
    """
    Route one ticket to the next eligible employee.

    Routing rules:
    - P1/P2 -> Lead pool, regardless of queue.
    - P3/P4 -> Agent pool, matching the ticket queue.
    - Employee must currently be within their shift.
    - Assignment uses persistent round-robin state.
    """

    pool = select_pool(ticket.priority)

    current_time = datetime.now().time()

    if pool == "lead":
        employees = [
            employee
            for employee in get_all_employees(db)
            if employee.role == "lead"
        ]
        queue = None

    else:
        employees = get_employees_by_role_and_queue(
            db,
            role="agent",
            queue=ticket.queue,
        )
        queue = ticket.queue

    eligible_employees = [
        EligibleEmployee(
            id=employee.id,
            name=employee.name,
            role=employee.role,
            shift_start=datetime.strptime(
                employee.shift_start,
                "%H:%M:%S",
            ).time(),
            shift_end=datetime.strptime(
                employee.shift_end,
                "%H:%M:%S",
            ).time(),
            queue=employee.queue,
        )
        for employee in employees
    ]

    eligible_employees = get_eligible_employees(
        employees=eligible_employees,
        role=pool,
        queue=queue,
        current_time=current_time,
    )

    if not eligible_employees:
        return None

    state = get_or_create_routing_state(
        db,
        queue=ticket.queue if queue else "GLOBAL",
        pool=pool,
    )

    selected_employee = next_in_round_robin(
        employees=eligible_employees,
        last_assigned_employee_id=state.last_assigned_employee_id,
    )

    if selected_employee is None:
        return None

    assignment = Assignment(
        ticket_id=ticket.id,
        employee_id=selected_employee.id,
        routing_type="round_robin",
    )

    db.add(assignment)

    ticket.status = "assigned"
    ticket.assigned_employee_id = selected_employee.id
    ticket.assigned_at = datetime.now()

    db.commit()
    db.refresh(assignment)

    update_last_assigned_employee(
        db,
        state,
        selected_employee.id,
    )

    return assignment

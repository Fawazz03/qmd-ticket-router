from dataclasses import dataclass
from datetime import time


@dataclass
class EligibleEmployee:
    id: int
    name: str
    role: str
    shift_start: time
    shift_end: time
    queue: str


def select_pool(priority: str) -> str:
    """
    Decide which employee pool should receive the ticket.

    P1/P2 -> Lead
    P3/P4 -> Agent
    """
    if priority in ("P1", "P2"):
        return "lead"

    if priority in ("P3", "P4"):
        return "agent"

    raise ValueError(
        f"Invalid priority: {priority}"
    )


def is_within_shift(
    current_time: time,
    shift_start: time,
    shift_end: time,
) -> bool:
    """
    Check whether an employee is currently within their shift.

    Example:
    Shift: 09:00 - 18:00
    Current time: 10:00 -> True
    Current time: 20:00 -> False
    """
    return shift_start <= current_time <= shift_end


def get_eligible_employees(
    employees: list[EligibleEmployee],
    role: str,
    queue: str | None,
    current_time: time,
) -> list[EligibleEmployee]:
    """
    Return employees who are eligible to receive a ticket.

    Rules:
    - Employee role must match the required pool.
    - P3/P4 routing uses the ticket's queue.
    - P1/P2 routing does not restrict Leads by queue.
    - Employee must currently be within their shift.
    """
    eligible = []

    for employee in employees:
        if employee.role != role:
            continue

        if queue is not None and employee.queue != queue:
            continue

        if not is_within_shift(
            current_time,
            employee.shift_start,
            employee.shift_end,
        ):
            continue

        eligible.append(employee)

    return eligible


def next_in_round_robin(
    employees: list[EligibleEmployee],
    last_assigned_employee_id: int | None,
) -> EligibleEmployee | None:
    """
    Select the next employee using round-robin ordering.

    If there is no previous assignment, the first eligible
    employee is selected.

    If there was a previous assignment, select the next
    employee after that employee.

    If the previous employee is no longer eligible, restart
    from the first eligible employee.
    """
    if not employees:
        return None

    if last_assigned_employee_id is None:
        return employees[0]

    for index, employee in enumerate(employees):
        if employee.id == last_assigned_employee_id:
            next_index = (index + 1) % len(employees)
            return employees[next_index]

    return employees[0]
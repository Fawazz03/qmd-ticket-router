from datetime import time

from app.routing.engine import (
    EligibleEmployee,
    get_eligible_employees,
    is_within_shift,
    next_in_round_robin,
    select_pool,
)


def make_employee(
    employee_id: int,
    name: str,
    role: str,
    queue: str,
    start: time = time(9, 0),
    end: time = time(18, 0),
) -> EligibleEmployee:
    return EligibleEmployee(
        id=employee_id,
        name=name,
        role=role,
        shift_start=start,
        shift_end=end,
        queue=queue,
    )


def test_select_pool_for_priority():
    assert select_pool("P1") == "lead"
    assert select_pool("P2") == "lead"
    assert select_pool("P3") == "agent"
    assert select_pool("P4") == "agent"


def test_invalid_priority():
    try:
        select_pool("P5")
        assert False
    except ValueError:
        assert True


def test_employee_within_shift():
    assert is_within_shift(
        time(10, 0),
        time(9, 0),
        time(18, 0),
    )

    assert not is_within_shift(
        time(20, 0),
        time(9, 0),
        time(18, 0),
    )


def test_p3_ticket_only_gets_matching_queue_agents():
    employees = [
        make_employee(1, "Arjun", "agent", "GenIT"),
        make_employee(2, "Priya", "agent", "Kite"),
        make_employee(3, "Rahul", "agent", "Research"),
        make_employee(4, "Sneha", "lead", "Research"),
    ]

    eligible = get_eligible_employees(
        employees=employees,
        role="agent",
        queue="Research",
        current_time=time(10, 0),
    )

    assert [employee.name for employee in eligible] == ["Rahul"]


def test_p1_p2_leads_are_not_restricted_by_queue():
    employees = [
        make_employee(1, "Arjun", "agent", "GenIT"),
        make_employee(2, "Sneha", "lead", "Medical Affairs"),
        make_employee(3, "Karthik", "lead", "Access Pod"),
    ]

    eligible = get_eligible_employees(
        employees=employees,
        role="lead",
        queue=None,
        current_time=time(10, 0),
    )

    assert [employee.name for employee in eligible] == [
        "Sneha",
        "Karthik",
    ]


def test_employee_outside_shift_is_not_eligible():
    employees = [
        make_employee(
            1,
            "Arjun",
            "agent",
            "GenIT",
            start=time(9, 0),
            end=time(18, 0),
        ),
        make_employee(
            2,
            "Rahul",
            "agent",
            "GenIT",
            start=time(14, 0),
            end=time(23, 0),
        ),
    ]

    eligible = get_eligible_employees(
        employees=employees,
        role="agent",
        queue="GenIT",
        current_time=time(10, 0),
    )

    assert [employee.name for employee in eligible] == ["Arjun"]


def test_round_robin_starts_with_first_employee():
    employees = [
        make_employee(1, "Arjun", "agent", "GenIT"),
        make_employee(2, "Priya", "agent", "GenIT"),
        make_employee(3, "Rahul", "agent", "GenIT"),
    ]

    selected = next_in_round_robin(
        employees,
        last_assigned_employee_id=None,
    )

    assert selected.name == "Arjun"


def test_round_robin_selects_next_employee():
    employees = [
        make_employee(1, "Arjun", "agent", "GenIT"),
        make_employee(2, "Priya", "agent", "GenIT"),
        make_employee(3, "Rahul", "agent", "GenIT"),
    ]

    selected = next_in_round_robin(
        employees,
        last_assigned_employee_id=1,
    )

    assert selected.name == "Priya"


def test_round_robin_wraps_to_first_employee():
    employees = [
        make_employee(1, "Arjun", "agent", "GenIT"),
        make_employee(2, "Priya", "agent", "GenIT"),
        make_employee(3, "Rahul", "agent", "GenIT"),
    ]

    selected = next_in_round_robin(
        employees,
        last_assigned_employee_id=3,
    )

    assert selected.name == "Arjun"


def test_round_robin_restarts_if_previous_employee_is_not_eligible():
    employees = [
        make_employee(2, "Priya", "agent", "GenIT"),
        make_employee(3, "Rahul", "agent", "GenIT"),
    ]

    selected = next_in_round_robin(
        employees,
        last_assigned_employee_id=1,
    )

    assert selected.name == "Priya"


def test_round_robin_returns_none_when_no_employee_is_eligible():
    selected = next_in_round_robin(
        employees=[],
        last_assigned_employee_id=None,
    )

    assert selected is None
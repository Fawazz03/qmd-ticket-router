from openpyxl import load_workbook
from fastapi import UploadFile, HTTPException
import io


# ============================================================
# ROSTER PARSER
# ============================================================

REQUIRED_COLUMNS = [
    "Name",
    "Role",
    "Shift Start",
    "Shift End",
    "Queue",
]

VALID_ROLES = {"Agent", "Lead"}


def parse_roster_excel(file: UploadFile) -> list[dict]:
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            400,
            "Invalid file type. Please upload an Excel file (.xlsx or .xls).",
        )

    contents = file.file.read()

    try:
        wb = load_workbook(io.BytesIO(contents), data_only=True)
    except Exception:
        raise HTTPException(
            400,
            "Could not read the Excel file. It may be corrupted.",
        )

    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))

    if not rows or len(rows) < 2:
        raise HTTPException(400, "The uploaded roster is empty.")

    headers = [str(h).strip() if h else "" for h in rows[0]]

    missing = [col for col in REQUIRED_COLUMNS if col not in headers]

    if missing:
        raise HTTPException(
            400,
            f"Missing required column(s): {', '.join(missing)}",
        )

    col_index = {
        col: headers.index(col)
        for col in REQUIRED_COLUMNS
    }

    employees = []
    seen_names = set()

    for i, row in enumerate(rows[1:], start=2):
        name = row[col_index["Name"]]
        role = row[col_index["Role"]]
        shift_start = row[col_index["Shift Start"]]
        shift_end = row[col_index["Shift End"]]
        queue = row[col_index["Queue"]]

        if not name or not str(name).strip():
            raise HTTPException(
                400,
                f"Row {i}: missing employee name.",
            )

        name = str(name).strip()

        if name in seen_names:
            raise HTTPException(
                400,
                f"Row {i}: duplicate employee name '{name}'.",
            )

        seen_names.add(name)

        if role not in VALID_ROLES:
            raise HTTPException(
                400,
                f"Row {i}: invalid role '{role}'. Must be Agent or Lead.",
            )

        if not shift_start or not str(shift_start).strip():
            raise HTTPException(
                400,
                f"Row {i}: missing shift start time.",
            )

        if not shift_end or not str(shift_end).strip():
            raise HTTPException(
                400,
                f"Row {i}: missing shift end time.",
            )

        if not queue or not str(queue).strip():
            raise HTTPException(
                400,
                f"Row {i}: missing queue.",
            )

        employees.append(
            {
                "name": name,
                "role": role.lower(),
                "shift_start": str(shift_start).strip(),
                "shift_end": str(shift_end).strip(),
                "queue": str(queue).strip(),
            }
        )

    return employees


# ============================================================
# TICKET PARSER
# ============================================================

TICKET_REQUIRED_COLUMNS = [
    "Ticket Number",
    "Title",
    "Priority",
    "Type",
    "Queue",
]

VALID_TICKET_PRIORITIES = {
    "P1",
    "P2",
    "P3",
    "P4",
}

VALID_TICKET_QUEUES = {
    "Kite",
    "Medical Affairs",
    "GenIT",
    "Access Pod",
    "Research",
}

VALID_TICKET_TYPES = {
    "Incident",
    "Task",
}


def parse_ticket_excel(file: UploadFile) -> list[dict]:
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(
            400,
            "Invalid file type. Please upload an Excel file (.xlsx).",
        )

    contents = file.file.read()

    try:
        wb = load_workbook(
            io.BytesIO(contents),
            data_only=True,
        )
    except Exception:
        raise HTTPException(
            400,
            "Could not read the Excel file. It may be corrupted.",
        )

    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))

    if not rows or len(rows) < 2:
        raise HTTPException(
            400,
            "The uploaded ticket file is empty.",
        )

    headers = [
        str(header).strip() if header else ""
        for header in rows[0]
    ]

    missing = [
        column
        for column in TICKET_REQUIRED_COLUMNS
        if column not in headers
    ]

    if missing:
        raise HTTPException(
            400,
            f"Missing required column(s): {', '.join(missing)}",
        )

    col_index = {
        column: headers.index(column)
        for column in TICKET_REQUIRED_COLUMNS
    }

    # Description is optional
    description_index = (
        headers.index("Description")
        if "Description" in headers
        else None
    )

    tickets = []
    seen_ticket_numbers = set()

    for row_number, row in enumerate(rows[1:], start=2):
        ticket_number = row[col_index["Ticket Number"]]
        title = row[col_index["Title"]]
        priority = row[col_index["Priority"]]
        ticket_type = row[col_index["Type"]]
        queue = row[col_index["Queue"]]

        description = (
            row[description_index]
            if description_index is not None
            else None
        )

        # ----------------------------------------------------
        # Ticket Number Validation
        # ----------------------------------------------------

        if not ticket_number or not str(ticket_number).strip():
            raise HTTPException(
                400,
                f"Row {row_number}: missing ticket number.",
            )

        ticket_number = str(ticket_number).strip()

        if ticket_number in seen_ticket_numbers:
            raise HTTPException(
                400,
                f"Row {row_number}: duplicate ticket number "
                f"'{ticket_number}'.",
            )

        seen_ticket_numbers.add(ticket_number)

        # ----------------------------------------------------
        # Title Validation
        # ----------------------------------------------------

        if not title or not str(title).strip():
            raise HTTPException(
                400,
                f"Row {row_number}: missing ticket title.",
            )

        title = str(title).strip()

        # ----------------------------------------------------
        # Priority Validation
        # ----------------------------------------------------

        if priority not in VALID_TICKET_PRIORITIES:
            raise HTTPException(
                400,
                f"Row {row_number}: invalid priority '{priority}'. "
                f"Must be P1, P2, P3, or P4.",
            )

        # ----------------------------------------------------
        # Type Validation
        # ----------------------------------------------------

        if ticket_type not in VALID_TICKET_TYPES:
            raise HTTPException(
                400,
                f"Row {row_number}: invalid type '{ticket_type}'. "
                f"Must be Incident or Task.",
            )

        # ----------------------------------------------------
        # Queue Validation
        # ----------------------------------------------------

        if not queue or not str(queue).strip():
            raise HTTPException(
                400,
                f"Row {row_number}: missing queue.",
            )

        queue = str(queue).strip()

        if queue not in VALID_TICKET_QUEUES:
            raise HTTPException(
                400,
                f"Row {row_number}: invalid queue '{queue}'.",
            )

        # ----------------------------------------------------
        # Create Ticket Dictionary
        # ----------------------------------------------------

        tickets.append(
            {
                "ticket_number": ticket_number,
                "title": title,
                "description": (
                    str(description).strip()
                    if description is not None
                    else None
                ),
                "priority": priority,
                "type": ticket_type,
                "queue": queue,
                "status": "backlog",
            }
        )

    return tickets
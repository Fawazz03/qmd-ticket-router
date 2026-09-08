from datetime import datetime
from typing import Optional

from pydantic import BaseModel


VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}

VALID_QUEUES = {
    "Kite",
    "Medical Affairs",
    "GenIT",
    "Access Pod",
    "Research",
}

VALID_TYPES = {
    "Incident",
    "Task",
}


class TicketOut(BaseModel):
    id: int
    ticket_number: str
    title: str
    priority: str
    type: Optional[str]
    queue: str
    status: str
    assigned_employee_id: Optional[int]
    created_at: datetime
    arrived_at: Optional[datetime]
    assigned_at: Optional[datetime]

    class Config:
        from_attributes = True


class TicketUploadResult(BaseModel):
    total_tickets: int
    backlog_count: int
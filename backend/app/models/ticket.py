from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.core.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False)
    type = Column(String, nullable=True)
    queue = Column(String, nullable=False, default="Gen IT")
    status = Column(String, nullable=False, default="backlog")

    assigned_employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    arrived_at = Column(DateTime(timezone=True), nullable=True)
    assigned_at = Column(DateTime(timezone=True), nullable=True)
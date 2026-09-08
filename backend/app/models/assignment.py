from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func

from app.core.database import Base


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    assignment_time = Column(DateTime(timezone=True), server_default=func.now())
    routing_type = Column(String, nullable=False)
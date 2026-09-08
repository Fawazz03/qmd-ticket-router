from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.database import Base


class RoutingState(Base):
    __tablename__ = "routing_state"

    id = Column(Integer, primary_key=True, index=True)
    queue = Column(String, nullable=False)
    pool = Column(String, nullable=False)
    last_assigned_employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=True,
    )
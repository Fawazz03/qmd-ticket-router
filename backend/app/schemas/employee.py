from pydantic import BaseModel


class EmployeeOut(BaseModel):
    id: int
    name: str
    role: str
    shift_start: str
    shift_end: str
    queue: str

    class Config:
        from_attributes = True


class RosterUploadResult(BaseModel):
    total_employees: int
    agents: int
    leads: int
    queue: str
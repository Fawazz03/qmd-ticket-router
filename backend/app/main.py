from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import roster, tickets, simulation
from app.core.config import settings
from app.core.database import Base, engine
from app.models import Assignment, Employee, RoutingState, Ticket


app = FastAPI(title=settings.app_name)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(roster.router)
app.include_router(tickets.router)
app.include_router(simulation.router)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
    }
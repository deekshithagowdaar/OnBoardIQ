from app.api.employees import router as employees_router
from app.api.tasks import router as tasks_router
from app.api.dependency import router as dependency_router
from app.api.risk import router as risk_router
from app.api.root_cause import router as root_cause_router
from app.api.simulation import router as simulation_router
from app.api.approvals import router as approvals_router
from app.api.readiness import router as readiness_router
from app.api.learning import router as learning_router
from app.api.agents import router as agents_router
from app.api.mock_department_apis import router as mock_router

__all__ = [
    "employees_router",
    "tasks_router",
    "dependency_router",
    "risk_router",
    "root_cause_router",
    "simulation_router",
    "approvals_router",
    "readiness_router",
    "learning_router",
    "agents_router",
    "mock_router",
]

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import DependencyGraphResponse

router = APIRouter(prefix="/dependency", tags=["Dependency Graph"])

@router.get("/{employee_id}/graph", response_model=DependencyGraphResponse)
def get_employee_dependency_graph(employee_id: str, db: Session = Depends(get_db)):
    try:
        return TaskService.get_dependency_graph(db, employee_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

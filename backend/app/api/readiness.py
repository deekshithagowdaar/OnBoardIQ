import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.analytics import ReadinessSnapshot
from app.services.task_service import TaskService
from app.engine.readiness_engine import ReadinessEngine
from app.engine.dependency_engine import DependencyEngine
from app.schemas.readiness import ReadinessResponse

router = APIRouter(prefix="/readiness", tags=["Readiness Score"])

@router.get("/{employee_id}", response_model=ReadinessResponse)
def get_readiness_score(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    tasks = TaskService.get_employee_tasks(db, emp.id)
    deps = TaskService.get_dependencies_for_employee(db, emp.id)

    task_dicts = [
        {
            "id": t.id,
            "task_id": t.task_id,
            "name": t.name,
            "department": t.department,
            "status": t.status,
            "priority": t.priority,
            "estimated_duration_days": t.estimated_duration_days,
            "is_critical": t.is_critical,
            "delay_reason": t.delay_reason,
        }
        for t in tasks
    ]

    crit_path = DependencyEngine.compute_critical_path(task_dicts, deps)
    readiness_data = ReadinessEngine.calculate_readiness(task_dicts, crit_path, emp.joining_date)

    snapshot = ReadinessSnapshot(
        id=str(uuid.uuid4()),
        employee_id=emp.id,
        overall_score=readiness_data["overall_score"],
        readiness_tier=readiness_data["readiness_tier"],
        department_scores=readiness_data["department_scores"],
        completed_tasks_count=readiness_data["completed_tasks_count"],
        total_tasks_count=readiness_data["total_tasks_count"],
        blocked_tasks_count=readiness_data["blocked_tasks_count"],
        critical_pending_count=readiness_data["critical_pending_count"],
        days_until_joining=readiness_data["days_until_joining"],
        score_explanation=readiness_data["score_explanation"],
    )
    db.add(snapshot)
    db.commit()

    return {
        "id": snapshot.id,
        "employee_id": emp.id,
        "overall_score": readiness_data["overall_score"],
        "readiness_tier": readiness_data["readiness_tier"],
        "department_scores": readiness_data["department_scores"],
        "completed_tasks_count": readiness_data["completed_tasks_count"],
        "total_tasks_count": readiness_data["total_tasks_count"],
        "blocked_tasks_count": readiness_data["blocked_tasks_count"],
        "critical_pending_count": readiness_data["critical_pending_count"],
        "days_until_joining": readiness_data["days_until_joining"],
        "score_explanation": readiness_data["score_explanation"],
        "formula_breakdown": readiness_data["formula_breakdown"],
        "critical_path_tasks": readiness_data["critical_path_tasks"],
        "timestamp": snapshot.timestamp or datetime.datetime.utcnow(),
    }

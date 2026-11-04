import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.risk import RootCauseAnalysis
from app.services.task_service import TaskService
from app.engine.root_cause_engine import RootCauseEngine
from app.schemas.risk import RootCauseAnalysisResponse

router = APIRouter(prefix="/root-cause", tags=["Root Cause Analysis"])

@router.get("/{employee_id}", response_model=RootCauseAnalysisResponse)
def get_root_cause_analysis(employee_id: str, db: Session = Depends(get_db)):
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

    rc_data = RootCauseEngine.analyze_root_cause(task_dicts, deps)
    if not rc_data:
        # If no delayed or blocked tasks, construct normal health report
        rc_data = {
            "primary_delayed_task_id": "NONE",
            "primary_delayed_task_name": "No Delayed Tasks",
            "root_cause_task_id": "NONE",
            "root_cause_task_name": "No Active Blocker",
            "root_cause_category": "Normal Operations",
            "explanation": "All onboarding tasks are proceeding normally or completed without upstream blockers.",
            "affected_downstream_task_ids": [],
            "affected_downstream_tasks": [],
            "estimated_joining_date_impact_days": 0.0,
            "evidence": {"status": "HEALTHY"}
        }

    analysis = RootCauseAnalysis(
        id=str(uuid.uuid4()),
        employee_id=emp.id,
        primary_delayed_task_id=rc_data["primary_delayed_task_id"],
        root_cause_task_id=rc_data["root_cause_task_id"],
        root_cause_category=rc_data["root_cause_category"],
        explanation=rc_data["explanation"],
        affected_downstream_task_ids=rc_data["affected_downstream_task_ids"],
        estimated_joining_date_impact_days=rc_data["estimated_joining_date_impact_days"],
        evidence=rc_data["evidence"],
    )
    db.add(analysis)
    db.commit()

    return {
        "id": analysis.id,
        "employee_id": emp.id,
        "primary_delayed_task_id": rc_data["primary_delayed_task_id"],
        "primary_delayed_task_name": rc_data["primary_delayed_task_name"],
        "root_cause_task_id": rc_data["root_cause_task_id"],
        "root_cause_task_name": rc_data["root_cause_task_name"],
        "root_cause_category": rc_data["root_cause_category"],
        "explanation": rc_data["explanation"],
        "affected_downstream_task_ids": rc_data["affected_downstream_task_ids"],
        "affected_downstream_tasks": rc_data["affected_downstream_tasks"],
        "estimated_joining_date_impact_days": rc_data["estimated_joining_date_impact_days"],
        "evidence": rc_data["evidence"],
        "created_at": analysis.created_at or datetime.datetime.utcnow(),
    }

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.services.task_service import TaskService
from app.orchestration.workflow import onboarding_graph
from app.orchestration.state import WorkflowState

router = APIRouter(prefix="/orchestration", tags=["LangGraph Agent Orchestration"])

@router.post("/run/{employee_id}")
def run_orchestration(employee_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
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
            "assigned_person": t.assigned_person,
            "estimated_duration_days": t.estimated_duration_days,
            "is_critical": t.is_critical,
            "delay_reason": t.delay_reason,
        }
        for t in tasks
    ]

    initial_state: WorkflowState = {
        "employee_id": emp.id,
        "employee_data": {
            "full_name": emp.full_name,
            "job_role": emp.job_role,
            "department": emp.department,
            "joining_date": emp.joining_date,
        },
        "tasks": task_dicts,
        "dependencies": deps,
        "department_statuses": {},
        "risk_info": {},
        "root_cause": None,
        "simulation_results": [],
        "recommendation": None,
        "approval_status": "NOT_STARTED",
        "readiness_score": 0.0,
        "readiness_details": {},
        "messages": [],
    }

    # Execute LangGraph state graph
    final_state = onboarding_graph.invoke(initial_state)

    return {
        "employee_id": emp.id,
        "department_statuses": final_state.get("department_statuses", {}),
        "risk_info": final_state.get("risk_info", {}),
        "root_cause": final_state.get("root_cause"),
        "simulation_results": final_state.get("simulation_results", []),
        "recommendation": final_state.get("recommendation"),
        "readiness_score": final_state.get("readiness_score", 0.0),
        "readiness_details": final_state.get("readiness_details", {}),
        "execution_trace": final_state.get("messages", []),
    }

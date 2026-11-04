import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.services.task_service import TaskService
from app.services.approval_service import ApprovalService
from app.engine.simulation_engine import SimulationEngine
from app.engine.recovery_optimizer import RecoveryOptimizer
from app.engine.readiness_engine import ReadinessEngine
from app.engine.risk_engine import RiskEngine
from app.schemas.simulation import WhatIfComparisonResponse, SimulationRunRequest, SimulationScenarioResponse

router = APIRouter(prefix="/simulation", tags=["What-If Simulator"])

@router.get("/{employee_id}/scenarios", response_model=WhatIfComparisonResponse)
def get_simulation_scenarios(employee_id: str, db: Session = Depends(get_db)):
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

    # Baseline readiness & risk
    baseline_readiness = ReadinessEngine.calculate_readiness(task_dicts)
    baseline_risk = RiskEngine.calculate_employee_risk(task_dicts, deps, emp.joining_date)

    # Run simulations
    scenarios = SimulationEngine.simulate_all_recovery_scenarios(
        employee_id=emp.id,
        tasks=task_dicts,
        dependencies=deps
    )

    # Optimize & pick recommended recovery strategy
    recommended_strategy = RecoveryOptimizer.optimize_recovery_strategy(
        employee_id=emp.id,
        scenarios=scenarios,
        employee_role=emp.job_role
    )

    # Synchronize recommendation with ApprovalRequest table so manager can review & approve
    if recommended_strategy:
        ApprovalService.create_approval_request_from_recommendation(
            db=db,
            employee_id=emp.id,
            recommendation=recommended_strategy
        )

    # Attach created_at for pydantic
    formatted_scenarios = []
    for sc in scenarios:
        sc["created_at"] = datetime.datetime.utcnow()
        formatted_scenarios.append(sc)

    if recommended_strategy:
        recommended_strategy["created_at"] = datetime.datetime.utcnow()

    return {
        "employee_id": emp.id,
        "baseline_readiness_score": baseline_readiness["overall_score"],
        "baseline_risk_level": baseline_risk["risk_category"],
        "scenarios": formatted_scenarios,
        "recommended_strategy": recommended_strategy,
    }

@router.post("/{employee_id}/run-custom", response_model=SimulationScenarioResponse)
def run_custom_simulation(
    employee_id: str,
    req: SimulationRunRequest,
    db: Session = Depends(get_db)
):
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

    res = SimulationEngine.run_scenario(
        employee_id=emp.id,
        tasks=task_dicts,
        dependencies=deps,
        scenario_key=req.scenario_key,
        scenario_title=f"Custom Action: {req.action_type}",
        description="Hypothetical user-configured workflow simulation.",
        action_type=req.action_type,
        parameters=req.parameters
    )
    res["created_at"] = datetime.datetime.utcnow()
    return res

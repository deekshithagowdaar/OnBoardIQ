import pytest
from app.seed_data import init_db, seed_demo_data
from app.services.employee_service import EmployeeService
from app.services.task_service import TaskService
from app.services.approval_service import ApprovalService
from app.engine.risk_engine import RiskEngine
from app.engine.root_cause_engine import RootCauseEngine
from app.engine.simulation_engine import SimulationEngine
from app.engine.recovery_optimizer import RecoveryOptimizer
from app.engine.readiness_engine import ReadinessEngine
from app.schemas.approval import ApprovalDecisionRequest

def test_full_alex_morgan_demo_workflow(db_session):
    # Initialize and seed
    init_db()
    seed_demo_data(target_db=db_session)

    # Step 1: Open Alex Morgan's profile
    alex = EmployeeService.get_employee_by_id(db_session, "EMP-2024-001")
    assert alex is not None
    assert alex.full_name == "Alex Morgan"
    assert alex.job_role == "Software Developer"

    # Step 2: Personalized Onboarding Plan
    tasks = TaskService.get_employee_tasks(db_session, alex.id)
    assert len(tasks) >= 8
    task_names = [t.name for t in tasks]
    assert "Identity Verification" in task_names
    assert "System Account Creation" in task_names
    assert "Developer Environment Setup" in task_names

    # Step 3: Graph shows Identity Verification is Delayed, downstream tasks Blocked
    id_task = next(t for t in tasks if t.name == "Identity Verification")
    account_task = next(t for t in tasks if t.name == "System Account Creation")
    dev_task = next(t for t in tasks if t.name == "Developer Environment Setup")

    assert id_task.status == "Delayed"
    assert account_task.status == "Blocked"
    assert dev_task.status == "Blocked"

    # Step 4: Risk Engine predicts delay
    deps = TaskService.get_dependencies_for_employee(db_session, alex.id)
    task_dicts = [{"id": t.id, "name": t.name, "status": t.status, "is_critical": t.is_critical, "estimated_duration_days": t.estimated_duration_days, "department": t.department, "delay_reason": t.delay_reason} for t in tasks]
    risk_res = RiskEngine.calculate_employee_risk(task_dicts, deps, alex.joining_date)
    assert risk_res["risk_category"] in ("High", "Critical")

    # Step 5: Root-cause engine pinpoints Identity Verification
    rc_res = RootCauseEngine.analyze_root_cause(task_dicts, deps)
    assert rc_res is not None
    assert rc_res["root_cause_task_name"] == "Identity Verification"
    assert len(rc_res["affected_downstream_task_ids"]) >= 2

    # Step 6 & 7: What-If simulation and recovery optimization
    scenarios = SimulationEngine.simulate_all_recovery_scenarios(
        employee_id=alex.id,
        tasks=task_dicts,
        dependencies=deps,
        root_cause_task_id=id_task.id
    )
    assert len(scenarios) == 3
    rec = RecoveryOptimizer.optimize_recovery_strategy(alex.id, scenarios, alex.job_role)
    assert rec["recommended_scenario_key"] == "scenario_a"

    # Step 8: Create Approval Request
    approval_req = ApprovalService.create_approval_request_from_recommendation(db_session, alex.id, rec)
    assert approval_req.status == "Pending"

    # Step 9 & 10: Manager approves and automated execution triggers
    decision = ApprovalDecisionRequest(
        status="Approved",
        approver_id="user-1",
        approver_name="Sarah Johnson",
        decision_notes="Expedited review approved for Day-1 developer readiness."
    )
    decided = ApprovalService.decide_approval(db_session, approval_req.id, decision)
    assert decided.status == "Approved"

    # Step 11: Refresh tasks from database and confirm state change
    db_session.refresh(id_task)
    db_session.refresh(account_task)
    assert id_task.status == "Completed"
    assert account_task.status != "Blocked"

    # Step 12: Readiness Score recalculation
    updated_tasks = TaskService.get_employee_tasks(db_session, alex.id)
    updated_dicts = [{"id": t.id, "name": t.name, "status": t.status, "is_critical": t.is_critical, "estimated_duration_days": t.estimated_duration_days, "department": t.department} for t in updated_tasks]
    readiness_res = ReadinessEngine.calculate_readiness(updated_dicts)
    # Readiness should significantly increase from baseline
    assert readiness_res["overall_score"] >= 35.0

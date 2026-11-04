import uuid
from app.services.approval_service import ApprovalService
from app.models.approval import ApprovalRequest
from app.models.task import Task, TaskDependency
from app.schemas.approval import ApprovalDecisionRequest
from app.services.task_service import TaskService

def test_approval_rejection_prevents_execution(db_session):
    emp_id = "test-emp-reject"
    rec = {
        "strategy_title": "Test Recovery Action",
        "rationale": "Justification",
        "action_type": "PRIORITIZE_TASK",
        "proposed_payload": {"task_id": "test-task-1"},
        "comparison_summary": {}
    }

    req = ApprovalService.create_approval_request_from_recommendation(db_session, emp_id, rec)
    assert req.status == "Pending"

    decision = ApprovalDecisionRequest(
        status="Rejected",
        approver_id="mgr-1",
        approver_name="Sarah Johnson",
        decision_notes="Budget limit reached"
    )
    decided = ApprovalService.decide_approval(db_session, req.id, decision)
    assert decided.status == "Rejected"
    assert len(decided.action_executions) == 0

def test_approval_and_automated_execution(db_session):
    emp_id = "test-emp-approve"
    
    # Create two tasks with dependency: t1 -> t2
    t1 = Task(
        id=str(uuid.uuid4()),
        employee_id=emp_id,
        task_id="TASK-1",
        name="Identity Verification",
        department="HR",
        assigned_person="Karen Vance",
        status="Delayed",
        start_date="2026-11-01",
        due_date="2026-11-03",
        estimated_duration_days=1.0,
        is_critical=True
    )
    t2 = Task(
        id=str(uuid.uuid4()),
        employee_id=emp_id,
        task_id="TASK-2",
        name="System Account",
        department="IT",
        assigned_person="David Miller",
        status="Blocked",
        start_date="2026-11-04",
        due_date="2026-11-06",
        estimated_duration_days=1.5,
        is_critical=True
    )
    db_session.add(t1)
    db_session.add(t2)
    db_session.commit()

    dep = TaskDependency(
        id=str(uuid.uuid4()),
        task_id=t2.id,
        depends_on_task_id=t1.id,
        dependency_type="Finish-to-Start"
    )
    db_session.add(dep)
    db_session.commit()

    # Create approval request to prioritize t1
    rec = {
        "strategy_title": "Expedite Identity Verification",
        "rationale": "Unblock IT access",
        "action_type": "PRIORITIZE_TASK",
        "proposed_payload": {"task_id": t1.id},
        "comparison_summary": {}
    }
    req = ApprovalService.create_approval_request_from_recommendation(db_session, emp_id, rec)

    # Approve
    decision = ApprovalDecisionRequest(
        status="Approved",
        approver_id="mgr-1",
        approver_name="Sarah Johnson",
        decision_notes="Approved for Day 1 readiness."
    )
    ApprovalService.decide_approval(db_session, req.id, decision)

    # Refresh tasks from DB
    db_session.refresh(t1)
    db_session.refresh(t2)

    # t1 should now be Completed!
    assert t1.status == "Completed"
    # t2 should now be Unblocked (Pending or In Progress)!
    assert t2.status != "Blocked"

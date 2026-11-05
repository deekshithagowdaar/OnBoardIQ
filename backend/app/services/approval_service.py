from typing import List, Dict, Any, Optional
import uuid
import datetime
from sqlalchemy.orm import Session
from app.models.approval import ApprovalRequest, ActionExecution, AuditLog
from app.models.task import Task
from app.models.employee import Employee
from app.models.analytics import HistoricalOutcome
from app.schemas.approval import ApprovalDecisionRequest
from app.services.task_service import TaskService
from app.integrations.mock_apis import MockHRSystem, MockITSystem, MockPayrollSystem, MockBenefitsSystem

class ApprovalService:
    @staticmethod
    def get_approval_requests(db: Session, employee_id: Optional[str] = None, status: Optional[str] = None) -> List[ApprovalRequest]:
        query = db.query(ApprovalRequest)
        if employee_id:
            query = query.filter(ApprovalRequest.employee_id == employee_id)
        if status:
            query = query.filter(ApprovalRequest.status == status)
        return query.order_by(ApprovalRequest.created_at.desc()).all()

    @staticmethod
    def create_approval_request_from_recommendation(
        db: Session,
        employee_id: str,
        recommendation: Dict[str, Any]
    ) -> ApprovalRequest:
        # If a Pending approval already exists for this employee+action, reuse it.
        # Also skip creation if one was already Approved (action already executed).
        existing = db.query(ApprovalRequest).filter(
            ApprovalRequest.employee_id == employee_id,
            ApprovalRequest.action_type == recommendation.get("action_type"),
            ApprovalRequest.status.in_(["Pending", "Approved"])
        ).first()
        if existing:
            return existing

        req = ApprovalRequest(
            id=str(uuid.uuid4()),
            employee_id=employee_id,
            title=recommendation.get("strategy_title", "Recovery Action Approval"),
            description=recommendation.get("rationale", "Proposed automated recovery workflow."),
            action_type=recommendation.get("action_type", "PRIORITIZE_TASK"),
            target_task_id=recommendation.get("proposed_payload", {}).get("task_id"),
            proposed_payload=recommendation.get("proposed_payload", {}),
            justification=recommendation.get("rationale", ""),
            impact_summary=recommendation.get("comparison_summary", {}),
            status="Pending",
            requested_by="AI Recovery Orchestrator",
        )
        db.add(req)
        db.commit()
        db.refresh(req)

        # Audit log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="APPROVAL",
            entity_id=req.id,
            action="CREATE",
            actor="AI Recovery Orchestrator",
            details={"title": req.title, "action_type": req.action_type}
        )
        db.add(audit)
        db.commit()

        return req

    @staticmethod
    def decide_approval(
        db: Session,
        approval_id: str,
        decision: ApprovalDecisionRequest
    ) -> ApprovalRequest:
        req = db.query(ApprovalRequest).filter(ApprovalRequest.id == approval_id).first()
        if not req:
            raise ValueError("Approval request not found.")

        if req.status != "Pending":
            raise ValueError(f"Approval request already decided with status: {req.status}")

        req.status = decision.status # Approved or Rejected
        req.approver_id = decision.approver_id
        req.approver_name = decision.approver_name
        req.decision_notes = decision.decision_notes
        req.decided_at = datetime.datetime.utcnow()

        db.commit()
        db.refresh(req)

        # Audit log decision
        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="APPROVAL",
            entity_id=req.id,
            action=decision.status.upper(),
            actor=decision.approver_name,
            details={"decision_notes": decision.decision_notes}
        )
        db.add(audit)
        db.commit()

        # If approved, immediately execute automated action & workflow adaptation!
        if decision.status == "Approved":
            ApprovalService.execute_action(db, req)

        return req

    @staticmethod
    def execute_action(db: Session, req: ApprovalRequest) -> ActionExecution:
        # Prevent duplicate execution
        existing_exec = db.query(ActionExecution).filter(ActionExecution.approval_id == req.id).first()
        if existing_exec:
            return existing_exec

        action_type = req.action_type
        payload = req.proposed_payload or {}
        emp_id = req.employee_id
        execution_summary = ""
        mock_result = {}

        if action_type == "PRIORITIZE_TASK":
            target_task_id = req.target_task_id or payload.get("task_id")
            target_task = db.query(Task).filter(Task.id == target_task_id).first()
            if target_task:
                # Dispatch to Mock HR System
                mock_result = MockHRSystem.verify_identity(emp_id)
                target_task.status = "Completed"
                target_task.actual_completion_date = datetime.date.today().isoformat()
                target_task.delay_reason = None
                execution_summary = (
                    f"Successfully executed '{mock_result.get('action')}' via {mock_result.get('system')}. "
                    f"Task '{target_task.name}' marked Completed. Upstream blocker cleared."
                )

        elif action_type == "RESOURCE_REASSIGNMENT":
            target_task_id = req.target_task_id or payload.get("task_id")
            new_assignee = payload.get("new_assignee", "Marcus Chen (Senior DevOps Lead)")
            target_task = db.query(Task).filter(Task.id == target_task_id).first()
            if target_task:
                mock_result = MockITSystem.reassign_it_resource(target_task_id, new_assignee)
                target_task.assigned_person = new_assignee
                target_task.status = "Completed"
                target_task.actual_completion_date = datetime.date.today().isoformat()
                target_task.delay_reason = None
                execution_summary = (
                    f"Reassigned '{target_task.name}' to {new_assignee} with P1 Priority. "
                    f"Sandbox credentials fast-tracked."
                )

        elif action_type == "REORDER_INDEPENDENT_TASKS":
            payroll_tasks = db.query(Task).filter(
                Task.employee_id == emp_id,
                Task.department.in_(["Payroll", "Benefits"])
            ).all()
            for pt in payroll_tasks:
                pt.status = "Completed"
                pt.actual_completion_date = datetime.date.today().isoformat()
            execution_summary = "Prioritized and completed independent Payroll & Benefits tasks."

        db.commit()

        # Recalculate downstream graph dependencies and sync statuses!
        TaskService.recalculate_and_sync_statuses(db, emp_id)

        # Create ActionExecution record
        execution = ActionExecution(
            id=str(uuid.uuid4()),
            approval_id=req.id,
            employee_id=emp_id,
            action_type=action_type,
            status="Success",
            execution_payload=mock_result or payload,
            result_summary=execution_summary,
            executed_by=req.approver_name or "System Orchestrator",
            executed_at=datetime.datetime.utcnow()
        )
        db.add(execution)

        # Log for continuous learning analytics
        outcome = HistoricalOutcome(
            id=str(uuid.uuid4()),
            employee_id=emp_id,
            department="Cross-Department",
            task_id=req.target_task_id or "TASK-RECOVERY",
            task_name=req.title,
            predicted_delay_days=2.5,
            actual_delay_days=0.0,
            root_cause_category="Upstream Bottleneck",
            recovery_strategy_used=req.title,
            was_approved=True,
            recovery_outcome="Success",
            time_saved_actual_days=2.5,
            completion_timestamp=datetime.datetime.utcnow(),
            is_synthetic_seed=False
        )
        db.add(outcome)

        # Audit log execution
        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="EXECUTION",
            entity_id=execution.id,
            action="EXECUTE",
            actor=req.approver_name or "System",
            details={"summary": execution_summary}
        )
        db.add(audit)
        db.commit()
        db.refresh(execution)

        return execution

    @staticmethod
    def get_audit_logs(db: Session, employee_id: Optional[str] = None) -> List[AuditLog]:
        query = db.query(AuditLog)
        return query.order_by(AuditLog.timestamp.desc()).limit(100).all()

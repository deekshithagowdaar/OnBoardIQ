import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    action_type = Column(String(100), nullable=False) # RESOURCE_REASSIGNMENT, PRIORITIZE_TASK, REORDER_TASKS, POLICY_WAIVER, SCHEDULE_UPDATE
    target_task_id = Column(String(50), nullable=True)
    proposed_payload = Column(JSON, default=dict)
    justification = Column(Text, nullable=False)
    impact_summary = Column(JSON, default=dict)
    status = Column(String(50), nullable=False, default="Pending") # Pending, Approved, Rejected
    requested_by = Column(String(100), nullable=False, default="AI Recovery Orchestrator")
    approver_id = Column(String(100), nullable=True)
    approver_name = Column(String(150), nullable=True)
    decision_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    decided_at = Column(DateTime, nullable=True)

    employee = relationship("Employee", back_populates="approval_requests")
    action_executions = relationship("ActionExecution", back_populates="approval_request")

class ActionExecution(Base):
    __tablename__ = "action_executions"

    id = Column(String(50), primary_key=True)
    approval_id = Column(String(50), ForeignKey("approval_requests.id", ondelete="SET NULL"), nullable=True)
    employee_id = Column(String(50), nullable=False, index=True)
    action_type = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="Success") # Success, Failed
    execution_payload = Column(JSON, default=dict)
    result_summary = Column(Text, nullable=False)
    executed_by = Column(String(100), nullable=False, default="System")
    executed_at = Column(DateTime, default=datetime.datetime.utcnow)

    approval_request = relationship("ApprovalRequest", back_populates="action_executions")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(50), primary_key=True)
    entity_type = Column(String(50), nullable=False) # EMPLOYEE, TASK, APPROVAL, EXECUTION
    entity_id = Column(String(50), nullable=False, index=True)
    action = Column(String(100), nullable=False) # CREATE, UPDATE, APPROVE, REJECT, EXECUTE
    actor = Column(String(100), nullable=False)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

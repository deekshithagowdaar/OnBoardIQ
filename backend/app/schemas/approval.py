from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class ApprovalDecisionRequest(BaseModel):
    status: str # Approved or Rejected
    approver_id: str
    approver_name: str
    decision_notes: Optional[str] = None

class ApprovalRequestResponse(BaseModel):
    id: str
    employee_id: str
    title: str
    description: str
    action_type: str
    target_task_id: Optional[str] = None
    proposed_payload: Dict[str, Any]
    justification: str
    impact_summary: Dict[str, Any]
    status: str # Pending, Approved, Rejected
    requested_by: str
    approver_id: Optional[str] = None
    approver_name: Optional[str] = None
    decision_notes: Optional[str] = None
    created_at: datetime
    decided_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ActionExecutionResponse(BaseModel):
    id: str
    approval_id: Optional[str] = None
    employee_id: str
    action_type: str
    status: str
    execution_payload: Dict[str, Any]
    result_summary: str
    executed_by: str
    executed_at: datetime
    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: str
    entity_type: str
    entity_id: str
    action: str
    actor: str
    details: Dict[str, Any]
    timestamp: datetime
    class Config:
        from_attributes = True

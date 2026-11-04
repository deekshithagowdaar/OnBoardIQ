from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.approval_service import ApprovalService
from app.schemas.approval import ApprovalRequestResponse, ApprovalDecisionRequest, AuditLogResponse

router = APIRouter(prefix="/approvals", tags=["Approvals & Self-Healing Workflow"])

@router.get("", response_model=List[ApprovalRequestResponse])
def get_approvals(
    employee_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return ApprovalService.get_approval_requests(db, employee_id=employee_id, status=status)

@router.post("/{approval_id}/decide", response_model=ApprovalRequestResponse)
def decide_approval(
    approval_id: str,
    decision: ApprovalDecisionRequest,
    db: Session = Depends(get_db)
):
    try:
        return ApprovalService.decide_approval(db, approval_id, decision)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    employee_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return ApprovalService.get_audit_logs(db, employee_id=employee_id)

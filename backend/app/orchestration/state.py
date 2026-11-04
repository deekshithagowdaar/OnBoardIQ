from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict

class WorkflowState(TypedDict, total=False):
    employee_id: str
    employee_data: Dict[str, Any]
    tasks: List[Dict[str, Any]]
    dependencies: List[Dict[str, Any]]
    department_statuses: Dict[str, Dict[str, Any]]
    risk_info: Dict[str, Any]
    root_cause: Optional[Dict[str, Any]]
    simulation_results: List[Dict[str, Any]]
    recommendation: Optional[Dict[str, Any]]
    approval_request: Optional[Dict[str, Any]]
    approval_status: str # "PENDING", "APPROVED", "REJECTED"
    execution_result: Optional[Dict[str, Any]]
    readiness_score: float
    readiness_details: Dict[str, Any]
    messages: List[str]
    next_step: str

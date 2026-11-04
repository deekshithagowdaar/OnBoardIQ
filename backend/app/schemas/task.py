from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class TaskBase(BaseModel):
    task_id: str
    name: str
    description: Optional[str] = None
    department: str # HR, IT, Payroll, Benefits
    assigned_person: str
    priority: str = "Medium" # Low, Medium, High, Critical
    start_date: str
    due_date: str
    estimated_duration_days: float = 1.0
    actual_completion_date: Optional[str] = None
    status: str = "Pending" # Pending, In Progress, Completed, Blocked, Delayed
    requires_approval: bool = False
    is_critical: bool = False
    delay_reason: Optional[str] = None
    category: Optional[str] = None

class TaskCreate(TaskBase):
    employee_id: str
    upstream_dependencies: Optional[List[str]] = [] # list of task_ids or db task IDs

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    assigned_person: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    estimated_duration_days: Optional[float] = None
    actual_completion_date: Optional[str] = None
    status: Optional[str] = None
    requires_approval: Optional[bool] = None
    is_critical: Optional[bool] = None
    delay_reason: Optional[str] = None

class TaskResponse(TaskBase):
    id: str
    employee_id: str
    upstream_dependencies: List[str] = []
    downstream_tasks: List[str] = []
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class TaskDependencyCreate(BaseModel):
    task_id: str # Downstream
    depends_on_task_id: str # Upstream
    dependency_type: str = "Finish-to-Start"

class TaskDependencyResponse(BaseModel):
    id: str
    task_id: str
    depends_on_task_id: str
    dependency_type: str
    created_at: datetime
    class Config:
        from_attributes = True

class ReactFlowNode(BaseModel):
    id: str
    type: str = "customTaskNode"
    position: Dict[str, float]
    data: Dict[str, Any]

class ReactFlowEdge(BaseModel):
    id: str
    source: str
    target: str
    animated: bool = False
    style: Optional[Dict[str, Any]] = None
    markerEnd: Optional[Dict[str, Any]] = None

class DependencyGraphResponse(BaseModel):
    employee_id: str
    nodes: List[ReactFlowNode]
    edges: List[ReactFlowEdge]
    blocked_task_ids: List[str]
    critical_path_task_ids: List[str]
    has_cycles: bool = False
    total_tasks: int
    completed_tasks: int

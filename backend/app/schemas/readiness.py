from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class ReadinessResponse(BaseModel):
    id: Optional[str] = None
    employee_id: str
    overall_score: float # 0 to 100
    readiness_tier: str # Not Ready, Needs Attention, On Track, Ready for Day 1
    department_scores: Dict[str, float] # {"HR": 60, "IT": 20, ...}
    completed_tasks_count: int
    total_tasks_count: int
    blocked_tasks_count: int
    critical_pending_count: int
    days_until_joining: int
    score_explanation: Optional[str] = None
    formula_breakdown: Optional[Dict[str, Any]] = None
    critical_path_tasks: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime
    class Config:
        from_attributes = True

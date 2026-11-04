from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class TaskRiskDetail(BaseModel):
    task_id: str
    task_name: str
    department: str
    status: str
    risk_score: float
    delay_probability: float
    reasons: List[str]

class RiskPredictionResponse(BaseModel):
    id: str
    employee_id: str
    overall_risk_score: float
    risk_category: str # Low, Medium, High, Critical
    factors: List[str]
    predicted_delay_days: float
    attention_level: str # Normal, Monitor Closely, Immediate Action Required
    task_risks: List[TaskRiskDetail]
    created_at: datetime
    class Config:
        from_attributes = True

class AffectedTaskDetail(BaseModel):
    task_id: str
    task_name: str
    department: str
    status: str
    delay_impact_days: float

class RootCauseAnalysisResponse(BaseModel):
    id: str
    employee_id: str
    primary_delayed_task_id: str
    primary_delayed_task_name: str
    root_cause_task_id: str
    root_cause_task_name: str
    root_cause_category: str
    explanation: str
    affected_downstream_task_ids: List[str]
    affected_downstream_tasks: List[AffectedTaskDetail]
    estimated_joining_date_impact_days: float
    evidence: Dict[str, Any]
    created_at: datetime
    class Config:
        from_attributes = True

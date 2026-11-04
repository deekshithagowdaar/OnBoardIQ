from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class SimulationRunRequest(BaseModel):
    scenario_key: str # scenario_a, scenario_b, scenario_c, custom
    action_type: str
    parameters: Dict[str, Any] = {}

class SimulationScenarioResponse(BaseModel):
    id: str
    employee_id: str
    scenario_key: str
    scenario_title: str
    description: str
    action_type: str
    parameters: Dict[str, Any]
    unblocked_task_ids: List[str]
    unblocked_count: int
    time_saved_days: float
    expected_completion_date: Optional[str] = None
    joining_date_risk: str
    readiness_score_projected: float
    department_readiness: Dict[str, float]
    feasibility_score: float
    policy_compliance: bool
    created_at: datetime
    class Config:
        from_attributes = True

class RecoveryRecommendationResponse(BaseModel):
    id: str
    employee_id: str
    recommended_scenario_key: str
    strategy_title: str
    rationale: str
    action_type: str
    proposed_payload: Dict[str, Any]
    requires_approval: bool
    approval_level: str
    comparison_summary: Dict[str, Any]
    created_at: datetime
    class Config:
        from_attributes = True

class WhatIfComparisonResponse(BaseModel):
    employee_id: str
    baseline_readiness_score: float
    baseline_risk_level: str
    scenarios: List[SimulationScenarioResponse]
    recommended_strategy: Optional[RecoveryRecommendationResponse] = None

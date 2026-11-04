from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class HistoricalOutcomeResponse(BaseModel):
    id: str
    employee_id: str
    department: str
    task_id: str
    task_name: str
    predicted_delay_days: float
    actual_delay_days: float
    root_cause_category: str
    recovery_strategy_used: str
    was_approved: bool
    recovery_outcome: str # Success, Partial, Escalated
    time_saved_actual_days: float
    completion_timestamp: datetime
    is_synthetic_seed: bool
    class Config:
        from_attributes = True

class BottleneckItem(BaseModel):
    department: str
    task_name: str
    delay_count: int
    avg_delay_days: float
    percentage_of_total_delays: float

class StrategyPerformanceItem(BaseModel):
    strategy_name: str
    times_recommended: int
    approval_rate: float
    success_rate: float
    avg_days_saved: float

class LearningAnalyticsResponse(BaseModel):
    total_completed_onboardings: int
    bottlenecks: List[BottleneckItem]
    recovery_strategies_performance: List[StrategyPerformanceItem]
    prediction_accuracy_mae: float # Mean Absolute Error in days
    prediction_vs_actual: List[Dict[str, Any]]
    department_performance: List[Dict[str, Any]]
    historical_outcomes: List[HistoricalOutcomeResponse]

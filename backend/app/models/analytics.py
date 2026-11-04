import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class ReadinessSnapshot(Base):
    __tablename__ = "readiness_snapshots"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    overall_score = Column(Float, nullable=False, default=0.0) # 0 to 100
    readiness_tier = Column(String(50), nullable=False) # Not Ready, Needs Attention, On Track, Ready for Day 1
    department_scores = Column(JSON, default=dict) # {"HR": 60.0, "IT": 20.0, ...}
    completed_tasks_count = Column(Integer, default=0)
    total_tasks_count = Column(Integer, default=0)
    blocked_tasks_count = Column(Integer, default=0)
    critical_pending_count = Column(Integer, default=0)
    days_until_joining = Column(Integer, default=0)
    score_explanation = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    employee = relationship("Employee", back_populates="readiness_snapshots")

class HistoricalOutcome(Base):
    __tablename__ = "historical_outcomes"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), nullable=False, index=True)
    department = Column(String(100), nullable=False, index=True)
    task_id = Column(String(50), nullable=False)
    task_name = Column(String(200), nullable=False)
    predicted_delay_days = Column(Float, default=0.0)
    actual_delay_days = Column(Float, default=0.0)
    root_cause_category = Column(String(100), nullable=False)
    recovery_strategy_used = Column(String(150), nullable=False)
    was_approved = Column(Boolean, default=True)
    recovery_outcome = Column(String(50), default="Success") # Success, Partial, Escalated
    time_saved_actual_days = Column(Float, default=0.0)
    completion_timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    is_synthetic_seed = Column(Boolean, default=False)

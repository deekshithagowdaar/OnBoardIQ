import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Float
from app.database import Base

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    overall_risk_score = Column(Float, nullable=False, default=0.0) # 0 to 100
    risk_category = Column(String(50), nullable=False, default="Low") # Low, Medium, High, Critical
    factors = Column(JSON, default=list) # List of factor strings / objects
    predicted_delay_days = Column(Float, default=0.0)
    attention_level = Column(String(50), default="Normal") # Normal, Monitor Closely, Immediate Action Required
    task_risks = Column(JSON, default=list) # Breakdown by task
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class RootCauseAnalysis(Base):
    __tablename__ = "root_cause_analyses"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    primary_delayed_task_id = Column(String(50), nullable=False)
    root_cause_task_id = Column(String(50), nullable=False)
    root_cause_category = Column(String(100), nullable=False)
    explanation = Column(Text, nullable=False)
    affected_downstream_task_ids = Column(JSON, default=list)
    estimated_joining_date_impact_days = Column(Float, default=0.0)
    evidence = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

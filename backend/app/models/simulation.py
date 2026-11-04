import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Float, Integer, Boolean
from app.database import Base

class SimulationScenario(Base):
    __tablename__ = "simulation_scenarios"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_key = Column(String(50), nullable=False) # scenario_a, scenario_b, scenario_c, custom
    scenario_title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    action_type = Column(String(100), nullable=False)
    parameters = Column(JSON, default=dict)
    unblocked_task_ids = Column(JSON, default=list)
    unblocked_count = Column(Integer, default=0)
    time_saved_days = Column(Float, default=0.0)
    expected_completion_date = Column(String(50), nullable=True)
    joining_date_risk = Column(String(50), default="Low") # Low, Medium, High, Critical
    readiness_score_projected = Column(Float, default=0.0)
    department_readiness = Column(JSON, default=dict)
    feasibility_score = Column(Float, default=1.0)
    policy_compliance = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RecoveryRecommendation(Base):
    __tablename__ = "recovery_recommendations"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    recommended_scenario_key = Column(String(50), nullable=False)
    strategy_title = Column(String(200), nullable=False)
    rationale = Column(Text, nullable=False)
    action_type = Column(String(100), nullable=False)
    proposed_payload = Column(JSON, default=dict)
    requires_approval = Column(Boolean, default=True)
    approval_level = Column(String(50), default="MANAGER") # MANAGER, HR_ADMIN, NONE
    comparison_summary = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

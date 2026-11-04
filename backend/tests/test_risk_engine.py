from app.engine.risk_engine import RiskEngine

def test_risk_clean_workflow():
    tasks = [
        {"id": "t1", "name": "Task 1", "status": "Completed", "estimated_duration_days": 1.0, "is_critical": True},
        {"id": "t2", "name": "Task 2", "status": "Completed", "estimated_duration_days": 1.0, "is_critical": False},
    ]
    deps = []
    res = RiskEngine.calculate_employee_risk(tasks, deps, "2026-11-20")
    assert res["overall_risk_score"] == 0.0
    assert res["risk_category"] == "Low"
    assert res["attention_level"] == "Normal"

def test_risk_delayed_critical_task():
    tasks = [
        {"id": "t1", "name": "Identity Verification", "status": "Delayed", "delay_reason": "Missing ID", "estimated_duration_days": 1.0, "is_critical": True},
        {"id": "t2", "name": "System Account", "status": "Blocked", "delay_reason": "Waiting on ID", "estimated_duration_days": 1.5, "is_critical": True},
    ]
    deps = [{"task_id": "t2", "depends_on_task_id": "t1"}]
    res = RiskEngine.calculate_employee_risk(tasks, deps, "2026-11-20")
    assert res["overall_risk_score"] >= 75.0
    assert res["risk_category"] in ("High", "Critical")
    assert res["predicted_delay_days"] > 0
    assert len(res["factors"]) > 0

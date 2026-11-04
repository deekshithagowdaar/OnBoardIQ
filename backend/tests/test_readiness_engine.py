from app.engine.readiness_engine import ReadinessEngine

def test_readiness_calculation():
    tasks = [
        {"id": "1", "department": "HR", "status": "Completed", "is_critical": True},
        {"id": "2", "department": "IT", "status": "Completed", "is_critical": True},
        {"id": "3", "department": "Payroll", "status": "Completed", "is_critical": False},
        {"id": "4", "department": "Benefits", "status": "Completed", "is_critical": False},
    ]
    res = ReadinessEngine.calculate_readiness(tasks)
    assert res["overall_score"] >= 90.0
    assert res["readiness_tier"] == "Ready for Day 1"

def test_readiness_blocked_penalty():
    tasks = [
        {"id": "1", "department": "HR", "status": "Delayed", "is_critical": True},
        {"id": "2", "department": "IT", "status": "Blocked", "is_critical": True},
        {"id": "3", "department": "Payroll", "status": "Pending", "is_critical": False},
        {"id": "4", "department": "Benefits", "status": "Pending", "is_critical": False},
    ]
    res = ReadinessEngine.calculate_readiness(tasks)
    assert res["overall_score"] < 50.0
    assert res["readiness_tier"] == "Not Ready"
    assert res["blocked_tasks_count"] == 2

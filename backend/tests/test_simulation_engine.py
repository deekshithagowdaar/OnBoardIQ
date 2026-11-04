import copy
from app.engine.simulation_engine import SimulationEngine
from app.engine.recovery_optimizer import RecoveryOptimizer

def test_simulation_ephemeral_isolation():
    original_tasks = [
        {"id": "t1", "name": "Identity Verification", "status": "Delayed", "department": "HR", "is_critical": True, "estimated_duration_days": 1.0},
        {"id": "t2", "name": "System Account", "status": "Blocked", "department": "IT", "is_critical": True, "estimated_duration_days": 1.5},
    ]
    deps = [{"task_id": "t2", "depends_on_task_id": "t1"}]

    tasks_copy = copy.deepcopy(original_tasks)

    # Run simulation of Scenario A
    res = SimulationEngine.run_scenario(
        employee_id="emp-1",
        tasks=original_tasks,
        dependencies=deps,
        scenario_key="scenario_a",
        scenario_title="Scenario A: Expedited ID",
        description="Expedite ID",
        action_type="PRIORITIZE_TASK",
        parameters={"task_id": "t1"}
    )

    # Verify original tasks are completely UNMUTATED!
    assert original_tasks[0]["status"] == "Delayed"
    assert original_tasks[1]["status"] == "Blocked"

    # Verify simulation result reflects unblocked status
    assert "t2" in res["unblocked_task_ids"]
    assert res["unblocked_count"] >= 1
    assert res["time_saved_days"] > 0

def test_recovery_optimizer_selection():
    scenarios = [
        {
            "scenario_key": "scenario_a",
            "scenario_title": "Scenario A: Priority HR",
            "action_type": "PRIORITIZE_TASK",
            "parameters": {"task_id": "t1"},
            "time_saved_days": 3.0,
            "unblocked_count": 2,
            "readiness_score_projected": 85.0,
            "feasibility_score": 0.95,
            "policy_compliance": True
        },
        {
            "scenario_key": "scenario_c",
            "scenario_title": "Scenario C: Reorder Tasks",
            "action_type": "REORDER_INDEPENDENT_TASKS",
            "parameters": {},
            "time_saved_days": 1.0,
            "unblocked_count": 0,
            "readiness_score_projected": 50.0,
            "feasibility_score": 0.90,
            "policy_compliance": True
        }
    ]

    rec = RecoveryOptimizer.optimize_recovery_strategy("emp-1", scenarios)
    assert rec["recommended_scenario_key"] == "scenario_a"
    assert rec["requires_approval"] is True
    assert rec["approval_level"] == "MANAGER"

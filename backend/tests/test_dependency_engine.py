from app.engine.dependency_engine import DependencyEngine

def test_cycle_detection():
    # A -> B -> C (No cycle)
    tasks = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
    deps = [
        {"task_id": "B", "depends_on_task_id": "A"},
        {"task_id": "C", "depends_on_task_id": "B"}
    ]
    has_cycle, _ = DependencyEngine.detect_cycles(tasks, deps)
    assert not has_cycle

    # A -> B -> C -> A (Has cycle!)
    deps_cycle = [
        {"task_id": "B", "depends_on_task_id": "A"},
        {"task_id": "C", "depends_on_task_id": "B"},
        {"task_id": "A", "depends_on_task_id": "C"}
    ]
    has_cycle, cycle_path = DependencyEngine.detect_cycles(tasks, deps_cycle)
    assert has_cycle

def test_upstream_and_downstream_traversal():
    tasks = [
        {"id": "t1", "name": "Identity Verification", "status": "Delayed"},
        {"id": "t2", "name": "System Account", "status": "Blocked"},
        {"id": "t3", "name": "Dev Setup", "status": "Blocked"},
        {"id": "t4", "name": "Laptop Allocation", "status": "Completed"}
    ]
    tasks_dict = {t["id"]: t for t in tasks}
    deps = [
        {"task_id": "t2", "depends_on_task_id": "t1"},
        {"task_id": "t3", "depends_on_task_id": "t2"},
        {"task_id": "t3", "depends_on_task_id": "t4"}
    ]

    # Downstream blast radius of t1
    affected = DependencyEngine.get_downstream_blast_radius("t1", tasks_dict, deps)
    affected_ids = [t["id"] for t in affected]
    assert "t2" in affected_ids
    assert "t3" in affected_ids
    assert len(affected_ids) == 2

    # Upstream blockers of t3
    blockers = DependencyEngine.get_upstream_blockers("t3", tasks_dict, deps)
    blocker_ids = [t["id"] for t in blockers]
    assert "t1" in blocker_ids
    assert "t2" in blocker_ids
    # t4 is Completed so it's not a blocker
    assert "t4" not in blocker_ids

def test_recalculate_task_statuses():
    tasks = [
        {"id": "t1", "name": "Task 1", "status": "Completed"},
        {"id": "t2", "name": "Task 2", "status": "Blocked"},
    ]
    deps = [
        {"task_id": "t2", "depends_on_task_id": "t1"}
    ]
    # Because t1 is completed, t2 should unblock to Pending
    updated = DependencyEngine.recalculate_task_statuses(tasks, deps)
    t2_updated = next(t for t in updated if t["id"] == "t2")
    assert t2_updated["status"] == "Pending"

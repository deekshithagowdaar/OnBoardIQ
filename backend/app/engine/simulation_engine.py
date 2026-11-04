from typing import List, Dict, Any, Optional
import copy
import uuid
from app.engine.dependency_engine import DependencyEngine
from app.engine.risk_engine import RiskEngine
from app.engine.readiness_engine import ReadinessEngine

class SimulationEngine:
    """
    Onboarding What-If Simulation Engine.
    Operates strictly on in-memory ephemeral copies of task graphs to evaluate hypothetical recovery options
    without mutating production database records.
    """

    @staticmethod
    def run_scenario(
        employee_id: str,
        tasks: List[Dict[str, Any]],
        dependencies: List[Dict[str, Any]],
        scenario_key: str,
        scenario_title: str,
        description: str,
        action_type: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulates a specific scenario on a cloned task list.
        """
        # Deep copy to ensure zero mutation of original records
        cloned_tasks = [copy.deepcopy(t) for t in tasks]
        tasks_dict = {t["id"]: t for t in cloned_tasks}

        # Baseline readiness before simulation
        baseline_readiness = ReadinessEngine.calculate_readiness(cloned_tasks)
        initially_blocked = set([t["id"] for t in cloned_tasks if t.get("status") in ("Blocked", "Delayed")])

        time_saved = 0.0
        policy_compliance = True
        feasibility_score = 1.0

        # Apply hypothetical mutations based on action_type
        if action_type == "PRIORITIZE_TASK":
            target_id = parameters.get("task_id")
            if target_id and target_id in tasks_dict:
                target = tasks_dict[target_id]
                target["status"] = "Completed"
                target["actual_completion_date"] = "Today (Simulated)"
                target["delay_reason"] = None
                time_saved += 2.5
                feasibility_score = 0.95

        elif action_type == "RESOURCE_REASSIGNMENT":
            target_id = parameters.get("task_id")
            new_assignee = parameters.get("new_assignee", "Marcus Chen (Senior DevOps Lead)")
            if target_id and target_id in tasks_dict:
                target = tasks_dict[target_id]
                target["assigned_person"] = new_assignee
                # Parallel staging allows unblocking technical tasks
                target["status"] = "Completed"
                target["actual_completion_date"] = "Today (Fast-Track)"
                target["delay_reason"] = None
                time_saved += 1.5
                feasibility_score = 0.85

        elif action_type == "REORDER_INDEPENDENT_TASKS":
            # Prioritize independent tasks (Payroll and Benefits)
            for t in cloned_tasks:
                if t.get("department") in ("Payroll", "Benefits") and t.get("status") in ("Pending", "In Progress"):
                    t["status"] = "Completed"
                    t["actual_completion_date"] = "Today (Prioritized)"
            time_saved += 1.0
            feasibility_score = 0.90

        # Recalculate graph statuses based on dependencies
        updated_tasks = DependencyEngine.recalculate_task_statuses(cloned_tasks, dependencies)

        # Detect newly unblocked tasks
        now_blocked = set([t["id"] for t in updated_tasks if t.get("status") in ("Blocked", "Delayed")])
        unblocked_ids = list(initially_blocked - now_blocked)

        # Calculate projected metrics
        projected_readiness = ReadinessEngine.calculate_readiness(updated_tasks)
        projected_risk = RiskEngine.calculate_employee_risk(updated_tasks, dependencies, "2026-11-20")

        return {
            "id": str(uuid.uuid4()),
            "employee_id": employee_id,
            "scenario_key": scenario_key,
            "scenario_title": scenario_title,
            "description": description,
            "action_type": action_type,
            "parameters": parameters,
            "unblocked_task_ids": unblocked_ids,
            "unblocked_count": len(unblocked_ids),
            "time_saved_days": round(time_saved, 1),
            "expected_completion_date": "On Time (Day-1 Ready)" if projected_risk["risk_category"] in ("Low", "Medium") else "Delayed by 1 day",
            "joining_date_risk": projected_risk["risk_category"],
            "readiness_score_projected": projected_readiness["overall_score"],
            "department_readiness": projected_readiness["department_scores"],
            "feasibility_score": feasibility_score,
            "policy_compliance": policy_compliance,
        }

    @staticmethod
    def simulate_all_recovery_scenarios(
        employee_id: str,
        tasks: List[Dict[str, Any]],
        dependencies: List[Dict[str, Any]],
        root_cause_task_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Runs standard Scenarios A, B, and C as required by the hackathon challenge.
        """
        tasks_dict = {t["id"]: t for t in tasks}
        
        # Identify Identity Verification task or root cause task
        identity_task_id = root_cause_task_id
        if not identity_task_id:
            for t in tasks:
                if "identity" in t.get("name", "").lower() or "verification" in t.get("name", "").lower():
                    identity_task_id = t["id"]
                    break
        if not identity_task_id and tasks:
            identity_task_id = tasks[0]["id"]

        # Identify IT task for Scenario B
        it_task_id = None
        for t in tasks:
            if t.get("department") == "IT" and t.get("status") in ("Blocked", "Delayed", "Pending"):
                it_task_id = t["id"]
                break
        if not it_task_id:
            it_task_id = identity_task_id

        # Scenario A: Expedited Identity Verification
        scenario_a = SimulationEngine.run_scenario(
            employee_id=employee_id,
            tasks=tasks,
            dependencies=dependencies,
            scenario_key="scenario_a",
            scenario_title="Scenario A: Expedited Identity Verification (Priority HR Review)",
            description="Escalate and complete Identity Verification today via dedicated HR priority queue. Unblocks IT System Account Creation and Dev Environment Setup directly.",
            action_type="PRIORITIZE_TASK",
            parameters={"task_id": identity_task_id}
        )

        # Scenario B: Fast-Track IT Provisioning with Level-2 Admin
        scenario_b = SimulationEngine.run_scenario(
            employee_id=employee_id,
            tasks=tasks,
            dependencies=dependencies,
            scenario_key="scenario_b",
            scenario_title="Scenario B: Assign Alternative Authorized IT Resource",
            description="Reassign IT provisioning to Marcus Chen (Level-2 Senior DevOps Engineer) to stage accounts in parallel while verification clears.",
            action_type="RESOURCE_REASSIGNMENT",
            parameters={"task_id": it_task_id, "new_assignee": "Marcus Chen (Senior DevOps Lead)"}
        )

        # Scenario C: Reorder Independent Tasks (Non-blocking Fast Path)
        scenario_c = SimulationEngine.run_scenario(
            employee_id=employee_id,
            tasks=tasks,
            dependencies=dependencies,
            scenario_key="scenario_c",
            scenario_title="Scenario C: Reorder Independent Tasks (Parallel Track)",
            description="Prioritize Payroll Direct Deposit, Benefits Health Enrollment, and Laptop Delivery in parallel while waiting for technical clearance.",
            action_type="REORDER_INDEPENDENT_TASKS",
            parameters={}
        )

        return [scenario_a, scenario_b, scenario_c]

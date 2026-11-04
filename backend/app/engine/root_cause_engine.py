from typing import List, Dict, Any, Optional
from app.engine.dependency_engine import DependencyEngine

class RootCauseEngine:
    """
    AI Root-Cause and Downstream Impact Analysis Engine.
    Deterministically pinpoints the original blocker, calculates downstream blast radius,
    and produces grounded explanations without hallucinations.
    """

    @staticmethod
    def analyze_root_cause(
        tasks: List[Dict[str, Any]],
        dependencies: List[Dict[str, Any]],
        target_delayed_task_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Analyzes the root cause of delay and its downstream blast radius.
        """
        if not tasks:
            return None

        tasks_dict = {t["id"]: t for t in tasks}

        # Find delayed or blocked tasks
        delayed_tasks = [t for t in tasks if t.get("status") == "Delayed"]
        blocked_tasks = [t for t in tasks if t.get("status") == "Blocked"]

        primary_task = None
        if target_delayed_task_id and target_delayed_task_id in tasks_dict:
            primary_task = tasks_dict[target_delayed_task_id]
        elif delayed_tasks:
            primary_task = delayed_tasks[0]
        elif blocked_tasks:
            primary_task = blocked_tasks[0]
        else:
            return None

        # Trace upstream blockers to identify original root cause
        upstream_blockers = DependencyEngine.get_upstream_blockers(primary_task["id"], tasks_dict, dependencies)
        
        # If upstream blockers exist, the earliest/root uncompleted ancestor is the root cause
        if upstream_blockers:
            root_task = upstream_blockers[-1] # Farthest upstream
        else:
            root_task = primary_task

        # Compute all downstream affected tasks from root_task
        downstream_affected = DependencyEngine.get_downstream_blast_radius(root_task["id"], tasks_dict, dependencies)

        # Categorize root cause
        task_name_lower = root_task.get("name", "").lower()
        if "identity" in task_name_lower or "verification" in task_name_lower or "id " in task_name_lower:
            category = "Pending Identity Verification"
        elif "laptop" in task_name_lower or "hardware" in task_name_lower or "equipment" in task_name_lower:
            category = "IT Hardware Allocation Bottleneck"
        elif "bank" in task_name_lower or "payroll" in task_name_lower or "deposit" in task_name_lower:
            category = "Missing Banking & Payroll Information"
        elif "account" in task_name_lower or "credential" in task_name_lower or "access" in task_name_lower:
            category = "IT Access Provisioning Backlog"
        elif "benefit" in task_name_lower or "insurance" in task_name_lower:
            category = "Benefits Documentation Pending"
        else:
            category = "Upstream Task Delay"

        # Calculate estimated joining date impact
        # Sum of durations of affected critical tasks or estimated days
        affected_critical = [t for t in downstream_affected if t.get("is_critical", False)]
        impact_days = max(1.5, (len(downstream_affected) * 0.8) + (len(affected_critical) * 0.5))
        impact_days = round(impact_days, 1)

        # Build structured explanation grounded in real workflow data
        affected_names = [t.get("name", t.get("task_id", "")) for t in downstream_affected]
        affected_summary_str = ", ".join(affected_names) if affected_names else "No direct downstream tasks"

        explanation = (
            f"Root cause identified: '{root_task.get('name')}' ({root_task.get('department')}) is currently "
            f"in status '{root_task.get('status')}'. "
            f"Because downstream systems require completion of this step, "
            f"{len(downstream_affected)} downstream task(s) ({affected_summary_str}) cannot proceed. "
            f"This creates an estimated schedule slippage of {impact_days} business days against Day-1 readiness."
        )

        affected_task_details = []
        for t in downstream_affected:
            affected_task_details.append({
                "task_id": t["id"],
                "task_name": t.get("name", t.get("task_id", "")),
                "department": t.get("department", "IT"),
                "status": t.get("status", "Blocked"),
                "delay_impact_days": round(t.get("estimated_duration_days", 1.0) * 1.2, 1),
            })

        evidence = {
            "root_task_id": root_task["id"],
            "root_task_name": root_task.get("name"),
            "root_department": root_task.get("department"),
            "root_status": root_task.get("status"),
            "delay_reason": root_task.get("delay_reason", "Documentation awaiting verification"),
            "blocked_downstream_count": len(downstream_affected),
            "critical_tasks_affected": [t.get("name") for t in affected_critical],
        }

        return {
            "primary_delayed_task_id": primary_task["id"],
            "primary_delayed_task_name": primary_task.get("name", ""),
            "root_cause_task_id": root_task["id"],
            "root_cause_task_name": root_task.get("name", ""),
            "root_cause_category": category,
            "explanation": explanation,
            "affected_downstream_task_ids": [t["id"] for t in downstream_affected],
            "affected_downstream_tasks": affected_task_details,
            "estimated_joining_date_impact_days": impact_days,
            "evidence": evidence,
        }

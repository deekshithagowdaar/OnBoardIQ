from typing import List, Dict, Any, Tuple
from collections import defaultdict

class ReadinessEngine:
    """
    Dynamic Onboarding Readiness Score Engine (0 to 100).
    Uses a transparent, explainable 4-factor formula:
      - 35% Completed Tasks Weight
      - 25% Critical Path Health (penalty if critical tasks are blocked/delayed)
      - 20% Department Parity (HR, IT, Payroll, Benefits)
      - 20% Timeline & Blocker Factor
    """

    @staticmethod
    def calculate_readiness(
        tasks: List[Dict[str, Any]],
        critical_path_task_ids: List[str] = None
    ) -> Dict[str, Any]:
        if not tasks:
            return {
                "overall_score": 0.0,
                "readiness_tier": "Not Ready",
                "department_scores": {"HR": 0.0, "IT": 0.0, "Payroll": 0.0, "Benefits": 0.0},
                "completed_tasks_count": 0,
                "total_tasks_count": 0,
                "blocked_tasks_count": 0,
                "critical_pending_count": 0,
                "days_until_joining": 5,
                "score_explanation": "No tasks present in onboarding plan.",
                "formula_breakdown": {},
                "critical_path_tasks": [],
            }

        total_tasks = len(tasks)
        completed_tasks = [t for t in tasks if t.get("status") == "Completed"]
        blocked_tasks = [t for t in tasks if t.get("status") in ("Blocked", "Delayed")]
        
        # Factor 1: Completed Task Ratio (0 - 100)
        completion_ratio = (len(completed_tasks) / total_tasks) * 100.0

        # Factor 2: Critical Path & Critical Task Health
        critical_tasks = [t for t in tasks if t.get("is_critical", False)]
        if critical_tasks:
            completed_crit = len([t for t in critical_tasks if t.get("status") == "Completed"])
            blocked_crit = len([t for t in critical_tasks if t.get("status") in ("Blocked", "Delayed")])
            crit_ratio = (completed_crit / len(critical_tasks)) * 100.0
            crit_penalty = min(50.0, blocked_crit * 25.0)
            critical_health = max(0.0, crit_ratio - crit_penalty)
        else:
            critical_health = completion_ratio

        # Factor 3: Department Parity
        dept_tasks = defaultdict(list)
        for t in tasks:
            dept_tasks[t.get("department", "HR")].append(t)

        dept_scores = {}
        for dept in ["HR", "IT", "Payroll", "Benefits"]:
            d_list = dept_tasks.get(dept, [])
            if not d_list:
                dept_scores[dept] = 100.0 if len(tasks) > 0 else 0.0
            else:
                d_done = len([t for t in d_list if t.get("status") == "Completed"])
                dept_scores[dept] = round((d_done / len(d_list)) * 100.0, 1)

        avg_dept_score = sum(dept_scores.values()) / max(1, len(dept_scores))

        # Factor 4: Timeline & Blocker Factor
        blocker_penalty = min(60.0, len(blocked_tasks) * 20.0)
        timeline_health = max(0.0, 100.0 - blocker_penalty)

        # Weighted calculation
        # 35% Task Completion + 25% Critical Health + 20% Dept Parity + 20% Timeline/Blocker
        overall_score = (
            (0.35 * completion_ratio) +
            (0.25 * critical_health) +
            (0.20 * avg_dept_score) +
            (0.20 * timeline_health)
        )
        overall_score = round(min(100.0, max(0.0, overall_score)), 1)

        # Tier classification
        if overall_score >= 90.0:
            tier = "Ready for Day 1"
        elif overall_score >= 75.0:
            tier = "On Track"
        elif overall_score >= 50.0:
            tier = "Needs Attention"
        else:
            tier = "Not Ready"

        # Critical path detail
        critical_path_info = []
        if critical_path_task_ids:
            tasks_dict = {t["id"]: t for t in tasks}
            for cid in critical_path_task_ids:
                if cid in tasks_dict:
                    ct = tasks_dict[cid]
                    critical_path_info.append({
                        "id": ct["id"],
                        "name": ct.get("name"),
                        "department": ct.get("department"),
                        "status": ct.get("status"),
                        "is_blocked": ct.get("status") in ("Blocked", "Delayed")
                    })

        explanation = (
            f"Readiness Score: {overall_score}% ({tier}). "
            f"Calculated from {len(completed_tasks)}/{total_tasks} completed tasks (35% weight: {round(completion_ratio*0.35,1)} pts), "
            f"Critical task health (25% weight: {round(critical_health*0.25,1)} pts), "
            f"Department completion balance (20% weight: {round(avg_dept_score*0.20,1)} pts), and "
            f"Blocker impact deduction ({len(blocked_tasks)} active blockers; 20% weight: {round(timeline_health*0.20,1)} pts)."
        )

        return {
            "overall_score": overall_score,
            "readiness_tier": tier,
            "department_scores": dept_scores,
            "completed_tasks_count": len(completed_tasks),
            "total_tasks_count": total_tasks,
            "blocked_tasks_count": len(blocked_tasks),
            "critical_pending_count": len([t for t in critical_tasks if t.get("status") != "Completed"]),
            "days_until_joining": 5,
            "score_explanation": explanation,
            "formula_breakdown": {
                "completion_ratio_component": round(completion_ratio * 0.35, 1),
                "critical_health_component": round(critical_health * 0.25, 1),
                "department_parity_component": round(avg_dept_score * 0.20, 1),
                "timeline_component": round(timeline_health * 0.20, 1),
            },
            "critical_path_tasks": critical_path_info,
        }

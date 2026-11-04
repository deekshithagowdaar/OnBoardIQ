from typing import List, Dict, Any, Tuple
from datetime import datetime, date

class RiskEngine:
    """
    Explainable Predictive Risk Engine for Onboarding Orchestration.
    Computes risk score (0-100), risk category, attention level, and explainable risk factors.
    """

    @staticmethod
    def calculate_employee_risk(
        tasks: List[Dict[str, Any]],
        dependencies: List[Dict[str, Any]],
        joining_date_str: str
    ) -> Dict[str, Any]:
        """
        Evaluates the risk of an employee's onboarding process.
        Returns risk scores, category, factors, predicted delay, and task risks.
        """
        if not tasks:
            return {
                "overall_risk_score": 0.0,
                "risk_category": "Low",
                "factors": ["No onboarding tasks assigned."],
                "predicted_delay_days": 0.0,
                "attention_level": "Normal",
                "task_risks": [],
            }

        # Calculate downstream counts
        downstream_counts = {}
        for t in tasks:
            downstream_counts[t["id"]] = 0
        for dep in dependencies:
            src = dep["depends_on_task_id"]
            downstream_counts[src] = downstream_counts.get(src, 0) + 1

        task_risks = []
        factors = []
        total_risk_accum = 0.0
        blocked_count = 0
        delayed_count = 0
        max_task_risk = 0.0
        total_predicted_delay = 0.0

        for t in tasks:
            status = t.get("status", "Pending")
            is_critical = t.get("is_critical", False)
            ds_count = downstream_counts.get(t["id"], 0)
            duration = t.get("estimated_duration_days", 1.0)
            
            reasons = []
            base_score = 0.0
            delay_prob = 0.0
            task_delay_impact = 0.0

            if status == "Completed":
                base_score = 0.0
                delay_prob = 0.0
            elif status == "Delayed":
                base_score = 85.0
                delay_prob = 0.95
                task_delay_impact = max(2.0, duration * 1.5)
                delayed_count += 1
                reasons.append(f"Task is explicitly delayed. Reason: {t.get('delay_reason', 'Unspecified bottleneck')}")
            elif status == "Blocked":
                base_score = 75.0
                delay_prob = 0.85
                task_delay_impact = max(1.5, duration)
                blocked_count += 1
                reasons.append(f"Task is blocked waiting for upstream dependencies: {t.get('delay_reason', 'Upstream dependency incomplete')}")
            elif status == "In Progress":
                base_score = 30.0
                delay_prob = 0.25
                reasons.append("Task is currently active.")
            else: # Pending
                base_score = 25.0
                delay_prob = 0.20
                reasons.append("Task has not started.")

            # Blast radius amplification
            if ds_count > 0 and status in ("Blocked", "Delayed", "Pending"):
                blast_penalty = min(20.0, ds_count * 5.0)
                base_score += blast_penalty
                reasons.append(f"Has {ds_count} downstream dependent task(s) directly waiting on completion.")

            # Critical path amplification
            if is_critical and status != "Completed":
                base_score += 15.0
                reasons.append("Task is marked as a critical Day-1 onboarding requirement.")

            task_score = min(100.0, base_score)
            max_task_risk = max(max_task_risk, task_score)
            total_risk_accum += task_score
            total_predicted_delay += task_delay_impact

            task_risks.append({
                "task_id": t["id"],
                "task_name": t.get("name", t.get("task_id", "")),
                "department": t.get("department", "HR"),
                "status": status,
                "risk_score": round(task_score, 1),
                "delay_probability": round(delay_prob, 2),
                "reasons": reasons,
            })

        # Calculate aggregate risk score
        # Weighted mix: 50% max task risk, 30% average risk, 20% blocked/delayed count factor
        avg_risk = total_risk_accum / len(tasks)
        blocker_factor = min(100.0, (blocked_count + delayed_count) * 20.0)
        overall_score = round(0.50 * max_task_risk + 0.30 * avg_risk + 0.20 * blocker_factor, 1)
        overall_score = min(100.0, max(0.0, overall_score))

        # Determine category & attention level
        if overall_score >= 75.0:
            category = "Critical"
            attention = "Immediate Action Required"
        elif overall_score >= 50.0:
            category = "High"
            attention = "Immediate Action Required"
        elif overall_score >= 25.0:
            category = "Medium"
            attention = "Monitor Closely"
        else:
            category = "Low"
            attention = "Normal"

        # Formulate human-readable factors
        if delayed_count > 0:
            factors.append(f"{delayed_count} task(s) are officially delayed, causing upstream stagnation.")
        if blocked_count > 0:
            factors.append(f"{blocked_count} downstream task(s) are actively blocked by unresolved prerequisites.")
        if max_task_risk >= 80.0:
            factors.append("At least one critical path task has an elevated risk score exceeding 80%.")
        if total_predicted_delay > 0:
            factors.append(f"Projected cumulative schedule slippage of {round(total_predicted_delay, 1)} business days.")
        if not factors:
            factors.append("All tasks are on track with normal progression.")

        return {
            "overall_risk_score": overall_score,
            "risk_category": category,
            "factors": factors,
            "predicted_delay_days": round(total_predicted_delay, 1),
            "attention_level": attention,
            "task_risks": task_risks,
        }

from typing import List, Dict, Any, Optional
import uuid

class RecoveryOptimizer:
    """
    Constraint-Aware Self-Healing Recovery Optimizer.
    Evaluates simulated scenarios against business rules, compliance policies,
    and efficiency criteria to recommend the optimal recovery strategy.
    """

    @staticmethod
    def optimize_recovery_strategy(
        employee_id: str,
        scenarios: List[Dict[str, Any]],
        employee_role: str = "Software Developer"
    ) -> Dict[str, Any]:
        """
        Ranks scenarios based on multi-criteria utility score:
          Utility = (0.35 * TimeSavedNormalized) +
                    (0.30 * TasksUnblockedNormalized) +
                    (0.20 * ReadinessDelta) +
                    (0.15 * PolicyFeasibility)
        """
        if not scenarios:
            return {}

        scored_scenarios = []
        for sc in scenarios:
            time_saved = sc.get("time_saved_days", 0.0)
            unblocked = sc.get("unblocked_count", 0)
            readiness = sc.get("readiness_score_projected", 0.0)
            feasibility = sc.get("feasibility_score", 1.0)
            compliant = sc.get("policy_compliance", True)

            # Normalizations (assuming max realistic time saved = 4 days, max unblocked = 4 tasks)
            norm_time = min(1.0, time_saved / 3.0)
            norm_unblocked = min(1.0, unblocked / 3.0)
            norm_readiness = readiness / 100.0

            policy_mult = 1.0 if compliant else 0.2

            score = (
                (0.35 * norm_time) +
                (0.30 * norm_unblocked) +
                (0.20 * norm_readiness) +
                (0.15 * feasibility)
            ) * policy_mult

            scored_scenarios.append({
                "scenario": sc,
                "score": round(score, 3)
            })

        # Sort descending by score
        scored_scenarios.sort(key=lambda x: x["score"], reverse=True)
        winner = scored_scenarios[0]["scenario"]

        # Compose explainable rationale
        if winner["scenario_key"] == "scenario_a":
            rationale = (
                f"Recommended: Scenario A ('{winner['scenario_title']}'). "
                f"This strategy directly addresses the root upstream bottleneck ('Identity Verification'), "
                f"immediately unblocking {winner['unblocked_count']} downstream technical task(s) including System Account Creation and Developer Environment Setup. "
                f"It delivers the highest timeline compression ({winner['time_saved_days']} days saved) and elevates the Onboarding Readiness Score "
                f"to {winner['readiness_score_projected']}% while strictly preserving 100% regulatory compliance."
            )
        elif winner["scenario_key"] == "scenario_b":
            rationale = (
                f"Recommended: Scenario B ('{winner['scenario_title']}'). "
                f"Assigning an authorized senior resource enables parallel account staging, saving {winner['time_saved_days']} days. "
                f"Approval is required to activate the staging clearance."
            )
        else:
            rationale = (
                f"Recommended: Scenario C ('{winner['scenario_title']}'). "
                f"Prioritizing independent tasks maintains momentum while waiting for upstream resolution, saving {winner['time_saved_days']} days."
            )

        comparison_summary = {
            "evaluated_scenarios_count": len(scenarios),
            "rankings": [
                {
                    "rank": idx + 1,
                    "scenario_key": item["scenario"]["scenario_key"],
                    "scenario_title": item["scenario"]["scenario_title"],
                    "utility_score": item["score"],
                    "unblocked_count": item["scenario"]["unblocked_count"],
                    "time_saved_days": item["scenario"]["time_saved_days"],
                    "projected_readiness": item["scenario"]["readiness_score_projected"],
                }
                for idx, item in enumerate(scored_scenarios)
            ]
        }

        return {
            "id": str(uuid.uuid4()),
            "employee_id": employee_id,
            "recommended_scenario_key": winner["scenario_key"],
            "strategy_title": winner["scenario_title"],
            "rationale": rationale,
            "action_type": winner["action_type"],
            "proposed_payload": winner["parameters"],
            "requires_approval": True,
            "approval_level": "MANAGER",
            "comparison_summary": comparison_summary,
        }

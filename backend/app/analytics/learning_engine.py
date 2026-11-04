from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.analytics import HistoricalOutcome
from collections import defaultdict

class LearningEngine:
    @staticmethod
    def get_analytics(db: Session) -> Dict[str, Any]:
        outcomes = db.query(HistoricalOutcome).order_by(HistoricalOutcome.completion_timestamp.desc()).all()
        
        total_outcomes = len(outcomes)
        if total_outcomes == 0:
            return {
                "total_completed_onboardings": 0,
                "bottlenecks": [],
                "recovery_strategies_performance": [],
                "prediction_accuracy_mae": 0.0,
                "prediction_vs_actual": [],
                "department_performance": [],
                "historical_outcomes": [],
            }

        # 1. Bottleneck Aggregation
        bottlenecks_map = defaultdict(lambda: {"count": 0, "total_delay": 0.0, "dept": ""})
        total_delays = 0
        for o in outcomes:
            key = f"{o.department}::{o.task_name}"
            bottlenecks_map[key]["count"] += 1
            bottlenecks_map[key]["total_delay"] += o.actual_delay_days
            bottlenecks_map[key]["dept"] = o.department
            total_delays += 1

        bottlenecks = []
        for key, val in bottlenecks_map.items():
            task_name = key.split("::")[1]
            bottlenecks.append({
                "department": val["dept"],
                "task_name": task_name,
                "delay_count": val["count"],
                "avg_delay_days": round(val["total_delay"] / val["count"], 1),
                "percentage_of_total_delays": round((val["count"] / max(1, total_delays)) * 100.0, 1),
            })
        bottlenecks.sort(key=lambda x: x["delay_count"], reverse=True)

        # 2. Recovery Strategy Performance
        strat_map = defaultdict(lambda: {"recs": 0, "approved": 0, "success": 0, "time_saved": 0.0})
        for o in outcomes:
            s_name = o.recovery_strategy_used
            strat_map[s_name]["recs"] += 1
            if o.was_approved:
                strat_map[s_name]["approved"] += 1
            if o.recovery_outcome == "Success":
                strat_map[s_name]["success"] += 1
            strat_map[s_name]["time_saved"] += o.time_saved_actual_days

        strategies = []
        for s_name, data in strat_map.items():
            strategies.append({
                "strategy_name": s_name,
                "times_recommended": data["recs"],
                "approval_rate": round((data["approved"] / data["recs"]) * 100.0, 1),
                "success_rate": round((data["success"] / data["recs"]) * 100.0, 1),
                "avg_days_saved": round(data["time_saved"] / max(1, data["success"]), 1),
            })

        # 3. Prediction Accuracy MAE
        abs_errors = [abs(o.predicted_delay_days - o.actual_delay_days) for o in outcomes]
        mae = sum(abs_errors) / len(abs_errors) if abs_errors else 0.0

        # 4. Prediction vs Actual Chart Points
        prediction_vs_actual = [
            {
                "task_name": o.task_name[:20],
                "predicted": round(o.predicted_delay_days, 1),
                "actual": round(o.actual_delay_days, 1),
                "time_saved": round(o.time_saved_actual_days, 1),
            }
            for o in outcomes[:15]
        ]

        # 5. Department Performance Trends
        dept_map = defaultdict(lambda: {"total": 0, "success": 0, "time_saved": 0.0})
        for o in outcomes:
            dept = o.department if o.department != "Cross-Department" else "HR"
            dept_map[dept]["total"] += 1
            if o.recovery_outcome == "Success":
                dept_map[dept]["success"] += 1
            dept_map[dept]["time_saved"] += o.time_saved_actual_days

        department_performance = [
            {
                "department": dept,
                "total_cases": data["total"],
                "success_rate": round((data["success"] / data["total"]) * 100.0, 1),
                "avg_recovery_days": round(data["time_saved"] / max(1, data["total"]), 1),
            }
            for dept, data in dept_map.items()
        ]

        return {
            "total_completed_onboardings": total_outcomes,
            "bottlenecks": bottlenecks[:5],
            "recovery_strategies_performance": strategies,
            "prediction_accuracy_mae": round(mae, 2),
            "prediction_vs_actual": prediction_vs_actual,
            "department_performance": department_performance,
            "historical_outcomes": outcomes[:50],
        }

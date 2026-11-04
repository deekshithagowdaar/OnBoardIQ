from typing import Dict, Any, List
import copy
from langgraph.graph import StateGraph, END
from app.orchestration.state import WorkflowState
from app.orchestration.agents import HRAgent, ITAgent, PayrollAgent, BenefitsAgent
from app.engine.dependency_engine import DependencyEngine
from app.engine.risk_engine import RiskEngine
from app.engine.root_cause_engine import RootCauseEngine
from app.engine.simulation_engine import SimulationEngine
from app.engine.recovery_optimizer import RecoveryOptimizer
from app.engine.readiness_engine import ReadinessEngine

def department_coordination_node(state: WorkflowState) -> WorkflowState:
    """Coordinates the 4 logical department agents."""
    tasks = state.get("tasks", [])
    hr_report = HRAgent.inspect(tasks)
    it_report = ITAgent.inspect(tasks, hr_report["status"])
    payroll_report = PayrollAgent.inspect(tasks)
    benefits_report = BenefitsAgent.inspect(tasks)

    messages = state.get("messages", [])
    messages.append(f"Department Coordination completed. HR: {hr_report['status']}, IT: {it_report['status']}.")

    return {
        **state,
        "department_statuses": {
            "HR": hr_report,
            "IT": it_report,
            "Payroll": payroll_report,
            "Benefits": benefits_report,
        },
        "messages": messages,
    }

def dependency_monitoring_node(state: WorkflowState) -> WorkflowState:
    """Updates blocked states and dependency graph."""
    tasks = state.get("tasks", [])
    deps = state.get("dependencies", [])

    recalculated_tasks = DependencyEngine.recalculate_task_statuses(tasks, deps)
    messages = state.get("messages", [])
    messages.append("Dependency engine evaluated task graph and recalculated blocked states.")

    return {
        **state,
        "tasks": recalculated_tasks,
        "messages": messages,
    }

def risk_analysis_node(state: WorkflowState) -> WorkflowState:
    """Evaluates predictive delays and risk scores."""
    tasks = state.get("tasks", [])
    deps = state.get("dependencies", [])
    joining_date = state.get("employee_data", {}).get("joining_date", "2026-11-20")

    risk_info = RiskEngine.calculate_employee_risk(tasks, deps, joining_date)
    messages = state.get("messages", [])
    messages.append(f"Risk analysis complete: Risk Score {risk_info['overall_risk_score']} ({risk_info['risk_category']}).")

    return {
        **state,
        "risk_info": risk_info,
        "messages": messages,
    }

def root_cause_analysis_node(state: WorkflowState) -> WorkflowState:
    """Traces upstream blockers and downstream blast radius."""
    tasks = state.get("tasks", [])
    deps = state.get("dependencies", [])

    root_cause = RootCauseEngine.analyze_root_cause(tasks, deps)
    messages = state.get("messages", [])
    if root_cause:
        messages.append(f"Root cause identified: {root_cause['root_cause_task_name']} ({root_cause['root_cause_category']}).")

    return {
        **state,
        "root_cause": root_cause,
        "messages": messages,
    }

def simulation_and_optimization_node(state: WorkflowState) -> WorkflowState:
    """Runs What-If simulations and selects the optimal recovery plan."""
    tasks = state.get("tasks", [])
    deps = state.get("dependencies", [])
    root_cause = state.get("root_cause")
    root_task_id = root_cause["root_cause_task_id"] if root_cause else None

    # Simulate Scenarios A, B, C
    scenarios = SimulationEngine.simulate_all_recovery_scenarios(
        employee_id=state.get("employee_id", "EMP-001"),
        tasks=tasks,
        dependencies=deps,
        root_cause_task_id=root_task_id
    )

    # Recovery Optimization
    recommendation = RecoveryOptimizer.optimize_recovery_strategy(
        employee_id=state.get("employee_id", "EMP-001"),
        scenarios=scenarios,
        employee_role=state.get("employee_data", {}).get("job_role", "Software Developer")
    )

    messages = state.get("messages", [])
    messages.append(f"What-If simulator evaluated {len(scenarios)} recovery scenarios. Recommended: {recommendation.get('strategy_title')}.")

    return {
        **state,
        "simulation_results": scenarios,
        "recommendation": recommendation,
        "approval_status": "PENDING" if recommendation.get("requires_approval") else "NOT_REQUIRED",
        "messages": messages,
    }

def readiness_evaluation_node(state: WorkflowState) -> WorkflowState:
    """Computes final onboarding readiness score."""
    tasks = state.get("tasks", [])
    deps = state.get("dependencies", [])
    crit_path = DependencyEngine.compute_critical_path(tasks, deps)

    readiness = ReadinessEngine.calculate_readiness(tasks, crit_path)

    return {
        **state,
        "readiness_score": readiness["overall_score"],
        "readiness_details": readiness,
    }

# Build LangGraph StateGraph
def build_onboarding_graph() -> StateGraph:
    builder = StateGraph(WorkflowState)

    builder.add_node("department_coordination", department_coordination_node)
    builder.add_node("dependency_monitoring", dependency_monitoring_node)
    builder.add_node("risk_analysis", risk_analysis_node)
    builder.add_node("root_cause_analysis", root_cause_analysis_node)
    builder.add_node("simulation_and_optimization", simulation_and_optimization_node)
    builder.add_node("readiness_evaluation", readiness_evaluation_node)

    builder.set_entry_point("department_coordination")
    builder.add_edge("department_coordination", "dependency_monitoring")
    builder.add_edge("dependency_monitoring", "risk_analysis")
    builder.add_edge("risk_analysis", "root_cause_analysis")
    builder.add_edge("root_cause_analysis", "simulation_and_optimization")
    builder.add_edge("simulation_and_optimization", "readiness_evaluation")
    builder.add_edge("readiness_evaluation", END)

    return builder.compile()

onboarding_graph = build_onboarding_graph()

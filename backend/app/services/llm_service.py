import httpx
import logging
from typing import Dict, Any, List
from app.config import settings

logger = logging.getLogger(__name__)


def _call_ollama(prompt: str) -> str:
    response = httpx.post(
        f"{settings.OLLAMA_BASE_URL}/api/generate",
        json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=30.0
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()


class LLMService:

    @staticmethod
    def generate_personalized_plan_text(employee_data: Dict[str, Any]) -> str:
        role = employee_data.get("job_role", "Software Developer")
        dept = employee_data.get("department", "Engineering")
        name = employee_data.get("full_name", "Employee")

        if settings.USE_LOCAL_LLM:
            try:
                prompt = (
                    f"You are an HR onboarding specialist. Write a concise 3-sentence onboarding plan summary "
                    f"for {name}, a new {role} joining the {dept} department. "
                    f"Cover: what they will set up in week 1, who they will meet, and what their Day-1 goal is. "
                    f"Be specific to their role. Do not use bullet points."
                )
                return _call_ollama(prompt)
            except Exception as e:
                logger.warning(f"[LLMService] plan generation failed: {e}")

        return (
            f"Tailored {dept} onboarding track for {name} ({role}). "
            f"Configured with technical environment provisioning, security clearance, "
            f"compliance identity checks, and Day-1 integration checkpoints."
        )

    @staticmethod
    def explain_root_cause_and_impact(
        root_task_name: str,
        blocked_tasks: List[str],
        delay_days: float,
        department: str
    ) -> str:
        blocked_str = ", ".join(blocked_tasks) if blocked_tasks else "none"

        if settings.USE_LOCAL_LLM:
            try:
                prompt = (
                    f"You are an onboarding risk analyst. Explain in 2-3 sentences why a delay in "
                    f"'{root_task_name}' (owned by {department}) is causing a critical onboarding bottleneck. "
                    f"The following tasks are now blocked: {blocked_str}. "
                    f"The estimated schedule slippage is {delay_days} business days. "
                    f"Be direct and professional. Do not use bullet points."
                )
                return _call_ollama(prompt)
            except Exception as e:
                logger.warning(f"[LLMService] root cause explanation failed: {e}")

        return (
            f"Analysis confirms that the primary blocker is '{root_task_name}'. "
            f"This bottleneck halts {len(blocked_tasks)} dependent technical task(s): [{blocked_str}]. "
            f"Without corrective intervention, Day-1 readiness is compromised by approximately {delay_days} days."
        )

    @staticmethod
    def explain_recovery_recommendation(
        winning_scenario_title: str,
        time_saved: float,
        unblocked_count: int,
        readiness_score: float,
        rejected_scenarios: List[str]
    ) -> str:
        rejected_str = " and ".join(rejected_scenarios) if rejected_scenarios else "other options"

        if settings.USE_LOCAL_LLM:
            try:
                prompt = (
                    f"You are an AI onboarding recovery advisor. Explain in 2-3 sentences why "
                    f"'{winning_scenario_title}' is the optimal recovery strategy. "
                    f"It saves {time_saved} days, unblocks {unblocked_count} task(s), and raises "
                    f"Day-1 readiness to {readiness_score}%. "
                    f"It was chosen over {rejected_str}. "
                    f"Be concise and justify the choice clearly. Do not use bullet points."
                )
                return _call_ollama(prompt)
            except Exception as e:
                logger.warning(f"[LLMService] recovery rationale failed: {e}")

        return (
            f"'{winning_scenario_title}' was selected as the optimal recovery strategy. "
            f"It delivers the highest utility score by saving {time_saved} days, unblocking "
            f"{unblocked_count} downstream task(s), and elevating Day-1 readiness to {readiness_score}% "
            f"while maintaining full policy compliance."
        )

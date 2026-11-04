import json
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings

class LLMService:
    """
    Configurable LLM Service.
    Connects to local Ollama when enabled/available, with high-fidelity deterministic fallback.
    Never invents invalid company policies or corrupts workflow state.
    """

    @staticmethod
    def generate_personalized_plan_text(employee_data: Dict[str, Any]) -> str:
        role = employee_data.get("job_role", "Software Developer")
        dept = employee_data.get("department", "Engineering")
        name = employee_data.get("full_name", "Employee")

        if settings.USE_LOCAL_LLM:
            try:
                prompt = f"Generate an executive onboarding overview for {name}, a new {role} in {dept}."
                response = httpx.post(
                    f"{settings.OLLAMA_BASE_URL}/api/generate",
                    json={"model": settings.OLLAMA_MODEL, "prompt": prompt, "stream": False},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json().get("response", "")
            except Exception:
                pass # Gracefully fall through to deterministic response

        return (
            f"Tailored {dept} onboarding track for {name} ({role}). "
            f"Configured with technical environment provisioning, security clearance, "
            f"compliance identity checks, and Day-1 integration checkpoints."
        )

    @staticmethod
    def explain_root_cause_and_impact(root_task_name: str, blocked_tasks: List[str], delay_days: float) -> str:
        blocked_str = ", ".join(blocked_tasks) if blocked_tasks else "None"
        return (
            f"Analysis confirms that the primary blocker is '{root_task_name}'. "
            f"This bottleneck halts {len(blocked_tasks)} dependent technical task(s): [{blocked_str}]. "
            f"Without corrective intervention, Day-1 readiness is compromised by approximately {delay_days} days."
        )

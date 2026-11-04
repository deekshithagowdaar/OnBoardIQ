from typing import List, Dict, Any

class HRAgent:
    """HR Department Agent - Responsible for documentation, identity verification, compliance."""
    name = "HR Agent"

    @staticmethod
    def inspect(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        hr_tasks = [t for t in tasks if t.get("department") == "HR"]
        completed = [t for t in hr_tasks if t.get("status") == "Completed"]
        delayed = [t for t in hr_tasks if t.get("status") in ("Delayed", "Blocked")]

        alerts = []
        status = "HEALTHY"

        for t in delayed:
            status = "ATTENTION_REQUIRED"
            alerts.append(f"Task '{t.get('name')}' is {t.get('status')}: {t.get('delay_reason', 'Awaiting verification')}")

        return {
            "agent": "HR Agent",
            "department": "HR",
            "total_tasks": len(hr_tasks),
            "completed_tasks": len(completed),
            "delayed_tasks": len(delayed),
            "status": status,
            "alerts": alerts,
            "recommendations": ["Prioritize Identity Verification via HR Fast-Track queue"] if delayed else []
        }

class ITAgent:
    """IT Department Agent - Responsible for system accounts, credentials, laptops, dev environment."""
    name = "IT Agent"

    @staticmethod
    def inspect(tasks: List[Dict[str, Any]], hr_status: str) -> Dict[str, Any]:
        it_tasks = [t for t in tasks if t.get("department") == "IT"]
        completed = [t for t in it_tasks if t.get("status") == "Completed"]
        blocked = [t for t in it_tasks if t.get("status") in ("Blocked", "Delayed")]

        alerts = []
        status = "HEALTHY"

        if blocked:
            status = "BLOCKED"
            for t in blocked:
                alerts.append(f"IT Task '{t.get('name')}' cannot proceed due to upstream blockage.")

        return {
            "agent": "IT Agent",
            "department": "IT",
            "total_tasks": len(it_tasks),
            "completed_tasks": len(completed),
            "blocked_tasks": len(blocked),
            "status": status,
            "alerts": alerts,
            "recommendations": ["Stage sandbox environment in parallel under Marcus Chen"] if blocked else []
        }

class PayrollAgent:
    """Payroll Department Agent - Responsible for banking, salary, tax setup."""
    name = "Payroll Agent"

    @staticmethod
    def inspect(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        payroll_tasks = [t for t in tasks if t.get("department") == "Payroll"]
        completed = [t for t in payroll_tasks if t.get("status") == "Completed"]
        pending = [t for t in payroll_tasks if t.get("status") in ("Pending", "In Progress")]

        return {
            "agent": "Payroll Agent",
            "department": "Payroll",
            "total_tasks": len(payroll_tasks),
            "completed_tasks": len(completed),
            "pending_tasks": len(pending),
            "status": "HEALTHY" if not pending else "IN_PROGRESS",
            "alerts": [],
            "recommendations": ["Process direct deposit in parallel"] if pending else []
        }

class BenefitsAgent:
    """Benefits Department Agent - Responsible for health coverage, retirement, perks."""
    name = "Benefits Agent"

    @staticmethod
    def inspect(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        benefits_tasks = [t for t in tasks if t.get("department") == "Benefits"]
        completed = [t for t in benefits_tasks if t.get("status") == "Completed"]
        pending = [t for t in benefits_tasks if t.get("status") in ("Pending", "In Progress")]

        return {
            "agent": "Benefits Agent",
            "department": "Benefits",
            "total_tasks": len(benefits_tasks),
            "completed_tasks": len(completed),
            "pending_tasks": len(pending),
            "status": "HEALTHY" if not pending else "IN_PROGRESS",
            "alerts": [],
            "recommendations": []
        }

from typing import Dict, Any
import datetime

class MockHRSystem:
    """Mock HRIS Department Integration (Clearly labeled as mock for Dayforce Hackathon)"""

    @staticmethod
    def verify_identity(employee_id: str, document_type: str = "Government ID") -> Dict[str, Any]:
        return {
            "system": "Mock Dayforce HRIS Gateway",
            "action": "IDENTITY_VERIFICATION",
            "employee_id": employee_id,
            "status": "VERIFIED",
            "verification_id": f"VER-HR-{employee_id[-4:]}",
            "verified_at": datetime.datetime.utcnow().isoformat(),
            "notes": "Fast-track digital identity verification confirmed via authorized HR reviewer."
        }

class MockITSystem:
    """Mock IT Access & Provisioning Gateway"""

    @staticmethod
    def provision_system_account(employee_id: str, role: str) -> Dict[str, Any]:
        return {
            "system": "Mock Dayforce IT Directory Gateway",
            "action": "ACCOUNT_PROVISION",
            "employee_id": employee_id,
            "status": "ACTIVE",
            "directory_dn": f"CN={employee_id},OU=Developers,DC=corp,DC=internal",
            "sso_email_created": True,
            "provisioned_at": datetime.datetime.utcnow().isoformat()
        }

    @staticmethod
    def reassign_it_resource(task_id: str, new_assignee: str) -> Dict[str, Any]:
        return {
            "system": "Mock IT Ticket Management",
            "action": "RESOURCE_REASSIGNMENT",
            "task_id": task_id,
            "assigned_to": new_assignee,
            "sla_tier": "P1_PRIORITY",
            "reassigned_at": datetime.datetime.utcnow().isoformat()
        }

class MockPayrollSystem:
    """Mock Payroll & Banking Integration"""

    @staticmethod
    def submit_direct_deposit(employee_id: str) -> Dict[str, Any]:
        return {
            "system": "Mock Dayforce Payroll Gateway",
            "action": "DIRECT_DEPOSIT_SETUP",
            "employee_id": employee_id,
            "status": "CONFIRMED",
            "cleared_at": datetime.datetime.utcnow().isoformat()
        }

class MockBenefitsSystem:
    """Mock Benefits & Healthcare Enrollment Integration"""

    @staticmethod
    def enroll_benefits(employee_id: str) -> Dict[str, Any]:
        return {
            "system": "Mock Dayforce Benefits Gateway",
            "action": "BENEFITS_ENROLLMENT",
            "employee_id": employee_id,
            "status": "ENROLLED",
            "effective_date": "Day 1 of Employment"
        }

from fastapi import APIRouter
from app.integrations.mock_apis import MockHRSystem, MockITSystem, MockPayrollSystem, MockBenefitsSystem

router = APIRouter(prefix="/mock", tags=["Mock Department Integrations (Dayforce Hackathon)"])

@router.post("/hr/verify-identity")
def mock_hr_verify(employee_id: str, document_type: str = "Government ID"):
    return MockHRSystem.verify_identity(employee_id, document_type)

@router.post("/it/provision-account")
def mock_it_provision(employee_id: str, role: str = "Developer"):
    return MockITSystem.provision_system_account(employee_id, role)

@router.post("/it/reassign-resource")
def mock_it_reassign(task_id: str, new_assignee: str):
    return MockITSystem.reassign_it_resource(task_id, new_assignee)

@router.post("/payroll/direct-deposit")
def mock_payroll_deposit(employee_id: str):
    return MockPayrollSystem.submit_direct_deposit(employee_id)

@router.post("/benefits/enroll")
def mock_benefits_enroll(employee_id: str):
    return MockBenefitsSystem.enroll_benefits(employee_id)

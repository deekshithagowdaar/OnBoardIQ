from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class DepartmentBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    head_of_department: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    department: Optional[str] = None

class UserResponse(UserBase):
    created_at: datetime
    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    employee_id: str
    full_name: str
    email: str
    department: str
    job_role: str
    employment_type: str = "Full-time"
    work_location: str = "Remote"
    joining_date: str # YYYY-MM-DD
    reporting_manager: str
    experience_level: str = "Mid-level"
    required_equipment: List[str] = []
    applicable_requirements: List[str] = []

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    job_role: Optional[str] = None
    employment_type: Optional[str] = None
    work_location: Optional[str] = None
    joining_date: Optional[str] = None
    reporting_manager: Optional[str] = None
    experience_level: Optional[str] = None
    required_equipment: Optional[List[str]] = None
    applicable_requirements: Optional[List[str]] = None
    status: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class OnboardingPlanResponse(BaseModel):
    id: str
    employee_id: str
    title: str
    plan_summary: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

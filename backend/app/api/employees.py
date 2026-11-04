from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.employee_service import EmployeeService
from app.schemas.employee import EmployeeResponse, EmployeeCreate, EmployeeUpdate, OnboardingPlanResponse

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("", response_model=List[EmployeeResponse])
def get_employees(
    search: Optional[str] = Query(None, description="Search by name, ID or role"),
    department: Optional[str] = Query(None, description="Filter by department"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    return EmployeeService.get_employees(db, search=search, department=department, status=status)

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: str, db: Session = Depends(get_db)):
    emp = EmployeeService.get_employee_by_id(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(emp_in: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return EmployeeService.create_employee(db, emp_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: str, emp_in: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = EmployeeService.update_employee(db, employee_id, emp_in)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.post("/{employee_id}/generate-plan", response_model=OnboardingPlanResponse)
def generate_onboarding_plan(employee_id: str, db: Session = Depends(get_db)):
    try:
        return EmployeeService.generate_personalized_plan(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

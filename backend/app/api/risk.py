import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.employee import Employee
from app.models.task import Task
from app.models.risk import RiskPrediction
from app.services.task_service import TaskService
from app.engine.risk_engine import RiskEngine
from app.schemas.risk import RiskPredictionResponse

router = APIRouter(prefix="/risk", tags=["Risk Analysis"])

@router.get("/{employee_id}", response_model=RiskPredictionResponse)
def get_employee_risk(employee_id: str, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        # Check by employee_id field
        emp = db.query(Employee).filter(Employee.employee_id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    tasks = TaskService.get_employee_tasks(db, emp.id)
    deps = TaskService.get_dependencies_for_employee(db, emp.id)

    task_dicts = [
        {
            "id": t.id,
            "task_id": t.task_id,
            "name": t.name,
            "department": t.department,
            "status": t.status,
            "priority": t.priority,
            "estimated_duration_days": t.estimated_duration_days,
            "is_critical": t.is_critical,
            "delay_reason": t.delay_reason,
        }
        for t in tasks
    ]

    risk_data = RiskEngine.calculate_employee_risk(task_dicts, deps, emp.joining_date)

    prediction = RiskPrediction(
        id=str(uuid.uuid4()),
        employee_id=emp.id,
        overall_risk_score=risk_data["overall_risk_score"],
        risk_category=risk_data["risk_category"],
        factors=risk_data["factors"],
        predicted_delay_days=risk_data["predicted_delay_days"],
        attention_level=risk_data["attention_level"],
        task_risks=risk_data["task_risks"],
    )
    db.add(prediction)
    db.commit()

    return {
        "id": prediction.id,
        "employee_id": emp.id,
        "overall_risk_score": risk_data["overall_risk_score"],
        "risk_category": risk_data["risk_category"],
        "factors": risk_data["factors"],
        "predicted_delay_days": risk_data["predicted_delay_days"],
        "attention_level": risk_data["attention_level"],
        "task_risks": risk_data["task_risks"],
        "created_at": prediction.created_at or datetime.datetime.utcnow(),
    }

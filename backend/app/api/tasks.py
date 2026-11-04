from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate, TaskDependencyCreate, TaskDependencyResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/employee/{employee_id}", response_model=List[TaskResponse])
def get_employee_tasks(employee_id: str, db: Session = Depends(get_db)):
    tasks = TaskService.get_employee_tasks(db, employee_id)
    deps = TaskService.get_dependencies_for_employee(db, employee_id)

    # Attach upstreams & downstreams
    upstream_map = {}
    downstream_map = {}
    for t in tasks:
        upstream_map[t.id] = []
        downstream_map[t.id] = []

    for d in deps:
        if d["task_id"] in upstream_map:
            upstream_map[d["task_id"]].append(d["depends_on_task_id"])
        if d["depends_on_task_id"] in downstream_map:
            downstream_map[d["depends_on_task_id"]].append(d["task_id"])

    res = []
    for t in tasks:
        t_dict = {
            "id": t.id,
            "employee_id": t.employee_id,
            "task_id": t.task_id,
            "name": t.name,
            "description": t.description,
            "department": t.department,
            "assigned_person": t.assigned_person,
            "priority": t.priority,
            "start_date": t.start_date,
            "due_date": t.due_date,
            "estimated_duration_days": t.estimated_duration_days,
            "actual_completion_date": t.actual_completion_date,
            "status": t.status,
            "requires_approval": t.requires_approval,
            "is_critical": t.is_critical,
            "delay_reason": t.delay_reason,
            "category": t.category,
            "upstream_dependencies": upstream_map.get(t.id, []),
            "downstream_tasks": downstream_map.get(t.id, []),
            "created_at": t.created_at,
            "updated_at": t.updated_at,
        }
        res.append(t_dict)
    return res

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    task = TaskService.create_task(db, task_in)
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_in: TaskUpdate, db: Session = Depends(get_db)):
    task = TaskService.update_task(db, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/dependencies", response_model=TaskDependencyResponse, status_code=201)
def add_task_dependency(dep_in: TaskDependencyCreate, db: Session = Depends(get_db)):
    try:
        return TaskService.add_dependency(db, dep_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

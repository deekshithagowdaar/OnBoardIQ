from typing import List, Dict, Any, Optional
import uuid
from sqlalchemy.orm import Session
from app.models.task import Task, TaskDependency
from app.models.approval import AuditLog
from app.engine.dependency_engine import DependencyEngine
from app.schemas.task import TaskCreate, TaskUpdate, TaskDependencyCreate

class TaskService:
    @staticmethod
    def get_employee_tasks(db: Session, employee_id: str) -> List[Task]:
        return db.query(Task).filter(Task.employee_id == employee_id).all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: str) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def get_dependencies_for_employee(db: Session, employee_id: str) -> List[Dict[str, Any]]:
        tasks = db.query(Task).filter(Task.employee_id == employee_id).all()
        task_ids = [t.id for t in tasks]
        if not task_ids:
            return []
        deps = db.query(TaskDependency).filter(TaskDependency.task_id.in_(task_ids)).all()
        return [
            {
                "id": d.id,
                "task_id": d.task_id,
                "depends_on_task_id": d.depends_on_task_id,
                "dependency_type": d.dependency_type
            }
            for d in deps
        ]

    @staticmethod
    def create_task(db: Session, task_in: TaskCreate) -> Task:
        new_id = str(uuid.uuid4())
        task = Task(
            id=new_id,
            employee_id=task_in.employee_id,
            task_id=task_in.task_id,
            name=task_in.name,
            description=task_in.description,
            department=task_in.department,
            assigned_person=task_in.assigned_person,
            priority=task_in.priority,
            start_date=task_in.start_date,
            due_date=task_in.due_date,
            estimated_duration_days=task_in.estimated_duration_days,
            status=task_in.status,
            requires_approval=task_in.requires_approval,
            is_critical=task_in.is_critical,
            category=task_in.category,
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        # Add upstream dependencies if provided
        if task_in.upstream_dependencies:
            for dep_id in task_in.upstream_dependencies:
                dep_record = TaskDependency(
                    id=str(uuid.uuid4()),
                    task_id=task.id,
                    depends_on_task_id=dep_id,
                    dependency_type="Finish-to-Start"
                )
                db.add(dep_record)
            db.commit()

        # Audit log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="TASK",
            entity_id=task.id,
            action="CREATE",
            actor="System",
            details={"name": task.name, "department": task.department}
        )
        db.add(audit)
        db.commit()

        return task

    @staticmethod
    def update_task(db: Session, task_id: str, task_update: TaskUpdate, actor: str = "User") -> Optional[Task]:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)

        # Recalculate downstream statuses
        TaskService.recalculate_and_sync_statuses(db, task.employee_id)

        # Audit log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="TASK",
            entity_id=task.id,
            action="UPDATE",
            actor=actor,
            details=update_data
        )
        db.add(audit)
        db.commit()

        return task

    @staticmethod
    def add_dependency(db: Session, dep_in: TaskDependencyCreate) -> TaskDependency:
        # Check cycle detection
        task = db.query(Task).filter(Task.id == dep_in.task_id).first()
        if not task:
            raise ValueError("Downstream task not found")
        
        all_tasks = db.query(Task).filter(Task.employee_id == task.employee_id).all()
        existing_deps = TaskService.get_dependencies_for_employee(db, task.employee_id)
        
        # Test addition for cycle
        hypothetical_deps = existing_deps + [{
            "id": "test",
            "task_id": dep_in.task_id,
            "depends_on_task_id": dep_in.depends_on_task_id,
        }]
        tasks_dicts = [{"id": t.id} for t in all_tasks]
        has_cycle, _ = DependencyEngine.detect_cycles(tasks_dicts, hypothetical_deps)
        if has_cycle:
            raise ValueError("Adding this dependency would introduce a circular dependency cycle!")

        dep = TaskDependency(
            id=str(uuid.uuid4()),
            task_id=dep_in.task_id,
            depends_on_task_id=dep_in.depends_on_task_id,
            dependency_type=dep_in.dependency_type
        )
        db.add(dep)
        db.commit()
        db.refresh(dep)

        TaskService.recalculate_and_sync_statuses(db, task.employee_id)
        return dep

    @staticmethod
    def recalculate_and_sync_statuses(db: Session, employee_id: str):
        tasks = db.query(Task).filter(Task.employee_id == employee_id).all()
        deps = TaskService.get_dependencies_for_employee(db, employee_id)

        task_dicts = [
            {
                "id": t.id,
                "task_id": t.task_id,
                "name": t.name,
                "status": t.status,
                "delay_reason": t.delay_reason,
                "estimated_duration_days": t.estimated_duration_days,
                "is_critical": t.is_critical,
                "department": t.department,
            }
            for t in tasks
        ]

        recalculated = DependencyEngine.recalculate_task_statuses(task_dicts, deps)
        recalculated_map = {t["id"]: t for t in recalculated}

        for t in tasks:
            new_info = recalculated_map.get(t.id)
            if new_info and t.status != "Completed":
                t.status = new_info["status"]
                t.delay_reason = new_info.get("delay_reason")

        db.commit()

    @staticmethod
    def get_dependency_graph(db: Session, employee_id: str) -> Dict[str, Any]:
        tasks = db.query(Task).filter(Task.employee_id == employee_id).all()
        deps = TaskService.get_dependencies_for_employee(db, employee_id)

        task_dicts = [
            {
                "id": t.id,
                "task_id": t.task_id,
                "name": t.name,
                "description": t.description,
                "department": t.department,
                "status": t.status,
                "priority": t.priority,
                "assigned_person": t.assigned_person,
                "due_date": t.due_date,
                "estimated_duration_days": t.estimated_duration_days,
                "is_critical": t.is_critical,
                "delay_reason": t.delay_reason,
            }
            for t in tasks
        ]

        return DependencyEngine.build_react_flow_elements(employee_id, task_dicts, deps)

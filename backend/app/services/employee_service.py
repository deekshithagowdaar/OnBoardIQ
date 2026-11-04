from typing import List, Dict, Any, Optional
import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.employee import Employee, OnboardingPlan
from app.models.task import Task, TaskDependency
from app.models.approval import AuditLog
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.llm_service import LLMService

class EmployeeService:
    @staticmethod
    def get_employees(
        db: Session,
        search: Optional[str] = None,
        department: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Employee]:
        query = db.query(Employee)
        if search:
            search_filter = or_(
                Employee.full_name.ilike(f"%{search}%"),
                Employee.employee_id.ilike(f"%{search}%"),
                Employee.job_role.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        if department:
            query = query.filter(Employee.department == department)
        if status:
            query = query.filter(Employee.status == status)
        return query.order_by(Employee.created_at.desc()).all()

    @staticmethod
    def get_employee_by_id(db: Session, employee_id: str) -> Optional[Employee]:
        return db.query(Employee).filter(
            or_(Employee.id == employee_id, Employee.employee_id == employee_id)
        ).first()

    @staticmethod
    def create_employee(db: Session, employee_in: EmployeeCreate) -> Employee:
        new_id = str(uuid.uuid4())
        emp = Employee(
            id=new_id,
            employee_id=employee_in.employee_id,
            full_name=employee_in.full_name,
            email=employee_in.email,
            department=employee_in.department,
            job_role=employee_in.job_role,
            employment_type=employee_in.employment_type,
            work_location=employee_in.work_location,
            joining_date=employee_in.joining_date,
            reporting_manager=employee_in.reporting_manager,
            experience_level=employee_in.experience_level,
            required_equipment=employee_in.required_equipment,
            applicable_requirements=employee_in.applicable_requirements,
            status="Onboarding"
        )
        db.add(emp)
        db.commit()
        db.refresh(emp)

        # Automatically generate personalized onboarding plan
        EmployeeService.generate_personalized_plan(db, emp.id)

        # Audit log
        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="EMPLOYEE",
            entity_id=emp.id,
            action="CREATE",
            actor="HR Administrator",
            details={"name": emp.full_name, "role": emp.job_role}
        )
        db.add(audit)
        db.commit()

        return emp

    @staticmethod
    def update_employee(db: Session, employee_id: str, employee_update: EmployeeUpdate) -> Optional[Employee]:
        emp = EmployeeService.get_employee_by_id(db, employee_id)
        if not emp:
            return None

        update_data = employee_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(emp, key, value)

        db.commit()
        db.refresh(emp)

        audit = AuditLog(
            id=str(uuid.uuid4()),
            entity_type="EMPLOYEE",
            entity_id=emp.id,
            action="UPDATE",
            actor="HR Administrator",
            details=update_data
        )
        db.add(audit)
        db.commit()

        return emp

    @staticmethod
    def generate_personalized_plan(db: Session, employee_id: str) -> OnboardingPlan:
        emp = db.query(Employee).filter(
            or_(Employee.id == employee_id, Employee.employee_id == employee_id)
        ).first()
        if not emp:
            raise ValueError(f"Employee {employee_id} not found")

        # Delete existing plan tasks for clean generation if regeneration requested
        existing_tasks = db.query(Task).filter(Task.employee_id == emp.id).all()
        for t in existing_tasks:
            db.delete(t)
        db.commit()

        plan_title = f"{emp.department} Onboarding Track - {emp.job_role}"
        summary = LLMService.generate_personalized_plan_text({
            "full_name": emp.full_name,
            "job_role": emp.job_role,
            "department": emp.department
        })

        plan = db.query(OnboardingPlan).filter(OnboardingPlan.employee_id == emp.id).first()
        if not plan:
            plan = OnboardingPlan(
                id=str(uuid.uuid4()),
                employee_id=emp.id,
                title=plan_title,
                plan_summary=summary,
                status="Active"
            )
            db.add(plan)
        else:
            plan.title = plan_title
            plan.plan_summary = summary
        db.commit()

        # Generate Tasks tailored to Role & Department
        created_tasks = {}

        # 1. Identity Verification (HR)
        # Note: If this is the main demo employee Alex Morgan, initialize as Delayed to demonstrate the orchestrator!
        is_demo_alex = "alex" in emp.full_name.lower() or "001" in emp.employee_id
        t1_status = "Delayed" if is_demo_alex else "Completed"
        t1_reason = "Pending passport scan re-submission by employee" if is_demo_alex else None

        t1 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-HR-001",
            name="Identity Verification",
            description="Verify employee government-issued identification documents and I-9 compliance.",
            department="HR",
            assigned_person="Karen Vance (HR Compliance Lead)",
            priority="Critical",
            start_date="2026-11-01",
            due_date="2026-11-03",
            estimated_duration_days=1.0,
            status=t1_status,
            requires_approval=True,
            is_critical=True,
            delay_reason=t1_reason,
            category="Compliance"
        )
        db.add(t1)
        created_tasks["identity_verification"] = t1

        # 2. Employee Documentation (HR)
        t2 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-HR-002",
            name="Employee Documentation & NDA",
            description="Countersign offer letter, confidentiality agreement, and employee handbook.",
            department="HR",
            assigned_person="Karen Vance (HR Compliance Lead)",
            priority="Medium",
            start_date="2026-11-01",
            due_date="2026-11-04",
            estimated_duration_days=1.0,
            status="Completed",
            actual_completion_date="2026-11-02",
            requires_approval=False,
            is_critical=False,
            category="Documentation"
        )
        db.add(t2)
        created_tasks["documentation"] = t2

        # 3. System Account Creation (IT)
        # Blocked by Identity Verification
        t3_status = "Blocked" if is_demo_alex else "Completed"
        t3 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-IT-001",
            name="System Account Creation",
            description="Provision Dayforce SSO credentials, corporate email, and Okta multi-factor authentication.",
            department="IT",
            assigned_person="David Miller (IT Operations Specialist)",
            priority="High",
            start_date="2026-11-04",
            due_date="2026-11-06",
            estimated_duration_days=1.5,
            status=t3_status,
            requires_approval=False,
            is_critical=True,
            delay_reason="Blocked by uncompleted upstream task: Identity Verification" if is_demo_alex else None,
            category="Identity & Access"
        )
        db.add(t3)
        created_tasks["system_account"] = t3

        # 4. Laptop Allocation (IT)
        t4 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-IT-002",
            name="Laptop & Hardware Allocation",
            description=f"Configure and ship equipment: {', '.join(emp.required_equipment or ['MacBook Pro M3'])}.",
            department="IT",
            assigned_person="Rachel Green (IT Logistics)",
            priority="High",
            start_date="2026-11-02",
            due_date="2026-11-07",
            estimated_duration_days=2.0,
            status="Completed" if not is_demo_alex else "In Progress",
            requires_approval=False,
            is_critical=True,
            category="Hardware"
        )
        db.add(t4)
        created_tasks["laptop_allocation"] = t4

        # 5. Developer Environment Setup (IT)
        # Blocked by System Account and Laptop Allocation
        t5_status = "Blocked" if is_demo_alex else "Completed"
        t5 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-IT-003",
            name="Developer Environment Setup",
            description="Configure GitHub Enterprise permissions, AWS sandbox access, VPN client, and Docker tooling.",
            department="IT",
            assigned_person="Marcus Chen (Senior DevOps Lead)",
            priority="Critical",
            start_date="2026-11-06",
            due_date="2026-11-08",
            estimated_duration_days=1.5,
            status=t5_status,
            requires_approval=False,
            is_critical=True,
            delay_reason="Blocked by uncompleted upstream tasks: System Account Creation, Laptop & Hardware Allocation" if is_demo_alex else None,
            category="Development"
        )
        db.add(t5)
        created_tasks["dev_env"] = t5

        # 6. Bank Details Submission (Payroll)
        t6 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-PAY-001",
            name="Bank Details Submission",
            description="Collect direct deposit void check, routing number, and tax withholding form (W-4).",
            department="Payroll",
            assigned_person="Sandra Lopez (Payroll Coordinator)",
            priority="Medium",
            start_date="2026-11-02",
            due_date="2026-11-05",
            estimated_duration_days=1.0,
            status="Completed",
            actual_completion_date="2026-11-03",
            requires_approval=False,
            is_critical=False,
            category="Payroll"
        )
        db.add(t6)
        created_tasks["bank_details"] = t6

        # 7. Payroll Registration (Payroll)
        t7 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-PAY-002",
            name="Payroll Registration",
            description="Enroll employee in automated bi-weekly payroll cycle with verified tax deductions.",
            department="Payroll",
            assigned_person="Sandra Lopez (Payroll Coordinator)",
            priority="High",
            start_date="2026-11-05",
            due_date="2026-11-07",
            estimated_duration_days=1.0,
            status="In Progress" if is_demo_alex else "Completed",
            requires_approval=False,
            is_critical=True,
            category="Payroll"
        )
        db.add(t7)
        created_tasks["payroll_reg"] = t7

        # 8. Benefits Enrollment (Benefits)
        t8 = Task(
            id=str(uuid.uuid4()),
            employee_id=emp.id,
            task_id=f"TASK-BEN-001",
            name="Benefits Enrollment",
            description="Elect medical, dental, vision, and 401(k) matching coverage options.",
            department="Benefits",
            assigned_person="Elena Rostova (Benefits Specialist)",
            priority="Medium",
            start_date="2026-11-03",
            due_date="2026-11-08",
            estimated_duration_days=2.0,
            status="In Progress" if is_demo_alex else "Completed",
            requires_approval=False,
            is_critical=False,
            category="Benefits"
        )
        db.add(t8)
        created_tasks["benefits_enroll"] = t8

        db.commit()

        # Configure Dependencies:
        # 1. Identity Verification -> System Account Creation
        dep1 = TaskDependency(
            id=str(uuid.uuid4()),
            task_id=created_tasks["system_account"].id,
            depends_on_task_id=created_tasks["identity_verification"].id,
            dependency_type="Finish-to-Start"
        )
        db.add(dep1)

        # 2. System Account Creation -> Dev Environment Setup
        dep2 = TaskDependency(
            id=str(uuid.uuid4()),
            task_id=created_tasks["dev_env"].id,
            depends_on_task_id=created_tasks["system_account"].id,
            dependency_type="Finish-to-Start"
        )
        db.add(dep2)

        # 3. Laptop Allocation -> Dev Environment Setup
        dep3 = TaskDependency(
            id=str(uuid.uuid4()),
            task_id=created_tasks["dev_env"].id,
            depends_on_task_id=created_tasks["laptop_allocation"].id,
            dependency_type="Finish-to-Start"
        )
        db.add(dep3)

        # 4. Bank Details Submission -> Payroll Registration
        dep4 = TaskDependency(
            id=str(uuid.uuid4()),
            task_id=created_tasks["payroll_reg"].id,
            depends_on_task_id=created_tasks["bank_details"].id,
            dependency_type="Finish-to-Start"
        )
        db.add(dep4)

        db.commit()
        return plan

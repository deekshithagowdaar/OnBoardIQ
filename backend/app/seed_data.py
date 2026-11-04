import uuid
import datetime
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.employee import Department, User, Employee
from app.models.analytics import HistoricalOutcome
from app.services.employee_service import EmployeeService

def init_db(target_engine=None):
    Base.metadata.create_all(bind=target_engine or engine)

def seed_demo_data(target_db: Session = None):
    db = target_db or SessionLocal()
    should_close = target_db is None
    try:
        # Check if already seeded
        if db.query(Employee).filter(Employee.employee_id == "EMP-2024-001").first():
            print("Database already contains seed demo data.")
            return

        # 1. Departments
        depts = [
            Department(id="dept-eng", name="Engineering", description="Software development and platform architecture", head_of_department="Sarah Johnson"),
            Department(id="dept-hr", name="Human Resources", description="People operations and compliance", head_of_department="Karen Vance"),
            Department(id="dept-it", name="Information Technology", description="Infrastructure, access and security", head_of_department="David Miller"),
            Department(id="dept-fin", name="Finance & Payroll", description="Corporate accounting, payroll and tax", head_of_department="Sandra Lopez"),
            Department(id="dept-prod", name="Product Management", description="Product strategy and UX design", head_of_department="Elena Rostova"),
            Department(id="dept-sales", name="Sales & Go-to-Market", description="Enterprise revenue and partnerships", head_of_department="Michael Scott"),
        ]
        for d in depts:
            if not db.query(Department).filter(Department.id == d.id).first():
                db.add(d)
        db.commit()

        # 2. Users (Roles: HR_ADMIN, MANAGER, DEPARTMENT_USER)
        users = [
            User(id="user-1", username="sarah.johnson", email="sarah.johnson@dayforce-demo.com", full_name="Sarah Johnson", role="MANAGER", department="Engineering"),
            User(id="user-2", username="karen.vance", email="karen.vance@dayforce-demo.com", full_name="Karen Vance", role="HR_ADMIN", department="Human Resources"),
            User(id="user-3", username="david.miller", email="david.miller@dayforce-demo.com", full_name="David Miller", role="IT_ADMIN", department="Information Technology"),
            User(id="user-4", username="alex.morgan", email="alex.morgan@dayforce-demo.com", full_name="Alex Morgan", role="DEPARTMENT_USER", department="Engineering"),
        ]
        for u in users:
            if not db.query(User).filter(User.username == u.username).first():
                db.add(u)
        db.commit()

        # 3. Main Demo Employee: Alex Morgan (Software Developer, Engineering)
        alex = Employee(
            id="emp-alex-001",
            employee_id="EMP-2024-001",
            full_name="Alex Morgan",
            email="alex.morgan@dayforce-demo.com",
            department="Engineering",
            job_role="Software Developer",
            employment_type="Full-time",
            work_location="Hybrid - New York HQ",
            joining_date="2026-11-20",
            reporting_manager="Sarah Johnson",
            experience_level="Senior",
            required_equipment=["MacBook Pro 16 M3 Max", "2x Dell UltraSharp 4K", "YubiKey 5C NFC", "CalDigit TS4 Dock"],
            applicable_requirements=["I-9 Verification", "Criminal Background Check", "Developer IP Agreement", "Direct Deposit Form"],
            status="At Risk"
        )
        db.add(alex)
        db.commit()
        # Generate personalized plan for Alex with the exact delayed scenario
        EmployeeService.generate_personalized_plan(db, alex.id)

        # 4. Secondary Demo Employee: Priya Sharma (Product Manager, Product)
        priya = Employee(
            id="emp-priya-002",
            employee_id="EMP-2024-002",
            full_name="Priya Sharma",
            email="priya.sharma@dayforce-demo.com",
            department="Product",
            job_role="Senior Product Manager",
            employment_type="Full-time",
            work_location="Remote - US",
            joining_date="2026-11-25",
            reporting_manager="Elena Rostova",
            experience_level="Lead",
            required_equipment=["MacBook Air 15 M3", "Dell 34 Curved Monitor", "YubiKey 5C"],
            applicable_requirements=["I-9 Verification", "Standard NDA", "Direct Deposit Form"],
            status="Onboarding"
        )
        db.add(priya)
        db.commit()
        EmployeeService.generate_personalized_plan(db, priya.id)

        # 5. Third Demo Employee: Marcus Vance (Account Executive, Sales)
        marcus = Employee(
            id="emp-marcus-003",
            employee_id="EMP-2024-003",
            full_name="Marcus Vance",
            email="marcus.vance@dayforce-demo.com",
            department="Sales",
            job_role="Enterprise Account Executive",
            employment_type="Full-time",
            work_location="On-site - San Francisco",
            joining_date="2026-12-01",
            reporting_manager="Michael Scott",
            experience_level="Senior",
            required_equipment=["ThinkPad X1 Carbon", "Logitech Wireless Headset"],
            applicable_requirements=["I-9 Verification", "Sales Incentive Plan", "Direct Deposit Form"],
            status="Ready"
        )
        db.add(marcus)
        db.commit()
        EmployeeService.generate_personalized_plan(db, marcus.id)

        # 6. Seed Historical Outcomes for Continuous Learning Analytics
        historical_samples = [
            ("Engineering", "Identity Verification", 3.0, 3.2, "Pending Identity Verification", "Expedited Identity Verification (Priority HR Review)", True, "Success", 2.8),
            ("Engineering", "System Account Creation", 2.0, 1.8, "IT Access Provisioning Backlog", "Assign Alternative Authorized IT Resource", True, "Success", 1.5),
            ("Engineering", "Developer Environment Setup", 2.5, 2.0, "IT Hardware Allocation Bottleneck", "Assign Alternative Authorized IT Resource", True, "Success", 1.8),
            ("Sales", "CRM Access Setup", 1.5, 1.0, "Delayed Manager Approval", "Reorder Independent Tasks (Parallel Track)", True, "Success", 1.0),
            ("Finance", "Direct Deposit Setup", 2.0, 2.5, "Missing Banking & Payroll Information", "Reorder Independent Tasks (Parallel Track)", True, "Partial", 0.8),
            ("Product", "Figma & Jira License Allocation", 1.0, 0.8, "IT Access Provisioning Backlog", "Assign Alternative Authorized IT Resource", True, "Success", 1.2),
            ("Human Resources", "Benefits Enrollment", 1.5, 1.4, "Benefits Documentation Pending", "Reorder Independent Tasks (Parallel Track)", True, "Success", 1.0),
            ("Engineering", "Identity Verification", 3.5, 3.8, "Pending Identity Verification", "Expedited Identity Verification (Priority HR Review)", True, "Success", 3.0),
            ("Sales", "Laptop Delivery", 2.0, 1.5, "IT Hardware Allocation Bottleneck", "Assign Alternative Authorized IT Resource", True, "Success", 1.5),
            ("Engineering", "AWS Sandbox Provisioning", 2.0, 2.2, "IT Access Provisioning Backlog", "Assign Alternative Authorized IT Resource", True, "Success", 1.7),
            ("Product", "Identity Verification", 2.5, 2.8, "Pending Identity Verification", "Expedited Identity Verification (Priority HR Review)", True, "Success", 2.2),
            ("Finance", "Tax Compliance Review", 1.5, 1.2, "Compliance & Background Check Stalled", "Reorder Independent Tasks (Parallel Track)", True, "Success", 1.1),
        ]

        for dept, t_name, p_delay, a_delay, rc, strat, app, outcome, saved in historical_samples:
            ho = HistoricalOutcome(
                id=str(uuid.uuid4()),
                employee_id=f"HIST-{dept[:3].upper()}-{uuid.uuid4().hex[:4]}",
                department=dept,
                task_id=f"HIST-TASK-{uuid.uuid4().hex[:4]}",
                task_name=t_name,
                predicted_delay_days=p_delay,
                actual_delay_days=a_delay,
                root_cause_category=rc,
                recovery_strategy_used=strat,
                was_approved=app,
                recovery_outcome=outcome,
                time_saved_actual_days=saved,
                completion_timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=int(p_delay * 5)),
                is_synthetic_seed=True
            )
            db.add(ho)

        db.commit()
        print("Demo seed data successfully populated!")
    finally:
        if should_close:
            db.close()

if __name__ == "__main__":
    init_db()
    seed_demo_data()

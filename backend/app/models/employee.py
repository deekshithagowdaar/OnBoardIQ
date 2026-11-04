import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    head_of_department = Column(String(100), nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    full_name = Column(String(150), nullable=False)
    role = Column(String(50), nullable=False, default="DEPARTMENT_USER") # HR_ADMIN, MANAGER, DEPARTMENT_USER
    department = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    full_name = Column(String(150), nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False)
    department = Column(String(100), nullable=False, index=True)
    job_role = Column(String(150), nullable=False)
    employment_type = Column(String(50), nullable=False, default="Full-time") # Full-time, Contractor, Intern
    work_location = Column(String(100), nullable=False, default="Remote")
    joining_date = Column(String(50), nullable=False) # ISO Date string YYYY-MM-DD
    reporting_manager = Column(String(150), nullable=False)
    experience_level = Column(String(50), nullable=False, default="Mid-level") # Junior, Mid-level, Senior, Lead
    required_equipment = Column(JSON, default=list) # List of equipment strings
    applicable_requirements = Column(JSON, default=list) # List of compliance requirements
    status = Column(String(50), default="Onboarding") # Onboarding, At Risk, Ready, Completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="employee", cascade="all, delete-orphan")
    plans = relationship("OnboardingPlan", back_populates="employee", cascade="all, delete-orphan")
    approval_requests = relationship("ApprovalRequest", back_populates="employee", cascade="all, delete-orphan")
    readiness_snapshots = relationship("ReadinessSnapshot", back_populates="employee", cascade="all, delete-orphan")

class OnboardingPlan(Base):
    __tablename__ = "onboarding_plans"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    plan_summary = Column(Text, nullable=True)
    status = Column(String(50), default="Active") # Active, Archived
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    employee = relationship("Employee", back_populates="plans")

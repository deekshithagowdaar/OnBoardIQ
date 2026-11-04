import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(50), primary_key=True)
    employee_id = Column(String(50), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    task_id = Column(String(50), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    department = Column(String(50), nullable=False, index=True) # HR, IT, Payroll, Benefits
    assigned_person = Column(String(150), nullable=False)
    priority = Column(String(50), nullable=False, default="Medium") # Low, Medium, High, Critical
    start_date = Column(String(50), nullable=False)
    due_date = Column(String(50), nullable=False)
    estimated_duration_days = Column(Float, default=1.0)
    actual_completion_date = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False, default="Pending") # Pending, In Progress, Completed, Blocked, Delayed
    requires_approval = Column(Boolean, default=False)
    is_critical = Column(Boolean, default=False)
    delay_reason = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    employee = relationship("Employee", back_populates="tasks")

class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id = Column(String(50), primary_key=True)
    task_id = Column(String(50), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True) # Downstream task
    depends_on_task_id = Column(String(50), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False, index=True) # Upstream task
    dependency_type = Column(String(50), default="Finish-to-Start")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

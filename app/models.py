from sqlalchemy import Column, String, DateTime, Enum, Index
from sqlalchemy.dialects.postgresql import UUID, JSON
from app.database import Base
from sqlalchemy.sql import func
from enum import Enum as PyEnum
import uuid


class TaskStatus(PyEnum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("idx_status", "status"),
        Index("idx_priority", "priority"),
        Index("idx_due_date", "due_date"),
        Index("idx_created_at", "created_at"),
    )
    id = Column(UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4, index=True)
    title = Column(String(120), nullable=False)
    description = Column(String(2000), nullable=True)
    status = Column(Enum(TaskStatus, name="task_status"),
                    nullable=False, default=TaskStatus.TODO)
    priority = Column(Enum(Priority, name="priority"),
                      nullable=False, default=Priority.LOW)
    due_date = Column(DateTime, nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now(), nullable=False)

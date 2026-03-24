from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskUpdate
from app.crud import create_task, get_task, get_all_tasks, update_task, delete_task
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from app.core.exceptions import AppException
router = APIRouter()


@router.get("/health")
def get_health():
    return {"status": "ok"}


@router.post("/tasks", status_code=201)
def create_task_route(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = create_task(db, task)
    return new_task


@router.get("/tasks/{task_id}")
def get_task_by_id(task_id: UUID, db: Session = Depends(get_db)):
    task = get_task(db, task_id)
    if not task:
        raise AppException(
            code="NOT_FOUND",
            message="Task not found",
            status_code=404
        )
    return task


@router.get("/tasks")
def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[datetime] = None,
    due_after: Optional[datetime] = None,
    tag: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    db: Session = Depends(get_db)
):
    tasks = get_all_tasks(db, status, priority, due_before,
                          due_after, tag, page, page_size, sort_by, sort_order)
    return tasks


@router.patch("/tasks/{task_id}")
def update_task_by_id(task_id: UUID, task: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = update_task(db, task_id, task)
    if not updated_task:
        raise AppException(
            code="NOT_FOUND",
            message="Task not found",
            status_code=404
        )
    return updated_task


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task_by_id(task_id, db: Session = Depends(get_db)):
    deleted_task = delete_task(db, task_id)
    if not deleted_task:
        raise AppException(
            code="NOT_FOUND",
            message="Task not found",
            status_code=404
        )
    return

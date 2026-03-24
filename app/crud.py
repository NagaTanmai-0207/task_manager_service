from app.models import Task, TaskStatus, Priority
from app.schemas import TaskCreate
from sqlalchemy import cast, asc, desc
from sqlalchemy.dialects.postgresql import JSONB


def create_task(db, task: TaskCreate):
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        tags=task.tags
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task(db, task_id):
    task = db.query(Task).filter(Task.id == task_id).first()
    return task


def get_all_tasks(db, status=None,
                  priority=None,
                  due_before=None,
                  due_after=None,
                  tag=None,
                  page=1,
                  page_size=10,
                  sort_by="created_at",
                  sort_order="asc"):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == TaskStatus(status))

    if priority:
        query = query.filter(Task.priority == Priority(priority))
    if due_before:
        query = query.filter(Task.due_date < due_before)
    if due_after:
        query = query.filter(Task.due_date > due_after)
    if tag:
        query = query.filter(cast(Task.tags, JSONB).contains([tag]))
    allowed_sort_fields = {
        "created_at": Task.created_at,
        "updated_at": Task.updated_at,
        "due_date": Task.due_date,
        "priority": Task.priority
    }

    sort_column = allowed_sort_fields.get(sort_by, Task.created_at)

    if sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    total_items = query.count()
    page_size = min(page_size, 10)
    skip = (page-1)*page_size
    items = query.offset(skip).limit(page_size).all()
    total_pages = (total_items+page_size-1)
    return {
        "items": items,
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages
    }


def update_task(db, task_id, task_data):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.tags is not None:
        task.tags = task_data.tags
    db.commit()
    db.refresh(task)
    return task


def delete_task(db, task_id):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    db.delete(task)
    db.commit()

    return task

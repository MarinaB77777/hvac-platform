# backend/app/api/manager_tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.manager_task import ManagerTask
from app.schemas.manager_task import (
    ManagerTaskCreate,
    ManagerTaskHvacUpdate,
    ManagerTaskManagerUpdate,
    ManagerTaskOut,
)

router = APIRouter(prefix="/manager-tasks", tags=["manager_tasks"])


# =========================================================
# ✅ HVAC: только свои задачи
# =========================================================
@router.get("/my", response_model=list[ManagerTaskOut])
def list_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can view own tasks")

    return (
        db.query(ManagerTask)
        .filter(ManagerTask.hvac_id == current_user.id)
        .order_by(ManagerTask.id.desc())
        .all()
    )


# =========================================================
# ✅ MANAGER: задачи выбранного мастера
# =========================================================
@router.get("/by-hvac/{hvac_id}", response_model=list[ManagerTaskOut])
def list_tasks_by_hvac(
    hvac_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can view tasks")

    if not current_user.organization:
        return []

    hvac_user = db.query(User).filter(User.id == hvac_id).first()
    if not hvac_user:
        raise HTTPException(status_code=404, detail="HVAC not found")

    if hvac_user.role != "hvac":
        raise HTTPException(status_code=400, detail="Selected user is not HVAC")

    if hvac_user.organization != current_user.organization:
        raise HTTPException(status_code=403, detail="Not your organization")

    return (
        db.query(ManagerTask)
        .filter(ManagerTask.hvac_id == hvac_id)
        .filter(ManagerTask.organization == current_user.organization)
        .order_by(ManagerTask.id.desc())
        .all()
    )


# =========================================================
# ✅ MANAGER: создать задачу
# =========================================================
@router.post("/", response_model=ManagerTaskOut, status_code=201)
def create_manager_task(
    payload: ManagerTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can create tasks")

    if not current_user.organization:
        raise HTTPException(status_code=400, detail="Manager has no organization")

    hvac_user = db.query(User).filter(User.id == payload.hvac_id).first()
    if not hvac_user:
        raise HTTPException(status_code=404, detail="HVAC not found")

    if hvac_user.role != "hvac":
        raise HTTPException(status_code=400, detail="Selected user is not HVAC")

    if hvac_user.organization != current_user.organization:
        raise HTTPException(status_code=403, detail="You can assign tasks only inside your organization")

    title = (payload.title or "").strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title is required")

    task = ManagerTask(
        organization=current_user.organization,
        manager_id=current_user.id,
        hvac_id=payload.hvac_id,
        title=title,
        description=(payload.description.strip() if payload.description else None),
        due_datetime=payload.due_datetime,
        materials_note=(payload.materials_note.strip() if payload.materials_note else None),
        status="new",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

# =========================================================
# ✅ HVAC: update own task (report files / comment / missing items)
# =========================================================
@router.patch("/{task_id}/hvac", response_model=ManagerTaskOut)
def update_my_task(
    task_id: int,
    payload: ManagerTaskHvacUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can update own tasks")

    task = db.query(ManagerTask).filter(ManagerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.hvac_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")

    if payload.result_files is not None:
        task.result_files = payload.result_files

    if payload.hvac_comment is not None:
        task.hvac_comment = payload.hvac_comment.strip() if payload.hvac_comment else None

    if payload.materials_note is not None:
        task.materials_note = payload.materials_note.strip() if payload.materials_note else None

    db.commit()
    db.refresh(task)
    return task


# =========================================================
# ✅ MANAGER: review task and update final status
# =========================================================
@router.patch("/{task_id}/manager", response_model=ManagerTaskOut)
def update_task_by_manager(
    task_id: int,
    payload: ManagerTaskManagerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can update tasks")

    task = db.query(ManagerTask).filter(ManagerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.organization != current_user.organization:
        raise HTTPException(status_code=403, detail="Not your organization")

    if payload.status not in ["done", "needs_rework"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    task.status = payload.status

    if payload.manager_comment is not None:
        task.manager_comment = payload.manager_comment.strip() if payload.manager_comment else None

    db.commit()
    db.refresh(task)
    return task

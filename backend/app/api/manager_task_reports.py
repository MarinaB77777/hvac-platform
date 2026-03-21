from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.auth import get_current_user
from app.models.user import User
from app.models.manager_task import ManagerTask
from app.models.manager_task_report import ManagerTaskReport
from app.schemas.manager_task_report import (
    ManagerTaskReportCreate,
    ManagerTaskReportOut,
)

router = APIRouter(prefix="/manager-task-reports", tags=["manager_task_reports"])


# =========================================================
# ✅ HVAC: создать новый отчет (итерация)
# =========================================================
@router.post("/", response_model=ManagerTaskReportOut, status_code=201)
def create_report(
    payload: ManagerTaskReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "hvac":
        raise HTTPException(status_code=403, detail="Only HVAC can create reports")

    task = db.query(ManagerTask).filter(ManagerTask.id == payload.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.hvac_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")

    report = ManagerTaskReport(
        task_id=payload.task_id,
        hvac_id=current_user.id,
        result_files=payload.result_files,
        hvac_comment=payload.hvac_comment,
        materials_note=payload.materials_note,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


# =========================================================
# ✅ получить все отчеты по задаче
# =========================================================
@router.get("/task/{task_id}", response_model=list[ManagerTaskReportOut])
def get_reports_by_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(ManagerTask).filter(ManagerTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # доступ только участникам
    if current_user.role == "hvac" and task.hvac_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your task")

    if current_user.role == "manager" and task.organization != current_user.organization:
        raise HTTPException(status_code=403, detail="Not your organization")

    return (
        db.query(ManagerTaskReport)
        .filter(ManagerTaskReport.task_id == task_id)
        .order_by(ManagerTaskReport.id.asc())
        .all()
    )

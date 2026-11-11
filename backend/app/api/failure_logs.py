
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.failure_log import (
    FailureLogCreate,
    FailureLogResponse,
)
from app.services import failure_log_service


router = APIRouter(
    prefix="/failure-logs",
    tags=["Failure Logs"],
)


@router.post(
    "/",
    response_model=FailureLogResponse,
    status_code=201,
)
def create_log(
    data: FailureLogCreate,
    db: Session = Depends(get_db),
):
    try:
        return failure_log_service.create_failure_log(
            db,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/",
    response_model=list[FailureLogResponse],
)
def list_logs(
    workflow_run_id: int,
    db: Session = Depends(get_db),
):
    return failure_log_service.list_failure_logs(
        db,
        workflow_run_id,
    )

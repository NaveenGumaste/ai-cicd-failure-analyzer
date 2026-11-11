
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.workflow_run import (
    WorkflowRunCreate,
    WorkflowRunResponse,
)
from app.services import workflow_run_service


router = APIRouter(
    prefix="/workflow-runs",
    tags=["Workflow Runs"],
)


@router.post(
    "/",
    response_model=WorkflowRunResponse,
    status_code=201,
)
def create_workflow(
    data: WorkflowRunCreate,
    db: Session = Depends(get_db),
):
    try:
        return workflow_run_service.create_workflow_run(
            db,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Workflow run already exists.",
        )


@router.get(
    "/",
    response_model=list[WorkflowRunResponse],
)
def list_workflows(
    repository_id: int | None = Query(default=None, gt=0),
    conclusion: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return workflow_run_service.list_workflow_runs(
        db,
        repository_id=repository_id,
        conclusion=conclusion,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{run_id}",
    response_model=WorkflowRunResponse,
)
def get_workflow(
    run_id: int,
    db: Session = Depends(get_db),
):
    workflow = workflow_run_service.get_workflow_run(
        db,
        run_id,
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow run not found.",
        )

    return workflow

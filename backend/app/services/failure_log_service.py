
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.failure_log import FailureLog
from app.models.workflow_run import WorkflowRun
from app.schemas.failure_log import FailureLogCreate


def create_failure_log(
    db: Session,
    data: FailureLogCreate,
) -> FailureLog:

    workflow_run = db.get(
        WorkflowRun,
        data.workflow_run_id,
    )

    if workflow_run is None:
        raise ValueError("Workflow run not found.")

    failure_log = FailureLog(**data.model_dump())

    db.add(failure_log)
    db.commit()
    db.refresh(failure_log)

    return failure_log


def list_failure_logs(
    db: Session,
    workflow_run_id: int,
) -> list[FailureLog]:

    statement = (
        select(FailureLog)
        .where(
            FailureLog.workflow_run_id == workflow_run_id
        )
        .order_by(FailureLog.created_at.desc())
    )

    return list(db.scalars(statement).all())

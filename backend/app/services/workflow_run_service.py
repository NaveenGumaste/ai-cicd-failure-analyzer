
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.workflow_run import WorkflowRun
from app.schemas.workflow_run import WorkflowRunCreate


def create_workflow_run(
    db: Session,
    data: WorkflowRunCreate,
) -> WorkflowRun:
    """Create a workflow run for an existing repository."""

    repository = db.get(Repository, data.repository_id)

    if repository is None:
        raise ValueError("Repository not found.")

    workflow_run = WorkflowRun(**data.model_dump())

    db.add(workflow_run)
    db.commit()
    db.refresh(workflow_run)

    return workflow_run


def get_workflow_run(
    db: Session,
    run_id: int,
) -> WorkflowRun | None:
    return db.get(WorkflowRun, run_id)


def list_workflow_runs(
    db: Session,
    repository_id: int | None = None,
    conclusion: str | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[WorkflowRun]:

    statement = select(WorkflowRun)

    if repository_id is not None:
        statement = statement.where(
            WorkflowRun.repository_id == repository_id
        )

    if conclusion is not None:
        statement = statement.where(
            WorkflowRun.conclusion == conclusion
        )

    statement = (
        statement
        .order_by(WorkflowRun.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())

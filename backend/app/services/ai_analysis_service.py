
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_analysis import AIAnalysis
from app.models.workflow_run import WorkflowRun
from app.schemas.ai_analysis import AIAnalysisCreate


def create_analysis(
    db: Session,
    data: AIAnalysisCreate,
) -> AIAnalysis:

    workflow_run = db.get(
        WorkflowRun,
        data.workflow_run_id,
    )

    if workflow_run is None:
        raise ValueError("Workflow run not found.")

    analysis = AIAnalysis(**data.model_dump())

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


def get_analysis(
    db: Session,
    analysis_id: int,
) -> AIAnalysis | None:

    return db.get(AIAnalysis, analysis_id)


def list_analyses(
    db: Session,
    workflow_run_id: int,
) -> list[AIAnalysis]:

    statement = (
        select(AIAnalysis)
        .where(
            AIAnalysis.workflow_run_id == workflow_run_id
        )
        .order_by(AIAnalysis.created_at.desc())
    )

    return list(db.scalars(statement).all())

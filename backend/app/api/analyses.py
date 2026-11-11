
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.ai_analysis import (
    AIAnalysisCreate,
    AIAnalysisResponse,
)
from app.services import ai_analysis_service


router = APIRouter(
    prefix="/analyses",
    tags=["AI Analyses"],
)


@router.post(
    "/",
    response_model=AIAnalysisResponse,
    status_code=201,
)
def create_analysis(
    data: AIAnalysisCreate,
    db: Session = Depends(get_db),
):
    try:
        return ai_analysis_service.create_analysis(
            db,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/{analysis_id}",
    response_model=AIAnalysisResponse,
)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    analysis = ai_analysis_service.get_analysis(
        db,
        analysis_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found.",
        )

    return analysis


@router.get(
    "/",
    response_model=list[AIAnalysisResponse],
)
def list_analyses(
    workflow_run_id: int,
    db: Session = Depends(get_db),
):
    return ai_analysis_service.list_analyses(
        db,
        workflow_run_id,
    )

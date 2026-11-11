
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class AIAnalysisCreate(BaseModel):
    workflow_run_id: int = Field(gt=0)

    root_cause: str = Field(min_length=1)

    severity: str = Field(
        pattern=r"^(low|medium|high|critical)$"
    )

    suggested_fix: str = Field(min_length=1)

    confidence: Decimal | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    evidence: list[dict] | None = None

    model_id: str = Field(min_length=1, max_length=100)


class AIAnalysisResponse(BaseModel):
    id: int
    workflow_run_id: int
    root_cause: str
    severity: str
    suggested_fix: str
    confidence: Decimal | None
    evidence: list[dict] | None
    model_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

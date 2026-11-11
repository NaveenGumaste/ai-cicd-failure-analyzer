
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FailureLogCreate(BaseModel):
    workflow_run_id: int = Field(gt=0)

    raw_log: str = Field(min_length=1)

    extracted_errors: str | None = None


class FailureLogResponse(BaseModel):
    id: int
    workflow_run_id: int
    raw_log: str
    extracted_errors: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

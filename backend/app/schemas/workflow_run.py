
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkflowRunCreate(BaseModel):
    repository_id: int = Field(gt=0)
    github_run_id: int = Field(gt=0)

    workflow_name: str = Field(min_length=1, max_length=255)

    status: str = Field(min_length=1, max_length=50)

    conclusion: str | None = Field(
        default=None,
        max_length=50,
    )

    branch: str = Field(min_length=1, max_length=255)

    commit_sha: str = Field(min_length=1, max_length=64)

    html_url: str | None = None

    started_at: datetime | None = None

    completed_at: datetime | None = None


class WorkflowRunResponse(BaseModel):
    id: int
    repository_id: int
    github_run_id: int
    workflow_name: str
    status: str
    conclusion: str | None
    branch: str
    commit_sha: str
    html_url: str | None
    started_at: datetime | None
    completed_at: datetime | None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

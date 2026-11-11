
from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RepositoryCreate(BaseModel):
    """Fields required to register a repository."""

    github_repo_id: int = Field(gt=0)

    name: str = Field(min_length=1, max_length=255)

    full_name: str = Field(min_length=1, max_length=512)

    html_url: HttpUrl


class RepositoryUpdate(BaseModel):
    """Fields that can be updated."""

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=512,
    )

    html_url: HttpUrl | None = None


class RepositoryResponse(BaseModel):
    """Repository data returned by the API."""

    id: int
    github_repo_id: int
    name: str
    full_name: str
    html_url: str

    model_config = ConfigDict(from_attributes=True)

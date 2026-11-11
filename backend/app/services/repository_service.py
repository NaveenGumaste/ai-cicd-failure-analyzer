
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryUpdate


def create_repository(
    db: Session,
    repository_data: RepositoryCreate,
) -> Repository:
    """Create and persist a repository."""

    repository = Repository(
        github_repo_id=repository_data.github_repo_id,
        name=repository_data.name,
        full_name=repository_data.full_name,
        html_url=str(repository_data.html_url),
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


def get_repository_by_id(
    db: Session,
    repository_id: int,
) -> Repository | None:
    """Retrieve a repository using its internal ID."""

    statement = select(Repository).where(
        Repository.id == repository_id
    )

    return db.scalar(statement)


def get_all_repositories(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[Repository]:
    """Retrieve repositories with pagination."""

    statement = (
        select(Repository)
        .order_by(Repository.id.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def update_repository(
    db: Session,
    repository: Repository,
    update_data: RepositoryUpdate,
) -> Repository:
    """Update an existing repository."""

    changes = update_data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if field == "html_url" and value is not None:
            value = str(value)

        setattr(repository, field, value)

    db.commit()
    db.refresh(repository)

    return repository


def delete_repository(
    db: Session,
    repository: Repository,
) -> None:
    """Delete a repository."""

    db.delete(repository)
    db.commit()

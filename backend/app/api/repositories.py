
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryUpdate,
    RepositoryResponse,
)
from app.services import repository_service


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "/",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_repository(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return repository_service.create_repository(
            db,
            repository_data,
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A repository with this GitHub ID already exists.",
        )


@router.get(
    "/",
    response_model=list[RepositoryResponse],
)
def list_repositories(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return repository_service.get_all_repositories(
        db,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = repository_service.get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found.",
        )

    return repository


@router.patch(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def update_repository(
    repository_id: int,
    update_data: RepositoryUpdate,
    db: Session = Depends(get_db),
):
    repository = repository_service.get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found.",
        )

    if not update_data.model_fields_set:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided.",
        )

    try:
        return repository_service.update_repository(
            db,
            repository,
            update_data,
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Repository update conflicts with existing data.",
        )


@router.delete(
    "/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_repository(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = repository_service.get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found.",
        )

    repository_service.delete_repository(db, repository)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

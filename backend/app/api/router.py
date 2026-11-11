
from fastapi import APIRouter

from app.api import (
    health,
    repositories,
    workflow_runs,
    failure_logs,
    analyses,
)


api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(repositories.router)
api_router.include_router(workflow_runs.router)
api_router.include_router(failure_logs.router)
api_router.include_router(analyses.router)

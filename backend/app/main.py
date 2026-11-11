
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings


# Initialize the application.
app = FastAPI(
    title=settings.app_name,
    description=(
        "An AI-powered platform for analyzing "
        "CI/CD pipeline failures."
    ),
    version=settings.app_version,
)


# Configure CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register versioned API routes.
app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/")
async def root():
    return {
        "message": f"{settings.app_name} API is running",
        "version": settings.app_version,
        "environment": settings.app_env,
        "docs": "/docs",
    }

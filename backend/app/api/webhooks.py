import json

from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    Request,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fastapi import BackgroundTasks

from app.services.webhook_processor import process_github_webhook

from app.core.config import settings
from app.core.database import get_db
from app.services.webhook_service import (
    verify_github_signature,
    register_webhook_delivery,
)

router = APIRouter(
    prefix="/webhooks",
    tags=["GitHub Webhooks"],
)


@router.post("/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    x_github_event: str | None = Header(default=None),
    x_github_delivery: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
):
    # 1. Verify webhook secret configuration.
    if not settings.github_webhook_secret:
        raise HTTPException(
            status_code=503,
            detail="GitHub webhook secret is not configured",
        )

    # 2. Read original request body.
    payload_body = await request.body()

    # 3. Verify HMAC signature.
    is_valid = verify_github_signature(
        payload_body=payload_body,
        secret=settings.github_webhook_secret,
        signature_header=x_hub_signature_256,
    )

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid GitHub webhook signature",
        )

    # 4. Validate required GitHub headers.
    if not x_github_event or not x_github_delivery:
        raise HTTPException(
            status_code=400,
            detail="Missing GitHub webhook headers",
        )

    # 5. Parse JSON.
    try:
        payload = json.loads(payload_body)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid JSON payload",
        ) from exc

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=400,
            detail="Webhook payload must be a JSON object",
        )

    # 6. Extract event information.
    action = payload.get("action")

    repository = payload.get("repository") or {}
    workflow_run = payload.get("workflow_run") or {}

    if not isinstance(repository, dict):
        repository = {}

    if not isinstance(workflow_run, dict):
        workflow_run = {}

    repository_full_name = repository.get("full_name")
    github_run_id = workflow_run.get("id")

    # 7. Register delivery in PostgreSQL.
    try:
        is_new_delivery = register_webhook_delivery(
            db=db,
            delivery_id=x_github_delivery,
            event_type=x_github_event,
            action=action,
            repository_full_name=repository_full_name,
            github_run_id=github_run_id,
        )

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to register webhook delivery",
        ) from exc

    # 8. Ignore duplicate deliveries.
    if not is_new_delivery:
        return {
            "message": "Duplicate webhook delivery ignored",
            "delivery_id": x_github_delivery,
        }

    # Handle GitHub ping.
    if x_github_event == "ping":
        return {
            "message": "GitHub webhook connection successful",
            "delivery_id": x_github_delivery,
        }

    # Ignore unsupported events.
    if x_github_event != "workflow_run":
        return {
            "message": "Event ignored",
            "event": x_github_event,
            "delivery_id": x_github_delivery,
        }

    # Process only completed workflow events.
    if action != "completed":
        return {
            "message": "Workflow event ignored",
            "action": action,
            "delivery_id": x_github_delivery,
        }

    # Schedule background processing.
    background_tasks.add_task(
        process_github_webhook,
        delivery_id=x_github_delivery,
        payload=payload,
    )

    return {
        "message": "Workflow event accepted for background processing",
        "delivery_id": x_github_delivery,
        "repository": repository_full_name,
        "github_run_id": github_run_id,
        "status": workflow_run.get("status"),
        "conclusion": workflow_run.get("conclusion"),
    }
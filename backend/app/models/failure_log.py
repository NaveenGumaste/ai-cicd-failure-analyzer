
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class FailureLog(Base):
    __tablename__ = "failure_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    workflow_run_id: Mapped[int] = mapped_column(
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    raw_log: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    extracted_errors: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    workflow_run: Mapped["WorkflowRun"] = relationship(
        back_populates="failure_logs",
    )

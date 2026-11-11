
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # Reference to our internal repository ID
    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
    )

    # GitHub's workflow run ID
    github_run_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    workflow_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    conclusion: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    branch: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    commit_sha: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    html_url: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    repository: Mapped["Repository"] = relationship(
        back_populates="workflow_runs",
    )

    failure_logs: Mapped[list["FailureLog"]] = relationship(
        back_populates="workflow_run",
        cascade="all, delete-orphan",
    )

    ai_analyses: Mapped[list["AIAnalysis"]] = relationship(
        back_populates="workflow_run",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index(
            "ix_workflow_runs_repository_created",
            "repository_id",
            "created_at",
        ),
    )

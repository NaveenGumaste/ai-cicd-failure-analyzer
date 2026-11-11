
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    # Internal primary key
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # GitHub's unique repository identifier
    github_repo_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    html_url: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # One repository can have multiple workflow runs.
    workflow_runs: Mapped[list["WorkflowRun"]] = relationship(
        back_populates="repository",
        cascade="all, delete-orphan",
    )

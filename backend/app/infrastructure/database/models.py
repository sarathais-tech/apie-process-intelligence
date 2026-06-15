from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.infrastructure.database.base import Base


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    session_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    process_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    window_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    activity: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProcessModel(Base):
    __tablename__ = "processes"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="discovered")
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    steps: Mapped[list["ProcessStepModel"]] = relationship(
        back_populates="process",
        cascade="all, delete-orphan",
        order_by="ProcessStepModel.order",
    )


class ProcessStepModel(Base):
    __tablename__ = "process_steps"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    process_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("processes.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    application: Mapped[str | None] = mapped_column(String(255), nullable=True)
    step_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    process: Mapped[ProcessModel] = relationship(back_populates="steps")

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.entities.process import ProcessStatus, ProcessStep, ReconstructedProcess
from app.domain.repositories.process_repository import ProcessRepository
from app.infrastructure.database.models import ProcessModel, ProcessStepModel


class SqlAlchemyProcessRepository(ProcessRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def add(self, process: ReconstructedProcess) -> ReconstructedProcess:
        model = ProcessModel(
            id=process.id,
            name=process.name,
            status=process.status.value,
            confidence_score=process.confidence_score,
            steps=[
                ProcessStepModel(
                    name=step.name,
                    order=step.order,
                    application=step.application,
                    step_metadata=step.metadata,
                )
                for step in process.steps
            ],
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self.get(model.id) or process

    def list(self, limit: int = 100, offset: int = 0) -> list[ReconstructedProcess]:
        statement = (
            select(ProcessModel)
            .options(selectinload(ProcessModel.steps))
            .order_by(ProcessModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [self._to_entity(model) for model in self.db.scalars(statement).all()]

    def get(self, process_id: UUID) -> ReconstructedProcess | None:
        statement = select(ProcessModel).options(selectinload(ProcessModel.steps)).where(ProcessModel.id == process_id)
        model = self.db.scalars(statement).first()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: ProcessModel) -> ReconstructedProcess:
        return ReconstructedProcess(
            id=model.id,
            name=model.name,
            status=ProcessStatus(model.status),
            confidence_score=model.confidence_score,
            created_at=model.created_at,
            steps=[
                ProcessStep(
                    name=step.name,
                    order=step.order,
                    application=step.application,
                    metadata=step.step_metadata,
                )
                for step in sorted(model.steps, key=lambda item: item.order)
            ],
        )

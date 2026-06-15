from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from app.application.use_cases.reconstruct_processes import ReconstructProcessesUseCase
from app.domain.entities.process import ReconstructedProcess
from app.infrastructure.process_mining.pm4py_discovery_engine import PM4PyProcessDiscoveryEngine
from app.infrastructure.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.repositories.sqlalchemy_process_repository import SqlAlchemyProcessRepository
from app.interfaces.api.dependencies import get_event_repository, get_process_discovery_engine, get_process_repository
from app.interfaces.api.schemas.processes import ProcessRead

router = APIRouter(prefix="/processes", tags=["processes"])

EventRepo = Annotated[SqlAlchemyEventRepository, Depends(get_event_repository)]
ProcessRepo = Annotated[SqlAlchemyProcessRepository, Depends(get_process_repository)]
DiscoveryEngine = Annotated[PM4PyProcessDiscoveryEngine, Depends(get_process_discovery_engine)]


@router.get("", response_model=list[ProcessRead])
def list_processes(
    repository: ProcessRepo,
    limit: Annotated[int, Query(ge=1, le=500)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[ReconstructedProcess]:
    return repository.list(limit=limit, offset=offset)


@router.post("/reconstruct", response_model=list[ProcessRead], status_code=201)
def reconstruct_processes(
    event_repository: EventRepo,
    process_repository: ProcessRepo,
    discovery_engine: DiscoveryEngine,
) -> list[ReconstructedProcess]:
    return ReconstructProcessesUseCase(event_repository, process_repository, discovery_engine).execute()


@router.post("/discover", response_model=list[ProcessRead], status_code=201)
def discover_processes(
    event_repository: EventRepo,
    process_repository: ProcessRepo,
    discovery_engine: DiscoveryEngine,
) -> list[ReconstructedProcess]:
    return ReconstructProcessesUseCase(event_repository, process_repository, discovery_engine).execute()


@router.get("/{process_id}", response_model=ProcessRead)
def get_process(process_id: UUID, repository: ProcessRepo) -> ReconstructedProcess:
    process = repository.get(process_id)
    if not process:
        raise HTTPException(status_code=404, detail="Processo nao encontrado")
    return process

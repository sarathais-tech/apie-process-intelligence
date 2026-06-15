from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.sop import StandardOperatingProcedureArtifact
from app.application.use_cases.generate_sop import GenerateSopFromFlowUseCase, GenerateSopFromProcessUseCase
from app.infrastructure.documents.reportlab_sop_generator import ReportLabSopGenerator
from app.infrastructure.repositories.sqlalchemy_process_repository import SqlAlchemyProcessRepository
from app.interfaces.api.dependencies import get_process_repository, get_sop_generator
from app.interfaces.api.schemas.sops import SopFromFlowCreate, SopFromProcessCreate, SopRead

router = APIRouter(prefix="/sops", tags=["sops"])

ProcessRepo = Annotated[SqlAlchemyProcessRepository, Depends(get_process_repository)]
SopGeneratorDep = Annotated[ReportLabSopGenerator, Depends(get_sop_generator)]


@router.post("", response_model=SopRead, status_code=201)
def generate_sop_from_flow(payload: SopFromFlowCreate, generator: SopGeneratorDep) -> StandardOperatingProcedureArtifact:
    try:
        return GenerateSopFromFlowUseCase(generator).execute(
            title=payload.title,
            activities=payload.activities,
            objective=payload.objective,
            responsible_roles=payload.responsible_roles,
            prerequisites=payload.prerequisites,
            expected_result=payload.expected_result,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/processes/{process_id}", response_model=SopRead, status_code=201)
def generate_sop_from_process(
    process_id: UUID,
    payload: SopFromProcessCreate,
    repository: ProcessRepo,
    generator: SopGeneratorDep,
) -> StandardOperatingProcedureArtifact:
    try:
        artifact = GenerateSopFromProcessUseCase(repository, generator).execute(
            process_id=process_id,
            responsible_roles=payload.responsible_roles,
            prerequisites=payload.prerequisites,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    if artifact is None:
        raise HTTPException(status_code=404, detail="Processo nao encontrado")
    return artifact

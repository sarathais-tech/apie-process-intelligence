from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.dto.narrative import FlowNarrative
from app.application.use_cases.narrate_flow import NarrateFlowUseCase
from app.infrastructure.llm.ollama_flow_narrator import OllamaFlowNarrator
from app.interfaces.api.dependencies import get_flow_narrator
from app.interfaces.api.schemas.narratives import FlowNarrativeCreate, FlowNarrativeRead

router = APIRouter(prefix="/narratives", tags=["narratives"])

FlowNarratorDep = Annotated[OllamaFlowNarrator, Depends(get_flow_narrator)]


@router.post("/flow", response_model=FlowNarrativeRead, status_code=201)
def narrate_flow(payload: FlowNarrativeCreate, narrator: FlowNarratorDep) -> FlowNarrative:
    try:
        return NarrateFlowUseCase(narrator).execute(payload.activities, model=payload.model)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

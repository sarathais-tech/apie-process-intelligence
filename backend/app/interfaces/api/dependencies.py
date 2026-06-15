from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import get_settings
from app.infrastructure.database.session import get_db
from app.infrastructure.documents.reportlab_sop_generator import ReportLabSopGenerator
from app.infrastructure.flowcharts.mermaid_flowchart_generator import MermaidFlowchartGenerator
from app.infrastructure.llm.ollama_flow_narrator import OllamaFlowNarrator
from app.infrastructure.process_mining.pm4py_discovery_engine import PM4PyProcessDiscoveryEngine
from app.infrastructure.repositories.sqlalchemy_event_repository import SqlAlchemyEventRepository
from app.infrastructure.repositories.sqlalchemy_process_repository import SqlAlchemyProcessRepository


DbSession = Annotated[Session, Depends(get_db)]


def get_event_repository(db: DbSession) -> SqlAlchemyEventRepository:
    return SqlAlchemyEventRepository(db)


def get_process_repository(db: DbSession) -> SqlAlchemyProcessRepository:
    return SqlAlchemyProcessRepository(db)


def get_process_discovery_engine() -> PM4PyProcessDiscoveryEngine:
    return PM4PyProcessDiscoveryEngine()


def get_flowchart_generator() -> MermaidFlowchartGenerator:
    return MermaidFlowchartGenerator()


def get_sop_generator() -> ReportLabSopGenerator:
    return ReportLabSopGenerator()


def get_flow_narrator() -> OllamaFlowNarrator:
    settings = get_settings()
    return OllamaFlowNarrator(
        base_url=settings.ollama_base_url,
        timeout_seconds=settings.ollama_timeout_seconds,
    )

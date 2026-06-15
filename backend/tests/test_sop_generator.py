import base64

from app.application.use_cases.generate_sop import GenerateSopFromFlowUseCase, build_sop_from_process
from app.domain.entities.process import ProcessStep, ReconstructedProcess
from app.infrastructure.documents.reportlab_sop_generator import ReportLabSopGenerator


def test_build_sop_from_discovered_process() -> None:
    process = ReconstructedProcess(
        name="Fluxo descoberto 1",
        steps=[
            ProcessStep(name="Login", order=1, application="erp.exe"),
            ProcessStep(name="Consultar pedido", order=2, application="erp.exe"),
            ProcessStep(name="Salvar", order=3, application="erp.exe"),
        ],
        confidence_score=0.8,
    )

    procedure = build_sop_from_process(process)

    assert procedure.title == "POP - Fluxo descoberto 1"
    assert "Padronizar a execucao" in procedure.objective
    assert procedure.responsible_roles == ["Operador do processo", "Gestor do processo", "Analista de processos"]
    assert len(procedure.prerequisites) == 3
    assert [step.name for step in procedure.steps] == ["Login", "Consultar pedido", "Salvar"]
    assert "Processo concluido" in procedure.expected_result


def test_generate_sop_from_flow_creates_pdf_artifact() -> None:
    artifact = GenerateSopFromFlowUseCase(ReportLabSopGenerator()).execute(
        title="Fluxo de pedido",
        activities=["Login", "Consultar pedido", "Salvar"],
    )

    pdf_bytes = base64.b64decode(artifact.pdf_base64)

    assert artifact.filename == "fluxo-de-pedido.pdf"
    assert artifact.mime_type == "application/pdf"
    assert pdf_bytes.startswith(b"%PDF")


def test_generate_sop_from_flow_rejects_empty_activities() -> None:
    use_case = GenerateSopFromFlowUseCase(ReportLabSopGenerator())

    try:
        use_case.execute(title="Vazio", activities=["", " "])
    except ValueError as exc:
        assert "ao menos uma atividade" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

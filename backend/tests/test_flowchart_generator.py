import base64

from app.application.use_cases.generate_flowchart import GenerateFlowchartUseCase
from app.infrastructure.flowcharts.mermaid_flowchart_generator import MermaidFlowchartGenerator


def test_generate_mermaid_flowchart_from_activity_sequence() -> None:
    generator = MermaidFlowchartGenerator()

    artifact = generator.generate(["Login", "Consultar pedido", "Salvar"])

    assert artifact.mermaid == "\n".join(
        [
            "flowchart TD",
            '    A1["Login"]',
            '    A2["Consultar pedido"]',
            '    A3["Salvar"]',
            "    A1 --> A2",
            "    A2 --> A3",
        ]
    )


def test_generate_svg_flowchart() -> None:
    generator = MermaidFlowchartGenerator()

    artifact = generator.generate(["Login", "Consultar pedido"], title="Pedido")

    assert artifact.svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')
    assert "Pedido" in artifact.svg
    assert "Login" in artifact.svg
    assert "Consultar pedido" in artifact.svg
    assert "marker-end" in artifact.svg


def test_generate_png_flowchart_as_base64() -> None:
    generator = MermaidFlowchartGenerator()

    artifact = generator.generate(["Login", "Salvar"])
    png_bytes = base64.b64decode(artifact.png_base64)

    assert artifact.png_mime_type == "image/png"
    assert png_bytes.startswith(b"\x89PNG\r\n\x1a\n")


def test_generate_flowchart_use_case_removes_empty_activities() -> None:
    use_case = GenerateFlowchartUseCase(MermaidFlowchartGenerator())

    artifact = use_case.execute([" Login ", "", "Salvar"])

    assert 'A1["Login"]' in artifact.mermaid
    assert 'A2["Salvar"]' in artifact.mermaid
    assert "A3" not in artifact.mermaid


def test_generate_flowchart_use_case_rejects_empty_sequence() -> None:
    use_case = GenerateFlowchartUseCase(MermaidFlowchartGenerator())

    try:
        use_case.execute([" ", ""])
    except ValueError as exc:
        assert "ao menos uma atividade" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

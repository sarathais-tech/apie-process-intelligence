from unittest.mock import patch

from app.application.use_cases.narrate_flow import NarrateFlowUseCase
from app.infrastructure.llm.ollama_flow_narrator import OllamaFlowNarrator


def test_narrate_flow_uses_ollama_response() -> None:
    with patch.object(
        OllamaFlowNarrator,
        "_call_ollama",
        return_value="O usuario acessa o ERP e salva as informacoes",
    ) as call_ollama:
        narrative = OllamaFlowNarrator(base_url="http://ollama:11434").narrate(["ERP", "Salvar"], model="mistral")

    assert narrative.text == "O usuario acessa o ERP e salva as informacoes."
    assert narrative.model == "mistral"
    assert narrative.provider == "ollama"
    assert narrative.used_fallback is False
    call_ollama.assert_called_once()


def test_narrate_flow_falls_back_when_ollama_is_unavailable() -> None:
    with patch.object(OllamaFlowNarrator, "_call_ollama", side_effect=ConnectionError("offline")):
        narrative = OllamaFlowNarrator().narrate(["ERP", "Compras", "Cadastro", "Salvar"], model="llama 3")

    assert narrative.model == "llama3"
    assert narrative.provider == "local-template"
    assert narrative.used_fallback is True
    assert narrative.text == "O usuario acessa o ERP, navega ate o modulo de compras, realiza o cadastro e salva as informacoes."


def test_narrate_flow_use_case_rejects_empty_flow() -> None:
    use_case = NarrateFlowUseCase(OllamaFlowNarrator())

    try:
        use_case.execute(["", " "])
    except ValueError as exc:
        assert "ao menos uma atividade" in str(exc)
    else:
        raise AssertionError("Expected ValueError")

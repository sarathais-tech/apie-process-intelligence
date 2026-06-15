import re

from app.application.dto.narrative import FlowNarrative
from app.application.services.flow_narrator import FlowNarrator


class OllamaFlowNarrator(FlowNarrator):
    def __init__(self, base_url: str = "http://localhost:11434", timeout_seconds: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def narrate(self, activities: list[str], model: str = "llama3") -> FlowNarrative:
        normalized_model = self._normalize_model(model)
        prompt = self._build_prompt(activities)

        try:
            text = self._call_ollama(prompt=prompt, model=normalized_model)
            if text:
                return FlowNarrative(
                    text=self._normalize_sentence(text),
                    model=normalized_model,
                    provider="ollama",
                    used_fallback=False,
                )
        except Exception:
            pass

        return FlowNarrative(
            text=self._fallback_narrative(activities),
            model=normalized_model,
            provider="local-template",
            used_fallback=True,
        )

    def _call_ollama(self, prompt: str, model: str) -> str:
        import requests

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2},
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        return str(payload.get("response", "")).strip()

    def _build_prompt(self, activities: list[str]) -> str:
        flow = " -> ".join(activities)
        return (
            "Transforme o fluxo de processo abaixo em uma unica frase em portugues do Brasil, "
            "em linguagem natural, objetiva e profissional. "
            "Nao use lista, nao explique, nao inclua aspas extras.\n\n"
            f"Fluxo: {flow}\n\n"
            "Frase:"
        )

    def _fallback_narrative(self, activities: list[str]) -> str:
        if len(activities) == 1:
            return f"O usuario executa a atividade {self._lower_activity(activities[0])}."

        first = self._verb_for_activity(activities[0], first=True)
        middle = [self._verb_for_activity(activity) for activity in activities[1:-1]]
        last = self._verb_for_activity(activities[-1], final=True)
        actions = [first, *middle, last]

        return "O usuario " + self._join_actions(actions) + "."

    def _verb_for_activity(self, activity: str, first: bool = False, final: bool = False) -> str:
        normalized = self._lower_activity(activity)
        if final and any(token in normalized for token in ["salvar", "gravar", "confirmar"]):
            return "salva as informacoes"
        if any(token in normalized for token in ["erp", "sistema", "portal"]):
            return f"acessa o {activity}"
        if any(token in normalized for token in ["compras", "financeiro", "estoque", "vendas"]):
            return f"navega ate o modulo de {normalized}"
        if any(token in normalized for token in ["cadastro", "cadastrar"]):
            return "realiza o cadastro"
        if any(token in normalized for token in ["consulta", "consultar"]):
            return f"consulta {normalized.replace('consultar ', '').replace('consulta ', '')}"
        if first:
            return f"inicia em {normalized}"
        return f"executa {normalized}"

    def _join_actions(self, actions: list[str]) -> str:
        if len(actions) == 1:
            return actions[0]
        if len(actions) == 2:
            return f"{actions[0]} e {actions[1]}"
        return ", ".join(actions[:-1]) + f" e {actions[-1]}"

    def _lower_activity(self, activity: str) -> str:
        return re.sub(r"\s+", " ", activity).strip().lower()

    def _normalize_model(self, model: str) -> str:
        cleaned = model.strip() if model else "llama3"
        if cleaned.lower() in {"llama", "llama3", "llama 3"}:
            return "llama3"
        if cleaned.lower() in {"mistral"}:
            return "mistral"
        return cleaned

    def _normalize_sentence(self, text: str) -> str:
        normalized = re.sub(r"\s+", " ", text).strip().strip('"')
        if not normalized.endswith((".", "!", "?")):
            normalized += "."
        return normalized

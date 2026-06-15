from app.application.dto.sop import StandardOperatingProcedure, StandardOperatingProcedureArtifact
from app.application.services.sop_generator import StandardOperatingProcedureGenerator
from app.domain.entities.process import ProcessStep, ReconstructedProcess
from app.domain.repositories.process_repository import ProcessRepository


class GenerateSopFromProcessUseCase:
    def __init__(
        self,
        process_repository: ProcessRepository,
        generator: StandardOperatingProcedureGenerator,
    ) -> None:
        self.process_repository = process_repository
        self.generator = generator

    def execute(
        self,
        process_id,
        responsible_roles: list[str] | None = None,
        prerequisites: list[str] | None = None,
    ) -> StandardOperatingProcedureArtifact | None:
        process = self.process_repository.get(process_id)
        if process is None:
            return None

        procedure = build_sop_from_process(
            process=process,
            responsible_roles=responsible_roles,
            prerequisites=prerequisites,
        )
        return self.generator.generate(procedure)


class GenerateSopFromFlowUseCase:
    def __init__(self, generator: StandardOperatingProcedureGenerator) -> None:
        self.generator = generator

    def execute(
        self,
        title: str,
        activities: list[str],
        objective: str | None = None,
        responsible_roles: list[str] | None = None,
        prerequisites: list[str] | None = None,
        expected_result: str | None = None,
    ) -> StandardOperatingProcedureArtifact:
        cleaned_activities = [activity.strip() for activity in activities if activity and activity.strip()]
        if not cleaned_activities:
            raise ValueError("O fluxo deve conter ao menos uma atividade.")

        steps = [
            ProcessStep(name=activity, order=index)
            for index, activity in enumerate(cleaned_activities, start=1)
        ]
        procedure = StandardOperatingProcedure(
            title=title.strip() or "Procedimento Operacional Padrao",
            objective=objective or f"Padronizar a execucao do fluxo {title}.",
            responsible_roles=responsible_roles or ["Operador do processo", "Gestor do processo"],
            prerequisites=prerequisites or ["Acesso aos sistemas necessarios", "Fluxo aprovado pelo responsavel"],
            steps=steps,
            expected_result=expected_result or "Processo executado de forma padronizada, rastreavel e conforme o fluxo definido.",
        )
        return self.generator.generate(procedure)


def build_sop_from_process(
    process: ReconstructedProcess,
    responsible_roles: list[str] | None = None,
    prerequisites: list[str] | None = None,
) -> StandardOperatingProcedure:
    step_names = ", ".join(step.name for step in process.steps[:3])
    objective = (
        f"Padronizar a execucao do processo '{process.name}', garantindo consistencia, "
        f"rastreabilidade e aderencia ao fluxo descoberto."
    )
    if step_names:
        objective += f" O fluxo inicia por: {step_names}."

    return StandardOperatingProcedure(
        title=f"POP - {process.name}",
        objective=objective,
        responsible_roles=responsible_roles or ["Operador do processo", "Gestor do processo", "Analista de processos"],
        prerequisites=prerequisites or [
            "Usuario autenticado nos sistemas envolvidos",
            "Permissoes de acesso concedidas",
            "Dados de entrada disponiveis e validados",
        ],
        steps=sorted(process.steps, key=lambda step: step.order),
        expected_result=(
            "Processo concluido com as atividades executadas na sequencia esperada, "
            "com registros disponiveis para auditoria e melhoria continua."
        ),
    )

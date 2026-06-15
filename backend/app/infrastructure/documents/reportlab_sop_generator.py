import base64
import io
import re

from app.application.dto.sop import StandardOperatingProcedure, StandardOperatingProcedureArtifact
from app.application.services.sop_generator import StandardOperatingProcedureGenerator


class ReportLabSopGenerator(StandardOperatingProcedureGenerator):
    def generate(self, procedure: StandardOperatingProcedure) -> StandardOperatingProcedureArtifact:
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
            from reportlab.lib.units import cm
            from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
        except ImportError as exc:
            raise RuntimeError("Instale reportlab para gerar PDFs de POP.") from exc

        output = io.BytesIO()
        document = SimpleDocTemplate(
            output,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=1.8 * cm,
            bottomMargin=1.8 * cm,
            title=procedure.title,
        )
        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="SectionTitle",
                parent=styles["Heading2"],
                fontSize=12,
                leading=15,
                spaceBefore=12,
                spaceAfter=6,
                textColor=colors.HexColor("#0f766e"),
            )
        )

        story = [
            Paragraph(procedure.title, styles["Title"]),
            Spacer(1, 10),
            Paragraph("Objetivo", styles["SectionTitle"]),
            Paragraph(self._escape(procedure.objective), styles["BodyText"]),
            Paragraph("Responsaveis", styles["SectionTitle"]),
            self._bullet_table(procedure.responsible_roles, styles),
            Paragraph("Pre-requisitos", styles["SectionTitle"]),
            self._bullet_table(procedure.prerequisites, styles),
            Paragraph("Etapas", styles["SectionTitle"]),
            self._steps_table(procedure, styles),
            Paragraph("Resultado esperado", styles["SectionTitle"]),
            Paragraph(self._escape(procedure.expected_result), styles["BodyText"]),
        ]

        document.build(story)
        pdf_bytes = output.getvalue()

        return StandardOperatingProcedureArtifact(
            filename=f"{self._slugify(procedure.title)}.pdf",
            pdf_base64=base64.b64encode(pdf_bytes).decode("ascii"),
        )

    def _bullet_table(self, items, styles):
        from reportlab.platypus import Paragraph, Table, TableStyle
        from reportlab.lib import colors

        rows = [["#", "Descricao"]]
        rows.extend([[str(index), Paragraph(self._escape(item), styles["BodyText"])] for index, item in enumerate(items, start=1)])
        table = Table(rows, colWidths=[34, 430])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e7f3f1")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#172026")),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d5d8")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return table

    def _steps_table(self, procedure: StandardOperatingProcedure, styles):
        from reportlab.platypus import Paragraph, Table, TableStyle
        from reportlab.lib import colors

        rows = [["Etapa", "Atividade", "Aplicacao", "Observacao"]]
        for step in procedure.steps:
            next_steps = step.metadata.get("next_steps", []) if step.metadata else []
            observation = self._format_next_steps(next_steps)
            rows.append(
                [
                    str(step.order),
                    Paragraph(self._escape(step.name), styles["BodyText"]),
                    self._escape(step.application or "-"),
                    Paragraph(self._escape(observation), styles["BodyText"]),
                ]
            )

        table = Table(rows, colWidths=[42, 190, 110, 122], repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d5d8")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        return table

    def _format_next_steps(self, next_steps) -> str:
        if not next_steps:
            return "Executar conforme sequencia definida."
        labels = [f"{item.get('activity')} ({item.get('frequency')})" for item in next_steps]
        return "Proximas etapas provaveis: " + ", ".join(labels)

    def _escape(self, value: str) -> str:
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
        return slug or "procedimento-operacional-padrao"

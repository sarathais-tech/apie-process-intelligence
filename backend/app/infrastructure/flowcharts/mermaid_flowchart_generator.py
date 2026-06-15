import base64
import html
import io
import re
import struct
import zlib

from app.application.dto.flowchart import FlowchartArtifact
from app.application.services.flowchart_generator import FlowchartGenerator


class MermaidFlowchartGenerator(FlowchartGenerator):
    def generate(self, activities: list[str], title: str | None = None) -> FlowchartArtifact:
        mermaid = self._build_mermaid(activities)
        svg = self._build_svg(activities, title=title)
        png_bytes = self._build_png(activities, title=title)

        return FlowchartArtifact(
            mermaid=mermaid,
            svg=svg,
            png_base64=base64.b64encode(png_bytes).decode("ascii"),
        )

    def _build_mermaid(self, activities: list[str]) -> str:
        lines = ["flowchart TD"]
        for index, activity in enumerate(activities, start=1):
            node_id = f"A{index}"
            lines.append(f'    {node_id}["{self._escape_mermaid_label(activity)}"]')

        for index in range(1, len(activities)):
            lines.append(f"    A{index} --> A{index + 1}")

        return "\n".join(lines)

    def _build_svg(self, activities: list[str], title: str | None = None) -> str:
        width = 760
        node_width = 320
        node_height = 56
        gap = 42
        top = 72 if title else 32
        height = top + len(activities) * node_height + max(0, len(activities) - 1) * gap + 32
        center_x = width // 2
        x = center_x - node_width // 2

        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            "<defs>",
            '<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#0f766e" />',
            "</marker>",
            "</defs>",
            '<rect width="100%" height="100%" fill="#f7faf9" />',
        ]

        if title:
            parts.append(
                f'<text x="{center_x}" y="36" text-anchor="middle" font-family="Arial, sans-serif" '
                f'font-size="20" font-weight="700" fill="#172026">{html.escape(title)}</text>'
            )

        for index, activity in enumerate(activities):
            y = top + index * (node_height + gap)
            node_id = f"step-{index + 1}"
            parts.append(f'<g id="{node_id}">')
            parts.append(
                f'<rect x="{x}" y="{y}" width="{node_width}" height="{node_height}" rx="8" '
                'fill="#ffffff" stroke="#0f766e" stroke-width="2" />'
            )
            parts.append(
                f'<text x="{center_x}" y="{y + 34}" text-anchor="middle" font-family="Arial, sans-serif" '
                f'font-size="15" font-weight="600" fill="#172026">{html.escape(self._truncate(activity, 42))}</text>'
            )
            parts.append("</g>")

            if index < len(activities) - 1:
                line_start_y = y + node_height
                line_end_y = y + node_height + gap - 8
                parts.append(
                    f'<line x1="{center_x}" y1="{line_start_y}" x2="{center_x}" y2="{line_end_y}" '
                    'stroke="#0f766e" stroke-width="2" marker-end="url(#arrow)" />'
                )

        parts.append("</svg>")
        return "".join(parts)

    def _build_png(self, activities: list[str], title: str | None = None) -> bytes:
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            return self._build_fallback_png(width=760, height=max(180, 96 + len(activities) * 98))

        width = 760
        node_width = 320
        node_height = 56
        gap = 42
        top = 72 if title else 32
        height = top + len(activities) * node_height + max(0, len(activities) - 1) * gap + 32
        center_x = width // 2
        x = center_x - node_width // 2

        image = Image.new("RGB", (width, height), "#f7faf9")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        if title:
            draw.text((center_x, 24), title, fill="#172026", anchor="mm", font=font)

        for index, activity in enumerate(activities):
            y = top + index * (node_height + gap)
            draw.rounded_rectangle(
                (x, y, x + node_width, y + node_height),
                radius=8,
                fill="#ffffff",
                outline="#0f766e",
                width=2,
            )
            draw.text((center_x, y + node_height // 2), self._truncate(activity, 42), fill="#172026", anchor="mm", font=font)

            if index < len(activities) - 1:
                start_y = y + node_height
                end_y = y + node_height + gap - 8
                draw.line((center_x, start_y, center_x, end_y), fill="#0f766e", width=2)
                draw.polygon(
                    [(center_x, end_y + 7), (center_x - 6, end_y - 3), (center_x + 6, end_y - 3)],
                    fill="#0f766e",
                )

        output = io.BytesIO()
        image.save(output, format="PNG")
        return output.getvalue()

    def _build_fallback_png(self, width: int, height: int) -> bytes:
        row = b"\x00" + (b"\xf7\xfa\xf9" * width)
        raw = row * height

        def chunk(kind: bytes, data: bytes) -> bytes:
            checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)

        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(raw))
        png += chunk(b"IEND", b"")
        return png

    def _escape_mermaid_label(self, value: str) -> str:
        return value.replace("\\", "\\\\").replace('"', '\\"')

    def _truncate(self, value: str, limit: int) -> str:
        normalized = re.sub(r"\s+", " ", value).strip()
        if len(normalized) <= limit:
            return normalized
        return normalized[: limit - 1] + "..."

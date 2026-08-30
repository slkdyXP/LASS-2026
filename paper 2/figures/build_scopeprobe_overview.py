"""Compose image-generated concept art with exact publication labels.

The source illustration was produced with OpenAI image generation from the
prompt documented in ``IMAGEGEN_PROMPT.md``. Scientific text, quoted evidence,
and counts are added deterministically. The PNG is rendered at 600 dpi; the PDF
keeps the source art rasterized but draws all labels, boxes, and arrows as
vectors.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "scopeprobe_overview_image2.png"
PDF_OUT = ROOT / "scopeprobe_overview.pdf"
PNG_OUT = ROOT / "scopeprobe_overview.png"

FONT_REGULAR = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
FONT_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

# Okabe--Ito-inspired colors used consistently across the paper.
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERMILION = "#D55E00"
CHARCOAL = "#343A40"
MID_GREY = "#6C757D"
LIGHT_GREY = "#E9ECEF"
PALE = "#F8F9FA"
PALE_RED = "#FFF3ED"

BASE_WIDTH = 1907
IMAGE_HEIGHT = 770
STRIP_HEIGHT = 138
TOTAL_HEIGHT = IMAGE_HEIGHT + STRIP_HEIGHT
FIGURE_WIDTH_IN = 7.15
PNG_DPI = 600


def _pil_font(points: float, bold: bool, scale: float) -> ImageFont.FreeTypeFont:
    # At the final 600-dpi physical size, one point is 600/72 pixels.
    size = max(1, round(points * PNG_DPI / 72))
    path = FONT_BOLD if bold else FONT_REGULAR
    return ImageFont.truetype(str(path), size=size)


def _pil_xy(x: float, y: float, scale: float) -> tuple[int, int]:
    return round(x * scale), round(y * scale)


def _draw_pil_text(draw, x, y, text, points, color, scale, bold=False, anchor="lm"):
    draw.text(
        _pil_xy(x, y, scale),
        text,
        fill=color,
        font=_pil_font(points, bold, scale),
        anchor=anchor,
    )


def _draw_pil_box(draw, x, y, width, edge, label, body, scale, body_size=8.0):
    xy = (*_pil_xy(x, y, scale), *_pil_xy(x + width, y + 92, scale))
    draw.rounded_rectangle(
        xy,
        radius=round(10 * scale),
        fill="white",
        outline=edge,
        width=max(2, round(1.5 * scale)),
    )
    _draw_pil_text(draw, x + 14, y + 24, label.upper(), 6.8, edge, scale, bold=True)
    _draw_pil_text(draw, x + 14, y + 61, body, body_size, CHARCOAL, scale, bold=True)


def build_png(source: Image.Image):
    scale = FIGURE_WIDTH_IN * PNG_DPI / BASE_WIDTH
    out = Image.new(
        "RGB",
        (round(BASE_WIDTH * scale), round(TOTAL_HEIGHT * scale)),
        "white",
    )
    art = source.resize(
        (round(BASE_WIDTH * scale), round(IMAGE_HEIGHT * scale)),
        Image.Resampling.LANCZOS,
    )
    out.paste(art, (0, 0))
    draw = ImageDraw.Draw(out)

    headings = [
        (18, "A  Matched events", "Same shortage; different causes"),
        (508, "B  Misconsolidation", "Distinct evidence → generic rule"),
        (870, "C  ScopeProbe audit", "Memory → attribution → later action"),
        (1440, "D  Evidence gate", "Route claims by target and time"),
    ]
    for x, title, subtitle in headings:
        _draw_pil_text(draw, x, 24, title, 9.0, CHARCOAL, scale, bold=True)
        _draw_pil_text(draw, x, 48, subtitle, 6.4, MID_GREY, scale)

    draw.rectangle(
        (*_pil_xy(0, IMAGE_HEIGHT, scale), *_pil_xy(BASE_WIDTH, TOTAL_HEIGHT, scale)),
        fill=PALE,
    )
    draw.line(
        (*_pil_xy(0, IMAGE_HEIGHT, scale), *_pil_xy(BASE_WIDTH, IMAGE_HEIGHT, scale)),
        fill=LIGHT_GREY,
        width=max(2, round(1.2 * scale)),
    )

    y = IMAGE_HEIGHT + 23
    _draw_pil_box(draw, 24, y, 230, GREEN, "Assigned role", '“You are Erin”', scale)
    _draw_pil_box(draw, 310, y, 300, BLUE, "Settlement", "winners include Erin", scale, 7.4)
    _draw_pil_box(draw, 668, y, 390, VERMILION, "Reflection", '“...bid strictly above Erin.”', scale)
    _draw_pil_box(draw, 1118, y, 280, ORANGE, "Later action", "escalating bids", scale, 7.4)

    for x in (277, 635, 1085):
        start = _pil_xy(x, y + 46, scale)
        end = _pil_xy(x + 24, y + 46, scale)
        draw.line((*start, *end), fill=MID_GREY, width=max(2, round(1.4 * scale)))
        ex, ey = end
        head = round(5 * scale)
        draw.polygon([(ex, ey), (ex - head, ey - head), (ex - head, ey + head)], fill=MID_GREY)

    badge_xy = (*_pil_xy(1445, y, scale), *_pil_xy(1875, y + 92, scale))
    draw.rounded_rectangle(
        badge_xy,
        radius=round(10 * scale),
        fill=PALE_RED,
        outline=VERMILION,
        width=max(2, round(1.5 * scale)),
    )
    _draw_pil_text(draw, 1462, y + 35, "8/15  Reflection", 10.0, VERMILION, scale, bold=True)
    _draw_pil_text(
        draw,
        1462,
        y + 68,
        "0/15 Full History   ·   0/15 scope-aware",
        6.9,
        CHARCOAL,
        scale,
    )

    out.save(PNG_OUT, dpi=(PNG_DPI, PNG_DPI), optimize=True)


def build_pdf(source: Image.Image):
    pdfmetrics.registerFont(TTFont("FigureArial", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("FigureArial-Bold", str(FONT_BOLD)))
    page_w = FIGURE_WIDTH_IN * 72
    unit = page_w / BASE_WIDTH
    page_h = TOTAL_HEIGHT * unit
    pdf = canvas.Canvas(str(PDF_OUT), pagesize=(page_w, page_h), pageCompression=1)

    def xpt(x):
        return x * unit

    def ypt(y):
        return page_h - y * unit

    def text(x, y, value, points, color, bold=False):
        pdf.setFillColor(HexColor(color))
        pdf.setFont("FigureArial-Bold" if bold else "FigureArial", points)
        pdf.drawString(xpt(x), ypt(y) - points * 0.35, value)

    def box(x, y, width, edge, label, body, body_size=8.0):
        pdf.setFillColor(HexColor("#FFFFFF"))
        pdf.setStrokeColor(HexColor(edge))
        pdf.setLineWidth(1.0)
        pdf.roundRect(xpt(x), ypt(y + 92), xpt(width), xpt(92), xpt(10), stroke=1, fill=1)
        text(x + 14, y + 24, label.upper(), 6.8, edge, True)
        text(x + 14, y + 61, body, body_size, CHARCOAL, True)

    pdf.drawImage(
        ImageReader(source),
        0,
        STRIP_HEIGHT * unit,
        width=page_w,
        height=IMAGE_HEIGHT * unit,
        preserveAspectRatio=False,
        mask="auto",
    )

    headings = [
        (18, "A  Matched events", "Same shortage; different causes"),
        (508, "B  Misconsolidation", "Distinct evidence → generic rule"),
        (870, "C  ScopeProbe audit", "Memory → attribution → later action"),
        (1440, "D  Evidence gate", "Route claims by target and time"),
    ]
    for x, title, subtitle in headings:
        text(x, 24, title, 9.0, CHARCOAL, True)
        text(x, 48, subtitle, 6.4, MID_GREY)

    pdf.setFillColor(HexColor(PALE))
    pdf.setStrokeColor(HexColor(PALE))
    pdf.rect(0, 0, page_w, STRIP_HEIGHT * unit, stroke=0, fill=1)
    pdf.setStrokeColor(HexColor(LIGHT_GREY))
    pdf.setLineWidth(0.8)
    pdf.line(0, STRIP_HEIGHT * unit, page_w, STRIP_HEIGHT * unit)

    y = IMAGE_HEIGHT + 23
    box(24, y, 230, GREEN, "Assigned role", '“You are Erin”')
    box(310, y, 300, BLUE, "Settlement", "winners include Erin", 7.4)
    box(668, y, 390, VERMILION, "Reflection", '“...bid strictly above Erin.”')
    box(1118, y, 280, ORANGE, "Later action", "escalating bids", 7.4)

    pdf.setStrokeColor(HexColor(MID_GREY))
    pdf.setFillColor(HexColor(MID_GREY))
    pdf.setLineWidth(0.9)
    for x in (277, 635, 1085):
        yy = ypt(y + 46)
        pdf.line(xpt(x), yy, xpt(x + 24), yy)
        pdf.drawPath(
            _triangle_path(pdf, xpt(x + 24), yy, xpt(5)),
            stroke=0,
            fill=1,
        )

    pdf.setFillColor(HexColor(PALE_RED))
    pdf.setStrokeColor(HexColor(VERMILION))
    pdf.setLineWidth(1.0)
    pdf.roundRect(xpt(1445), ypt(y + 92), xpt(430), xpt(92), xpt(10), stroke=1, fill=1)
    text(1462, y + 35, "8/15  Reflection", 10.0, VERMILION, True)
    text(1462, y + 68, "0/15 Full History   ·   0/15 scope-aware", 6.9, CHARCOAL)

    pdf.showPage()
    pdf.save()


def _triangle_path(pdf: canvas.Canvas, x: float, y: float, size: float):
    path = pdf.beginPath()
    path.moveTo(x, y)
    path.lineTo(x - size, y - size)
    path.lineTo(x - size, y + size)
    path.close()
    return path


def main():
    source = Image.open(SOURCE).convert("RGB").crop((0, 0, BASE_WIDTH, IMAGE_HEIGHT))
    build_png(source)
    build_pdf(source)


if __name__ == "__main__":
    main()

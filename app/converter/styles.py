from typing import Union

from openpyxl.styles import (Alignment, Border, Font, NamedStyle, PatternFill,
                             Side)

DEFAULT_BORDER = True
DEFAULT_BORDER_STYLE = 'thin'
DEFAULT_BORDER_COLOR = 'FF000000'
DEFAULT_FONT_NAME = 'Arial'
DEFAULT_FONT_SIZE = 11
DEFAULT_FONT_BOLD = False
DEFAULT_FONT_ITALIC = False
DEFAULT_FONT_VERTICAL_ALIGN = None
DEFAULT_FONT_UNDERLINE = 'none'
DEFAULT_STRIKE = False
DEFAULT_FONT_COLOR = 'FF000000'
DEFAULT_ALIGNMENT_WRAP_TEXT = True
DEFAULT_ALIGNMENT_HORIZONTAL = 'left'
DEFAULT_ALIGNMENT_VERTICAL = 'bottom'
DEFAULT_ALIGNMENT_TEXT_ROTATION = 0
DEFAULT_ALIGNMENT_INDENT = 0
DEFAULT_FILL = False
DEFAULT_FILL_BG_COLOR = 'D7D7D7'


def get_pattern_fill(bg_color: str):
    return PatternFill(start_color=bg_color, fill_type='solid')


def get_style(
        name: str = 'custom',
        border: bool = DEFAULT_BORDER,
        border_style: str = DEFAULT_BORDER_STYLE,
        border_color: str = DEFAULT_BORDER_COLOR,
        font_name: str = DEFAULT_FONT_NAME,
        font_size: int = DEFAULT_FONT_SIZE,
        font_bold: bool = DEFAULT_FONT_BOLD,
        font_italic: bool = DEFAULT_FONT_ITALIC,
        font_strike: bool = DEFAULT_STRIKE,
        font_vertical_align: Union[str, None] = DEFAULT_FONT_VERTICAL_ALIGN,
        font_underline: str = DEFAULT_FONT_UNDERLINE,
        font_color: str = DEFAULT_FONT_COLOR,
        alignment_wrap_text: bool = DEFAULT_ALIGNMENT_WRAP_TEXT,
        alignment_horizontal: str = DEFAULT_ALIGNMENT_HORIZONTAL,
        alignment_vertical: str = DEFAULT_ALIGNMENT_VERTICAL,
        alignment_text_rotation: int = DEFAULT_ALIGNMENT_TEXT_ROTATION,
        alignment_indent: int = DEFAULT_ALIGNMENT_INDENT,
        fill: bool = DEFAULT_FILL,
        fill_bg_color: str = DEFAULT_FILL_BG_COLOR
):
    """
    params:
    name: str Название стиля
    border: bool Граница
    border_style: str {
                        'dashDot','dashDotDot', 'dashed','dotted', 'double','hair', 'medium', 'mediumDashDot',
                        'mediumDashDotDot', 'mediumDashed', 'slantDashDot', 'thick', 'thin'
                        }
    border_color: str формат 'FF000000'
    font_name: str Название шрифта
    font_size: int Размер шрифта
    font_bold: bool Жирный шрифт
    font_italic: bool Курсив
    font_strike: bool Зачеркивание
    font_vertical_align: [str, None] Значение должно быть одним из {'baseline', 'subscript', 'superscript', None}
    font_underline: str Значение должно быть одним из {'double', 'doubleAccounting', 'single', 'singleAccounting'}
    font_color: str формат 'FF000000'
    alignment_wrap_text: bool
    alignment_horizontal: str Выравнивание по горизонтали {
    ‘fill’, ‘general’, ‘justify’, ‘center’, ‘left’, ‘centerContinuous’, ‘distributed’, ‘right’
    }
    alignment_vertical: str Выравнивание по вертикали {
    ‘justify’, ‘center’, ‘distributed’, ‘top’, ‘bottom’
    }
    alignment_text_rotation: int Значение от 0 до 180
    alignment_indent: int Отступ
    fill: bool Заливка
    fill_bg_color: str формат 'FF000000'
    """
    font = Font(
        name=font_name,
        size=font_size,
        bold=font_bold,
        italic=font_italic,
        vertAlign=font_vertical_align,
        underline=font_underline,
        strike=font_strike,
        color=font_color,
    )
    alignment = Alignment(
        wrap_text=alignment_wrap_text,
        horizontal=alignment_horizontal,
        vertical=alignment_vertical,
        text_rotation=alignment_text_rotation,
        indent=alignment_indent
    )
    style = NamedStyle(name=str(name))
    if fill:
        style.fill = get_pattern_fill(fill_bg_color)
    if border:
        side = Side(border_style=border_style, color=border_color)
        border = Border(left=side, right=side, top=side, bottom=side)
        style.border = border
    style.font = font
    style.alignment = alignment

    return style
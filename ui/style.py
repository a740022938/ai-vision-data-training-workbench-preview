"""
UI 样式入口
后续统一颜色 字体 间距 按钮风格都从这里走
"""

APP_BG = "#202124"
PANEL_BG = "#2B2D31"
TEXT_FG = "#F1F3F4"
MUTED_FG = "#BDC1C6"

ACCENT_COLOR = "#4EA1FF"
SUCCESS_COLOR = "#34A853"
WARNING_COLOR = "#FBBC05"
ERROR_COLOR = "#EA4335"

DEFAULT_FONT = ("Microsoft YaHei UI", 10)
TITLE_FONT = ("Microsoft YaHei UI", 12, "bold")
SMALL_FONT = ("Microsoft YaHei UI", 9)

PADDING_X = 8
PADDING_Y = 6
BUTTON_WIDTH = 12


def get_basic_style():
    return {
        "app_bg": APP_BG,
        "panel_bg": PANEL_BG,
        "text_fg": TEXT_FG,
        "muted_fg": MUTED_FG,
        "accent": ACCENT_COLOR,
        "success": SUCCESS_COLOR,
        "warning": WARNING_COLOR,
        "error": ERROR_COLOR,
        "default_font": DEFAULT_FONT,
        "title_font": TITLE_FONT,
        "small_font": SMALL_FONT,
        "padding_x": PADDING_X,
        "padding_y": PADDING_Y,
        "button_width": BUTTON_WIDTH,
    }

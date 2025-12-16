"""
ThemeManager Template for PySide6 Applications

Centralized theme manager - load JSON themes, generate QSS, and apply to the app.

Usage:
    from utils.theme_manager import load_theme, get_theme

    app = QApplication(sys.argv)
    load_theme(app, "themes/default.json")

    theme = get_theme()
    color = theme.get("colors.brand.primary")
"""

import json
from pathlib import Path
from typing import Any, Optional
from PySide6.QtWidgets import QApplication


class ThemeManager:
    """Centralized theme manager (singleton)."""

    _instance: Optional["ThemeManager"] = None
    _theme_data: dict = {}
    _qss_cache: str = ""

    def __new__(cls) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_theme(self, theme_path: str) -> None:
        """Load a JSON theme file.

        Args:
            theme_path: Path to the theme JSON file
        """
        path = Path(theme_path)
        if not path.exists():
            raise FileNotFoundError(f"Theme not found: {theme_path}")

        with open(path, "r", encoding="utf-8") as f:
            self._theme_data = json.load(f)

        self._generate_qss()

    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a theme value using dotted path notation.

        Args:
            key_path: Dotted key path (e.g. "colors.brand.primary")
            default: Default value if the key is missing

        Returns:
            Theme value or the default

        Example:
            theme.get("colors.brand.primary")  # "#3ECF8E"
            theme.get("spacing.md", 12)        # 12
        """
        keys = key_path.split(".")
        value = self._theme_data

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def _generate_qss(self) -> None:
        """Generate QSS from theme data."""
        colors = self._theme_data.get("colors", {})
        typography = self._theme_data.get("typography", {})
        spacing = self._theme_data.get("spacing", {})
        radius = self._theme_data.get("radius", {})

        # Extract colors
        primary = colors.get("brand", {}).get("primary", "#3ECF8E")
        secondary = colors.get("brand", {}).get("secondary", "#1DB7B0")
        accent = colors.get("brand", {}).get("accent", "#7C3AED")

        bg_primary = colors.get("background", {}).get("primary", "#FFFFFF")
        bg_secondary = colors.get("background", {}).get("secondary", "#F5F5F5")
        bg_tertiary = colors.get("background", {}).get("tertiary", "#EBEBEB")

        text_primary = colors.get("text", {}).get("primary", "#171717")
        text_secondary = colors.get("text", {}).get("secondary", "#737373")
        text_disabled = colors.get("text", {}).get("disabled", "#A3A3A3")

        border_default = colors.get("border", {}).get("default", "#E5E5E5")
        border_focus = colors.get("border", {}).get("focus", primary)

        success = colors.get("semantic", {}).get("success", "#10B981")
        warning = colors.get("semantic", {}).get("warning", "#F59E0B")
        error = colors.get("semantic", {}).get("error", "#EF4444")
        info = colors.get("semantic", {}).get("info", "#3B82F6")

        neutral = colors.get("neutral", {})
        neutral_300 = neutral.get("300", "#D4D4D4")
        neutral_800 = neutral.get("800", "#262626")

        # Extract typography
        font_family = typography.get("fontFamily", "Segoe UI, -apple-system, sans-serif")
        sizes = typography.get("sizes", {})
        font_xs = sizes.get("xs", 10)
        font_sm = sizes.get("sm", 12)
        font_base = sizes.get("base", 14)
        font_lg = sizes.get("lg", 16)
        font_xl = sizes.get("xl", 20)
        font_2xl = sizes.get("2xl", 24)

        # Extract spacing
        spacing_sm = spacing.get("sm", 8)
        spacing_md = spacing.get("md", 12)
        spacing_lg = spacing.get("lg", 16)

        # Extract border radius
        radius_sm = radius.get("sm", 4)
        radius_md = radius.get("md", 8)
        radius_lg = radius.get("lg", 12)

        self._qss_cache = f"""
        /* ===== Global Styles ===== */
        QWidget {{
            font-family: {font_family};
            font-size: {font_base}px;
            color: {text_primary};
        }}

        QMainWindow, QDialog {{
            background-color: {bg_primary};
        }}

        /* ===== Labels ===== */
        QLabel {{
            color: {text_primary};
            background: transparent;
        }}

        QLabel[variant="title"] {{
            font-size: {font_xl}px;
            font-weight: 600;
        }}

        QLabel[variant="subtitle"] {{
            font-size: {font_lg}px;
            font-weight: 500;
        }}

        QLabel[variant="caption"] {{
            font-size: {font_sm}px;
            color: {text_secondary};
        }}

        QLabel[status="success"] {{
            color: {success};
        }}

        QLabel[status="warning"] {{
            color: {warning};
        }}

        QLabel[status="error"] {{
            color: {error};
        }}

        /* ===== Buttons ===== */
        QPushButton {{
            background-color: {bg_secondary};
            color: {text_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            padding: {spacing_md}px {spacing_md * 2}px;
            font-weight: 500;
            min-height: 36px;
        }}

        QPushButton:hover {{
            background-color: {border_default};
        }}

        QPushButton:pressed {{
            background-color: {neutral_300};
        }}

        QPushButton:disabled {{
            background-color: {bg_secondary};
            color: {text_disabled};
            border-color: {bg_secondary};
        }}

        /* Primary Button */
        QPushButton[variant="primary"] {{
            background-color: {primary};
            color: white;
            border: none;
        }}

        QPushButton[variant="primary"]:hover {{
            background-color: {self._darken(primary, 10)};
        }}

        QPushButton[variant="primary"]:pressed {{
            background-color: {self._darken(primary, 20)};
        }}

        /* Secondary Button */
        QPushButton[variant="secondary"] {{
            background-color: transparent;
            color: {primary};
            border: 1px solid {primary};
        }}

        QPushButton[variant="secondary"]:hover {{
            background-color: {self._lighten(primary, 90)};
        }}

        /* Danger Button */
        QPushButton[variant="danger"] {{
            background-color: {error};
            color: white;
            border: none;
        }}

        QPushButton[variant="danger"]:hover {{
            background-color: {self._darken(error, 10)};
        }}

        /* Ghost Button */
        QPushButton[variant="ghost"] {{
            background-color: transparent;
            color: {text_primary};
            border: none;
        }}

        QPushButton[variant="ghost"]:hover {{
            background-color: {bg_secondary};
        }}

        /* ===== Input Fields ===== */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            padding: {spacing_md}px;
            selection-background-color: {primary};
            selection-color: white;
        }}

        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {border_focus};
        }}

        QLineEdit:disabled, QTextEdit:disabled {{
            background-color: {bg_secondary};
            color: {text_disabled};
        }}

        QLineEdit[state="error"], QTextEdit[state="error"] {{
            border-color: {error};
        }}

        /* ===== SpinBox ===== */
        QSpinBox, QDoubleSpinBox {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            padding: {spacing_sm}px;
            min-height: 36px;
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {border_focus};
        }}

        QSpinBox::up-button, QDoubleSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border: none;
        }}

        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border: none;
        }}

        /* ===== ComboBox ===== */
        QComboBox {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            padding: {spacing_md}px;
            min-height: 36px;
        }}

        QComboBox:hover {{
            border-color: {primary};
        }}

        QComboBox:focus {{
            border-color: {border_focus};
        }}

        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {text_secondary};
            margin-right: 10px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            selection-background-color: {primary};
            selection-color: white;
            outline: none;
        }}

        /* ===== GroupBox (Cards) ===== */
        QGroupBox {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_lg}px;
            margin-top: 16px;
            padding-top: 16px;
            font-weight: 500;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            color: {text_primary};
        }}

        /* ===== Tables ===== */
        QTableWidget, QTableView {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            gridline-color: {border_default};
            outline: none;
        }}

        QTableWidget::item, QTableView::item {{
            padding: {spacing_md}px;
        }}

        QTableWidget::item:selected, QTableView::item:selected {{
            background-color: {primary};
            color: white;
        }}

        QTableWidget::item:hover, QTableView::item:hover {{
            background-color: {bg_secondary};
        }}

        QHeaderView::section {{
            background-color: {bg_secondary};
            color: {text_primary};
            padding: {spacing_md}px;
            border: none;
            border-bottom: 1px solid {border_default};
            font-weight: 600;
        }}

        /* ===== Lists ===== */
        QListWidget, QListView {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            outline: none;
        }}

        QListWidget::item, QListView::item {{
            padding: {spacing_md}px;
        }}

        QListWidget::item:selected, QListView::item:selected {{
            background-color: {primary};
            color: white;
        }}

        QListWidget::item:hover, QListView::item:hover {{
            background-color: {bg_secondary};
        }}

        /* ===== Tree ===== */
        QTreeWidget, QTreeView {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            outline: none;
        }}

        QTreeWidget::item, QTreeView::item {{
            padding: {spacing_sm}px;
        }}

        QTreeWidget::item:selected, QTreeView::item:selected {{
            background-color: {primary};
            color: white;
        }}

        /* ===== ScrollBar ===== */
        QScrollBar:vertical {{
            background-color: {bg_secondary};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}

        QScrollBar::handle:vertical {{
            background-color: {neutral_300};
            border-radius: 6px;
            min-height: 30px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {text_secondary};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}

        QScrollBar:horizontal {{
            background-color: {bg_secondary};
            height: 12px;
            border-radius: 6px;
            margin: 0;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {neutral_300};
            border-radius: 6px;
            min-width: 30px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {text_secondary};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}

        /* ===== Progress Bar ===== */
        QProgressBar {{
            background-color: {bg_secondary};
            border: none;
            border-radius: {radius_md}px;
            text-align: center;
            height: 20px;
        }}

        QProgressBar::chunk {{
            background-color: {primary};
            border-radius: {radius_md}px;
        }}

        /* ===== Checkbox & Radio ===== */
        QCheckBox, QRadioButton {{
            spacing: 8px;
        }}

        QCheckBox::indicator, QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {border_default};
            background-color: {bg_primary};
        }}

        QCheckBox::indicator {{
            border-radius: {radius_sm}px;
        }}

        QRadioButton::indicator {{
            border-radius: 9px;
        }}

        QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
            border-color: {primary};
        }}

        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: {primary};
            border-color: {primary};
        }}

        QCheckBox::indicator:disabled, QRadioButton::indicator:disabled {{
            border-color: {bg_tertiary};
            background-color: {bg_secondary};
        }}

        /* ===== Slider ===== */
        QSlider::groove:horizontal {{
            border: none;
            height: 6px;
            background-color: {bg_secondary};
            border-radius: 3px;
        }}

        QSlider::handle:horizontal {{
            background-color: {primary};
            border: none;
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }}

        QSlider::handle:horizontal:hover {{
            background-color: {self._darken(primary, 10)};
        }}

        /* ===== Tab Widget ===== */
        QTabWidget::pane {{
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            background-color: {bg_primary};
            top: -1px;
        }}

        QTabBar::tab {{
            background-color: {bg_secondary};
            padding: {spacing_md}px {spacing_md * 2}px;
            border: 1px solid {border_default};
            border-bottom: none;
            border-top-left-radius: {radius_md}px;
            border-top-right-radius: {radius_md}px;
        }}

        QTabBar::tab:selected {{
            background-color: {bg_primary};
            border-bottom: 2px solid {primary};
        }}

        QTabBar::tab:hover:!selected {{
            background-color: {bg_tertiary};
        }}

        /* ===== Menu ===== */
        QMenuBar {{
            background-color: {bg_primary};
            border-bottom: 1px solid {border_default};
            padding: 4px;
        }}

        QMenuBar::item {{
            padding: {spacing_sm}px {spacing_md}px;
            border-radius: {radius_sm}px;
        }}

        QMenuBar::item:selected {{
            background-color: {bg_secondary};
        }}

        QMenu {{
            background-color: {bg_primary};
            border: 1px solid {border_default};
            border-radius: {radius_md}px;
            padding: {spacing_sm}px;
        }}

        QMenu::item {{
            padding: {spacing_md}px {spacing_lg}px;
            border-radius: {radius_sm}px;
        }}

        QMenu::item:selected {{
            background-color: {primary};
            color: white;
        }}

        QMenu::separator {{
            height: 1px;
            background-color: {border_default};
            margin: {spacing_sm}px 0;
        }}

        /* ===== ToolTip ===== */
        QToolTip {{
            background-color: {neutral_800};
            color: white;
            border: none;
            border-radius: {radius_sm}px;
            padding: {spacing_sm}px;
            font-size: {font_sm}px;
        }}

        /* ===== StatusBar ===== */
        QStatusBar {{
            background-color: {bg_secondary};
            border-top: 1px solid {border_default};
        }}

        QStatusBar::item {{
            border: none;
        }}

        /* ===== ToolBar ===== */
        QToolBar {{
            background-color: {bg_primary};
            border-bottom: 1px solid {border_default};
            padding: {spacing_sm}px;
            spacing: {spacing_sm}px;
        }}

        QToolBar::separator {{
            width: 1px;
            background-color: {border_default};
            margin: {spacing_sm}px;
        }}

        QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: {radius_sm}px;
            padding: {spacing_sm}px;
        }}

        QToolButton:hover {{
            background-color: {bg_secondary};
        }}

        QToolButton:pressed {{
            background-color: {neutral_300};
        }}

        /* ===== Dock Widget ===== */
        QDockWidget {{
            titlebar-close-icon: none;
            titlebar-normal-icon: none;
        }}

        QDockWidget::title {{
            background-color: {bg_secondary};
            padding: {spacing_md}px;
            border-bottom: 1px solid {border_default};
        }}

        /* ===== Splitter ===== */
        QSplitter::handle {{
            background-color: {border_default};
        }}

        QSplitter::handle:horizontal {{
            width: 2px;
        }}

        QSplitter::handle:vertical {{
            height: 2px;
        }}

        QSplitter::handle:hover {{
            background-color: {primary};
        }}
        """

    def _darken(self, hex_color: str, percent: int) -> str:
        """Darken a color.

        Args:
            hex_color: Hex color code (#RRGGBB)
            percent: Percentage to darken (0–100)

        Returns:
            Darkened color code
        """
        hex_color = hex_color.lstrip("#")
        r = max(0, int(int(hex_color[0:2], 16) * (100 - percent) / 100))
        g = max(0, int(int(hex_color[2:4], 16) * (100 - percent) / 100))
        b = max(0, int(int(hex_color[4:6], 16) * (100 - percent) / 100))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _lighten(self, hex_color: str, percent: int) -> str:
        """Lighten a color.

        Args:
            hex_color: Hex color code (#RRGGBB)
            percent: Percentage to lighten (0–100)

        Returns:
            Lightened color code
        """
        hex_color = hex_color.lstrip("#")
        r = min(255, int(int(hex_color[0:2], 16) + (255 - int(hex_color[0:2], 16)) * percent / 100))
        g = min(255, int(int(hex_color[2:4], 16) + (255 - int(hex_color[2:4], 16)) * percent / 100))
        b = min(255, int(int(hex_color[4:6], 16) + (255 - int(hex_color[4:6], 16)) * percent / 100))
        return f"#{r:02x}{g:02x}{b:02x}"

    def apply_to_app(self, app: QApplication) -> None:
        """Apply the theme to the application.

        Args:
            app: QApplication instance
        """
        app.setStyleSheet(self._qss_cache)

    @property
    def qss(self) -> str:
        """Return the generated QSS."""
        return self._qss_cache

    @property
    def data(self) -> dict:
        """Return the raw theme data."""
        return self._theme_data


# Singleton instance
_theme_manager = ThemeManager()


def get_theme() -> ThemeManager:
    """Return the ThemeManager instance.

    Returns:
        ThemeManager singleton instance
    """
    return _theme_manager


def load_theme(app: QApplication, theme_path: str) -> ThemeManager:
    """Load a theme and apply it to the app.

    Args:
        app: QApplication instance
        theme_path: Path to the theme JSON file

    Returns:
        ThemeManager instance

    Example:
        app = QApplication(sys.argv)
        load_theme(app, "themes/default.json")
    """
    manager = get_theme()
    manager.load_theme(theme_path)
    manager.apply_to_app(app)
    return manager

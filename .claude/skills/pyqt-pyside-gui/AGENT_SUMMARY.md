# PySide6 GUI Development - Agent Summary

> Core reference document for the Claude Agent

---

## 🎯 5 Core Principles

1. **JSON Theme System** - define all colors and spacing only in JSON
2. **ThemeManager Singleton** - load themes and auto-generate QSS
3. **Property Variant** - style widgets with `setProperty("variant", "primary")`
4. **Load Theme Right After QApplication** - always load before creating any windows
5. **Component Reuse** - build a theme-based widget library

---

## ⚡ Quick Start (3 Steps)

```python
# Step 1: Load the theme immediately after creating QApplication
from utils.theme_manager import load_theme, get_theme
app = QApplication(sys.argv)
load_theme(app, "themes/default.json")

# Step 2: Using theme values
theme = get_theme()
primary_color = theme.get("colors.brand.primary", "#007bff")

# Step 3: Applying Property Variant
button = QPushButton("확인")
button.setProperty("variant", "primary")
```

---

## ✅ Best Practices Checklist

### Required
- ✅ Call `load_theme()` right after creating `QApplication`
- ✅ Always use `theme.get("colors.xxx")` for colors
- ✅ Set `setObjectName()` on widgets
- ✅ Write docstrings
- ✅ Apply styles using Property Variant

### Prohibited
- ❌ Hardcoded colors (`#ffffff`, `rgb(255,255,255)`)
- ❌ Loading the theme after windows are created
- ❌ Calling `setStyleSheet()` directly on individual widgets
- ❌ Meaningless variable names (`widget1`, `button2`)
- ❌ Using setStyleSheet inside QGroupBox

### Common Mistakes
1. **Theme load order** - must load before creating any windows
2. **No refresh after changing properties** - need `style().unpolish(widget); style().polish(widget)`
3. **Dot-notation mistakes** - always provide a default: `theme.get("key", "default")`

---

## 📁 File Reference Map

| Question/Task | Reference File |
|--------------|----------------|
| Create a new theme | `references/theme_template.json` |
| Implement ThemeManager | `references/theme_manager_template.py` |
| QSS selectors/variants | `references/qss_systematic_guide.md` |
| Create custom widgets | `references/advanced_patterns.md` |
| Component library | `ui_components/components.py` |
| Validate code quality | `tools/gui_analyzer.py` |
| Multithreading | `examples/threaded_app.py` |
| Table implementation | `examples/table_model.py` |
| Dialogs | `examples/dialog_examples.py` |

---

## 🎨 JSON Theme Basic Structure

```json
{
  "colors": {
    "brand": {
      "primary": "#007bff",
      "secondary": "#6c757d",
      "accent": "#28a745"
    },
    "background": {
      "primary": "#ffffff",
      "secondary": "#f8f9fa",
      "tertiary": "#e9ecef"
    },
    "text": {
      "primary": "#212529",
      "secondary": "#6c757d",
      "disabled": "#adb5bd"
    },
    "semantic": {
      "success": "#28a745",
      "warning": "#ffc107",
      "error": "#dc3545",
      "info": "#17a2b8"
    }
  },
  "typography": {
    "fontFamily": "Segoe UI",
    "sizes": {
      "sm": "11px",
      "base": "13px",
      "lg": "15px",
      "xl": "18px"
    }
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "radius": {
    "sm": "4px",
    "md": "8px",
    "lg": "12px"
  }
}
```

---

## 🔧 Property Variant Usage

### QSS Definition (Global)
```css
/* Primary button */
QPushButton[variant="primary"] {
    background-color: {colors.brand.primary};
    color: white;
    border: none;
    border-radius: {radius.md};
    padding: {spacing.sm} {spacing.md};
}

/* Secondary button */
QPushButton[variant="secondary"] {
    background-color: transparent;
    color: {colors.brand.primary};
    border: 1px solid {colors.brand.primary};
}

/* Danger button */
QPushButton[variant="danger"] {
    background-color: {colors.semantic.error};
    color: white;
}
```

### Python Usage
```python
# Variant settings
button.setProperty("variant", "primary")

# Style update required for dynamic changes
button.setProperty("variant", "danger")
button.style().unpolish(button)
button.style().polish(button)
```

---

## 🛠️ Tool Usage

### GUI Analyzer (Static Analysis)
```bash
# Single file analysis
python .claude/skills/pyqt-pyside-gui/tools/gui_analyzer.py path/to/file.py

# Output: Generate HTML report
# - Widget tree visualization
# - Issue list (size, visibility, layout, naming)
# - Best Practices checklist
```

### Debugging Workflow
```
During development: Hot Reload (live editing)
    ↓
Debugging: Visual Debugger (runtime analysis)
    ↓
Verification: GUI Analyzer (static analysis)
    ↓
Deployment
```

---

## 📋 Basic App Template

```python
"""PySide6 Basic Application Template"""
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from utils.theme_manager import load_theme, get_theme


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application")
        self.setMinimumSize(800, 600)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Add widgets here
        self._setup_ui(layout)

    def _setup_ui(self, layout):
        """UI configuration."""
        pass


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("MyApp")

    # Theme loading (before window creation!)
    load_theme(app, "themes/default.json")

    # Main window creation and display
    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
```

---

## 🔍 Common Imports

```python
# Qt Core
from PySide6.QtCore import Qt, Signal, Slot, QThread, QTimer, QSettings

# Qt Widgets
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QComboBox, QCheckBox, QRadioButton, QSpinBox,
    QTableView, QListView, QTreeView,
    QMessageBox, QFileDialog,
    QStatusBar, QMenuBar, QToolBar,
    QGroupBox, QFrame, QScrollArea, QSplitter
)

# Qt GUI
from PySide6.QtGui import QFont, QIcon, QPixmap, QColor, QPalette

# Theme
from utils.theme_manager import load_theme, get_theme
```

---

## 📊 Styling by Widget Type

### Input Fields
```python
input_field = QLineEdit()
input_field.setPlaceholderText("입력하세요")
input_field.setProperty("variant", "default")  # or "error"
```

### Card Container
```python
card = QFrame()
card.setProperty("variant", "elevated")  # or "outlined"
card.setObjectName("card")
```

### Label Variants
```python
# Heading
label = QLabel("Title")
label.setProperty("variant", "heading")

# Caption
caption = QLabel("Description text")
caption.setProperty("variant", "caption")

# Error
error = QLabel("Error message")
error.setProperty("variant", "error")
```

---

## 🚨 Troubleshooting

### Styles not applied
1. Check that the theme is loaded
2. Check for typos in property names
3. Check that the selector exists in QSS
4. Check whether `unpolish/polish` needs to be called

### Widget not visible
1. Check if `show()` has been called
2. Check if the widget has been added to a layout
3. Check that the size is not zero (`setMinimumSize`)
4. Check that the parent widget exists

### Theme value not found
```python
# Incorrect
color = theme.get("colors.brand.primary")  # KeyError possible

# Correct
color = theme.get("colors.brand.primary", "#007bff")  # provide default
```

---

> **Full documentation reference:** `skill.md` (complete guide)


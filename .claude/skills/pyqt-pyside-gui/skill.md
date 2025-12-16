---
name: pyqt-pyside-gui
description: PySide6 GUI development guide with theme system, component library, QSS styling, and threading patterns.
---

# PySide6 GUI Development

This is a guide for building production-grade desktop apps using PySide6.

## Core Principles

1. **JSON Theme System**: define all colors and spacing in JSON
2. **ThemeManager**: load themes and auto-generate QSS
3. **Property Variant**: style with `setProperty("variant", "primary")`
4. **Component Reuse**: build app-specific themed components

---

## Quick Start

### 1. Load Theme (Required)

```python
from utils.theme_manager import load_theme, get_theme

app = QApplication(sys.argv)
load_theme(app, "themes/default.json")  # Right after creating the app!

window = MainWindow()
window.show()
```

### 2. Use Theme Values

```python
theme = get_theme()
primary = theme.get("colors.brand.primary")
spacing = theme.get("spacing.md", 12)
```

### 3. Apply Property Variants

```python
button = QPushButton("Save")
button.setProperty("variant", "primary")

label = QLabel("Error message")
label.setProperty("status", "error")
```

---

## Project Structure

```
your_app/
├── main.py
├── themes/
│   └── default.json        # Theme definition
├── utils/
│   └── theme_manager.py    # ThemeManager class
├── widgets/
│   └── themed_components.py # Themed components
└── views/
    └── main_window.py
```

---

## JSON Theme Structure

```json
{
  "colors": {
    "brand": { "primary": "#3ECF8E", "secondary": "#1DB7B0" },
    "background": { "primary": "#FFFFFF", "secondary": "#F5F5F5" },
    "text": { "primary": "#171717", "secondary": "#737373" },
    "semantic": { "success": "#10B981", "error": "#EF4444" }
  },
  "typography": {
    "fontFamily": "Segoe UI",
    "sizes": { "sm": 12, "base": 14, "lg": 16, "xl": 20 }
  },
  "spacing": { "sm": 8, "md": 12, "lg": 16, "xl": 24 },
  "radius": { "sm": 4, "md": 8, "lg": 12 }
}
```

---

## Styling Patterns

### QSS Variant Selectors

```css
/* Default button */
QPushButton {
    background-color: #F5F5F5;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    padding: 8px 16px;
}

/* Primary Variant */
QPushButton[variant="primary"] {
    background-color: #3ECF8E;
    color: white;
    border: none;
}

/* Status Labels */
QLabel[status="success"] { color: #10B981; }
QLabel[status="error"] { color: #EF4444; }
```

### Dynamic Style Changes

```python
# Refresh style after changing properties
button.setProperty("variant", "danger")
button.style().unpolish(button)
button.style().polish(button)
```

---

## Threading

```python
class Worker(QThread):
    progress = Signal(int)
    result = Signal(object)

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.progress.emit(i)
        self.result.emit(final_result)

# Usage
self.worker = Worker()
self.worker.progress.connect(self.update_progress)
self.worker.result.connect(self.handle_result)
self.worker.start()
```

---

## Best Practices

### Required

- [ ] Call `load_theme()` right after creating `QApplication`
- [ ] Define all colors only in the theme JSON
- [ ] Use property variants for style changes
- [ ] Apply descendant styles for QGroupBox in MainWindow

### Forbidden

- [ ] Hardcoded colors (e.g., using `#3498db` directly)
- [ ] Loading theme after window creation
- [ ] Applying full stylesheets to individual widgets

---

## Common Mistakes

### 1. Theme Load Order

```python
# ❌ Wrong
window = MainWindow()
load_theme(app, "theme.json")

# ✅ Correct
load_theme(app, "theme.json")
window = MainWindow()
```

### 2. Property Style Not Applied

```python
# ❌ Only setting property
button.setProperty("variant", "primary")

# ✅ Refresh style after setting property
button.setProperty("variant", "primary")
button.style().unpolish(button)
button.style().polish(button)
```

### 3. QGroupBox Inner Styles

```python
# ❌ setStyleSheet inside GroupBox
class MyGroupBox(QGroupBox):
    def __init__(self):
        self.setStyleSheet("QPushButton { ... }")  # Does not work

# ✅ Apply from MainWindow/parent
class MainWindow(QMainWindow):
    def __init__(self):
        # Define styles at app level
        ...
```

---

## AI Request Guide

### Good Requests

```python
"Change colors.brand.primary in themes/default.json to #7C3AED"

"Add a variant='success' style for QPushButton:
- background: semantic.success color
- 10% darker on hover"

"Create a FormField component:
- QLabel + QLineEdit
- show * on label when required
- red border in error state"
```

### Bad Requests

```
"Make the button blue"  # Which blue? Which theme variable?
"The form looks weird"  # What exactly looks wrong?
"Fix the colors"        # Which file? Which colors?
```

---

## References

### Core Guides

- **[qss_systematic_guide.md](references/qss_systematic_guide.md)** - Systematic QSS usage (selectors, best practices)
- **[theme_manager_template.py](references/theme_manager_template.py)** - Full ThemeManager implementation
- **[theme_template.json](references/theme_template.json)** - JSON theme template

### Additional References

- **[json_theme_guide.md](references/json_theme_guide.md)** - Detailed JSON theme guide
- **[component_library_guide.md](references/component_library_guide.md)** - Component library usage
- **[advanced_patterns.md](references/advanced_patterns.md)** - Advanced patterns (animation, drag & drop, settings)

---

## Base Template

```python
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
from utils.theme_manager import load_theme, get_theme


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.setMinimumSize(800, 600)
        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        theme = get_theme()
        spacing = theme.get("spacing.lg", 16)

        layout = QVBoxLayout(central)
        layout.setSpacing(spacing)
        layout.setContentsMargins(spacing, spacing, spacing, spacing)

        # Header
        header = QLabel("Welcome")
        header.setProperty("variant", "title")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Button
        btn = QPushButton("시작하기")
        btn.setProperty("variant", "primary")
        btn.clicked.connect(self._on_start)
        layout.addWidget(btn)

        layout.addStretch()

    def _on_start(self):
        print("시작!")


def main():
    app = QApplication(sys.argv)
    load_theme(app, str(PROJECT_ROOT / "themes" / "default.json"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

---

## Standard Imports

```python
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit,
    QComboBox, QSpinBox, QCheckBox, QRadioButton,
    QGroupBox, QTabWidget, QScrollArea, QStackedWidget,
    QTableWidget, QListWidget, QTreeWidget,
    QMessageBox, QFileDialog, QInputDialog
)
from PySide6.QtCore import Qt, Signal, Slot, QThread, QTimer
from PySide6.QtGui import QIcon, QAction, QFont, QPixmap
```


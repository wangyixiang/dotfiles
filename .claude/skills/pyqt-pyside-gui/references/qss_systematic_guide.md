# PySide6 QSS Systematic Application Guide

This guide explains how to build a systematic QSS (Qt Style Sheet) system for high‑quality PySide6 GUIs.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Architecture](#architecture)
3. [Theme System Design](#theme-system-design)
4. [QSS Authoring Rules](#qss-authoring-rules)
5. [Component Styling](#component-styling)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Core Principles

### 1. Single Source of Truth

All design tokens must be defined in a single **JSON theme file**.

```python
# ❌ Bad: hardcoded
button.setStyleSheet("background-color: #3498db;")

# ✅ Good: read from theme
theme = get_theme()
color = theme.get("colors.brand.primary")
```

### 2. Variable-Based Design System

Define colors, spacing, fonts, etc. as semantic variables.

```json
{
  "colors": {
    "brand": { "primary": "#3ECF8E" },
    "semantic": { "success": "#10B981", "error": "#EF4444" }
  },
  "spacing": { "sm": 8, "md": 12, "lg": 16 },
  "radius": { "sm": 4, "md": 8 }
}
```

### 3. Hierarchical Style Structure

```
Global (App) → Container (Card) → Component (Button) → State (Hover)
```

### 4. Property-Based Variant System

```python
button.setProperty("variant", "primary")  # QSS selector [variant="primary"]
```

---

## Architecture

### Recommended Project Structure

```
your_app/
├── main.py                    # App entry point
├── themes/
│   ├── default.json           # Default light theme
│   ├── dark.json              # Dark theme (optional)
│   └── components/            # Component-specific QSS (optional)
│       ├── buttons.qss
│       └── inputs.qss
├── utils/
│   ├── __init__.py
│   └── theme_manager.py       # ThemeManager class
├── widgets/
│   ├── __init__.py
│   └── themed_components.py   # Themed widgets
└── views/
    └── main_window.py
```

### Core Components

1. **ThemeManager**: JSON → QSS generation → apply to app
2. **Theme JSON**: design token definitions
3. **Themed Widgets**: property-based variants

---

## Theme System Design

### JSON Theme Structure

```json
{
  "name": "App Theme",
  "version": "1.0.0",

  "colors": {
    "brand": {
      "primary": "#3ECF8E",
      "secondary": "#1DB7B0",
      "accent": "#7C3AED"
    },
    "background": {
      "primary": "#FFFFFF",
      "secondary": "#F5F5F5",
      "tertiary": "#EBEBEB"
    },
    "text": {
      "primary": "#171717",
      "secondary": "#737373",
      "disabled": "#A3A3A3"
    },
    "border": {
      "default": "#E5E5E5",
      "focus": "#3ECF8E"
    },
    "semantic": {
      "success": "#10B981",
      "warning": "#F59E0B",
      "error": "#EF4444",
      "info": "#3B82F6"
    },
    "neutral": {
      "50": "#FAFAFA",
      "100": "#F5F5F5",
      "200": "#E5E5E5",
      "300": "#D4D4D4",
      "400": "#A3A3A3",
      "500": "#737373",
      "600": "#525252",
      "700": "#404040",
      "800": "#262626",
      "900": "#171717"
    }
  },

  "typography": {
    "fontFamily": "Segoe UI, -apple-system, sans-serif",
    "sizes": {
      "xs": 10,
      "sm": 12,
      "base": 14,
      "lg": 16,
      "xl": 20,
      "2xl": 24,
      "3xl": 30
    },
    "weights": {
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    }
  },

  "spacing": {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "2xl": 32
  },

  "radius": {
    "none": 0,
    "sm": 4,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "full": 9999
  },

  "shadows": {
    "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px rgba(0, 0, 0, 0.15)"
  },

  "components": {
    "button": {
      "minHeight": 36,
      "paddingX": 16,
      "paddingY": 8
    },
    "input": {
      "minHeight": 40,
      "padding": 12
    },
    "card": {
      "padding": 16,
      "borderRadius": 12
    }
  }
}
```

### ThemeManager Usage

```python
from utils.theme_manager import load_theme, get_theme

# 1. Load theme right after creating the app
app = QApplication(sys.argv)
load_theme(app, "themes/default.json")

# 2. Read theme values anywhere
theme = get_theme()
primary = theme.get("colors.brand.primary")
spacing = theme.get("spacing.md", 12)  # with default
```

---

## QSS Authoring Rules

### Selector Types

```css
/* 1. Type selector - applies to all widgets of that type */
QPushButton { }

/* 2. ID selector - based on objectName */
#submitButton { }

/* 3. Property selector - based on properties */
QPushButton[variant="primary"] { }
QLabel[status="error"] { }

/* 4. State selector - widget states */
QPushButton:hover { }
QPushButton:pressed { }
QPushButton:disabled { }
QPushButton:checked { }
QPushButton:focus { }

/* 5. Descendant selectors */
QGroupBox QPushButton { }      /* all descendants */
QGroupBox > QPushButton { }    /* direct children */

/* 6. Subcontrols */
QComboBox::drop-down { }
QScrollBar::handle:vertical { }
QCheckBox::indicator { }
```

### Priority Rules

1. Inline `setStyleSheet()` > `app.setStyleSheet()`
2. ID selector > property selector > type selector
3. More specific selectors win

### Supported Properties

```css
/* Box model */
margin: 10px;
padding: 8px 16px;
border: 1px solid #E5E5E5;
border-radius: 8px;

/* Colors */
background-color: #FFFFFF;
color: #171717;
selection-background-color: #3ECF8E;
selection-color: white;

/* Fonts */
font-family: "Segoe UI";
font-size: 14px;
font-weight: 500;

/* Size */
min-height: 36px;
max-width: 200px;

/* Alignment */
text-align: center;
```

### ⚠️ Differences from CSS

- No `box-shadow` (use images instead)
- No `flex` or `grid` layouts
- Limited `transition`/`animation` support
- Some properties only work on specific widgets

---

## Component Styling

### QPushButton

```css
QPushButton {
    background-color: #F5F5F5;
    color: #171717;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
    min-height: 36px;
}

QPushButton:hover {
    background-color: #E5E5E5;
}

QPushButton:pressed {
    background-color: #D4D4D4;
}

QPushButton:disabled {
    background-color: #F5F5F5;
    color: #A3A3A3;
}

/* Variants */
QPushButton[variant="primary"] {
    background-color: #3ECF8E;
    color: white;
    border: none;
}

QPushButton[variant="primary"]:hover {
    background-color: #35b87d;
}

QPushButton[variant="secondary"] {
    background-color: transparent;
    color: #3ECF8E;
    border: 1px solid #3ECF8E;
}

QPushButton[variant="danger"] {
    background-color: #EF4444;
    color: white;
    border: none;
}
```

### QLineEdit / QTextEdit

```css
QLineEdit, QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    padding: 12px;
    selection-background-color: #3ECF8E;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #3ECF8E;
}

QLineEdit:disabled {
    background-color: #F5F5F5;
    color: #A3A3A3;
}

QLineEdit[state="error"] {
    border-color: #EF4444;
}
```

### QComboBox

```css
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    padding: 8px 12px;
    min-height: 36px;
}

QComboBox:hover {
    border-color: #3ECF8E;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #737373;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    selection-background-color: #3ECF8E;
    selection-color: white;
}
```

### QGroupBox (Card)

```css
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 12px;
    margin-top: 16px;
    padding-top: 16px;
    font-weight: 500;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #171717;
}
```

### QTableWidget

```css
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    gridline-color: #E5E5E5;
}

QTableWidget::item {
    padding: 12px;
}

QTableWidget::item:selected {
    background-color: #3ECF8E;
    color: white;
}

QHeaderView::section {
    background-color: #F5F5F5;
    color: #171717;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #E5E5E5;
    font-weight: 600;
}
```

### QScrollBar

```css
QScrollBar:vertical {
    background-color: #F5F5F5;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #D4D4D4;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #A3A3A3;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar:horizontal {
    background-color: #F5F5F5;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #D4D4D4;
    border-radius: 6px;
    min-width: 30px;
}
```

### QCheckBox / QRadioButton

```css
QCheckBox, QRadioButton {
    spacing: 8px;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #E5E5E5;
    background-color: #FFFFFF;
}

QCheckBox::indicator {
    border-radius: 4px;
}

QRadioButton::indicator {
    border-radius: 9px;
}

QCheckBox::indicator:checked,
QRadioButton::indicator:checked {
    background-color: #3ECF8E;
    border-color: #3ECF8E;
}
```

### QProgressBar

```css
QProgressBar {
    background-color: #F5F5F5;
    border: none;
    border-radius: 8px;
    text-align: center;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #3ECF8E;
    border-radius: 8px;
}
```

### QTabWidget

```css
QTabWidget::pane {
    border: 1px solid #E5E5E5;
    border-radius: 8px;
    background-color: #FFFFFF;
}

QTabBar::tab {
    background-color: #F5F5F5;
    padding: 12px 24px;
    border: 1px solid #E5E5E5;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QTabBar::tab:selected {
    background-color: #FFFFFF;
    border-bottom: 2px solid #3ECF8E;
}
```

---

## Best Practices

### ✅ Essential Checklist

#### Styling
- [ ] Define all colors only in the theme JSON
- [ ] Call `load_theme()` right after creating `QApplication`
- [ ] Use `setProperty()` for variants
- [ ] Apply descendant styles for QGroupBox from the parent (MainWindow)

#### Structure
- [ ] Use hierarchical JSON (`colors.brand.primary`)
- [ ] Use semantic names (`success`, `warning`, `error`)
- [ ] Split QSS into component sections
- [ ] Version your themes

#### Maintainability
- [ ] Set `setObjectName()` on all widgets
- [ ] Document the purpose of theme variables
- [ ] Prepare for dark mode by separating themes

### Styling Order

```python
# 1. Create app
app = QApplication(sys.argv)

# 2. Load theme (must be before window creation)
load_theme(app, "themes/default.json")

# 3. Create and show window
window = MainWindow()
window.show()

# 4. Event loop
sys.exit(app.exec())
```

### Property Variant Pattern

```python
class ThemedButton(QPushButton):
    def __init__(self, text: str, variant: str = "default"):
        super().__init__(text)
        self.setProperty("variant", variant)
        # Trigger style refresh
        self.style().unpolish(self)
        self.style().polish(self)
```

### Dynamic Style Changes

```python
# Refresh style after changing properties
button.setProperty("variant", "danger")
button.style().unpolish(button)
button.style().polish(button)
```

---

## Troubleshooting

### Common Issues

#### 1. Styles Not Applied

**Cause**: theme load order
```python
# ❌ Wrong
window = MainWindow()
load_theme(app, "theme.json")  # too late

# ✅ Correct
load_theme(app, "theme.json")  # first!
window = MainWindow()
```

#### 2. Property Selector Not Working

**Cause**: missing style refresh
```python
widget.setProperty("variant", "primary")
# Must refresh styles
widget.style().unpolish(widget)
widget.style().polish(widget)
```

#### 3. QGroupBox Descendant Styles Not Applied

**Cause**: calling setStyleSheet on the group box itself
```python
# ❌ Wrong - inside GroupBox
class MyGroupBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QPushButton { ... }")  # does not work!

# ✅ Correct - in MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Define global app styles here
```

#### 4. Colors Not As Expected

**Cause**: inheritance or precedence issues
```css
/* Use more specific selectors */
QGroupBox > QPushButton { ... }  /* direct children */
#specificButton { ... }          /* ID selector */
```

### Debugging Tips

1. **Use Visual Debugger**: inspect actual styles
2. **Set objectName**: makes widgets easy to identify
3. **Apply styles incrementally**: add styles one step at a time
4. **Log theme values**: verify theme loading

```python
theme = get_theme()
print(f"Primary color: {theme.get('colors.brand.primary')}")
```

---

## Related Files

- [theme_manager_template.py](theme_manager_template.py) - Full ThemeManager implementation
- [theme_template.json](theme_template.json) - JSON theme template
- [qss_guide.md](qss_guide.md) - Basic QSS guide

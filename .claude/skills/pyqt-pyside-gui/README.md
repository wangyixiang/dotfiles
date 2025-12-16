# PyQt/PySide GUI Development Tools

## Overview

This is a collection of tools for developing PySide6/PyQt6 GUIs.

## 📁 Directory Structure

```
pyqt-pyside-gui/
├── skill.md                              # PyQt/PySide Best Practices ⭐
├── README.md                             # This file
│
├── tools/                                # Development tools
│   ├── gui_analyzer.py                   # GUI code static analysis tool ⭐
│   └── example_ui.py                     # Example file for analyzer tests
│
├── docs/                                 # Detailed documentation
│   ├── README_GUI_ANALYZER.md            # Detailed GUI Analyzer guide
│   └── GUI_DEBUGGING_TOOLS_SUMMARY.md    # Summary comparison of debugging tools
│
├── examples/                             # Learning examples
│   ├── basic_app.py                      # Basic PySide6 app
│   ├── component_example.py              # Component usage example
│   ├── dialog_examples.py                # Dialog examples
│   ├── table_model.py                    # Table model example
│   ├── threaded_app.py                   # Multithreading example
│   └── json_theme_example.py             # JSON theme system example
│
├── ui_components/                        # Reusable components
│   ├── __init__.py
│   ├── components.py                     # Custom widgets
│   ├── constants.py                      # Constant definitions
│   ├── theme.py                          # Theme management
│   ├── theme_loader.py                   # Theme loader
│   └── themes/                           # Theme JSON files
│       ├── contact-manager.json
│       ├── dark.json
│       └── default.json
│
└── references/                           # Reference documents
    ├── advanced_patterns.md
    ├── ai_friendly_patterns.md
    ├── component_library.md
    ├── json_theme_guide.md
    └── qss_guide.md
```

## 🔧 GUI Code Analyzer - Static Analysis Tool

### Quick Start

```bash
cd .claude/skills/pyqt-pyside-gui/tools

# Analyze example file
python gui_analyzer.py example_ui.py

# Analyze a real project file
python gui_analyzer.py ../../../../neurohub_client/views/main_window.py
```

### Main Features

#### 🌳 Automatic Widget Tree Generation
- Extract widget hierarchy using AST parsing
- Auto-detect parent-child relationships
- Analyze layout relationships

#### 🔍 Widget Property Analysis
Analyzes the following properties for each widget:
- **Geometry**: position and size (x, y, width, height)
- **Visibility**: visible/hidden state
- **Stylesheet**: applied stylesheet
- **Parent/Children**: parent-child relationships
- **Layout**: layout type

#### ⚠️ Automatic Issue Detection

1. **Size Issues**
   - Widgets that are too small (less than 10px)
   - Min/Max size conflicts
   - Abnormal size settings

2. **Visibility Issues**
   - Hidden widgets (`setVisible(False)`)
   - Disabled widgets (`setEnabled(False)`)

3. **Overlapping Detection**
   - Detect overlapping widgets
   - Coordinate-based collision checks

4. **Layout Issues**
   - Widgets without a parent (potential memory leak)
   - Widgets not added to any layout

5. **Naming Issues**
   - Meaningless variable names (widget1, var2, etc.)

#### ✅ skill.md Best Practices Validation

- Uses Theme Manager (`get_theme()`)
- Uses Themed Components
- Detects hardcoded colors (#RRGGBB)
- Uses object names (`setObjectName`)
- Checks for docstrings

#### 📊 HTML Report Generation

Generates a comprehensive report including:
- Statistics dashboard
- Widget tree visualization
- Widget details table
- Issues list (by severity)
- Best practices checklist
- Widget type distribution

### Usage Examples

#### 1. Analyze an Example File
```bash
python gui_analyzer.py example_ui.py
```

**Output:**
```
🔍 Analyzing: example_ui.py
✅ Analysis complete: 16 widgets, 21 issues
📄 Report generated: example_ui_analysis_report.html

============================================================
📊 Analysis Summary:
============================================================
Total Widgets: 16
Total Issues: 21
  - Errors: 0
  - Warnings: 18
  - Info: 3

✅ Report saved to: example_ui_analysis_report.html
```

#### 2. Analyze a Real Project
```bash
python gui_analyzer.py ../../../neurohub_client/views/main_window.py
```

**Output:**
```
🔍 Analyzing: main_window.py
✅ Analysis complete: 5 widgets, 5 issues
📄 Report generated: main_window_analysis_report.html
```

### HTML Report Structure

The generated HTML report includes:

1. **Statistics Section**
   - Total widgets, total issues
   - Error/Warning/Info counts

2. **Widget Tree**
   - Visual hierarchy
   - Widget types and names

3. **Widget Details Table**
   - Detailed properties per widget
   - Geometry, visibility, issues

4. **Issues Detected**
   - List by severity
   - Includes line numbers

5. **Best Practices Checklist**
   - Compliance with `skill.md`
   - ✅/❌ indicators

6. **Widget Type Distribution**
   - Statistics by widget type
   - Graph visualization

## 📚 Related Tools

### 1. Visual Debugger (Dynamic Analysis)
**Location**: `neurohub_client/visual_debugger.py`

**Usage:**
```python
from visual_debugger import launch_with_debugger

app = QApplication(sys.argv)
window = MainWindow()
debugger = launch_with_debugger(window)
sys.exit(app.exec())
```

**Features:**
- Analyze the running app
- Highlight widgets in real time
- Detect dynamically created widgets

### 2. Hot Reload (Development Tool)
**Location**: `neurohub_client/hot_reload.py`

**Usage:**
```bash
python hot_reload.py
```

**Features:**
- Automatically restarts on file changes
- Watches `.py` and `.json` files
- Maximizes development productivity

## 🔄 Recommended Workflow

```
1. Run Hot Reload (during development)
   └─> Automatically restarts on file changes

2. Run Visual Debugger (for debugging)
   └─> Inspect actual widget structure
   └─> Check rendered sizes

3. Run GUI Analyzer (before code review)
   └─> python gui_analyzer.py your_file.py
   └─> Review HTML report
   └─> Validate best practices
   └─> Fix issues

4. Deploy to production ✅
```

## 📖 Detailed Documents

- **[skill.md](skill.md)** - Full PyQt/PySide Best Practices guide
- **[docs/README_GUI_ANALYZER.md](docs/README_GUI_ANALYZER.md)** - Detailed GUI Analyzer docs
- **[docs/GUI_DEBUGGING_TOOLS_SUMMARY.md](docs/GUI_DEBUGGING_TOOLS_SUMMARY.md)** - Comparison of the three tools
- **[tools/example_ui.py](tools/example_ui.py)** - Example file for testing

## 📚 Learning Examples

- **[examples/basic_app.py](examples/basic_app.py)** - Basic PySide6 app structure
- **[examples/component_example.py](examples/component_example.py)** - Custom component usage
- **[examples/dialog_examples.py](examples/dialog_examples.py)** - Dialog patterns
- **[examples/table_model.py](examples/table_model.py)** - QTableView + Model/View
- **[examples/threaded_app.py](examples/threaded_app.py)** - QThread multithreading
- **[examples/json_theme_example.py](examples/json_theme_example.py)** - JSON theme system

## 🎯 Use Cases

### Code Review
```bash
# Analyze all UI files before a PR
python gui_analyzer.py views/main_window.py
python gui_analyzer.py views/settings_dialog.py
python gui_analyzer.py widgets/custom_card.py
```

### Refactoring
- Find hardcoded colors
- Check whether the theme system is used
- Validate naming conventions

### Documentation
- Auto-document widget structure
- Onboarding material for new team members
- Architecture explanation

## ⚙️ Setup

### Python Version
- Requires Python 3.9 or higher

### Dependencies
```bash
# GUI Analyzer uses only the standard library:
# ast, re, json, pathlib, typing, dataclasses, datetime
```

## 🐛 Troubleshooting

### Widgets not detected
- Check that code follows standard patterns
- Use the `self.widget = QWidget()` style
- Dynamically created widgets cannot be detected (use Visual Debugger)

### UnicodeDecodeError
```bash
# Check file encoding
file --mime-encoding your_file.py
```

### AST parsing error
- Check for syntax errors
- Confirm you are using Python 3.9+ syntax

## 📝 License

Copyright (c) 2025 F2X. All rights reserved.

## 👥 Support

If you encounter issues:
- GitHub Issues
- Email: support@f2x.com


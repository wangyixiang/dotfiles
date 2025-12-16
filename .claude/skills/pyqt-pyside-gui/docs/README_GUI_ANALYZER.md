# GUI Code Analyzer - Static Code Analysis Tool

## Overview

This tool statically analyzes PySide6/PyQt6 UI code and generates a comprehensive report.

## Main Features

### 🌳 Automatic Widget Tree Generation
- Automatically extracts widget hierarchy from Python code
- Visualizes parent-child relationships
- Analyzes layout relationships

### 🔍 Widget Property Analysis
For each widget, the following properties are analyzed:
- **Geometry**: position and size (x, y, width, height)
- **Visibility**: visible/hidden state
- **Min/Max Size**: minimum and maximum size
- **Stylesheet**: applied stylesheet
- **Parent/Children**: parent-child relationships
- **Layout Type**: layout type

### ⚠️ Automatic Issue Detection

#### 1. Size Issues
- Widgets that are too small (less than 10px)
- Min/Max size conflicts
- Abnormal size settings

#### 2. Visibility Issues
- Hidden widgets (`setVisible(False)`)
- Disabled widgets (`setEnabled(False)`)

#### 3. Overlapping Detection
- Detects overlapping widgets
- Coordinate-based collision checks
- Warns when multiple widgets are placed in the same area

#### 4. Layout Issues
- Widgets without a parent (potential memory leak)
- Widgets not added to any layout
- Conflicting layouts

#### 5. Naming Issues
- Meaningless variable names (widget1, var2, etc.)
- Naming convention violations

### ✅ skill.md Best Practices Validation

- **Theme Manager usage**: checks for `get_theme()` calls
- **Themed Components usage**: checks use of ThemedCard, ThemedLabel, etc.
- **Hardcoded color removal**: scans for #RRGGBB-style colors in code
- **Object Names usage**: checks for `setObjectName()`
- **Docstrings presence**: basic documentation level

### 📊 HTML Report Generation

Generates a comprehensive report that includes:
- Statistics dashboard
- Widget tree visualization
- Widget details table
- Issues list by severity
- Best practices checklist
- Widget type distribution

## Usage

### Basic Usage
```bash
cd .claude/skills/pyqt-pyside-gui/tools
python gui_analyzer.py <path_to_ui_file.py>
```

### Examples
```bash
# Analyze main window
python gui_analyzer.py ../../../../neurohub_client/views/main_window.py

# Analyze dialog
python gui_analyzer.py ../../../../neurohub_client/views/login_dialog.py

# Analyze widget
python gui_analyzer.py ../../../../neurohub_client/widgets/lot_display_card.py
```

### Sample Output
```
🔍 Analyzing: views/main_window.py
✅ Analysis complete: 5 widgets, 5 issues
📄 Report generated: main_window_analysis_report.html

============================================================
📊 Analysis Summary:
============================================================
Total Widgets: 5
Total Issues: 5
  - Errors: 0
  - Warnings: 5
  - Info: 0

✅ Report saved to: main_window_analysis_report.html
```

## HTML Report Structure

### 1. Statistics Section
- Total widgets
- Total issues
- Error/Warning/Info counts
- Lines of code

### 2. Widget Tree
```
ROOT
├── QMainWindow MainWindow
    ├── QWidget central_widget
    │   ├── QVBoxLayout layout
    │   │   ├── InfoCard lot_card
    │   │   ├── QLabel status_label
    │   │   └── ThemedLabel recent_label
    └── QStatusBar status_bar
        └── StatusIndicator connection_indicator
```

### 3. Widget Details Table
| Name | Type | Parent | Geometry | Visible | Issues |
|------|------|--------|----------|---------|--------|
| lot_card | InfoCard | central_widget | (0, 0, 800, 120) | ✅ | None |
| status_label | QLabel | layout | N/A | ✅ | No parent |

### 4. Issues Detected
Each issue contains:
- **Severity**: error/warning/info
- **Category**: size/visibility/overlap/layout/naming
- **Widget**: the widget with the issue
- **Message**: detailed description
- **Line Number**: line in the code

### 5. Best Practices Checklist
- ✅ Uses Theme Manager (`get_theme()`)
- ✅ Uses Themed Components
- ❌ No Hardcoded Colors (found 3)
- ❌ Uses Object Names (`setObjectName`)
- ✅ Has Docstrings

### 6. Widget Type Distribution
- Counts by widget type
- Graph visualization

## Analysis Algorithms

### AST-Based Parsing
Uses Python's `ast` module to parse the code into an abstract syntax tree:

```python
tree = ast.parse(code)
```

### Widget Detection
1. **Class Definitions**: finds classes that inherit from Qt widgets
2. **Assignments**: detects `self.widget = QWidget()` style patterns
3. **Method Calls**: tracks calls like `setGeometry()`, `setStyleSheet()`, etc.

### Property Extraction
```python
# Example: setGeometry(10, 20, 300, 200)
widget.geometry = (10, 20, 300, 200)

# Example: setMinimumSize(100, 50)
widget.properties['min_size'] = (100, 50)
```

### Overlap Detection Algorithm
```python
def rectangles_overlap(rect1, rect2):
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    return not (x1 + w1 < x2 or x2 + w2 < x1 or
               y1 + h1 < y2 or y2 + h2 < y1)
```

## Supported Widget Types

### Qt Standard Widgets
- QMainWindow, QWidget, QDialog
- QLabel, QPushButton, QLineEdit, QTextEdit
- QComboBox, QCheckBox, QRadioButton
- QSpinBox, QDoubleSpinBox, QSlider
- QListWidget, QTreeWidget, QTableWidget
- QTabWidget, QGroupBox, QFrame
- QMenuBar, QToolBar, QStatusBar

### Qt Layouts
- QVBoxLayout, QHBoxLayout
- QGridLayout, QFormLayout
- QStackedLayout

### Custom Themed Components
- ThemedCard, ThemedLabel, ThemedButton
- InfoCard, StatusIndicator, StatBadge
- LotDisplayCard, StatsCard

## Limitations

### 1. No Dynamic Code Analysis
- Cannot detect widgets created only at runtime
- Limited support for widgets created inside conditionals/loops

### 2. Complex Expressions
- Difficult to track values passed via variables or function calls
- Example: `setGeometry(*calculate_geometry())`

### 3. External Modules
- Widgets imported from other files are recognized only by type

## Comparison with Visual Debugger

| Feature | GUI Analyzer (Static) | Visual Debugger (Dynamic) |
|--------|------------------------|---------------------------|
| Analysis timing | After code is written | While app is running |
| Widget detection | AST parsing | Actual widget tree |
| Dynamic widgets | ❌ Not detected | ✅ All detected |
| Actual size | ❌ Estimated from code | ✅ Real rendered size |
| Requires running app | ❌ No | ✅ Yes |
| Reports | ✅ HTML saved | ⚠️ Real-time only |
| Code quality | ✅ Best practices | ❌ Not supported |

**Recommended Usage:**
1. **During development**: use GUI Analyzer to validate code quality
2. **For testing**: use Visual Debugger to inspect actual rendering
3. **For debugging**: use both tools together

## Use Cases

### 1. Code Review
```bash
# Analyze all UI files before a PR
python gui_analyzer.py views/main_window.py
python gui_analyzer.py views/settings_dialog.py
python gui_analyzer.py widgets/custom_card.py
```

### 2. Refactoring
- Find hardcoded colors
- Check whether the theme system is used
- Validate naming conventions

### 3. Quality Management
- Integrate into CI/CD pipeline
- Generate automatic reports
- Track issues over time

### 4. Documentation
- Auto-document widget structure
- Onboarding material for new team members
- Architecture explanation

## Future Improvements

### Phase 1 (Current)
- ✅ Basic AST parsing
- ✅ Widget tree generation
- ✅ Issue detection
- ✅ HTML report

### Phase 2 (Planned)
- [ ] More advanced dynamic analysis (using eval)
- [ ] Layout optimization suggestions
- [ ] Accessibility checks (WCAG)
- [ ] Multi-language support

### Phase 3 (Future)
- [ ] Auto-fix suggestions
- [ ] VS Code extension
- [ ] GitHub Action integration
- [ ] Performance metrics

## Example Output

### Console Output
```
🔍 Analyzing: views/main_window.py
✅ Analysis complete: 15 widgets, 3 issues
📄 Report generated: main_window_analysis_report.html

============================================================
📊 Analysis Summary:
============================================================
Total Widgets: 15
Total Issues: 3
  - Errors: 0
  - Warnings: 2
  - Info: 1

✅ Report saved to: main_window_analysis_report.html
```

### HTML Report Preview
![Example Report](https://placeholder.com/report-preview.png)

## Troubleshooting

### ImportError: No module named 'ast'
```bash
# Python 3.9+ required
python --version
```

### UnicodeDecodeError
```bash
# Check file encoding
file --mime-encoding your_file.py
```

### Widgets not detected
- Check that code follows standard patterns
- Use the `self.widget = QWidget()` style
- Dynamically created widgets cannot be detected

## Contributing

Please send issues or suggestions to:
- GitHub Issues
- Pull Requests
- Email: support@f2x.com

## License

Copyright (c) 2025 F2X. All rights reserved.

## References

- [skill.md](../skill.md) - PySide6/PyQt6 Best Practices
- [visual_debugger.py](../../../neurohub_client/visual_debugger.py) - Dynamic debugger
- [ARCHITECTURE.md](../../../neurohub_client/ARCHITECTURE.md) - Architecture guide


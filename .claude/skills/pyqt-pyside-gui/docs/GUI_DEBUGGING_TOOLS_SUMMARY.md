# GUI Debugging Tools - Comprehensive Guide

## Overview

Three powerful debugging tools for PySide6/PyQt6 GUI development:

1. **Visual Debugger** (dynamic analysis) - analyze the running app
2. **GUI Code Analyzer** (static analysis) - analyze code files
3. **Hot Reload** (development tool) - automatically restart on file changes

## Tool Comparison

| Feature | Visual Debugger | GUI Analyzer | Hot Reload |
|--------|-----------------|-------------|-----------|
| **Analysis timing** | While app is running | After code is written | During development |
| **Requires running app** | ✅ Yes | ❌ No | ✅ App runs |
| **Widget detection** | All dynamic widgets | AST-based parsing | - |
| **Actual size** | Rendered size | Estimated from code | - |
| **Overlap detection** | Visual | Coordinate-based | - |
| **Reports** | Real-time | HTML saved | Console logs |
| **Best Practices** | ❌ | ✅ | - |
| **Productivity** | Debugging | Code quality | 🚀 Maximum |

## 1. Visual Debugger - Real-Time Analysis

### Purpose
Analyze widgets of the running app in real time.

### When to Use
- When the layout does not look as expected
- When widgets are not visible
- When debugging stylesheet issues
- When you need to check widget size/position

### Usage
```python
from visual_debugger import launch_with_debugger

app = QApplication(sys.argv)
window = MainWindow()
debugger = launch_with_debugger(window)  # Launch debugger
sys.exit(app.exec())
```

### Features
- 📂 **Widget Tree**: visual hierarchy
- 🔧 **Properties Inspector**: geometry, visibility, parent
- 🎨 **Stylesheet Viewer**: view applied styles
- ⚠️ **Issue Detection**: very small widgets, widgets without parents
- ✨ **Visual Highlight**: highlight selected widgets
- 🖼️ **Show All Borders**: draw borders around all widgets

### Advantages
✅ Inspect actual rendering results  
✅ Detect all dynamically created widgets  
✅ Real-time interaction  
✅ Visual highlighting  

### Disadvantages
❌ App must be running  
❌ No persistent reports  
❌ No best-practices validation  

---

## 2. GUI Code Analyzer - Static Analysis

### Purpose
Analyze UI code files and generate a comprehensive report.

### When to Use
- Before code review
- Before submitting a PR
- After refactoring
- When documentation is needed
- In CI/CD pipelines

### Usage
```bash
cd .claude/skills/pyqt-pyside-gui/tools
python gui_analyzer.py path/to/ui_file.py
```

### Features
- 🌳 **Automatic Widget Tree**: AST-based widget extraction
- 🔍 **Property Analysis**: geometry, visibility, styling
- ⚠️ **Issue Detection**:
  - Size issues (too small widgets, min/max conflicts)
  - Visibility issues (hidden widgets)
  - Overlaps (coordinate-based overlap detection)
  - Layout issues (widgets without parents)
  - Naming issues (meaningless names)
- ✅ **Best Practices Validation**:
  - Theme Manager usage (`get_theme()`)
  - Themed Components usage
  - Hardcoded color detection (#RRGGBB)
  - Object Names usage
  - Docstrings presence
- 📊 **HTML Report**: comprehensive, shareable report

### Advantages
✅ No need to run the app  
✅ Saves HTML reports  
✅ Validates best practices  
✅ Easy to integrate with CI/CD  
✅ Great for code quality management  

### Disadvantages
❌ Cannot detect dynamically created widgets  
❌ Cannot know real rendered size  
❌ Limited support for complex expressions  

---

## 3. Hot Reload - Development Productivity

### Purpose
Automatically restart the app when files change.

### When to Use
- During development (always!)
- While tweaking UI layout
- While changing themes
- During frequent code edits

### Usage
```bash
python hot_reload.py
```

### Features
- 🔥 **Auto-Restart**: watches `.py` and `.json` files
- ⏱️ **1-second Debounce**: prevents repeated restarts
- 📝 **Console Output**: keeps logs
- 🛑 **Ctrl+C**: exit

### Advantages
✅ No manual restarts  
✅ Greatly improves development speed  
✅ Immediate feedback on theme changes  
✅ Overall productivity boost  

### Disadvantages
❌ No analysis features  
❌ State is lost on every restart  

---

## Recommended Workflow

### Phase 1: During Development
```bash
# Run Hot Reload
python hot_reload.py

# Edit code → auto restart → check result → repeat
```

### Phase 2: Debugging
```python
# Integrate Visual Debugger
from visual_debugger import launch_with_debugger

app = QApplication(sys.argv)
window = MainWindow()
debugger = launch_with_debugger(window)
sys.exit(app.exec())
```

**Check:**
- Widget tree structure
- Actual rendered size
- Stylesheet application state
- Widget visibility

### Phase 3: Before Code Review
```bash
# Run static analysis
python gui_analyzer.py views/main_window.py
python gui_analyzer.py widgets/custom_card.py

# Review HTML report
# - Validate best practices
# - Check issues and fix them
# - Attach report to PR
```

### Phase 4: CI/CD
```yaml
# GitHub Actions example
- name: Analyze GUI Code
  run: |
    python gui_analyzer.py views/*.py
    # Upload reports as artifacts
```

---

## Real-World Examples

### Example 1: Widget Not Visible

**Step 1: Run Visual Debugger**
```python
debugger = launch_with_debugger(window)
```

**Step 2: Inspect Widget Tree**
- Check if the widget appears in the tree
- Check if `Visible` is False
- Check if geometry is `(0,0,0,0)`

**Step 3: Check Issues Tab**
- "Widget is very small" warning
- "Widget has no parent" warning

**Step 4: Fix the Code**
```python
# Before
self.button = QPushButton("Click")  # No parent

# After
self.button = QPushButton("Click", parent=self)
self.button.setMinimumSize(100, 40)
```

---

### Example 2: Overlapping Layouts

**Step 1: Run GUI Analyzer**
```bash
python gui_analyzer.py views/main_window.py
```

**Step 2: Inspect HTML Report**
- In the Issues section, check "Widgets may overlap" warnings
- Confirm geometry in the Widget Details table

**Step 3: Fix the Code**
```python
# Before - manual geometry
self.button1.setGeometry(10, 10, 100, 50)
self.button2.setGeometry(15, 15, 100, 50)  # Overlap!

# After - use layouts
layout = QHBoxLayout()
layout.addWidget(self.button1)
layout.addWidget(self.button2)
```

---

### Example 3: Theme System Validation

**Step 1: Run GUI Analyzer**
```bash
python gui_analyzer.py views/main_window.py
```

**Step 2: Check Best Practices**
```
✅ Uses Theme Manager (get_theme())
✅ Uses Themed Components
❌ No Hardcoded Colors (found 5)
❌ Uses Object Names (setObjectName)
✅ Has Docstrings
```

**Step 3: Fix Hardcoded Colors**
```python
# Before
label.setStyleSheet("color: #ffffff; background: #1a1a1a;")

# After
theme = get_theme()
label = ThemedLabel("Text", style_type="primary")
```

**Step 4: Add Object Names**
```python
self.submit_button.setObjectName("submit_button")
self.cancel_button.setObjectName("cancel_button")
```

**Step 5: Re-Validate**
```bash
python gui_analyzer.py views/main_window.py
# All checks should now be ✅
```

---

## Integrated Development Setup

### 1. Demo Mode (Visual Debugger)
```python
# demo_mode.py
from visual_debugger import launch_with_debugger

app = QApplication(sys.argv)
window = MainWindow()
debugger = launch_with_debugger(window)
sys.exit(app.exec())
```

### 2. Hot Reload + Visual Debugger
```python
# hot_reload.py runs demo_mode.py
# File changes → auto restart → debugger auto-launch
```

### 3. Pre-Commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash
python gui_analyzer.py views/*.py
if [ $? -ne 0 ]; then
    echo "GUI analysis failed! Fix issues before committing."
    exit 1
fi
```

---

## Summary

### Visual Debugger
**When:** runtime debugging  
**What:** inspect real widgets  
**Result:** real-time interaction  

### GUI Analyzer
**When:** before code review/PR  
**What:** static code analysis  
**Result:** HTML report  

### Hot Reload
**When:** during development (always)  
**What:** auto restart on change  
**Result:** higher productivity  

### Best Combination
```
Hot Reload (development)
    → Visual Debugger (debugging)
        → GUI Analyzer (validation)
            → Production deployment
```

---

## References

- [skill.md](../skill.md) - PyQt/PySide Best Practices
- [README_GUI_ANALYZER.md](README_GUI_ANALYZER.md) - Detailed GUI Analyzer guide
- [visual_debugger.py](../../../neurohub_client/visual_debugger.py) - Visual Debugger source
- [hot_reload.py](../../../neurohub_client/hot_reload.py) - Hot Reload source
- [GUI_ANALYSIS_REPORT.md](../../../neurohub_client/GUI_ANALYSIS_REPORT.md) - Example analysis report

---

**Copyright (c) 2025 F2X. All rights reserved.**


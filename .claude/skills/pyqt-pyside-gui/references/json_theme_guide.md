# JSON Theme System Guide

Complete guide to using JSON-based theming for consistent, customizable UI design.

## Why JSON Themes?

### Problems with Hardcoded Themes
❌ Requires editing Python code whenever the theme changes  
❌ AI has to modify color values directly in code  
❌ Difficult to manage multiple themes  
❌ No real-time theme switching  

### JSON Themes Solution
✅ **Declarative**: define themes in JSON files  
✅ **Flexible**: switch themes at runtime  
✅ **Easy to manage**: control the entire theme from one file  
✅ **AI-friendly**: structured JSON is easy for AI to edit  
✅ **Variable references**: use references like `{colors.primary.main}`  

## Quick Start

### 1. Load Theme

```python
from ui_components import load_theme

app = QApplication(sys.argv)

# Load and apply theme
theme = load_theme(app, "default")  # or "dark"
```

### 2. List Available Themes

```python
from ui_components import list_themes

themes = list_themes()
print(themes)  # ['default', 'dark', ...]
```

### 3. Switch Theme at Runtime

```python
# Switch to dark theme
load_theme(app, "dark")

# Rebuild UI to apply the new theme
```

## JSON Theme Structure

### Basic Structure

```json
{
  "theme": {
    "name": "my-theme",
    "version": "1.0.0",
    "description": "My custom theme"
  },
  
  "colors": {
    "primary": {
      "main": "#3498db",
      "dark": "#2980b9",
      "light": "#5dade2",
      "contrast": "#ffffff"
    }
  },
  
  "typography": {
    "fontFamily": {
      "default": "Arial, sans-serif"
    },
    "fontSize": {
      "normal": 14,
      "large": 18
    }
  },
  
  "spacing": {
    "small": 8,
    "normal": 12,
    "large": 24
  },
  
  "components": {
    "button": {
      "primary": {
        "backgroundColor": "{colors.primary.main}",
        "color": "{colors.primary.contrast}"
      }
    }
  }
}
```

### Variable References

You can reference other values within the theme:

```json
{
  "colors": {
    "primary": {
      "main": "#3498db"
    }
  },
  
  "components": {
    "button": {
      "primary": {
        "backgroundColor": "{colors.primary.main}",
        "hover": {
          "backgroundColor": "{colors.primary.dark}"
        }
      }
    }
  }
}
```

References are resolved automatically.

## Theme Sections in Detail

### 1. colors

Defines all colors:

```json
{
  "colors": {
    "primary": {
      "main": "#3498db",
      "dark": "#2980b9",
      "light": "#5dade2",
      "contrast": "#ffffff"
    },
    "secondary": { /* ... */ },
    "success": { /* ... */ },
    "danger": { /* ... */ },
    "warning": { /* ... */ },
    "info": { /* ... */ },
    "text": {
      "primary": "#2c3e50",
      "secondary": "#7f8c8d",
      "disabled": "#bdc3c7",
      "hint": "#95a5a6"
    },
    "background": {
      "default": "#ecf0f1",
      "paper": "#ffffff",
      "hover": "#f8f9fa"
    },
    "border": {
      "main": "#bdc3c7",
      "dark": "#95a5a6",
      "light": "#ecf0f1"
    }
  }
}
```

### 2. typography

Font configuration:

```json
{
  "typography": {
    "fontFamily": {
      "default": "Segoe UI, Roboto, Arial, sans-serif",
      "monospace": "Consolas, Monaco, monospace"
    },
    "fontSize": {
      "xxlarge": 28,
      "xlarge": 24,
      "large": 18,
      "normal": 14,
      "small": 12,
      "xsmall": 10
    },
    "fontWeight": {
      "light": 300,
      "normal": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    }
  }
}
```

### 3. spacing

Spacing values:

```json
{
  "spacing": {
    "none": 0,
    "xxsmall": 2,
    "xsmall": 4,
    "small": 8,
    "normal": 12,
    "medium": 16,
    "large": 24,
    "xlarge": 32,
    "xxlarge": 48
  }
}
```

### 4. borderRadius

Rounded corners:

```json
{
  "borderRadius": {
    "none": 0,
    "small": 2,
    "normal": 4,
    "medium": 6,
    "large": 8,
    "xlarge": 12,
    "round": 9999
  }
}
```

### 5. components

Component-specific styles:

```json
{
  "components": {
    "button": {
      "primary": {
        "backgroundColor": "{colors.primary.main}",
        "color": "{colors.primary.contrast}",
        "border": "none",
        "borderRadius": "{borderRadius.normal}",
        "padding": "{spacing.small} {spacing.medium}",
        "fontSize": "{typography.fontSize.normal}",
        "fontWeight": "{typography.fontWeight.medium}",
        "hover": {
          "backgroundColor": "{colors.primary.dark}"
        },
        "pressed": {
          "backgroundColor": "{colors.primary.dark}"
        },
        "disabled": {
          "backgroundColor": "{colors.border.main}",
          "color": "{colors.text.disabled}"
        }
      }
    }
  }
}
```

## Creating a Custom Theme

### Step-by-Step

**1. Copy an existing theme**
```bash
cp scripts/ui_components/themes/default.json \
   scripts/ui_components/themes/my-theme.json
```

**2. Edit theme metadata**
```json
{
  "theme": {
    "name": "my-theme",
    "version": "1.0.0",
    "description": "My custom theme"
  }
}
```

**3. Customize colors**
```json
{
  "colors": {
    "primary": {
      "main": "#9C27B0",      // change to purple
      "dark": "#7B1FA2",
      "light": "#BA68C8",
      "contrast": "#ffffff"
    }
  }
}
```

**4. Use the theme**
```python
theme = load_theme(app, "my-theme")
```

### Quick Color Changes

To change only the primary color:

```json
{
  "colors": {
    "primary": {
      "main": "#FF5722",     // Orange
      "dark": "#E64A19",
      "light": "#FF7043",
      "contrast": "#ffffff"
    }
  }
}
```

Other values can remain unchanged.

## Examples

### Example 1: Company Brand Colors

```json
{
  "theme": {
    "name": "company-brand",
    "version": "1.0.0"
  },
  
  "colors": {
    "primary": {
      "main": "#FF6B35",      // Company brand orange
      "dark": "#E55A2B",
      "light": "#FF8554",
      "contrast": "#ffffff"
    },
    "secondary": {
      "main": "#004E89",      // Company brand blue
      "dark": "#003A66",
      "light": "#1A6BA1",
      "contrast": "#ffffff"
    }
  }
}
```

### Example 2: Dark Mode

See `scripts/ui_components/themes/dark.json` for a full example.

Key differences:
- Dark backgrounds
- Light text
- Slightly brighter accent colors

### Example 3: Minimal Theme

```json
{
  "colors": {
    "primary": {
      "main": "#000000",
      "dark": "#000000",
      "light": "#333333",
      "contrast": "#ffffff"
    },
    "text": {
      "primary": "#000000",
      "secondary": "#666666"
    },
    "background": {
      "default": "#ffffff",
      "paper": "#ffffff"
    },
    "border": {
      "main": "#000000"
    }
  },
  
  "borderRadius": {
    "normal": 0,
    "medium": 0
  }
}
```

## Using Themes with AI

### Asking AI to Modify Themes

❌ **Bad example:**
```
"Make the theme a bit brighter"
```

✅ **Good example:**
```
"In scripts/ui_components/themes/default.json,
change colors.primary.main to #64b5f6"
```

✅ **Even better:**
```
"Create blue-theme.json in scripts/ui_components/themes/:
- colors.primary.main: #2196F3
- colors.secondary.main: #FF9800
- all other values same as default.json"
```

### Theme Switching Feature

```
"Add a theme selection feature:
- Use a QComboBox to show available themes
- Switch with load_theme() on selection
- Use list_themes() to list available themes"
```

## Advanced Features

### 1. Programmatic Theme Access

```python
from ui_components import ThemeLoader

# Load theme
theme = ThemeLoader.load_theme("default")

# Get a specific value
primary_color = theme.get("colors.primary.main")
print(f"Primary: {primary_color}")

# Get component style
button_style = theme.get_component_style("button", "primary")
print(button_style)
```

### 2. Runtime Theme Switching

```python
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_theme = "default"
        self.setup_ui()
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        if self.current_theme == "default":
            self.current_theme = "dark"
        else:
            self.current_theme = "default"
        
        # Switch theme
        load_theme(QApplication.instance(), self.current_theme)
        
        # Rebuild UI
        self.setup_ui()
```

### 3. Custom Variables

```json
{
  "custom": {
    "cardShadow": "0 2px 8px rgba(0,0,0,0.1)",
    "animationDuration": 250
  },
  
  "components": {
    "card": {
      "default": {
        "shadow": "{custom.cardShadow}"
      }
    }
  }
}
```

## Troubleshooting

### Theme Not Loaded
```python
# Check available themes
print(list_themes())

# Check file path:
# scripts/ui_components/themes/your-theme.json
```

### Variable Reference Not Resolved
```json
// ❌ Incorrect
"backgroundColor": "{color.primary}"

// ✅ Correct
"backgroundColor": "{colors.primary.main}"
```

### Styles Not Applied
```python
# Load theme before creating components
theme = load_theme(app, "default")  # first
button = Button("Text")             # then create components
```

## Best Practices

1. **Use semantic color names**
   - `primary`, `secondary` (good)
   - `blue`, `red` (bad)

2. **Use variable references**
   - Minimize duplication
   - Maintain consistency

3. **Use hierarchical structure**
   - Define base colors
   - Components reference color and typography tokens

4. **Version themes**
   - Use the `version` field
   - Document changes

5. **Test themes**
   - Check all components
   - Test both dark and light themes

## Summary

With a JSON theme system you can:
- ✅ Separate themes from code
- ✅ Allow AI to edit themes easily
- ✅ Support runtime theme switching
- ✅ Improve maintainability
- ✅ Scale and extend your design system

**Next steps:**
1. Run `json_theme_example.py`
2. Edit `themes/default.json`
3. Create a custom theme
4. Apply it to your app


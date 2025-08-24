# Appendix A: Tkinter Widget Reference

## 📚 Quick Reference Guide

This appendix provides a comprehensive reference for all Tkinter widgets, their properties, and common usage patterns.

## 🎯 Basic Widgets

### Label
**Purpose**: Display text or images
```python
tk.Label(parent, text="Hello World", font=("Arial", 12))
```

**Common Properties**:
- `text`: Text to display
- `font`: Font family, size, and style
- `fg`: Text color (foreground)
- `bg`: Background color
- `image`: Image to display
- `width`, `height`: Widget dimensions

### Button
**Purpose**: Clickable button
```python
tk.Button(parent, text="Click Me", command=callback_function)
```

**Common Properties**:
- `text`: Button text
- `command`: Function to call when clicked
- `state`: "normal", "disabled", "active"
- `width`, `height`: Button dimensions
- `fg`, `bg`: Colors

### Entry
**Purpose**: Single-line text input
```python
tk.Entry(parent, width=30, show="*")  # show="*" for password
```

**Common Properties**:
- `width`: Width in characters
- `show`: Character to display (for passwords)
- `state`: "normal", "readonly", "disabled"
- `fg`, `bg`: Colors

**Common Methods**:
- `get()`: Get current text
- `delete(start, end)`: Delete text
- `insert(index, text)`: Insert text
- `focus()`: Set focus to entry

### Text
**Purpose**: Multi-line text input/display
```python
tk.Text(parent, width=40, height=10)
```

**Common Properties**:
- `width`, `height`: Dimensions in characters
- `wrap`: "word", "char", "none"
- `state`: "normal", "disabled"

**Common Methods**:
- `get(start, end)`: Get text
- `insert(index, text)`: Insert text
- `delete(start, end)`: Delete text

## 📋 Container Widgets

### Frame
**Purpose**: Container for other widgets
```python
tk.Frame(parent, relief="raised", borderwidth=2)
```

**Common Properties**:
- `relief`: "flat", "raised", "sunken", "groove", "ridge"
- `borderwidth`: Border width
- `bg`: Background color

### LabelFrame
**Purpose**: Frame with a label
```python
tk.LabelFrame(parent, text="Group Title", padx=10, pady=10)
```

### PanedWindow
**Purpose**: Resizable panes
```python
tk.PanedWindow(parent, orient="horizontal")
```

## 📊 Data Display Widgets

### Listbox
**Purpose**: List of selectable items
```python
tk.Listbox(parent, height=5, selectmode="single")
```

**Common Properties**:
- `height`: Number of visible items
- `selectmode`: "single", "multiple", "extended"

**Common Methods**:
- `insert(index, item)`: Add item
- `delete(index)`: Remove item
- `get(index)`: Get item
- `curselection()`: Get selected indices

### Treeview
**Purpose**: Hierarchical data display
```python
ttk.Treeview(parent, columns=("Name", "Age"), show="headings")
```

**Common Properties**:
- `columns`: Column names
- `show`: "tree", "headings", "tree headings"

**Common Methods**:
- `insert(parent, index, values=())`: Add item
- `delete(item)`: Remove item
- `selection()`: Get selected items

### Scale
**Purpose**: Slider widget
```python
tk.Scale(parent, from_=0, to=100, orient="horizontal")
```

**Common Properties**:
- `from_`, `to`: Range values
- `orient`: "horizontal", "vertical"
- `resolution`: Step size

## 🎨 Advanced Widgets

### Canvas
**Purpose**: Drawing area
```python
tk.Canvas(parent, width=300, height=200)
```

**Common Methods**:
- `create_line(x1, y1, x2, y2)`: Draw line
- `create_rectangle(x1, y1, x2, y2)`: Draw rectangle
- `create_oval(x1, y1, x2, y2)`: Draw oval
- `create_text(x, y, text="")`: Add text

### Spinbox
**Purpose**: Number input with increment/decrement
```python
tk.Spinbox(parent, from_=0, to=100, increment=1)
```

### Checkbutton
**Purpose**: Checkbox
```python
tk.Checkbutton(parent, text="Option", variable=var)
```

### Radiobutton
**Purpose**: Radio button
```python
tk.Radiobutton(parent, text="Option", variable=var, value=1)
```

## 📋 Menu Widgets

### Menu
**Purpose**: Menu bar
```python
menubar = tk.Menu(root)
root.config(menu=menubar)
```

### MenuItem
**Purpose**: Menu item
```python
menubar.add_command(label="File", command=file_function)
menubar.add_separator()
menubar.add_cascade(label="Edit", menu=edit_menu)
```

## 📊 Dialog Widgets

### Messagebox
**Purpose**: Popup dialogs
```python
from tkinter import messagebox

messagebox.showinfo("Title", "Message")
messagebox.showwarning("Title", "Warning")
messagebox.showerror("Title", "Error")
messagebox.askyesno("Title", "Question")
```

### Filedialog
**Purpose**: File selection dialogs
```python
from tkinter import filedialog

filename = filedialog.askopenfilename()
filename = filedialog.asksaveasfilename()
```

### Colorchooser
**Purpose**: Color selection dialog
```python
from tkinter import colorchooser

color = colorchooser.askcolor()
```

## 🎯 Layout Management

### Pack Geometry Manager
```python
widget.pack(side="top", fill="both", expand=True, padx=10, pady=10)
```

**Options**:
- `side`: "top", "bottom", "left", "right"
- `fill`: "none", "x", "y", "both"
- `expand`: True/False
- `padx`, `pady`: Padding
- `anchor`: "n", "s", "e", "w", "center"

### Grid Geometry Manager
```python
widget.grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")
```

**Options**:
- `row`, `column`: Position
- `rowspan`, `columnspan`: Span multiple cells
- `sticky`: "n", "s", "e", "w" combinations
- `padx`, `pady`: Padding
- `ipadx`, `ipady`: Internal padding

### Place Geometry Manager
```python
widget.place(x=100, y=50, relx=0.5, rely=0.5, anchor="center")
```

**Options**:
- `x`, `y`: Absolute coordinates
- `relx`, `rely`: Relative coordinates (0.0 to 1.0)
- `anchor`: "n", "s", "e", "w", "center"
- `width`, `height`: Dimensions

## 🎨 Styling and Theming

### Common Colors
```python
# Named colors
"red", "blue", "green", "yellow", "white", "black"

# Hex colors
"#FF0000", "#00FF00", "#0000FF"

# RGB colors
"rgb(255, 0, 0)"
```

### Fonts
```python
# Font tuple: (family, size, style)
("Arial", 12, "bold")
("Times New Roman", 14, "italic")
("Courier", 10, "normal")
```

### Relief Styles
```python
"flat", "raised", "sunken", "groove", "ridge"
```

## 🔧 Common Patterns

### Variable Classes
```python
# String variable
var = tk.StringVar()
var.set("Initial value")
entry = tk.Entry(parent, textvariable=var)

# Integer variable
var = tk.IntVar()
var.set(0)
scale = tk.Scale(parent, variable=var)

# Boolean variable
var = tk.BooleanVar()
var.set(True)
check = tk.Checkbutton(parent, variable=var)
```

### Event Binding
```python
# Bind to specific event
widget.bind("<Button-1>", callback_function)
widget.bind("<Key>", callback_function)
widget.bind("<Return>", callback_function)

# Common event types
"<Button-1>": Left mouse click
"<Button-3>": Right mouse click
"<Key>": Any key press
"<Return>": Enter key
"<FocusIn>": Widget gains focus
"<FocusOut>": Widget loses focus
```

### Widget Configuration
```python
# Configure multiple properties
widget.configure(
    text="New text",
    bg="red",
    font=("Arial", 12)
)

# Or use config() method
widget.config(text="New text")
```

## 🚀 Best Practices

1. **Use meaningful variable names** for widgets
2. **Group related widgets** in frames
3. **Choose appropriate layout managers** for your needs
4. **Handle events properly** with try-except blocks
5. **Use consistent styling** throughout your application
6. **Test your layouts** at different window sizes
7. **Document your widget hierarchy** for complex layouts

---

**This reference covers the most commonly used Tkinter widgets. For complete documentation, visit the official Python documentation.**

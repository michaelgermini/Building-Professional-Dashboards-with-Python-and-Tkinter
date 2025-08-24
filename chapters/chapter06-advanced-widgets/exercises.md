# Chapter 6: Advanced Widgets for Dashboards - Exercises

## Exercise 1: Enhanced Treeview with Advanced Features

### Objective
Create an advanced Treeview application with hierarchical data, custom styling, and advanced filtering capabilities.

### Requirements
- Create a Treeview that displays hierarchical data (e.g., organizational structure)
- Implement advanced filtering with multiple criteria
- Add custom styling with alternating row colors
- Include export functionality (CSV, JSON)
- Add right-click context menu for common actions

### Starter Code
```python
import tkinter as tk
from tkinter import ttk, messagebox
import json
import csv

class AdvancedTreeviewExercise:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Treeview Exercise")
        self.root.geometry("1000x600")
        
        # Sample hierarchical data
        self.data = {
            "CEO": {
                "name": "John Smith",
                "department": "Executive",
                "salary": 150000,
                "employees": {
                    "CTO": {
                        "name": "Jane Doe",
                        "department": "Technology",
                        "salary": 120000,
                        "employees": {
                            "Dev Lead": {"name": "Bob Johnson", "department": "Engineering", "salary": 90000},
                            "QA Lead": {"name": "Alice Brown", "department": "Quality", "salary": 85000}
                        }
                    },
                    "CFO": {
                        "name": "Mike Wilson",
                        "department": "Finance",
                        "salary": 110000,
                        "employees": {
                            "Accountant": {"name": "Sarah Davis", "department": "Accounting", "salary": 70000}
                        }
                    }
                }
            }
        }
        
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        # TODO: Implement the advanced Treeview interface
        pass
    
    def load_data(self):
        # TODO: Load hierarchical data into Treeview
        pass
    
    def filter_data(self):
        # TODO: Implement advanced filtering
        pass
    
    def export_data(self, format_type):
        # TODO: Export data to CSV or JSON
        pass

def main():
    root = tk.Tk()
    app = AdvancedTreeviewExercise(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A professional Treeview application with:
- Hierarchical data display with expandable/collapsible nodes
- Advanced filtering panel with multiple criteria
- Custom styling with alternating row colors
- Export functionality with format selection
- Context menu for common actions (edit, delete, add child)

---

## Exercise 2: Multi-Tab Dashboard with Dynamic Content

### Objective
Create a comprehensive multi-tab dashboard that dynamically loads content and manages tab state.

### Requirements
- Create a Notebook with at least 4 different tab types
- Implement dynamic tab loading (load content only when tab is selected)
- Add tab state management (save/restore tab content)
- Include tab-specific toolbars and context menus
- Implement tab reordering and custom tab styling

### Starter Code
```python
import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class TabContent:
    """Base class for tab content"""
    
    def __init__(self, parent, title):
        self.parent = parent
        self.title = title
        self.is_loaded = False
        self.widget = None
    
    def load_content(self):
        """Load tab content - to be implemented by subclasses"""
        pass
    
    def save_state(self):
        """Save tab state - to be implemented by subclasses"""
        pass
    
    def restore_state(self, state):
        """Restore tab state - to be implemented by subclasses"""
        pass

class MultiTabDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Tab Dashboard Exercise")
        self.root.geometry("1200x800")
        
        self.tabs = {}
        self.tab_states = {}
        
        self.create_widgets()
        self.create_tabs()
    
    def create_widgets(self):
        # TODO: Create the main dashboard interface
        pass
    
    def create_tabs(self):
        # TODO: Create different tab types
        pass
    
    def on_tab_changed(self, event):
        # TODO: Handle tab selection and dynamic loading
        pass
    
    def save_all_states(self):
        # TODO: Save all tab states
        pass
    
    def load_all_states(self):
        # TODO: Load all tab states
        pass

def main():
    root = tk.Tk()
    app = MultiTabDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A professional multi-tab dashboard with:
- Dynamic content loading for better performance
- Tab state persistence across sessions
- Custom tab styling and reordering
- Tab-specific toolbars and context menus
- Professional layout and user experience

---

## Exercise 3: Advanced Form Builder with Validation

### Objective
Create a dynamic form builder that allows users to create custom forms with various field types and validation rules.

### Requirements
- Create a form builder interface with drag-and-drop field creation
- Support multiple field types (text, number, date, dropdown, checkbox, etc.)
- Implement custom validation rules and error handling
- Add form preview and testing functionality
- Include form template saving and loading

### Starter Code
```python
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class FormField:
    """Base class for form fields"""
    
    def __init__(self, field_type, label, required=False, validators=None):
        self.field_type = field_type
        self.label = label
        self.required = required
        self.validators = validators or []
        self.value = None
    
    def create_widget(self, parent):
        """Create the field widget - to be implemented by subclasses"""
        pass
    
    def get_value(self):
        """Get field value"""
        return self.value
    
    def validate(self):
        """Validate field value"""
        pass

class FormBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Form Builder Exercise")
        self.root.geometry("1400x800")
        
        self.fields = []
        self.current_form = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # TODO: Create the form builder interface
        pass
    
    def add_field(self, field_type):
        # TODO: Add new field to the form
        pass
    
    def preview_form(self):
        # TODO: Show form preview
        pass
    
    def save_form(self):
        # TODO: Save form template
        pass
    
    def load_form(self):
        # TODO: Load form template
        pass

def main():
    root = tk.Tk()
    app = FormBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A comprehensive form builder with:
- Drag-and-drop field creation interface
- Multiple field types with custom validation
- Form preview and testing functionality
- Template saving and loading
- Professional form rendering

---

## Exercise 4: Professional Menu and Toolbar System

### Objective
Create a professional menu and toolbar system with keyboard shortcuts, context menus, and customizable toolbars.

### Requirements
- Create a comprehensive menu system with File, Edit, View, Tools, Help menus
- Implement keyboard shortcuts and accelerators
- Add context menus for different widgets
- Create customizable toolbars with icons
- Include menu state management (enable/disable based on context)

### Starter Code
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class MenuToolbarSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu and Toolbar System Exercise")
        self.root.geometry("1000x600")
        
        self.current_file = None
        self.is_modified = False
        
        self.create_menu()
        self.create_toolbar()
        self.create_context_menus()
        self.create_widgets()
    
    def create_menu(self):
        # TODO: Create comprehensive menu system
        pass
    
    def create_toolbar(self):
        # TODO: Create customizable toolbar
        pass
    
    def create_context_menus(self):
        # TODO: Create context menus for different widgets
        pass
    
    def create_widgets(self):
        # TODO: Create main application widgets
        pass
    
    def file_new(self):
        # TODO: Implement new file functionality
        pass
    
    def file_open(self):
        # TODO: Implement open file functionality
        pass
    
    def file_save(self):
        # TODO: Implement save functionality
        pass
    
    def edit_cut(self):
        # TODO: Implement cut functionality
        pass
    
    def edit_copy(self):
        # TODO: Implement copy functionality
        pass
    
    def edit_paste(self):
        # TODO: Implement paste functionality
        pass

def main():
    root = tk.Tk()
    app = MenuToolbarSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A professional menu and toolbar system with:
- Comprehensive menu structure with keyboard shortcuts
- Context menus for different widgets
- Customizable toolbar with icons
- Menu state management
- Professional user experience

---

## Exercise 5: Status and Progress Management System

### Objective
Create a comprehensive status and progress management system for long-running operations.

### Requirements
- Create a status bar with multiple sections (main status, progress, time, memory usage)
- Implement progress tracking for multiple concurrent operations
- Add notification system with different types (info, warning, error, success)
- Include operation queue management
- Create progress history and logging

### Starter Code
```python
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import psutil
from datetime import datetime
import queue

class Operation:
    """Represents a long-running operation"""
    
    def __init__(self, name, total_steps=100):
        self.name = name
        self.total_steps = total_steps
        self.current_step = 0
        self.status = "pending"
        self.start_time = None
        self.end_time = None
    
    def start(self):
        self.status = "running"
        self.start_time = datetime.now()
    
    def update_progress(self, step):
        self.current_step = step
    
    def complete(self):
        self.status = "completed"
        self.end_time = datetime.now()
    
    def fail(self, error):
        self.status = "failed"
        self.error = error
        self.end_time = datetime.now()

class StatusProgressSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Status and Progress Management Exercise")
        self.root.geometry("1000x700")
        
        self.operations = {}
        self.operation_queue = queue.Queue()
        self.notifications = []
        
        self.create_widgets()
        self.start_background_threads()
    
    def create_widgets(self):
        # TODO: Create status and progress management interface
        pass
    
    def add_operation(self, operation):
        # TODO: Add operation to queue
        pass
    
    def update_operation_progress(self, operation_id, progress):
        # TODO: Update operation progress
        pass
    
    def show_notification(self, message, notification_type="info"):
        # TODO: Show notification
        pass
    
    def start_background_threads(self):
        # TODO: Start background processing threads
        pass

def main():
    root = tk.Tk()
    app = StatusProgressSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A comprehensive status and progress management system with:
- Multi-section status bar with real-time updates
- Progress tracking for multiple concurrent operations
- Notification system with different types and auto-dismiss
- Operation queue management
- Progress history and logging

---

## Bonus Challenge: Complete Dashboard Application

### Objective
Create a complete professional dashboard application that combines all the advanced widgets and features learned in this chapter.

### Requirements
- Create a comprehensive dashboard with multiple sections
- Implement all advanced widgets (Treeview, Notebook, Forms, Menus, Status)
- Add data visualization and real-time updates
- Include user preferences and settings management
- Create a professional theme and styling system
- Add export and reporting capabilities

### Advanced Features
- Plugin system for extending functionality
- Multi-language support
- Advanced theming and customization
- Data persistence and backup
- Performance monitoring and optimization

### Implementation Guidelines
1. **Architecture**: Use MVC pattern with clear separation of concerns
2. **Modularity**: Create reusable components and widgets
3. **Performance**: Implement efficient data handling and UI updates
4. **User Experience**: Focus on intuitive navigation and responsive design
5. **Extensibility**: Design for easy addition of new features

### Expected Result
A production-ready dashboard application that demonstrates:
- Professional UI/UX design
- Comprehensive functionality
- Robust error handling
- Performance optimization
- Extensibility and maintainability

---

## Summary

These exercises progressively build your skills in:

1. **Advanced Treeview**: Hierarchical data, filtering, styling, and export
2. **Multi-Tab Interfaces**: Dynamic loading, state management, and customization
3. **Form Building**: Dynamic forms, validation, and template management
4. **Menu Systems**: Comprehensive menus, toolbars, and context menus
5. **Status Management**: Progress tracking, notifications, and operation management
6. **Complete Integration**: Professional dashboard with all advanced features

Each exercise includes starter code and detailed requirements to help you understand the concepts and build upon them for your own projects. The bonus challenge provides an opportunity to create a complete, production-ready application that demonstrates mastery of all advanced widget concepts.

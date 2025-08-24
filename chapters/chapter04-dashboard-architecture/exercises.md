# Chapter 4 Exercises

## 🎯 Exercise Overview

These exercises will help you practice the concepts learned in Chapter 4. You'll work with modular design, MVC patterns, and custom widget creation to build professional dashboard architectures.

## 📝 Exercise 1: Refactor Counter Application

### Objective
Refactor your Chapter 3 counter application into a modular design with separate components.

### Instructions
1. Create separate classes for different components:
   - `CounterModel`: Handles the counter data and logic
   - `CounterView`: Displays the counter interface
   - `CounterController`: Handles user interactions
2. Use the Observer pattern to update the view when data changes
3. Implement proper separation of concerns

### Starter Code
```python
import tkinter as tk

# TODO: Create CounterModel class
class CounterModel:
    def __init__(self):
        self.value = 0
        self.observers = []
    
    def add_observer(self, observer):
        # TODO: Add observer to the list
        pass
    
    def notify_observers(self):
        # TODO: Notify all observers of changes
        pass
    
    def increment(self):
        # TODO: Increment value and notify observers
        pass
    
    def decrement(self):
        # TODO: Decrement value and notify observers
        pass
    
    def reset(self):
        # TODO: Reset value and notify observers
        pass

# TODO: Create CounterView class
class CounterView(tk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.model.add_observer(self)
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        # TODO: Create the interface widgets
        pass
    
    def update(self):
        # TODO: Update the view with current model data
        pass

# TODO: Create CounterController class
class CounterController:
    def __init__(self, model):
        self.model = model
    
    def increment(self):
        # TODO: Call model increment
        pass
    
    def decrement(self):
        # TODO: Call model decrement
        pass
    
    def reset(self):
        # TODO: Call model reset
        pass

# TODO: Create main application class
class ModularCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Counter")
        self.root.geometry("300x200")
        
        # TODO: Create model, controller, and view
        pass

def main():
    root = tk.Tk()
    app = ModularCounterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A counter application with the same functionality as Chapter 3, but organized using modular design principles.

### Solution
```python
import tkinter as tk

class CounterModel:
    def __init__(self):
        self.value = 0
        self.observers = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update()
    
    def increment(self):
        self.value += 1
        self.notify_observers()
    
    def decrement(self):
        self.value -= 1
        self.notify_observers()
    
    def reset(self):
        self.value = 0
        self.notify_observers()
    
    def get_value(self):
        return self.value

class CounterView(tk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.model.add_observer(self)
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Modular Counter", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Counter display
        self.counter_label = tk.Label(self, text="0", font=("Arial", 24))
        self.counter_label.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Buttons
        self.increment_btn = tk.Button(button_frame, text="Increment", width=10)
        self.increment_btn.pack(side="left", padx=5)
        
        self.decrement_btn = tk.Button(button_frame, text="Decrement", width=10)
        self.decrement_btn.pack(side="left", padx=5)
        
        self.reset_btn = tk.Button(button_frame, text="Reset", width=10)
        self.reset_btn.pack(side="left", padx=5)
    
    def update(self):
        self.counter_label.config(text=str(self.model.get_value()))
    
    def set_callbacks(self, controller):
        self.increment_btn.config(command=controller.increment)
        self.decrement_btn.config(command=controller.decrement)
        self.reset_btn.config(command=controller.reset)

class CounterController:
    def __init__(self, model):
        self.model = model
    
    def increment(self):
        self.model.increment()
    
    def decrement(self):
        self.model.decrement()
    
    def reset(self):
        self.model.reset()

class ModularCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Counter")
        self.root.geometry("300x200")
        
        # Create model, controller, and view
        self.model = CounterModel()
        self.controller = CounterController(self.model)
        self.view = CounterView(self.root, self.model)
        self.view.pack(fill="both", expand=True)
        
        # Set up callbacks
        self.view.set_callbacks(self.controller)

def main():
    root = tk.Tk()
    app = ModularCounterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 2: Create a Custom Widget

### Objective
Create a custom widget class that can be reused across different applications.

### Instructions
1. Create a `NotificationWidget` class that displays notifications
2. Include features like:
   - Different notification types (info, warning, error, success)
   - Auto-dismiss functionality
   - Customizable appearance
   - Animation effects
3. Make it reusable and configurable

### Starter Code
```python
import tkinter as tk
from tkinter import ttk
import time

class NotificationWidget(tk.Frame):
    """Custom notification widget"""
    
    def __init__(self, parent, message="", notification_type="info", 
                 auto_dismiss=True, dismiss_time=3000, **kwargs):
        super().__init__(parent, **kwargs)
        self.message = message
        self.notification_type = notification_type
        self.auto_dismiss = auto_dismiss
        self.dismiss_time = dismiss_time
        
        # TODO: Define colors for different notification types
        self.colors = {
            'info': ('#3498DB', '#2980B9'),
            'warning': ('#F39C12', '#E67E22'),
            'error': ('#E74C3C', '#C0392B'),
            'success': ('#27AE60', '#229954')
        }
        
        self.create_widgets()
        
        if self.auto_dismiss:
            self.schedule_dismiss()
    
    def create_widgets(self):
        # TODO: Create the notification interface
        pass
    
    def schedule_dismiss(self):
        # TODO: Schedule auto-dismiss
        pass
    
    def dismiss(self):
        # TODO: Remove the notification
        pass
    
    def show(self):
        # TODO: Display the notification with animation
        pass

# Test the widget
class NotificationDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Notification Widget Demo")
        self.root.geometry("400x300")
        
        # TODO: Create test interface
        pass

def main():
    root = tk.Tk()
    demo = NotificationDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A reusable notification widget that can display different types of notifications with auto-dismiss functionality.

### Solution
```python
import tkinter as tk
from tkinter import ttk
import time

class NotificationWidget(tk.Frame):
    """Custom notification widget"""
    
    def __init__(self, parent, message="", notification_type="info", 
                 auto_dismiss=True, dismiss_time=3000, **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.message = message
        self.notification_type = notification_type
        self.auto_dismiss = auto_dismiss
        self.dismiss_time = dismiss_time
        
        # Define colors for different notification types
        self.colors = {
            'info': ('#3498DB', '#2980B9'),
            'warning': ('#F39C12', '#E67E22'),
            'error': ('#E74C3C', '#C0392B'),
            'success': ('#27AE60', '#229954')
        }
        
        self.create_widgets()
        
        if self.auto_dismiss:
            self.schedule_dismiss()
    
    def create_widgets(self):
        # Get colors for this notification type
        bg_color, border_color = self.colors.get(self.notification_type, self.colors['info'])
        
        # Configure frame
        self.configure(bg=bg_color)
        
        # Message label
        self.message_label = tk.Label(
            self,
            text=self.message,
            font=("Arial", 10),
            fg="white",
            bg=bg_color,
            wraplength=300
        )
        self.message_label.pack(side="left", padx=10, pady=5)
        
        # Close button
        close_btn = tk.Button(
            self,
            text="×",
            font=("Arial", 12, "bold"),
            fg="white",
            bg=bg_color,
            bd=0,
            command=self.dismiss,
            width=3
        )
        close_btn.pack(side="right", padx=5, pady=5)
        
        # Type indicator
        type_label = tk.Label(
            self,
            text=self.notification_type.upper(),
            font=("Arial", 8, "bold"),
            fg="white",
            bg=border_color
        )
        type_label.pack(side="left", padx=(5, 0), pady=5)
    
    def schedule_dismiss(self):
        """Schedule auto-dismiss"""
        self.after(self.dismiss_time, self.dismiss)
    
    def dismiss(self):
        """Remove the notification"""
        self.pack_forget()
        self.destroy()
    
    def show(self):
        """Display the notification"""
        self.pack(fill="x", padx=10, pady=5)

class NotificationDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Notification Widget Demo")
        self.root.geometry("400x300")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Notification Widget Demo",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Test buttons
        tk.Button(
            button_frame,
            text="Show Info",
            command=lambda: self.show_notification("info", "This is an info message")
        ).pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Show Warning",
            command=lambda: self.show_notification("warning", "This is a warning message")
        ).pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Show Error",
            command=lambda: self.show_notification("error", "This is an error message")
        ).pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Show Success",
            command=lambda: self.show_notification("success", "This is a success message")
        ).pack(pady=5)
    
    def show_notification(self, notification_type, message):
        """Show a notification"""
        notification = NotificationWidget(
            self.root,
            message=message,
            notification_type=notification_type,
            auto_dismiss=True,
            dismiss_time=3000
        )
        notification.show()

def main():
    root = tk.Tk()
    demo = NotificationDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 3: Build a Modular Dashboard

### Objective
Create a complete modular dashboard application using the concepts learned in this chapter.

### Instructions
1. Create a dashboard with multiple components:
   - Header component with title and time
   - Metrics panel with multiple metric cards
   - Control panel with buttons
   - Data table component
2. Use MVC pattern for data management
3. Implement custom widgets for metrics display
4. Add real-time updates

### Requirements
- At least 3 different metric types
- Real-time data updates
- Modular component design
- Proper error handling
- Professional appearance

### Starter Structure
```python
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

# TODO: Create Model classes
class DashboardModel:
    def __init__(self):
        # TODO: Initialize data and observers
        pass

# TODO: Create View classes
class HeaderView(tk.Frame):
    def __init__(self, parent, model):
        # TODO: Create header component
        pass

class MetricsView(tk.Frame):
    def __init__(self, parent, model):
        # TODO: Create metrics display
        pass

class ControlView(tk.Frame):
    def __init__(self, parent, controller):
        # TODO: Create control panel
        pass

# TODO: Create Controller class
class DashboardController:
    def __init__(self, model):
        # TODO: Initialize controller
        pass

# TODO: Create main application
class ModularDashboardApp:
    def __init__(self, root):
        # TODO: Create complete dashboard
        pass

def main():
    root = tk.Tk()
    app = ModularDashboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A professional-looking dashboard with multiple components, real-time updates, and modular architecture.

### Solution
```python
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

class DashboardModel:
    def __init__(self):
        self.metrics = {
            'temperature': 25.0,
            'humidity': 60.0,
            'pressure': 1013.0,
            'cpu_usage': 45.0
        }
        self.observers = []
        self.data_history = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update()
    
    def update_metrics(self, new_metrics):
        self.metrics.update(new_metrics)
        self.add_to_history()
        self.notify_observers()
    
    def add_to_history(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.data_history.append({
            'timestamp': timestamp,
            'temperature': self.metrics['temperature'],
            'humidity': self.metrics['humidity']
        })
        # Keep only last 10 entries
        if len(self.data_history) > 10:
            self.data_history.pop(0)
    
    def get_metrics(self):
        return self.metrics.copy()
    
    def get_history(self):
        return self.data_history.copy()

class MetricCard(tk.Frame):
    def __init__(self, parent, title, value, unit="", **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.title = title
        self.value = value
        self.unit = unit
        self.create_widgets()
    
    def create_widgets(self):
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 12, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=(10, 5))
        
        self.value_label = tk.Label(
            self,
            text=f"{self.value}{self.unit}",
            font=("Arial", 16, "bold"),
            fg="#2980B9"
        )
        self.value_label.pack(pady=(0, 10))
    
    def update_value(self, new_value):
        self.value = new_value
        self.value_label.config(text=f"{self.value}{self.unit}")

class HeaderView(tk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.create_widgets()
        self.update_time()
    
    def create_widgets(self):
        title_label = tk.Label(
            self,
            text="Modular Dashboard",
            font=("Arial", 18, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(side="left", padx=10, pady=5)
        
        self.time_label = tk.Label(
            self,
            text="",
            font=("Arial", 10),
            fg="#7F8C8D"
        )
        self.time_label.pack(side="right", padx=10, pady=5)
    
    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Time: {current_time}")
        self.after(1000, self.update_time)

class MetricsView(tk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.model.add_observer(self)
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        # Create metric cards
        self.temp_card = MetricCard(self, "Temperature", 25, "°C")
        self.temp_card.pack(side="left", padx=5, pady=5)
        
        self.humidity_card = MetricCard(self, "Humidity", 60, "%")
        self.humidity_card.pack(side="left", padx=5, pady=5)
        
        self.pressure_card = MetricCard(self, "Pressure", 1013, " hPa")
        self.pressure_card.pack(side="left", padx=5, pady=5)
        
        self.cpu_card = MetricCard(self, "CPU Usage", 45, "%")
        self.cpu_card.pack(side="left", padx=5, pady=5)
    
    def update(self):
        metrics = self.model.get_metrics()
        self.temp_card.update_value(metrics['temperature'])
        self.humidity_card.update_value(metrics['humidity'])
        self.pressure_card.update_value(metrics['pressure'])
        self.cpu_card.update_value(metrics['cpu_usage'])

class ControlView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, relief="groove", borderwidth=2)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        title_label = tk.Label(
            self,
            text="Controls",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Refresh Data",
            command=self.controller.refresh_data,
            width=15
        ).pack(pady=5)
        
        tk.Button(
            button_frame,
            text="Reset Metrics",
            command=self.controller.reset_metrics,
            width=15
        ).pack(pady=5)

class DataTableView(tk.Frame):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.model.add_observer(self)
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        title_label = tk.Label(
            self,
            text="Data History",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        columns = ("Time", "Temperature", "Humidity")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
    
    def update(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new data
        history = self.model.get_history()
        for entry in history:
            self.tree.insert("", "end", values=(
                entry['timestamp'],
                f"{entry['temperature']:.1f}°C",
                f"{entry['humidity']:.1f}%"
            ))

class DashboardController:
    def __init__(self, model):
        self.model = model
    
    def refresh_data(self):
        new_metrics = {
            'temperature': random.uniform(20, 30),
            'humidity': random.uniform(50, 70),
            'pressure': random.uniform(1000, 1020),
            'cpu_usage': random.uniform(30, 80)
        }
        self.model.update_metrics(new_metrics)
    
    def reset_metrics(self):
        default_metrics = {
            'temperature': 25.0,
            'humidity': 60.0,
            'pressure': 1013.0,
            'cpu_usage': 45.0
        }
        self.model.update_metrics(default_metrics)

class ModularDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Dashboard")
        self.root.geometry("800x600")
        
        # Create model and controller
        self.model = DashboardModel()
        self.controller = DashboardController(self.model)
        
        # Create the interface
        self.create_widgets()
        
        # Start data simulation
        self.simulate_data()
    
    def create_widgets(self):
        self.root.configure(bg="#ECF0F1")
        
        # Header
        self.header = HeaderView(self.root, self.model)
        self.header.pack(fill="x", padx=10, pady=5)
        
        # Main content
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel
        left_panel = tk.Frame(main_frame, bg="#ECF0F1")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Metrics view
        self.metrics_view = MetricsView(left_panel, self.model)
        self.metrics_view.pack(fill="x", pady=(0, 10))
        
        # Data table
        self.data_table = DataTableView(left_panel, self.model)
        self.data_table.pack(fill="both", expand=True)
        
        # Right panel
        right_panel = tk.Frame(main_frame, bg="#ECF0F1")
        right_panel.pack(side="right", fill="y", padx=(5, 0))
        
        # Control view
        self.control_view = ControlView(right_panel, self.controller)
        self.control_view.pack(fill="x")
    
    def simulate_data(self):
        self.controller.refresh_data()
        self.root.after(5000, self.simulate_data)

def main():
    root = tk.Tk()
    app = ModularDashboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 🎯 Bonus Challenge

### Create a Plugin System

Design and implement a plugin system for your dashboard that allows adding new components dynamically.

### Requirements
1. Create a base plugin interface
2. Implement at least 3 different plugins (e.g., weather widget, stock ticker, system monitor)
3. Allow plugins to be loaded/unloaded at runtime
4. Implement proper communication between plugins and the main dashboard

### Advanced Features
- Plugin configuration management
- Plugin dependency handling
- Plugin marketplace concept
- Hot-reloading of plugins

---

## 🔍 Key Concepts Reinforced

- **Modular Design**: Breaking applications into reusable components
- **MVC Pattern**: Separating data, logic, and presentation
- **Observer Pattern**: Implementing event-driven updates
- **Custom Widgets**: Creating reusable UI components
- **Code Organization**: Structuring applications for maintainability
- **Error Handling**: Implementing robust error management

## 🚀 Next Steps

Once you've completed these exercises:

1. Experiment with different architectural patterns
2. Create more complex custom widgets
3. Implement additional dashboard components
4. Move on to Chapter 5 to learn about data visualization

---

**Great job completing Chapter 4! You're now ready to build professional, scalable dashboard applications! 🎉**

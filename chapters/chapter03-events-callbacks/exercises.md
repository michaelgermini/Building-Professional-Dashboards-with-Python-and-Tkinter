# Chapter 3 Exercises

## 🎯 Exercise Overview

These exercises will help you practice working with events and callbacks in Tkinter. Each exercise builds upon the previous one, gradually increasing in complexity.

## 📝 Exercise 1: Interactive Counter

### Objective
Learn how to handle button clicks and update widget values dynamically.

### Instructions
1. Create a counter application with increment and decrement buttons
2. Display the current count in a label
3. Add a reset button to set the count back to zero
4. Add keyboard shortcuts (Up arrow for increment, Down arrow for decrement)

### Starter Code
```python
import tkinter as tk

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Counter")
        self.root.geometry("300x200")
        
        self.count = 0
        
        # TODO: Create the UI elements and bind events
        
    def increment(self):
        # TODO: Increment the counter and update display
        pass
        
    def decrement(self):
        # TODO: Decrement the counter and update display
        pass
        
    def reset(self):
        # TODO: Reset the counter to zero
        pass
        
    def update_display(self):
        # TODO: Update the count label
        pass

def main():
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A counter application that responds to button clicks and keyboard events.

### Solution
```python
import tkinter as tk

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Counter")
        self.root.geometry("300x200")
        
        self.count = 0
        
        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True)
        
        # Count display
        self.count_label = tk.Label(main_frame, text="0", font=("Arial", 24, "bold"))
        self.count_label.pack(pady=20)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        # Buttons
        tk.Button(button_frame, text="-", command=self.decrement, width=5).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reset", command=self.reset, width=8).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="+", command=self.increment, width=5).pack(side=tk.LEFT, padx=5)
        
        # Bind keyboard events
        self.root.bind("<Up>", lambda e: self.increment())
        self.root.bind("<Down>", lambda e: self.decrement())
        self.root.bind("<r>", lambda e: self.reset())
        self.root.bind("<R>", lambda e: self.reset())
        
        # Focus on window to capture keyboard events
        self.root.focus_set()
        
    def increment(self):
        self.count += 1
        self.update_display()
        
    def decrement(self):
        self.count -= 1
        self.update_display()
        
    def reset(self):
        self.count = 0
        self.update_display()
        
    def update_display(self):
        self.count_label.config(text=str(self.count))

def main():
    root = tk.Tk()
    app = CounterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 2: Form Validation

### Objective
Learn how to validate user input in real-time and provide feedback.

### Instructions
1. Create a registration form with validation
2. Validate email format in real-time
3. Check password strength
4. Show validation messages to the user
5. Only enable submit button when all fields are valid

### Starter Code
```python
import tkinter as tk
import re

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form with Validation")
        self.root.geometry("400x500")
        
        # TODO: Create form fields and validation logic
        
    def validate_email(self, email):
        # TODO: Implement email validation
        pass
        
    def validate_password(self, password):
        # TODO: Implement password strength validation
        pass
        
    def update_submit_button(self):
        # TODO: Enable/disable submit button based on validation
        pass

def main():
    root = tk.Tk()
    app = RegistrationForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A form that validates input in real-time and provides user feedback.

### Solution
```python
import tkinter as tk
import re
from tkinter import messagebox

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form with Validation")
        self.root.geometry("400x500")
        
        # Validation states
        self.email_valid = False
        self.password_valid = False
        
        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="Registration Form", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Username
        tk.Label(main_frame, text="Username:").pack(anchor=tk.W)
        self.username_entry = tk.Entry(main_frame, width=30)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Email
        tk.Label(main_frame, text="Email:").pack(anchor=tk.W)
        self.email_entry = tk.Entry(main_frame, width=30)
        self.email_entry.pack(fill=tk.X, pady=5)
        self.email_entry.bind('<KeyRelease>', self.validate_email)
        
        # Email validation message
        self.email_message = tk.Label(main_frame, text="", fg="red")
        self.email_message.pack(anchor=tk.W)
        
        # Password
        tk.Label(main_frame, text="Password:").pack(anchor=tk.W)
        self.password_entry = tk.Entry(main_frame, width=30, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)
        self.password_entry.bind('<KeyRelease>', self.validate_password)
        
        # Password validation message
        self.password_message = tk.Label(main_frame, text="", fg="red")
        self.password_message.pack(anchor=tk.W)
        
        # Submit button
        self.submit_button = tk.Button(main_frame, text="Submit", command=self.submit, state=tk.DISABLED)
        self.submit_button.pack(pady=20)
        
    def validate_email(self, event=None):
        email = self.email_entry.get()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if re.match(pattern, email):
            self.email_message.config(text="✓ Valid email", fg="green")
            self.email_valid = True
        else:
            self.email_message.config(text="✗ Invalid email format", fg="red")
            self.email_valid = False
            
        self.update_submit_button()
        
    def validate_password(self, event=None):
        password = self.password_entry.get()
        
        # Check password strength
        has_length = len(password) >= 8
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if has_length and has_upper and has_lower and has_digit:
            self.password_message.config(text="✓ Strong password", fg="green")
            self.password_valid = True
        else:
            requirements = []
            if not has_length:
                requirements.append("8+ characters")
            if not has_upper:
                requirements.append("uppercase")
            if not has_lower:
                requirements.append("lowercase")
            if not has_digit:
                requirements.append("number")
            
            self.password_message.config(text=f"✗ Need: {', '.join(requirements)}", fg="red")
            self.password_valid = False
            
        self.update_submit_button()
        
    def update_submit_button(self):
        if self.email_valid and self.password_valid and self.username_entry.get():
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED)
            
    def submit(self):
        messagebox.showinfo("Success", "Registration successful!")

def main():
    root = tk.Tk()
    app = RegistrationForm(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 3: Interactive Dashboard

### Objective
Create an interactive dashboard that responds to various user events.

### Instructions
1. Create a dashboard with multiple interactive elements
2. Include a color picker that changes the theme
3. Add a slider that controls font size
4. Create buttons that show different information panels
5. Add mouse hover effects and tooltips

### Starter Code
```python
import tkinter as tk
from tkinter import ttk

class InteractiveDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Dashboard")
        self.root.geometry("600x400")
        
        # TODO: Create interactive dashboard elements
        
    def change_theme(self, color):
        # TODO: Change the application theme
        pass
        
    def update_font_size(self, size):
        # TODO: Update font sizes throughout the application
        pass
        
    def show_panel(self, panel_name):
        # TODO: Show different information panels
        pass

def main():
    root = tk.Tk()
    app = InteractiveDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
An interactive dashboard that responds to user interactions with visual feedback.

### Solution
```python
import tkinter as tk
from tkinter import ttk

class InteractiveDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Dashboard")
        self.root.geometry("600x400")
        
        # Current theme and font size
        self.current_theme = "#f0f0f0"
        self.font_size = 10
        
        # Create main container
        self.main_frame = tk.Frame(root, bg=self.current_theme)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header = tk.Frame(self.main_frame, bg=self.current_theme)
        self.header.pack(fill=tk.X, padx=10, pady=10)
        
        self.title_label = tk.Label(
            self.header, 
            text="Interactive Dashboard", 
            font=("Arial", 16, "bold"),
            bg=self.current_theme
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Controls frame
        controls_frame = tk.Frame(self.header, bg=self.current_theme)
        controls_frame.pack(side=tk.RIGHT)
        
        # Theme selector
        tk.Label(controls_frame, text="Theme:", bg=self.current_theme).pack(side=tk.LEFT)
        theme_var = tk.StringVar(value="Light")
        theme_combo = ttk.Combobox(
            controls_frame, 
            textvariable=theme_var, 
            values=["Light", "Dark", "Blue", "Green"],
            width=10
        )
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self.change_theme(theme_var.get()))
        
        # Font size slider
        tk.Label(controls_frame, text="Font Size:", bg=self.current_theme).pack(side=tk.LEFT, padx=(10, 0))
        self.font_slider = tk.Scale(
            controls_frame, 
            from_=8, 
            to=20, 
            orient=tk.HORIZONTAL, 
            command=self.update_font_size,
            length=100
        )
        self.font_slider.set(10)
        self.font_slider.pack(side=tk.LEFT, padx=5)
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame, bg=self.current_theme)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.content_frame, bg=self.current_theme)
        nav_frame.pack(fill=tk.X, pady=10)
        
        buttons = [
            ("Overview", self.show_overview),
            ("Statistics", self.show_statistics),
            ("Settings", self.show_settings),
            ("Help", self.show_help)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                nav_frame, 
                text=text, 
                command=command,
                relief=tk.RAISED,
                bg="#e0e0e0"
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Add hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg="#d0d0d0"))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg="#e0e0e0"))
        
        # Default panel
        self.show_overview()
        
    def change_theme(self, theme_name):
        themes = {
            "Light": "#f0f0f0",
            "Dark": "#2c2c2c",
            "Blue": "#e6f3ff",
            "Green": "#e6ffe6"
        }
        
        self.current_theme = themes.get(theme_name, "#f0f0f0")
        
        # Update all widgets
        widgets = [self.main_frame, self.header, self.content_frame, self.title_label]
        for widget in widgets:
            widget.config(bg=self.current_theme)
            
    def update_font_size(self, size):
        self.font_size = int(size)
        self.title_label.config(font=("Arial", self.font_size + 6, "bold"))
        
    def show_overview(self):
        self.clear_content()
        
        # Overview content
        content = tk.Frame(self.content_frame, bg=self.current_theme)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content, 
            text="Dashboard Overview", 
            font=("Arial", self.font_size + 2, "bold"),
            bg=self.current_theme
        ).pack(pady=10)
        
        # Sample metrics
        metrics = [
            ("Total Users", "1,234"),
            ("Active Sessions", "567"),
            ("System Status", "Online"),
            ("Last Update", "2 minutes ago")
        ]
        
        for label, value in metrics:
            metric_frame = tk.Frame(content, bg=self.current_theme)
            metric_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(
                metric_frame, 
                text=f"{label}:", 
                font=("Arial", self.font_size),
                bg=self.current_theme
            ).pack(side=tk.LEFT)
            
            tk.Label(
                metric_frame, 
                text=value, 
                font=("Arial", self.font_size, "bold"),
                fg="blue",
                bg=self.current_theme
            ).pack(side=tk.RIGHT)
            
    def show_statistics(self):
        self.clear_content()
        
        content = tk.Frame(self.content_frame, bg=self.current_theme)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content, 
            text="Statistics Panel", 
            font=("Arial", self.font_size + 2, "bold"),
            bg=self.current_theme
        ).pack(pady=10)
        
        # Sample chart placeholder
        chart_frame = tk.Frame(content, bg="white", relief=tk.RAISED, borderwidth=2)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(
            chart_frame, 
            text="Chart Area\n(Click to interact)", 
            font=("Arial", self.font_size),
            bg="white"
        ).pack(expand=True)
        
        # Make it interactive
        chart_frame.bind('<Button-1>', lambda e: tk.messagebox.showinfo("Chart", "Chart clicked!"))
        
    def show_settings(self):
        self.clear_content()
        
        content = tk.Frame(self.content_frame, bg=self.current_theme)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content, 
            text="Settings Panel", 
            font=("Arial", self.font_size + 2, "bold"),
            bg=self.current_theme
        ).pack(pady=10)
        
        # Settings options
        settings = [
            ("Auto-refresh", tk.BooleanVar()),
            ("Notifications", tk.BooleanVar()),
            ("Dark mode", tk.BooleanVar())
        ]
        
        for setting, var in settings:
            tk.Checkbutton(
                content, 
                text=setting, 
                variable=var,
                bg=self.current_theme,
                font=("Arial", self.font_size)
            ).pack(anchor=tk.W, pady=5)
            
    def show_help(self):
        self.clear_content()
        
        content = tk.Frame(self.content_frame, bg=self.current_theme)
        content.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content, 
            text="Help & Documentation", 
            font=("Arial", self.font_size + 2, "bold"),
            bg=self.current_theme
        ).pack(pady=10)
        
        help_text = """
        Welcome to the Interactive Dashboard!
        
        Features:
        • Change themes using the dropdown
        • Adjust font size with the slider
        • Navigate between different panels
        • Interactive elements respond to clicks
        
        Keyboard shortcuts:
        • Ctrl+T: Toggle theme
        • Ctrl+F: Focus search
        • F1: Show this help
        """
        
        text_widget = tk.Text(
            content, 
            wrap=tk.WORD, 
            bg=self.current_theme,
            font=("Arial", self.font_size),
            relief=tk.FLAT
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
    def clear_content(self):
        # Remove existing content
        for widget in self.content_frame.winfo_children():
            if widget != self.content_frame.winfo_children()[0]:  # Keep nav frame
                widget.destroy()

def main():
    root = tk.Tk()
    app = InteractiveDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 🎯 Bonus Challenge

### Create a Real-time Data Monitor

Combine all the concepts from the exercises to create a real-time data monitoring dashboard:

1. **Real-time Updates**: Use `root.after()` to update data periodically
2. **Interactive Charts**: Create simple bar charts that respond to clicks
3. **Data Input**: Allow users to add new data points
4. **Alerts**: Show notifications when certain thresholds are exceeded
5. **Export Functionality**: Save data to a file

### Example Features
- **Live Data Display**: Shows current system metrics
- **Interactive Controls**: Buttons to start/stop monitoring
- **Alert System**: Visual indicators for critical values
- **Data History**: Graph showing trends over time

---

## 🔍 Key Concepts Reinforced

- **Event Handling**: Button clicks, keyboard events, mouse events
- **Real-time Updates**: Using `root.after()` for periodic updates
- **Input Validation**: Checking user input and providing feedback
- **Interactive UI**: Creating responsive user interfaces
- **State Management**: Tracking application state and updating UI accordingly

## 🚀 Next Steps

Once you've completed these exercises:

1. Experiment with different event types
2. Try creating more complex validation rules
3. Practice with real-time data updates
4. Move on to Chapter 4 to learn about dashboard architecture

---

**Great job completing Chapter 3! You're now ready to build truly interactive dashboards! 🎉**

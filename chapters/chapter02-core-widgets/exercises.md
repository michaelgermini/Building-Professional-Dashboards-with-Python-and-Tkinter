# Chapter 2 Exercises

## 🎯 Exercise Overview

These exercises will help you practice working with core Tkinter widgets and layout management. Each exercise builds upon the previous one, gradually increasing in complexity.

## 📝 Exercise 1: Create a Simple Form

### Objective
Learn how to create a basic form using Entry widgets and buttons.

### Instructions
1. Create a window with a title "User Registration Form"
2. Add labels and entry fields for:
   - First Name
   - Last Name
   - Email
3. Add a "Submit" button
4. Add a "Clear" button that clears all fields

### Starter Code
```python
import tkinter as tk
from tkinter import messagebox

def submit_form():
    # TODO: Get values from entry fields and show a message
    pass

def clear_form():
    # TODO: Clear all entry fields
    pass

def main():
    root = tk.Tk()
    root.title("User Registration Form")
    root.geometry("400x300")
    
    # TODO: Add your form widgets here
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A form with entry fields and buttons that can submit or clear the data.

### Solution
```python
import tkinter as tk
from tkinter import messagebox

def submit_form():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    email = email_entry.get()
    
    if first_name and last_name and email:
        messagebox.showinfo("Success", f"Welcome {first_name} {last_name}!")
    else:
        messagebox.showerror("Error", "Please fill all fields")

def clear_form():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    root.title("User Registration Form")
    root.geometry("400x300")
    
    # First Name
    tk.Label(root, text="First Name:").pack(pady=5)
    first_name_entry = tk.Entry(root, width=30)
    first_name_entry.pack(pady=5)
    
    # Last Name
    tk.Label(root, text="Last Name:").pack(pady=5)
    last_name_entry = tk.Entry(root, width=30)
    last_name_entry.pack(pady=5)
    
    # Email
    tk.Label(root, text="Email:").pack(pady=5)
    email_entry = tk.Entry(root, width=30)
    email_entry.pack(pady=5)
    
    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Submit", command=submit_form).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Clear", command=clear_form).pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 2: Layout Management with Grid

### Objective
Learn how to use the grid layout manager for more complex arrangements.

### Instructions
1. Create a calculator-like interface using grid layout
2. Add labels and entry fields arranged in a grid
3. Use different column and row spans for better layout

### Starter Code
```python
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Grid Layout Demo")
    root.geometry("500x400")
    
    # TODO: Create a grid layout with labels and entry fields
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A form with widgets arranged in a grid pattern.

### Solution
```python
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Grid Layout Demo")
    root.geometry("500x400")
    
    # Configure grid weights
    root.grid_columnconfigure(1, weight=1)
    
    # Personal Information Section
    tk.Label(root, text="Personal Information", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    
    # Name fields
    tk.Label(root, text="First Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    
    tk.Label(root, text="Last Name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
    
    # Contact Information Section
    tk.Label(root, text="Contact Information", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, pady=10)
    
    tk.Label(root, text="Email:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=4, column=1, sticky="ew", padx=5, pady=5)
    
    tk.Label(root, text="Phone:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=5, column=1, sticky="ew", padx=5, pady=5)
    
    # Address Section
    tk.Label(root, text="Address", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=10)
    
    tk.Label(root, text="Street:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=7, column=1, sticky="ew", padx=5, pady=5)
    
    tk.Label(root, text="City:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=8, column=1, sticky="ew", padx=5, pady=5)
    
    tk.Label(root, text="State:").grid(row=9, column=0, sticky="e", padx=5, pady=5)
    tk.Entry(root, width=30).grid(row=9, column=1, sticky="ew", padx=5, pady=5)
    
    # Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=10, column=0, columnspan=2, pady=20)
    
    tk.Button(button_frame, text="Save", width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear", width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", width=10).pack(side=tk.LEFT, padx=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 3: Advanced Widgets

### Objective
Learn how to use more advanced widgets like Text, Listbox, and Checkbutton.

### Instructions
1. Create a dashboard with multiple widget types
2. Include a Text widget for notes
3. Add a Listbox for displaying items
4. Include Checkbuttons for options
5. Use different layout managers (pack, grid, place)

### Starter Code
```python
import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Advanced Widgets Dashboard")
    root.geometry("600x500")
    
    # TODO: Create a dashboard with various widgets
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A dashboard with multiple widget types arranged in a professional layout.

### Solution
```python
import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Advanced Widgets Dashboard")
    root.geometry("600x500")
    
    # Main container
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Left panel
    left_panel = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=2)
    left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    
    # Right panel
    right_panel = tk.Frame(main_frame, relief=tk.RAISED, borderwidth=2)
    right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
    
    # Left Panel Content
    tk.Label(left_panel, text="Task List", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Listbox for tasks
    task_listbox = tk.Listbox(left_panel, height=10)
    task_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Add some sample tasks
    tasks = ["Complete Chapter 2", "Review exercises", "Start Chapter 3", "Practice layouts"]
    for task in tasks:
        task_listbox.insert(tk.END, task)
    
    # Task controls
    task_frame = tk.Frame(left_panel)
    task_frame.pack(fill=tk.X, padx=10, pady=5)
    
    tk.Button(task_frame, text="Add Task", width=10).pack(side=tk.LEFT, padx=2)
    tk.Button(task_frame, text="Remove", width=10).pack(side=tk.LEFT, padx=2)
    
    # Right Panel Content
    tk.Label(right_panel, text="Notes & Settings", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Notes section
    tk.Label(right_panel, text="Notes:").pack(anchor=tk.W, padx=10)
    notes_text = tk.Text(right_panel, height=8, width=30)
    notes_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    
    # Settings section
    settings_frame = tk.Frame(right_panel)
    settings_frame.pack(fill=tk.X, padx=10, pady=10)
    
    tk.Label(settings_frame, text="Settings:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
    
    # Checkbuttons
    auto_save_var = tk.BooleanVar()
    tk.Checkbutton(settings_frame, text="Auto-save", variable=auto_save_var).pack(anchor=tk.W)
    
    notifications_var = tk.BooleanVar()
    tk.Checkbutton(settings_frame, text="Enable notifications", variable=notifications_var).pack(anchor=tk.W)
    
    dark_mode_var = tk.BooleanVar()
    tk.Checkbutton(settings_frame, text="Dark mode", variable=dark_mode_var).pack(anchor=tk.W)
    
    # Status bar
    status_bar = tk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 🎯 Bonus Challenge

### Create a Professional Dashboard Layout

Combine all the concepts from the exercises to create a professional dashboard:

1. Use multiple layout managers (pack, grid, place)
2. Include various widget types (Entry, Text, Listbox, Checkbutton, Button)
3. Create a responsive layout that adapts to window resizing
4. Add proper spacing and visual hierarchy
5. Include a menu bar and status bar

### Example Features
- **Header**: Title and navigation buttons
- **Sidebar**: Quick access menu with icons
- **Main Content**: Data display area with tabs
- **Footer**: Status information and controls

---

## 🔍 Key Concepts Reinforced

- **Widget Types**: Entry, Label, Button, Text, Listbox, Checkbutton
- **Layout Management**: Pack, Grid, and Place managers
- **Event Handling**: Button clicks and form submission
- **Data Entry**: Getting and setting widget values
- **Visual Design**: Creating professional-looking interfaces

## 🚀 Next Steps

Once you've completed these exercises:

1. Experiment with different widget combinations
2. Try creating more complex layouts
3. Practice with different layout managers
4. Move on to Chapter 3 to learn about events and callbacks

---

**Great job completing Chapter 2! You're now ready to create more interactive dashboards! 🎉**

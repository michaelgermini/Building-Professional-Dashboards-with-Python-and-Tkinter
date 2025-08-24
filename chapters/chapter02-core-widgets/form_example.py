"""
Chapter 2: Core Widgets and Layout Management
Example: Form with Labels, Entry Fields, and Buttons

This example demonstrates how to create a form with multiple widgets
using the grid layout manager.
"""

import tkinter as tk

def submit_form():
    """Handle form submission"""
    name = name_entry.get()
    email = email_entry.get()
    age = age_entry.get()
    
    print(f"Form submitted:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Age: {age}")
    
    # Clear the form
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)

def main():
    # Create the main window
    root = tk.Tk()
    root.title("User Registration Form")
    root.geometry("400x300")
    
    # Configure grid weights for responsive design
    root.grid_columnconfigure(1, weight=1)
    
    # Title label
    title_label = tk.Label(root, text="User Registration Form", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=20)
    
    # Name field
    name_label = tk.Label(root, text="Name:")
    name_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
    
    name_entry = tk.Entry(root, width=30)
    name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
    
    # Email field
    email_label = tk.Label(root, text="Email:")
    email_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
    
    email_entry = tk.Entry(root, width=30)
    email_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
    
    # Age field
    age_label = tk.Label(root, text="Age:")
    age_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
    
    age_entry = tk.Entry(root, width=30)
    age_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
    
    # Submit button
    submit_button = tk.Button(root, text="Submit", command=submit_form, width=15)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)
    
    # Status label
    status_label = tk.Label(root, text="Enter your information and click Submit", fg="gray")
    status_label.grid(row=5, column=0, columnspan=2, pady=10)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()

"""
Chapter 3: Events and Callbacks
Example: Counter Application

This example demonstrates how to create an interactive counter that
increments when a button is clicked.
"""

import tkinter as tk

class CounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Counter Application")
        self.root.geometry("300x200")
        
        # Initialize counter variable
        self.counter = 0
        
        # Create the interface
        self.create_widgets()
    
    def create_widgets(self):
        """Create and arrange the widgets"""
        # Title
        title_label = tk.Label(self.root, text="Interactive Counter", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Counter display
        self.counter_label = tk.Label(self.root, text="0", font=("Arial", 24))
        self.counter_label.pack(pady=20)
        
        # Button frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Increment button
        increment_button = tk.Button(
            button_frame, 
            text="Increment", 
            command=self.increment_counter,
            width=10
        )
        increment_button.pack(side="left", padx=5)
        
        # Decrement button
        decrement_button = tk.Button(
            button_frame, 
            text="Decrement", 
            command=self.decrement_counter,
            width=10
        )
        decrement_button.pack(side="left", padx=5)
        
        # Reset button
        reset_button = tk.Button(
            button_frame, 
            text="Reset", 
            command=self.reset_counter,
            width=10
        )
        reset_button.pack(side="left", padx=5)
    
    def increment_counter(self):
        """Increment the counter and update display"""
        self.counter += 1
        self.update_display()
    
    def decrement_counter(self):
        """Decrement the counter and update display"""
        self.counter -= 1
        self.update_display()
    
    def reset_counter(self):
        """Reset the counter to zero"""
        self.counter = 0
        self.update_display()
    
    def update_display(self):
        """Update the counter display"""
        self.counter_label.config(text=str(self.counter))

def main():
    # Create the main window
    root = tk.Tk()
    
    # Create the counter application
    app = CounterApp(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()

"""
Chapter 1: Getting Started with Tkinter
Example: Hello Dashboard

This is your first Tkinter application - a simple window with a welcome message.
Run this file to see your first dashboard window appear!
"""

import tkinter as tk

def main():
    # Create the main window
    root = tk.Tk()
    
    # Set the window title
    root.title("Hello Dashboard")
    
    # Set the window size (width x height)
    root.geometry("400x200")
    
    # Create a label widget with welcome text
    label = tk.Label(root, text="Welcome to Your First Dashboard!")
    
    # Pack the label into the window with some padding
    label.pack(pady=20)
    
    # Start the event loop - this keeps the window open
    root.mainloop()

if __name__ == "__main__":
    main()

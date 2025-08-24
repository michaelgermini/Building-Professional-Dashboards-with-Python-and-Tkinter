"""
Chapter 2: Core Widgets and Layout Management
Example: Layout Managers Demo

This example demonstrates the three different layout managers in Tkinter:
- pack(): Simple stacking layout
- grid(): Table-like layout with rows and columns  
- place(): Precise positioning with coordinates
"""

import tkinter as tk

def create_pack_demo(parent):
    """Demonstrate pack() layout manager"""
    frame = tk.LabelFrame(parent, text="Pack Layout", padx=10, pady=10)
    
    # Pack widgets vertically (default)
    tk.Label(frame, text="Top Label").pack()
    tk.Button(frame, text="Middle Button").pack(pady=5)
    tk.Label(frame, text="Bottom Label").pack()
    
    return frame

def create_grid_demo(parent):
    """Demonstrate grid() layout manager"""
    frame = tk.LabelFrame(parent, text="Grid Layout", padx=10, pady=10)
    
    # Configure grid weights for responsive design
    frame.grid_columnconfigure(1, weight=1)
    
    # Create a 2x2 grid
    tk.Label(frame, text="Row 1, Col 1").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(frame, text="Row 1, Col 2").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    
    tk.Label(frame, text="Row 2, Col 1").grid(row=1, column=0, padx=5, pady=5)
    tk.Button(frame, text="Row 2, Col 2").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    
    return frame

def create_place_demo(parent):
    """Demonstrate place() layout manager"""
    frame = tk.LabelFrame(parent, text="Place Layout", padx=10, pady=10, width=200, height=150)
    frame.pack_propagate(False)  # Prevent frame from shrinking
    
    # Place widgets at specific coordinates
    tk.Label(frame, text="Top Left").place(x=10, y=10)
    tk.Button(frame, text="Center").place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(frame, text="Bottom Right").place(relx=1.0, rely=1.0, anchor="se")
    
    return frame

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Layout Managers Demo")
    root.geometry("600x400")
    
    # Title
    title_label = tk.Label(root, text="Tkinter Layout Managers", font=("Arial", 16, "bold"))
    title_label.pack(pady=20)
    
    # Create a frame to hold all demos
    main_frame = tk.Frame(root)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Create the three layout demos
    pack_frame = create_pack_demo(main_frame)
    pack_frame.pack(side="left", fill="both", expand=True, padx=5)
    
    grid_frame = create_grid_demo(main_frame)
    grid_frame.pack(side="left", fill="both", expand=True, padx=5)
    
    place_frame = create_place_demo(main_frame)
    place_frame.pack(side="left", fill="both", expand=True, padx=5)
    
    # Instructions
    instructions = tk.Label(
        root, 
        text="Resize the window to see how different layouts behave",
        fg="gray"
    )
    instructions.pack(pady=10)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()

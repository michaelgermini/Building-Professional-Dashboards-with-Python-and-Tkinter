# Chapter 1 Exercises

## 🎯 Exercise Overview

These exercises will help you practice the concepts learned in Chapter 1. Each exercise builds upon the previous one, gradually increasing in complexity.

## 📝 Exercise 1: Modify Window Properties

### Objective
Learn how to customize the main window by changing its title and dimensions.

### Instructions
1. Open the `hello_dashboard.py` file
2. Modify the window title to something personal (e.g., "My First Dashboard")
3. Change the window size to 500x300 pixels
4. Run the program to see your changes

### Starter Code
```python
import tkinter as tk

def main():
    root = tk.Tk()
    
    # TODO: Change the title here
    root.title("Hello Dashboard")
    
    # TODO: Change the size here
    root.geometry("400x200")
    
    label = tk.Label(root, text="Welcome to Your First Dashboard!")
    label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A window with your custom title and larger dimensions.

### Solution
```python
import tkinter as tk

def main():
    root = tk.Tk()
    
    root.title("My First Dashboard")  # Changed title
    
    root.geometry("500x300")  # Changed size
    
    label = tk.Label(root, text="Welcome to Your First Dashboard!")
    label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 2: Add Multiple Labels

### Objective
Learn how to add multiple widgets to your window and understand widget hierarchy.

### Instructions
1. Add a second label below the first one
2. Make the second label display your name
3. Add some spacing between the labels

### Starter Code
```python
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("My First Dashboard")
    root.geometry("500x300")
    
    # First label
    label = tk.Label(root, text="Welcome to Your First Dashboard!")
    label.pack(pady=20)
    
    # TODO: Add a second label here with your name
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
Two labels displayed vertically with spacing between them.

### Solution
```python
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("My First Dashboard")
    root.geometry("500x300")
    
    # First label
    label = tk.Label(root, text="Welcome to Your First Dashboard!")
    label.pack(pady=20)
    
    # Second label
    name_label = tk.Label(root, text="Created by: Your Name")
    name_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 📝 Exercise 3: Customize Colors

### Objective
Learn how to change the appearance of your window and widgets using colors.

### Instructions
1. Change the background color of the main window
2. Change the text color of the labels
3. Experiment with different color combinations

### Color Options
You can use:
- Color names: "red", "blue", "green", "yellow", "white", "black"
- Hex codes: "#FF0000", "#0000FF", "#00FF00"
- RGB values: "rgb(255, 0, 0)"

### Starter Code
```python
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("My First Dashboard")
    root.geometry("500x300")
    
    # TODO: Add background color to the window
    # root.configure(bg="color_name")
    
    # First label
    label = tk.Label(root, text="Welcome to Your First Dashboard!")
    # TODO: Add text color to the label
    # label.configure(fg="color_name", bg="color_name")
    label.pack(pady=20)
    
    # Second label
    name_label = tk.Label(root, text="Created by: Your Name")
    # TODO: Add text color to the second label
    name_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

### Expected Result
A window with custom colors for the background and text.

### Solution
```python
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("My First Dashboard")
    root.geometry("500x300")
    
    # Set background color
    root.configure(bg="#2C3E50")  # Dark blue background
    
    # First label with custom colors
    label = tk.Label(
        root, 
        text="Welcome to Your First Dashboard!",
        fg="white",  # White text
        bg="#2C3E50"  # Same as window background
    )
    label.pack(pady=20)
    
    # Second label with custom colors
    name_label = tk.Label(
        root, 
        text="Created by: Your Name",
        fg="#3498DB",  # Light blue text
        bg="#2C3E50"   # Same as window background
    )
    name_label.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 🎯 Bonus Challenge

### Create a Personal Dashboard Header

Combine all the concepts from the exercises to create a personalized dashboard header:

1. Use a custom title with your name
2. Set a professional color scheme
3. Add multiple labels with different information:
   - A main title
   - Your name and role
   - Today's date
   - A motivational quote

### Example Result
```python
import tkinter as tk
from datetime import datetime

def main():
    root = tk.Tk()
    root.title("John's Professional Dashboard")
    root.geometry("600x400")
    root.configure(bg="#34495E")
    
    # Main title
    title_label = tk.Label(
        root,
        text="PROFESSIONAL DASHBOARD",
        font=("Arial", 16, "bold"),
        fg="#ECF0F1",
        bg="#34495E"
    )
    title_label.pack(pady=20)
    
    # Name and role
    name_label = tk.Label(
        root,
        text="John Smith - Data Analyst",
        font=("Arial", 12),
        fg="#3498DB",
        bg="#34495E"
    )
    name_label.pack(pady=10)
    
    # Date
    date_label = tk.Label(
        root,
        text=f"Date: {datetime.now().strftime('%B %d, %Y')}",
        font=("Arial", 10),
        fg="#95A5A6",
        bg="#34495E"
    )
    date_label.pack(pady=5)
    
    # Quote
    quote_label = tk.Label(
        root,
        text='"Data is the new oil" - Clive Humby',
        font=("Arial", 10, "italic"),
        fg="#E74C3C",
        bg="#34495E"
    )
    quote_label.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 🔍 Key Concepts Reinforced

- **Window Management**: Creating and configuring the main window
- **Widget Creation**: Adding labels to display information
- **Layout**: Using the pack() method to arrange widgets
- **Styling**: Customizing colors and fonts
- **Code Organization**: Structuring code with functions and comments

## 🚀 Next Steps

Once you've completed these exercises:

1. Experiment with different colors and fonts
2. Try adding more labels with different information
3. Move on to Chapter 2 to learn about more widgets and layout management

---

**Great job completing Chapter 1! You're now ready to build more complex dashboards! 🎉**

"""
Chapter 4: Dashboard Architecture
Example: Modular Dashboard Application

This example demonstrates how to create a modular dashboard application
by breaking it down into separate, reusable components.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

# =============================================================================
# CUSTOM WIDGET CLASSES
# =============================================================================

class DashboardHeader(tk.Frame):
    """Header component for the dashboard"""
    
    def __init__(self, parent, title="Dashboard", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.create_widgets()
    
    def create_widgets(self):
        """Create the header widgets"""
        # Title label
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 18, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(side="left", padx=10, pady=5)
        
        # Current time label
        self.time_label = tk.Label(
            self,
            text="",
            font=("Arial", 10),
            fg="#7F8C8D"
        )
        self.time_label.pack(side="right", padx=10, pady=5)
        
        # Update time immediately
        self.update_time()
    
    def update_time(self):
        """Update the current time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=f"Time: {current_time}")
        # Update every second
        self.after(1000, self.update_time)


class MetricCard(tk.Frame):
    """Reusable metric card component"""
    
    def __init__(self, parent, title, value, unit="", **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.title = title
        self.value = value
        self.unit = unit
        self.create_widgets()
    
    def create_widgets(self):
        """Create the metric card widgets"""
        # Title
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 12, "bold"),
            fg="#34495E"
        )
        title_label.pack(pady=(10, 5))
        
        # Value
        self.value_label = tk.Label(
            self,
            text=f"{self.value}{self.unit}",
            font=("Arial", 16, "bold"),
            fg="#2980B9"
        )
        self.value_label.pack(pady=(0, 10))
    
    def update_value(self, new_value):
        """Update the metric value"""
        self.value = new_value
        self.value_label.config(text=f"{self.value}{self.unit}")


class ControlPanel(tk.Frame):
    """Control panel component"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, relief="groove", borderwidth=2, **kwargs)
        self.callbacks = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Create the control panel widgets"""
        # Title
        title_label = tk.Label(
            self,
            text="Controls",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            button_frame,
            text="Refresh Data",
            command=self.refresh_data,
            width=15
        )
        refresh_btn.pack(pady=5)
        
        # Settings button
        settings_btn = tk.Button(
            button_frame,
            text="Settings",
            command=self.open_settings,
            width=15
        )
        settings_btn.pack(pady=5)
        
        # Quit button
        quit_btn = tk.Button(
            button_frame,
            text="Quit",
            command=self.quit_app,
            width=15,
            bg="#E74C3C",
            fg="white"
        )
        quit_btn.pack(pady=5)
    
    def refresh_data(self):
        """Refresh data callback"""
        if 'refresh' in self.callbacks:
            self.callbacks['refresh']()
    
    def open_settings(self):
        """Open settings callback"""
        if 'settings' in self.callbacks:
            self.callbacks['settings']()
    
    def quit_app(self):
        """Quit application callback"""
        if 'quit' in self.callbacks:
            self.callbacks['quit']()
    
    def register_callback(self, action, callback):
        """Register a callback function for an action"""
        self.callbacks[action] = callback


class DataTable(tk.Frame):
    """Data table component using Treeview"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.create_widgets()
    
    def create_widgets(self):
        """Create the data table widgets"""
        # Title
        title_label = tk.Label(
            self,
            text="Recent Data",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        # Create Treeview
        columns = ("Time", "Value", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=6)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
    
    def add_row(self, time, value, status):
        """Add a new row to the table"""
        self.tree.insert("", "end", values=(time, value, status))
        # Keep only last 10 rows
        if len(self.tree.get_children()) > 10:
            self.tree.delete(self.tree.get_children()[0])
    
    def clear_table(self):
        """Clear all rows from the table"""
        for item in self.tree.get_children():
            self.tree.delete(item)


# =============================================================================
# MAIN DASHBOARD APPLICATION
# =============================================================================

class ModularDashboard:
    """Main dashboard application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Modular Dashboard")
        self.root.geometry("800x600")
        
        # Initialize data
        self.metrics = {
            'temperature': 25,
            'humidity': 60,
            'pressure': 1013
        }
        
        # Create the interface
        self.create_widgets()
        self.setup_callbacks()
        
        # Start data simulation
        self.simulate_data()
    
    def create_widgets(self):
        """Create the main dashboard widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Header
        self.header = DashboardHeader(self.root, title="Modular Dashboard")
        self.header.pack(fill="x", padx=10, pady=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Left panel - Metrics
        left_panel = tk.Frame(main_frame, bg="#ECF0F1")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Metrics cards
        self.temp_card = MetricCard(left_panel, "Temperature", 25, "°C")
        self.temp_card.pack(fill="x", pady=5)
        
        self.humidity_card = MetricCard(left_panel, "Humidity", 60, "%")
        self.humidity_card.pack(fill="x", pady=5)
        
        self.pressure_card = MetricCard(left_panel, "Pressure", 1013, " hPa")
        self.pressure_card.pack(fill="x", pady=5)
        
        # Right panel
        right_panel = tk.Frame(main_frame, bg="#ECF0F1")
        right_panel.pack(side="right", fill="both", padx=(5, 0))
        
        # Control panel
        self.control_panel = ControlPanel(right_panel)
        self.control_panel.pack(fill="x", pady=(0, 10))
        
        # Data table
        self.data_table = DataTable(right_panel)
        self.data_table.pack(fill="both", expand=True)
    
    def setup_callbacks(self):
        """Setup callback functions for the control panel"""
        self.control_panel.register_callback('refresh', self.refresh_data)
        self.control_panel.register_callback('settings', self.open_settings)
        self.control_panel.register_callback('quit', self.quit_application)
    
    def refresh_data(self):
        """Refresh all dashboard data"""
        # Update metrics with new random values
        self.metrics['temperature'] = random.randint(20, 30)
        self.metrics['humidity'] = random.randint(50, 70)
        self.metrics['pressure'] = random.randint(1000, 1020)
        
        # Update metric cards
        self.temp_card.update_value(self.metrics['temperature'])
        self.humidity_card.update_value(self.metrics['humidity'])
        self.pressure_card.update_value(self.metrics['pressure'])
        
        # Add to data table
        current_time = datetime.now().strftime("%H:%M:%S")
        self.data_table.add_row(
            current_time,
            f"{self.metrics['temperature']}°C",
            "Normal"
        )
        
        print("Data refreshed!")
    
    def open_settings(self):
        """Open settings dialog"""
        print("Settings dialog would open here")
        # In a real application, this would open a settings window
    
    def quit_application(self):
        """Quit the application"""
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.quit()
    
    def simulate_data(self):
        """Simulate real-time data updates"""
        # Update data every 5 seconds
        self.refresh_data()
        self.root.after(5000, self.simulate_data)


def main():
    """Main application entry point"""
    # Import messagebox for quit confirmation
    global tk
    from tkinter import messagebox
    
    # Create the main window
    root = tk.Tk()
    
    # Create the dashboard application
    dashboard = ModularDashboard(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

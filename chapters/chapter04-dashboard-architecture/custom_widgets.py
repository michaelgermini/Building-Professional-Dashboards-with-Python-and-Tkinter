"""
Chapter 4: Dashboard Architecture
Example: Custom Widget Classes

This example demonstrates how to create reusable custom widget classes
for dashboard components.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import math

# =============================================================================
# CUSTOM WIDGET CLASSES
# =============================================================================

class GaugeWidget(tk.Canvas):
    """Custom gauge widget for displaying values with visual indicators"""
    
    def __init__(self, parent, title="Gauge", min_value=0, max_value=100, 
                 size=150, **kwargs):
        super().__init__(parent, width=size, height=size, **kwargs)
        self.title = title
        self.min_value = min_value
        self.max_value = max_value
        self.size = size
        self.current_value = min_value
        self.create_gauge()
    
    def create_gauge(self):
        """Create the gauge display"""
        # Calculate dimensions
        center_x = self.size // 2
        center_y = self.size // 2
        radius = (self.size // 2) - 20
        
        # Draw gauge background (semi-circle)
        start_angle = 180
        end_angle = 0
        
        # Background arc
        self.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=180,
            fill="#E8E8E8", outline="#CCCCCC", width=3
        )
        
        # Value arc (will be updated)
        self.value_arc = self.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=start_angle, extent=0,
            fill="#2980B9", outline="#2980B9", width=3
        )
        
        # Center circle
        self.create_oval(
            center_x - 10, center_y - 10,
            center_x + 10, center_y + 10,
            fill="#FFFFFF", outline="#CCCCCC", width=2
        )
        
        # Title
        self.create_text(
            center_x, center_y + radius + 20,
            text=self.title,
            font=("Arial", 12, "bold"),
            fill="#2C3E50"
        )
        
        # Value text
        self.value_text = self.create_text(
            center_x, center_y - 10,
            text=f"{self.current_value}",
            font=("Arial", 16, "bold"),
            fill="#2C3E50"
        )
    
    def update_value(self, new_value):
        """Update the gauge value"""
        self.current_value = max(self.min_value, min(self.max_value, new_value))
        
        # Calculate angle
        percentage = (self.current_value - self.min_value) / (self.max_value - self.min_value)
        angle = percentage * 180
        
        # Update value arc
        self.coords(self.value_arc, 
                   self.size//2 - (self.size//2 - 20),
                   self.size//2 - (self.size//2 - 20),
                   self.size//2 + (self.size//2 - 20),
                   self.size//2 + (self.size//2 - 20))
        self.itemconfig(self.value_arc, extent=angle)
        
        # Update value text
        self.itemconfig(self.value_text, text=f"{self.current_value:.1f}")
        
        # Change color based on value
        if percentage < 0.3:
            color = "#27AE60"  # Green
        elif percentage < 0.7:
            color = "#F39C12"  # Orange
        else:
            color = "#E74C3C"  # Red
        
        self.itemconfig(self.value_arc, fill=color, outline=color)


class ProgressCard(tk.Frame):
    """Custom progress card widget with title, value, and progress bar"""
    
    def __init__(self, parent, title="Progress", current=0, maximum=100, 
                 unit="%", **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.title = title
        self.current = current
        self.maximum = maximum
        self.unit = unit
        self.create_widgets()
    
    def create_widgets(self):
        """Create the progress card widgets"""
        # Title
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 12, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=(10, 5))
        
        # Value display
        self.value_label = tk.Label(
            self,
            text=f"{self.current}{self.unit}",
            font=("Arial", 14, "bold"),
            fg="#2980B9"
        )
        self.value_label.pack(pady=(0, 5))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self,
            length=200,
            mode='determinate'
        )
        self.progress.pack(pady=(0, 10))
        
        # Update progress
        self.update_progress()
    
    def update_progress(self):
        """Update the progress bar"""
        percentage = (self.current / self.maximum) * 100
        self.progress['value'] = percentage
        self.value_label.config(text=f"{self.current}{self.unit}")
    
    def set_value(self, new_value):
        """Set a new value"""
        self.current = max(0, min(self.maximum, new_value))
        self.update_progress()


class StatusIndicator(tk.Frame):
    """Custom status indicator widget with colored status lights"""
    
    def __init__(self, parent, title="Status", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.status = "offline"  # offline, online, warning, error
        self.create_widgets()
    
    def create_widgets(self):
        """Create the status indicator widgets"""
        # Title
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 10, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(side="left", padx=(0, 10))
        
        # Status light
        self.status_light = tk.Canvas(
            self,
            width=20,
            height=20,
            bg=self.cget('bg'),
            highlightthickness=0
        )
        self.status_light.pack(side="left")
        
        # Status text
        self.status_text = tk.Label(
            self,
            text="Offline",
            font=("Arial", 10),
            fg="#7F8C8D"
        )
        self.status_text.pack(side="left", padx=(5, 0))
        
        # Set initial status
        self.set_status(self.status)
    
    def set_status(self, status):
        """Set the status indicator"""
        self.status = status
        
        # Define colors for different statuses
        colors = {
            'offline': ('#BDC3C7', '#7F8C8D', 'Offline'),
            'online': ('#27AE60', '#27AE60', 'Online'),
            'warning': ('#F39C12', '#F39C12', 'Warning'),
            'error': ('#E74C3C', '#E74C3C', 'Error')
        }
        
        if status in colors:
            light_color, text_color, text = colors[status]
            
            # Update status light
            self.status_light.delete("all")
            self.status_light.create_oval(
                2, 2, 18, 18,
                fill=light_color,
                outline="#2C3E50",
                width=1
            )
            
            # Update status text
            self.status_text.config(text=text, fg=text_color)


class DataDisplay(tk.Frame):
    """Custom data display widget with multiple data points"""
    
    def __init__(self, parent, title="Data Display", **kwargs):
        super().__init__(parent, relief="groove", borderwidth=2, **kwargs)
        self.title = title
        self.data_points = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Create the data display widgets"""
        # Title
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        # Data frame
        self.data_frame = tk.Frame(self)
        self.data_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def add_data_point(self, name, value, unit=""):
        """Add or update a data point"""
        if name not in self.data_points:
            # Create new data point
            frame = tk.Frame(self.data_frame)
            frame.pack(fill="x", pady=2)
            
            # Label
            label = tk.Label(
                frame,
                text=f"{name}:",
                font=("Arial", 10),
                fg="#34495E"
            )
            label.pack(side="left")
            
            # Value
            value_label = tk.Label(
                frame,
                text=f"{value}{unit}",
                font=("Arial", 10, "bold"),
                fg="#2980B9"
            )
            value_label.pack(side="right")
            
            self.data_points[name] = value_label
        else:
            # Update existing data point
            self.data_points[name].config(text=f"{value}{unit}")
    
    def clear_data(self):
        """Clear all data points"""
        for widget in self.data_frame.winfo_children():
            widget.destroy()
        self.data_points.clear()


# =============================================================================
# EXAMPLE APPLICATION USING CUSTOM WIDGETS
# =============================================================================

class CustomWidgetsDemo:
    """Demo application showcasing custom widgets"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Widgets Demo")
        self.root.geometry("800x600")
        
        # Initialize data
        self.temperature = 25.0
        self.humidity = 60.0
        self.cpu_usage = 45.0
        self.memory_usage = 70.0
        
        self.create_widgets()
        self.start_simulation()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Custom Widgets Dashboard",
            font=("Arial", 18, "bold"),
            fg="#2C3E50",
            bg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Top row - Gauges
        top_frame = tk.Frame(main_frame, bg="#ECF0F1")
        top_frame.pack(fill="x", pady=(0, 20))
        
        # Temperature gauge
        self.temp_gauge = GaugeWidget(
            top_frame,
            title="Temperature",
            min_value=0,
            max_value=50,
            size=150
        )
        self.temp_gauge.pack(side="left", padx=10)
        
        # Humidity gauge
        self.humidity_gauge = GaugeWidget(
            top_frame,
            title="Humidity",
            min_value=0,
            max_value=100,
            size=150
        )
        self.humidity_gauge.pack(side="left", padx=10)
        
        # CPU gauge
        self.cpu_gauge = GaugeWidget(
            top_frame,
            title="CPU Usage",
            min_value=0,
            max_value=100,
            size=150
        )
        self.cpu_gauge.pack(side="left", padx=10)
        
        # Memory gauge
        self.memory_gauge = GaugeWidget(
            top_frame,
            title="Memory",
            min_value=0,
            max_value=100,
            size=150
        )
        self.memory_gauge.pack(side="left", padx=10)
        
        # Bottom row - Other widgets
        bottom_frame = tk.Frame(main_frame, bg="#ECF0F1")
        bottom_frame.pack(fill="both", expand=True)
        
        # Left panel - Progress cards
        left_panel = tk.Frame(bottom_frame, bg="#ECF0F1")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Progress cards
        self.cpu_progress = ProgressCard(
            left_panel,
            title="CPU Usage",
            current=45,
            maximum=100,
            unit="%"
        )
        self.cpu_progress.pack(fill="x", pady=5)
        
        self.memory_progress = ProgressCard(
            left_panel,
            title="Memory Usage",
            current=70,
            maximum=100,
            unit="%"
        )
        self.memory_progress.pack(fill="x", pady=5)
        
        self.disk_progress = ProgressCard(
            left_panel,
            title="Disk Usage",
            current=35,
            maximum=100,
            unit="%"
        )
        self.disk_progress.pack(fill="x", pady=5)
        
        # Right panel - Status and data
        right_panel = tk.Frame(bottom_frame, bg="#ECF0F1")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Status indicators
        status_frame = tk.Frame(right_panel, bg="#ECF0F1")
        status_frame.pack(fill="x", pady=(0, 10))
        
        self.system_status = StatusIndicator(status_frame, title="System")
        self.system_status.pack(fill="x", pady=2)
        
        self.network_status = StatusIndicator(status_frame, title="Network")
        self.network_status.pack(fill="x", pady=2)
        
        self.database_status = StatusIndicator(status_frame, title="Database")
        self.database_status.pack(fill="x", pady=2)
        
        # Data display
        self.data_display = DataDisplay(right_panel, title="System Info")
        self.data_display.pack(fill="both", expand=True)
        
        # Initialize data display
        self.update_data_display()
    
    def update_data_display(self):
        """Update the data display with current values"""
        self.data_display.add_data_point("Temperature", f"{self.temperature:.1f}", "°C")
        self.data_display.add_data_point("Humidity", f"{self.humidity:.1f}", "%")
        self.data_display.add_data_point("CPU Usage", f"{self.cpu_usage:.1f}", "%")
        self.data_display.add_data_point("Memory Usage", f"{self.memory_usage:.1f}", "%")
        self.data_display.add_data_point("Uptime", "2d 14h 32m", "")
        self.data_display.add_data_point("Active Users", "127", "")
    
    def start_simulation(self):
        """Start the data simulation"""
        self.simulate_data()
    
    def simulate_data(self):
        """Simulate changing data values"""
        import random
        
        # Update values with some randomness
        self.temperature += random.uniform(-1, 1)
        self.temperature = max(15, min(35, self.temperature))
        
        self.humidity += random.uniform(-2, 2)
        self.humidity = max(40, min(80, self.humidity))
        
        self.cpu_usage += random.uniform(-5, 5)
        self.cpu_usage = max(10, min(90, self.cpu_usage))
        
        self.memory_usage += random.uniform(-3, 3)
        self.memory_usage = max(50, min(85, self.memory_usage))
        
        # Update gauges
        self.temp_gauge.update_value(self.temperature)
        self.humidity_gauge.update_value(self.humidity)
        self.cpu_gauge.update_value(self.cpu_usage)
        self.memory_gauge.update_value(self.memory_usage)
        
        # Update progress cards
        self.cpu_progress.set_value(self.cpu_usage)
        self.memory_progress.set_value(self.memory_usage)
        
        # Update data display
        self.update_data_display()
        
        # Update status indicators randomly
        if random.random() < 0.1:  # 10% chance to change status
            statuses = ['online', 'warning', 'error']
            self.system_status.set_status(random.choice(statuses))
        
        # Schedule next update
        self.root.after(2000, self.simulate_data)


def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the custom widgets demo
    demo = CustomWidgetsDemo(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

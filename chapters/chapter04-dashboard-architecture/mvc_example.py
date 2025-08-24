"""
Chapter 4: Dashboard Architecture
Example: MVC Pattern Implementation

This example demonstrates how to implement the Model-View-Controller (MVC)
pattern in a Tkinter dashboard application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# =============================================================================
# MODEL - Data and Business Logic
# =============================================================================

class DashboardModel:
    """Model class - handles data and business logic"""
    
    def __init__(self):
        self.data_file = "dashboard_data.json"
        self.metrics = {
            'temperature': 25.0,
            'humidity': 60.0,
            'pressure': 1013.0,
            'last_updated': datetime.now().isoformat()
        }
        self.observers = []  # List of views to notify
        self.load_data()
    
    def add_observer(self, observer):
        """Add a view as an observer"""
        self.observers.append(observer)
    
    def notify_observers(self):
        """Notify all observers of data changes"""
        for observer in self.observers:
            observer.update()
    
    def get_metrics(self):
        """Get current metrics"""
        return self.metrics.copy()
    
    def update_metric(self, metric_name, value):
        """Update a specific metric"""
        if metric_name in self.metrics:
            self.metrics[metric_name] = value
            self.metrics['last_updated'] = datetime.now().isoformat()
            self.save_data()
            self.notify_observers()
            return True
        return False
    
    def update_all_metrics(self, new_metrics):
        """Update all metrics at once"""
        for key, value in new_metrics.items():
            if key in self.metrics:
                self.metrics[key] = value
        
        self.metrics['last_updated'] = datetime.now().isoformat()
        self.save_data()
        self.notify_observers()
    
    def save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.metrics.update(data)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_last_updated(self):
        """Get formatted last updated time"""
        try:
            dt = datetime.fromisoformat(self.metrics['last_updated'])
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "Unknown"


# =============================================================================
# VIEW - User Interface Components
# =============================================================================

class MetricView(tk.Frame):
    """View class for displaying metrics"""
    
    def __init__(self, parent, model, **kwargs):
        super().__init__(parent, **kwargs)
        self.model = model
        self.model.add_observer(self)
        self.create_widgets()
        self.update()
    
    def create_widgets(self):
        """Create the metric display widgets"""
        # Title
        title_label = tk.Label(
            self,
            text="Current Metrics",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        # Metrics frame
        metrics_frame = tk.Frame(self)
        metrics_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Temperature
        self.temp_label = tk.Label(
            metrics_frame,
            text="Temperature: --°C",
            font=("Arial", 14),
            fg="#2980B9"
        )
        self.temp_label.pack(pady=5)
        
        # Humidity
        self.humidity_label = tk.Label(
            metrics_frame,
            text="Humidity: --%",
            font=("Arial", 14),
            fg="#27AE60"
        )
        self.humidity_label.pack(pady=5)
        
        # Pressure
        self.pressure_label = tk.Label(
            metrics_frame,
            text="Pressure: -- hPa",
            font=("Arial", 14),
            fg="#8E44AD"
        )
        self.pressure_label.pack(pady=5)
        
        # Last updated
        self.last_updated_label = tk.Label(
            metrics_frame,
            text="Last Updated: --",
            font=("Arial", 10),
            fg="#7F8C8D"
        )
        self.last_updated_label.pack(pady=10)
    
    def update(self):
        """Update the view with current data"""
        metrics = self.model.get_metrics()
        
        self.temp_label.config(text=f"Temperature: {metrics['temperature']}°C")
        self.humidity_label.config(text=f"Humidity: {metrics['humidity']}%")
        self.pressure_label.config(text=f"Pressure: {metrics['pressure']} hPa")
        self.last_updated_label.config(text=f"Last Updated: {self.model.get_last_updated()}")


class ControlView(tk.Frame):
    """View class for controls"""
    
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller
        self.create_widgets()
    
    def create_widgets(self):
        """Create the control widgets"""
        # Title
        title_label = tk.Label(
            self,
            text="Controls",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10, padx=10)
        
        # Temperature input
        tk.Label(input_frame, text="Temperature (°C):").grid(row=0, column=0, sticky="w", pady=2)
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Humidity input
        tk.Label(input_frame, text="Humidity (%):").grid(row=1, column=0, sticky="w", pady=2)
        self.humidity_entry = tk.Entry(input_frame, width=10)
        self.humidity_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Pressure input
        tk.Label(input_frame, text="Pressure (hPa):").grid(row=2, column=0, sticky="w", pady=2)
        self.pressure_entry = tk.Entry(input_frame, width=10)
        self.pressure_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        # Update button
        update_btn = tk.Button(
            button_frame,
            text="Update Metrics",
            command=self.update_metrics,
            width=15
        )
        update_btn.pack(pady=5)
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self.reset_metrics,
            width=15
        )
        reset_btn.pack(pady=5)
        
        # Load current values
        self.load_current_values()
    
    def load_current_values(self):
        """Load current metric values into entry fields"""
        metrics = self.controller.get_metrics()
        self.temp_entry.delete(0, tk.END)
        self.temp_entry.insert(0, str(metrics['temperature']))
        self.humidity_entry.delete(0, tk.END)
        self.humidity_entry.insert(0, str(metrics['humidity']))
        self.pressure_entry.delete(0, tk.END)
        self.pressure_entry.insert(0, str(metrics['pressure']))
    
    def update_metrics(self):
        """Update metrics with entered values"""
        try:
            temp = float(self.temp_entry.get())
            humidity = float(self.humidity_entry.get())
            pressure = float(self.pressure_entry.get())
            
            new_metrics = {
                'temperature': temp,
                'humidity': humidity,
                'pressure': pressure
            }
            
            self.controller.update_metrics(new_metrics)
            messagebox.showinfo("Success", "Metrics updated successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields.")
    
    def reset_metrics(self):
        """Reset metrics to default values"""
        if messagebox.askyesno("Reset", "Are you sure you want to reset to default values?"):
            self.controller.reset_metrics()
            self.load_current_values()
            messagebox.showinfo("Success", "Metrics reset to default values!")


# =============================================================================
# CONTROLLER - Handles User Interactions
# =============================================================================

class DashboardController:
    """Controller class - handles user interactions and coordinates Model/View"""
    
    def __init__(self, model):
        self.model = model
    
    def get_metrics(self):
        """Get current metrics from model"""
        return self.model.get_metrics()
    
    def update_metrics(self, new_metrics):
        """Update metrics in model"""
        self.model.update_all_metrics(new_metrics)
    
    def reset_metrics(self):
        """Reset metrics to default values"""
        default_metrics = {
            'temperature': 25.0,
            'humidity': 60.0,
            'pressure': 1013.0
        }
        self.model.update_all_metrics(default_metrics)
    
    def update_single_metric(self, metric_name, value):
        """Update a single metric"""
        return self.model.update_metric(metric_name, value)


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class MVCDashboard:
    """Main MVC Dashboard Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MVC Dashboard")
        self.root.geometry("600x500")
        
        # Create Model
        self.model = DashboardModel()
        
        # Create Controller
        self.controller = DashboardController(self.model)
        
        # Create the interface
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="MVC Pattern Dashboard",
            font=("Arial", 18, "bold"),
            fg="#2C3E50",
            bg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Metrics View
        left_panel = tk.Frame(main_frame, bg="#ECF0F1")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.metric_view = MetricView(left_panel, self.model)
        self.metric_view.pack(fill="both", expand=True)
        
        # Right panel - Control View
        right_panel = tk.Frame(main_frame, bg="#ECF0F1")
        right_panel.pack(side="right", fill="both", padx=(10, 0))
        
        self.control_view = ControlView(right_panel, self.controller)
        self.control_view.pack(fill="both", expand=True)
        
        # Status bar
        status_frame = tk.Frame(self.root, bg="#BDC3C7", height=30)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            bg="#BDC3C7",
            fg="#2C3E50"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)


def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the MVC dashboard application
    dashboard = MVCDashboard(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

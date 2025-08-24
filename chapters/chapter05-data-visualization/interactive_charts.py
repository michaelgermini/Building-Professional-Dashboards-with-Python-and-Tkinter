"""
Chapter 5: Data Visualization in Tkinter
Example: Interactive Charts

This example demonstrates how to create interactive charts with
real-time updates, user interactions, and dynamic features.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import random
from datetime import datetime, timedelta
import threading
import time

# =============================================================================
# INTERACTIVE CHART WIDGETS
# =============================================================================

class InteractiveChartWidget(tk.Frame):
    """Base class for interactive chart widgets"""
    
    def __init__(self, parent, title="Interactive Chart", **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.title = title
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.is_updating = False
        self.create_widgets()
    
    def create_widgets(self):
        """Create the interactive chart widget interface"""
        # Title frame
        title_frame = tk.Frame(self)
        title_frame.pack(fill="x", padx=5, pady=5)
        
        # Title
        title_label = tk.Label(
            title_frame,
            text=self.title,
            font=("Arial", 12, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(side="left")
        
        # Control buttons
        self.pause_btn = tk.Button(
            title_frame,
            text="Pause",
            command=self.toggle_pause,
            width=8
        )
        self.pause_btn.pack(side="right", padx=5)
        
        self.clear_btn = tk.Button(
            title_frame,
            text="Clear",
            command=self.clear_data,
            width=8
        )
        self.clear_btn.pack(side="right", padx=5)
        
        # Chart will be created by subclasses
        self.create_chart()
    
    def create_chart(self):
        """Create the chart - to be implemented by subclasses"""
        pass
    
    def toggle_pause(self):
        """Toggle chart updates on/off"""
        self.is_updating = not self.is_updating
        if self.is_updating:
            self.pause_btn.config(text="Pause")
        else:
            self.pause_btn.config(text="Resume")
    
    def clear_data(self):
        """Clear chart data - to be implemented by subclasses"""
        pass


class RealTimeLineChart(InteractiveChartWidget):
    """Real-time line chart with live data updates"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Real-Time Line Chart", **kwargs)
        self.data_x = []
        self.data_y = []
        self.max_points = 100
        self.update_interval = 1000  # milliseconds
        self.start_time = datetime.now()
        self.is_updating = True
        self.start_data_thread()
    
    def create_chart(self):
        """Create the real-time line chart"""
        # Create figure and axes
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Initial data
        self.data_x = [0]
        self.data_y = [random.randint(20, 80)]
        
        # Create the line plot
        self.line, = self.ax.plot(self.data_x, self.data_y, 'b-', linewidth=2, marker='o', markersize=4)
        
        # Customize the chart
        self.ax.set_title("Real-Time Data Stream", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Time (seconds)", fontsize=12)
        self.ax.set_ylabel("Value", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(0, 100)
        
        # Add horizontal lines for thresholds
        self.ax.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='High Threshold')
        self.ax.axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Low Threshold')
        self.ax.legend()
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        
        # Bind mouse events
        self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)
        self.canvas.mpl_connect('button_press_event', self.on_click)
    
    def add_data_point(self, value):
        """Add a new data point to the chart"""
        if not self.is_updating:
            return
        
        # Calculate time since start
        current_time = datetime.now()
        elapsed = (current_time - self.start_time).total_seconds()
        
        # Add new point
        self.data_x.append(elapsed)
        self.data_y.append(value)
        
        # Keep only the last max_points
        if len(self.data_x) > self.max_points:
            self.data_x.pop(0)
            self.data_y.pop(0)
        
        # Update the line data
        self.line.set_data(self.data_x, self.data_y)
        
        # Adjust x-axis limits for scrolling effect
        if len(self.data_x) > 1:
            x_min = max(0, self.data_x[-1] - 30)  # Show last 30 seconds
            x_max = self.data_x[-1] + 2
            self.ax.set_xlim(x_min, x_max)
        
        # Redraw the canvas
        self.canvas.draw()
    
    def clear_data(self):
        """Clear all data from the chart"""
        self.data_x = [0]
        self.data_y = [random.randint(20, 80)]
        self.start_time = datetime.now()
        self.line.set_data(self.data_x, self.data_y)
        self.ax.set_xlim(0, 10)
        self.canvas.draw()
    
    def on_mouse_move(self, event):
        """Handle mouse movement over the chart"""
        if event.inaxes:
            # Update status bar or tooltip with coordinates
            pass
    
    def on_click(self, event):
        """Handle mouse clicks on the chart"""
        if event.inaxes and event.button == 1:  # Left click
            # Add a manual data point
            if event.ydata is not None:
                self.add_data_point(event.ydata)
    
    def start_data_thread(self):
        """Start the data generation thread"""
        def generate_data():
            while True:
                if self.is_updating:
                    # Generate realistic data with some trend
                    if len(self.data_y) > 0:
                        last_value = self.data_y[-1]
                        # Add some trend and noise
                        trend = random.uniform(-2, 2)
                        noise = random.uniform(-5, 5)
                        new_value = max(0, min(100, last_value + trend + noise))
                    else:
                        new_value = random.randint(20, 80)
                    
                    # Use after() to update from main thread
                    self.after(0, self.add_data_point, new_value)
                
                time.sleep(self.update_interval / 1000)
        
        # Start thread
        thread = threading.Thread(target=generate_data, daemon=True)
        thread.start()


class InteractiveBarChart(InteractiveChartWidget):
    """Interactive bar chart with clickable bars"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Interactive Bar Chart", **kwargs)
        self.categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        self.values = [random.randint(10, 90) for _ in range(5)]
        self.colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6']
        self.selected_bar = None
    
    def create_chart(self):
        """Create the interactive bar chart"""
        # Create figure and axes
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create the bar plot
        self.bars = self.ax.bar(self.categories, self.values, color=self.colors, alpha=0.7)
        
        # Add value labels on bars
        self.value_labels = []
        for bar, value in zip(self.bars, self.values):
            height = bar.get_height()
            label = self.ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                               f'{value}', ha='center', va='bottom', fontweight='bold')
            self.value_labels.append(label)
        
        # Customize the chart
        self.ax.set_title("Interactive Bar Chart (Click bars to update)", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("Categories", fontsize=12)
        self.ax.set_ylabel("Values", fontsize=12)
        self.ax.grid(True, alpha=0.3, axis='y')
        self.ax.set_ylim(0, 100)
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        
        # Bind click events
        self.canvas.mpl_connect('button_press_event', self.on_bar_click)
    
    def on_bar_click(self, event):
        """Handle clicks on bars"""
        if event.inaxes:
            for i, bar in enumerate(self.bars):
                if bar.contains(event)[0]:
                    # Update the clicked bar
                    new_value = random.randint(10, 90)
                    self.values[i] = new_value
                    bar.set_height(new_value)
                    
                    # Update the value label
                    self.value_labels[i].set_text(f'{new_value}')
                    self.value_labels[i].set_position((bar.get_x() + bar.get_width()/2., new_value + 1))
                    
                    # Highlight the selected bar
                    if self.selected_bar:
                        self.selected_bar.set_alpha(0.7)
                    bar.set_alpha(1.0)
                    self.selected_bar = bar
                    
                    # Redraw the canvas
                    self.canvas.draw()
                    
                    # Show message
                    messagebox.showinfo("Bar Updated", f"{self.categories[i]}: {new_value}")
                    break
    
    def clear_data(self):
        """Clear and reset the bar chart data"""
        self.values = [random.randint(10, 90) for _ in range(5)]
        
        # Update bars
        for bar, value in zip(self.bars, self.values):
            bar.set_height(value)
        
        # Update labels
        for label, value in zip(self.value_labels, self.values):
            label.set_text(f'{value}')
            label.set_position((label.get_position()[0], value + 1))
        
        # Reset alpha
        for bar in self.bars:
            bar.set_alpha(0.7)
        self.selected_bar = None
        
        self.canvas.draw()


class DynamicPieChart(InteractiveChartWidget):
    """Dynamic pie chart with animated updates"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Dynamic Pie Chart", **kwargs)
        self.labels = ['Sales', 'Marketing', 'Development', 'Support', 'Other']
        self.values = [30, 25, 20, 15, 10]
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        self.wedges = None
        self.autotexts = None
        self.is_updating = True
        self.start_animation()
    
    def create_chart(self):
        """Create the dynamic pie chart"""
        # Create figure and axes
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create the pie chart
        self.wedges, texts, self.autotexts = self.ax.pie(
            self.values, 
            labels=self.labels, 
            autopct='%1.1f%%',
            colors=self.colors,
            startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05)
        )
        
        # Customize text
        for autotext in self.autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Customize the chart
        self.ax.set_title("Dynamic Pie Chart", fontsize=14, fontweight='bold')
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def update_values(self):
        """Update pie chart values with animation"""
        if not self.is_updating:
            return
        
        # Generate new values
        new_values = []
        for i in range(len(self.values)):
            # Add some randomness to current values
            change = random.uniform(-5, 5)
            new_value = max(5, min(40, self.values[i] + change))
            new_values.append(new_value)
        
        # Normalize to sum to 100
        total = sum(new_values)
        self.values = [int(v * 100 / total) for v in new_values]
        
        # Update the pie chart
        self.ax.clear()
        self.wedges, texts, self.autotexts = self.ax.pie(
            self.values, 
            labels=self.labels, 
            autopct='%1.1f%%',
            colors=self.colors,
            startangle=90,
            explode=(0.05, 0.05, 0.05, 0.05, 0.05)
        )
        
        # Customize text
        for autotext in self.autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Customize the chart
        self.ax.set_title("Dynamic Pie Chart", fontsize=14, fontweight='bold')
        
        # Redraw the canvas
        self.canvas.draw()
    
    def clear_data(self):
        """Reset pie chart to initial values"""
        self.values = [30, 25, 20, 15, 10]
        self.update_values()
    
    def start_animation(self):
        """Start the animation loop"""
        def animate():
            while True:
                if self.is_updating:
                    self.after(0, self.update_values)
                time.sleep(3)  # Update every 3 seconds
        
        # Start animation thread
        thread = threading.Thread(target=animate, daemon=True)
        thread.start()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class InteractiveChartsDemo:
    """Demo application showcasing interactive charts"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Charts Demo")
        self.root.geometry("1400x900")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Interactive Charts Demo",
            font=("Arial", 18, "bold"),
            fg="#2C3E50",
            bg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="• Real-time line chart updates automatically\n• Click bars in the bar chart to update values\n• Pie chart animates every 3 seconds\n• Use pause/resume buttons to control updates",
            font=("Arial", 10),
            fg="#7F8C8D",
            bg="#ECF0F1",
            justify="left"
        )
        instructions.pack(pady=10)
        
        # Charts frame
        charts_frame = tk.Frame(self.root, bg="#ECF0F1")
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Top row - Real-time line chart
        top_frame = tk.Frame(charts_frame, bg="#ECF0F1")
        top_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.realtime_chart = RealTimeLineChart(top_frame)
        self.realtime_chart.pack(fill="both", expand=True)
        
        # Bottom row - Bar and Pie charts
        bottom_frame = tk.Frame(charts_frame, bg="#ECF0F1")
        bottom_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Bar chart
        self.bar_chart = InteractiveBarChart(bottom_frame)
        self.bar_chart.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Pie chart
        self.pie_chart = DynamicPieChart(bottom_frame)
        self.pie_chart.pack(side="right", fill="both", expand=True, padx=(5, 0))


def main():
    """Main application entry point"""
    # Set Matplotlib style
    plt.style.use('default')
    
    # Create the main window
    root = tk.Tk()
    
    # Create the interactive charts demo
    demo = InteractiveChartsDemo(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

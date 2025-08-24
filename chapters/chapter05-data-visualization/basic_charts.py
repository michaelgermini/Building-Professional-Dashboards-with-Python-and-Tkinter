"""
Chapter 5: Data Visualization in Tkinter
Example: Basic Chart Types

This example demonstrates how to create various chart types
using Matplotlib integrated with Tkinter.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import random

# =============================================================================
# CHART WIDGET CLASSES
# =============================================================================

class ChartWidget(tk.Frame):
    """Base class for chart widgets"""
    
    def __init__(self, parent, title="Chart", **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.title = title
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create the chart widget interface"""
        # Title
        title_label = tk.Label(
            self,
            text=self.title,
            font=("Arial", 12, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=5)
        
        # Chart will be created by subclasses
        self.create_chart()
    
    def create_chart(self):
        """Create the chart - to be implemented by subclasses"""
        pass
    
    def update_chart(self):
        """Update the chart - to be implemented by subclasses"""
        pass


class LineChartWidget(ChartWidget):
    """Line chart widget for time series data"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Line Chart", **kwargs)
        self.data_x = []
        self.data_y = []
        self.max_points = 50
    
    def create_chart(self):
        """Create the line chart"""
        # Create figure and axes
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Initial data
        self.data_x = list(range(10))
        self.data_y = [random.randint(10, 90) for _ in range(10)]
        
        # Create the line plot
        self.line, = self.ax.plot(self.data_x, self.data_y, 'b-', linewidth=2, marker='o')
        
        # Customize the chart
        self.ax.set_title("Time Series Data", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Time", fontsize=10)
        self.ax.set_ylabel("Value", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(0, 100)
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def add_data_point(self, value):
        """Add a new data point to the chart"""
        # Add new point
        if len(self.data_x) == 0:
            self.data_x.append(0)
        else:
            self.data_x.append(self.data_x[-1] + 1)
        
        self.data_y.append(value)
        
        # Keep only the last max_points
        if len(self.data_x) > self.max_points:
            self.data_x.pop(0)
            self.data_y.pop(0)
        
        # Update the line data
        self.line.set_data(self.data_x, self.data_y)
        
        # Adjust x-axis limits
        if len(self.data_x) > 1:
            self.ax.set_xlim(self.data_x[0], self.data_x[-1])
        
        # Redraw the canvas
        self.canvas.draw()


class BarChartWidget(ChartWidget):
    """Bar chart widget for categorical data"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Bar Chart", **kwargs)
        self.categories = []
        self.values = []
    
    def create_chart(self):
        """Create the bar chart"""
        # Create figure and axes
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Sample data
        self.categories = ['A', 'B', 'C', 'D', 'E']
        self.values = [23, 45, 56, 78, 32]
        
        # Create the bar plot
        bars = self.ax.bar(self.categories, self.values, color='skyblue', alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, self.values):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{value}', ha='center', va='bottom', fontweight='bold')
        
        # Customize the chart
        self.ax.set_title("Categorical Data", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Categories", fontsize=10)
        self.ax.set_ylabel("Values", fontsize=10)
        self.ax.grid(True, alpha=0.3, axis='y')
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def update_data(self, categories, values):
        """Update the bar chart data"""
        self.categories = categories
        self.values = values
        
        # Clear the axes
        self.ax.clear()
        
        # Create new bar plot
        bars = self.ax.bar(self.categories, self.values, color='skyblue', alpha=0.7)
        
        # Add value labels on bars
        for bar, value in zip(bars, self.values):
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{value}', ha='center', va='bottom', fontweight='bold')
        
        # Customize the chart
        self.ax.set_title("Categorical Data", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Categories", fontsize=10)
        self.ax.set_ylabel("Values", fontsize=10)
        self.ax.grid(True, alpha=0.3, axis='y')
        
        # Redraw the canvas
        self.canvas.draw()


class PieChartWidget(ChartWidget):
    """Pie chart widget for proportional data"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Pie Chart", **kwargs)
        self.labels = []
        self.values = []
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    def create_chart(self):
        """Create the pie chart"""
        # Create figure and axes
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Sample data
        self.labels = ['Category A', 'Category B', 'Category C', 'Category D']
        self.values = [30, 25, 20, 25]
        
        # Create the pie chart
        wedges, texts, autotexts = self.ax.pie(
            self.values, 
            labels=self.labels, 
            autopct='%1.1f%%',
            colors=self.colors[:len(self.values)],
            startangle=90
        )
        
        # Customize text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Customize the chart
        self.ax.set_title("Proportional Data", fontsize=12, fontweight='bold')
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def update_data(self, labels, values):
        """Update the pie chart data"""
        self.labels = labels
        self.values = values
        
        # Clear the axes
        self.ax.clear()
        
        # Create new pie chart
        wedges, texts, autotexts = self.ax.pie(
            self.values, 
            labels=self.labels, 
            autopct='%1.1f%%',
            colors=self.colors[:len(self.values)],
            startangle=90
        )
        
        # Customize text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # Customize the chart
        self.ax.set_title("Proportional Data", fontsize=12, fontweight='bold')
        
        # Redraw the canvas
        self.canvas.draw()


class ScatterChartWidget(ChartWidget):
    """Scatter plot widget for correlation data"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Scatter Plot", **kwargs)
        self.data_x = []
        self.data_y = []
        self.max_points = 100
    
    def create_chart(self):
        """Create the scatter plot"""
        # Create figure and axes
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Generate sample data
        np.random.seed(42)
        self.data_x = np.random.randn(50)
        self.data_y = 0.7 * self.data_x + np.random.randn(50) * 0.5
        
        # Create the scatter plot
        self.scatter = self.ax.scatter(self.data_x, self.data_y, alpha=0.6, c='blue', s=50)
        
        # Customize the chart
        self.ax.set_title("Correlation Analysis", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("X Values", fontsize=10)
        self.ax.set_ylabel("Y Values", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(self.data_x, self.data_y, 1)
        p = np.poly1d(z)
        self.ax.plot(self.data_x, p(self.data_x), "r--", alpha=0.8, linewidth=2)
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def add_data_point(self, x, y):
        """Add a new data point to the scatter plot"""
        self.data_x.append(x)
        self.data_y.append(y)
        
        # Keep only the last max_points
        if len(self.data_x) > self.max_points:
            self.data_x.pop(0)
            self.data_y.pop(0)
        
        # Update the scatter plot
        self.ax.clear()
        self.scatter = self.ax.scatter(self.data_x, self.data_y, alpha=0.6, c='blue', s=50)
        
        # Add trend line if we have enough points
        if len(self.data_x) > 2:
            z = np.polyfit(self.data_x, self.data_y, 1)
            p = np.poly1d(z)
            self.ax.plot(self.data_x, p(self.data_x), "r--", alpha=0.8, linewidth=2)
        
        # Customize the chart
        self.ax.set_title("Correlation Analysis", fontsize=12, fontweight='bold')
        self.ax.set_xlabel("X Values", fontsize=10)
        self.ax.set_ylabel("Y Values", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        
        # Redraw the canvas
        self.canvas.draw()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class BasicChartsDemo:
    """Demo application showcasing basic chart types"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Charts Demo")
        self.root.geometry("1200x800")
        
        # Initialize data
        self.line_counter = 0
        self.scatter_counter = 0
        
        self.create_widgets()
        self.start_data_simulation()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Basic Chart Types Demo",
            font=("Arial", 18, "bold"),
            fg="#2C3E50",
            bg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Control panel
        control_frame = tk.Frame(self.root, bg="#ECF0F1")
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Add data buttons
        tk.Button(
            control_frame,
            text="Add Line Data",
            command=self.add_line_data,
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="Add Scatter Data",
            command=self.add_scatter_data,
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="Update Bar Chart",
            command=self.update_bar_chart,
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            control_frame,
            text="Update Pie Chart",
            command=self.update_pie_chart,
            width=15
        ).pack(side="left", padx=5)
        
        # Charts frame
        charts_frame = tk.Frame(self.root, bg="#ECF0F1")
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Top row - Line and Bar charts
        top_frame = tk.Frame(charts_frame, bg="#ECF0F1")
        top_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Line chart
        self.line_chart = LineChartWidget(top_frame)
        self.line_chart.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Bar chart
        self.bar_chart = BarChartWidget(top_frame)
        self.bar_chart.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Bottom row - Pie and Scatter charts
        bottom_frame = tk.Frame(charts_frame, bg="#ECF0F1")
        bottom_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Pie chart
        self.pie_chart = PieChartWidget(bottom_frame)
        self.pie_chart.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Scatter chart
        self.scatter_chart = ScatterChartWidget(bottom_frame)
        self.scatter_chart.pack(side="right", fill="both", expand=True, padx=(5, 0))
    
    def add_line_data(self):
        """Add data point to line chart"""
        value = random.randint(10, 90)
        self.line_chart.add_data_point(value)
        self.line_counter += 1
    
    def add_scatter_data(self):
        """Add data point to scatter chart"""
        x = random.uniform(-3, 3)
        y = 0.7 * x + random.uniform(-1, 1)
        self.scatter_chart.add_data_point(x, y)
        self.scatter_counter += 1
    
    def update_bar_chart(self):
        """Update bar chart with new data"""
        categories = ['A', 'B', 'C', 'D', 'E', 'F']
        values = [random.randint(20, 80) for _ in range(6)]
        self.bar_chart.update_data(categories, values)
    
    def update_pie_chart(self):
        """Update pie chart with new data"""
        labels = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        values = [random.randint(10, 40) for _ in range(5)]
        # Ensure values sum to 100
        total = sum(values)
        values = [int(v * 100 / total) for v in values]
        self.pie_chart.update_data(labels, values)
    
    def start_data_simulation(self):
        """Start automatic data simulation"""
        self.simulate_data()
    
    def simulate_data(self):
        """Simulate data updates"""
        # Add random data points
        if random.random() < 0.3:  # 30% chance
            self.add_line_data()
        
        if random.random() < 0.2:  # 20% chance
            self.add_scatter_data()
        
        # Schedule next update
        self.root.after(2000, self.simulate_data)


def main():
    """Main application entry point"""
    # Set Matplotlib style
    plt.style.use('default')
    
    # Create the main window
    root = tk.Tk()
    
    # Create the charts demo
    demo = BasicChartsDemo(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

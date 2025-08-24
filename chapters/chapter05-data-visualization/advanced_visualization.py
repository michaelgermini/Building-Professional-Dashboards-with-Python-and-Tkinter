"""
Chapter 5: Data Visualization in Tkinter
Example: Advanced Visualization Features

This example demonstrates advanced visualization techniques including:
- Subplot layouts and complex chart arrangements
- Custom styling and themes
- Statistical charts (histograms, box plots)
- 3D visualizations
- Custom color maps and annotations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import random
import pandas as pd
from datetime import datetime, timedelta
import threading
import time

# =============================================================================
# ADVANCED CHART WIDGETS
# =============================================================================

class AdvancedChartWidget(tk.Frame):
    """Base class for advanced chart widgets"""
    
    def __init__(self, parent, title="Advanced Chart", **kwargs):
        super().__init__(parent, relief="raised", borderwidth=2, **kwargs)
        self.title = title
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create the advanced chart widget interface"""
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
        self.refresh_btn = tk.Button(
            title_frame,
            text="Refresh",
            command=self.refresh_data,
            width=8
        )
        self.refresh_btn.pack(side="right", padx=5)
        
        self.export_btn = tk.Button(
            title_frame,
            text="Export",
            command=self.export_chart,
            width=8
        )
        self.export_btn.pack(side="right", padx=5)
        
        # Chart will be created by subclasses
        self.create_chart()
    
    def create_chart(self):
        """Create the chart - to be implemented by subclasses"""
        pass
    
    def refresh_data(self):
        """Refresh chart data - to be implemented by subclasses"""
        pass
    
    def export_chart(self):
        """Export chart to file"""
        try:
            filename = f"{self.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Export Successful", f"Chart saved as {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export chart: {e}")


class MultiSubplotDashboard(AdvancedChartWidget):
    """Dashboard with multiple subplots showing different visualizations"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Multi-Subplot Dashboard", **kwargs)
        self.data = self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample data for all charts"""
        np.random.seed(42)
        
        # Time series data
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        sales_data = np.cumsum(np.random.randn(100) * 10 + 50)
        
        # Categorical data
        categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
        category_sales = np.random.randint(100, 1000, 5)
        
        # Distribution data
        normal_data = np.random.normal(100, 20, 1000)
        exponential_data = np.random.exponential(50, 1000)
        
        # Correlation data
        x_corr = np.random.normal(0, 1, 100)
        y_corr = 0.7 * x_corr + np.random.normal(0, 0.3, 100)
        
        return {
            'dates': dates,
            'sales': sales_data,
            'categories': categories,
            'category_sales': category_sales,
            'normal_data': normal_data,
            'exponential_data': exponential_data,
            'x_corr': x_corr,
            'y_corr': y_corr
        }
    
    def create_chart(self):
        """Create the multi-subplot dashboard"""
        # Create figure with subplots
        self.figure = Figure(figsize=(12, 8), dpi=100)
        
        # Create a 2x3 grid of subplots
        gs = self.figure.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
        
        # 1. Line chart (top left)
        ax1 = self.figure.add_subplot(gs[0, 0])
        ax1.plot(self.data['dates'], self.data['sales'], 'b-', linewidth=2)
        ax1.set_title('Sales Trend', fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sales')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Bar chart (top middle)
        ax2 = self.figure.add_subplot(gs[0, 1])
        bars = ax2.bar(self.data['categories'], self.data['category_sales'], 
                      color=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6'])
        ax2.set_title('Sales by Category', fontweight='bold')
        ax2.set_ylabel('Sales')
        ax2.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, value in zip(bars, self.data['category_sales']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 10,
                    f'{value}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Histogram (top right)
        ax3 = self.figure.add_subplot(gs[0, 2])
        ax3.hist(self.data['normal_data'], bins=30, alpha=0.7, color='#3498DB', edgecolor='black')
        ax3.set_title('Sales Distribution', fontweight='bold')
        ax3.set_xlabel('Sales Value')
        ax3.set_ylabel('Frequency')
        ax3.grid(True, alpha=0.3)
        
        # Add mean line
        mean_val = np.mean(self.data['normal_data'])
        ax3.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.1f}')
        ax3.legend()
        
        # 4. Scatter plot (bottom left)
        ax4 = self.figure.add_subplot(gs[1, 0])
        scatter = ax4.scatter(self.data['x_corr'], self.data['y_corr'], 
                            alpha=0.6, c=self.data['x_corr'], cmap='viridis')
        ax4.set_title('Correlation Analysis', fontweight='bold')
        ax4.set_xlabel('Variable X')
        ax4.set_ylabel('Variable Y')
        ax4.grid(True, alpha=0.3)
        
        # Add correlation coefficient
        corr_coef = np.corrcoef(self.data['x_corr'], self.data['y_corr'])[0, 1]
        ax4.text(0.05, 0.95, f'r = {corr_coef:.3f}', transform=ax4.transAxes, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # 5. Box plot (bottom middle)
        ax5 = self.figure.add_subplot(gs[1, 1])
        box_data = [self.data['normal_data'], self.data['exponential_data']]
        bp = ax5.boxplot(box_data, labels=['Normal', 'Exponential'], patch_artist=True)
        
        # Color the boxes
        colors = ['#3498DB', '#E74C3C']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax5.set_title('Data Distribution Comparison', fontweight='bold')
        ax5.set_ylabel('Values')
        ax5.grid(True, alpha=0.3)
        
        # 6. Pie chart (bottom right)
        ax6 = self.figure.add_subplot(gs[1, 2])
        wedges, texts, autotexts = ax6.pie(self.data['category_sales'], 
                                          labels=self.data['categories'],
                                          autopct='%1.1f%%',
                                          colors=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12', '#9B59B6'])
        
        # Customize pie chart text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax6.set_title('Market Share', fontweight='bold')
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def refresh_data(self):
        """Refresh all chart data"""
        self.data = self.generate_sample_data()
        self.create_chart()


class StatisticalChartsWidget(AdvancedChartWidget):
    """Widget showcasing various statistical charts"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Statistical Charts", **kwargs)
        self.data = self.generate_statistical_data()
    
    def generate_statistical_data(self):
        """Generate statistical data for charts"""
        np.random.seed(42)
        
        # Multiple normal distributions
        data1 = np.random.normal(50, 10, 200)
        data2 = np.random.normal(70, 15, 200)
        data3 = np.random.normal(30, 8, 200)
        
        # Time series with trend and seasonality
        t = np.linspace(0, 10, 100)
        trend = 2 * t
        seasonality = 10 * np.sin(2 * np.pi * t)
        noise = np.random.normal(0, 2, 100)
        time_series = trend + seasonality + noise
        
        # Categorical data with confidence intervals
        categories = ['Group A', 'Group B', 'Group C', 'Group D']
        means = [45, 62, 38, 55]
        stds = [8, 12, 6, 10]
        
        return {
            'data1': data1, 'data2': data2, 'data3': data3,
            'time_series': time_series, 'time': t,
            'categories': categories, 'means': means, 'stds': stds
        }
    
    def create_chart(self):
        """Create statistical charts"""
        # Create figure with subplots
        self.figure = Figure(figsize=(12, 8), dpi=100)
        
        # Create a 2x2 grid
        gs = self.figure.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Violin plot
        ax1 = self.figure.add_subplot(gs[0, 0])
        violin_parts = ax1.violinplot([self.data['data1'], self.data['data2'], self.data['data3']], 
                                    positions=[1, 2, 3], showmeans=True)
        
        # Color the violin plots
        colors = ['#3498DB', '#E74C3C', '#2ECC71']
        for pc, color in zip(violin_parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        
        ax1.set_title('Distribution Comparison (Violin Plot)', fontweight='bold')
        ax1.set_ylabel('Values')
        ax1.set_xticks([1, 2, 3])
        ax1.set_xticklabels(['Group 1', 'Group 2', 'Group 3'])
        ax1.grid(True, alpha=0.3)
        
        # 2. Time series with confidence intervals
        ax2 = self.figure.add_subplot(gs[0, 1])
        
        # Calculate rolling mean and std
        window = 10
        rolling_mean = pd.Series(self.data['time_series']).rolling(window=window).mean()
        rolling_std = pd.Series(self.data['time_series']).rolling(window=window).std()
        
        # Plot time series
        ax2.plot(self.data['time'], self.data['time_series'], 'b-', alpha=0.6, label='Raw Data')
        ax2.plot(self.data['time'], rolling_mean, 'r-', linewidth=2, label='Rolling Mean')
        
        # Add confidence intervals
        ax2.fill_between(self.data['time'], 
                        rolling_mean - 2*rolling_std, 
                        rolling_mean + 2*rolling_std, 
                        alpha=0.3, color='red', label='95% CI')
        
        ax2.set_title('Time Series with Confidence Intervals', fontweight='bold')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Value')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Error bar chart
        ax3 = self.figure.add_subplot(gs[1, 0])
        bars = ax3.bar(self.data['categories'], self.data['means'], 
                      yerr=self.data['stds'], capsize=5, 
                      color=['#3498DB', '#E74C3C', '#2ECC71', '#F39C12'], alpha=0.7)
        
        ax3.set_title('Means with Standard Deviation', fontweight='bold')
        ax3.set_ylabel('Mean Value')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # 4. Heatmap-like visualization
        ax4 = self.figure.add_subplot(gs[1, 1])
        
        # Create correlation matrix
        data_matrix = np.column_stack([self.data['data1'], self.data['data2'], self.data['data3']])
        corr_matrix = np.corrcoef(data_matrix.T)
        
        im = ax4.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Add correlation values as text
        for i in range(corr_matrix.shape[0]):
            for j in range(corr_matrix.shape[1]):
                text = ax4.text(j, i, f'{corr_matrix[i, j]:.2f}',
                              ha="center", va="center", color="white", fontweight='bold')
        
        ax4.set_title('Correlation Matrix', fontweight='bold')
        ax4.set_xticks(range(3))
        ax4.set_yticks(range(3))
        ax4.set_xticklabels(['Group 1', 'Group 2', 'Group 3'])
        ax4.set_yticklabels(['Group 1', 'Group 2', 'Group 3'])
        
        # Add colorbar
        self.figure.colorbar(im, ax=ax4, shrink=0.8)
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def refresh_data(self):
        """Refresh statistical data"""
        self.data = self.generate_statistical_data()
        self.create_chart()


class CustomStyledCharts(AdvancedChartWidget):
    """Widget showcasing custom styled charts with advanced features"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Custom Styled Charts", **kwargs)
        self.data = self.generate_custom_data()
    
    def generate_custom_data(self):
        """Generate data for custom styled charts"""
        np.random.seed(42)
        
        # Generate sample data
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x) + np.random.normal(0, 0.1, 100)
        y2 = np.cos(x) + np.random.normal(0, 0.1, 100)
        
        # Generate categorical data
        categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        values1 = [120, 150, 180, 200, 220, 250]
        values2 = [100, 130, 160, 180, 200, 230]
        
        return {
            'x': x, 'y1': y1, 'y2': y2,
            'categories': categories, 'values1': values1, 'values2': values2
        }
    
    def create_chart(self):
        """Create custom styled charts"""
        # Set custom style
        plt.style.use('seaborn-v0_8')
        
        # Create figure with custom styling
        self.figure = Figure(figsize=(12, 8), dpi=100, facecolor='#f8f9fa')
        
        # Create a 2x2 grid
        gs = self.figure.add_gridspec(2, 2, hspace=0.4, wspace=0.3)
        
        # 1. Custom styled line chart
        ax1 = self.figure.add_subplot(gs[0, 0])
        ax1.plot(self.data['x'], self.data['y1'], 'o-', linewidth=2, markersize=4, 
                color='#3498DB', label='Sine Wave', alpha=0.8)
        ax1.plot(self.data['x'], self.data['y2'], 's-', linewidth=2, markersize=4, 
                color='#E74C3C', label='Cosine Wave', alpha=0.8)
        
        # Customize the plot
        ax1.set_title('Custom Styled Line Chart', fontsize=14, fontweight='bold', color='#2C3E50')
        ax1.set_xlabel('X Axis', fontsize=12, color='#34495E')
        ax1.set_ylabel('Y Axis', fontsize=12, color='#34495E')
        ax1.legend(frameon=True, fancybox=True, shadow=True)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Add custom annotations
        ax1.annotate('Peak', xy=(np.pi/2, 1), xytext=(np.pi/2 + 1, 1.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    fontsize=10, color='red', fontweight='bold')
        
        # 2. Gradient filled area chart
        ax2 = self.figure.add_subplot(gs[0, 1])
        
        # Create gradient fill
        ax2.fill_between(self.data['x'], self.data['y1'], alpha=0.3, 
                        color='#3498DB', label='Sine Area')
        ax2.fill_between(self.data['x'], self.data['y2'], alpha=0.3, 
                        color='#E74C3C', label='Cosine Area')
        
        ax2.plot(self.data['x'], self.data['y1'], 'b-', linewidth=2, alpha=0.8)
        ax2.plot(self.data['x'], self.data['y2'], 'r-', linewidth=2, alpha=0.8)
        
        ax2.set_title('Gradient Filled Area Chart', fontsize=14, fontweight='bold', color='#2C3E50')
        ax2.set_xlabel('X Axis', fontsize=12, color='#34495E')
        ax2.set_ylabel('Y Axis', fontsize=12, color='#34495E')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Custom styled bar chart with patterns
        ax3 = self.figure.add_subplot(gs[1, 0])
        
        x_pos = np.arange(len(self.data['categories']))
        width = 0.35
        
        bars1 = ax3.bar(x_pos - width/2, self.data['values1'], width, 
                       label='Series 1', color='#3498DB', alpha=0.8, edgecolor='black')
        bars2 = ax3.bar(x_pos + width/2, self.data['values2'], width, 
                       label='Series 2', color='#E74C3C', alpha=0.8, edgecolor='black')
        
        # Add patterns to bars
        for bar in bars1:
            bar.set_hatch('///')
        for bar in bars2:
            bar.set_hatch('\\\\\\')
        
        ax3.set_title('Patterned Bar Chart', fontsize=14, fontweight='bold', color='#2C3E50')
        ax3.set_xlabel('Months', fontsize=12, color='#34495E')
        ax3.set_ylabel('Values', fontsize=12, color='#34495E')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(self.data['categories'])
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Custom styled scatter plot with color mapping
        ax4 = self.figure.add_subplot(gs[1, 1])
        
        # Create color mapping based on y values
        colors = plt.cm.viridis((self.data['y1'] - self.data['y1'].min()) / 
                               (self.data['y1'].max() - self.data['y1'].min()))
        
        scatter = ax4.scatter(self.data['x'], self.data['y1'], c=colors, s=50, alpha=0.7, 
                            edgecolors='black', linewidth=0.5)
        
        ax4.set_title('Color-Mapped Scatter Plot', fontsize=14, fontweight='bold', color='#2C3E50')
        ax4.set_xlabel('X Axis', fontsize=12, color='#34495E')
        ax4.set_ylabel('Y Axis', fontsize=12, color='#34495E')
        ax4.grid(True, alpha=0.3)
        
        # Add colorbar
        self.figure.colorbar(scatter, ax=ax4, shrink=0.8)
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add navigation toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
    
    def refresh_data(self):
        """Refresh custom data"""
        self.data = self.generate_custom_data()
        self.create_chart()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class AdvancedVisualizationDemo:
    """Demo application showcasing advanced visualization features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Visualization Demo")
        self.root.geometry("1600x1000")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Advanced Visualization Features",
            font=("Arial", 18, "bold"),
            fg="#2C3E50",
            bg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="• Multi-subplot dashboard with various chart types\n• Statistical charts with advanced analysis\n• Custom styled charts with professional appearance\n• Use refresh buttons to generate new data\n• Export charts as high-resolution PNG files",
            font=("Arial", 10),
            fg="#7F8C8D",
            bg="#ECF0F1",
            justify="left"
        )
        instructions.pack(pady=10)
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Tab 1: Multi-subplot Dashboard
        tab1 = tk.Frame(self.notebook, bg="#ECF0F1")
        self.notebook.add(tab1, text="Multi-Subplot Dashboard")
        
        self.multi_dashboard = MultiSubplotDashboard(tab1)
        self.multi_dashboard.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 2: Statistical Charts
        tab2 = tk.Frame(self.notebook, bg="#ECF0F1")
        self.notebook.add(tab2, text="Statistical Charts")
        
        self.statistical_charts = StatisticalChartsWidget(tab2)
        self.statistical_charts.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 3: Custom Styled Charts
        tab3 = tk.Frame(self.notebook, bg="#ECF0F1")
        self.notebook.add(tab3, text="Custom Styled Charts")
        
        self.custom_charts = CustomStyledCharts(tab3)
        self.custom_charts.pack(fill="both", expand=True, padx=10, pady=10)


def main():
    """Main application entry point"""
    # Set Matplotlib style
    plt.style.use('default')
    
    # Create the main window
    root = tk.Tk()
    
    # Create the advanced visualization demo
    demo = AdvancedVisualizationDemo(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

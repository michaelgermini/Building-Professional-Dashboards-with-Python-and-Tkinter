# Data Visualization Best Practices in Tkinter

## Table of Contents
1. [Chart Design Principles](#chart-design-principles)
2. [Performance Optimization](#performance-optimization)
3. [User Experience Guidelines](#user-experience-guidelines)
4. [Code Organization](#code-organization)
5. [Common Pitfalls and Solutions](#common-pitfalls-and-solutions)
6. [Advanced Techniques](#advanced-techniques)

---

## Chart Design Principles

### 1. Choose the Right Chart Type

**Line Charts**
- Use for time series data and trends
- Show continuous data over time
- Good for comparing multiple series

```python
# Good: Time series data
dates = pd.date_range('2024-01-01', periods=100, freq='D')
sales = np.cumsum(np.random.randn(100) * 10 + 50)
ax.plot(dates, sales, 'b-', linewidth=2, label='Sales')

# Bad: Categorical data
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]
ax.plot(categories, values)  # Use bar chart instead
```

**Bar Charts**
- Use for categorical data comparison
- Show discrete values
- Good for ranking and comparison

```python
# Good: Categorical comparison
categories = ['Product A', 'Product B', 'Product C']
sales = [100, 150, 120]
ax.bar(categories, sales, color=['#3498DB', '#E74C3C', '#2ECC71'])

# Bad: Time series data
dates = ['Jan', 'Feb', 'Mar']
values = [100, 120, 110]
ax.bar(dates, values)  # Use line chart instead
```

**Pie Charts**
- Use for showing proportions of a whole
- Limit to 5-7 categories maximum
- Ensure values sum to 100%

```python
# Good: Proportion data
labels = ['Red', 'Blue', 'Green']
sizes = [30, 45, 25]  # Sums to 100
ax.pie(sizes, labels=labels, autopct='%1.1f%%')

# Bad: Too many categories
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
sizes = [10] * 10  # Too many slices
```

### 2. Color Selection

**Use Consistent Color Schemes**
```python
# Professional color palette
COLORS = {
    'primary': '#3498DB',    # Blue
    'secondary': '#E74C3C',  # Red
    'success': '#2ECC71',    # Green
    'warning': '#F39C12',    # Orange
    'info': '#9B59B6',       # Purple
    'light': '#ECF0F1',      # Light gray
    'dark': '#2C3E50'        # Dark gray
}

# Apply consistently
ax.plot(x, y1, color=COLORS['primary'], label='Series 1')
ax.plot(x, y2, color=COLORS['secondary'], label='Series 2')
```

**Accessibility Considerations**
```python
# High contrast colors for accessibility
ACCESSIBLE_COLORS = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Gray
    '#bcbd22',  # Olive
    '#17becf'   # Cyan
]
```

### 3. Typography and Labels

**Clear and Readable Text**
```python
# Good typography
ax.set_title('Sales Performance Q1 2024', 
            fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Sales ($)', fontsize=12, fontweight='bold')

# Rotate labels for readability
ax.tick_params(axis='x', rotation=45)

# Add value labels on bars
for bar, value in zip(bars, values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'${value:,}', ha='center', va='bottom', fontweight='bold')
```

---

## Performance Optimization

### 1. Efficient Data Handling

**Use NumPy for Large Datasets**
```python
# Good: Use NumPy arrays
import numpy as np

# Generate large dataset efficiently
x = np.linspace(0, 100, 10000)
y = np.sin(x) + np.random.normal(0, 0.1, 10000)

# Bad: Use Python lists for large data
x = list(range(10000))
y = [math.sin(i) + random.gauss(0, 0.1) for i in x]
```

**Limit Data Points for Real-Time Charts**
```python
class RealTimeChart:
    def __init__(self, max_points=100):
        self.max_points = max_points
        self.data_x = []
        self.data_y = []
    
    def add_data_point(self, x, y):
        self.data_x.append(x)
        self.data_y.append(y)
        
        # Keep only recent points
        if len(self.data_x) > self.max_points:
            self.data_x.pop(0)
            self.data_y.pop(0)
```

### 2. Efficient Chart Updates

**Update Only What's Necessary**
```python
# Good: Update only data, not entire chart
def update_chart(self, new_data):
    self.line.set_data(self.x_data, new_data)
    self.canvas.draw_idle()  # More efficient than draw()

# Bad: Recreate entire chart
def update_chart(self, new_data):
    self.ax.clear()
    self.ax.plot(self.x_data, new_data)
    self.canvas.draw()
```

**Use Blitting for Animation**
```python
# For smooth animations
import matplotlib.animation as animation

def animate(self, frame):
    # Update data
    new_data = self.generate_data()
    self.line.set_data(self.x_data, new_data)
    return self.line,

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=100, 
                            interval=100, blit=True)
```

### 3. Memory Management

**Clean Up Resources**
```python
class ChartWidget(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = None
        self.canvas = None
    
    def destroy(self):
        # Clean up matplotlib resources
        if self.figure:
            plt.close(self.figure)
        super().destroy()
```

---

## User Experience Guidelines

### 1. Responsive Design

**Adapt to Window Resizing**
```python
class ResponsiveChart(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.bind('<Configure>', self.on_resize)
    
    def on_resize(self, event):
        # Update chart size based on window size
        width = event.width - 20  # Account for padding
        height = event.height - 20
        
        if width > 100 and height > 100:  # Minimum size
            self.figure.set_size_inches(width/100, height/100)
            self.canvas.draw()
```

**Use Grid Weights for Flexible Layout**
```python
# Configure grid weights for responsive layout
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Charts will expand with window
chart1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
chart2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
```

### 2. Interactive Features

**Add Hover Effects**
```python
def on_mouse_move(self, event):
    if event.inaxes:
        # Show tooltip with data point info
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            self.show_tooltip(f"({x:.2f}, {y:.2f})")

def show_tooltip(self, text):
    # Create or update tooltip
    if hasattr(self, 'tooltip'):
        self.tooltip.destroy()
    
    self.tooltip = tk.Toplevel(self)
    self.tooltip.wm_overrideredirect(True)
    self.tooltip.wm_geometry(f"+{self.winfo_pointerx()}+{self.winfo_pointery()}")
    
    label = tk.Label(self.tooltip, text=text, bg="yellow", relief="solid")
    label.pack()
```

**Keyboard Shortcuts**
```python
def bind_shortcuts(self):
    self.root.bind('<Control-r>', lambda e: self.refresh_data())
    self.root.bind('<Control-s>', lambda e: self.save_chart())
    self.root.bind('<Control-z>', lambda e: self.zoom_reset())
```

### 3. Loading States

**Show Progress for Long Operations**
```python
def load_data(self):
    # Show loading indicator
    self.show_loading("Loading data...")
    
    # Run in background thread
    thread = threading.Thread(target=self._load_data_thread)
    thread.start()

def _load_data_thread(self):
    # Perform data loading
    data = self.fetch_large_dataset()
    
    # Update UI in main thread
    self.after(0, self._update_chart, data)
    self.after(0, self.hide_loading)

def show_loading(self, message):
    self.loading_label = tk.Label(self, text=message, bg="yellow")
    self.loading_label.pack()
```

---

## Code Organization

### 1. Modular Chart Classes

**Base Chart Class**
```python
class BaseChart(tk.Frame):
    """Base class for all chart widgets"""
    
    def __init__(self, parent, title="Chart", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create the chart interface"""
        # Title
        title_label = tk.Label(self, text=self.title, font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # Chart will be created by subclasses
        self.create_chart()
    
    def create_chart(self):
        """Create the chart - to be implemented by subclasses"""
        raise NotImplementedError
    
    def refresh_data(self):
        """Refresh chart data - to be implemented by subclasses"""
        pass
    
    def export_chart(self):
        """Export chart to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.figure.savefig(filename, dpi=300, bbox_inches='tight')
```

**Specific Chart Implementations**
```python
class LineChart(BaseChart):
    def create_chart(self):
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create line chart
        self.line, = self.ax.plot([], [], 'b-', linewidth=2)
        self.ax.set_title("Line Chart")
        self.ax.grid(True, alpha=0.3)
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

class BarChart(BaseChart):
    def create_chart(self):
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        
        # Create bar chart
        self.bars = self.ax.bar([], [], color='#3498DB')
        self.ax.set_title("Bar Chart")
        self.ax.grid(True, alpha=0.3, axis='y')
        
        # Create canvas and toolbar
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
```

### 2. Data Management

**Separate Data Logic**
```python
class DataManager:
    """Manages data for charts"""
    
    def __init__(self):
        self.data = {}
        self.observers = []
    
    def add_observer(self, observer):
        """Add chart as observer"""
        self.observers.append(observer)
    
    def notify_observers(self):
        """Notify all charts of data changes"""
        for observer in self.observers:
            observer.update_data(self.data)
    
    def update_data(self, new_data):
        """Update data and notify observers"""
        self.data.update(new_data)
        self.notify_observers()

class ChartWithData(BaseChart):
    def __init__(self, parent, data_manager, **kwargs):
        self.data_manager = data_manager
        super().__init__(parent, **kwargs)
        self.data_manager.add_observer(self)
    
    def update_data(self, data):
        """Update chart with new data"""
        # Update chart based on data
        pass
```

### 3. Configuration Management

**Chart Configuration**
```python
class ChartConfig:
    """Configuration for chart appearance and behavior"""
    
    def __init__(self):
        self.colors = {
            'primary': '#3498DB',
            'secondary': '#E74C3C',
            'success': '#2ECC71',
            'warning': '#F39C12'
        }
        self.fonts = {
            'title': ('Arial', 14, 'bold'),
            'label': ('Arial', 12, 'bold'),
            'tick': ('Arial', 10)
        }
        self.grid_alpha = 0.3
        self.figure_dpi = 100
        self.export_dpi = 300

class ConfigurableChart(BaseChart):
    def __init__(self, parent, config=None, **kwargs):
        self.config = config or ChartConfig()
        super().__init__(parent, **kwargs)
    
    def apply_config(self):
        """Apply configuration to chart"""
        self.figure.set_dpi(self.config.figure_dpi)
        self.ax.grid(True, alpha=self.config.grid_alpha)
        # Apply other configuration settings
```

---

## Common Pitfalls and Solutions

### 1. Memory Leaks

**Problem**: Charts not properly cleaned up
```python
# Bad: Charts accumulate in memory
def create_chart(self):
    self.figure = Figure()
    # ... chart creation
    # Old figures not cleaned up

# Good: Proper cleanup
def create_chart(self):
    if self.figure:
        plt.close(self.figure)  # Clean up old figure
    self.figure = Figure()
    # ... chart creation
```

### 2. Threading Issues

**Problem**: Updating charts from background threads
```python
# Bad: Direct update from thread
def update_from_thread(self):
    self.line.set_data(new_x, new_y)  # Thread unsafe

# Good: Use after() method
def update_from_thread(self):
    self.after(0, self.safe_update, new_x, new_y)

def safe_update(self, x, y):
    self.line.set_data(x, y)
    self.canvas.draw()
```

### 3. Performance Issues

**Problem**: Redrawing entire chart for small updates
```python
# Bad: Redraw everything
def update_chart(self):
    self.ax.clear()
    self.ax.plot(self.data)
    self.canvas.draw()

# Good: Update only data
def update_chart(self):
    self.line.set_data(self.x_data, self.y_data)
    self.canvas.draw_idle()  # More efficient
```

### 4. Layout Issues

**Problem**: Charts not resizing properly
```python
# Bad: Fixed size
chart_frame = tk.Frame(root, width=400, height=300)

# Good: Responsive layout
chart_frame = tk.Frame(root)
chart_frame.grid(row=0, column=0, sticky="nsew")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
```

---

## Advanced Techniques

### 1. Custom Chart Types

**Creating Custom Widgets**
```python
class GaugeChart(tk.Canvas):
    """Custom gauge widget"""
    
    def __init__(self, parent, title="Gauge", min_val=0, max_val=100, **kwargs):
        super().__init__(parent, width=200, height=200, **kwargs)
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = min_val
        self.create_gauge()
    
    def create_gauge(self):
        """Draw the gauge"""
        center_x, center_y = 100, 100
        radius = 80
        
        # Draw gauge background
        self.create_arc(center_x-radius, center_y-radius,
                       center_x+radius, center_y+radius,
                       start=180, extent=180, fill="#E8E8E8")
        
        # Draw value arc
        self.value_arc = self.create_arc(center_x-radius, center_y-radius,
                                       center_x+radius, center_y+radius,
                                       start=180, extent=0, fill="#3498DB")
        
        # Draw center circle
        self.create_oval(center_x-10, center_y-10,
                        center_x+10, center_y+10, fill="white")
        
        # Add title
        self.create_text(center_x, center_y+radius+20,
                        text=self.title, font=("Arial", 12, "bold"))
    
    def update_value(self, new_value):
        """Update gauge value"""
        self.current_val = max(self.min_val, min(self.max_val, new_value))
        percentage = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        angle = percentage * 180
        
        # Update value arc
        self.coords(self.value_arc, 20, 20, 180, 180)
        self.itemconfig(self.value_arc, extent=angle)
```

### 2. Real-Time Data Streaming

**Efficient Real-Time Updates**
```python
class RealTimeChartManager:
    """Manages real-time chart updates"""
    
    def __init__(self, chart, update_interval=1000):
        self.chart = chart
        self.update_interval = update_interval
        self.is_running = False
        self.data_buffer = []
        self.max_buffer_size = 100
    
    def start(self):
        """Start real-time updates"""
        self.is_running = True
        self.update_chart()
    
    def stop(self):
        """Stop real-time updates"""
        self.is_running = False
    
    def update_chart(self):
        """Update chart with new data"""
        if self.is_running:
            # Generate new data point
            new_data = self.generate_data_point()
            self.data_buffer.append(new_data)
            
            # Keep buffer size manageable
            if len(self.data_buffer) > self.max_buffer_size:
                self.data_buffer.pop(0)
            
            # Update chart
            self.chart.update_data(self.data_buffer)
            
            # Schedule next update
            self.chart.after(self.update_interval, self.update_chart)
    
    def generate_data_point(self):
        """Generate a new data point"""
        # Implement your data generation logic
        return random.random()
```

### 3. Advanced Styling

**Custom Themes**
```python
class ChartTheme:
    """Custom chart theme"""
    
    def __init__(self, name="default"):
        self.name = name
        self.setup_theme()
    
    def setup_theme(self):
        """Setup matplotlib theme"""
        if self.name == "dark":
            plt.style.use('dark_background')
            self.colors = {
                'background': '#2C3E50',
                'text': '#ECF0F1',
                'grid': '#34495E',
                'primary': '#3498DB',
                'secondary': '#E74C3C'
            }
        elif self.name == "light":
            plt.style.use('default')
            self.colors = {
                'background': '#FFFFFF',
                'text': '#2C3E50',
                'grid': '#BDC3C7',
                'primary': '#3498DB',
                'secondary': '#E74C3C'
            }
    
    def apply_to_chart(self, ax):
        """Apply theme to chart"""
        ax.set_facecolor(self.colors['background'])
        ax.tick_params(colors=self.colors['text'])
        ax.xaxis.label.set_color(self.colors['text'])
        ax.yaxis.label.set_color(self.colors['text'])
        ax.title.set_color(self.colors['text'])
        ax.grid(True, alpha=0.3, color=self.colors['grid'])
```

---

## Summary

Following these best practices will help you create:

1. **Professional-looking charts** with consistent design
2. **High-performance applications** that handle large datasets efficiently
3. **User-friendly interfaces** with responsive design and interactive features
4. **Maintainable code** with proper organization and modularity
5. **Robust applications** that handle errors gracefully and manage resources properly

Remember to:
- Choose appropriate chart types for your data
- Use consistent colors and typography
- Optimize for performance with large datasets
- Provide responsive and interactive user experiences
- Organize code into modular, reusable components
- Handle common pitfalls like memory leaks and threading issues
- Implement advanced features like custom widgets and real-time updates

These guidelines will help you build production-ready data visualization applications with Tkinter and Matplotlib.

# Chapter 8: Real-Time Dashboards - Exercises

## Exercise 1: Real-Time Data Stream Simulator

**Objective**: Create a real-time data stream simulator that generates and displays live data.

**Requirements**:
- Simulate multiple data streams (temperature, humidity, pressure)
- Display real-time charts with configurable update intervals
- Implement data buffering to handle high-frequency updates
- Add threshold monitoring with alerts

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk
import random
import time
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DataStreamSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Data Stream Simulator")
        self.root.geometry("800x600")
        
        # Data storage
        self.temperature_data = deque(maxlen=100)
        self.humidity_data = deque(maxlen=100)
        self.pressure_data = deque(maxlen=100)
        
        # Thresholds
        self.temp_threshold = 25.0
        self.humidity_threshold = 60.0
        
        # Initialize data
        self.initialize_data()
        
        # Create interface
        self.create_widgets()
        
        # Start simulation
        self.running = True
        self.start_simulation()
    
    def initialize_data(self):
        """Initialize data with random values"""
        # TODO: Initialize data structures with random values
        pass
    
    def create_widgets(self):
        """Create the user interface"""
        # TODO: Create widgets for data display and controls
        pass
    
    def start_simulation(self):
        """Start the data simulation"""
        # TODO: Implement data generation and display updates
        pass
    
    def generate_data(self):
        """Generate new data points"""
        # TODO: Generate realistic sensor data with some randomness
        pass
    
    def update_charts(self):
        """Update all charts with new data"""
        # TODO: Update matplotlib charts with new data
        pass
    
    def check_thresholds(self):
        """Check if data exceeds thresholds and show alerts"""
        # TODO: Implement threshold monitoring and alerts
        pass

def main():
    root = tk.Tk()
    app = DataStreamSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Real-time charts updating with simulated sensor data
- Configurable update intervals (100ms to 5 seconds)
- Threshold monitoring with visual alerts
- Smooth data visualization with proper buffering
- Professional dashboard layout with multiple data streams

## Exercise 2: Performance Monitoring Dashboard

**Objective**: Build a comprehensive performance monitoring dashboard for a web application.

**Requirements**:
- Monitor response times, request rates, and error rates
- Display real-time performance metrics
- Implement alerting for performance degradation
- Create historical trend analysis
- Add performance optimization recommendations

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PerformanceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Performance Monitoring Dashboard")
        self.root.geometry("1000x700")
        
        # Performance data
        self.response_times = deque(maxlen=200)
        self.request_rates = deque(maxlen=200)
        self.error_rates = deque(maxlen=200)
        self.cpu_usage = deque(maxlen=200)
        self.memory_usage = deque(maxlen=200)
        
        # Alert thresholds
        self.response_time_threshold = 1000  # ms
        self.error_rate_threshold = 5.0  # %
        self.cpu_threshold = 80.0  # %
        
        # Initialize data
        self.initialize_data()
        
        # Create interface
        self.create_widgets()
        
        # Start monitoring
        self.running = True
        self.start_monitoring()
    
    def initialize_data(self):
        """Initialize performance data"""
        # TODO: Initialize data structures with baseline values
        pass
    
    def create_widgets(self):
        """Create the monitoring interface"""
        # TODO: Create tabs for different performance metrics
        pass
    
    def create_overview_tab(self):
        """Create overview tab with key metrics"""
        # TODO: Display key performance indicators
        pass
    
    def create_response_time_tab(self):
        """Create response time monitoring tab"""
        # TODO: Show response time trends and alerts
        pass
    
    def create_error_monitoring_tab(self):
        """Create error rate monitoring tab"""
        # TODO: Monitor and display error rates
        pass
    
    def start_monitoring(self):
        """Start the performance monitoring"""
        # TODO: Implement real-time performance monitoring
        pass
    
    def simulate_performance_data(self):
        """Simulate performance metrics"""
        # TODO: Generate realistic performance data
        pass
    
    def check_performance_alerts(self):
        """Check for performance issues and show alerts"""
        # TODO: Implement alerting system
        pass
    
    def generate_recommendations(self):
        """Generate performance optimization recommendations"""
        # TODO: Analyze data and provide recommendations
        pass

def main():
    root = tk.Tk()
    app = PerformanceMonitor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Real-time performance metrics display
- Multiple monitoring tabs (overview, response times, errors, resources)
- Alert system for performance degradation
- Historical trend analysis with charts
- Performance optimization recommendations
- Professional dashboard with status indicators

## Exercise 3: IoT Device Management Dashboard

**Objective**: Create a comprehensive IoT device management dashboard with real-time monitoring.

**Requirements**:
- Monitor multiple IoT devices simultaneously
- Display device status, sensor data, and connectivity
- Implement device control and configuration
- Add data logging and export functionality
- Create device health monitoring and alerts

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
import json
from datetime import datetime
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class IoTDevice:
    def __init__(self, device_id, device_type, location):
        self.device_id = device_id
        self.device_type = device_type
        self.location = location
        self.status = "online"
        self.last_seen = datetime.now()
        self.sensor_data = {}
        self.connected = True

class IoTDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("IoT Device Management Dashboard")
        self.root.geometry("1200x800")
        
        # Device management
        self.devices = {}
        self.device_data = {}
        
        # Initialize sample devices
        self.initialize_devices()
        
        # Create interface
        self.create_widgets()
        
        # Start monitoring
        self.running = True
        self.start_monitoring()
    
    def initialize_devices(self):
        """Initialize sample IoT devices"""
        # TODO: Create sample devices with different types
        pass
    
    def create_widgets(self):
        """Create the main interface"""
        # TODO: Create device management interface
        pass
    
    def create_device_overview_tab(self):
        """Create device overview tab"""
        # TODO: Show all devices with status and basic info
        pass
    
    def create_device_detail_tab(self):
        """Create detailed device monitoring tab"""
        # TODO: Show detailed sensor data and device control
        pass
    
    def create_device_management_tab(self):
        """Create device management and configuration tab"""
        # TODO: Add/remove devices, configure settings
        pass
    
    def start_monitoring(self):
        """Start monitoring all IoT devices"""
        # TODO: Implement device monitoring loop
        pass
    
    def update_device_data(self):
        """Update data for all devices"""
        # TODO: Simulate device data updates
        pass
    
    def check_device_health(self):
        """Check device health and connectivity"""
        # TODO: Monitor device status and connectivity
        pass
    
    def export_device_data(self):
        """Export device data to file"""
        # TODO: Implement data export functionality
        pass
    
    def add_device(self, device_id, device_type, location):
        """Add a new IoT device"""
        # TODO: Implement device addition
        pass
    
    def remove_device(self, device_id):
        """Remove an IoT device"""
        # TODO: Implement device removal
        pass
    
    def configure_device(self, device_id, settings):
        """Configure device settings"""
        # TODO: Implement device configuration
        pass

def main():
    root = tk.Tk()
    app = IoTDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Multi-device monitoring with status indicators
- Real-time sensor data visualization
- Device control and configuration interface
- Data logging and export capabilities
- Device health monitoring with alerts
- Professional IoT management interface

## Bonus Challenge: Advanced Real-Time Analytics Dashboard

**Objective**: Create an advanced analytics dashboard that processes and visualizes real-time business data.

**Requirements**:
- Real-time data processing and aggregation
- Advanced visualizations (heatmaps, 3D charts, network graphs)
- Machine learning integration for trend prediction
- Multi-user support with role-based access
- Advanced alerting and notification system
- Data export and reporting capabilities

**Advanced Features**:
- Real-time data streaming from multiple sources
- Advanced analytics and predictive modeling
- Interactive visualizations with drill-down capabilities
- Automated report generation
- Integration with external APIs and databases
- Performance optimization for large datasets

## Solutions

### Exercise 1 Solution
```python
# Data Stream Simulator Implementation
def initialize_data(self):
    """Initialize data with random values"""
    for _ in range(100):
        self.temperature_data.append(random.uniform(20, 30))
        self.humidity_data.append(random.uniform(40, 80))
        self.pressure_data.append(random.uniform(1000, 1020))

def generate_data(self):
    """Generate new data points with realistic patterns"""
    # Temperature with some trend
    last_temp = self.temperature_data[-1] if self.temperature_data else 25
    new_temp = last_temp + random.uniform(-0.5, 0.5)
    new_temp = max(15, min(35, new_temp))  # Clamp to realistic range
    
    # Humidity (inverse relationship with temperature)
    new_humidity = 80 - (new_temp - 15) * 2 + random.uniform(-5, 5)
    new_humidity = max(20, min(95, new_humidity))
    
    # Pressure (slow changes)
    last_pressure = self.pressure_data[-1] if self.pressure_data else 1013
    new_pressure = last_pressure + random.uniform(-0.1, 0.1)
    new_pressure = max(990, min(1030, new_pressure))
    
    return new_temp, new_humidity, new_pressure

def check_thresholds(self):
    """Check if data exceeds thresholds and show alerts"""
    current_temp = self.temperature_data[-1]
    current_humidity = self.humidity_data[-1]
    
    alerts = []
    if current_temp > self.temp_threshold:
        alerts.append(f"Temperature high: {current_temp:.1f}°C")
    
    if current_humidity > self.humidity_threshold:
        alerts.append(f"Humidity high: {current_humidity:.1f}%")
    
    if alerts:
        # Show alert in status bar or popup
        self.show_alerts(alerts)
```

### Exercise 2 Solution
```python
# Performance Monitor Implementation
def simulate_performance_data(self):
    """Simulate realistic performance metrics"""
    # Response time (ms) - varies based on load
    base_response_time = 200
    load_factor = random.uniform(0.5, 2.0)
    new_response_time = base_response_time * load_factor + random.uniform(-50, 50)
    new_response_time = max(50, new_response_time)
    
    # Request rate (requests per second)
    base_rate = 100
    new_rate = base_rate + random.uniform(-20, 20)
    new_rate = max(0, new_rate)
    
    # Error rate (%)
    base_error_rate = 1.0
    if new_response_time > self.response_time_threshold:
        new_error_rate = base_error_rate + random.uniform(0, 5)
    else:
        new_error_rate = base_error_rate + random.uniform(-0.5, 0.5)
    new_error_rate = max(0, min(10, new_error_rate))
    
    # CPU and memory usage
    new_cpu = 30 + (new_rate / 200) * 50 + random.uniform(-10, 10)
    new_cpu = max(0, min(100, new_cpu))
    
    new_memory = 40 + (new_rate / 200) * 30 + random.uniform(-5, 5)
    new_memory = max(0, min(100, new_memory))
    
    return new_response_time, new_rate, new_error_rate, new_cpu, new_memory

def check_performance_alerts(self):
    """Check for performance issues and show alerts"""
    current_response_time = self.response_times[-1]
    current_error_rate = self.error_rates[-1]
    current_cpu = self.cpu_usage[-1]
    
    alerts = []
    
    if current_response_time > self.response_time_threshold:
        alerts.append(f"High response time: {current_response_time:.0f}ms")
    
    if current_error_rate > self.error_rate_threshold:
        alerts.append(f"High error rate: {current_error_rate:.1f}%")
    
    if current_cpu > self.cpu_threshold:
        alerts.append(f"High CPU usage: {current_cpu:.1f}%")
    
    if alerts:
        self.show_performance_alerts(alerts)
```

### Exercise 3 Solution
```python
# IoT Dashboard Implementation
def initialize_devices(self):
    """Initialize sample IoT devices"""
    device_types = ["Temperature Sensor", "Humidity Sensor", "Motion Detector", "Smart Light", "Security Camera"]
    locations = ["Living Room", "Kitchen", "Bedroom", "Office", "Garage"]
    
    for i in range(5):
        device_id = f"DEV_{i+1:03d}"
        device_type = random.choice(device_types)
        location = random.choice(locations)
        
        device = IoTDevice(device_id, device_type, location)
        self.devices[device_id] = device
        
        # Initialize sensor data
        self.device_data[device_id] = {
            'temperature': deque(maxlen=100),
            'humidity': deque(maxlen=100),
            'motion': deque(maxlen=100),
            'light_level': deque(maxlen=100),
            'battery': deque(maxlen=100)
        }
        
        # Add initial data
        for _ in range(100):
            self.device_data[device_id]['temperature'].append(random.uniform(18, 28))
            self.device_data[device_id]['humidity'].append(random.uniform(30, 70))
            self.device_data[device_id]['motion'].append(random.choice([0, 1]))
            self.device_data[device_id]['light_level'].append(random.uniform(0, 100))
            self.device_data[device_id]['battery'].append(random.uniform(20, 100))

def update_device_data(self):
    """Update data for all IoT devices"""
    for device_id, device in self.devices.items():
        if device.connected:
            # Simulate device data updates
            if device.device_type == "Temperature Sensor":
                last_temp = self.device_data[device_id]['temperature'][-1]
                new_temp = last_temp + random.uniform(-0.5, 0.5)
                self.device_data[device_id]['temperature'].append(new_temp)
            
            elif device.device_type == "Humidity Sensor":
                last_humidity = self.device_data[device_id]['humidity'][-1]
                new_humidity = last_humidity + random.uniform(-2, 2)
                self.device_data[device_id]['humidity'].append(new_humidity)
            
            elif device.device_type == "Motion Detector":
                # Motion is binary (0 or 1)
                motion = random.choice([0, 0, 0, 0, 1])  # 20% chance of motion
                self.device_data[device_id]['motion'].append(motion)
            
            # Update battery level (slowly decreasing)
            last_battery = self.device_data[device_id]['battery'][-1]
            new_battery = last_battery - random.uniform(0, 0.1)
            self.device_data[device_id]['battery'].append(max(0, new_battery))
            
            # Update last seen time
            device.last_seen = datetime.now()
```

## Learning Objectives

After completing these exercises, you should be able to:

1. **Real-Time Data Processing**: Handle high-frequency data streams efficiently
2. **Performance Optimization**: Optimize real-time applications for smooth operation
3. **Data Visualization**: Create dynamic charts and visualizations
4. **Alert Systems**: Implement threshold monitoring and alerting
5. **Multi-Device Management**: Monitor and control multiple devices simultaneously
6. **Data Buffering**: Manage data queues and prevent memory issues
7. **Error Handling**: Implement robust error handling for real-time systems
8. **User Interface Design**: Create professional real-time dashboards

## Next Steps

- Implement real data source integration (APIs, databases, sensors)
- Add machine learning for predictive analytics
- Create distributed monitoring systems
- Implement advanced alerting (email, SMS, webhooks)
- Add user authentication and role-based access
- Optimize for high-frequency data (1000+ updates per second)
- Implement data persistence and historical analysis

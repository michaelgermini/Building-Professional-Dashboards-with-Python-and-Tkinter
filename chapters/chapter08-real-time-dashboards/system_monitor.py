"""
System Monitor Dashboard - Chapter 8 Example
Real-time system resource monitoring using psutil
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import threading
import time
from collections import deque
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor Dashboard")
        self.root.geometry("1200x800")
        
        # Data storage for charts
        self.cpu_history = deque(maxlen=100)
        self.memory_history = deque(maxlen=100)
        self.disk_history = deque(maxlen=100)
        self.network_history = deque(maxlen=100)
        
        # Initialize data
        self.initialize_data()
        
        # Create interface
        self.create_widgets()
        
        # Start monitoring
        self.running = True
        self.start_monitoring()
    
    def initialize_data(self):
        """Initialize data structures with current values"""
        # Get initial system data
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # Initialize history with current values
        for _ in range(100):
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory.percent)
            self.disk_history.append(disk.percent)
            self.network_history.append(network.bytes_sent + network.bytes_recv)
    
    def create_widgets(self):
        """Create the main interface"""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(self.root, text="System Monitor Dashboard", 
                              font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Create tabs
        self.create_overview_tab()
        self.create_cpu_tab()
        self.create_memory_tab()
        self.create_disk_tab()
        self.create_network_tab()
        self.create_processes_tab()
        
        # Control panel
        self.create_control_panel()
    
    def create_overview_tab(self):
        """Create the overview tab with key metrics"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="Overview")
        
        # Configure grid
        overview_frame.grid_columnconfigure(0, weight=1)
        overview_frame.grid_columnconfigure(1, weight=1)
        overview_frame.grid_rowconfigure(1, weight=1)
        
        # Key metrics frame
        metrics_frame = ttk.Frame(overview_frame)
        metrics_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
        
        # CPU metric
        cpu_frame = ttk.LabelFrame(metrics_frame, text="CPU Usage")
        cpu_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        self.cpu_label = tk.Label(cpu_frame, text="0%", font=("Arial", 24, "bold"), fg="red")
        self.cpu_label.pack(pady=10)
        
        self.cpu_progress = ttk.Progressbar(cpu_frame, length=200, mode='determinate')
        self.cpu_progress.pack(pady=5)
        
        # Memory metric
        memory_frame = ttk.LabelFrame(metrics_frame, text="Memory Usage")
        memory_frame.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        self.memory_label = tk.Label(memory_frame, text="0%", font=("Arial", 24, "bold"), fg="blue")
        self.memory_label.pack(pady=10)
        
        self.memory_progress = ttk.Progressbar(memory_frame, length=200, mode='determinate')
        self.memory_progress.pack(pady=5)
        
        # Disk metric
        disk_frame = ttk.LabelFrame(metrics_frame, text="Disk Usage")
        disk_frame.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        
        self.disk_label = tk.Label(disk_frame, text="0%", font=("Arial", 24, "bold"), fg="green")
        self.disk_label.pack(pady=10)
        
        self.disk_progress = ttk.Progressbar(disk_frame, length=200, mode='determinate')
        self.disk_progress.pack(pady=5)
        
        # Network metric
        network_frame = ttk.LabelFrame(metrics_frame, text="Network Activity")
        network_frame.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
        
        self.network_label = tk.Label(network_frame, text="0 KB/s", font=("Arial", 16, "bold"), fg="purple")
        self.network_label.pack(pady=10)
        
        # Overview chart
        chart_frame = ttk.LabelFrame(overview_frame, text="System Overview")
        chart_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Create matplotlib figure
        self.overview_fig = Figure(figsize=(12, 6), dpi=100)
        self.overview_ax = self.overview_fig.add_subplot(111)
        
        self.overview_canvas = FigureCanvasTkAgg(self.overview_fig, chart_frame)
        self.overview_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_cpu_tab(self):
        """Create the CPU monitoring tab"""
        cpu_frame = ttk.Frame(self.notebook)
        self.notebook.add(cpu_frame, text="CPU")
        
        # CPU details
        details_frame = ttk.LabelFrame(cpu_frame, text="CPU Details")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        # CPU info
        cpu_info = psutil.cpu_count()
        ttk.Label(details_frame, text=f"CPU Cores: {cpu_info}").pack(anchor="w", padx=10, pady=5)
        
        self.cpu_freq_label = ttk.Label(details_frame, text="CPU Frequency: --")
        self.cpu_freq_label.pack(anchor="w", padx=10, pady=5)
        
        self.cpu_temp_label = ttk.Label(details_frame, text="CPU Temperature: --")
        self.cpu_temp_label.pack(anchor="w", padx=10, pady=5)
        
        # CPU chart
        chart_frame = ttk.LabelFrame(cpu_frame, text="CPU Usage Over Time")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.cpu_fig = Figure(figsize=(10, 6), dpi=100)
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, chart_frame)
        self.cpu_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_memory_tab(self):
        """Create the memory monitoring tab"""
        memory_frame = ttk.Frame(self.notebook)
        self.notebook.add(memory_frame, text="Memory")
        
        # Memory details
        details_frame = ttk.LabelFrame(memory_frame, text="Memory Details")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        self.memory_total_label = ttk.Label(details_frame, text="Total Memory: --")
        self.memory_total_label.pack(anchor="w", padx=10, pady=5)
        
        self.memory_used_label = ttk.Label(details_frame, text="Used Memory: --")
        self.memory_used_label.pack(anchor="w", padx=10, pady=5)
        
        self.memory_available_label = ttk.Label(details_frame, text="Available Memory: --")
        self.memory_available_label.pack(anchor="w", padx=10, pady=5)
        
        # Memory chart
        chart_frame = ttk.LabelFrame(memory_frame, text="Memory Usage Over Time")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.memory_fig = Figure(figsize=(10, 6), dpi=100)
        self.memory_ax = self.memory_fig.add_subplot(111)
        
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, chart_frame)
        self.memory_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_disk_tab(self):
        """Create the disk monitoring tab"""
        disk_frame = ttk.Frame(self.notebook)
        self.notebook.add(disk_frame, text="Disk")
        
        # Disk details
        details_frame = ttk.LabelFrame(disk_frame, text="Disk Details")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        self.disk_total_label = ttk.Label(details_frame, text="Total Space: --")
        self.disk_total_label.pack(anchor="w", padx=10, pady=5)
        
        self.disk_used_label = ttk.Label(details_frame, text="Used Space: --")
        self.disk_used_label.pack(anchor="w", padx=10, pady=5)
        
        self.disk_free_label = ttk.Label(details_frame, text="Free Space: --")
        self.disk_free_label.pack(anchor="w", padx=10, pady=5)
        
        # Disk chart
        chart_frame = ttk.LabelFrame(disk_frame, text="Disk Usage Over Time")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.disk_fig = Figure(figsize=(10, 6), dpi=100)
        self.disk_ax = self.disk_fig.add_subplot(111)
        
        self.disk_canvas = FigureCanvasTkAgg(self.disk_fig, chart_frame)
        self.disk_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_network_tab(self):
        """Create the network monitoring tab"""
        network_frame = ttk.Frame(self.notebook)
        self.notebook.add(network_frame, text="Network")
        
        # Network details
        details_frame = ttk.LabelFrame(network_frame, text="Network Details")
        details_frame.pack(fill="x", padx=10, pady=10)
        
        self.network_sent_label = ttk.Label(details_frame, text="Bytes Sent: --")
        self.network_sent_label.pack(anchor="w", padx=10, pady=5)
        
        self.network_recv_label = ttk.Label(details_frame, text="Bytes Received: --")
        self.network_recv_label.pack(anchor="w", padx=10, pady=5)
        
        self.network_packets_label = ttk.Label(details_frame, text="Packets: --")
        self.network_packets_label.pack(anchor="w", padx=10, pady=5)
        
        # Network chart
        chart_frame = ttk.LabelFrame(network_frame, text="Network Activity Over Time")
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.network_fig = Figure(figsize=(10, 6), dpi=100)
        self.network_ax = self.network_fig.add_subplot(111)
        
        self.network_canvas = FigureCanvasTkAgg(self.network_fig, chart_frame)
        self.network_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_processes_tab(self):
        """Create the processes monitoring tab"""
        processes_frame = ttk.Frame(self.notebook)
        self.notebook.add(processes_frame, text="Processes")
        
        # Process list
        list_frame = ttk.LabelFrame(processes_frame, text="Top Processes")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create Treeview
        columns = ("PID", "Name", "CPU %", "Memory %", "Status")
        self.process_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=scrollbar.set)
        
        self.process_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Refresh button
        refresh_btn = ttk.Button(processes_frame, text="Refresh Processes", 
                                command=self.refresh_processes)
        refresh_btn.pack(pady=10)
    
    def create_control_panel(self):
        """Create the control panel"""
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Update interval control
        ttk.Label(control_frame, text="Update Interval (ms):").pack(side="left", padx=10)
        
        self.interval_var = tk.StringVar(value="1000")
        interval_spinbox = ttk.Spinbox(control_frame, from_=500, to=5000, 
                                      increment=500, textvariable=self.interval_var,
                                      width=10)
        interval_spinbox.pack(side="left", padx=5)
        
        # Start/Stop button
        self.toggle_button = ttk.Button(control_frame, text="Stop Monitoring", 
                                       command=self.toggle_monitoring)
        self.toggle_button.pack(side="left", padx=10)
        
        # Status indicator
        self.status_label = ttk.Label(control_frame, text="Status: Running", 
                                     foreground="green")
        self.status_label.pack(side="right", padx=10)
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        self.update_system_data()
    
    def update_system_data(self):
        """Update all system data"""
        if not self.running:
            return
        
        try:
            # Get system data
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            
            # Update history
            self.cpu_history.append(cpu_percent)
            self.memory_history.append(memory.percent)
            self.disk_history.append(disk.percent)
            self.network_history.append(network.bytes_sent + network.bytes_recv)
            
            # Update UI
            self.update_overview_metrics(cpu_percent, memory, disk, network)
            self.update_charts()
            self.update_detailed_info(cpu_percent, memory, disk, network)
            
            # Schedule next update
            interval = int(self.interval_var.get())
            self.root.after(interval, self.update_system_data)
            
        except Exception as e:
            print(f"Error updating system data: {e}")
            # Continue monitoring even if there's an error
            self.root.after(1000, self.update_system_data)
    
    def update_overview_metrics(self, cpu_percent, memory, disk, network):
        """Update overview metrics"""
        # CPU
        self.cpu_label.config(text=f"{cpu_percent:.1f}%")
        self.cpu_progress['value'] = cpu_percent
        
        # Color coding for CPU
        if cpu_percent > 80:
            self.cpu_label.config(fg="red")
        elif cpu_percent > 60:
            self.cpu_label.config(fg="orange")
        else:
            self.cpu_label.config(fg="green")
        
        # Memory
        self.memory_label.config(text=f"{memory.percent:.1f}%")
        self.memory_progress['value'] = memory.percent
        
        # Color coding for memory
        if memory.percent > 80:
            self.memory_label.config(fg="red")
        elif memory.percent > 60:
            self.memory_label.config(fg="orange")
        else:
            self.memory_label.config(fg="blue")
        
        # Disk
        self.disk_label.config(text=f"{disk.percent:.1f}%")
        self.disk_progress['value'] = disk.percent
        
        # Color coding for disk
        if disk.percent > 80:
            self.disk_label.config(fg="red")
        elif disk.percent > 60:
            self.disk_label.config(fg="orange")
        else:
            self.disk_label.config(fg="green")
        
        # Network (calculate rate)
        if len(self.network_history) > 1:
            current = self.network_history[-1]
            previous = self.network_history[-2]
            rate = (current - previous) / (int(self.interval_var.get()) / 1000)
            
            if rate > 1024 * 1024:  # MB/s
                rate_str = f"{rate / (1024 * 1024):.1f} MB/s"
            elif rate > 1024:  # KB/s
                rate_str = f"{rate / 1024:.1f} KB/s"
            else:  # B/s
                rate_str = f"{rate:.0f} B/s"
            
            self.network_label.config(text=rate_str)
    
    def update_charts(self):
        """Update all charts"""
        self.update_overview_chart()
        self.update_cpu_chart()
        self.update_memory_chart()
        self.update_disk_chart()
        self.update_network_chart()
    
    def update_overview_chart(self):
        """Update the overview chart"""
        self.overview_ax.clear()
        
        x = list(range(len(self.cpu_history)))
        
        self.overview_ax.plot(x, list(self.cpu_history), label='CPU %', color='red')
        self.overview_ax.plot(x, list(self.memory_history), label='Memory %', color='blue')
        self.overview_ax.plot(x, list(self.disk_history), label='Disk %', color='green')
        
        self.overview_ax.set_title('System Overview')
        self.overview_ax.set_xlabel('Time')
        self.overview_ax.set_ylabel('Percentage')
        self.overview_ax.legend()
        self.overview_ax.grid(True, alpha=0.3)
        
        self.overview_canvas.draw()
    
    def update_cpu_chart(self):
        """Update the CPU chart"""
        self.cpu_ax.clear()
        
        x = list(range(len(self.cpu_history)))
        self.cpu_ax.plot(x, list(self.cpu_history), color='red', linewidth=2)
        
        self.cpu_ax.set_title('CPU Usage Over Time')
        self.cpu_ax.set_xlabel('Time')
        self.cpu_ax.set_ylabel('CPU %')
        self.cpu_ax.grid(True, alpha=0.3)
        self.cpu_ax.set_ylim(0, 100)
        
        self.cpu_canvas.draw()
    
    def update_memory_chart(self):
        """Update the memory chart"""
        self.memory_ax.clear()
        
        x = list(range(len(self.memory_history)))
        self.memory_ax.plot(x, list(self.memory_history), color='blue', linewidth=2)
        
        self.memory_ax.set_title('Memory Usage Over Time')
        self.memory_ax.set_xlabel('Time')
        self.memory_ax.set_ylabel('Memory %')
        self.memory_ax.grid(True, alpha=0.3)
        self.memory_ax.set_ylim(0, 100)
        
        self.memory_canvas.draw()
    
    def update_disk_chart(self):
        """Update the disk chart"""
        self.disk_ax.clear()
        
        x = list(range(len(self.disk_history)))
        self.disk_ax.plot(x, list(self.disk_history), color='green', linewidth=2)
        
        self.disk_ax.set_title('Disk Usage Over Time')
        self.disk_ax.set_xlabel('Time')
        self.disk_ax.set_ylabel('Disk %')
        self.disk_ax.grid(True, alpha=0.3)
        self.disk_ax.set_ylim(0, 100)
        
        self.disk_canvas.draw()
    
    def update_network_chart(self):
        """Update the network chart"""
        self.network_ax.clear()
        
        x = list(range(len(self.network_history)))
        # Convert to MB for better display
        network_data = [n / (1024 * 1024) for n in self.network_history]
        self.network_ax.plot(x, network_data, color='purple', linewidth=2)
        
        self.network_ax.set_title('Network Activity Over Time')
        self.network_ax.set_xlabel('Time')
        self.network_ax.set_ylabel('Total Bytes (MB)')
        self.network_ax.grid(True, alpha=0.3)
        
        self.network_canvas.draw()
    
    def update_detailed_info(self, cpu_percent, memory, disk, network):
        """Update detailed information displays"""
        # CPU details
        try:
            cpu_freq = psutil.cpu_freq()
            if cpu_freq:
                self.cpu_freq_label.config(text=f"CPU Frequency: {cpu_freq.current:.0f} MHz")
        except:
            self.cpu_freq_label.config(text="CPU Frequency: N/A")
        
        # Memory details
        total_gb = memory.total / (1024**3)
        used_gb = memory.used / (1024**3)
        available_gb = memory.available / (1024**3)
        
        self.memory_total_label.config(text=f"Total Memory: {total_gb:.1f} GB")
        self.memory_used_label.config(text=f"Used Memory: {used_gb:.1f} GB")
        self.memory_available_label.config(text=f"Available Memory: {available_gb:.1f} GB")
        
        # Disk details
        total_gb = disk.total / (1024**3)
        used_gb = disk.used / (1024**3)
        free_gb = disk.free / (1024**3)
        
        self.disk_total_label.config(text=f"Total Space: {total_gb:.1f} GB")
        self.disk_used_label.config(text=f"Used Space: {used_gb:.1f} GB")
        self.disk_free_label.config(text=f"Free Space: {free_gb:.1f} GB")
        
        # Network details
        sent_mb = network.bytes_sent / (1024**2)
        recv_mb = network.bytes_recv / (1024**2)
        
        self.network_sent_label.config(text=f"Bytes Sent: {sent_mb:.1f} MB")
        self.network_recv_label.config(text=f"Bytes Received: {recv_mb:.1f} MB")
        self.network_packets_label.config(text=f"Packets: {network.packets_sent + network.packets_recv}")
    
    def refresh_processes(self):
        """Refresh the process list"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        try:
            # Get top processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and take top 20
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            top_processes = processes[:20]
            
            # Add to treeview
            for proc in top_processes:
                self.process_tree.insert("", "end", values=(
                    proc['pid'],
                    proc['name'][:20],  # Truncate long names
                    f"{proc['cpu_percent']:.1f}",
                    f"{proc['memory_percent']:.1f}",
                    proc['status']
                ))
                
        except Exception as e:
            print(f"Error refreshing processes: {e}")
    
    def toggle_monitoring(self):
        """Toggle monitoring on/off"""
        self.running = not self.running
        
        if self.running:
            self.toggle_button.config(text="Stop Monitoring")
            self.status_label.config(text="Status: Running", foreground="green")
            self.start_monitoring()
        else:
            self.toggle_button.config(text="Start Monitoring")
            self.status_label.config(text="Status: Stopped", foreground="red")

def main():
    root = tk.Tk()
    app = SystemMonitor(root)
    root.mainloop()

if __name__ == "__main__":
    main()

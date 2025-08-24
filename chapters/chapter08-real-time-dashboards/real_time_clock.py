"""
Real-Time Clock - Chapter 8 Example
Demonstrates basic real-time updates using Tkinter's after() method
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time

class RealTimeClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Clock Dashboard")
        self.root.geometry("600x400")
        
        # Configure grid weights for responsive layout
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Create main interface
        self.create_widgets()
        
        # Start real-time updates
        self.update_clock()
        self.update_date()
        self.update_timestamp()
    
    def create_widgets(self):
        """Create the main interface widgets"""
        # Title
        title_label = tk.Label(self.root, text="Real-Time Clock Dashboard", 
                              font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Main content frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Digital clock section
        clock_frame = ttk.LabelFrame(main_frame, text="Digital Clock")
        clock_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.time_label = tk.Label(clock_frame, font=("Arial", 36, "bold"), 
                                  fg="blue")
        self.time_label.pack(pady=20)
        
        self.date_label = tk.Label(clock_frame, font=("Arial", 16), 
                                  fg="darkgreen")
        self.date_label.pack(pady=10)
        
        # Timestamp section
        timestamp_frame = ttk.LabelFrame(main_frame, text="Unix Timestamp")
        timestamp_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.timestamp_label = tk.Label(timestamp_frame, font=("Arial", 14), 
                                       fg="purple")
        self.timestamp_label.pack(pady=20)
        
        self.milliseconds_label = tk.Label(timestamp_frame, font=("Arial", 12), 
                                          fg="gray")
        self.milliseconds_label.pack(pady=10)
        
        # Control panel
        control_frame = ttk.LabelFrame(self.root, text="Controls")
        control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Update interval control
        ttk.Label(control_frame, text="Update Interval (ms):").pack(side="left", padx=10)
        
        self.interval_var = tk.StringVar(value="1000")
        interval_spinbox = ttk.Spinbox(control_frame, from_=100, to=5000, 
                                      increment=100, textvariable=self.interval_var,
                                      width=10)
        interval_spinbox.pack(side="left", padx=5)
        
        # Start/Stop button
        self.running = True
        self.toggle_button = ttk.Button(control_frame, text="Stop Updates", 
                                       command=self.toggle_updates)
        self.toggle_button.pack(side="left", padx=10)
        
        # Status indicator
        self.status_label = ttk.Label(control_frame, text="Status: Running", 
                                     foreground="green")
        self.status_label.pack(side="right", padx=10)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.root, text="Statistics")
        stats_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Update counter
        self.update_count = 0
        self.update_count_label = ttk.Label(stats_frame, text="Updates: 0")
        self.update_count_label.pack(side="left", padx=10)
        
        # Last update time
        self.last_update_label = ttk.Label(stats_frame, text="Last Update: Never")
        self.last_update_label.pack(side="right", padx=10)
    
    def update_clock(self):
        """Update the digital clock display"""
        if not self.running:
            return
        
        try:
            # Get current time
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            # Update the time label
            self.time_label.config(text=current_time)
            
            # Update statistics
            self.update_count += 1
            self.update_count_label.config(text=f"Updates: {self.update_count}")
            
            # Get update interval
            interval = int(self.interval_var.get())
            
            # Schedule next update
            self.root.after(interval, self.update_clock)
            
        except Exception as e:
            print(f"Error updating clock: {e}")
            # Continue updates even if there's an error
            self.root.after(1000, self.update_clock)
    
    def update_date(self):
        """Update the date display"""
        if not self.running:
            return
        
        try:
            now = datetime.now()
            current_date = now.strftime("%A, %B %d, %Y")
            self.date_label.config(text=current_date)
            
            # Update less frequently (every 5 seconds)
            self.root.after(5000, self.update_date)
            
        except Exception as e:
            print(f"Error updating date: {e}")
            self.root.after(5000, self.update_date)
    
    def update_timestamp(self):
        """Update the Unix timestamp display"""
        if not self.running:
            return
        
        try:
            # Get current timestamp
            timestamp = int(time.time())
            milliseconds = int(time.time() * 1000) % 1000
            
            self.timestamp_label.config(text=f"{timestamp}")
            self.milliseconds_label.config(text=f"Milliseconds: {milliseconds:03d}")
            
            # Update timestamp more frequently (every 100ms for smooth milliseconds)
            self.root.after(100, self.update_timestamp)
            
        except Exception as e:
            print(f"Error updating timestamp: {e}")
            self.root.after(100, self.update_timestamp)
    
    def toggle_updates(self):
        """Toggle between starting and stopping updates"""
        self.running = not self.running
        
        if self.running:
            self.toggle_button.config(text="Stop Updates")
            self.status_label.config(text="Status: Running", foreground="green")
            
            # Restart updates
            self.update_clock()
            self.update_date()
            self.update_timestamp()
        else:
            self.toggle_button.config(text="Start Updates")
            self.status_label.config(text="Status: Stopped", foreground="red")
    
    def update_last_update_time(self):
        """Update the last update time display"""
        now = datetime.now()
        self.last_update_label.config(text=f"Last Update: {now.strftime('%H:%M:%S')}")

class AdvancedRealTimeClock:
    """Advanced real-time clock with multiple time zones and formats"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Real-Time Clock")
        self.root.geometry("800x600")
        
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        self.start_updates()
    
    def create_widgets(self):
        """Create advanced interface with multiple time displays"""
        # Title
        title_label = tk.Label(self.root, text="Advanced Real-Time Clock", 
                              font=("Arial", 20, "bold"))
        title_label.grid(row=0, column=0, pady=20)
        
        # Main content
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Local time section
        local_frame = ttk.LabelFrame(main_frame, text="Local Time")
        local_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.local_time_label = tk.Label(local_frame, font=("Arial", 24, "bold"), 
                                        fg="blue")
        self.local_time_label.pack(pady=20)
        
        self.local_date_label = tk.Label(local_frame, font=("Arial", 14))
        self.local_date_label.pack(pady=10)
        
        # UTC time section
        utc_frame = ttk.LabelFrame(main_frame, text="UTC Time")
        utc_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.utc_time_label = tk.Label(utc_frame, font=("Arial", 24, "bold"), 
                                      fg="green")
        self.utc_time_label.pack(pady=20)
        
        self.utc_date_label = tk.Label(utc_frame, font=("Arial", 14))
        self.utc_date_label.pack(pady=10)
        
        # Additional information frame
        info_frame = ttk.LabelFrame(main_frame, text="Additional Information")
        info_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Week number and day of year
        self.week_info_label = ttk.Label(info_frame, font=("Arial", 12))
        self.week_info_label.pack(pady=10)
        
        # Time zone information
        self.timezone_label = ttk.Label(info_frame, font=("Arial", 12))
        self.timezone_label.pack(pady=5)
        
        # Control panel
        control_frame = ttk.LabelFrame(self.root, text="Display Options")
        control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # 12/24 hour format toggle
        self.hour_format = tk.StringVar(value="24")
        ttk.Radiobutton(control_frame, text="12-Hour Format", 
                       variable=self.hour_format, value="12").pack(side="left", padx=10)
        ttk.Radiobutton(control_frame, text="24-Hour Format", 
                       variable=self.hour_format, value="24").pack(side="left", padx=10)
        
        # Show seconds toggle
        self.show_seconds = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Show Seconds", 
                       variable=self.show_seconds).pack(side="left", padx=10)
        
        # Update frequency
        ttk.Label(control_frame, text="Update Frequency:").pack(side="left", padx=10)
        self.frequency_var = tk.StringVar(value="1000")
        frequency_combo = ttk.Combobox(control_frame, textvariable=self.frequency_var,
                                      values=["100", "500", "1000", "2000"], 
                                      width=10, state="readonly")
        frequency_combo.pack(side="left", padx=5)
    
    def start_updates(self):
        """Start all update functions"""
        self.update_local_time()
        self.update_utc_time()
        self.update_additional_info()
    
    def update_local_time(self):
        """Update local time display"""
        try:
            now = datetime.now()
            
            # Format time based on user preference
            if self.hour_format.get() == "12":
                time_format = "%I:%M"
                if self.show_seconds.get():
                    time_format += ":%S"
                time_format += " %p"
            else:
                time_format = "%H:%M"
                if self.show_seconds.get():
                    time_format += ":%S"
            
            current_time = now.strftime(time_format)
            current_date = now.strftime("%A, %B %d, %Y")
            
            self.local_time_label.config(text=current_time)
            self.local_date_label.config(text=current_date)
            
            # Schedule next update
            interval = int(self.frequency_var.get())
            self.root.after(interval, self.update_local_time)
            
        except Exception as e:
            print(f"Error updating local time: {e}")
            self.root.after(1000, self.update_local_time)
    
    def update_utc_time(self):
        """Update UTC time display"""
        try:
            from datetime import timezone
            now = datetime.now(timezone.utc)
            
            # Format UTC time
            if self.hour_format.get() == "12":
                time_format = "%I:%M"
                if self.show_seconds.get():
                    time_format += ":%S"
                time_format += " %p UTC"
            else:
                time_format = "%H:%M"
                if self.show_seconds.get():
                    time_format += ":%S"
                time_format += " UTC"
            
            current_time = now.strftime(time_format)
            current_date = now.strftime("%A, %B %d, %Y")
            
            self.utc_time_label.config(text=current_time)
            self.utc_date_label.config(text=current_date)
            
            # Schedule next update
            interval = int(self.frequency_var.get())
            self.root.after(interval, self.update_utc_time)
            
        except Exception as e:
            print(f"Error updating UTC time: {e}")
            self.root.after(1000, self.update_utc_time)
    
    def update_additional_info(self):
        """Update additional time information"""
        try:
            now = datetime.now()
            
            # Week number and day of year
            week_number = now.isocalendar()[1]
            day_of_year = now.timetuple().tm_yday
            
            week_info = f"Week {week_number}, Day {day_of_year} of {now.year}"
            self.week_info_label.config(text=week_info)
            
            # Time zone information
            import time
            timezone_info = f"Timezone: {time.tzname[time.daylight]}"
            self.timezone_label.config(text=timezone_info)
            
            # Update less frequently (every 5 seconds)
            self.root.after(5000, self.update_additional_info)
            
        except Exception as e:
            print(f"Error updating additional info: {e}")
            self.root.after(5000, self.update_additional_info)

def main():
    root = tk.Tk()
    
    # Create notebook for multiple examples
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Basic clock tab
    basic_frame = ttk.Frame(notebook)
    notebook.add(basic_frame, text="Basic Clock")
    basic_clock = RealTimeClock(basic_frame)
    
    # Advanced clock tab
    advanced_frame = ttk.Frame(notebook)
    notebook.add(advanced_frame, text="Advanced Clock")
    advanced_clock = AdvancedRealTimeClock(advanced_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main()

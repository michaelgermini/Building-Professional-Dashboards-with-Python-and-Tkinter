"""
Professional Dashboard - Chapter 10 Final Project
Complete enterprise-level dashboard application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import hashlib
import threading
import time
from datetime import datetime, timedelta
import random
import os
from collections import defaultdict

# Import custom modules (these would be separate files in a real project)
class DatabaseManager:
    def __init__(self, db_path="professional_dashboard.db"):
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Connect to the database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {e}")
    
    def create_tables(self):
        """Create necessary database tables"""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT,
                    role TEXT DEFAULT 'user',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # Sales data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    region TEXT,
                    salesperson TEXT
                )
            """)
            
            # System metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    preference_key TEXT NOT NULL,
                    preference_value TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            self.connection.commit()
            
            # Insert default admin user if not exists
            self.create_default_admin()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to create tables: {e}")
    
    def create_default_admin(self):
        """Create default admin user"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                password_hash = hashlib.sha256("admin123".encode()).hexdigest()
                cursor.execute("""
                    INSERT INTO users (username, password_hash, email, role)
                    VALUES (?, ?, ?, ?)
                """, ("admin", password_hash, "admin@company.com", "admin"))
                self.connection.commit()
        except Exception as e:
            print(f"Error creating default admin: {e}")

class AuthenticationSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.current_user = None
    
    def login(self, username, password):
        """Authenticate user login"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                SELECT * FROM users WHERE username = ? AND password_hash = ?
            """, (username, password_hash))
            
            user = cursor.fetchone()
            if user:
                # Update last login
                cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                """, (user['id'],))
                self.db_manager.connection.commit()
                
                self.current_user = dict(user)
                return True
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user

class DataManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_sales_data(self, limit=100):
        """Get sales data for dashboard"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                SELECT * FROM sales ORDER BY sale_date DESC LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching sales data: {e}")
            return []
    
    def add_sale(self, product_name, quantity, price, region, salesperson):
        """Add new sale record"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                INSERT INTO sales (product_name, quantity, price, region, salesperson)
                VALUES (?, ?, ?, ?, ?)
            """, (product_name, quantity, price, region, salesperson))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding sale: {e}")
            return False
    
    def get_sales_summary(self):
        """Get sales summary statistics"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_sales,
                    SUM(quantity * price) as total_revenue,
                    AVG(price) as avg_price,
                    COUNT(DISTINCT product_name) as unique_products
                FROM sales
            """)
            return dict(cursor.fetchone())
        except Exception as e:
            print(f"Error getting sales summary: {e}")
            return {}

class ReportGenerator:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def generate_sales_report(self, format_type="csv"):
        """Generate sales report in specified format"""
        try:
            sales_data = self.data_manager.get_sales_data()
            summary = self.data_manager.get_sales_summary()
            
            if format_type == "csv":
                return self.generate_csv_report(sales_data, summary)
            elif format_type == "json":
                return self.generate_json_report(sales_data, summary)
            else:
                return None
        except Exception as e:
            print(f"Error generating report: {e}")
            return None
    
    def generate_csv_report(self, sales_data, summary):
        """Generate CSV format report"""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write summary
        writer.writerow(["Sales Summary Report"])
        writer.writerow(["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        writer.writerow([])
        writer.writerow(["Total Sales", "Total Revenue", "Average Price", "Unique Products"])
        writer.writerow([summary.get('total_sales', 0), 
                        summary.get('total_revenue', 0),
                        summary.get('avg_price', 0),
                        summary.get('unique_products', 0)])
        writer.writerow([])
        
        # Write sales data
        if sales_data:
            writer.writerow(sales_data[0].keys())
            for sale in sales_data:
                writer.writerow(sale.values())
        
        return output.getvalue()
    
    def generate_json_report(self, sales_data, summary):
        """Generate JSON format report"""
        report = {
            "report_type": "sales_report",
            "generated_at": datetime.now().isoformat(),
            "summary": summary,
            "sales_data": sales_data
        }
        return json.dumps(report, indent=2)

class ProfessionalDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Professional Dashboard")
        self.root.geometry("1400x900")
        self.root.state('zoomed')  # Maximize window
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.auth_system = AuthenticationSystem(self.db_manager)
        self.data_manager = DataManager(self.db_manager)
        self.report_generator = ReportGenerator(self.data_manager)
        
        # Application state
        self.current_page = "login"
        self.pages = {}
        
        # Setup application
        self.setup_styles()
        self.create_main_interface()
        self.show_login()
        
        # Start real-time updates
        self.start_real_time_updates()
    
    def setup_styles(self):
        """Setup application styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure custom styles
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Metric.TLabel', font=('Arial', 14, 'bold'), foreground='blue')
        style.configure('Success.TLabel', foreground='green')
        style.configure('Warning.TLabel', foreground='orange')
        style.configure('Error.TLabel', foreground='red')
    
    def create_main_interface(self):
        """Create the main application interface"""
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Create pages
        self.create_login_page()
        self.create_dashboard_page()
        self.create_data_management_page()
        self.create_reports_page()
        self.create_settings_page()
    
    def create_login_page(self):
        """Create login page"""
        self.pages["login"] = ttk.Frame(self.main_container)
        
        # Login form
        login_frame = ttk.LabelFrame(self.pages["login"], text="Login", padding=20)
        login_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        # Username
        ttk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=10)
        
        # Password
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        # Login button
        login_button = ttk.Button(login_frame, text="Login", command=self.handle_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Default credentials
        ttk.Label(login_frame, text="Default: admin / admin123", 
                 style="Warning.TLabel").grid(row=3, column=0, columnspan=2, pady=10)
    
    def create_dashboard_page(self):
        """Create main dashboard page"""
        self.pages["dashboard"] = ttk.Frame(self.main_container)
        
        # Navigation bar
        nav_frame = ttk.Frame(self.pages["dashboard"])
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(nav_frame, text="Dashboard", 
                  command=lambda: self.show_page("dashboard")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Data Management", 
                  command=lambda: self.show_page("data_management")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Reports", 
                  command=lambda: self.show_page("reports")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Settings", 
                  command=lambda: self.show_page("settings")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Logout", 
                  command=self.handle_logout).pack(side="right", padx=5)
        
        # User info
        self.user_info_label = ttk.Label(nav_frame, text="")
        self.user_info_label.pack(side="right", padx=10)
        
        # Dashboard content
        content_frame = ttk.Frame(self.pages["dashboard"])
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Metrics row
        metrics_frame = ttk.Frame(content_frame)
        metrics_frame.pack(fill="x", pady=10)
        
        self.total_sales_label = ttk.Label(metrics_frame, text="Total Sales: 0", style="Metric.TLabel")
        self.total_sales_label.pack(side="left", padx=20)
        
        self.total_revenue_label = ttk.Label(metrics_frame, text="Total Revenue: $0", style="Metric.TLabel")
        self.total_revenue_label.pack(side="left", padx=20)
        
        self.avg_price_label = ttk.Label(metrics_frame, text="Avg Price: $0", style="Metric.TLabel")
        self.avg_price_label.pack(side="left", padx=20)
        
        self.products_label = ttk.Label(metrics_frame, text="Products: 0", style="Metric.TLabel")
        self.products_label.pack(side="left", padx=20)
        
        # Recent sales table
        sales_frame = ttk.LabelFrame(content_frame, text="Recent Sales", padding=10)
        sales_frame.pack(fill="both", expand=True, pady=10)
        
        # Create Treeview for sales data
        columns = ("ID", "Product", "Quantity", "Price", "Date", "Region", "Salesperson")
        self.sales_tree = ttk.Treeview(sales_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=100)
        
        # Add scrollbar
        sales_scrollbar = ttk.Scrollbar(sales_frame, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=sales_scrollbar.set)
        
        self.sales_tree.pack(side="left", fill="both", expand=True)
        sales_scrollbar.pack(side="right", fill="y")
        
        # Refresh button
        refresh_button = ttk.Button(content_frame, text="Refresh Data", command=self.refresh_dashboard)
        refresh_button.pack(pady=10)
    
    def create_data_management_page(self):
        """Create data management page"""
        self.pages["data_management"] = ttk.Frame(self.main_container)
        
        # Navigation
        nav_frame = ttk.Frame(self.pages["data_management"])
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(nav_frame, text="Dashboard", 
                  command=lambda: self.show_page("dashboard")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Data Management", 
                  command=lambda: self.show_page("data_management")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Reports", 
                  command=lambda: self.show_page("reports")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Settings", 
                  command=lambda: self.show_page("settings")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Logout", 
                  command=self.handle_logout).pack(side="right", padx=5)
        
        # Content
        content_frame = ttk.Frame(self.pages["data_management"])
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add sale form
        form_frame = ttk.LabelFrame(content_frame, text="Add New Sale", padding=10)
        form_frame.pack(fill="x", pady=10)
        
        # Form fields
        ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.product_entry = ttk.Entry(form_frame, width=30)
        self.product_entry.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, sticky="w", pady=5)
        self.quantity_entry = ttk.Entry(form_frame, width=30)
        self.quantity_entry.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, sticky="w", pady=5)
        self.price_entry = ttk.Entry(form_frame, width=30)
        self.price_entry.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Region:").grid(row=3, column=0, sticky="w", pady=5)
        self.region_entry = ttk.Entry(form_frame, width=30)
        self.region_entry.grid(row=3, column=1, pady=5, padx=10)
        
        ttk.Label(form_frame, text="Salesperson:").grid(row=4, column=0, sticky="w", pady=5)
        self.salesperson_entry = ttk.Entry(form_frame, width=30)
        self.salesperson_entry.grid(row=4, column=1, pady=5, padx=10)
        
        # Add button
        add_button = ttk.Button(form_frame, text="Add Sale", command=self.add_sale)
        add_button.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Sales data table
        table_frame = ttk.LabelFrame(content_frame, text="All Sales Data", padding=10)
        table_frame.pack(fill="both", expand=True, pady=10)
        
        # Create Treeview
        columns = ("ID", "Product", "Quantity", "Price", "Date", "Region", "Salesperson")
        self.data_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=100)
        
        # Add scrollbar
        data_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.data_tree.yview)
        self.data_tree.configure(yscrollcommand=data_scrollbar.set)
        
        self.data_tree.pack(side="left", fill="both", expand=True)
        data_scrollbar.pack(side="right", fill="y")
        
        # Refresh button
        refresh_button = ttk.Button(content_frame, text="Refresh Data", command=self.refresh_data_management)
        refresh_button.pack(pady=10)
    
    def create_reports_page(self):
        """Create reports page"""
        self.pages["reports"] = ttk.Frame(self.main_container)
        
        # Navigation
        nav_frame = ttk.Frame(self.pages["reports"])
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(nav_frame, text="Dashboard", 
                  command=lambda: self.show_page("dashboard")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Data Management", 
                  command=lambda: self.show_page("data_management")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Reports", 
                  command=lambda: self.show_page("reports")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Settings", 
                  command=lambda: self.show_page("settings")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Logout", 
                  command=self.handle_logout).pack(side="right", padx=5)
        
        # Content
        content_frame = ttk.Frame(self.pages["reports"])
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Report options
        options_frame = ttk.LabelFrame(content_frame, text="Report Options", padding=10)
        options_frame.pack(fill="x", pady=10)
        
        ttk.Label(options_frame, text="Report Format:").pack(side="left", padx=10)
        self.report_format_var = tk.StringVar(value="csv")
        format_combo = ttk.Combobox(options_frame, textvariable=self.report_format_var,
                                   values=["csv", "json"], state="readonly", width=10)
        format_combo.pack(side="left", padx=10)
        
        generate_button = ttk.Button(options_frame, text="Generate Report", command=self.generate_report)
        generate_button.pack(side="left", padx=20)
        
        # Report preview
        preview_frame = ttk.LabelFrame(content_frame, text="Report Preview", padding=10)
        preview_frame.pack(fill="both", expand=True, pady=10)
        
        self.report_text = tk.Text(preview_frame, wrap="word", height=20)
        report_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=report_scrollbar.set)
        
        self.report_text.pack(side="left", fill="both", expand=True)
        report_scrollbar.pack(side="right", fill="y")
    
    def create_settings_page(self):
        """Create settings page"""
        self.pages["settings"] = ttk.Frame(self.main_container)
        
        # Navigation
        nav_frame = ttk.Frame(self.pages["settings"])
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(nav_frame, text="Dashboard", 
                  command=lambda: self.show_page("dashboard")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Data Management", 
                  command=lambda: self.show_page("data_management")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Reports", 
                  command=lambda: self.show_page("reports")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Settings", 
                  command=lambda: self.show_page("settings")).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Logout", 
                  command=self.handle_logout).pack(side="right", padx=5)
        
        # Content
        content_frame = ttk.Frame(self.pages["settings"])
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Settings form
        settings_frame = ttk.LabelFrame(content_frame, text="Application Settings", padding=20)
        settings_frame.pack(fill="x", pady=10)
        
        # Auto-refresh setting
        self.auto_refresh_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Enable Auto-Refresh", 
                       variable=self.auto_refresh_var).pack(anchor="w", pady=5)
        
        # Refresh interval
        ttk.Label(settings_frame, text="Refresh Interval (seconds):").pack(anchor="w", pady=5)
        self.refresh_interval_var = tk.StringVar(value="30")
        interval_spinbox = ttk.Spinbox(settings_frame, from_=5, to=300, 
                                     textvariable=self.refresh_interval_var, width=10)
        interval_spinbox.pack(anchor="w", pady=5)
        
        # Save button
        save_button = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=20)
        
        # System info
        info_frame = ttk.LabelFrame(content_frame, text="System Information", padding=20)
        info_frame.pack(fill="x", pady=10)
        
        ttk.Label(info_frame, text=f"Database: {self.db_manager.db_path}").pack(anchor="w", pady=2)
        ttk.Label(info_frame, text=f"Current User: {self.auth_system.current_user.get('username', 'Not logged in') if self.auth_system.current_user else 'Not logged in'}").pack(anchor="w", pady=2)
        ttk.Label(info_frame, text=f"User Role: {self.auth_system.current_user.get('role', 'N/A') if self.auth_system.current_user else 'N/A'}").pack(anchor="w", pady=2)
        ttk.Label(info_frame, text=f"Last Login: {self.auth_system.current_user.get('last_login', 'N/A') if self.auth_system.current_user else 'N/A'}").pack(anchor="w", pady=2)
    
    def show_login(self):
        """Show login page"""
        self.current_page = "login"
        for page_name, page in self.pages.items():
            if page_name == "login":
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()
        
        # Focus on username entry
        self.username_entry.focus()
    
    def show_page(self, page_name):
        """Show specified page"""
        if not self.auth_system.current_user:
            self.show_login()
            return
        
        self.current_page = page_name
        for name, page in self.pages.items():
            if name == page_name:
                page.pack(fill="both", expand=True)
            else:
                page.pack_forget()
        
        # Update page-specific content
        if page_name == "dashboard":
            self.refresh_dashboard()
        elif page_name == "data_management":
            self.refresh_data_management()
    
    def handle_login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.auth_system.login(username, password):
            self.show_page("dashboard")
            self.update_user_info()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")
    
    def handle_logout(self):
        """Handle user logout"""
        self.auth_system.logout()
        self.show_login()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def update_user_info(self):
        """Update user information display"""
        user = self.auth_system.get_current_user()
        if user:
            self.user_info_label.config(text=f"Welcome, {user['username']} ({user['role']})")
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        try:
            # Update metrics
            summary = self.data_manager.get_sales_summary()
            total_sales = summary.get('total_sales', 0) or 0
            total_revenue = summary.get('total_revenue', 0) or 0
            avg_price = summary.get('avg_price', 0) or 0
            unique_products = summary.get('unique_products', 0) or 0
            
            self.total_sales_label.config(text=f"Total Sales: {total_sales}")
            self.total_revenue_label.config(text=f"Total Revenue: ${total_revenue:,.2f}")
            self.avg_price_label.config(text=f"Avg Price: ${avg_price:,.2f}")
            self.products_label.config(text=f"Products: {unique_products}")
            
            # Update sales table
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
            
            sales_data = self.data_manager.get_sales_data(20)  # Last 20 sales
            for sale in sales_data:
                self.sales_tree.insert("", "end", values=(
                    sale['id'],
                    sale['product_name'],
                    sale['quantity'],
                    f"${sale['price']:.2f}",
                    sale['sale_date'],
                    sale['region'],
                    sale['salesperson']
                ))
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
    
    def refresh_data_management(self):
        """Refresh data management page"""
        try:
            # Clear existing data
            for item in self.data_tree.get_children():
                self.data_tree.delete(item)
            
            # Load all sales data
            sales_data = self.data_manager.get_sales_data(1000)  # Get more data
            for sale in sales_data:
                self.data_tree.insert("", "end", values=(
                    sale['id'],
                    sale['product_name'],
                    sale['quantity'],
                    f"${sale['price']:.2f}",
                    sale['sale_date'],
                    sale['region'],
                    sale['salesperson']
                ))
        except Exception as e:
            print(f"Error refreshing data management: {e}")
    
    def add_sale(self):
        """Add new sale record"""
        try:
            product_name = self.product_entry.get().strip()
            quantity = int(self.quantity_entry.get().strip())
            price = float(self.price_entry.get().strip())
            region = self.region_entry.get().strip()
            salesperson = self.salesperson_entry.get().strip()
            
            if not all([product_name, quantity, price, region, salesperson]):
                messagebox.showwarning("Validation Error", "All fields are required")
                return
            
            if quantity <= 0 or price <= 0:
                messagebox.showwarning("Validation Error", "Quantity and price must be positive")
                return
            
            if self.data_manager.add_sale(product_name, quantity, price, region, salesperson):
                messagebox.showinfo("Success", "Sale added successfully")
                # Clear form
                self.product_entry.delete(0, tk.END)
                self.quantity_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.region_entry.delete(0, tk.END)
                self.salesperson_entry.delete(0, tk.END)
                # Refresh data
                self.refresh_data_management()
            else:
                messagebox.showerror("Error", "Failed to add sale")
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid numbers for quantity and price")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add sale: {e}")
    
    def generate_report(self):
        """Generate and display report"""
        try:
            format_type = self.report_format_var.get()
            report_content = self.report_generator.generate_sales_report(format_type)
            
            if report_content:
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(1.0, report_content)
                messagebox.showinfo("Success", f"Report generated in {format_type.upper()} format")
            else:
                messagebox.showerror("Error", "Failed to generate report")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {e}")
    
    def save_settings(self):
        """Save application settings"""
        try:
            # In a real application, you would save these to a configuration file or database
            settings = {
                "auto_refresh": self.auto_refresh_var.get(),
                "refresh_interval": int(self.refresh_interval_var.get())
            }
            messagebox.showinfo("Success", "Settings saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def start_real_time_updates(self):
        """Start real-time data updates"""
        def update_loop():
            while True:
                try:
                    if (self.current_page == "dashboard" and 
                        self.auth_system.current_user and 
                        self.auto_refresh_var.get()):
                        self.root.after(0, self.refresh_dashboard)
                    
                    # Update every 30 seconds by default
                    time.sleep(int(self.refresh_interval_var.get()))
                except Exception as e:
                    print(f"Error in update loop: {e}")
                    time.sleep(30)
        
        # Start update thread
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main application entry point"""
    try:
        app = ProfessionalDashboard()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()

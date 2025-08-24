"""
Database Dashboard - Chapter 7 Example
A comprehensive dashboard for managing multiple database tables with visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DatabaseDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Dashboard")
        self.root.geometry("1200x800")
        
        # Database connection
        self.db_path = "dashboard_data.db"
        self.connection = None
        self.connect_database()
        self.create_tables()
        self.load_sample_data()
        
        # Create main interface
        self.create_widgets()
        self.refresh_all_data()
    
    def connect_database(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print("Database connected successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
    
    def create_tables(self):
        """Create necessary tables"""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT DEFAULT 'user',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)
            
            # Analytics table for dashboard metrics
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.connection.commit()
            print("Tables created successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to create tables: {e}")
    
    def load_sample_data(self):
        """Load sample data if tables are empty"""
        try:
            cursor = self.connection.cursor()
            
            # Check if users table is empty
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # Insert sample users
                sample_users = [
                    ("John Doe", "john@example.com", "admin"),
                    ("Jane Smith", "jane@example.com", "user"),
                    ("Bob Johnson", "bob@example.com", "user"),
                    ("Alice Brown", "alice@example.com", "manager")
                ]
                cursor.executemany(
                    "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
                    sample_users
                )
            
            # Check if products table is empty
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                # Insert sample products
                sample_products = [
                    ("Laptop", "Electronics", 999.99, 50),
                    ("Mouse", "Electronics", 29.99, 100),
                    ("Desk Chair", "Furniture", 199.99, 25),
                    ("Coffee Mug", "Kitchen", 9.99, 200),
                    ("Notebook", "Office", 5.99, 150)
                ]
                cursor.executemany(
                    "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
                    sample_products
                )
            
            # Check if orders table is empty
            cursor.execute("SELECT COUNT(*) FROM orders")
            if cursor.fetchone()[0] == 0:
                # Insert sample orders
                for _ in range(20):
                    user_id = random.randint(1, 4)
                    product_id = random.randint(1, 5)
                    quantity = random.randint(1, 5)
                    
                    # Get product price
                    cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
                    price = cursor.fetchone()['price']
                    total_price = price * quantity
                    
                    # Random date within last 30 days
                    random_days = random.randint(0, 30)
                    order_date = datetime.now() - timedelta(days=random_days)
                    
                    cursor.execute(
                        "INSERT INTO orders (user_id, product_id, quantity, total_price, order_date) VALUES (?, ?, ?, ?, ?)",
                        (user_id, product_id, quantity, total_price, order_date)
                    )
            
            self.connection.commit()
            print("Sample data loaded successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load sample data: {e}")
    
    def create_widgets(self):
        """Create the main dashboard interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_overview_tab()
        self.create_users_tab()
        self.create_products_tab()
        self.create_orders_tab()
        self.create_analytics_tab()
    
    def create_overview_tab(self):
        """Create the overview tab with key metrics"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="Overview")
        
        # Title
        title_label = ttk.Label(overview_frame, text="Dashboard Overview", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Metrics frame
        metrics_frame = ttk.Frame(overview_frame)
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        # Create metric cards
        self.total_users_label = ttk.Label(metrics_frame, text="Total Users: 0", 
                                          font=("Arial", 12))
        self.total_users_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.total_products_label = ttk.Label(metrics_frame, text="Total Products: 0", 
                                             font=("Arial", 12))
        self.total_products_label.grid(row=0, column=1, padx=20, pady=10)
        
        self.total_orders_label = ttk.Label(metrics_frame, text="Total Orders: 0", 
                                           font=("Arial", 12))
        self.total_orders_label.grid(row=0, column=2, padx=20, pady=10)
        
        self.total_revenue_label = ttk.Label(metrics_frame, text="Total Revenue: $0", 
                                            font=("Arial", 12))
        self.total_revenue_label.grid(row=0, column=3, padx=20, pady=10)
        
        # Charts frame
        charts_frame = ttk.Frame(overview_frame)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create charts
        self.create_sales_chart(charts_frame)
        self.create_category_chart(charts_frame)
        
        # Refresh button
        refresh_btn = ttk.Button(overview_frame, text="Refresh Data", 
                                command=self.refresh_all_data)
        refresh_btn.pack(pady=10)
    
    def create_sales_chart(self, parent):
        """Create sales over time chart"""
        chart_frame = ttk.LabelFrame(parent, text="Sales Over Time")
        chart_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        fig = Figure(figsize=(6, 4), dpi=100)
        self.sales_plot = fig.add_subplot(111)
        
        self.sales_canvas = FigureCanvasTkAgg(fig, chart_frame)
        self.sales_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_category_chart(self, parent):
        """Create category distribution chart"""
        chart_frame = ttk.LabelFrame(parent, text="Sales by Category")
        chart_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        fig = Figure(figsize=(6, 4), dpi=100)
        self.category_plot = fig.add_subplot(111)
        
        self.category_canvas = FigureCanvasTkAgg(fig, chart_frame)
        self.category_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_users_tab(self):
        """Create the users management tab"""
        users_frame = ttk.Frame(self.notebook)
        self.notebook.add(users_frame, text="Users")
        
        # Title
        title_label = ttk.Label(users_frame, text="User Management", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = ttk.LabelFrame(users_frame, text="Add New User")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Form fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.user_name_entry = ttk.Entry(form_frame, width=30)
        self.user_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.user_email_entry = ttk.Entry(form_frame, width=30)
        self.user_email_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        self.user_role_combo = ttk.Combobox(form_frame, values=["user", "admin", "manager"], 
                                           state="readonly", width=27)
        self.user_role_combo.set("user")
        self.user_role_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add User", 
                  command=self.add_user).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", 
                  command=self.clear_user_form).pack(side="left", padx=5)
        
        # Users table
        table_frame = ttk.LabelFrame(users_frame, text="Users List")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ID", "Name", "Email", "Role", "Created")
        self.users_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click for editing
        self.users_tree.bind("<Double-1>", self.edit_user)
    
    def create_products_tab(self):
        """Create the products management tab"""
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text="Products")
        
        # Title
        title_label = ttk.Label(products_frame, text="Product Management", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = ttk.LabelFrame(products_frame, text="Add New Product")
        form_frame.pack(fill="x", padx=20, pady=10)
        
        # Form fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = ttk.Entry(form_frame, width=30)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.product_category_entry = ttk.Entry(form_frame, width=30)
        self.product_category_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.product_price_entry = ttk.Entry(form_frame, width=30)
        self.product_price_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Stock:").grid(row=3, column=0, padx=5, pady=5)
        self.product_stock_entry = ttk.Entry(form_frame, width=30)
        self.product_stock_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Add Product", 
                  command=self.add_product).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear Form", 
                  command=self.clear_product_form).pack(side="left", padx=5)
        
        # Products table
        table_frame = ttk.LabelFrame(products_frame, text="Products List")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ID", "Name", "Category", "Price", "Stock", "Created")
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind double-click for editing
        self.products_tree.bind("<Double-1>", self.edit_product)
    
    def create_orders_tab(self):
        """Create the orders management tab"""
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="Orders")
        
        # Title
        title_label = ttk.Label(orders_frame, text="Order Management", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Orders table
        table_frame = ttk.LabelFrame(orders_frame, text="Orders List")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ID", "User", "Product", "Quantity", "Total", "Date")
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_analytics_tab(self):
        """Create the analytics tab"""
        analytics_frame = ttk.Frame(self.notebook)
        self.notebook.add(analytics_frame, text="Analytics")
        
        # Title
        title_label = ttk.Label(analytics_frame, text="Analytics Dashboard", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Analytics content
        content_frame = ttk.Frame(analytics_frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Top selling products
        top_products_frame = ttk.LabelFrame(content_frame, text="Top Selling Products")
        top_products_frame.pack(fill="x", pady=10)
        
        self.top_products_text = tk.Text(top_products_frame, height=8, width=50)
        self.top_products_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Recent orders
        recent_orders_frame = ttk.LabelFrame(content_frame, text="Recent Orders")
        recent_orders_frame.pack(fill="x", pady=10)
        
        self.recent_orders_text = tk.Text(recent_orders_frame, height=8, width=50)
        self.recent_orders_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def refresh_all_data(self):
        """Refresh all data displays"""
        self.refresh_overview_metrics()
        self.refresh_users_table()
        self.refresh_products_table()
        self.refresh_orders_table()
        self.refresh_analytics()
        self.update_charts()
    
    def refresh_overview_metrics(self):
        """Update overview metrics"""
        try:
            cursor = self.connection.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            self.total_users_label.config(text=f"Total Users: {total_users}")
            
            # Total products
            cursor.execute("SELECT COUNT(*) FROM products")
            total_products = cursor.fetchone()[0]
            self.total_products_label.config(text=f"Total Products: {total_products}")
            
            # Total orders
            cursor.execute("SELECT COUNT(*) FROM orders")
            total_orders = cursor.fetchone()[0]
            self.total_orders_label.config(text=f"Total Orders: {total_orders}")
            
            # Total revenue
            cursor.execute("SELECT SUM(total_price) FROM orders")
            total_revenue = cursor.fetchone()[0] or 0
            self.total_revenue_label.config(text=f"Total Revenue: ${total_revenue:.2f}")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to refresh metrics: {e}")
    
    def refresh_users_table(self):
        """Refresh users table"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users ORDER BY created_date DESC")
            users = cursor.fetchall()
            
            for user in users:
                self.users_tree.insert("", "end", values=(
                    user['id'], user['name'], user['email'], 
                    user['role'], user['created_date']
                ))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load users: {e}")
    
    def refresh_products_table(self):
        """Refresh products table"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products ORDER BY created_date DESC")
            products = cursor.fetchall()
            
            for product in products:
                self.products_tree.insert("", "end", values=(
                    product['id'], product['name'], product['category'],
                    f"${product['price']:.2f}", product['stock'], product['created_date']
                ))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load products: {e}")
    
    def refresh_orders_table(self):
        """Refresh orders table"""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT o.id, u.name as user_name, p.name as product_name, 
                       o.quantity, o.total_price, o.order_date
                FROM orders o
                JOIN users u ON o.user_id = u.id
                JOIN products p ON o.product_id = p.id
                ORDER BY o.order_date DESC
            """)
            orders = cursor.fetchall()
            
            for order in orders:
                self.orders_tree.insert("", "end", values=(
                    order['id'], order['user_name'], order['product_name'],
                    order['quantity'], f"${order['total_price']:.2f}", order['order_date']
                ))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load orders: {e}")
    
    def refresh_analytics(self):
        """Refresh analytics data"""
        try:
            cursor = self.connection.cursor()
            
            # Top selling products
            cursor.execute("""
                SELECT p.name, SUM(o.quantity) as total_sold
                FROM orders o
                JOIN products p ON o.product_id = p.id
                GROUP BY p.id, p.name
                ORDER BY total_sold DESC
                LIMIT 5
            """)
            top_products = cursor.fetchall()
            
            self.top_products_text.delete(1.0, tk.END)
            self.top_products_text.insert(tk.END, "Top Selling Products:\n\n")
            for product in top_products:
                self.top_products_text.insert(tk.END, 
                    f"{product['name']}: {product['total_sold']} units\n")
            
            # Recent orders
            cursor.execute("""
                SELECT u.name as user_name, p.name as product_name, 
                       o.quantity, o.total_price, o.order_date
                FROM orders o
                JOIN users u ON o.user_id = u.id
                JOIN products p ON o.product_id = p.id
                ORDER BY o.order_date DESC
                LIMIT 10
            """)
            recent_orders = cursor.fetchall()
            
            self.recent_orders_text.delete(1.0, tk.END)
            self.recent_orders_text.insert(tk.END, "Recent Orders:\n\n")
            for order in recent_orders:
                self.recent_orders_text.insert(tk.END, 
                    f"{order['user_name']} - {order['product_name']} "
                    f"({order['quantity']}x) - ${order['total_price']:.2f}\n")
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load analytics: {e}")
    
    def update_charts(self):
        """Update dashboard charts"""
        try:
            cursor = self.connection.cursor()
            
            # Sales over time chart
            cursor.execute("""
                SELECT DATE(order_date) as date, SUM(total_price) as daily_sales
                FROM orders
                WHERE order_date >= date('now', '-30 days')
                GROUP BY DATE(order_date)
                ORDER BY date
            """)
            sales_data = cursor.fetchall()
            
            if sales_data:
                dates = [row['date'] for row in sales_data]
                sales = [row['daily_sales'] for row in sales_data]
                
                self.sales_plot.clear()
                self.sales_plot.plot(dates, sales, marker='o')
                self.sales_plot.set_title("Daily Sales (Last 30 Days)")
                self.sales_plot.set_xlabel("Date")
                self.sales_plot.set_ylabel("Sales ($)")
                self.sales_plot.tick_params(axis='x', rotation=45)
                self.sales_plot.grid(True, alpha=0.3)
                self.sales_canvas.draw()
            
            # Category distribution chart
            cursor.execute("""
                SELECT p.category, SUM(o.total_price) as category_sales
                FROM orders o
                JOIN products p ON o.product_id = p.id
                GROUP BY p.category
                ORDER BY category_sales DESC
            """)
            category_data = cursor.fetchall()
            
            if category_data:
                categories = [row['category'] for row in category_data]
                sales = [row['category_sales'] for row in category_data]
                
                self.category_plot.clear()
                self.category_plot.pie(sales, labels=categories, autopct='%1.1f%%')
                self.category_plot.set_title("Sales by Category")
                self.category_canvas.draw()
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update charts: {e}")
    
    def add_user(self):
        """Add a new user"""
        name = self.user_name_entry.get().strip()
        email = self.user_email_entry.get().strip()
        role = self.user_role_combo.get()
        
        if not name or not email:
            messagebox.showwarning("Validation Error", "Please fill in all fields")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", 
                          (name, email, role))
            self.connection.commit()
            
            self.clear_user_form()
            self.refresh_users_table()
            self.refresh_overview_metrics()
            messagebox.showinfo("Success", "User added successfully")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add user: {e}")
    
    def add_product(self):
        """Add a new product"""
        name = self.product_name_entry.get().strip()
        category = self.product_category_entry.get().strip()
        price = self.product_price_entry.get().strip()
        stock = self.product_stock_entry.get().strip()
        
        if not all([name, category, price, stock]):
            messagebox.showwarning("Validation Error", "Please fill in all fields")
            return
        
        try:
            price = float(price)
            stock = int(stock)
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a number and stock must be an integer")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)", 
                          (name, category, price, stock))
            self.connection.commit()
            
            self.clear_product_form()
            self.refresh_products_table()
            self.refresh_overview_metrics()
            messagebox.showinfo("Success", "Product added successfully")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add product: {e}")
    
    def clear_user_form(self):
        """Clear user form fields"""
        self.user_name_entry.delete(0, tk.END)
        self.user_email_entry.delete(0, tk.END)
        self.user_role_combo.set("user")
    
    def clear_product_form(self):
        """Clear product form fields"""
        self.product_name_entry.delete(0, tk.END)
        self.product_category_entry.delete(0, tk.END)
        self.product_price_entry.delete(0, tk.END)
        self.product_stock_entry.delete(0, tk.END)
    
    def edit_user(self, event):
        """Edit user on double-click"""
        selection = self.users_tree.selection()
        if not selection:
            return
        
        item = self.users_tree.item(selection[0])
        user_id = item['values'][0]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit User")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get current user data
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                messagebox.showerror("Error", "User not found")
                dialog.destroy()
                return
            
            # Form fields
            ttk.Label(dialog, text="Name:").pack(pady=5)
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, user['name'])
            name_entry.pack(pady=5)
            
            ttk.Label(dialog, text="Email:").pack(pady=5)
            email_entry = ttk.Entry(dialog, width=30)
            email_entry.insert(0, user['email'])
            email_entry.pack(pady=5)
            
            ttk.Label(dialog, text="Role:").pack(pady=5)
            role_combo = ttk.Combobox(dialog, values=["user", "admin", "manager"], 
                                     state="readonly", width=27)
            role_combo.set(user['role'])
            role_combo.pack(pady=5)
            
            def save_changes():
                try:
                    cursor.execute("UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?",
                                  (name_entry.get().strip(), email_entry.get().strip(), 
                                   role_combo.get(), user_id))
                    self.connection.commit()
                    self.refresh_users_table()
                    dialog.destroy()
                    messagebox.showinfo("Success", "User updated successfully")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Email already exists")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Failed to update user: {e}")
            
            ttk.Button(dialog, text="Save", command=save_changes).pack(pady=10)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load user: {e}")
            dialog.destroy()
    
    def edit_product(self, event):
        """Edit product on double-click"""
        selection = self.products_tree.selection()
        if not selection:
            return
        
        item = self.products_tree.item(selection[0])
        product_id = item['values'][0]
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Get current product data
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                messagebox.showerror("Error", "Product not found")
                dialog.destroy()
                return
            
            # Form fields
            ttk.Label(dialog, text="Name:").pack(pady=5)
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.insert(0, product['name'])
            name_entry.pack(pady=5)
            
            ttk.Label(dialog, text="Category:").pack(pady=5)
            category_entry = ttk.Entry(dialog, width=30)
            category_entry.insert(0, product['category'])
            category_entry.pack(pady=5)
            
            ttk.Label(dialog, text="Price:").pack(pady=5)
            price_entry = ttk.Entry(dialog, width=30)
            price_entry.insert(0, str(product['price']))
            price_entry.pack(pady=5)
            
            ttk.Label(dialog, text="Stock:").pack(pady=5)
            stock_entry = ttk.Entry(dialog, width=30)
            stock_entry.insert(0, str(product['stock']))
            stock_entry.pack(pady=5)
            
            def save_changes():
                try:
                    price = float(price_entry.get().strip())
                    stock = int(stock_entry.get().strip())
                    
                    cursor.execute("UPDATE products SET name = ?, category = ?, price = ?, stock = ? WHERE id = ?",
                                  (name_entry.get().strip(), category_entry.get().strip(), 
                                   price, stock, product_id))
                    self.connection.commit()
                    self.refresh_products_table()
                    dialog.destroy()
                    messagebox.showinfo("Success", "Product updated successfully")
                except ValueError:
                    messagebox.showerror("Validation Error", "Price must be a number and stock must be an integer")
                except sqlite3.Error as e:
                    messagebox.showerror("Database Error", f"Failed to update product: {e}")
            
            ttk.Button(dialog, text="Save", command=save_changes).pack(pady=10)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load product: {e}")
            dialog.destroy()

def main():
    root = tk.Tk()
    app = DatabaseDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()

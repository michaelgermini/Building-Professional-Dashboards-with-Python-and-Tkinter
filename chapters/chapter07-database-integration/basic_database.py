"""
Chapter 7: Database Integration
Example: Basic SQLite Database Operations

This example demonstrates fundamental SQLite database operations
including connection management, table creation, and basic CRUD operations.
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import logging

# =============================================================================
# DATABASE MANAGER
# =============================================================================

class DatabaseManager:
    """Manages SQLite database connections and operations"""
    
    def __init__(self, db_path="dashboard.db"):
        self.db_path = db_path
        self.connection = None
        self.setup_logging()
        self.connect()
        self.create_tables()
    
    def setup_logging(self):
        """Setup logging for database operations"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('database.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.logger.info(f"Database connected successfully: {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("Database connection closed")
    
    def create_tables(self):
        """Create necessary database tables"""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT DEFAULT 'user',
                    is_active BOOLEAN DEFAULT 1,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    category TEXT,
                    stock_quantity INTEGER DEFAULT 0,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")
            
            self.connection.commit()
            self.logger.info("Database tables created successfully")
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create tables: {e}")
            messagebox.showerror("Database Error", f"Failed to create tables: {e}")
    
    def execute_query(self, query, parameters=None):
        """Execute a database query with error handling"""
        try:
            cursor = self.connection.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            self.logger.error(f"Query execution failed: {e}")
            raise e
    
    def insert_record(self, table, data):
        """Insert a record into the specified table"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor = self.execute_query(query, list(data.values()))
            self.connection.commit()
            
            record_id = cursor.lastrowid
            self.logger.info(f"Record inserted into {table} with ID: {record_id}")
            return record_id
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to insert record into {table}: {e}")
            raise e
    
    def select_records(self, table, conditions=None, order_by=None, limit=None):
        """Select records from the specified table"""
        try:
            query = f"SELECT * FROM {table}"
            parameters = []
            
            if conditions:
                where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
                query += f" WHERE {where_clause}"
                parameters.extend(conditions.values())
            
            if order_by:
                query += f" ORDER BY {order_by}"
            
            if limit:
                query += f" LIMIT {limit}"
            
            cursor = self.execute_query(query, parameters)
            return cursor.fetchall()
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to select records from {table}: {e}")
            raise e
    
    def update_record(self, table, data, conditions):
        """Update records in the specified table"""
        try:
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            
            parameters = list(data.values()) + list(conditions.values())
            cursor = self.execute_query(query, parameters)
            self.connection.commit()
            
            rows_affected = cursor.rowcount
            self.logger.info(f"Updated {rows_affected} records in {table}")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update records in {table}: {e}")
            raise e
    
    def delete_record(self, table, conditions):
        """Delete records from the specified table"""
        try:
            where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            query = f"DELETE FROM {table} WHERE {where_clause}"
            
            cursor = self.execute_query(query, list(conditions.values()))
            self.connection.commit()
            
            rows_affected = cursor.rowcount
            self.logger.info(f"Deleted {rows_affected} records from {table}")
            return rows_affected
            
        except sqlite3.Error as e:
            self.logger.error(f"Failed to delete records from {table}: {e}")
            raise e
    
    def get_table_info(self, table):
        """Get information about table structure"""
        try:
            cursor = self.execute_query(f"PRAGMA table_info({table})")
            return cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Failed to get table info for {table}: {e}")
            raise e
    
    def backup_database(self, backup_path):
        """Create a backup of the database"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            self.logger.info(f"Database backed up to: {backup_path}")
        except Exception as e:
            self.logger.error(f"Failed to backup database: {e}")
            raise e

# =============================================================================
# BASIC DATABASE DEMO
# =============================================================================

class BasicDatabaseDemo:
    """Demo application showing basic database operations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Database Operations Demo")
        self.root.geometry("1000x700")
        
        self.db_manager = DatabaseManager()
        self.create_widgets()
        self.load_sample_data()
    
    def create_widgets(self):
        """Create the main application interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="Basic Database Operations Demo",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Operations
        left_panel = tk.LabelFrame(content_frame, text="Database Operations", font=("Arial", 12, "bold"))
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Users section
        users_frame = tk.LabelFrame(left_panel, text="Users", font=("Arial", 10))
        users_frame.pack(fill="x", padx=10, pady=10)
        
        # Add user form
        tk.Label(users_frame, text="Username:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.username_entry = tk.Entry(users_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(users_frame, text="Email:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.email_entry = tk.Entry(users_frame, width=20)
        self.email_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(users_frame, text="Full Name:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.fullname_entry = tk.Entry(users_frame, width=20)
        self.fullname_entry.grid(row=2, column=1, padx=5, pady=2)
        
        tk.Button(users_frame, text="Add User", command=self.add_user, width=15).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Products section
        products_frame = tk.LabelFrame(left_panel, text="Products", font=("Arial", 10))
        products_frame.pack(fill="x", padx=10, pady=10)
        
        # Add product form
        tk.Label(products_frame, text="Name:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.product_name_entry = tk.Entry(products_frame, width=20)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(products_frame, text="Price:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.price_entry = tk.Entry(products_frame, width=20)
        self.price_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(products_frame, text="Category:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.category_entry = tk.Entry(products_frame, width=20)
        self.category_entry.grid(row=2, column=1, padx=5, pady=2)
        
        tk.Button(products_frame, text="Add Product", command=self.add_product, width=15).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Database operations
        operations_frame = tk.LabelFrame(left_panel, text="Database Operations", font=("Arial", 10))
        operations_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(operations_frame, text="Refresh Data", command=self.refresh_data, width=15).pack(pady=5)
        tk.Button(operations_frame, text="Backup Database", command=self.backup_database, width=15).pack(pady=5)
        tk.Button(operations_frame, text="Show Table Info", command=self.show_table_info, width=15).pack(pady=5)
        
        # Right panel - Data display
        right_panel = tk.Frame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Notebook for different tables
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill="both", expand=True)
        
        # Users tab
        self.users_tab = tk.Frame(self.notebook)
        self.notebook.add(self.users_tab, text="Users")
        self.create_users_table()
        
        # Products tab
        self.products_tab = tk.Frame(self.notebook)
        self.notebook.add(self.products_tab, text="Products")
        self.create_products_table()
        
        # Orders tab
        self.orders_tab = tk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text="Orders")
        self.create_orders_table()
    
    def create_users_table(self):
        """Create the users table display"""
        # Control frame
        control_frame = tk.Frame(self.users_tab)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(control_frame, text="Delete Selected", command=self.delete_selected_user).pack(side="left", padx=5)
        tk.Button(control_frame, text="Refresh", command=self.load_users).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Username", "Email", "Full Name", "Role", "Active", "Created")
        self.users_tree = ttk.Treeview(self.users_tab, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.users_tab, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
    
    def create_products_table(self):
        """Create the products table display"""
        # Control frame
        control_frame = tk.Frame(self.products_tab)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(control_frame, text="Delete Selected", command=self.delete_selected_product).pack(side="left", padx=5)
        tk.Button(control_frame, text="Refresh", command=self.load_products).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Name", "Description", "Price", "Category", "Stock", "Created")
        self.products_tree = ttk.Treeview(self.products_tab, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.products_tab, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        self.products_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
    
    def create_orders_table(self):
        """Create the orders table display"""
        # Control frame
        control_frame = tk.Frame(self.orders_tab)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(control_frame, text="Refresh", command=self.load_orders).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "User ID", "Product ID", "Quantity", "Total Price", "Status", "Order Date")
        self.orders_tree = ttk.Treeview(self.orders_tab, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.orders_tab, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        self.orders_tree.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
    
    def add_user(self):
        """Add a new user to the database"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        full_name = self.fullname_entry.get().strip()
        
        if not all([username, email, full_name]):
            messagebox.showwarning("Validation Error", "Please fill in all fields")
            return
        
        try:
            user_data = {
                'username': username,
                'email': email,
                'full_name': full_name,
                'role': 'user',
                'is_active': 1
            }
            
            self.db_manager.insert_record('users', user_data)
            
            # Clear form
            self.username_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.fullname_entry.delete(0, tk.END)
            
            # Refresh display
            self.load_users()
            messagebox.showinfo("Success", "User added successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {e}")
    
    def add_product(self):
        """Add a new product to the database"""
        name = self.product_name_entry.get().strip()
        price = self.price_entry.get().strip()
        category = self.category_entry.get().strip()
        
        if not all([name, price]):
            messagebox.showwarning("Validation Error", "Please fill in name and price")
            return
        
        try:
            price_value = float(price)
            product_data = {
                'name': name,
                'price': price_value,
                'category': category or 'General',
                'stock_quantity': 0
            }
            
            self.db_manager.insert_record('products', product_data)
            
            # Clear form
            self.product_name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
            
            # Refresh display
            self.load_products()
            messagebox.showinfo("Success", "Product added successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Price must be a valid number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")
    
    def load_users(self):
        """Load and display users"""
        try:
            # Clear existing items
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)
            
            # Load users from database
            users = self.db_manager.select_records('users', order_by='created_date DESC')
            
            for user in users:
                self.users_tree.insert("", "end", values=(
                    user['id'],
                    user['username'],
                    user['email'],
                    user['full_name'],
                    user['role'],
                    "Yes" if user['is_active'] else "No",
                    user['created_date']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {e}")
    
    def load_products(self):
        """Load and display products"""
        try:
            # Clear existing items
            for item in self.products_tree.get_children():
                self.products_tree.delete(item)
            
            # Load products from database
            products = self.db_manager.select_records('products', order_by='created_date DESC')
            
            for product in products:
                self.products_tree.insert("", "end", values=(
                    product['id'],
                    product['name'],
                    product['description'] or '',
                    f"${product['price']:.2f}",
                    product['category'],
                    product['stock_quantity'],
                    product['created_date']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products: {e}")
    
    def load_orders(self):
        """Load and display orders"""
        try:
            # Clear existing items
            for item in self.orders_tree.get_children():
                self.orders_tree.delete(item)
            
            # Load orders from database
            orders = self.db_manager.select_records('orders', order_by='order_date DESC')
            
            for order in orders:
                self.orders_tree.insert("", "end", values=(
                    order['id'],
                    order['user_id'],
                    order['product_id'],
                    order['quantity'],
                    f"${order['total_price']:.2f}",
                    order['status'],
                    order['order_date']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load orders: {e}")
    
    def delete_selected_user(self):
        """Delete the selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            try:
                item = self.users_tree.item(selected[0])
                user_id = item['values'][0]
                
                self.db_manager.delete_record('users', {'id': user_id})
                self.load_users()
                messagebox.showinfo("Success", "User deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")
    
    def delete_selected_product(self):
        """Delete the selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?"):
            try:
                item = self.products_tree.item(selected[0])
                product_id = item['values'][0]
                
                self.db_manager.delete_record('products', {'id': product_id})
                self.load_products()
                messagebox.showinfo("Success", "Product deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {e}")
    
    def refresh_data(self):
        """Refresh all data displays"""
        self.load_users()
        self.load_products()
        self.load_orders()
        messagebox.showinfo("Success", "Data refreshed successfully")
    
    def backup_database(self):
        """Create a backup of the database"""
        try:
            backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            self.db_manager.backup_database(backup_path)
            messagebox.showinfo("Success", f"Database backed up to: {backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup database: {e}")
    
    def show_table_info(self):
        """Show information about database tables"""
        try:
            info_window = tk.Toplevel(self.root)
            info_window.title("Database Table Information")
            info_window.geometry("600x400")
            
            notebook = ttk.Notebook(info_window)
            notebook.pack(fill="both", expand=True, padx=10, pady=10)
            
            tables = ['users', 'products', 'orders']
            for table in tables:
                tab = tk.Frame(notebook)
                notebook.add(tab, text=table.capitalize())
                
                # Get table info
                table_info = self.db_manager.get_table_info(table)
                
                # Create treeview for table info
                columns = ("Column", "Type", "Not Null", "Default", "Primary Key")
                tree = ttk.Treeview(tab, columns=columns, show="headings", height=10)
                
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100)
                
                for info in table_info:
                    tree.insert("", "end", values=(
                        info['name'],
                        info['type'],
                        "Yes" if info['notnull'] else "No",
                        info['dflt_value'] or '',
                        "Yes" if info['pk'] else "No"
                    ))
                
                tree.pack(fill="both", expand=True, padx=10, pady=10)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show table info: {e}")
    
    def load_sample_data(self):
        """Load sample data into the database"""
        try:
            # Check if data already exists
            users = self.db_manager.select_records('users', limit=1)
            if users:
                return  # Data already exists
            
            # Sample users
            sample_users = [
                {'username': 'admin', 'email': 'admin@example.com', 'full_name': 'Administrator', 'role': 'admin'},
                {'username': 'john_doe', 'email': 'john@example.com', 'full_name': 'John Doe', 'role': 'user'},
                {'username': 'jane_smith', 'email': 'jane@example.com', 'full_name': 'Jane Smith', 'role': 'user'}
            ]
            
            for user_data in sample_users:
                self.db_manager.insert_record('users', user_data)
            
            # Sample products
            sample_products = [
                {'name': 'Laptop', 'description': 'High-performance laptop', 'price': 999.99, 'category': 'Electronics', 'stock_quantity': 10},
                {'name': 'Mouse', 'description': 'Wireless mouse', 'price': 29.99, 'category': 'Electronics', 'stock_quantity': 50},
                {'name': 'Desk Chair', 'description': 'Ergonomic office chair', 'price': 199.99, 'category': 'Furniture', 'stock_quantity': 5}
            ]
            
            for product_data in sample_products:
                self.db_manager.insert_record('products', product_data)
            
            self.logger.info("Sample data loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to load sample data: {e}")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

class BasicDatabaseApp:
    """Main application for basic database operations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Database Operations")
        self.root.geometry("1000x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Create demo
        self.demo = BasicDatabaseDemo(self.root)
    
    def on_closing(self):
        """Handle application closing"""
        if hasattr(self.demo, 'db_manager'):
            self.demo.db_manager.disconnect()
        self.root.destroy()

def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the basic database app
    app = BasicDatabaseApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()

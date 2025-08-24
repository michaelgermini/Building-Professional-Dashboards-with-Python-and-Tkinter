"""
Chapter 7: Database Integration
Example: Advanced CRUD Operations

This example demonstrates advanced CRUD operations with professional
forms, data validation, search/filtering, and comprehensive data management.
"""

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import re
from datetime import datetime
import json

# =============================================================================
# VALIDATION UTILITIES
# =============================================================================

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class Validator:
    """Base class for form validators"""
    
    def __init__(self, error_message="Invalid input"):
        self.error_message = error_message
    
    def validate(self, value):
        """Validate the input value - to be implemented by subclasses"""
        return True, None

class RequiredValidator(Validator):
    """Validator for required fields"""
    
    def __init__(self, error_message="This field is required"):
        super().__init__(error_message)
    
    def validate(self, value):
        if not value or value.strip() == "":
            return False, self.error_message
        return True, None

class EmailValidator(Validator):
    """Validator for email addresses"""
    
    def __init__(self, error_message="Invalid email address"):
        super().__init__(error_message)
    
    def validate(self, value):
        if not value:
            return True, None  # Allow empty if not required
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            return False, self.error_message
        return True, None

class NumberValidator(Validator):
    """Validator for numeric input"""
    
    def __init__(self, min_value=None, max_value=None, error_message="Invalid number"):
        super().__init__(error_message)
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value):
        if not value:
            return True, None  # Allow empty if not required
        
        try:
            num_value = float(value)
            if self.min_value is not None and num_value < self.min_value:
                return False, f"Value must be at least {self.min_value}"
            if self.max_value is not None and num_value > self.max_value:
                return False, f"Value must be at most {self.max_value}"
            return True, None
        except ValueError:
            return False, self.error_message

# =============================================================================
# ADVANCED FORM WIDGETS
# =============================================================================

class ValidatedEntry(tk.Frame):
    """Entry widget with validation and error display"""
    
    def __init__(self, parent, label="", validators=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.label = label
        self.validators = validators or []
        self.error_label = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create the validated entry interface"""
        # Label
        if self.label:
            label_widget = tk.Label(self, text=self.label, anchor="w")
            label_widget.pack(fill="x", pady=(0, 2))
        
        # Entry frame
        entry_frame = tk.Frame(self)
        entry_frame.pack(fill="x")
        
        # Entry widget
        self.entry = tk.Entry(entry_frame)
        self.entry.pack(side="left", fill="x", expand=True)
        
        # Error label (initially hidden)
        self.error_label = tk.Label(
            entry_frame,
            text="",
            fg="red",
            font=("Arial", 8),
            anchor="w"
        )
        self.error_label.pack(side="right", padx=(5, 0))
        
        # Bind validation events
        self.entry.bind("<FocusOut>", self.validate_on_focus_out)
        self.entry.bind("<KeyRelease>", self.validate_on_key_release)
    
    def get_value(self):
        """Get the current value"""
        return self.entry.get()
    
    def set_value(self, value):
        """Set the current value"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def validate(self):
        """Validate the current value"""
        value = self.get_value()
        
        for validator in self.validators:
            is_valid, error_message = validator.validate(value)
            if not is_valid:
                self.show_error(error_message)
                return False
        
        self.clear_error()
        return True
    
    def validate_on_focus_out(self, event=None):
        """Validate when focus leaves the entry"""
        self.validate()
    
    def validate_on_key_release(self, event=None):
        """Validate on key release (for real-time validation)"""
        # Only clear error on key release, don't show new errors
        if self.error_label.cget("text"):
            self.clear_error()
    
    def show_error(self, message):
        """Show error message"""
        self.error_label.configure(text=message)
        self.entry.configure(bg="#FFE6E6")  # Light red background
    
    def clear_error(self):
        """Clear error message"""
        self.error_label.configure(text="")
        self.entry.configure(bg="white")

class SearchFilterFrame(tk.Frame):
    """Search and filter interface"""
    
    def __init__(self, parent, search_callback=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.search_callback = search_callback
        self.create_widgets()
    
    def create_widgets(self):
        """Create the search and filter interface"""
        # Search frame
        search_frame = tk.LabelFrame(self, text="Search & Filter", font=("Arial", 10, "bold"))
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search entry
        tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Filter options
        tk.Label(search_frame, text="Filter by:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(search_frame, textvariable=self.filter_var, 
                                   values=["all", "active", "inactive"], width=15)
        filter_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Search button
        search_btn = tk.Button(search_frame, text="Search", command=self.perform_search, width=10)
        search_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Clear button
        clear_btn = tk.Button(search_frame, text="Clear", command=self.clear_search, width=10)
        clear_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Configure grid weights
        search_frame.columnconfigure(1, weight=1)
    
    def perform_search(self):
        """Perform the search operation"""
        if self.search_callback:
            search_term = self.search_var.get().strip()
            filter_value = self.filter_var.get()
            self.search_callback(search_term, filter_value)
    
    def clear_search(self):
        """Clear search and filter"""
        self.search_var.set("")
        self.filter_var.set("all")
        if self.search_callback:
            self.search_callback("", "all")

# =============================================================================
# CRUD OPERATIONS DEMO
# =============================================================================

class CRUDOperationsDemo:
    """Demo application showing advanced CRUD operations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced CRUD Operations Demo")
        self.root.geometry("1200x800")
        
        self.db_manager = DatabaseManager()
        self.current_record = None
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create the main application interface"""
        # Title
        title_label = tk.Label(
            self.root,
            text="Advanced CRUD Operations Demo",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Form
        left_panel = tk.LabelFrame(content_frame, text="Data Entry Form", font=("Arial", 12, "bold"))
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        # Create form
        self.create_form(left_panel)
        
        # Right panel - Data display
        right_panel = tk.Frame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Search and filter
        self.search_filter = SearchFilterFrame(right_panel, self.perform_search)
        self.search_filter.pack(fill="x", pady=(0, 10))
        
        # Data table
        self.create_data_table(right_panel)
    
    def create_form(self, parent):
        """Create the data entry form"""
        # Form fields
        form_frame = tk.Frame(parent)
        form_frame.pack(fill="x", padx=10, pady=10)
        
        # Username field
        self.username_field = ValidatedEntry(
            form_frame,
            label="Username *",
            validators=[RequiredValidator()]
        )
        self.username_field.pack(fill="x", pady=5)
        
        # Email field
        self.email_field = ValidatedEntry(
            form_frame,
            label="Email *",
            validators=[RequiredValidator(), EmailValidator()]
        )
        self.email_field.pack(fill="x", pady=5)
        
        # Full name field
        self.fullname_field = ValidatedEntry(
            form_frame,
            label="Full Name *",
            validators=[RequiredValidator()]
        )
        self.fullname_field.pack(fill="x", pady=5)
        
        # Role selection
        role_frame = tk.Frame(form_frame)
        role_frame.pack(fill="x", pady=5)
        
        tk.Label(role_frame, text="Role *").pack(anchor="w")
        self.role_var = tk.StringVar(value="user")
        role_combo = ttk.Combobox(role_frame, textvariable=self.role_var, 
                                 values=["user", "admin", "manager"], state="readonly")
        role_combo.pack(fill="x", pady=2)
        
        # Active status
        status_frame = tk.Frame(form_frame)
        status_frame.pack(fill="x", pady=5)
        
        self.active_var = tk.BooleanVar(value=True)
        active_check = tk.Checkbutton(status_frame, text="Active", variable=self.active_var)
        active_check.pack(anchor="w")
        
        # Buttons frame
        button_frame = tk.Frame(form_frame)
        button_frame.pack(fill="x", pady=20)
        
        # Create button
        self.create_btn = tk.Button(
            button_frame,
            text="Create User",
            command=self.create_user,
            bg="#2ECC71",
            fg="white",
            width=12
        )
        self.create_btn.pack(side="left", padx=5)
        
        # Update button
        self.update_btn = tk.Button(
            button_frame,
            text="Update User",
            command=self.update_user,
            bg="#3498DB",
            fg="white",
            width=12,
            state="disabled"
        )
        self.update_btn.pack(side="left", padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            width=12
        )
        clear_btn.pack(side="left", padx=5)
    
    def create_data_table(self, parent):
        """Create the data display table"""
        # Control frame
        control_frame = tk.Frame(parent)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready", anchor="w")
        self.status_label.pack(side="left")
        
        # Action buttons
        tk.Button(control_frame, text="Refresh", command=self.load_data).pack(side="right", padx=5)
        tk.Button(control_frame, text="Delete Selected", command=self.delete_selected).pack(side="right", padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill="both", expand=True)
        
        # Create Treeview
        columns = ("ID", "Username", "Email", "Full Name", "Role", "Active", "Created", "Last Login")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=120)
        
        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_record_select)
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack widgets
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
    
    def create_user(self):
        """Create a new user"""
        if not self.validate_form():
            return
        
        try:
            user_data = {
                'username': self.username_field.get_value(),
                'email': self.email_field.get_value(),
                'full_name': self.fullname_field.get_value(),
                'role': self.role_var.get(),
                'is_active': 1 if self.active_var.get() else 0
            }
            
            self.db_manager.insert_record('users', user_data)
            self.load_data()
            self.clear_form()
            self.status_label.config(text="User created successfully")
            messagebox.showinfo("Success", "User created successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create user: {e}")
    
    def update_user(self):
        """Update the selected user"""
        if not self.current_record:
            messagebox.showwarning("Warning", "Please select a user to update")
            return
        
        if not self.validate_form():
            return
        
        try:
            user_data = {
                'username': self.username_field.get_value(),
                'email': self.email_field.get_value(),
                'full_name': self.fullname_field.get_value(),
                'role': self.role_var.get(),
                'is_active': 1 if self.active_var.get() else 0
            }
            
            self.db_manager.update_record('users', user_data, {'id': self.current_record['id']})
            self.load_data()
            self.clear_form()
            self.current_record = None
            self.update_btn.config(state="disabled")
            self.create_btn.config(state="normal")
            self.status_label.config(text="User updated successfully")
            messagebox.showinfo("Success", "User updated successfully")
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user: {e}")
    
    def delete_selected(self):
        """Delete the selected user"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            try:
                item = self.tree.item(selected[0])
                user_id = item['values'][0]
                
                self.db_manager.delete_record('users', {'id': user_id})
                self.load_data()
                self.clear_form()
                self.current_record = None
                self.update_btn.config(state="disabled")
                self.create_btn.config(state="normal")
                self.status_label.config(text="User deleted successfully")
                messagebox.showinfo("Success", "User deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {e}")
    
    def validate_form(self):
        """Validate all form fields"""
        fields = [self.username_field, self.email_field, self.fullname_field]
        
        for field in fields:
            if not field.validate():
                return False
        
        return True
    
    def clear_form(self):
        """Clear all form fields"""
        self.username_field.set_value("")
        self.email_field.set_value("")
        self.fullname_field.set_value("")
        self.role_var.set("user")
        self.active_var.set(True)
        
        self.current_record = None
        self.update_btn.config(state="disabled")
        self.create_btn.config(state="normal")
    
    def load_data(self, search_term="", filter_value="all"):
        """Load and display users with search and filter"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Build query
            query = "SELECT * FROM users"
            conditions = []
            parameters = []
            
            if search_term:
                conditions.append("(username LIKE ? OR email LIKE ? OR full_name LIKE ?)")
                search_pattern = f"%{search_term}%"
                parameters.extend([search_pattern, search_pattern, search_pattern])
            
            if filter_value == "active":
                conditions.append("is_active = 1")
            elif filter_value == "inactive":
                conditions.append("is_active = 0")
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY created_date DESC"
            
            # Execute query
            cursor = self.db_manager.execute_query(query, parameters)
            users = cursor.fetchall()
            
            # Display results
            for user in users:
                self.tree.insert("", "end", values=(
                    user['id'],
                    user['username'],
                    user['email'],
                    user['full_name'],
                    user['role'],
                    "Yes" if user['is_active'] else "No",
                    user['created_date'],
                    user['last_login'] or "Never"
                ))
            
            self.status_label.config(text=f"Loaded {len(users)} users")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
    
    def perform_search(self, search_term, filter_value):
        """Perform search and filter operation"""
        self.load_data(search_term, filter_value)
    
    def on_record_select(self, event):
        """Handle record selection"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Store current record
            self.current_record = {
                'id': values[0],
                'username': values[1],
                'email': values[2],
                'full_name': values[3],
                'role': values[4],
                'is_active': values[5] == "Yes"
            }
            
            # Update form
            self.username_field.set_value(self.current_record['username'])
            self.email_field.set_value(self.current_record['email'])
            self.fullname_field.set_value(self.current_record['full_name'])
            self.role_var.set(self.current_record['role'])
            self.active_var.set(self.current_record['is_active'])
            
            # Update buttons
            self.create_btn.config(state="disabled")
            self.update_btn.config(state="normal")
    
    def on_double_click(self, event):
        """Handle double-click on record"""
        self.on_record_select(event)
    
    def sort_by_column(self, column):
        """Sort data by column"""
        # This is a simplified implementation
        # In a real application, you would implement proper sorting
        self.load_data()

# =============================================================================
# DATABASE MANAGER (Reused from basic_database.py)
# =============================================================================

class DatabaseManager:
    """Manages SQLite database connections and operations"""
    
    def __init__(self, db_path="dashboard.db"):
        self.db_path = db_path
        self.connection = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect: {e}")
    
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
            
            self.connection.commit()
            
        except sqlite3.Error as e:
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
            raise e
    
    def insert_record(self, table, data):
        """Insert a record into the specified table"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            cursor = self.execute_query(query, list(data.values()))
            self.connection.commit()
            
            return cursor.lastrowid
            
        except sqlite3.Error as e:
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
            
            return cursor.rowcount
            
        except sqlite3.Error as e:
            raise e
    
    def delete_record(self, table, conditions):
        """Delete records from the specified table"""
        try:
            where_clause = ' AND '.join([f"{k} = ?" for k in conditions.keys()])
            query = f"DELETE FROM {table} WHERE {where_clause}"
            
            cursor = self.execute_query(query, list(conditions.values()))
            self.connection.commit()
            
            return cursor.rowcount
            
        except sqlite3.Error as e:
            raise e

# =============================================================================
# MAIN APPLICATION
# =============================================================================

class CRUDOperationsApp:
    """Main application for CRUD operations"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced CRUD Operations")
        self.root.geometry("1200x800")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Create demo
        self.demo = CRUDOperationsDemo(self.root)
    
    def on_closing(self):
        """Handle application closing"""
        if hasattr(self.demo, 'db_manager'):
            self.demo.db_manager.connection.close()
        self.root.destroy()

def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the CRUD operations app
    app = CRUDOperationsApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()

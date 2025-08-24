# Chapter 7: Database Integration - Exercises

## Exercise 1: Basic Database Operations

**Objective**: Create a simple contact management system with basic CRUD operations.

**Requirements**:
- Create a contacts table with fields: id, name, email, phone, created_date
- Implement add, view, edit, and delete operations
- Display contacts in a Treeview
- Add form validation

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("600x400")
        
        # Database setup
        self.db_path = "contacts.db"
        self.connection = None
        self.setup_database()
        
        # Create UI
        self.create_widgets()
        self.load_contacts()
    
    def setup_database(self):
        """Initialize database and create tables"""
        # TODO: Implement database connection and table creation
        pass
    
    def create_widgets(self):
        """Create the user interface"""
        # TODO: Create form and table widgets
        pass
    
    def load_contacts(self):
        """Load and display all contacts"""
        # TODO: Implement contact loading
        pass
    
    def add_contact(self):
        """Add a new contact"""
        # TODO: Implement contact addition with validation
        pass
    
    def edit_contact(self, event):
        """Edit selected contact"""
        # TODO: Implement contact editing
        pass
    
    def delete_contact(self):
        """Delete selected contact"""
        # TODO: Implement contact deletion
        pass

def main():
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Functional contact management system
- Form validation for required fields
- Double-click to edit contacts
- Confirmation dialog for deletion
- Real-time updates to the contact list

## Exercise 2: Advanced Database Dashboard

**Objective**: Build a multi-table dashboard with relationships and analytics.

**Requirements**:
- Create tables for: customers, products, orders, order_items
- Implement foreign key relationships
- Add search and filtering capabilities
- Create summary statistics
- Export data to CSV

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime

class SalesDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Dashboard")
        self.root.geometry("1000x700")
        
        # Database setup
        self.db_path = "sales.db"
        self.connection = None
        self.setup_database()
        
        # Create interface
        self.create_widgets()
        self.load_data()
    
    def setup_database(self):
        """Create database schema with relationships"""
        # TODO: Create tables with proper relationships
        pass
    
    def create_widgets(self):
        """Create tabbed interface"""
        # TODO: Create notebook with multiple tabs
        pass
    
    def load_data(self):
        """Load all data from database"""
        # TODO: Implement data loading for all tables
        pass
    
    def search_records(self):
        """Search functionality"""
        # TODO: Implement search across multiple fields
        pass
    
    def export_to_csv(self):
        """Export data to CSV file"""
        # TODO: Implement CSV export functionality
        pass
    
    def show_statistics(self):
        """Display summary statistics"""
        # TODO: Calculate and display key metrics
        pass

def main():
    root = tk.Tk()
    app = SalesDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Multi-table database with proper relationships
- Search and filter functionality
- Summary statistics dashboard
- CSV export capability
- Professional tabbed interface

## Exercise 3: Data Validation and Error Handling

**Objective**: Implement robust data validation and comprehensive error handling.

**Requirements**:
- Create custom validators for different data types
- Implement comprehensive error handling
- Add data integrity checks
- Create user-friendly error messages
- Add logging functionality

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import logging
from datetime import datetime
import re

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class DataValidator:
    """Custom data validation class"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        # TODO: Implement email validation
        pass
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number format"""
        # TODO: Implement phone validation
        pass
    
    @staticmethod
    def validate_date(date_str):
        """Validate date format"""
        # TODO: Implement date validation
        pass

class RobustDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Robust Database Application")
        self.root.geometry("800x600")
        
        # Setup logging
        self.setup_logging()
        
        # Database setup
        self.db_path = "robust_app.db"
        self.connection = None
        self.setup_database()
        
        # Create interface
        self.create_widgets()
    
    def setup_logging(self):
        """Setup logging configuration"""
        # TODO: Configure logging
        pass
    
    def setup_database(self):
        """Setup database with error handling"""
        # TODO: Implement robust database setup
        pass
    
    def create_widgets(self):
        """Create user interface with validation"""
        # TODO: Create validated form widgets
        pass
    
    def validate_and_save(self):
        """Validate data and save to database"""
        # TODO: Implement comprehensive validation
        pass
    
    def handle_database_error(self, error):
        """Handle database errors gracefully"""
        # TODO: Implement error handling
        pass

def main():
    root = tk.Tk()
    app = RobustDatabaseApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Comprehensive data validation
- Professional error handling
- Detailed logging
- User-friendly error messages
- Data integrity maintenance

## Bonus Challenge: Real-Time Database Monitoring

**Objective**: Create a real-time database monitoring system with live updates.

**Requirements**:
- Monitor database changes in real-time
- Display live statistics and metrics
- Implement database backup functionality
- Add performance monitoring
- Create alert system for critical events

**Advanced Features**:
- Real-time data visualization
- Database performance metrics
- Automated backup scheduling
- Email/SMS alerts for critical events
- Database optimization recommendations

## Solutions

### Exercise 1 Solution
```python
# Contact Manager Implementation
def setup_database(self):
    try:
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                phone TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to setup database: {e}")

def add_contact(self):
    name = self.name_entry.get().strip()
    email = self.email_entry.get().strip()
    phone = self.phone_entry.get().strip()
    
    if not name:
        messagebox.showwarning("Validation Error", "Name is required")
        return
    
    try:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
                      (name, email, phone))
        self.connection.commit()
        self.load_contacts()
        self.clear_form()
        messagebox.showinfo("Success", "Contact added successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to add contact: {e}")
```

### Exercise 2 Solution
```python
# Sales Dashboard Implementation
def setup_database(self):
    try:
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        cursor = self.connection.cursor()
        
        # Create tables with relationships
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        """)
        
        self.connection.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to setup database: {e}")

def export_to_csv(self):
    try:
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT c.name as customer, p.name as product, 
                       oi.quantity, oi.price, o.order_date
                FROM order_items oi
                JOIN orders o ON oi.order_id = o.id
                JOIN customers c ON o.customer_id = c.id
                JOIN products p ON oi.product_id = p.id
                ORDER BY o.order_date DESC
            """)
            
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Customer', 'Product', 'Quantity', 'Price', 'Date'])
                writer.writerows(cursor.fetchall())
            
            messagebox.showinfo("Success", f"Data exported to {filename}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data: {e}")
```

### Exercise 3 Solution
```python
# Data Validation Implementation
class DataValidator:
    @staticmethod
    def validate_email(email):
        if not email:
            return True  # Optional field
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        return True
    
    @staticmethod
    def validate_phone(phone):
        if not phone:
            return True  # Optional field
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, phone):
            raise ValidationError("Invalid phone number format")
        return True
    
    @staticmethod
    def validate_date(date_str):
        if not date_str:
            return True  # Optional field
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            raise ValidationError("Invalid date format (YYYY-MM-DD)")

def validate_and_save(self):
    try:
        # Get form data
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        birth_date = self.date_entry.get().strip()
        
        # Validate data
        if not name:
            raise ValidationError("Name is required")
        
        DataValidator.validate_email(email)
        DataValidator.validate_phone(phone)
        DataValidator.validate_date(birth_date)
        
        # Save to database
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, phone, birth_date) 
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, birth_date))
        self.connection.commit()
        
        self.logger.info(f"User added successfully: {name}")
        messagebox.showinfo("Success", "User added successfully")
        self.clear_form()
        
    except ValidationError as e:
        messagebox.showerror("Validation Error", str(e))
        self.logger.warning(f"Validation error: {e}")
    except sqlite3.IntegrityError as e:
        messagebox.showerror("Database Error", "Email already exists")
        self.logger.error(f"Integrity error: {e}")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to save data: {e}")
        self.logger.error(f"Database error: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")
        self.logger.error(f"Unexpected error: {e}")
```

## Learning Objectives

After completing these exercises, you should be able to:

1. **Database Design**: Design and implement multi-table databases with proper relationships
2. **CRUD Operations**: Implement comprehensive Create, Read, Update, Delete operations
3. **Data Validation**: Create robust validation systems for different data types
4. **Error Handling**: Implement professional error handling and user feedback
5. **User Interface**: Build intuitive database management interfaces
6. **Data Export**: Implement data export functionality (CSV, etc.)
7. **Performance**: Optimize database queries and application performance
8. **Security**: Implement basic database security measures

## Next Steps

- Practice with larger datasets
- Implement more complex relationships
- Add user authentication and authorization
- Explore other database systems (PostgreSQL, MySQL)
- Learn about database migration and versioning
- Study database optimization techniques

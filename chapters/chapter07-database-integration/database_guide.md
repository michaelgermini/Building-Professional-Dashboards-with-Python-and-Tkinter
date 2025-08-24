# Database Integration Guide - Chapter 7

## Table of Contents

1. [Database Design Principles](#database-design-principles)
2. [SQLite Best Practices](#sqlite-best-practices)
3. [Connection Management](#connection-management)
4. [Data Validation Patterns](#data-validation-patterns)
5. [Error Handling Strategies](#error-handling-strategies)
6. [Performance Optimization](#performance-optimization)
7. [Security Considerations](#security-considerations)
8. [Testing Database Applications](#testing-database-applications)
9. [Migration and Versioning](#migration-and-versioning)
10. [Advanced Patterns](#advanced-patterns)

## Database Design Principles

### 1. Normalization

**First Normal Form (1NF)**
- Each column contains atomic values
- No repeating groups or arrays
- Each row is unique

```sql
-- Bad: Repeating groups
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phones TEXT  -- "555-1234, 555-5678"
);

-- Good: Normalized
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_phones (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    phone TEXT,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

**Second Normal Form (2NF)**
- 1NF + no partial dependencies
- All non-key attributes depend on the entire primary key

**Third Normal Form (3NF)**
- 2NF + no transitive dependencies
- Non-key attributes don't depend on other non-key attributes

### 2. Relationships

**One-to-Many**
```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments (id)
);
```

**Many-to-Many**
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE enrollments (
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (course_id) REFERENCES courses (id)
);
```

### 3. Indexing Strategy

```sql
-- Primary key (automatically indexed)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,  -- Indexed automatically
    email TEXT UNIQUE,       -- Indexed automatically
    name TEXT,
    created_date TIMESTAMP
);

-- Custom indexes for performance
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_created ON users(created_date);
CREATE INDEX idx_users_email_name ON users(email, name);  -- Composite index
```

## SQLite Best Practices

### 1. Connection Management

```python
import sqlite3
import threading
from contextlib import contextmanager

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._local = threading.local()
    
    @contextmanager
    def get_connection(self):
        """Thread-safe connection management"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = sqlite3.connect(self.db_path)
            self._local.connection.row_factory = sqlite3.Row
        
        try:
            yield self._local.connection
        except Exception:
            self._local.connection.rollback()
            raise
        finally:
            # Don't close connection here - reuse for thread
            pass
    
    def close_all_connections(self):
        """Close all thread connections"""
        if hasattr(self._local, 'connection'):
            self._local.connection.close()
            del self._local.connection

# Usage
db_manager = DatabaseManager("app.db")

def save_user(name, email):
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
```

### 2. Prepared Statements

```python
# Good: Use parameterized queries
def add_user(name, email, age):
    cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", 
                  (name, email, age))

# Bad: String formatting (SQL injection risk)
def add_user_bad(name, email, age):
    cursor.execute(f"INSERT INTO users (name, email, age) VALUES ('{name}', '{email}', {age})")
```

### 3. Transaction Management

```python
def transfer_money(from_account, to_account, amount):
    with db_manager.get_connection() as conn:
        try:
            cursor = conn.cursor()
            
            # Check balance
            cursor.execute("SELECT balance FROM accounts WHERE id = ?", (from_account,))
            current_balance = cursor.fetchone()['balance']
            
            if current_balance < amount:
                raise ValueError("Insufficient funds")
            
            # Deduct from source
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", 
                         (amount, from_account))
            
            # Add to destination
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                         (amount, to_account))
            
            conn.commit()
            
        except Exception:
            conn.rollback()
            raise
```

## Data Validation Patterns

### 1. Validation Framework

```python
from abc import ABC, abstractmethod
import re
from datetime import datetime

class Validator(ABC):
    @abstractmethod
    def validate(self, value):
        pass
    
    @abstractmethod
    def get_error_message(self):
        pass

class RequiredValidator(Validator):
    def validate(self, value):
        return value is not None and str(value).strip() != ""
    
    def get_error_message(self):
        return "This field is required"

class EmailValidator(Validator):
    def __init__(self, required=True):
        self.required = required
        self.pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def validate(self, value):
        if not value and not self.required:
            return True
        return bool(re.match(self.pattern, str(value)))
    
    def get_error_message(self):
        return "Invalid email format"

class NumberValidator(Validator):
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
    
    def validate(self, value):
        try:
            num = float(value)
            if self.min_value is not None and num < self.min_value:
                return False
            if self.max_value is not None and num > self.max_value:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    def get_error_message(self):
        if self.min_value is not None and self.max_value is not None:
            return f"Value must be between {self.min_value} and {self.max_value}"
        elif self.min_value is not None:
            return f"Value must be at least {self.min_value}"
        elif self.max_value is not None:
            return f"Value must be at most {self.max_value}"
        return "Invalid number format"

class ValidationManager:
    def __init__(self):
        self.validators = {}
    
    def add_validator(self, field_name, validator):
        if field_name not in self.validators:
            self.validators[field_name] = []
        self.validators[field_name].append(validator)
    
    def validate_field(self, field_name, value):
        if field_name not in self.validators:
            return True, None
        
        for validator in self.validators[field_name]:
            if not validator.validate(value):
                return False, validator.get_error_message()
        
        return True, None
    
    def validate_form(self, form_data):
        errors = {}
        for field_name, value in form_data.items():
            is_valid, error_message = self.validate_field(field_name, value)
            if not is_valid:
                errors[field_name] = error_message
        
        return len(errors) == 0, errors
```

### 2. Form Validation Integration

```python
class ValidatedEntry(ttk.Entry):
    def __init__(self, parent, validators=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.validators = validators or []
        self.error_label = None
        self.bind('<FocusOut>', self.validate)
        self.bind('<KeyRelease>', self.clear_error)
    
    def set_error_label(self, label):
        self.error_label = label
    
    def validate(self, event=None):
        value = self.get()
        for validator in self.validators:
            if not validator.validate(value):
                self.show_error(validator.get_error_message())
                return False
        
        self.clear_error()
        return True
    
    def show_error(self, message):
        if self.error_label:
            self.error_label.config(text=message, foreground="red")
        self.config(style="Error.TEntry")
    
    def clear_error(self, event=None):
        if self.error_label:
            self.error_label.config(text="")
        self.config(style="TEntry")
```

## Error Handling Strategies

### 1. Database Error Handling

```python
import logging
from sqlite3 import Error as SQLiteError, IntegrityError

class DatabaseErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error, operation="database operation"):
        """Centralized error handling"""
        if isinstance(error, IntegrityError):
            if "UNIQUE constraint failed" in str(error):
                return "A record with this information already exists"
            elif "NOT NULL constraint failed" in str(error):
                return "Required field is missing"
            else:
                return "Data integrity error occurred"
        
        elif isinstance(error, SQLiteError):
            self.logger.error(f"SQLite error during {operation}: {error}")
            return "Database error occurred"
        
        else:
            self.logger.error(f"Unexpected error during {operation}: {error}")
            return "An unexpected error occurred"
    
    def execute_with_error_handling(self, operation_func, *args, **kwargs):
        """Execute database operation with error handling"""
        try:
            return operation_func(*args, **kwargs)
        except Exception as e:
            error_message = self.handle_error(e, operation_func.__name__)
            raise DatabaseOperationError(error_message) from e

class DatabaseOperationError(Exception):
    """Custom exception for database operations"""
    pass
```

### 2. User-Friendly Error Messages

```python
def save_user_with_feedback(name, email, age):
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", 
                         (name, email, age))
            conn.commit()
        
        messagebox.showinfo("Success", "User saved successfully")
        
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            messagebox.showerror("Error", "A user with this email already exists")
        else:
            messagebox.showerror("Error", "Data integrity error")
    
    except SQLiteError as e:
        messagebox.showerror("Database Error", "Failed to save user to database")
        logging.error(f"Database error: {e}")
    
    except Exception as e:
        messagebox.showerror("Error", "An unexpected error occurred")
        logging.error(f"Unexpected error: {e}")
```

## Performance Optimization

### 1. Query Optimization

```python
# Bad: N+1 query problem
def get_users_with_orders_bad():
    users = cursor.execute("SELECT * FROM users").fetchall()
    for user in users:
        orders = cursor.execute("SELECT * FROM orders WHERE user_id = ?", 
                              (user['id'],)).fetchall()
        user['orders'] = orders

# Good: Single query with JOIN
def get_users_with_orders_good():
    query = """
        SELECT u.*, o.id as order_id, o.total_amount, o.order_date
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        ORDER BY u.id, o.order_date DESC
    """
    return cursor.execute(query).fetchall()
```

### 2. Batch Operations

```python
def insert_multiple_users(users_data):
    """Insert multiple users efficiently"""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Use executemany for batch inserts
        cursor.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            users_data
        )
        conn.commit()

# Usage
users_data = [
    ("John Doe", "john@example.com", 30),
    ("Jane Smith", "jane@example.com", 25),
    ("Bob Johnson", "bob@example.com", 35)
]
insert_multiple_users(users_data)
```

### 3. Connection Pooling

```python
import queue
import threading

class ConnectionPool:
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = queue.Queue(maxsize=max_connections)
        self.lock = threading.Lock()
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            return self.connections.get_nowait()
        except queue.Empty:
            return sqlite3.connect(self.db_path)
    
    def return_connection(self, connection):
        """Return a connection to the pool"""
        try:
            self.connections.put_nowait(connection)
        except queue.Full:
            connection.close()
    
    def close_all(self):
        """Close all connections in the pool"""
        while not self.connections.empty():
            conn = self.connections.get()
            conn.close()
```

## Security Considerations

### 1. SQL Injection Prevention

```python
# Always use parameterized queries
def search_users_safe(search_term):
    query = "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?"
    search_pattern = f"%{search_term}%"
    return cursor.execute(query, (search_pattern, search_pattern)).fetchall()

# Never use string formatting
def search_users_unsafe(search_term):
    query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
    return cursor.execute(query).fetchall()  # Vulnerable to SQL injection
```

### 2. Input Sanitization

```python
import html
import re

class InputSanitizer:
    @staticmethod
    def sanitize_text(text):
        """Sanitize text input"""
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Escape HTML entities
        text = html.escape(text)
        
        # Remove control characters
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    @staticmethod
    def validate_filename(filename):
        """Validate filename for security"""
        # Remove path traversal attempts
        filename = os.path.basename(filename)
        
        # Allow only safe characters
        if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
            raise ValueError("Invalid filename")
        
        return filename
```

### 3. Access Control

```python
class DatabaseAccessControl:
    def __init__(self):
        self.current_user = None
        self.user_permissions = {}
    
    def set_current_user(self, user_id):
        """Set current user and load permissions"""
        self.current_user = user_id
        self.load_user_permissions(user_id)
    
    def can_read_table(self, table_name):
        """Check if user can read from table"""
        return self.user_permissions.get(f"read_{table_name}", False)
    
    def can_write_table(self, table_name):
        """Check if user can write to table"""
        return self.user_permissions.get(f"write_{table_name}", False)
    
    def enforce_read_permission(self, table_name):
        """Enforce read permission"""
        if not self.can_read_table(table_name):
            raise PermissionError(f"Access denied to read {table_name}")
    
    def enforce_write_permission(self, table_name):
        """Enforce write permission"""
        if not self.can_write_table(table_name):
            raise PermissionError(f"Access denied to write {table_name}")
```

## Testing Database Applications

### 1. Unit Testing

```python
import unittest
import tempfile
import os

class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.db_manager = DatabaseManager(self.db_path)
        self.setup_test_data()
    
    def tearDown(self):
        """Clean up test database"""
        self.temp_db.close()
        os.unlink(self.db_path)
    
    def setup_test_data(self):
        """Create test data"""
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE
                )
            """)
            conn.commit()
    
    def test_add_user(self):
        """Test adding a user"""
        add_user("Test User", "test@example.com")
        
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute("SELECT * FROM users WHERE email = ?", 
                                ("test@example.com",)).fetchone()
            
            self.assertIsNotNone(user)
            self.assertEqual(user['name'], "Test User")
    
    def test_duplicate_email(self):
        """Test duplicate email handling"""
        add_user("User 1", "test@example.com")
        
        with self.assertRaises(IntegrityError):
            add_user("User 2", "test@example.com")

if __name__ == '__main__':
    unittest.main()
```

### 2. Integration Testing

```python
class TestDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        """Set up integration test environment"""
        self.app = tk.Tk()
        self.app.withdraw()  # Hide window during tests
        self.db_app = DatabaseApp(self.app)
    
    def tearDown(self):
        """Clean up integration test environment"""
        self.app.destroy()
    
    def test_full_user_workflow(self):
        """Test complete user management workflow"""
        # Add user
        self.db_app.add_user("Test User", "test@example.com")
        
        # Verify user appears in list
        users = self.db_app.get_all_users()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], "Test User")
        
        # Edit user
        user_id = users[0]['id']
        self.db_app.edit_user(user_id, "Updated User", "updated@example.com")
        
        # Verify changes
        updated_user = self.db_app.get_user(user_id)
        self.assertEqual(updated_user['name'], "Updated User")
        
        # Delete user
        self.db_app.delete_user(user_id)
        
        # Verify deletion
        users = self.db_app.get_all_users()
        self.assertEqual(len(users), 0)
```

## Migration and Versioning

### 1. Database Schema Versioning

```python
class DatabaseMigrator:
    def __init__(self, db_path):
        self.db_path = db_path
        self.migrations = []
        self.setup_migrations()
    
    def setup_migrations(self):
        """Define all database migrations"""
        self.migrations = [
            Migration(1, "Create users table", self.migration_001),
            Migration(2, "Add email index", self.migration_002),
            Migration(3, "Add user roles", self.migration_003),
        ]
    
    def get_current_version(self):
        """Get current database version"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY
                )
            """)
            
            result = cursor.execute("SELECT version FROM schema_version").fetchone()
            return result[0] if result else 0
    
    def set_version(self, version):
        """Set database version"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM schema_version")
            cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))
            conn.commit()
    
    def migrate(self):
        """Run all pending migrations"""
        current_version = self.get_current_version()
        
        for migration in self.migrations:
            if migration.version > current_version:
                print(f"Running migration {migration.version}: {migration.description}")
                migration.execute(self.db_path)
                self.set_version(migration.version)
    
    def migration_001(self, db_path):
        """Create users table"""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def migration_002(self, db_path):
        """Add email index"""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE INDEX idx_users_email ON users(email)")
            conn.commit()
    
    def migration_003(self, db_path):
        """Add user roles"""
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user'")
            conn.commit()

class Migration:
    def __init__(self, version, description, execute_func):
        self.version = version
        self.description = description
        self.execute_func = execute_func
    
    def execute(self, db_path):
        self.execute_func(db_path)
```

### 2. Data Migration

```python
class DataMigrator:
    def __init__(self, source_db, target_db):
        self.source_db = source_db
        self.target_db = target_db
    
    def migrate_users(self):
        """Migrate user data between databases"""
        with sqlite3.connect(self.source_db) as source_conn:
            with sqlite3.connect(self.target_db) as target_conn:
                source_cursor = source_conn.cursor()
                target_cursor = target_conn.cursor()
                
                # Read from source
                users = source_cursor.execute("SELECT * FROM users").fetchall()
                
                # Write to target
                for user in users:
                    target_cursor.execute("""
                        INSERT INTO users (name, email, created_date) 
                        VALUES (?, ?, ?)
                    """, (user['name'], user['email'], user['created_date']))
                
                target_conn.commit()
```

## Advanced Patterns

### 1. Repository Pattern

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class UserRepository(ABC):
    @abstractmethod
    def create(self, user_data: Dict[str, Any]) -> int:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def update(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def create(self, user_data: Dict[str, Any]) -> int:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, role) VALUES (?, ?, ?)
            """, (user_data['name'], user_data['email'], user_data.get('role', 'user')))
            conn.commit()
            return cursor.lastrowid
    
    def get_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            user = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
    
    def get_all(self) -> List[Dict[str, Any]]:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            users = cursor.execute("SELECT * FROM users ORDER BY created_date DESC").fetchall()
            return [dict(user) for user in users]
    
    def update(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?
            """, (user_data['name'], user_data['email'], user_data.get('role', 'user'), user_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete(self, user_id: int) -> bool:
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
```

### 2. Unit of Work Pattern

```python
class UnitOfWork:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.operations = []
    
    def add_operation(self, operation):
        """Add operation to be executed"""
        self.operations.append(operation)
    
    def commit(self):
        """Execute all operations in a transaction"""
        with self.db_manager.get_connection() as conn:
            try:
                for operation in self.operations:
                    operation.execute(conn)
                conn.commit()
                self.operations.clear()
            except Exception:
                conn.rollback()
                raise

class CreateUserOperation:
    def __init__(self, user_data):
        self.user_data = user_data
    
    def execute(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (name, email, role) VALUES (?, ?, ?)
        """, (self.user_data['name'], self.user_data['email'], self.user_data.get('role', 'user')))

class UpdateUserOperation:
    def __init__(self, user_id, user_data):
        self.user_id = user_id
        self.user_data = user_data
    
    def execute(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?
        """, (self.user_data['name'], self.user_data['email'], self.user_data.get('role', 'user'), self.user_id))

# Usage
uow = UnitOfWork(db_manager)
uow.add_operation(CreateUserOperation({"name": "John", "email": "john@example.com"}))
uow.add_operation(UpdateUserOperation(1, {"name": "Jane", "email": "jane@example.com"}))
uow.commit()
```

### 3. Observer Pattern for Database Changes

```python
from abc import ABC, abstractmethod
from typing import List

class DatabaseObserver(ABC):
    @abstractmethod
    def on_record_created(self, table_name: str, record_id: int, data: Dict[str, Any]):
        pass
    
    @abstractmethod
    def on_record_updated(self, table_name: str, record_id: int, data: Dict[str, Any]):
        pass
    
    @abstractmethod
    def on_record_deleted(self, table_name: str, record_id: int):
        pass

class DatabaseSubject:
    def __init__(self):
        self.observers: List[DatabaseObserver] = []
    
    def add_observer(self, observer: DatabaseObserver):
        self.observers.append(observer)
    
    def remove_observer(self, observer: DatabaseObserver):
        self.observers.remove(observer)
    
    def notify_created(self, table_name: str, record_id: int, data: Dict[str, Any]):
        for observer in self.observers:
            observer.on_record_created(table_name, record_id, data)
    
    def notify_updated(self, table_name: str, record_id: int, data: Dict[str, Any]):
        for observer in self.observers:
            observer.on_record_updated(table_name, record_id, data)
    
    def notify_deleted(self, table_name: str, record_id: int):
        for observer in self.observers:
            observer.on_record_deleted(table_name, record_id)

class AuditLogger(DatabaseObserver):
    def on_record_created(self, table_name: str, record_id: int, data: Dict[str, Any]):
        logging.info(f"Record created in {table_name}: ID {record_id}")
    
    def on_record_updated(self, table_name: str, record_id: int, data: Dict[str, Any]):
        logging.info(f"Record updated in {table_name}: ID {record_id}")
    
    def on_record_deleted(self, table_name: str, record_id: int):
        logging.info(f"Record deleted from {table_name}: ID {record_id}")

class CacheManager(DatabaseObserver):
    def __init__(self):
        self.cache = {}
    
    def on_record_created(self, table_name: str, record_id: int, data: Dict[str, Any]):
        self.cache[f"{table_name}:{record_id}"] = data
    
    def on_record_updated(self, table_name: str, record_id: int, data: Dict[str, Any]):
        self.cache[f"{table_name}:{record_id}"] = data
    
    def on_record_deleted(self, table_name: str, record_id: int):
        cache_key = f"{table_name}:{record_id}"
        if cache_key in self.cache:
            del self.cache[cache_key]
```

## Conclusion

This comprehensive guide covers the essential aspects of database integration in Tkinter applications. Key takeaways include:

1. **Design First**: Always design your database schema before implementation
2. **Security Matters**: Use parameterized queries and validate all inputs
3. **Error Handling**: Implement comprehensive error handling and user feedback
4. **Performance**: Optimize queries and use appropriate indexing
5. **Testing**: Write thorough tests for database operations
6. **Maintenance**: Plan for database migrations and versioning
7. **Patterns**: Use established patterns for maintainable code

Remember that database integration is a critical component of any application. Take the time to implement it correctly, and your Tkinter applications will be more robust, secure, and maintainable.

# Chapter 10: Complete Professional Dashboard - Exercises

## Exercise 1: Enhanced User Management System

### Objective
Extend the dashboard with a comprehensive user management system including user roles, permissions, and profile management.

### Requirements
- Create a new "User Management" page in the dashboard
- Implement user creation, editing, and deletion functionality
- Add role-based access control (RBAC)
- Include user profile management with avatar upload
- Add password reset functionality

### Starter Code
```python
class UserManagementSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.roles = {
            'admin': ['all'],
            'manager': ['view_dashboard', 'manage_sales', 'view_reports'],
            'sales': ['view_dashboard', 'add_sales', 'view_own_reports'],
            'analyst': ['view_dashboard', 'view_reports', 'export_data'],
            'viewer': ['view_dashboard']
        }
    
    def create_user(self, username, password, email, role):
        """Create a new user account"""
        # Implementation here
        pass
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        # Implementation here
        pass
    
    def delete_user(self, user_id):
        """Delete user account"""
        # Implementation here
        pass
    
    def check_permission(self, user_role, permission):
        """Check if user has specific permission"""
        # Implementation here
        pass
```

### Expected Results
- Complete user management interface with CRUD operations
- Role-based menu visibility and functionality
- User profile pages with editable information
- Secure password handling and validation

### Solution Hints
1. Create a new database table for user permissions
2. Implement a permission checking decorator
3. Use file dialogs for avatar upload
4. Add email validation for password reset

---

## Exercise 2: Advanced Analytics Dashboard

### Objective
Create an advanced analytics dashboard with interactive charts, filters, and drill-down capabilities.

### Requirements
- Implement multiple chart types (line, bar, pie, scatter, heatmap)
- Add interactive filtering by date range, region, product category
- Create drill-down functionality for detailed analysis
- Include trend analysis and forecasting
- Add export capabilities for charts and data

### Starter Code
```python
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime, timedelta

class AnalyticsDashboard:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.filters = {}
        self.charts = {}
    
    def create_sales_trend_chart(self, date_range=None):
        """Create sales trend line chart"""
        # Implementation here
        pass
    
    def create_regional_analysis(self, chart_type='bar'):
        """Create regional sales analysis chart"""
        # Implementation here
        pass
    
    def create_product_performance(self, metric='revenue'):
        """Create product performance comparison"""
        # Implementation here
        pass
    
    def apply_filters(self, **filters):
        """Apply filters to all charts"""
        # Implementation here
        pass
    
    def export_chart(self, chart_name, format='png'):
        """Export chart to file"""
        # Implementation here
        pass
```

### Expected Results
- Interactive dashboard with multiple chart types
- Real-time filtering and data updates
- Drill-down capabilities for detailed analysis
- Export functionality for reports and charts
- Responsive layout that adapts to different screen sizes

### Solution Hints
1. Use pandas for data manipulation and aggregation
2. Implement chart update callbacks for real-time updates
3. Create a filter manager to handle multiple filter types
4. Use matplotlib's animation features for dynamic charts

---

## Exercise 3: Real-Time Notifications and Alerts

### Objective
Implement a comprehensive notification system with real-time alerts, email notifications, and alert management.

### Requirements
- Create a notification center with different alert types
- Implement real-time alerts for sales thresholds, system issues
- Add email notification system for important events
- Create alert rules and thresholds management
- Include notification history and acknowledgment system

### Starter Code
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

class NotificationSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.alert_rules = {}
        self.notification_queue = []
        self.email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your-email@gmail.com',
            'password': 'your-app-password'
        }
    
    def add_alert_rule(self, rule_name, condition, threshold, action):
        """Add a new alert rule"""
        # Implementation here
        pass
    
    def check_alerts(self, data):
        """Check data against alert rules"""
        # Implementation here
        pass
    
    def send_notification(self, notification_type, message, recipients):
        """Send notification via different channels"""
        # Implementation here
        pass
    
    def send_email_alert(self, subject, message, recipients):
        """Send email notification"""
        # Implementation here
        pass
    
    def acknowledge_notification(self, notification_id):
        """Mark notification as acknowledged"""
        # Implementation here
        pass
```

### Expected Results
- Real-time notification center with different alert types
- Email notification system for critical alerts
- Configurable alert rules and thresholds
- Notification history and management interface
- Acknowledgment system for tracking alert responses

### Solution Hints
1. Use threading for background alert monitoring
2. Implement a notification queue for managing alerts
3. Create email templates for different notification types
4. Use database to store notification history and rules

---

## Exercise 4: Advanced Data Import/Export System

### Objective
Create a comprehensive data import/export system with support for multiple formats and data validation.

### Requirements
- Support multiple file formats (CSV, Excel, JSON, XML)
- Implement data validation and error handling
- Add bulk import/export functionality
- Create data mapping and transformation tools
- Include import/export scheduling and automation

### Starter Code
```python
import pandas as pd
import xml.etree.ElementTree as ET
import json
import csv
from datetime import datetime
import schedule
import time

class DataImportExportSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.supported_formats = ['csv', 'excel', 'json', 'xml']
        self.import_mappings = {}
        self.export_templates = {}
    
    def import_data(self, file_path, format_type, mapping=None):
        """Import data from file"""
        # Implementation here
        pass
    
    def export_data(self, data, format_type, template=None):
        """Export data to file"""
        # Implementation here
        pass
    
    def validate_data(self, data, schema):
        """Validate imported data against schema"""
        # Implementation here
        pass
    
    def create_mapping(self, source_fields, target_fields):
        """Create field mapping for import/export"""
        # Implementation here
        pass
    
    def schedule_export(self, schedule_config):
        """Schedule automated export"""
        # Implementation here
        pass
```

### Expected Results
- Multi-format import/export with validation
- Data mapping interface for field mapping
- Bulk import/export with progress tracking
- Scheduled import/export functionality
- Error handling and reporting system

### Solution Hints
1. Use pandas for Excel and CSV handling
2. Implement data validation schemas
3. Create progress bars for bulk operations
4. Use threading for background import/export operations

---

## Exercise 5: Advanced Security and Audit System

### Objective
Implement comprehensive security features including audit logging, session management, and data encryption.

### Requirements
- Create detailed audit logging for all user actions
- Implement session management with timeout and renewal
- Add data encryption for sensitive information
- Create security dashboard for monitoring
- Include IP tracking and suspicious activity detection

### Starter Code
```python
import hashlib
import hmac
import secrets
import json
from datetime import datetime, timedelta
import logging

class SecuritySystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.sessions = {}
        self.audit_logger = logging.getLogger('audit')
        self.security_config = {
            'session_timeout': 3600,  # 1 hour
            'max_login_attempts': 5,
            'password_min_length': 8
        }
    
    def create_session(self, user_id, ip_address):
        """Create new user session"""
        # Implementation here
        pass
    
    def validate_session(self, session_token):
        """Validate and refresh session"""
        # Implementation here
        pass
    
    def log_audit_event(self, user_id, action, details):
        """Log audit event"""
        # Implementation here
        pass
    
    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive data"""
        # Implementation here
        pass
    
    def detect_suspicious_activity(self, user_id, action):
        """Detect suspicious user activity"""
        # Implementation here
        pass
```

### Expected Results
- Comprehensive audit logging system
- Secure session management with timeout
- Data encryption for sensitive information
- Security monitoring dashboard
- Suspicious activity detection and alerts

### Solution Hints
1. Use SQLite for audit log storage
2. Implement HMAC for session token security
3. Use cryptography library for data encryption
4. Create security event correlation for threat detection

---

## Bonus Challenge: Enterprise Integration

### Objective
Extend the dashboard to integrate with external enterprise systems and APIs.

### Requirements
- Integrate with external CRM systems (Salesforce, HubSpot)
- Add REST API endpoints for external access
- Implement webhook support for real-time updates
- Create data synchronization with cloud services
- Add multi-tenant support for different organizations

### Advanced Features
- OAuth 2.0 authentication for external services
- WebSocket support for real-time communication
- Microservices architecture for scalability
- Docker containerization for deployment
- CI/CD pipeline for automated testing and deployment

### Implementation Tips
1. Use Flask or FastAPI for REST API endpoints
2. Implement OAuth 2.0 flow for external integrations
3. Use message queues (Redis/RabbitMQ) for async processing
4. Create Docker containers for easy deployment
5. Implement comprehensive API documentation

---

## Exercise Solutions

### Exercise 1: Enhanced User Management System
```python
# Complete implementation of UserManagementSystem
class UserManagementSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.setup_permissions_table()
    
    def setup_permissions_table(self):
        """Create permissions table if not exists"""
        cursor = self.db_manager.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                permission TEXT NOT NULL,
                granted BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        self.db_manager.connection.commit()
    
    def create_user(self, username, password, email, role):
        """Create new user with role-based permissions"""
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor = self.db_manager.connection.cursor()
            
            cursor.execute("""
                INSERT INTO users (username, password_hash, email, role)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, email, role))
            
            user_id = cursor.lastrowid
            
            # Assign default permissions based on role
            self.assign_role_permissions(user_id, role)
            
            self.db_manager.connection.commit()
            return user_id
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def assign_role_permissions(self, user_id, role):
        """Assign permissions based on user role"""
        role_permissions = {
            'admin': ['all'],
            'manager': ['view_dashboard', 'manage_sales', 'view_reports', 'manage_users'],
            'sales': ['view_dashboard', 'add_sales', 'view_own_reports'],
            'analyst': ['view_dashboard', 'view_reports', 'export_data'],
            'viewer': ['view_dashboard']
        }
        
        permissions = role_permissions.get(role, ['view_dashboard'])
        cursor = self.db_manager.connection.cursor()
        
        for permission in permissions:
            cursor.execute("""
                INSERT INTO user_permissions (user_id, permission)
                VALUES (?, ?)
            """, (user_id, permission))
```

### Exercise 2: Advanced Analytics Dashboard
```python
# Complete implementation of AnalyticsDashboard
class AnalyticsDashboard:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.filters = {}
        self.charts = {}
    
    def create_sales_trend_chart(self, date_range=None):
        """Create sales trend line chart"""
        try:
            # Get sales data with date filtering
            query = """
                SELECT DATE(sale_date) as date, 
                       SUM(quantity * price) as daily_revenue,
                       COUNT(*) as daily_sales
                FROM sales
            """
            
            if date_range:
                query += f" WHERE sale_date BETWEEN '{date_range[0]}' AND '{date_range[1]}'"
            
            query += " GROUP BY DATE(sale_date) ORDER BY date"
            
            cursor = self.data_manager.db_manager.connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            # Create matplotlib chart
            fig, ax = plt.subplots(figsize=(10, 6))
            dates = [row['date'] for row in data]
            revenue = [row['daily_revenue'] for row in data]
            
            ax.plot(dates, revenue, marker='o', linewidth=2, markersize=6)
            ax.set_title('Daily Sales Revenue Trend')
            ax.set_xlabel('Date')
            ax.set_ylabel('Revenue ($)')
            ax.grid(True, alpha=0.3)
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            return fig
        except Exception as e:
            print(f"Error creating sales trend chart: {e}")
            return None
```

### Exercise 3: Real-Time Notifications and Alerts
```python
# Complete implementation of NotificationSystem
class NotificationSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.setup_notification_tables()
        self.alert_rules = {}
        self.notification_queue = []
    
    def setup_notification_tables(self):
        """Create notification tables"""
        cursor = self.db_manager.connection.cursor()
        
        # Notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT FALSE,
                acknowledged_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Alert rules table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alert_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                condition_type TEXT NOT NULL,
                threshold REAL NOT NULL,
                action TEXT NOT NULL,
                enabled BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.db_manager.connection.commit()
    
    def add_alert_rule(self, rule_name, condition_type, threshold, action):
        """Add new alert rule"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                INSERT INTO alert_rules (name, condition_type, threshold, action)
                VALUES (?, ?, ?, ?)
            """, (rule_name, condition_type, threshold, action))
            self.db_manager.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error adding alert rule: {e}")
            return None
    
    def check_sales_alerts(self, sales_data):
        """Check sales data against alert rules"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("SELECT * FROM alert_rules WHERE enabled = TRUE")
            rules = cursor.fetchall()
            
            for rule in rules:
                if rule['condition_type'] == 'revenue_threshold':
                    total_revenue = sum(sale['quantity'] * sale['price'] for sale in sales_data)
                    if total_revenue > rule['threshold']:
                        self.create_notification(
                            user_id=1,  # Admin user
                            notification_type='alert',
                            title=f"Revenue Alert: {rule['name']}",
                            message=f"Revenue ${total_revenue:,.2f} exceeded threshold ${rule['threshold']:,.2f}"
                        )
        except Exception as e:
            print(f"Error checking sales alerts: {e}")
    
    def create_notification(self, user_id, notification_type, title, message):
        """Create new notification"""
        try:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                INSERT INTO notifications (user_id, type, title, message)
                VALUES (?, ?, ?, ?)
            """, (user_id, notification_type, title, message))
            self.db_manager.connection.commit()
            
            # Add to notification queue for real-time display
            self.notification_queue.append({
                'id': cursor.lastrowid,
                'user_id': user_id,
                'type': notification_type,
                'title': title,
                'message': message,
                'created_at': datetime.now()
            })
            
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None
```

These exercises provide comprehensive challenges that build upon the foundation established in the previous chapters, allowing students to create a truly professional and enterprise-ready dashboard application.

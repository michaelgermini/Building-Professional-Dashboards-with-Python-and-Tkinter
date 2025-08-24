# Chapter 9: Exporting and Reporting - Exercises

## Exercise 1: Multi-Format Data Exporter

**Objective**: Create a comprehensive data exporter that supports multiple formats with advanced filtering and formatting options.

**Requirements**:
- Export data to CSV, Excel, JSON, and XML formats
- Implement advanced filtering (date ranges, numeric ranges, text search)
- Add data formatting options (number formatting, date formatting, currency)
- Include export metadata and audit trail
- Create batch export functionality

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import pandas as pd
import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os

class MultiFormatExporter:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Format Data Exporter")
        self.root.geometry("1200x800")
        
        # Sample data
        self.data = self.generate_sample_data()
        
        # Export history
        self.export_history = []
        
        # Create interface
        self.create_widgets()
        self.load_data_preview()
    
    def generate_sample_data(self):
        """Generate sample data for export"""
        # TODO: Generate comprehensive sample data
        pass
    
    def create_widgets(self):
        """Create the main interface"""
        # TODO: Create comprehensive export interface
        pass
    
    def create_filter_panel(self):
        """Create advanced filtering panel"""
        # TODO: Implement date range, numeric range, and text search filters
        pass
    
    def create_format_options(self):
        """Create format-specific export options"""
        # TODO: Add format-specific settings for each export type
        pass
    
    def export_to_csv(self, data, filename, options):
        """Export data to CSV with advanced options"""
        # TODO: Implement CSV export with formatting options
        pass
    
    def export_to_excel(self, data, filename, options):
        """Export data to Excel with multiple sheets and formatting"""
        # TODO: Implement Excel export with styling and multiple sheets
        pass
    
    def export_to_json(self, data, filename, options):
        """Export data to JSON with metadata"""
        # TODO: Implement JSON export with export metadata
        pass
    
    def export_to_xml(self, data, filename, options):
        """Export data to XML format"""
        # TODO: Implement XML export with proper structure
        pass
    
    def batch_export(self):
        """Export data to multiple formats simultaneously"""
        # TODO: Implement batch export functionality
        pass
    
    def add_export_metadata(self, data, export_info):
        """Add metadata to exported data"""
        # TODO: Add export timestamp, user info, and filter details
        pass

def main():
    root = tk.Tk()
    app = MultiFormatExporter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Professional export interface with multiple format support
- Advanced filtering capabilities (date ranges, numeric ranges, text search)
- Format-specific export options and styling
- Export metadata and audit trail
- Batch export functionality
- Export history tracking

## Exercise 2: Automated Report Scheduler

**Objective**: Build an automated report generation and delivery system with scheduling capabilities.

**Requirements**:
- Schedule reports for automatic generation (daily, weekly, monthly)
- Email integration for report delivery
- Report template management
- Multiple output formats (PDF, Excel, HTML)
- Report delivery tracking and logging

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox
import schedule
import time
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
import json
import os

class ReportScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Report Scheduler")
        self.root.geometry("1000x700")
        
        # Scheduler settings
        self.scheduled_reports = []
        self.report_templates = {}
        self.email_settings = {}
        
        # Create interface
        self.create_widgets()
        self.load_scheduled_reports()
    
    def create_widgets(self):
        """Create the main interface"""
        # TODO: Create scheduler interface with report management
        pass
    
    def create_schedule_panel(self):
        """Create report scheduling panel"""
        # TODO: Implement scheduling interface (daily, weekly, monthly)
        pass
    
    def create_email_settings(self):
        """Create email configuration panel"""
        # TODO: Implement email server settings and recipient management
        pass
    
    def create_report_templates(self):
        """Create report template management"""
        # TODO: Implement template creation and management
        pass
    
    def schedule_report(self, report_config):
        """Schedule a report for automatic generation"""
        # TODO: Implement report scheduling logic
        pass
    
    def generate_scheduled_report(self, report_config):
        """Generate a scheduled report"""
        # TODO: Implement automated report generation
        pass
    
    def send_report_email(self, report_file, recipients, subject):
        """Send report via email"""
        # TODO: Implement email delivery with attachments
        pass
    
    def start_scheduler(self):
        """Start the automated scheduler"""
        # TODO: Implement background scheduler thread
        pass
    
    def log_report_delivery(self, report_info, status):
        """Log report delivery status"""
        # TODO: Implement delivery logging and tracking
        pass

def main():
    root = tk.Tk()
    app = ReportScheduler(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Automated report scheduling system
- Email integration for report delivery
- Report template management
- Multiple output format support
- Delivery tracking and logging
- Background scheduler operation

## Exercise 3: Interactive Report Builder

**Objective**: Create an interactive report builder that allows users to design custom reports with drag-and-drop functionality.

**Requirements**:
- Drag-and-drop report design interface
- Multiple chart types and data visualizations
- Custom report templates and layouts
- Real-time preview functionality
- Export to multiple formats (PDF, HTML, PowerPoint)

**Starter Code**:
```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import Canvas
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ReportElement:
    def __init__(self, element_type, properties):
        self.element_type = element_type
        self.properties = properties
        self.id = None

class InteractiveReportBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Report Builder")
        self.root.geometry("1400x900")
        
        # Report elements
        self.report_elements = []
        self.selected_element = None
        self.dragging = False
        
        # Sample data
        self.sample_data = self.generate_sample_data()
        
        # Create interface
        self.create_widgets()
    
    def generate_sample_data(self):
        """Generate sample data for reports"""
        # TODO: Generate comprehensive sample datasets
        pass
    
    def create_widgets(self):
        """Create the main interface"""
        # TODO: Create drag-and-drop report builder interface
        pass
    
    def create_toolbox(self):
        """Create element toolbox"""
        # TODO: Implement drag-and-drop toolbox with chart types
        pass
    
    def create_canvas(self):
        """Create report design canvas"""
        # TODO: Implement interactive design canvas
        pass
    
    def create_properties_panel(self):
        """Create element properties panel"""
        # TODO: Implement properties editing panel
        pass
    
    def add_element(self, element_type, x, y):
        """Add a new element to the report"""
        # TODO: Implement element addition with positioning
        pass
    
    def select_element(self, element_id):
        """Select an element for editing"""
        # TODO: Implement element selection and highlighting
        pass
    
    def update_element_properties(self, element_id, properties):
        """Update element properties"""
        # TODO: Implement property updates with real-time preview
        pass
    
    def generate_preview(self):
        """Generate real-time report preview"""
        # TODO: Implement live preview generation
        pass
    
    def export_report(self, format_type):
        """Export report to specified format"""
        # TODO: Implement multi-format export
        pass
    
    def save_report_template(self):
        """Save current report as template"""
        # TODO: Implement template saving
        pass
    
    def load_report_template(self):
        """Load a saved report template"""
        # TODO: Implement template loading
        pass

def main():
    root = tk.Tk()
    app = InteractiveReportBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
```

**Expected Results**:
- Interactive drag-and-drop report design interface
- Multiple chart types and visualizations
- Real-time preview functionality
- Custom report templates
- Multi-format export capabilities
- Professional report builder experience

## Bonus Challenge: Enterprise Reporting System

**Objective**: Build a comprehensive enterprise reporting system with advanced features for large-scale deployments.

**Requirements**:
- Multi-user support with role-based access
- Database integration for report storage
- Advanced analytics and data processing
- Report versioning and collaboration
- Integration with external systems (APIs, databases)
- Performance optimization for large datasets

**Advanced Features**:
- User authentication and authorization
- Report sharing and collaboration
- Advanced data visualization
- Automated data refresh
- Report distribution workflows
- Compliance and audit features

## Solutions

### Exercise 1 Solution
```python
# Multi-Format Exporter Implementation
def generate_sample_data(self):
    """Generate comprehensive sample data"""
    data = []
    departments = ['Sales', 'Marketing', 'Engineering', 'HR', 'Finance']
    positions = ['Manager', 'Senior', 'Junior', 'Intern']
    
    for i in range(100):
        hire_date = datetime.now() - timedelta(days=random.randint(0, 1000))
        data.append({
            'ID': i + 1,
            'Name': f'Employee {i + 1}',
            'Email': f'employee{i+1}@company.com',
            'Department': random.choice(departments),
            'Position': random.choice(positions),
            'Salary': random.randint(40000, 120000),
            'Hire_Date': hire_date.strftime('%Y-%m-%d'),
            'Performance_Score': round(random.uniform(60, 100), 1),
            'Active': random.choice(['Yes', 'No']),
            'Last_Review': (hire_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        })
    return data

def export_to_excel(self, data, filename, options):
    """Export data to Excel with advanced formatting"""
    try:
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Apply filters
        if options.get('filters'):
            for filter_key, filter_value in options['filters'].items():
                if filter_value:
                    df = df[df[filter_key] == filter_value]
        
        # Create Excel writer with formatting
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Summary sheet
            summary_data = self.create_summary_data(df)
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Get workbook and worksheet for formatting
            workbook = writer.book
            worksheet = writer.sheets['Data']
            
            # Apply formatting
            if options.get('formatting'):
                self.apply_excel_formatting(worksheet, options['formatting'])
        
        return True
    except Exception as e:
        print(f"Excel export error: {e}")
        return False

def apply_excel_formatting(self, worksheet, formatting):
    """Apply formatting to Excel worksheet"""
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    # Header formatting
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    for cell in worksheet[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")
    
    # Data formatting
    for row in worksheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(horizontal="center")
    
    # Auto-adjust column widths
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        
        adjusted_width = min(max_length + 2, 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width
```

### Exercise 2 Solution
```python
# Report Scheduler Implementation
def schedule_report(self, report_config):
    """Schedule a report for automatic generation"""
    try:
        schedule_type = report_config['schedule_type']
        schedule_time = report_config['schedule_time']
        report_template = report_config['template']
        recipients = report_config['recipients']
        
        if schedule_type == 'daily':
            schedule.every().day.at(schedule_time).do(
                self.generate_scheduled_report, report_config
            )
        elif schedule_type == 'weekly':
            schedule.every().week.at(schedule_time).do(
                self.generate_scheduled_report, report_config
            )
        elif schedule_type == 'monthly':
            schedule.every().month.at(schedule_time).do(
                self.generate_scheduled_report, report_config
            )
        
        # Add to scheduled reports list
        self.scheduled_reports.append(report_config)
        self.save_scheduled_reports()
        
        return True
    except Exception as e:
        print(f"Scheduling error: {e}")
        return False

def send_report_email(self, report_file, recipients, subject):
    """Send report via email with attachment"""
    try:
        # Email configuration
        smtp_server = self.email_settings.get('smtp_server', 'smtp.gmail.com')
        smtp_port = self.email_settings.get('smtp_port', 587)
        sender_email = self.email_settings.get('sender_email')
        sender_password = self.email_settings.get('sender_password')
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # Email body
        body = f"""
        Hello,
        
        Please find attached the requested report.
        
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Best regards,
        Automated Report System
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach report file
        with open(report_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(report_file)}'
        )
        msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipients, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email sending error: {e}")
        return False

def start_scheduler(self):
    """Start the automated scheduler in background thread"""
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
```

### Exercise 3 Solution
```python
# Interactive Report Builder Implementation
def add_element(self, element_type, x, y):
    """Add a new element to the report"""
    try:
        # Create element with default properties
        element_properties = self.get_default_properties(element_type)
        element = ReportElement(element_type, element_properties)
        
        # Generate unique ID
        element.id = f"{element_type}_{len(self.report_elements)}"
        
        # Add to canvas
        self.add_element_to_canvas(element, x, y)
        
        # Add to elements list
        self.report_elements.append(element)
        
        # Update properties panel
        self.update_properties_panel(element)
        
        return element.id
    except Exception as e:
        print(f"Error adding element: {e}")
        return None

def add_element_to_canvas(self, element, x, y):
    """Add element to the design canvas"""
    try:
        if element.element_type == 'chart':
            # Create chart element
            chart_frame = tk.Frame(self.canvas, relief="raised", borderwidth=2)
            chart_frame.place(x=x, y=y, width=300, height=200)
            
            # Add chart title
            title_label = tk.Label(chart_frame, text="Chart", font=("Arial", 10, "bold"))
            title_label.pack(pady=5)
            
            # Add placeholder for chart
            placeholder = tk.Label(chart_frame, text="Chart will be rendered here", 
                                 bg="lightgray", width=35, height=8)
            placeholder.pack(pady=10)
            
            # Make draggable
            self.make_draggable(chart_frame, element.id)
            
        elif element.element_type == 'table':
            # Create table element
            table_frame = tk.Frame(self.canvas, relief="raised", borderwidth=2)
            table_frame.place(x=x, y=y, width=400, height=250)
            
            # Add table title
            title_label = tk.Label(table_frame, text="Data Table", font=("Arial", 10, "bold"))
            title_label.pack(pady=5)
            
            # Add placeholder for table
            placeholder = tk.Label(table_frame, text="Table will be rendered here", 
                                 bg="lightgray", width=45, height=10)
            placeholder.pack(pady=10)
            
            # Make draggable
            self.make_draggable(table_frame, element.id)
            
        elif element.element_type == 'text':
            # Create text element
            text_frame = tk.Frame(self.canvas, relief="raised", borderwidth=2)
            text_frame.place(x=x, y=y, width=200, height=100)
            
            # Add text area
            text_area = tk.Text(text_frame, wrap="word", width=25, height=5)
            text_area.pack(padx=5, pady=5)
            text_area.insert("1.0", "Enter text here...")
            
            # Make draggable
            self.make_draggable(text_frame, element.id)
            
    except Exception as e:
        print(f"Error adding element to canvas: {e}")

def make_draggable(self, widget, element_id):
    """Make a widget draggable on the canvas"""
    def on_press(event):
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
    
    def on_drag(event):
        dx = event.x - widget._drag_start_x
        dy = event.y - widget._drag_start_y
        
        x = widget.winfo_x() + dx
        y = widget.winfo_y() + dy
        
        widget.place(x=x, y=y)
        
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
    
    def on_release(event):
        # Update element position in data
        for element in self.report_elements:
            if element.id == element_id:
                element.properties['x'] = widget.winfo_x()
                element.properties['y'] = widget.winfo_y()
                break
    
    widget.bind("<Button-1>", on_press)
    widget.bind("<B1-Motion>", on_drag)
    widget.bind("<ButtonRelease-1>", on_release)
```

## Learning Objectives

After completing these exercises, you should be able to:

1. **Multi-Format Export**: Export data to various formats with advanced options
2. **Automated Reporting**: Create scheduled report generation and delivery systems
3. **Interactive Design**: Build drag-and-drop report design interfaces
4. **Email Integration**: Implement automated email delivery of reports
5. **Template Management**: Create and manage reusable report templates
6. **Data Filtering**: Implement advanced filtering and data processing
7. **Performance Optimization**: Handle large datasets efficiently
8. **User Experience**: Create professional and intuitive export interfaces

## Next Steps

- Implement enterprise-level reporting systems
- Add integration with business intelligence tools
- Create advanced data visualization components
- Implement report collaboration features
- Add compliance and audit capabilities
- Develop mobile-friendly report interfaces
- Create API-based report generation services

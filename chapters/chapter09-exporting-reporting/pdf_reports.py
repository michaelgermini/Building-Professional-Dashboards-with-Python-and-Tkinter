"""
PDF Report Generation - Chapter 9 Example
Demonstrates professional PDF report creation using ReportLab
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.colors import HexColor
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from datetime import datetime
import random
import json

class PDFReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Report Generator")
        self.root.geometry("1000x700")
        
        # Sample data for reports
        self.sample_data = self.generate_sample_data()
        
        # Report templates
        self.report_templates = {
            'executive_summary': self.create_executive_summary,
            'detailed_analysis': self.create_detailed_analysis,
            'monthly_report': self.create_monthly_report,
            'custom_report': self.create_custom_report
        }
        
        # Create interface
        self.create_widgets()
    
    def generate_sample_data(self):
        """Generate sample data for reports"""
        # Sales data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        sales_data = {
            'Product A': [random.randint(1000, 5000) for _ in months],
            'Product B': [random.randint(800, 4000) for _ in months],
            'Product C': [random.randint(1200, 6000) for _ in months]
        }
        
        # Employee data
        employees = [
            {'name': 'John Smith', 'department': 'Sales', 'salary': 65000, 'performance': 85},
            {'name': 'Jane Doe', 'department': 'Marketing', 'salary': 58000, 'performance': 92},
            {'name': 'Bob Johnson', 'department': 'Engineering', 'salary': 75000, 'performance': 88},
            {'name': 'Alice Brown', 'department': 'HR', 'salary': 52000, 'performance': 78},
            {'name': 'Charlie Wilson', 'department': 'Finance', 'salary': 68000, 'performance': 90}
        ]
        
        # Financial data
        financial_data = {
            'revenue': [random.randint(50000, 100000) for _ in months],
            'expenses': [random.randint(30000, 70000) for _ in months],
            'profit': [random.randint(10000, 40000) for _ in months]
        }
        
        return {
            'sales': sales_data,
            'employees': employees,
            'financial': financial_data,
            'months': months
        }
    
    def create_widgets(self):
        """Create the main interface"""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(self.root, text="PDF Report Generator", 
                              font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Report options
        left_frame = ttk.Frame(self.root)
        left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.create_report_options(left_frame)
        self.create_report_settings(left_frame)
        
        # Right panel - Preview and controls
        right_frame = ttk.Frame(self.root)
        right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.create_preview_section(right_frame)
        self.create_control_buttons(right_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief="sunken", anchor="w")
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
    def create_report_options(self, parent):
        """Create report type selection"""
        options_frame = ttk.LabelFrame(parent, text="Report Type")
        options_frame.pack(fill="x", pady=(0, 10))
        
        # Report type selection
        self.report_type_var = tk.StringVar(value="executive_summary")
        
        report_types = [
            ("Executive Summary", "executive_summary"),
            ("Detailed Analysis", "detailed_analysis"),
            ("Monthly Report", "monthly_report"),
            ("Custom Report", "custom_report")
        ]
        
        for i, (text, value) in enumerate(report_types):
            ttk.Radiobutton(options_frame, text=text, variable=self.report_type_var, 
                           value=value).pack(anchor="w", padx=10, pady=2)
        
        # Report sections
        sections_frame = ttk.LabelFrame(parent, text="Report Sections")
        sections_frame.pack(fill="x", pady=(0, 10))
        
        self.section_vars = {}
        sections = [
            "Executive Summary",
            "Sales Analysis",
            "Employee Performance",
            "Financial Overview",
            "Charts and Graphs",
            "Recommendations"
        ]
        
        for section in sections:
            var = tk.BooleanVar(value=True)
            self.section_vars[section] = var
            ttk.Checkbutton(sections_frame, text=section, variable=var).pack(anchor="w", padx=10, pady=2)
    
    def create_report_settings(self, parent):
        """Create report settings"""
        settings_frame = ttk.LabelFrame(parent, text="Report Settings")
        settings_frame.pack(fill="x", pady=(0, 10))
        
        # Page size
        ttk.Label(settings_frame, text="Page Size:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.page_size_var = tk.StringVar(value="A4")
        page_size_combo = ttk.Combobox(settings_frame, textvariable=self.page_size_var,
                                      values=["A4", "Letter"], state="readonly", width=15)
        page_size_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Orientation
        ttk.Label(settings_frame, text="Orientation:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.orientation_var = tk.StringVar(value="Portrait")
        orientation_combo = ttk.Combobox(settings_frame, textvariable=self.orientation_var,
                                       values=["Portrait", "Landscape"], state="readonly", width=15)
        orientation_combo.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Include charts
        self.include_charts_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Include Charts", 
                       variable=self.include_charts_var).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Include tables
        self.include_tables_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Include Tables", 
                       variable=self.include_tables_var).grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Company branding
        self.include_branding_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Include Company Branding", 
                       variable=self.include_branding_var).grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
    
    def create_preview_section(self, parent):
        """Create preview section"""
        preview_frame = ttk.LabelFrame(parent, text="Report Preview")
        preview_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Preview text
        self.preview_text = tk.Text(preview_frame, wrap="word", height=20)
        preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", 
                                         command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=preview_scrollbar.set)
        
        self.preview_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        preview_scrollbar.pack(side="right", fill="y", pady=5)
        
        # Load initial preview
        self.update_preview()
    
    def create_control_buttons(self, parent):
        """Create control buttons"""
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Generate preview button
        ttk.Button(controls_frame, text="Update Preview", 
                  command=self.update_preview).pack(side="left", padx=5)
        
        # Generate PDF button
        ttk.Button(controls_frame, text="Generate PDF", 
                  command=self.generate_pdf).pack(side="left", padx=5)
        
        # Save template button
        ttk.Button(controls_frame, text="Save Template", 
                  command=self.save_template).pack(side="left", padx=5)
        
        # Load template button
        ttk.Button(controls_frame, text="Load Template", 
                  command=self.load_template).pack(side="left", padx=5)
    
    def update_preview(self):
        """Update the preview text"""
        try:
            # Clear preview
            self.preview_text.delete(1.0, tk.END)
            
            # Get selected report type
            report_type = self.report_type_var.get()
            
            # Generate preview content
            preview_content = self.generate_preview_content(report_type)
            
            # Display preview
            self.preview_text.insert(tk.END, preview_content)
            
            self.status_var.set("Preview updated")
            
        except Exception as e:
            self.status_var.set(f"Preview error: {e}")
    
    def generate_preview_content(self, report_type):
        """Generate preview content for the selected report type"""
        content = f"REPORT PREVIEW: {report_type.replace('_', ' ').title()}\n"
        content += "=" * 50 + "\n\n"
        
        # Add sections based on selection
        for section, var in self.section_vars.items():
            if var.get():
                content += f"✓ {section}\n"
                content += f"  - Content will be included in the report\n\n"
        
        # Add settings info
        content += "REPORT SETTINGS:\n"
        content += f"- Page Size: {self.page_size_var.get()}\n"
        content += f"- Orientation: {self.orientation_var.get()}\n"
        content += f"- Include Charts: {'Yes' if self.include_charts_var.get() else 'No'}\n"
        content += f"- Include Tables: {'Yes' if self.include_tables_var.get() else 'No'}\n"
        content += f"- Include Branding: {'Yes' if self.include_branding_var.get() else 'No'}\n\n"
        
        # Add sample data info
        content += "SAMPLE DATA INCLUDED:\n"
        content += f"- Sales data for {len(self.sample_data['months'])} months\n"
        content += f"- {len(self.sample_data['employees'])} employee records\n"
        content += f"- Financial data with revenue, expenses, and profit\n\n"
        
        content += "Click 'Generate PDF' to create the actual report."
        
        return content
    
    def generate_pdf(self):
        """Generate the PDF report"""
        try:
            # Get filename
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            self.status_var.set("Generating PDF...")
            self.root.update()
            
            # Get report type and create report
            report_type = self.report_type_var.get()
            report_function = self.report_templates[report_type]
            
            # Generate the report
            report_function(filename)
            
            self.status_var.set("PDF generated successfully")
            messagebox.showinfo("Success", f"PDF report generated: {filename}")
            
        except Exception as e:
            self.status_var.set(f"PDF generation failed: {e}")
            messagebox.showerror("Error", f"Failed to generate PDF: {e}")
    
    def create_executive_summary(self, filename):
        """Create executive summary report"""
        # Get page size
        page_size = A4 if self.page_size_var.get() == "A4" else letter
        
        # Create document
        doc = SimpleDocTemplate(filename, pagesize=page_size)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#2E86AB')
        )
        
        story.append(Paragraph("Executive Summary Report", title_style))
        story.append(Spacer(1, 20))
        
        # Date
        date_style = ParagraphStyle(
            'Date',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_RIGHT,
            textColor=colors.grey
        )
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y')}", date_style))
        story.append(Spacer(1, 30))
        
        # Executive Summary section
        if self.section_vars["Executive Summary"].get():
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            summary_text = """
            This report provides a comprehensive overview of our company's performance 
            across key business areas including sales, employee performance, and financial metrics. 
            The data shows positive trends in most areas with opportunities for improvement 
            in specific departments.
            """
            story.append(Paragraph(summary_text, styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Key Metrics Table
        if self.include_tables_var.get():
            story.append(Paragraph("Key Performance Metrics", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Calculate key metrics
            total_revenue = sum(self.sample_data['financial']['revenue'])
            total_expenses = sum(self.sample_data['financial']['expenses'])
            total_profit = sum(self.sample_data['financial']['profit'])
            avg_performance = sum(emp['performance'] for emp in self.sample_data['employees']) / len(self.sample_data['employees'])
            
            metrics_data = [
                ['Metric', 'Value'],
                ['Total Revenue', f"${total_revenue:,}"],
                ['Total Expenses', f"${total_expenses:,}"],
                ['Total Profit', f"${total_profit:,}"],
                ['Average Employee Performance', f"{avg_performance:.1f}%"],
                ['Number of Employees', str(len(self.sample_data['employees']))]
            ]
            
            metrics_table = Table(metrics_data, colWidths=[2*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(metrics_table)
            story.append(Spacer(1, 20))
        
        # Charts
        if self.include_charts_var.get():
            story.append(Paragraph("Performance Charts", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Create revenue chart
            chart_data = self.create_revenue_chart()
            story.append(chart_data)
            story.append(Spacer(1, 20))
        
        # Recommendations
        if self.section_vars["Recommendations"].get():
            story.append(Paragraph("Recommendations", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            recommendations = [
                "Continue monitoring sales performance and adjust strategies as needed",
                "Implement employee development programs to improve performance scores",
                "Review expense management to optimize profit margins",
                "Consider expanding successful product lines based on sales data"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(f"• {rec}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
    
    def create_detailed_analysis(self, filename):
        """Create detailed analysis report"""
        # Get page size
        page_size = A4 if self.page_size_var.get() == "A4" else letter
        
        # Create document
        doc = SimpleDocTemplate(filename, pagesize=page_size)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=HexColor('#2E86AB')
        )
        
        story.append(Paragraph("Detailed Analysis Report", title_style))
        story.append(Spacer(1, 20))
        
        # Sales Analysis
        if self.section_vars["Sales Analysis"].get():
            story.append(Paragraph("Sales Analysis", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Sales data table
            sales_data = [['Month'] + list(self.sample_data['sales'].keys())]
            for i, month in enumerate(self.sample_data['months']):
                row = [month]
                for product in self.sample_data['sales'].keys():
                    row.append(str(self.sample_data['sales'][product][i]))
                sales_data.append(row)
            
            sales_table = Table(sales_data, colWidths=[1*inch] + [1.5*inch] * len(self.sample_data['sales']))
            sales_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(sales_table)
            story.append(Spacer(1, 20))
        
        # Employee Performance
        if self.section_vars["Employee Performance"].get():
            story.append(Paragraph("Employee Performance", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Employee data table
            emp_data = [['Name', 'Department', 'Salary', 'Performance']]
            for emp in self.sample_data['employees']:
                emp_data.append([
                    emp['name'],
                    emp['department'],
                    f"${emp['salary']:,}",
                    f"{emp['performance']}%"
                ])
            
            emp_table = Table(emp_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
            emp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(emp_table)
            story.append(Spacer(1, 20))
        
        # Financial Overview
        if self.section_vars["Financial Overview"].get():
            story.append(Paragraph("Financial Overview", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Financial data table
            fin_data = [['Month', 'Revenue', 'Expenses', 'Profit']]
            for i, month in enumerate(self.sample_data['months']):
                fin_data.append([
                    month,
                    f"${self.sample_data['financial']['revenue'][i]:,}",
                    f"${self.sample_data['financial']['expenses'][i]:,}",
                    f"${self.sample_data['financial']['profit'][i]:,}"
                ])
            
            fin_table = Table(fin_data, colWidths=[1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            fin_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(fin_table)
            story.append(Spacer(1, 20))
        
        # Build PDF
        doc.build(story)
    
    def create_monthly_report(self, filename):
        """Create monthly report"""
        # Similar structure to detailed analysis but focused on monthly trends
        self.create_detailed_analysis(filename)
    
    def create_custom_report(self, filename):
        """Create custom report based on user selections"""
        # Similar structure but only includes selected sections
        self.create_detailed_analysis(filename)
    
    def create_revenue_chart(self):
        """Create a revenue chart using ReportLab"""
        drawing = Drawing(400, 200)
        
        # Create line chart
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        
        # Set data
        chart.data = [self.sample_data['financial']['revenue']]
        chart.categoryAxis.categoryNames = self.sample_data['months']
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(self.sample_data['financial']['revenue']) * 1.1
        chart.valueAxis.valueStep = max(self.sample_data['financial']['revenue']) / 5
        
        # Set colors
        chart.lines[0].strokeColor = colors.blue
        chart.lines[0].strokeWidth = 2
        
        drawing.add(chart)
        return drawing
    
    def save_template(self):
        """Save current report settings as a template"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                template = {
                    'report_type': self.report_type_var.get(),
                    'sections': {section: var.get() for section, var in self.section_vars.items()},
                    'settings': {
                        'page_size': self.page_size_var.get(),
                        'orientation': self.orientation_var.get(),
                        'include_charts': self.include_charts_var.get(),
                        'include_tables': self.include_tables_var.get(),
                        'include_branding': self.include_branding_var.get()
                    }
                }
                
                with open(filename, 'w') as f:
                    json.dump(template, f, indent=2)
                
                messagebox.showinfo("Success", f"Template saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save template: {e}")
    
    def load_template(self):
        """Load a saved template"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r') as f:
                    template = json.load(f)
                
                # Apply template settings
                self.report_type_var.set(template['report_type'])
                
                for section, enabled in template['sections'].items():
                    if section in self.section_vars:
                        self.section_vars[section].set(enabled)
                
                settings = template['settings']
                self.page_size_var.set(settings['page_size'])
                self.orientation_var.set(settings['orientation'])
                self.include_charts_var.set(settings['include_charts'])
                self.include_tables_var.set(settings['include_tables'])
                self.include_branding_var.set(settings['include_branding'])
                
                # Update preview
                self.update_preview()
                
                messagebox.showinfo("Success", f"Template loaded from {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load template: {e}")

def main():
    root = tk.Tk()
    app = PDFReportGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()

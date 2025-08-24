"""
CSV and Excel Export - Chapter 9 Example
Demonstrates comprehensive data export functionality
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
import pandas as pd
import json
from datetime import datetime
import sqlite3
from collections import defaultdict
import os

class DataExporter:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Export Dashboard")
        self.root.geometry("1000x700")
        
        # Sample data for demonstration
        self.sample_data = self.generate_sample_data()
        
        # Export settings
        self.export_settings = {
            'include_headers': True,
            'date_format': '%Y-%m-%d',
            'encoding': 'utf-8',
            'delimiter': ',',
            'quote_all': False
        }
        
        # Create interface
        self.create_widgets()
        self.load_data_preview()
    
    def generate_sample_data(self):
        """Generate sample data for demonstration"""
        departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance']
        positions = ['Manager', 'Senior', 'Junior', 'Intern']
        
        data = []
        for i in range(50):
            data.append({
                'ID': i + 1,
                'Name': f'Employee {i + 1}',
                'Email': f'employee{i+1}@company.com',
                'Department': departments[i % len(departments)],
                'Position': positions[i % len(positions)],
                'Salary': 50000 + (i * 1000),
                'Hire_Date': datetime.now().strftime('%Y-%m-%d'),
                'Performance_Score': round(70 + (i % 30), 1),
                'Active': 'Yes' if i % 10 != 0 else 'No'
            })
        return data
    
    def create_widgets(self):
        """Create the main interface"""
        # Configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(self.root, text="Data Export Dashboard", 
                              font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Data preview and filters
        left_frame = ttk.Frame(self.root)
        left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.create_data_preview(left_frame)
        self.create_filters(left_frame)
        
        # Right panel - Export options
        right_frame = ttk.Frame(self.root)
        right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.create_export_options(right_frame)
        self.create_export_controls(right_frame)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief="sunken", anchor="w")
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
    def create_data_preview(self, parent):
        """Create data preview section"""
        preview_frame = ttk.LabelFrame(parent, text="Data Preview")
        preview_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create Treeview for data preview
        columns = list(self.sample_data[0].keys())
        self.preview_tree = ttk.Treeview(preview_frame, columns=columns, 
                                        show="headings", height=10)
        
        # Configure columns
        for col in columns:
            self.preview_tree.heading(col, text=col)
            self.preview_tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", 
                                 command=self.preview_tree.yview)
        self.preview_tree.configure(yscrollcommand=scrollbar.set)
        
        self.preview_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Data info
        info_frame = ttk.Frame(preview_frame)
        info_frame.pack(fill="x", pady=5)
        
        self.data_info_label = ttk.Label(info_frame, text="")
        self.data_info_label.pack(side="left")
    
    def create_filters(self, parent):
        """Create data filtering section"""
        filter_frame = ttk.LabelFrame(parent, text="Data Filters")
        filter_frame.pack(fill="x", pady=(0, 10))
        
        # Department filter
        ttk.Label(filter_frame, text="Department:").grid(row=0, column=0, padx=5, pady=5)
        self.dept_var = tk.StringVar(value="All")
        dept_combo = ttk.Combobox(filter_frame, textvariable=self.dept_var, 
                                 values=["All"] + list(set(d['Department'] for d in self.sample_data)),
                                 state="readonly", width=15)
        dept_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Position filter
        ttk.Label(filter_frame, text="Position:").grid(row=0, column=2, padx=5, pady=5)
        self.pos_var = tk.StringVar(value="All")
        pos_combo = ttk.Combobox(filter_frame, textvariable=self.pos_var,
                                values=["All"] + list(set(d['Position'] for d in self.sample_data)),
                                state="readonly", width=15)
        pos_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Active status filter
        ttk.Label(filter_frame, text="Status:").grid(row=1, column=0, padx=5, pady=5)
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var,
                                   values=["All", "Yes", "No"], state="readonly", width=15)
        status_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Apply filters button
        ttk.Button(filter_frame, text="Apply Filters", 
                  command=self.apply_filters).grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        
        # Clear filters button
        ttk.Button(filter_frame, text="Clear Filters", 
                  command=self.clear_filters).grid(row=2, column=0, columnspan=4, padx=5, pady=5)
    
    def create_export_options(self, parent):
        """Create export options section"""
        options_frame = ttk.LabelFrame(parent, text="Export Options")
        options_frame.pack(fill="x", pady=(0, 10))
        
        # Format selection
        ttk.Label(options_frame, text="Export Format:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.format_var = tk.StringVar(value="CSV")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var,
                                   values=["CSV", "Excel", "JSON"], state="readonly", width=15)
        format_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Include headers
        self.headers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include Headers", 
                       variable=self.headers_var).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Column selection
        ttk.Label(options_frame, text="Columns to Export:").grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        columns_frame = ttk.Frame(options_frame)
        columns_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        self.column_vars = {}
        columns = list(self.sample_data[0].keys())
        for i, col in enumerate(columns):
            var = tk.BooleanVar(value=True)
            self.column_vars[col] = var
            ttk.Checkbutton(columns_frame, text=col, variable=var).grid(
                row=i//2, column=i%2, padx=5, pady=2, sticky="w")
        
        # Encoding selection
        ttk.Label(options_frame, text="Encoding:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.encoding_var = tk.StringVar(value="utf-8")
        encoding_combo = ttk.Combobox(options_frame, textvariable=self.encoding_var,
                                     values=["utf-8", "utf-8-sig", "latin-1", "cp1252"], 
                                     state="readonly", width=15)
        encoding_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    
    def create_export_controls(self, parent):
        """Create export control buttons"""
        controls_frame = ttk.LabelFrame(parent, text="Export Controls")
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # Export buttons
        ttk.Button(controls_frame, text="Export Data", 
                  command=self.export_data).pack(fill="x", padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Export Summary", 
                  command=self.export_summary).pack(fill="x", padx=10, pady=5)
        
        ttk.Button(controls_frame, text="Export Statistics", 
                  command=self.export_statistics).pack(fill="x", padx=10, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(controls_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        
        # Recent exports
        recent_frame = ttk.LabelFrame(parent, text="Recent Exports")
        recent_frame.pack(fill="both", expand=True)
        
        self.recent_listbox = tk.Listbox(recent_frame, height=6)
        self.recent_listbox.pack(fill="both", expand=True, padx=5, pady=5)
    
    def load_data_preview(self):
        """Load data into the preview treeview"""
        # Clear existing items
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        # Add data (show first 20 rows)
        for i, row in enumerate(self.sample_data[:20]):
            self.preview_tree.insert("", "end", values=list(row.values()))
        
        # Update data info
        self.update_data_info()
    
    def update_data_info(self):
        """Update data information display"""
        total_records = len(self.sample_data)
        self.data_info_label.config(text=f"Total Records: {total_records}")
    
    def apply_filters(self):
        """Apply selected filters to the data"""
        filtered_data = []
        
        for row in self.sample_data:
            # Department filter
            if self.dept_var.get() != "All" and row['Department'] != self.dept_var.get():
                continue
            
            # Position filter
            if self.pos_var.get() != "All" and row['Position'] != self.pos_var.get():
                continue
            
            # Status filter
            if self.status_var.get() != "All" and row['Active'] != self.status_var.get():
                continue
            
            filtered_data.append(row)
        
        # Update preview
        self.update_preview_with_data(filtered_data)
        self.status_var.set(f"Filtered: {len(filtered_data)} records")
    
    def clear_filters(self):
        """Clear all filters"""
        self.dept_var.set("All")
        self.pos_var.set("All")
        self.status_var.set("All")
        
        # Reload original data
        self.load_data_preview()
        self.status_var.set("Filters cleared")
    
    def update_preview_with_data(self, data):
        """Update preview with filtered data"""
        # Clear existing items
        for item in self.preview_tree.get_children():
            self.preview_tree.delete(item)
        
        # Add filtered data
        for row in data[:20]:  # Show first 20 rows
            self.preview_tree.insert("", "end", values=list(row.values()))
        
        # Update data info
        self.data_info_label.config(text=f"Filtered Records: {len(data)}")
    
    def get_filtered_data(self):
        """Get currently filtered data"""
        filtered_data = []
        
        for row in self.sample_data:
            # Apply current filters
            if self.dept_var.get() != "All" and row['Department'] != self.dept_var.get():
                continue
            if self.pos_var.get() != "All" and row['Position'] != self.pos_var.get():
                continue
            if self.status_var.get() != "All" and row['Active'] != self.status_var.get():
                continue
            
            filtered_data.append(row)
        
        return filtered_data
    
    def get_selected_columns(self):
        """Get list of selected columns"""
        return [col for col, var in self.column_vars.items() if var.get()]
    
    def export_data(self):
        """Export data based on current settings"""
        try:
            # Get filtered data
            data = self.get_filtered_data()
            if not data:
                messagebox.showwarning("Warning", "No data to export")
                return
            
            # Get selected columns
            columns = self.get_selected_columns()
            if not columns:
                messagebox.showwarning("Warning", "Please select at least one column")
                return
            
            # Get export format
            export_format = self.format_var.get()
            
            # Get filename
            filetypes = {
                "CSV": [("CSV files", "*.csv"), ("All files", "*.*")],
                "Excel": [("Excel files", "*.xlsx"), ("All files", "*.*")],
                "JSON": [("JSON files", "*.json"), ("All files", "*.*")]
            }
            
            filename = filedialog.asksaveasfilename(
                defaultextension=f".{export_format.lower()}",
                filetypes=filetypes[export_format]
            )
            
            if not filename:
                return
            
            # Start export
            self.progress_var.set(0)
            self.status_var.set("Exporting...")
            self.root.update()
            
            if export_format == "CSV":
                self.export_to_csv(data, columns, filename)
            elif export_format == "Excel":
                self.export_to_excel(data, columns, filename)
            elif export_format == "JSON":
                self.export_to_json(data, columns, filename)
            
            # Update progress
            self.progress_var.set(100)
            self.status_var.set("Export completed")
            
            # Add to recent exports
            self.add_recent_export(filename, export_format, len(data))
            
            messagebox.showinfo("Success", f"Data exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Export failed: {e}")
            self.status_var.set("Export failed")
    
    def export_to_csv(self, data, columns, filename):
        """Export data to CSV format"""
        with open(filename, 'w', newline='', encoding=self.encoding_var.get()) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            
            if self.headers_var.get():
                writer.writeheader()
            
            for i, row in enumerate(data):
                # Filter row to selected columns
                filtered_row = {col: row[col] for col in columns}
                writer.writerow(filtered_row)
                
                # Update progress
                if i % 10 == 0:
                    progress = (i / len(data)) * 100
                    self.progress_var.set(progress)
                    self.root.update()
    
    def export_to_excel(self, data, columns, filename):
        """Export data to Excel format"""
        # Create DataFrame with selected columns
        df = pd.DataFrame(data)[columns]
        
        # Create Excel writer
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Main data sheet
            df.to_excel(writer, sheet_name='Data', index=False)
            
            # Summary sheet
            summary_data = self.create_summary_data(data)
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Statistics sheet
            stats_data = self.create_statistics_data(data)
            stats_df = pd.DataFrame(stats_data)
            stats_df.to_excel(writer, sheet_name='Statistics', index=False)
    
    def export_to_json(self, data, columns, filename):
        """Export data to JSON format"""
        # Filter data to selected columns
        filtered_data = []
        for row in data:
            filtered_row = {col: row[col] for col in columns}
            filtered_data.append(filtered_row)
        
        # Export metadata
        export_info = {
            'export_date': datetime.now().isoformat(),
            'total_records': len(filtered_data),
            'columns': columns,
            'filters_applied': {
                'department': self.dept_var.get(),
                'position': self.pos_var.get(),
                'status': self.status_var.get()
            },
            'data': filtered_data
        }
        
        with open(filename, 'w', encoding=self.encoding_var.get()) as jsonfile:
            json.dump(export_info, jsonfile, indent=2)
    
    def create_summary_data(self, data):
        """Create summary data for Excel export"""
        summary = []
        
        # Department summary
        dept_counts = defaultdict(int)
        for row in data:
            dept_counts[row['Department']] += 1
        
        for dept, count in dept_counts.items():
            summary.append({
                'Category': 'Department',
                'Value': dept,
                'Count': count
            })
        
        # Position summary
        pos_counts = defaultdict(int)
        for row in data:
            pos_counts[row['Position']] += 1
        
        for pos, count in pos_counts.items():
            summary.append({
                'Category': 'Position',
                'Value': pos,
                'Count': count
            })
        
        return summary
    
    def create_statistics_data(self, data):
        """Create statistics data for Excel export"""
        stats = []
        
        # Salary statistics
        salaries = [row['Salary'] for row in data]
        stats.append({
            'Metric': 'Salary',
            'Average': round(sum(salaries) / len(salaries), 2),
            'Min': min(salaries),
            'Max': max(salaries),
            'Count': len(salaries)
        })
        
        # Performance statistics
        scores = [row['Performance_Score'] for row in data]
        stats.append({
            'Metric': 'Performance Score',
            'Average': round(sum(scores) / len(scores), 2),
            'Min': min(scores),
            'Max': max(scores),
            'Count': len(scores)
        })
        
        return stats
    
    def export_summary(self):
        """Export summary report"""
        try:
            data = self.get_filtered_data()
            if not data:
                messagebox.showwarning("Warning", "No data to summarize")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                summary_data = self.create_summary_data(data)
                stats_data = self.create_statistics_data(data)
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
                    pd.DataFrame(stats_data).to_excel(writer, sheet_name='Statistics', index=False)
                
                messagebox.showinfo("Success", f"Summary exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Summary export failed: {e}")
    
    def export_statistics(self):
        """Export detailed statistics"""
        try:
            data = self.get_filtered_data()
            if not data:
                messagebox.showwarning("Warning", "No data for statistics")
                return
            
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if filename:
                stats_data = self.create_statistics_data(data)
                
                with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                    pd.DataFrame(stats_data).to_excel(writer, sheet_name='Statistics', index=False)
                
                messagebox.showinfo("Success", f"Statistics exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Statistics export failed: {e}")
    
    def add_recent_export(self, filename, format_type, record_count):
        """Add export to recent list"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        display_text = f"{timestamp} - {format_type} ({record_count} records)"
        
        self.recent_listbox.insert(0, display_text)
        
        # Keep only last 10 exports
        if self.recent_listbox.size() > 10:
            self.recent_listbox.delete(10)

def main():
    root = tk.Tk()
    app = DataExporter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

"""
Chapter 6: Advanced Widgets for Dashboards
Example: Treeview for Tabular Data

This example demonstrates how to use Treeview widgets for displaying
and managing tabular data in dashboards.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime, timedelta

# =============================================================================
# SAMPLE DATA GENERATION
# =============================================================================

def generate_sample_data(num_records=50):
    """Generate sample data for the Treeview"""
    names = [
        "John Smith", "Emma Johnson", "Michael Brown", "Sarah Davis", "David Wilson",
        "Lisa Anderson", "James Taylor", "Jennifer Martinez", "Robert Garcia", "Amanda Rodriguez",
        "William Lopez", "Michelle Gonzalez", "Christopher Perez", "Stephanie Torres", "Daniel Moore",
        "Nicole Jackson", "Matthew Martin", "Ashley Lee", "Joshua Thompson", "Brittany White",
        "Andrew Harris", "Samantha Clark", "Ryan Lewis", "Megan Hall", "Kevin Young",
        "Rachel Allen", "Brian King", "Lauren Wright", "Jason Green", "Amber Baker",
        "Eric Adams", "Kimberly Nelson", "Steven Carter", "Rebecca Mitchell", "Timothy Perez",
        "Heather Roberts", "Jeffrey Turner", "Laura Phillips", "Mark Campbell", "Crystal Parker",
        "Scott Evans", "Tiffany Edwards", "Benjamin Collins", "Monica Stewart", "Gregory Sanchez",
        "Melissa Morris", "Frank Rogers", "Angela Reed", "Raymond Cook", "Diana Morgan"
    ]
    
    cities = [
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
        "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
        "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
        "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington",
        "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
        "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
        "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
        "Mesa", "Kansas City", "Atlanta", "Long Beach", "Colorado Springs",
        "Raleigh", "Miami", "Virginia Beach", "Omaha", "Oakland",
        "Minneapolis", "Tampa", "Tulsa", "Arlington", "New Orleans"
    ]
    
    departments = ["Engineering", "Sales", "Marketing", "HR", "Finance", "IT", "Operations"]
    statuses = ["Active", "Inactive", "Pending", "Suspended"]
    
    data = []
    for i in range(num_records):
        name = random.choice(names)
        age = random.randint(22, 65)
        city = random.choice(cities)
        department = random.choice(departments)
        salary = random.randint(30000, 120000)
        status = random.choice(statuses)
        hire_date = datetime.now() - timedelta(days=random.randint(30, 3650))
        
        data.append({
            'id': i + 1,
            'name': name,
            'age': age,
            'city': city,
            'department': department,
            'salary': salary,
            'status': status,
            'hire_date': hire_date.strftime('%Y-%m-%d')
        })
    
    return data

# =============================================================================
# TREEVIEW WIDGET CLASSES
# =============================================================================

class DataTable(tk.Frame):
    """A reusable data table widget using Treeview"""
    
    def __init__(self, parent, columns, title="Data Table", **kwargs):
        super().__init__(parent, **kwargs)
        self.columns = columns
        self.title = title
        self.data = []
        self.filtered_data = []
        self.sort_column = None
        self.sort_reverse = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the data table interface"""
        # Title frame
        title_frame = tk.Frame(self)
        title_frame.pack(fill="x", padx=5, pady=5)
        
        # Title
        title_label = tk.Label(
            title_frame,
            text=self.title,
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(side="left")
        
        # Control buttons
        button_frame = tk.Frame(title_frame)
        button_frame.pack(side="right")
        
        # Add button
        add_btn = tk.Button(
            button_frame,
            text="Add Row",
            command=self.add_row_dialog,
            width=10
        )
        add_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = tk.Button(
            button_frame,
            text="Delete Row",
            command=self.delete_selected_row,
            width=10
        )
        delete_btn.pack(side="left", padx=2)
        
        # Refresh button
        refresh_btn = tk.Button(
            button_frame,
            text="Refresh",
            command=self.refresh_data,
            width=10
        )
        refresh_btn.pack(side="left", padx=2)
        
        # Search frame
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=5, pady=5)
        
        # Search label
        search_label = tk.Label(search_frame, text="Search:", font=("Arial", 10))
        search_label.pack(side="left", padx=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_data)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(0, 10))
        
        # Clear search button
        clear_btn = tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search,
            width=8
        )
        clear_btn.pack(side="left")
        
        # Treeview frame
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create Treeview
        self.tree = ttk.Treeview(tree_frame, columns=self.columns, show="headings", height=15)
        
        # Configure columns
        for col in self.columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=100, minwidth=80)
        
        # Configure specific column widths
        self.tree.column("Name", width=150)
        self.tree.column("City", width=120)
        self.tree.column("Department", width=100)
        self.tree.column("Salary", width=80)
        self.tree.column("Hire Date", width=100)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        # Bind double-click event for editing
        self.tree.bind("<Double-1>", self.edit_row)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(fill="x", padx=5, pady=2)
    
    def load_data(self, data):
        """Load data into the table"""
        self.data = data
        self.filtered_data = data.copy()
        self.refresh_display()
    
    def refresh_display(self):
        """Refresh the table display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert filtered data
        for row in self.filtered_data:
            values = [row.get(col, "") for col in self.columns]
            self.tree.insert("", "end", values=values)
        
        # Update status
        self.status_var.set(f"Showing {len(self.filtered_data)} of {len(self.data)} records")
    
    def sort_by_column(self, column):
        """Sort data by column"""
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # Sort the filtered data
        self.filtered_data.sort(
            key=lambda x: x.get(column, ""),
            reverse=self.sort_reverse
        )
        
        # Update column heading to show sort direction
        for col in self.columns:
            if col == column:
                direction = " ▼" if self.sort_reverse else " ▲"
                self.tree.heading(col, text=f"{col}{direction}")
            else:
                self.tree.heading(col, text=col)
        
        self.refresh_display()
    
    def filter_data(self, *args):
        """Filter data based on search term"""
        search_term = self.search_var.get().lower()
        
        if search_term:
            self.filtered_data = [
                row for row in self.data
                if any(search_term in str(value).lower() for value in row.values())
            ]
        else:
            self.filtered_data = self.data.copy()
        
        # Reset sorting
        self.sort_column = None
        self.sort_reverse = False
        
        # Clear sort indicators
        for col in self.columns:
            self.tree.heading(col, text=col)
        
        self.refresh_display()
    
    def clear_search(self):
        """Clear the search filter"""
        self.search_var.set("")
    
    def add_row_dialog(self):
        """Open dialog to add a new row"""
        dialog = AddRowDialog(self, self.columns)
        self.wait_window(dialog)
        
        if dialog.result:
            new_row = dialog.result
            new_row['id'] = len(self.data) + 1
            self.data.append(new_row)
            self.filter_data()
    
    def delete_selected_row(self):
        """Delete the selected row"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected row?"):
            # Get the selected item's values
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Find and remove from data
            for i, row in enumerate(self.data):
                if [row.get(col, "") for col in self.columns] == list(values):
                    del self.data[i]
                    break
            
            self.filter_data()
    
    def edit_row(self, event):
        """Edit the double-clicked row"""
        selected = self.tree.selection()
        if not selected:
            return
        
        # Get the selected item's values
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Create edit dialog
        dialog = EditRowDialog(self, self.columns, values)
        self.wait_window(dialog)
        
        if dialog.result:
            # Find and update the row in data
            for i, row in enumerate(self.data):
                if [row.get(col, "") for col in self.columns] == list(values):
                    for j, col in enumerate(self.columns):
                        self.data[i][col] = dialog.result[j]
                    break
            
            self.filter_data()
    
    def refresh_data(self):
        """Refresh data (regenerate sample data)"""
        new_data = generate_sample_data(len(self.data))
        self.load_data(new_data)


class AddRowDialog(tk.Toplevel):
    """Dialog for adding a new row"""
    
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.columns = columns
        self.result = None
        
        self.title("Add New Row")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        title_label = tk.Label(self, text="Add New Row", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create entry fields
        self.entries = {}
        for i, col in enumerate(self.columns):
            if col == "ID":  # Skip ID field
                continue
            
            # Label
            label = tk.Label(form_frame, text=f"{col}:", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            # Entry
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.entries[col] = entry
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # Buttons
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel, width=10)
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = tk.Button(button_frame, text="Save", command=self.save, width=10)
        save_btn.pack(side="right", padx=5)
        
        # Bind Enter key to save
        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.cancel())
    
    def save(self):
        """Save the new row"""
        # Collect values
        values = {}
        for col in self.columns:
            if col == "ID":
                continue
            values[col] = self.entries[col].get()
        
        self.result = values
        self.destroy()
    
    def cancel(self):
        """Cancel the operation"""
        self.result = None
        self.destroy()


class EditRowDialog(tk.Toplevel):
    """Dialog for editing an existing row"""
    
    def __init__(self, parent, columns, values):
        super().__init__(parent)
        self.columns = columns
        self.values = values
        self.result = None
        
        self.title("Edit Row")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center the dialog
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        title_label = tk.Label(self, text="Edit Row", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Form frame
        form_frame = tk.Frame(self)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create entry fields
        self.entries = {}
        for i, col in enumerate(self.columns):
            if col == "ID":  # Skip ID field
                continue
            
            # Label
            label = tk.Label(form_frame, text=f"{col}:", anchor="w")
            label.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            # Entry
            entry = tk.Entry(form_frame, width=30)
            entry.insert(0, self.values[i])
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=2)
            self.entries[col] = entry
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # Buttons
        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel, width=10)
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = tk.Button(button_frame, text="Save", command=self.save, width=10)
        save_btn.pack(side="right", padx=5)
        
        # Bind Enter key to save
        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.cancel())
    
    def save(self):
        """Save the edited row"""
        # Collect values
        values = []
        for col in self.columns:
            if col == "ID":
                values.append(self.values[self.columns.index(col)])
            else:
                values.append(self.entries[col].get())
        
        self.result = values
        self.destroy()
    
    def cancel(self):
        """Cancel the operation"""
        self.result = None
        self.destroy()


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class TreeviewExample:
    """Main application demonstrating Treeview usage"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview Example - Advanced Data Table")
        self.root.geometry("1200x800")
        
        self.create_widgets()
        self.load_sample_data()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Advanced Data Table with Treeview",
            font=("Arial", 18, "bold"),
            fg="#2C3E50",
            bg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="• Double-click rows to edit • Use search to filter data • Click column headers to sort • Use buttons to add/delete rows",
            font=("Arial", 10),
            fg="#7F8C8D",
            bg="#ECF0F1"
        )
        instructions.pack(pady=10)
        
        # Create data table
        columns = ("ID", "Name", "Age", "City", "Department", "Salary", "Status", "Hire Date")
        self.data_table = DataTable(self.root, columns, title="Employee Data")
        self.data_table.pack(fill="both", expand=True, padx=20, pady=10)
    
    def load_sample_data(self):
        """Load sample data into the table"""
        sample_data = generate_sample_data(50)
        self.data_table.load_data(sample_data)


def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the Treeview example
    app = TreeviewExample(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

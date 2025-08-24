"""
Chapter 6: Advanced Widgets for Dashboards
Example: Notebook and Tabbed Interfaces

This example demonstrates how to create professional tabbed interfaces
using the Notebook widget for organizing dashboard content.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime, timedelta

# =============================================================================
# TAB CONTENT WIDGETS
# =============================================================================

class DashboardTab(tk.Frame):
    """Base class for dashboard tab content"""
    
    def __init__(self, parent, title="Dashboard Tab", **kwargs):
        super().__init__(parent, **kwargs)
        self.title = title
        self.create_widgets()
    
    def create_widgets(self):
        """Create the tab content - to be implemented by subclasses"""
        pass
    
    def refresh_content(self):
        """Refresh tab content - to be implemented by subclasses"""
        pass


class OverviewTab(DashboardTab):
    """Overview tab with summary information"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Overview", **kwargs)
    
    def create_widgets(self):
        """Create overview content"""
        # Title
        title_label = tk.Label(
            self,
            text="Dashboard Overview",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Summary cards frame
        cards_frame = tk.Frame(self)
        cards_frame.pack(fill="x", padx=20, pady=10)
        
        # Create summary cards
        self.create_summary_card(cards_frame, "Total Users", "1,234", "#3498DB", 0, 0)
        self.create_summary_card(cards_frame, "Active Sessions", "567", "#2ECC71", 0, 1)
        self.create_summary_card(cards_frame, "Revenue", "$45,678", "#E74C3C", 0, 2)
        self.create_summary_card(cards_frame, "Orders", "890", "#F39C12", 0, 3)
        
        # Recent activity frame
        activity_frame = tk.Frame(self)
        activity_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Activity title
        activity_title = tk.Label(
            activity_frame,
            text="Recent Activity",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        activity_title.pack(anchor="w", pady=(0, 10))
        
        # Activity list
        self.activity_listbox = tk.Listbox(
            activity_frame,
            height=10,
            font=("Arial", 10),
            selectmode="none"
        )
        self.activity_listbox.pack(fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(activity_frame, orient="vertical", command=self.activity_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.activity_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Load sample activity
        self.load_recent_activity()
    
    def create_summary_card(self, parent, title, value, color, row, col):
        """Create a summary card widget"""
        card = tk.Frame(parent, relief="raised", borderwidth=2, bg=color)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Title
        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 12, "bold"),
            fg="white",
            bg=color
        )
        title_label.pack(pady=(10, 5))
        
        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 18, "bold"),
            fg="white",
            bg=color
        )
        value_label.pack(pady=(0, 10))
        
        # Configure grid weights
        parent.grid_columnconfigure(col, weight=1)
    
    def load_recent_activity(self):
        """Load sample recent activity"""
        activities = [
            "New user registration: john.doe@example.com",
            "Order #12345 completed - $299.99",
            "System backup completed successfully",
            "New product added: Premium Widget",
            "User login: admin@company.com",
            "Database maintenance completed",
            "Email campaign sent to 1,000 subscribers",
            "Payment processed: Order #12344",
            "System update installed: v2.1.0",
            "New customer support ticket created"
        ]
        
        for activity in activities:
            timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
            time_str = timestamp.strftime("%H:%M")
            self.activity_listbox.insert("end", f"[{time_str}] {activity}")
    
    def refresh_content(self):
        """Refresh overview content"""
        # Clear activity list
        self.activity_listbox.delete(0, tk.END)
        # Reload activity
        self.load_recent_activity()


class DataTab(DashboardTab):
    """Data management tab with Treeview"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Data Management", **kwargs)
        self.data = self.generate_sample_data()
    
    def create_widgets(self):
        """Create data management content"""
        # Title
        title_label = tk.Label(
            self,
            text="Data Management",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Control frame
        control_frame = tk.Frame(self)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Add button
        add_btn = tk.Button(
            control_frame,
            text="Add Record",
            command=self.add_record,
            width=12
        )
        add_btn.pack(side="left", padx=5)
        
        # Delete button
        delete_btn = tk.Button(
            control_frame,
            text="Delete Selected",
            command=self.delete_selected,
            width=12
        )
        delete_btn.pack(side="left", padx=5)
        
        # Refresh button
        refresh_btn = tk.Button(
            control_frame,
            text="Refresh",
            command=self.refresh_content,
            width=12
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Search frame
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)
        
        search_label = tk.Label(search_frame, text="Search:", font=("Arial", 10))
        search_label.pack(side="left", padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_data)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(0, 10))
        
        # Data table frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create Treeview
        columns = ("ID", "Name", "Category", "Value", "Status", "Date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=80)
        
        # Configure specific widths
        self.tree.column("Name", width=150)
        self.tree.column("Category", width=120)
        self.tree.column("Date", width=120)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)
        
        # Load data
        self.load_data()
    
    def generate_sample_data(self):
        """Generate sample data"""
        categories = ["Product", "Service", "Support", "Marketing", "Sales"]
        statuses = ["Active", "Inactive", "Pending", "Completed"]
        names = [
            "Widget A", "Service B", "Support Ticket", "Campaign C", "Sale D",
            "Product E", "Consultation", "Bug Report", "Email Campaign", "Deal F"
        ]
        
        data = []
        for i in range(20):
            data.append({
                'id': i + 1,
                'name': random.choice(names),
                'category': random.choice(categories),
                'value': random.randint(100, 5000),
                'status': random.choice(statuses),
                'date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            })
        
        return data
    
    def load_data(self):
        """Load data into Treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert data
        for row in self.data:
            values = [row['id'], row['name'], row['category'], 
                     f"${row['value']}", row['status'], row['date']]
            self.tree.insert("", "end", values=values)
    
    def filter_data(self, *args):
        """Filter data based on search term"""
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter and insert data
        for row in self.data:
            if search_term in str(row).lower():
                values = [row['id'], row['name'], row['category'], 
                         f"${row['value']}", row['status'], row['date']]
                self.tree.insert("", "end", values=values)
    
    def add_record(self):
        """Add a new record"""
        # Simple add dialog
        dialog = tk.Toplevel(self)
        dialog.title("Add Record")
        dialog.geometry("300x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(dialog, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        category_entry = tk.Entry(dialog)
        category_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", 
                 command=lambda: self.save_record(name_entry.get(), category_entry.get(), dialog)).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cancel", 
                 command=dialog.destroy).pack(side="left", padx=5)
    
    def save_record(self, name, category, dialog):
        """Save the new record"""
        if name and category:
            new_record = {
                'id': len(self.data) + 1,
                'name': name,
                'category': category,
                'value': random.randint(100, 5000),
                'status': 'Active',
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            self.data.append(new_record)
            self.load_data()
            dialog.destroy()
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")
    
    def delete_selected(self):
        """Delete selected record"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected record?"):
            # Get selected item values
            item = self.tree.item(selected[0])
            values = item['values']
            
            # Remove from data
            for i, row in enumerate(self.data):
                if row['id'] == values[0]:
                    del self.data[i]
                    break
            
            self.load_data()
    
    def refresh_content(self):
        """Refresh data content"""
        self.data = self.generate_sample_data()
        self.load_data()


class SettingsTab(DashboardTab):
    """Settings tab with configuration options"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="Settings", **kwargs)
        self.settings = {
            'auto_refresh': tk.BooleanVar(value=True),
            'notifications': tk.BooleanVar(value=True),
            'theme': tk.StringVar(value="light"),
            'refresh_interval': tk.StringVar(value="30"),
            'max_records': tk.StringVar(value="1000")
        }
    
    def create_widgets(self):
        """Create settings content"""
        # Title
        title_label = tk.Label(
            self,
            text="Dashboard Settings",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Settings frame
        settings_frame = tk.Frame(self)
        settings_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # General settings section
        self.create_section(settings_frame, "General Settings", 0)
        
        # Auto refresh setting
        auto_refresh_cb = tk.Checkbutton(
            settings_frame,
            text="Enable auto-refresh",
            variable=self.settings['auto_refresh'],
            font=("Arial", 10)
        )
        auto_refresh_cb.grid(row=1, column=0, sticky="w", padx=20, pady=5)
        
        # Refresh interval
        tk.Label(settings_frame, text="Refresh interval (seconds):", 
                font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=20, pady=5)
        refresh_entry = tk.Entry(settings_frame, textvariable=self.settings['refresh_interval'], width=10)
        refresh_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        
        # Notifications section
        self.create_section(settings_frame, "Notifications", 4)
        
        # Notifications setting
        notifications_cb = tk.Checkbutton(
            settings_frame,
            text="Enable notifications",
            variable=self.settings['notifications'],
            font=("Arial", 10)
        )
        notifications_cb.grid(row=5, column=0, sticky="w", padx=20, pady=5)
        
        # Display section
        self.create_section(settings_frame, "Display", 7)
        
        # Theme selection
        tk.Label(settings_frame, text="Theme:", 
                font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=20, pady=5)
        theme_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.settings['theme'],
            values=["light", "dark", "blue", "green"],
            state="readonly",
            width=15
        )
        theme_combo.grid(row=8, column=1, sticky="w", padx=10, pady=5)
        
        # Max records
        tk.Label(settings_frame, text="Max records to display:", 
                font=("Arial", 10)).grid(row=9, column=0, sticky="w", padx=20, pady=5)
        max_records_entry = tk.Entry(settings_frame, textvariable=self.settings['max_records'], width=10)
        max_records_entry.grid(row=9, column=1, sticky="w", padx=10, pady=5)
        
        # Buttons frame
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=40, pady=20)
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="Save Settings",
            command=self.save_settings,
            width=15
        )
        save_btn.pack(side="right", padx=5)
        
        # Reset button
        reset_btn = tk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self.reset_settings,
            width=15
        )
        reset_btn.pack(side="right", padx=5)
    
    def create_section(self, parent, title, row):
        """Create a settings section"""
        section_label = tk.Label(
            parent,
            text=title,
            font=("Arial", 12, "bold"),
            fg="#2C3E50"
        )
        section_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 10))
        
        # Separator line
        separator = ttk.Separator(parent, orient="horizontal")
        separator.grid(row=row+1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
    def save_settings(self):
        """Save current settings"""
        # In a real application, you would save to a configuration file
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings to defaults?"):
            self.settings['auto_refresh'].set(True)
            self.settings['notifications'].set(True)
            self.settings['theme'].set("light")
            self.settings['refresh_interval'].set("30")
            self.settings['max_records'].set("1000")
            messagebox.showinfo("Success", "Settings reset to defaults!")
    
    def refresh_content(self):
        """Refresh settings content"""
        # Settings don't need refresh, but we implement for consistency
        pass


# =============================================================================
# NOTEBOOK DASHBOARD
# =============================================================================

class NotebookDashboard(tk.Frame):
    """Main dashboard with tabbed interface"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.tabs = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Create the notebook dashboard"""
        # Title
        title_label = tk.Label(
            self,
            text="Professional Dashboard",
            font=("Arial", 18, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Create notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_tabs()
        
        # Tab control frame
        control_frame = tk.Frame(self)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        # Add tab button
        add_tab_btn = tk.Button(
            control_frame,
            text="Add Custom Tab",
            command=self.add_custom_tab,
            width=15
        )
        add_tab_btn.pack(side="left", padx=5)
        
        # Remove tab button
        remove_tab_btn = tk.Button(
            control_frame,
            text="Remove Current Tab",
            command=self.remove_current_tab,
            width=15
        )
        remove_tab_btn.pack(side="left", padx=5)
        
        # Refresh all button
        refresh_all_btn = tk.Button(
            control_frame,
            text="Refresh All Tabs",
            command=self.refresh_all_tabs,
            width=15
        )
        refresh_all_btn.pack(side="right", padx=5)
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def create_tabs(self):
        """Create the main tabs"""
        # Overview tab
        overview_tab = OverviewTab(self.notebook)
        self.notebook.add(overview_tab, text="Overview")
        self.tabs["Overview"] = overview_tab
        
        # Data tab
        data_tab = DataTab(self.notebook)
        self.notebook.add(data_tab, text="Data Management")
        self.tabs["Data Management"] = data_tab
        
        # Settings tab
        settings_tab = SettingsTab(self.notebook)
        self.notebook.add(settings_tab, text="Settings")
        self.tabs["Settings"] = settings_tab
    
    def add_custom_tab(self):
        """Add a custom tab"""
        tab_name = f"Custom Tab {len(self.tabs) + 1}"
        
        # Create custom tab content
        custom_tab = tk.Frame(self.notebook)
        
        # Add content to custom tab
        title_label = tk.Label(
            custom_tab,
            text=f"Custom Tab Content",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=50)
        
        content_label = tk.Label(
            custom_tab,
            text="This is a dynamically added tab.\nYou can add any content here.",
            font=("Arial", 12),
            fg="#7F8C8D"
        )
        content_label.pack(pady=20)
        
        # Add to notebook
        self.notebook.add(custom_tab, text=tab_name)
        self.tabs[tab_name] = custom_tab
    
    def remove_current_tab(self):
        """Remove the currently selected tab"""
        current_tab = self.notebook.select()
        if current_tab:
            tab_id = self.notebook.index(current_tab)
            tab_text = self.notebook.tab(tab_id, "text")
            
            # Don't remove the first three tabs
            if tab_text in ["Overview", "Data Management", "Settings"]:
                messagebox.showwarning("Warning", "Cannot remove main tabs!")
                return
            
            if messagebox.askyesno("Confirm Remove", f"Are you sure you want to remove '{tab_text}'?"):
                self.notebook.forget(tab_id)
                if tab_text in self.tabs:
                    del self.tabs[tab_text]
    
    def refresh_all_tabs(self):
        """Refresh all tabs"""
        for tab_name, tab in self.tabs.items():
            if hasattr(tab, 'refresh_content'):
                tab.refresh_content()
        
        messagebox.showinfo("Success", "All tabs refreshed!")
    
    def on_tab_changed(self, event):
        """Handle tab change events"""
        current_tab = self.notebook.select()
        if current_tab:
            tab_id = self.notebook.index(current_tab)
            tab_text = self.notebook.tab(tab_id, "text")
            print(f"Switched to tab: {tab_text}")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class NotebookDemo:
    """Main application demonstrating Notebook usage"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook Demo - Tabbed Dashboard")
        self.root.geometry("1200x800")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Create dashboard
        self.dashboard = NotebookDashboard(self.root)
        self.dashboard.pack(fill="both", expand=True)


def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the notebook demo
    app = NotebookDemo(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

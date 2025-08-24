"""
Chapter 6: Advanced Widgets for Dashboards
Example: Advanced Form Widgets

This example demonstrates how to create sophisticated form widgets
with validation, dynamic fields, auto-complete, and form state management.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import json
from datetime import datetime

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
    
    def format(self, value):
        """Format the input value - to be implemented by subclasses"""
        return value

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

class PhoneValidator(Validator):
    """Validator for phone numbers"""
    
    def __init__(self, error_message="Invalid phone number"):
        super().__init__(error_message)
    
    def validate(self, value):
        if not value:
            return True, None  # Allow empty if not required
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', value)
        if len(digits_only) < 10:
            return False, self.error_message
        return True, None
    
    def format(self, value):
        """Format phone number as (XXX) XXX-XXXX"""
        if not value:
            return value
        
        digits_only = re.sub(r'\D', '', value)
        if len(digits_only) >= 10:
            return f"({digits_only[:3]}) {digits_only[3:6]}-{digits_only[6:10]}"
        return value

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

class AutoCompleteEntry(tk.Frame):
    """Entry widget with auto-complete functionality"""
    
    def __init__(self, parent, label="", suggestions=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.label = label
        self.suggestions = suggestions or []
        self.filtered_suggestions = []
        self.listbox = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create the auto-complete entry interface"""
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
        
        # Bind events
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        self.entry.bind("<Down>", self.on_down)
        self.entry.bind("<Up>", self.on_up)
        self.entry.bind("<Return>", self.on_return)
    
    def get_value(self):
        """Get the current value"""
        return self.entry.get()
    
    def set_value(self, value):
        """Set the current value"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def set_suggestions(self, suggestions):
        """Set the suggestion list"""
        self.suggestions = suggestions
    
    def on_key_release(self, event):
        """Handle key release events"""
        if event.keysym in ['Down', 'Up', 'Return']:
            return
        
        value = self.get_value()
        if value:
            self.filtered_suggestions = [
                suggestion for suggestion in self.suggestions
                if suggestion.lower().startswith(value.lower())
            ]
            self.show_suggestions()
        else:
            self.hide_suggestions()
    
    def show_suggestions(self):
        """Show the suggestion listbox"""
        if not self.filtered_suggestions:
            self.hide_suggestions()
            return
        
        # Create listbox if it doesn't exist
        if not self.listbox:
            self.listbox = tk.Listbox(
                self,
                height=min(len(self.filtered_suggestions), 5),
                bg="white",
                relief="solid",
                borderwidth=1
            )
            self.listbox.pack(fill="x", pady=(2, 0))
        
        # Update listbox content
        self.listbox.delete(0, tk.END)
        for suggestion in self.filtered_suggestions[:5]:  # Limit to 5 suggestions
            self.listbox.insert(tk.END, suggestion)
        
        # Bind selection event
        self.listbox.bind("<Button-1>", self.on_suggestion_select)
    
    def hide_suggestions(self):
        """Hide the suggestion listbox"""
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None
    
    def on_focus_out(self, event):
        """Handle focus out events"""
        # Delay hiding to allow for listbox clicks
        self.after(150, self.hide_suggestions)
    
    def on_down(self, event):
        """Handle down arrow key"""
        if self.listbox and self.filtered_suggestions:
            current_selection = self.listbox.curselection()
            if current_selection:
                next_index = (current_selection[0] + 1) % len(self.filtered_suggestions)
            else:
                next_index = 0
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(next_index)
            self.listbox.see(next_index)
        return "break"
    
    def on_up(self, event):
        """Handle up arrow key"""
        if self.listbox and self.filtered_suggestions:
            current_selection = self.listbox.curselection()
            if current_selection:
                prev_index = (current_selection[0] - 1) % len(self.filtered_suggestions)
            else:
                prev_index = len(self.filtered_suggestions) - 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(prev_index)
            self.listbox.see(prev_index)
        return "break"
    
    def on_return(self, event):
        """Handle return key"""
        if self.listbox and self.listbox.curselection():
            self.on_suggestion_select(None)
        return "break"
    
    def on_suggestion_select(self, event):
        """Handle suggestion selection"""
        if self.listbox and self.listbox.curselection():
            selected_index = self.listbox.curselection()[0]
            selected_value = self.filtered_suggestions[selected_index]
            self.set_value(selected_value)
            self.hide_suggestions()

class DynamicForm(tk.Frame):
    """Dynamic form with conditional fields"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.fields = {}
        self.conditional_fields = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Create the dynamic form interface"""
        # Title
        title_label = tk.Label(
            self,
            text="Dynamic Form with Conditional Fields",
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=20)
        
        # Form frame
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create form fields
        self.create_form_fields()
    
    def create_form_fields(self):
        """Create the form fields"""
        # Basic information section
        basic_frame = tk.LabelFrame(self.form_frame, text="Basic Information", font=("Arial", 12, "bold"))
        basic_frame.pack(fill="x", pady=10)
        
        # Name field
        self.fields['name'] = ValidatedEntry(
            basic_frame,
            label="Full Name *",
            validators=[RequiredValidator()]
        )
        self.fields['name'].pack(fill="x", padx=10, pady=5)
        
        # Email field
        self.fields['email'] = ValidatedEntry(
            basic_frame,
            label="Email Address",
            validators=[EmailValidator()]
        )
        self.fields['email'].pack(fill="x", padx=10, pady=5)
        
        # Phone field
        self.fields['phone'] = ValidatedEntry(
            basic_frame,
            label="Phone Number",
            validators=[PhoneValidator()]
        )
        self.fields['phone'].pack(fill="x", padx=10, pady=5)
        
        # Age field
        self.fields['age'] = ValidatedEntry(
            basic_frame,
            label="Age",
            validators=[NumberValidator(min_value=0, max_value=120)]
        )
        self.fields['age'].pack(fill="x", padx=10, pady=5)
        
        # User type selection
        user_type_frame = tk.Frame(basic_frame)
        user_type_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(user_type_frame, text="User Type *").pack(side="left")
        
        self.user_type_var = tk.StringVar(value="individual")
        individual_rb = tk.Radiobutton(
            user_type_frame,
            text="Individual",
            variable=self.user_type_var,
            value="individual",
            command=self.on_user_type_change
        )
        individual_rb.pack(side="left", padx=(10, 5))
        
        business_rb = tk.Radiobutton(
            user_type_frame,
            text="Business",
            variable=self.user_type_var,
            value="business",
            command=self.on_user_type_change
        )
        business_rb.pack(side="left", padx=5)
        
        # Conditional fields frame
        self.conditional_frame = tk.LabelFrame(self.form_frame, text="Additional Information", font=("Arial", 12, "bold"))
        self.conditional_frame.pack(fill="x", pady=10)
        
        # Create conditional fields
        self.create_conditional_fields()
        
        # Buttons frame
        button_frame = tk.Frame(self.form_frame)
        button_frame.pack(fill="x", pady=20)
        
        # Submit button
        submit_btn = tk.Button(
            button_frame,
            text="Submit Form",
            command=self.submit_form,
            width=15
        )
        submit_btn.pack(side="right", padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            width=15
        )
        clear_btn.pack(side="right", padx=5)
        
        # Load sample data button
        load_btn = tk.Button(
            button_frame,
            text="Load Sample",
            command=self.load_sample_data,
            width=15
        )
        load_btn.pack(side="left", padx=5)
    
    def create_conditional_fields(self):
        """Create conditional form fields"""
        # Individual-specific fields
        self.conditional_fields['individual'] = {}
        
        # Auto-complete for interests
        interests_suggestions = [
            "Reading", "Writing", "Cooking", "Gardening", "Photography",
            "Painting", "Music", "Sports", "Travel", "Technology",
            "Science", "History", "Art", "Dance", "Fitness"
        ]
        
        self.conditional_fields['individual']['interests'] = AutoCompleteEntry(
            self.conditional_frame,
            label="Interests",
            suggestions=interests_suggestions
        )
        
        # Business-specific fields
        self.conditional_fields['business'] = {}
        
        # Company name
        self.conditional_fields['business']['company'] = ValidatedEntry(
            self.conditional_frame,
            label="Company Name *",
            validators=[RequiredValidator()]
        )
        
        # Industry auto-complete
        industry_suggestions = [
            "Technology", "Healthcare", "Finance", "Education", "Retail",
            "Manufacturing", "Real Estate", "Transportation", "Energy", "Media",
            "Consulting", "Legal", "Marketing", "Construction", "Food & Beverage"
        ]
        
        self.conditional_fields['business']['industry'] = AutoCompleteEntry(
            self.conditional_frame,
            label="Industry",
            suggestions=industry_suggestions
        )
        
        # Employee count
        self.conditional_fields['business']['employees'] = ValidatedEntry(
            self.conditional_frame,
            label="Number of Employees",
            validators=[NumberValidator(min_value=1, max_value=100000)]
        )
        
        # Initially show individual fields
        self.show_conditional_fields("individual")
    
    def on_user_type_change(self):
        """Handle user type change"""
        user_type = self.user_type_var.get()
        self.show_conditional_fields(user_type)
    
    def show_conditional_fields(self, user_type):
        """Show fields for the specified user type"""
        # Hide all conditional fields
        for fields in self.conditional_fields.values():
            for field in fields.values():
                field.pack_forget()
        
        # Show fields for the selected user type
        if user_type in self.conditional_fields:
            for field in self.conditional_fields[user_type].values():
                field.pack(fill="x", padx=10, pady=5)
    
    def validate_form(self):
        """Validate all form fields"""
        errors = []
        
        # Validate basic fields
        for field_name, field in self.fields.items():
            if hasattr(field, 'validate'):
                if not field.validate():
                    errors.append(f"{field.label or field_name}: validation failed")
        
        # Validate conditional fields
        user_type = self.user_type_var.get()
        if user_type in self.conditional_fields:
            for field_name, field in self.conditional_fields[user_type].items():
                if hasattr(field, 'validate'):
                    if not field.validate():
                        errors.append(f"{field.label or field_name}: validation failed")
        
        return errors
    
    def get_form_data(self):
        """Get all form data as a dictionary"""
        data = {
            'user_type': self.user_type_var.get(),
            'timestamp': datetime.now().isoformat()
        }
        
        # Get basic field values
        for field_name, field in self.fields.items():
            if hasattr(field, 'get_value'):
                data[field_name] = field.get_value()
            elif hasattr(field, 'get'):
                data[field_name] = field.get()
        
        # Get conditional field values
        user_type = self.user_type_var.get()
        if user_type in self.conditional_fields:
            data[user_type] = {}
            for field_name, field in self.conditional_fields[user_type].items():
                if hasattr(field, 'get_value'):
                    data[user_type][field_name] = field.get_value()
                elif hasattr(field, 'get'):
                    data[user_type][field_name] = field.get()
        
        return data
    
    def submit_form(self):
        """Submit the form"""
        errors = self.validate_form()
        
        if errors:
            error_message = "Please fix the following errors:\n\n" + "\n".join(errors)
            messagebox.showerror("Validation Errors", error_message)
            return
        
        # Get form data
        form_data = self.get_form_data()
        
        # Show success message with data
        success_message = f"Form submitted successfully!\n\nData:\n{json.dumps(form_data, indent=2)}"
        messagebox.showinfo("Success", success_message)
        
        # Clear form after successful submission
        self.clear_form()
    
    def clear_form(self):
        """Clear all form fields"""
        # Clear basic fields
        for field in self.fields.values():
            if hasattr(field, 'set_value'):
                field.set_value("")
            elif hasattr(field, 'delete'):
                field.delete(0, tk.END)
        
        # Clear conditional fields
        for fields in self.conditional_fields.values():
            for field in fields.values():
                if hasattr(field, 'set_value'):
                    field.set_value("")
                elif hasattr(field, 'delete'):
                    field.delete(0, tk.END)
        
        # Reset user type
        self.user_type_var.set("individual")
        self.show_conditional_fields("individual")
    
    def load_sample_data(self):
        """Load sample data into the form"""
        # Clear form first
        self.clear_form()
        
        # Set sample data
        self.fields['name'].set_value("John Doe")
        self.fields['email'].set_value("john.doe@example.com")
        self.fields['phone'].set_value("(555) 123-4567")
        self.fields['age'].set_value("30")
        
        # Set user type to business
        self.user_type_var.set("business")
        self.show_conditional_fields("business")
        
        # Set business sample data
        self.conditional_fields['business']['company'].set_value("Acme Corporation")
        self.conditional_fields['business']['industry'].set_value("Technology")
        self.conditional_fields['business']['employees'].set_value("150")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

class AdvancedFormsDemo:
    """Main application demonstrating advanced form features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Forms Demo")
        self.root.geometry("800x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create the main application widgets"""
        # Configure main window
        self.root.configure(bg="#ECF0F1")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.root, bg="#ECF0F1")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ECF0F1")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create dynamic form
        self.dynamic_form = DynamicForm(scrollable_frame)
        self.dynamic_form.pack(fill="both", expand=True)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


def main():
    """Main application entry point"""
    # Create the main window
    root = tk.Tk()
    
    # Create the advanced forms demo
    app = AdvancedFormsDemo(root)
    
    # Start the application
    root.mainloop()


if __name__ == "__main__":
    main()

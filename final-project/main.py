"""
Final Project: Professional Dashboard Application
Complete enterprise-level dashboard demonstrating all book concepts
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import hashlib
import threading
import time
from datetime import datetime, timedelta
import random
import os
import sys
from collections import defaultdict

# Add the parent directory to the path to import from chapters
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the complete dashboard from Chapter 10
from chapters.chapter10_complete_professional_dashboard.main import ProfessionalDashboard

def main():
    """Main application entry point for the final project"""
    try:
        print("Starting Professional Dashboard - Final Project")
        print("=" * 50)
        print("This application demonstrates all concepts from the book:")
        print("- Tkinter GUI development")
        print("- Database integration with SQLite")
        print("- Data visualization with Matplotlib")
        print("- Real-time updates and threading")
        print("- User authentication and security")
        print("- Export and reporting capabilities")
        print("- Professional UI/UX design")
        print("=" * 50)
        
        # Start the professional dashboard
        app = ProfessionalDashboard()
        app.run()
        
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

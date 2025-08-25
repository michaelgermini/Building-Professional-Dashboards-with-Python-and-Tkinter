#!/usr/bin/env python3
"""
Script to add navigation links to all chapter README files.
This script will add a navigation section to each chapter's README.
"""

import os
import re

def create_chapter_navigation(chapter_num, chapter_title, chapter_dir):
    """Create navigation section for a specific chapter."""
    
    # Determine previous and next chapters
    prev_chapter = chapter_num - 1 if chapter_num > 1 else None
    next_chapter = chapter_num + 1 if chapter_num < 10 else None
    
    # Create navigation table
    nav_table = "| Previous | Current | Next |\n"
    nav_table += "|----------|---------|------|\n"
    
    if prev_chapter:
        prev_link = f"[← Chapter {prev_chapter}](../chapter{prev_chapter:02d}-*/README.md)"
    else:
        prev_link = "← Beginning"
    
    current = f"**Chapter {chapter_num}: {chapter_title}**"
    
    if next_chapter:
        next_link = f"[Chapter {next_chapter} →](../chapter{next_chapter:02d}-*/README.md)"
    else:
        next_link = "End →"
    
    nav_table += f"| {prev_link} | {current} | {next_link} |\n"
    
    # Create the full navigation section
    navigation = f"""## 📚 Navigation

### 🔗 Quick Navigation
- **🏠 [Main README](../../README.md)** - Return to main documentation
- **🌐 [Interactive Website](../../index.html)** - Modern web interface
- **📝 [Preface](../../preface.md)** - Book introduction

### 📖 Chapter Navigation
{nav_table}

### 📖 Book Structure
- **📝 [Preface](../../preface.md)** - Introduction and book overview
- **📋 [Table of Contents](../../TABLE_OF_CONTENTS.md)** - Detailed book structure

### 🎯 Direct Chapter Links
- **🎯 [Chapter 1: Getting Started](../chapter01-getting-started/README.md)** - Basic Tkinter concepts
- **🧩 [Chapter 2: Core Widgets](../chapter02-core-widgets/README.md)** - Essential widgets
- **⚡ [Chapter 3: Events & Callbacks](../chapter03-events-callbacks/README.md)** - Interactive applications
- **🏗️ [Chapter 4: Dashboard Architecture](../chapter04-dashboard-architecture/README.md)** - MVC patterns
- **📊 [Chapter 5: Data Visualization](../chapter05-data-visualization/README.md)** - Charts and graphs
- **🔧 [Chapter 6: Advanced Widgets](../chapter06-advanced-widgets/README.md)** - Professional components
- **💾 [Chapter 7: Database Integration](../chapter07-database-integration/README.md)** - SQLite operations
- **⏱️ [Chapter 8: Real-time Dashboards](../chapter08-real-time-dashboards/README.md)** - Live applications
- **📤 [Chapter 9: Exporting & Reporting](../chapter09-exporting-reporting/README.md)** - PDF generation
- **🏆 [Chapter 10: Complete Professional Dashboard](../chapter10-complete-professional-dashboard/README.md)** - Full application

### 📚 Learning Resources
- **🧪 [Exercise Collection](../../exercises_summary.md)** - All exercises overview
- **💡 [Complete Solutions](../../exercise_solutions.md)** - Step-by-step solutions
- **📈 [Learning Progression](../../learning_progression_guide.md)** - 10-week learning plan
- **🔧 [Advanced Exercises](../../additional_exercises.md)** - Additional practice

### 📖 Reference Materials
- **📖 [Tkinter Widget Reference](../../appendices/appendix_a_tkinter_widget_reference.md)** - Complete widget catalog
- **📦 [Python Packaging Guide](../../appendices/appendix_b_python_packaging.md)** - Application packaging
- **🚀 [Deployment Guide](../../appendices/appendix_c_deployment_guide.md)** - Production deployment

---

**💡 Tip**: Use the navigation links above to easily move between chapters and resources!

"""
    
    return navigation

def add_navigation_to_readme(readme_path, navigation):
    """Add navigation section to a README file."""
    
    if not os.path.exists(readme_path):
        print(f"⚠️  README not found: {readme_path}")
        return False
    
    # Read the current README content
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if navigation already exists
    if "## 📚 Navigation" in content:
        print(f"✅ Navigation already exists in: {readme_path}")
        return True
    
    # Add navigation at the end of the file
    updated_content = content + "\n\n" + navigation
    
    # Write the updated content back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Added navigation to: {readme_path}")
    return True

def main():
    """Main function to add navigation to all chapter READMEs."""
    
    # Chapter information
    chapters = [
        (1, "Getting Started", "chapter01-getting-started"),
        (2, "Core Widgets", "chapter02-core-widgets"),
        (3, "Events & Callbacks", "chapter03-events-callbacks"),
        (4, "Dashboard Architecture", "chapter04-dashboard-architecture"),
        (5, "Data Visualization", "chapter05-data-visualization"),
        (6, "Advanced Widgets", "chapter06-advanced-widgets"),
        (7, "Database Integration", "chapter07-database-integration"),
        (8, "Real-time Dashboards", "chapter08-real-time-dashboards"),
        (9, "Exporting & Reporting", "chapter09-exporting-reporting"),
        (10, "Complete Professional Dashboard", "chapter10-complete-professional-dashboard")
    ]
    
    print("🚀 Adding navigation to all chapter READMEs...\n")
    
    success_count = 0
    total_count = len(chapters)
    
    for chapter_num, chapter_title, chapter_dir in chapters:
        readme_path = f"chapters/{chapter_dir}/README.md"
        
        # Create navigation for this chapter
        navigation = create_chapter_navigation(chapter_num, chapter_title, chapter_dir)
        
        # Add navigation to README
        if add_navigation_to_readme(readme_path, navigation):
            success_count += 1
    
    print(f"\n🎉 Navigation added to {success_count}/{total_count} chapter READMEs!")
    
    if success_count == total_count:
        print("✅ All chapters now have navigation links!")
    else:
        print("⚠️  Some chapters may not have README files yet.")

if __name__ == "__main__":
    main()

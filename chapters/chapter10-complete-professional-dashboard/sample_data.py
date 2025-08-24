"""
Sample Data Generator for Professional Dashboard
Generates realistic sample data for demonstration purposes
"""

import sqlite3
import random
from datetime import datetime, timedelta
import hashlib

class SampleDataGenerator:
    def __init__(self, db_path="professional_dashboard.db"):
        self.db_path = db_path
        self.connection = None
        self.connect()
    
    def connect(self):
        """Connect to the database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except Exception as e:
            print(f"Failed to connect to database: {e}")
    
    def generate_sample_data(self):
        """Generate comprehensive sample data"""
        print("Generating sample data...")
        
        # Generate users
        self.generate_users()
        
        # Generate sales data
        self.generate_sales_data()
        
        # Generate system metrics
        self.generate_system_metrics()
        
        print("Sample data generation completed!")
    
    def generate_users(self):
        """Generate sample user accounts"""
        users = [
            ("admin", "admin123", "admin@company.com", "admin"),
            ("manager", "manager123", "manager@company.com", "manager"),
            ("sales1", "sales123", "sales1@company.com", "sales"),
            ("sales2", "sales123", "sales2@company.com", "sales"),
            ("analyst", "analyst123", "analyst@company.com", "analyst"),
            ("viewer", "viewer123", "viewer@company.com", "viewer")
        ]
        
        try:
            cursor = self.connection.cursor()
            
            for username, password, email, role in users:
                # Check if user already exists
                cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
                if not cursor.fetchone():
                    password_hash = hashlib.sha256(password.encode()).hexdigest()
                    cursor.execute("""
                        INSERT INTO users (username, password_hash, email, role)
                        VALUES (?, ?, ?, ?)
                    """, (username, password_hash, email, role))
            
            self.connection.commit()
            print(f"Generated {len(users)} user accounts")
            
        except Exception as e:
            print(f"Error generating users: {e}")
    
    def generate_sales_data(self):
        """Generate realistic sales data - 100 recent sales"""
        products = [
            "Laptop Pro X1", "Desktop Workstation", "Tablet Air", "Smartphone Galaxy",
            "Wireless Headphones", "Gaming Console", "Smart Watch", "Bluetooth Speaker",
            "External Hard Drive", "USB-C Cable", "Wireless Mouse", "Mechanical Keyboard",
            "Monitor 27\"", "Webcam HD", "Microphone Pro", "Graphics Card RTX",
            "SSD 1TB", "RAM 16GB", "Power Supply", "Cooling Fan"
        ]
        
        regions = ["North America", "Europe", "Asia Pacific", "Latin America", "Middle East"]
        salespeople = ["John Smith", "Sarah Johnson", "Mike Davis", "Lisa Wilson", "David Brown"]
        
        # Generate sales for the last 30 days (more recent)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        try:
            cursor = self.connection.cursor()
            
            # Clear existing sales data
            cursor.execute("DELETE FROM sales")
            
            # Generate 100 sales records (recent sales)
            for i in range(100):
                # Random date within the last 30 days
                random_days = random.randint(0, 30)
                sale_date = start_date + timedelta(days=random_days)
                
                # Random product and quantity
                product = random.choice(products)
                quantity = random.randint(1, 10)
                
                # Realistic pricing based on product type
                base_prices = {
                    "Laptop Pro X1": 1200,
                    "Desktop Workstation": 800,
                    "Tablet Air": 400,
                    "Smartphone Galaxy": 600,
                    "Wireless Headphones": 150,
                    "Gaming Console": 500,
                    "Smart Watch": 300,
                    "Bluetooth Speaker": 80,
                    "External Hard Drive": 120,
                    "USB-C Cable": 15,
                    "Wireless Mouse": 50,
                    "Mechanical Keyboard": 120,
                    "Monitor 27\"": 300,
                    "Webcam HD": 100,
                    "Microphone Pro": 200,
                    "Graphics Card RTX": 800,
                    "SSD 1TB": 100,
                    "RAM 16GB": 80,
                    "Power Supply": 150,
                    "Cooling Fan": 40
                }
                
                base_price = base_prices.get(product, 100)
                # Add some price variation (±20%)
                price_variation = random.uniform(0.8, 1.2)
                price = round(base_price * price_variation, 2)
                
                region = random.choice(regions)
                salesperson = random.choice(salespeople)
                
                cursor.execute("""
                    INSERT INTO sales (product_name, quantity, price, sale_date, region, salesperson)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (product, quantity, price, sale_date, region, salesperson))
            
            self.connection.commit()
            print(f"Generated 100 recent sales records")
            
        except Exception as e:
            print(f"Error generating sales data: {e}")
    
    def generate_system_metrics(self):
        """Generate sample system metrics"""
        metrics = [
            "cpu_usage", "memory_usage", "disk_usage", "network_traffic",
            "active_users", "database_connections", "response_time", "error_rate"
        ]
        
        try:
            cursor = self.connection.cursor()
            
            # Clear existing metrics
            cursor.execute("DELETE FROM system_metrics")
            
            # Generate metrics for the last 24 hours
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            for i in range(24):  # One record per hour
                timestamp = start_time + timedelta(hours=i)
                
                for metric in metrics:
                    # Generate realistic metric values
                    if metric == "cpu_usage":
                        value = random.uniform(20, 85)
                    elif metric == "memory_usage":
                        value = random.uniform(40, 90)
                    elif metric == "disk_usage":
                        value = random.uniform(60, 95)
                    elif metric == "network_traffic":
                        value = random.uniform(10, 100)
                    elif metric == "active_users":
                        value = random.randint(5, 50)
                    elif metric == "database_connections":
                        value = random.randint(10, 100)
                    elif metric == "response_time":
                        value = random.uniform(50, 500)
                    elif metric == "error_rate":
                        value = random.uniform(0, 5)
                    else:
                        value = random.uniform(0, 100)
                    
                    cursor.execute("""
                        INSERT INTO system_metrics (metric_name, metric_value, timestamp)
                        VALUES (?, ?, ?)
                    """, (metric, round(value, 2), timestamp))
            
            self.connection.commit()
            print(f"Generated system metrics for 24 hours")
            
        except Exception as e:
            print(f"Error generating system metrics: {e}")
    
    def get_data_summary(self):
        """Get summary of generated data"""
        try:
            cursor = self.connection.cursor()
            
            # Count users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            user_count = cursor.fetchone()['count']
            
            # Count sales
            cursor.execute("SELECT COUNT(*) as count FROM sales")
            sales_count = cursor.fetchone()['count']
            
            # Sales summary
            cursor.execute("""
                SELECT 
                    SUM(quantity * price) as total_revenue,
                    AVG(price) as avg_price,
                    COUNT(DISTINCT product_name) as unique_products
                FROM sales
            """)
            sales_summary = cursor.fetchone()
            
            # Count metrics
            cursor.execute("SELECT COUNT(*) as count FROM system_metrics")
            metrics_count = cursor.fetchone()['count']
            
            print("\n=== Data Summary ===")
            print(f"Users: {user_count}")
            print(f"Sales Records: {sales_count}")
            print(f"Total Revenue: ${sales_summary['total_revenue']:,.2f}")
            print(f"Average Price: ${sales_summary['avg_price']:,.2f}")
            print(f"Unique Products: {sales_summary['unique_products']}")
            print(f"System Metrics: {metrics_count}")
            
        except Exception as e:
            print(f"Error getting data summary: {e}")

def main():
    """Main function to generate sample data"""
    print("Professional Dashboard - Sample Data Generator")
    print("=" * 50)
    
    generator = SampleDataGenerator()
    generator.generate_sample_data()
    generator.get_data_summary()
    
    print("\nSample data generation completed!")
    print("You can now run the main dashboard application.")

if __name__ == "__main__":
    main()

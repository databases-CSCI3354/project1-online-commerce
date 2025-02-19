import os
import sqlite3

from app.utils.logger import setup_logger

log = setup_logger(__name__)


def init_db(app):
    """Initialize the database with required tables."""
    with app.app_context():
        db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        
        # Enable foreign key support
        db.execute("PRAGMA foreign_keys = ON")
        
        # Create tables
        db.executescript('''
            -- Create Authentication table
            CREATE TABLE IF NOT EXISTS Authentication (
                UserID TEXT PRIMARY KEY,
                PasswordHash TEXT NOT NULL,
                SessionID TEXT UNIQUE,
                FOREIGN KEY (UserID) REFERENCES Customers(CustomerID)
            );

            -- Create Shopping_Cart table
            CREATE TABLE IF NOT EXISTS Shopping_Cart (
                CartID INTEGER PRIMARY KEY AUTOINCREMENT,
                SessionID TEXT NOT NULL,
                ProductID INTEGER NOT NULL,
                Quantity INTEGER NOT NULL,
                AddedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
            );

            -- Add index for faster lookups
            CREATE INDEX IF NOT EXISTS idx_shopping_cart_session 
            ON Shopping_Cart(SessionID);
            
            CREATE INDEX IF NOT EXISTS idx_shopping_cart_added_at 
            ON Shopping_Cart(AddedAt);
            
            -- Add WEB employee if not exists
            INSERT OR IGNORE INTO Employees (
                FirstName, LastName, Title
            ) VALUES (
                'WEB', 'WEB', 'Online Sales System'
            );
        ''')
        
        db.commit()
        
        # Get the WEB employee ID for reference
        cursor = db.cursor()
        cursor.execute(
            "SELECT EmployeeID FROM Employees WHERE FirstName = 'WEB' AND LastName = 'WEB'"
        )
        web_employee_id = cursor.fetchone()[0]
        
        log.info(f"Database initialized. WEB employee ID: {web_employee_id}")
        
        return web_employee_id 

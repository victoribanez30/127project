#!/usr/bin/env python3
"""
Database Manager Module
Handles database connection and operations for the Organization Management System
"""

import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self, host='localhost', database='127project', user='admin', password='admin'):
        """Connect to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            print("✓ Successfully connected to the database")
            return True
        except Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database connection closed")
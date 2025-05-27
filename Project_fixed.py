#!/usr/bin/env python3
"""
Organization Management System
Terminal-based application for managing memberships and fees

Refactored version with modular structure:
- database_manager.py: Database connection management
- member_manage.py: Member and membership management
- org_manage.py: Organization management
- fees_manage.py: Fee and payment management
- advanced_reports.py: Advanced reporting features
"""

import sys
import getpass
from database_manager import DatabaseManager
from member_manage import MembershipManager
from org_manage import OrganizationManager
from fees_manage import FeesManager
from advanced_reports import AdvancedReports


class OrganizationManagementSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.membership_manager = None
        self.fees_manager = None
        self.advanced_reports = None
        self.organization_manager = None
        self.user_type = None  # 'admin' for full access, 'user' for limited access
        self.current_user = None
    
    def login(self):
        """Handle user login and determine access level"""
        print("=" * 60)
        print("    ORGANIZATION MANAGEMENT SYSTEM - LOGIN")
        print("=" * 60)
        
        if not self.db_manager.connect():
            print("Failed to connect to database. Exiting...")
            return False
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            print(f"\nLogin Attempt {attempts + 1}/{max_attempts}")
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            
            # Check admin credentials first (database admin)
            if username == "admin" and password == "admin":
                self.user_type = "admin"
                self.current_user = "System Administrator"
                print(f"✓ Welcome, {self.current_user}! (Full Access)")
                return True
            
            # Check organization credentials
            try:
                query = "SELECT org_id, name FROM org WHERE username = %s AND password = %s"
                self.db_manager.cursor.execute(query, (username, password))
                result = self.db_manager.cursor.fetchone()
                
                if result:
                    self.user_type = "user"
                    self.current_user = result[1]  # Organization name
                    self.current_org_id = result[0]  # Organization ID
                    print(f"✓ Welcome, {self.current_user}! (Limited Access)")
                    return True
                else:
                    attempts += 1
                    if attempts < max_attempts:
                        print("✗ Invalid credentials. Please try again.")
                    else:
                        print("✗ Maximum login attempts exceeded.")
                        
            except Exception as e:
                print(f"✗ Login error: {e}")
                attempts += 1
        
        print("Access denied. Exiting...")
        return False
    
    def initialize(self):
        """Initialize the system after successful login"""
        self.membership_manager = MembershipManager(self.db_manager)
        self.fees_manager = FeesManager(self.db_manager)
        self.advanced_reports = AdvancedReports(self.db_manager)
        self.organization_manager = OrganizationManager(self.db_manager)
        
        # Pass user information to managers
        self.membership_manager.user_type = self.user_type
        self.membership_manager.current_org_id = getattr(self, 'current_org_id', None)
        self.fees_manager.user_type = self.user_type
        self.fees_manager.current_org_id = getattr(self, 'current_org_id', None)
        self.organization_manager.user_type = self.user_type
        self.organization_manager.current_org_id = getattr(self, 'current_org_id', None)
        self.advanced_reports.user_type = self.user_type
        self.advanced_reports.current_org_id = getattr(self, 'current_org_id', None)
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\n" + "=" * 60)
            print(f"     MAIN MENU - {self.current_user}")
            print(f"     Access Level: {'Full Access' if self.user_type == 'admin' else 'Limited Access'}")
            print("=" * 60)
            
            if self.user_type == "admin":
                print("1. Organization Management")
                print("2. Membership Management")
                print("3. Fees Management")
                print("4. Advanced Reports")
                print("5. Exit")
                choices = ['1', '2', '3', '4', '5']
            else:
                print("1. View Organization Info")
                print("2. Membership Management")
                print("3. Fees Management")
                print("4. Basic Reports")
                print("5. Exit")
                choices = ['1', '2', '3', '4', '5']
            
            choice = input("\nEnter your choice: ")
            
            if choice not in choices:
                print("Invalid choice! Please try again.")
                continue
            
            if choice == '1':
                if self.user_type == "admin":
                    self.organization_manager.manage_organizations()
                else:
                    self.organization_manager.view_own_organization()
            elif choice == '2':
                self.membership_menu()
            elif choice == '3':
                self.fees_menu()
            elif choice == '4':
                if self.user_type == "admin":
                    self.advanced_reports.advanced_reports_menu()
                else:
                    self.advanced_reports.basic_reports_menu()
            elif choice == '5':
                print("Goodbye!")
                self.db_manager.disconnect()
                sys.exit(0)
    
    def membership_menu(self):
        """Display membership management menu"""
        while True:
            print("\n" + "=" * 60)
            print("              MEMBERSHIP MANAGEMENT")
            print("=" * 60)
            print("1. Add new member")
            print("2. Update member information")
            print("3. Delete member")
            print("4. Search members")
            print("5. Manage organization membership")
            print("6. Back to main menu")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.membership_manager.add_member()
            elif choice == '2':
                self.membership_manager.update_member()
            elif choice == '3':
                self.membership_manager.delete_member()
            elif choice == '4':
                self.membership_manager.search_members()
            elif choice == '5':
                self.membership_manager.manage_membership()
            elif choice == '6':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def fees_menu(self):
        """Display fees management menu"""
        self.fees_manager.manage_fees()
    
    def run(self):
        """Run the application"""
        try:
            if not self.login():
                sys.exit(1)
            
            self.initialize()
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            self.db_manager.disconnect()
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.db_manager.disconnect()
            sys.exit(1)


if __name__ == "__main__":
    app = OrganizationManagementSystem()
    app.run()

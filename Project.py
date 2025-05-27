#!/usr/bin/env python3
"""
Organization Management System
Terminal-based application for managing memberships and fees with user authentication
"""

import sys
from database_manager import DatabaseManager
from member_manage import MembershipManager
from fees_manage import FeesManager
from advanced_reports import AdvancedReports
from org_manage import OrganizationManager

class OrganizationManagementSystem:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.membership_manager = None
        self.fees_manager = None
        self.advanced_reports = None
        self.organization_manager = None
        self.user_type = None
        self.current_org_id = None
        self.current_username = None
        self.current_student_number = None
    
    def initialize(self):
        """Initialize the system"""
        print("=" * 60)
        print("    ORGANIZATION MANAGEMENT SYSTEM")
        print("=" * 60)
        
        if not self.db_manager.connect():
            print("Failed to connect to database. Exiting...")
            sys.exit(1)
    
    def login(self):
        """Handle user login with authentication"""
        print("\n" + "=" * 60)
        print("                    LOGIN")
        print("=" * 60)
        
        attempts = 0
        max_attempts = 3        
        while attempts < max_attempts:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            # Check admin credentials
            if username == "admin" and password == "admin":
                self.user_type = "admin"
                self.current_username = username
                print(f"\nWelcome, {username}! You have admin access.")
                return True
            
            # Check organization credentials
            cursor = self.db_manager.connection.cursor()
            cursor.execute("""
                SELECT org_id, name FROM org 
                WHERE username = %s AND password = %s
            """, (username, password))
            
            org_result = cursor.fetchone()
            
            if org_result:
                cursor.close()
                self.user_type = "organization"
                self.current_org_id = org_result[0]
                self.current_username = org_result[1]
                print(f"\nWelcome, {org_result[1]}! You have access to your organization data.")
                return True
            
            # Check member credentials (using student number as username)
            try:
                student_number = int(username)
                cursor.execute("""
                    SELECT student_number, name FROM member 
                    WHERE student_number = %s AND password = %s
                """, (student_number, password))
                
                member_result = cursor.fetchone()
                cursor.close()
                
                if member_result:
                    self.user_type = "member"
                    self.current_org_id = None
                    self.current_username = member_result[1]
                    self.current_student_number = member_result[0]
                    print(f"\nWelcome, {member_result[1]}! You have member access.")
                    return True
            except ValueError:
                cursor.close()
                # Username is not a number, so it's not a student number
            
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Invalid credentials. {remaining} attempts remaining.")
            else:
                print("Too many failed login attempts. Exiting...")
                
        return False
    
    def initialize_managers(self):
        """Initialize all manager classes with user context"""
        extra_context = getattr(self, 'current_student_number', None)
        self.membership_manager = MembershipManager(self.db_manager, self.user_type, self.current_org_id, extra_context)
        self.fees_manager = FeesManager(self.db_manager, self.user_type, self.current_org_id, extra_context)
        self.advanced_reports = AdvancedReports(self.db_manager, self.user_type, self.current_org_id)
        self.organization_manager = OrganizationManager(self.db_manager, self.user_type, self.current_org_id)
    
    def main_menu(self):
        """Display main menu based on user access level"""
        while True:
            print("\n" + "=" * 60)
            print("                    MAIN MENU")
            print("=" * 60)
            print(f"Logged in as: {self.current_username} ({self.user_type})")
            print("=" * 60)
            
            if self.user_type == "admin":
                print("1. Organization Management")
                print("2. Membership Management")
                print("3. Fees Management")
                print("4. Advanced Reports")
                print("5. Exit")
                max_choice = 5
            elif self.user_type == "organization":
                print("1. View Organization Information")
                print("2. View Members")
                print("3. View Fees")
                print("4. Basic Reports")
                print("5. Exit")
                max_choice = 5
            else:  # member access
                print("1. View My Information")
                print("2. View My Fees")
                print("3. View My Organizations")
                print("4. Exit")
                max_choice = 4
            
            choice = input(f"\nEnter your choice (1-{max_choice}): ")
            
            if choice == '1':
                if self.user_type == "admin":
                    self.organization_manager.manage_organizations()
                elif self.user_type == "organization":
                    self.organization_manager.view_own_organization()
                else:  # member
                    self.membership_manager.view_my_information()
            elif choice == '2':
                if self.user_type == "admin":
                    self.membership_menu()                
                elif self.user_type == "organization":
                    self.membership_manager.view_org_members()
                else:  # member
                    self.fees_manager.view_my_fees()
            elif choice == '3':
                if self.user_type == "admin":
                    self.fees_manager.manage_fees()
                elif self.user_type == "organization":
                    self.fees_manager.view_organization_fees()
                else:  # member
                    self.membership_manager.view_my_organizations()
            elif choice == '4':
                if self.user_type == "admin":
                    self.advanced_reports.advanced_reports_menu()
                elif self.user_type == "organization":
                    self.advanced_reports.basic_reports_menu()
                else:  # member
                    print("Goodbye!")
                    self.db_manager.disconnect()
                    sys.exit(0)
            elif choice == '5' and self.user_type in ["admin", "organization"]:
                print("Goodbye!")
                self.db_manager.disconnect()
                sys.exit(0)
            else:
                print("Invalid choice! Please try again.")
    
    def membership_menu(self):
        """Display membership management menu (admin only)"""
        while True:
            print("\n" + "=" * 60)
            print("              MEMBERSHIP MANAGEMENT")
            print("=" * 60)
            print("1. Add new member")
            print("2. Update member information")
            print("3. Delete member")
            print("4. Search members")
            print("5. Manage organization membership")
            print("6. View all students regardless of org membership")
            print("7. Back to main menu")
            
            choice = input("\nEnter your choice (1-7): ")
            if choice == '1':
                self.membership_manager.add_member()
            elif choice == '2':
                self.membership_manager.update_member()
            elif choice == '3':
                self.membership_manager.delete_member()
            elif choice == '4':
                self.membership_manager.search_member()
            elif choice == '5':
                self.membership_manager.manage_organization_membership()
            elif choice == '6':
                self.membership_manager.view_all_students()
            elif choice == '7':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def run(self):
        """Run the application"""
        try:
            self.initialize()
            
            # Login required
            if not self.login():
                self.db_manager.disconnect()
                sys.exit(1)
            
            # Initialize managers with user context
            self.initialize_managers()
            
            # Start main menu
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
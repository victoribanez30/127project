#!/usr/bin/env python3
"""
Organization Management System
Terminal-based application for managing memberships and fees
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
    
    def initialize(self):
        """Initialize the system"""
        print("=" * 60)
        print("    ORGANIZATION MANAGEMENT SYSTEM")
        print("=" * 60)
        
        if not self.db_manager.connect():
            print("Failed to connect to database. Exiting...")
            sys.exit(1)
        
        self.membership_manager = MembershipManager(self.db_manager)
        self.fees_manager = FeesManager(self.db_manager)
        self.advanced_reports = AdvancedReports(self.db_manager)
        self.organization_manager = OrganizationManager(self.db_manager)
    
    def main_menu(self):
        """Display main menu and handle user choices"""
        while True:
            print("\n" + "=" * 60)
            print("                    MAIN MENU")
            print("=" * 60)
            print("1. Organization Management")
            print("2. Membership Management")
            print("3. Fees Management")
            print("4. Advanced Reports")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '2':
                self.membership_menu()
            elif choice == '3':
                self.fees_menu()
            elif choice == '4':
                self.advanced_reports.advanced_reports_menu()
            elif choice == '1':
                self.organization_manager.manage_organizations()
            elif choice == '5':
                print("Goodbye!")
                self.db_manager.disconnect()
                sys.exit(0)
            else:
                print("Invalid choice! Please try again.")
    
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
        while True:
            print("\n" + "=" * 60)
            print("                FEES MANAGEMENT")
            print("=" * 60)
            print("1. Add new fee")
            print("2. Process payment")
            print("3. View member fees")
            print("4. View organization fees")
            print("5. Generate financial reports")
            print("6. Back to main menu")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.fees_manager.add_fee()
            elif choice == '2':
                self.fees_manager.process_payment()
            elif choice == '3':
                self.fees_manager.view_member_fees()
            elif choice == '4':
                self.fees_manager.view_org_fees()
            elif choice == '5':
                self.fees_manager.generate_reports()
            elif choice == '6':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def run(self):
        """Run the application"""
        try:
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

#!/usr/bin/env python3
"""
Organization Management Module
Handles organization creation, updates, deletion, and information management
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
import getpass

class OrganizationManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def manage_organizations(self):
        """Main organization management menu"""
        while True:
            print("\n" + "=" * 60)
            print("              ORGANIZATION MANAGEMENT")
            print("=" * 60)
            print("1. Add new organization")
            print("2. Update organization information")
            print("3. Delete organization")
            print("4. Search organizations")
            print("5. View all organizations")
            print("6. Back to main menu")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.add_organization()
            elif choice == '2':
                self.update_organization()
            elif choice == '3':
                self.delete_organization()
            elif choice == '4':
                self.search_organizations()
            elif choice == '5':
                self.view_all_organizations()
            elif choice == '6':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def add_organization(self):
        """Add a new organization to the system"""
        print("\n=== Add New Organization ===")
        try:
            name = input("Organization Name: ")
            org_type = input("Organization Type (e.g., Academic, Social, Professional): ")
            year_established = int(input("Year Established: "))
            money_balance = float(input("Initial Money Balance (default 0.00): ") or "0.00")
            username = input("Organization Username: ")
            password = getpass.getpass("Organization Password: ")
            
            query = """INSERT INTO org (money_balance, type, name, year_established, username, password) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
            values = (money_balance, org_type, name, year_established, username, password)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            
            # Get the auto-generated org_id
            org_id = self.db.cursor.lastrowid
            print(f"✓ Organization added successfully with ID: {org_id}")
            
        except ValueError:
            print("✗ Invalid input. Please enter valid numbers where required.")
        except Error as e:
            print(f"✗ Error adding organization: {e}")
    
    def update_organization(self):
        """Update organization information"""
        print("\n=== Update Organization ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            if not orgs:
                print("No organizations found!")
                return
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("\nEnter organization ID to update: "))
            
            # Check if organization exists and get current info
            self.db.cursor.execute("SELECT * FROM org WHERE org_id = %s", (org_id,))
            organization = self.db.cursor.fetchone()
            
            if not organization:
                print("✗ Organization not found!")
                return
            
            print("Current organization information:")
            print(f"Name: {organization[3]}")
            print(f"Type: {organization[2]}")
            print(f"Year Established: {organization[4]}")
            print(f"Money Balance: ₱{organization[1]:.2f}")
            print(f"Username: {organization[5]}")
            
            print("\nEnter new information (press Enter to keep current value):")
            name = input(f"Organization Name ({organization[3]}): ") or organization[3]
            org_type = input(f"Type ({organization[2]}): ") or organization[2]
            year_established = input(f"Year Established ({organization[4]}): ")
            year_established = int(year_established) if year_established else organization[4]
            money_balance = input(f"Money Balance ({organization[1]}): ")
            money_balance = float(money_balance) if money_balance else organization[1]
            username = input(f"Username ({organization[5]}): ") or organization[5]
            
            update_password = input("Update password? (yes/no): ").lower() == 'yes'
            if update_password:
                password = getpass.getpass("New Password: ")
                query = """UPDATE org SET name = %s, type = %s, year_established = %s, 
                          money_balance = %s, username = %s, password = %s WHERE org_id = %s"""
                values = (name, org_type, year_established, money_balance, username, password, org_id)
            else:
                query = """UPDATE org SET name = %s, type = %s, year_established = %s, 
                          money_balance = %s, username = %s WHERE org_id = %s"""
                values = (name, org_type, year_established, money_balance, username, org_id)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("✓ Organization updated successfully!")
            
        except ValueError:
            print("✗ Invalid input. Please enter valid numbers where required.")
        except Error as e:
            print(f"✗ Error updating organization: {e}")
    
    def delete_organization(self):
        """Delete an organization from the system"""
        print("\n=== Delete Organization ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            if not orgs:
                print("No organizations found!")
                return
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("\nEnter organization ID to delete: "))
            
            # Check if organization exists
            self.db.cursor.execute("SELECT name FROM org WHERE org_id = %s", (org_id,))
            organization = self.db.cursor.fetchone()
            
            if not organization:
                print("✗ Organization not found!")
                return
            
            # Check if organization has members or fees
            self.db.cursor.execute("SELECT COUNT(*) FROM joins WHERE org_id = %s", (org_id,))
            member_count = self.db.cursor.fetchone()[0]
            
            self.db.cursor.execute("SELECT COUNT(*) FROM fee WHERE org_id = %s", (org_id,))
            fee_count = self.db.cursor.fetchone()[0]
            
            if member_count > 0 or fee_count > 0:
                print(f"⚠️  Warning: This organization has {member_count} members and {fee_count} fee records.")
                print("Deleting the organization will also delete all related membership and fee records.")
            
            confirm = input(f"Are you sure you want to delete '{organization[0]}'? (yes/no): ")
            if confirm.lower() == 'yes':
                # Delete related records first due to foreign key constraints
                self.db.cursor.execute("DELETE FROM fee WHERE org_id = %s", (org_id,))
                self.db.cursor.execute("DELETE FROM joins WHERE org_id = %s", (org_id,))
                self.db.cursor.execute("DELETE FROM org WHERE org_id = %s", (org_id,))
                self.db.connection.commit()
                print("✓ Organization and all related records deleted successfully!")
            else:
                print("Delete operation cancelled.")
                
        except ValueError:
            print("✗ Invalid organization ID.")
        except Error as e:
            print(f"✗ Error deleting organization: {e}")
    
    def search_organizations(self):
        """Search for organizations"""
        print("\n=== Search Organizations ===")
        print("1. Search by name")
        print("2. Search by type")
        print("3. Search by year established")
        print("4. View all organizations")
        
        choice = input("Choose search option: ")
        
        try:
            if choice == '1':
                name = input("Enter organization name (partial match allowed): ")
                query = "SELECT * FROM org WHERE name LIKE %s"
                self.db.cursor.execute(query, (f"%{name}%",))
            elif choice == '2':
                org_type = input("Enter organization type: ")
                query = "SELECT * FROM org WHERE type LIKE %s"
                self.db.cursor.execute(query, (f"%{org_type}%",))
            elif choice == '3':
                year = int(input("Enter year established: "))
                query = "SELECT * FROM org WHERE year_established = %s"
                self.db.cursor.execute(query, (year,))
            elif choice == '4':
                query = "SELECT * FROM org"
                self.db.cursor.execute(query)
            else:
                print("Invalid choice!")
                return
            
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Org ID", "Balance", "Type", "Name", "Year Est.", "Username"]
                table_data = []
                for row in results:
                    table_data.append([row[0], f"₱{row[1]:.2f}", row[2], row[3], row[4], row[5]])
                
                print("\nSearch Results:")
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print("No organizations found!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error searching organizations: {e}")
    
    def view_all_organizations(self):
        """View all organizations with detailed information"""
        try:
            query = """SELECT org_id, name, type, year_established, money_balance, username,
                             (SELECT COUNT(*) FROM joins WHERE joins.org_id = org.org_id) as member_count,
                             (SELECT COUNT(*) FROM fee WHERE fee.org_id = org.org_id) as fee_count
                      FROM org
                      ORDER BY name"""
            
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["ID", "Name", "Type", "Year Est.", "Balance", "Username", "Members", "Fees"]
                table_data = []
                for row in results:
                    table_data.append([
                        row[0], row[1], row[2], row[3], 
                        f"₱{row[4]:.2f}", row[5], row[6], row[7]
                    ])
                
                print("\nAll Organizations:")
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                
                # Summary statistics
                total_balance = sum(row[4] for row in results)
                total_members = sum(row[6] for row in results)
                total_fees = sum(row[7] for row in results)
                
                print(f"\nSummary:")
                print(f"Total Organizations: {len(results)}")
                print(f"Total System Balance: ₱{total_balance:.2f}")
                print(f"Total Members Across All Organizations: {total_members}")
                print(f"Total Fee Records: {total_fees}")
            else:
                print("No organizations found!")
                
        except Error as e:
            print(f"✗ Error viewing organizations: {e}")
#!/usr/bin/env python3
"""
Member Management Module
Handles member registration, updates, and organization membership management
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
import getpass

class MembershipManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_member(self):
        """Add a new member to the system"""
        print("\n=== Add New Member ===")
        try:
            student_number = int(input("Student Number (9 digits): "))
            phone_number = input("Phone Number: ")
            name = input("Full Name: ")
            gender = input("Gender (M/F): ").upper()
            batch = int(input("Batch Year: "))
            degprog = input("Degree Program: ")
            email = input("Email: ")
            password = getpass.getpass("Password: ")
            
            query = """INSERT INTO member (student_number, phone_number, name, gender, 
                      batch, degprog, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            values = (student_number, phone_number, name, gender, batch, degprog, email, password)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("✓ Member added successfully!")
            
        except ValueError:
            print("✗ Invalid input. Please enter valid numbers where required.")
        except Error as e:
            print(f"✗ Error adding member: {e}")
    
    def update_member(self):
        """Update member information"""
        print("\n=== Update Member ===")
        try:
            student_number = int(input("Enter student number to update: "))
            
            # Check if member exists
            self.db.cursor.execute("SELECT * FROM member WHERE student_number = %s", (student_number,))
            member = self.db.cursor.fetchone()
            
            if not member:
                print("✗ Member not found!")
                return
            
            print("Current member information:")
            print(f"Name: {member[2]}")
            print(f"Phone: {member[1]}")
            print(f"Email: {member[6]}")
            
            print("\nEnter new information (press Enter to keep current value):")
            phone_number = input(f"Phone Number ({member[1]}): ") or member[1]
            name = input(f"Full Name ({member[2]}): ") or member[2]
            email = input(f"Email ({member[6]}): ") or member[6]
            
            query = """UPDATE member SET phone_number = %s, name = %s, email = %s 
                      WHERE student_number = %s"""
            values = (phone_number, name, email, student_number)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("✓ Member updated successfully!")
            
        except ValueError:
            print("✗ Invalid student number.")
        except Error as e:
            print(f"✗ Error updating member: {e}")
    
    def delete_member(self):
        """Delete a member from the system"""
        print("\n=== Delete Member ===")
        try:
            student_number = int(input("Enter student number to delete: "))
            
            # Check if member exists
            self.db.cursor.execute("SELECT name FROM member WHERE student_number = %s", (student_number,))
            member = self.db.cursor.fetchone()
            
            if not member:
                print("✗ Member not found!")
                return
            
            confirm = input(f"Are you sure you want to delete {member[0]}? (yes/no): ")
            if confirm.lower() == 'yes':
                self.db.cursor.execute("DELETE FROM member WHERE student_number = %s", (student_number,))
                self.db.connection.commit()
                print("✓ Member deleted successfully!")
            else:
                print("Delete operation cancelled.")
                
        except ValueError:
            print("✗ Invalid student number.")
        except Error as e:
            print(f"✗ Error deleting member: {e}")
    
    def search_members(self):
        """Search for members"""
        print("\n=== Search Members ===")
        print("1. Search by name")
        print("2. Search by student number")
        print("3. Search by degree program")
        print("4. View all members")
        
        choice = input("Choose search option: ")
        
        try:
            if choice == '1':
                name = input("Enter name (partial match allowed): ")
                query = "SELECT * FROM member WHERE name LIKE %s"
                self.db.cursor.execute(query, (f"%{name}%",))
            elif choice == '2':
                student_number = int(input("Enter student number: "))
                query = "SELECT * FROM member WHERE student_number = %s"
                self.db.cursor.execute(query, (student_number,))
            elif choice == '3':
                degprog = input("Enter degree program: ")
                query = "SELECT * FROM member WHERE degprog LIKE %s"
                self.db.cursor.execute(query, (f"%{degprog}%",))
            elif choice == '4':
                query = "SELECT * FROM member"
                self.db.cursor.execute(query)
            else:
                print("Invalid choice!")
                return
            
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Phone", "Name", "Gender", "Batch", "Degree Program", "Email"]
                table_data = []
                for row in results:
                    table_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
                
                print("\nSearch Results:")
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
            else:
                print("No members found!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error searching members: {e}")
    
    def manage_membership(self):
        """Manage organization memberships"""
        print("\n=== Manage Organization Membership ===")
        print("1. Add member to organization")
        print("2. Update member role/status")
        print("3. Remove member from organization")
        print("4. View organization members")
        
        choice = input("Choose option: ")
        
        if choice == '1':
            self.add_member_to_org()
        elif choice == '2':
            self.update_member_role()
        elif choice == '3':
            self.remove_member_from_org()
        elif choice == '4':
            self.view_org_members()
        else:
            print("Invalid choice!")
    
    def add_member_to_org(self):
        """Add a member to an organization"""
        try:
            student_number = int(input("Student Number: "))
            
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            year = input("Year (e.g., 2023): ")
            semester = int(input("Semester (1 or 2): "))
            committee = input("Committee (optional): ") or None
            role = input("Role (e.g., Member, Secretary, President): ")
            status = input("Status (Active/Inactive): ")
            
            query = """INSERT INTO joins (student_number, org_id, year, semester, 
                      committee, role, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (student_number, org_id, year, semester, committee, role, status)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("✓ Member added to organization successfully!")
            
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error adding member to organization: {e}")
    
    def update_member_role(self):
        """Update member's role or status in an organization"""
        try:
            student_number = int(input("Student Number: "))
            org_id = int(input("Organization ID: "))
            year = input("Year: ")
            semester = int(input("Semester: "))
            
            # Check if membership exists
            query = """SELECT role, status FROM joins 
                      WHERE student_number = %s AND org_id = %s AND year = %s AND semester = %s"""
            self.db.cursor.execute(query, (student_number, org_id, year, semester))
            result = self.db.cursor.fetchone()
            
            if not result:
                print("✗ Membership record not found!")
                return
            
            print(f"Current role: {result[0]}")
            print(f"Current status: {result[1]}")
            
            new_role = input("New role (press Enter to keep current): ") or result[0]
            new_status = input("New status (press Enter to keep current): ") or result[1]
            
            update_query = """UPDATE joins SET role = %s, status = %s 
                             WHERE student_number = %s AND org_id = %s AND year = %s AND semester = %s"""
            self.db.cursor.execute(update_query, (new_role, new_status, student_number, org_id, year, semester))
            self.db.connection.commit()
            print("✓ Member role/status updated successfully!")
            
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error updating member role: {e}")
    
    def remove_member_from_org(self):
        """Remove a member from an organization"""
        try:
            student_number = int(input("Student Number: "))
            org_id = int(input("Organization ID: "))
            year = input("Year: ")
            semester = int(input("Semester: "))
            
            query = """DELETE FROM joins 
                      WHERE student_number = %s AND org_id = %s AND year = %s AND semester = %s"""
            self.db.cursor.execute(query, (student_number, org_id, year, semester))
            
            if self.db.cursor.rowcount > 0:
                self.db.connection.commit()
                print("✓ Member removed from organization successfully!")
            else:
                print("✗ Membership record not found!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error removing member from organization: {e}")
    
    def view_org_members(self):
        """View all members of an organization"""
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            
            query = """SELECT m.student_number, m.name, j.role, j.status, j.committee, j.year, j.semester
                      FROM member m
                      JOIN joins j ON m.student_number = j.student_number
                      WHERE j.org_id = %s
                      ORDER BY j.year DESC, j.semester DESC"""
            
            self.db.cursor.execute(query, (org_id,))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Role", "Status", "Committee", "Year", "Semester"]
                print(f"\nMembers of Organization {org_id}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
            else:
                print("No members found for this organization!")
                
        except ValueError:
            print("✗ Invalid organization ID.")
        except Error as e:
            print(f"✗ Error viewing organization members: {e}")
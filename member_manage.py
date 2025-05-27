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
    def __init__(self, db_manager, user_type=None, current_org_id=None, current_student_number=None):
        self.db = db_manager
        self.user_type = user_type
        self.current_org_id = current_org_id
        self.current_student_number = current_student_number
    
    def add_member(self):
        """Add a new member to the system"""
        print("\n=== Add New Member ===")
        try:
            student_number = int(input("Student Number (9 digits): "))
            phone_number = input("Phone Number: ")
            name = input("Full Name: ")
            username = input("Username: ")
            gender = input("Gender (M/F): ").upper()
            batch = int(input("Batch Year: "))
            degprog = input("Degree Program: ")
            email = input("Email: ")
            password = getpass.getpass("Password: ")
            
            # Check if username column exists in the member table
            try:
                self.db.cursor.execute("DESCRIBE member")
                columns = [col[0] for col in self.db.cursor.fetchall()]
                
                if 'username' in columns:
                    # If username column exists, include it in the query
                    query = """INSERT INTO member (student_number, phone_number, name, username, gender, 
                            batch, degprog, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (student_number, phone_number, name, username, gender, batch, degprog, email, password)
                else:
                    # If username column doesn't exist, exclude it from the query
                    print("[INFO] Username column not found. Adding member without username.")
                    query = """INSERT INTO member (student_number, phone_number, name, gender, 
                            batch, degprog, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (student_number, phone_number, name, gender, batch, degprog, email, password)
                    
                    # Try to add username column for future use
                    try:
                        self.db.cursor.execute("ALTER TABLE member ADD COLUMN username VARCHAR(40) AFTER name")
                        self.db.connection.commit()
                        print("[INFO] Username column added to the database for future use.")
                        
                        # Now update this record with the username
                        update_query = "UPDATE member SET username = %s WHERE student_number = %s"
                        self.db.cursor.execute(update_query, (username, student_number))
                    except Error as e:
                        print(f"[WARNING] Could not add username column: {e}")
            
                self.db.cursor.execute(query, values)
                self.db.connection.commit()
                print("[SUCCESS] Member added successfully!")
            except Error as schema_error:
                print(f"[ERROR] Database schema error: {schema_error}")
                # Fall back to basic insert without username if there's a schema issue
                try:
                    query = """INSERT INTO member (student_number, phone_number, name, gender, 
                            batch, degprog, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (student_number, phone_number, name, gender, batch, degprog, email, password)
                    self.db.cursor.execute(query, values)
                    self.db.connection.commit()
                    print("[SUCCESS] Member added successfully (without username)!")
                except Error as basic_error:
                    print(f"[ERROR] Could not add member: {basic_error}")
            
        except ValueError:
            print("[ERROR] Invalid input. Please enter valid numbers where required.")
        except Error as e:
            print(f"[ERROR] Error adding member: {e}")

    def update_member(self):
            """Update member information"""
            print("\n=== Update Member ===")
            try:
                student_number = int(input("Enter student number to update: "))
                
                # Check if member exists
                self.db.cursor.execute("SELECT * FROM member WHERE student_number = %s", (student_number,))
                member = self.db.cursor.fetchone()
                
                if not member:
                    print("[ERROR] Member not found!")
                    return
                
                print("Current member information:")
                print(f"Name: {member[2]}")
                print(f"Username: {member[3]}")
                print(f"Phone: {member[1]}")
                print(f"Email: {member[7]}")
                
                print("\nEnter new information (press Enter to keep current value):")
                phone_number = input(f"Phone Number ({member[1]}): ") or member[1]
                name = input(f"Full Name ({member[2]}): ") or member[2]
                username = input(f"Username ({member[3]}): ") or member[3]
                email = input(f"Email ({member[7]}): ") or member[7]
                
                query = """UPDATE member SET phone_number = %s, name = %s, username = %s, email = %s 
                        WHERE student_number = %s"""
                values = (phone_number, name, username, email, student_number)
                
                self.db.cursor.execute(query, values)
                self.db.connection.commit()
                print("[SUCCESS] Member updated successfully!")
                
            except ValueError:
                print("[ERROR] Invalid student number.")
            except Error as e:
                print(f"[ERROR] Error updating member: {e}")
        
    def delete_member(self):
            """Delete a member from the system"""
            print("\n=== Delete Member ===")
            try:
                student_number = int(input("Enter student number to delete: "))
                
                # Check if member exists
                self.db.cursor.execute("SELECT name FROM member WHERE student_number = %s", (student_number,))
                member = self.db.cursor.fetchone()
                
                if not member:
                    print("[ERROR] Member not found!")
                    return
                
                confirm = input(f"Are you sure you want to delete {member[0]}? (yes/no): ")
                if confirm.lower() != 'yes':
                    print("Deletion cancelled.")
                    return
                
                # Delete related records first
                self.db.cursor.execute("DELETE FROM fee WHERE student_number = %s", (student_number,))
                self.db.cursor.execute("DELETE FROM joins WHERE student_number = %s", (student_number,))
                self.db.cursor.execute("DELETE FROM member WHERE student_number = %s", (student_number,))
                
                self.db.connection.commit()
                print("[SUCCESS] Member deleted successfully!")
                
            except ValueError:
                print("[ERROR] Invalid student number.")
            except Error as e:
                print(f"[ERROR] Error deleting member: {e}")
        
    def search_member(self):
            """Search for members by name or student number"""
            print("\n=== Search Member ===")
            try:
                search_term = input("Enter name or student number: ")
                
                if search_term.isdigit():
                    query = "SELECT * FROM member WHERE student_number = %s"
                    self.db.cursor.execute(query, (int(search_term),))
                else:
                    query = "SELECT * FROM member WHERE name LIKE %s"
                    self.db.cursor.execute(query, (f"%{search_term}%",))
                
                results = self.db.cursor.fetchall()
                
                if results:
                    headers = ["Student No.", "Phone", "Name", "Username", "Gender", "Batch", "Degree Program", "Email"]
                    table_data = []
                    for row in results:
                        table_data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                    
                    print(f"\nSearch Results for '{search_term}':")
                    print(tabulate(table_data, headers=headers, tablefmt="grid"))
                    print(f"Found {len(results)} member(s)")
                else:
                    print(f"No members found matching '{search_term}'")
                    
            except ValueError:
                print("[ERROR] Invalid input.")
            except Error as e:
                print(f"[ERROR] Error searching member: {e}")
        
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
                
                query = """SELECT m.student_number, m.name, m.username, j.role, j.status, j.committee, j.year, j.semester
                        FROM member m
                        JOIN joins j ON m.student_number = j.student_number
                        WHERE j.org_id = %s
                        ORDER BY j.year DESC, j.semester DESC"""
                
                self.db.cursor.execute(query, (org_id,))
                results = self.db.cursor.fetchall()
                
                if results:
                    headers = ["Student No.", "Name", "Username", "Role", "Status", "Committee", "Year", "Semester"]
                    print(f"\nMembers of Organization {org_id}:")
                    print(tabulate(results, headers=headers, tablefmt="grid"))
                else:
                    print("No members found for this organization!")
                    
            except ValueError:
                print("[ERROR] Invalid organization ID.")
            except Error as e:
                print(f"[ERROR] Error viewing organization members: {e}")
        
    def view_all_students(self):
            """View all students in the system regardless of organization membership"""
            try:
                print("\n=== All Students in System ===")
                
                # Simple query that matches the member table structure exactly
                query = "SELECT * FROM member ORDER BY name"
                
                self.db.cursor.execute(query)
                results = self.db.cursor.fetchall()
                
                if results:
                    # Get column names directly from cursor description
                    column_names = [desc[0] for desc in self.db.cursor.description]
                    
                    # Create readable headers mapping
                    header_mapping = {
                        'student_number': 'Student No.',
                        'phone_number': 'Phone',
                        'name': 'Name',
                        'username': 'Username',
                        'gender': 'Gender',
                        'batch': 'Batch',
                        'degprog': 'Program',
                        'email': 'Email',
                        'password': 'Password'
                    }
                    
                    # Create headers - use mapping or original name if not in mapping
                    headers = [header_mapping.get(col, col) for col in column_names]
                    
                    # Filter out password column for display
                    if 'password' in column_names:
                        password_idx = column_names.index('password')
                        # Create a new list of results without the password
                        filtered_results = []
                        for row in results:
                            filtered_row = list(row)
                            filtered_row[password_idx] = '********'  # Mask password
                            filtered_results.append(filtered_row)
                        
                        print(tabulate(filtered_results, headers=headers, tablefmt="grid"))
                    else:
                        print(tabulate(results, headers=headers, tablefmt="grid"))
                    
                    # Statistics - find gender index dynamically
                    total_students = len(results)
                    gender_idx = column_names.index('gender') if 'gender' in column_names else -1
                    
                    male_count = sum(1 for row in results if gender_idx >= 0 and row[gender_idx] == 'M')
                    female_count = sum(1 for row in results if gender_idx >= 0 and row[gender_idx] == 'F')
                    
                    print(f"\nSummary:")
                    print(f"Total Students: {total_students}")
                    print(f"Male: {male_count}")
                    print(f"Female: {female_count}")
                    
                else:
                    print("No students found in the system!")
                    
            except Error as e:
                print(f"[ERROR] Error viewing all students: {e}")
                print("\nTrying alternative query...")
                
                try:
                    # Try with explicit column names to identify which one is problematic
                    query = """SELECT student_number, phone_number, name, gender, 
                                batch, degprog, email FROM member ORDER BY name"""
                    
                    self.db.cursor.execute(query)
                    results = self.db.cursor.fetchall()
                    
                    if results:
                        headers = ["Student No.", "Phone", "Name", "Gender", "Batch", "Program", "Email"]
                        print(tabulate(results, headers=headers, tablefmt="grid"))
                        
                        total_students = len(results)
                        male_count = sum(1 for row in results if row[3] == 'M')
                        female_count = sum(1 for row in results if row[3] == 'F')
                        
                        print(f"\nSummary:")
                        print(f"Total Students: {total_students}")
                        print(f"Male: {male_count}")
                        print(f"Female: {female_count}")
                    else:
                        print("No students found in the system!")
                except Error as e2:
                    print(f"[ERROR] Secondary error: {e2}")

    def view_my_information(self):
            """View personal information for logged-in member"""
            try:
                student_number = self.current_student_number
                if not student_number:
                    print("[ERROR] No student number available!")
                    return
                
                query = "SELECT * FROM member WHERE student_number = %s"
                self.db.cursor.execute(query, (student_number,))
                member = self.db.cursor.fetchone()
                
                if member:
                    print("\n=== My Information ===")
                    print(f"Student Number: {member[0]}")
                    print(f"Phone Number: {member[1]}")
                    print(f"Name: {member[2]}")
                    print(f"Username: {member[3]}")
                    print(f"Gender: {member[4]}")
                    print(f"Batch: {member[5]}")
                    print(f"Degree Program: {member[6]}")
                    print(f"Email: {member[7]}")
                else:
                    print("[ERROR] Member information not found!")
                    
            except Exception as e:
                print(f"[ERROR] Error viewing information: {e}")

    def view_my_organizations(self):
            """View organizations for the logged-in member"""
            try:
                student_number = self.current_student_number
                if not student_number:
                    print("[ERROR] No student number available!")
                    return
                    
                query = """SELECT o.name, o.type, j.role, j.status, j.year, j.semester
                        FROM org o
                        JOIN joins j ON o.org_id = j.org_id
                        WHERE j.student_number = %s
                        ORDER BY j.year DESC, j.semester DESC"""
                
                self.db.cursor.execute(query, (student_number,))
                results = self.db.cursor.fetchall()
                
                if results:
                    headers = ["Organization", "Type", "Role", "Status", "Year", "Semester"]
                    print("\n=== My Organizations ===")
                    print(tabulate(results, headers=headers, tablefmt="grid"))
                else:
                    print("You are not a member of any organization!")
                    
            except Exception as e:
                print(f"[ERROR] Error viewing organizations: {e}")

    def view_my_fees(self):
            """View fees for the logged-in member"""
            try:
                student_number = self.current_student_number
                if not student_number:
                    print("[ERROR] No student number available!")
                    return
                    
                query = """SELECT o.name, f.fee_id, f.amount, f.due_date, f.date_of_payment,
                                f.status, f.year, f.semester
                        FROM fee f
                        JOIN org o ON f.org_id = o.org_id
                        WHERE f.student_number = %s
                        ORDER BY f.year DESC, f.semester DESC, f.due_date"""
                
                self.db.cursor.execute(query, (student_number,))
                results = self.db.cursor.fetchall()
                
                if results:
                    headers = ["Organization", "Fee ID", "Amount", "Due Date", "Payment Date", "Status", "Year", "Semester"]
                    print("\n=== My Fees ===")
                    print(tabulate(results, headers=headers, tablefmt="grid"))
                    
                    unpaid_total = sum(row[2] for row in results if row[5] == 'Unpaid')
                    if unpaid_total > 0:
                        print(f"\nTotal Unpaid Amount: ₱{unpaid_total:.2f}")
                else:
                    print("No fees found for your account!")
                    
            except Exception as e:
                print(f"[ERROR] Error viewing fees: {e}")

    def manage_members(self):
            """Main member management menu"""
            while True:
                print("\n" + "=" * 60)
                print("              MEMBERSHIP MANAGEMENT")
                print("=" * 60)
                
                if self.user_type == "admin":
                    print("1. Add new member")
                    print("2. Update member information")
                    print("3. Delete member")
                    print("4. Search members")
                    print("5. Manage organization membership")
                    print("6. View all students regardless of org membership")
                    print("7. Back to main menu")
                    
                    choice = input("\nEnter your choice (1-7): ")
                    
                    if choice == '1':
                        self.add_member()
                    elif choice == '2':
                        self.update_member()
                    elif choice == '3':
                        self.delete_member()
                    elif choice == '4':
                        self.search_member()  # Changed from search_members to match the actual method name
                    elif choice == '5':
                        self.manage_organization_membership()
                    elif choice == '6':
                        self.view_all_students()
                    elif choice == '7':
                        break
                    else:
                        print("Invalid choice! Please try again.")
                        
                elif self.user_type == "member":
                    print("1. View my information")
                    print("2. View my organizations")
                    print("3. Back to main menu")
                    
                    choice = input("\nEnter your choice (1-3): ")
                    if choice == '1':
                        self.view_my_information()
                    elif choice == '2':
                        self.view_my_organizations()
                    elif choice == '3':
                        break
                    else:
                        print("Invalid choice! Please try again.")
                else:
                    print("[ERROR] Unauthorized access!")
                    break
                    
    def manage_organization_membership(self):
        """Manage organization membership"""
        while True:
            print("\n=== Manage Organization Membership ===")
            print("1. Add member to organization")
            print("2. Update member role/status in organization")
            print("3. Remove member from organization")
            print("4. View organization members")
            print("5. Back to main menu")
            
            choice = input("\nChoose option (1-5): ")
            
            if choice == '1':
                self.add_member_to_org()
            elif choice == '2':
                self.update_member_role_in_org()
            elif choice == '3':
                self.remove_member_from_org()
            elif choice == '4':
                self.view_org_members()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def add_member_to_org(self):
        """Add a member to an organization"""
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            student_number = int(input("Student Number: "))
            
            # Check if member exists
            self.db.cursor.execute("SELECT name FROM member WHERE student_number = %s", (student_number,))
            member = self.db.cursor.fetchone()
            
            if not member:
                print("[ERROR] Member not found!")
                return
            
            # Check if already a member
            self.db.cursor.execute("""
                SELECT * FROM joins 
                WHERE student_number = %s AND org_id = %s
            """, (student_number, org_id))
            
            if self.db.cursor.fetchone():
                print("[ERROR] Member is already part of this organization!")
                return
            
            year = input("Year: ")
            semester = int(input("Semester: "))
            role = input("Role (e.g., Member, Officer, President): ")
            status = input("Status (Active/Inactive): ").title()
            committee = input("Committee (optional, press Enter to skip): ") or None
            
            query = """INSERT INTO joins (student_number, org_id, year, semester, role, status, committee) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            values = (student_number, org_id, year, semester, role, status, committee)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print(f"[SUCCESS] {member[0]} added to organization successfully!")
            
        except ValueError:
            print("[ERROR] Invalid input. Please enter valid numbers where required.")
        except Exception as e:
            print(f"[ERROR] Error adding member to organization: {e}")
    
    def update_member_role_in_org(self):
        """Update member's role or status in an organization"""
        try:
            student_number = int(input("Student Number: "))
            org_id = int(input("Organization ID: "))
            year = input("Year: ")
            semester = int(input("Semester: "))
            
            # Check if membership exists
            query = """SELECT j.role, j.status, j.committee, m.name, o.name 
                      FROM joins j
                      JOIN member m ON j.student_number = m.student_number
                      JOIN org o ON j.org_id = o.org_id
                      WHERE j.student_number = %s AND j.org_id = %s AND j.year = %s AND j.semester = %s"""
            
            self.db.cursor.execute(query, (student_number, org_id, year, semester))
            result = self.db.cursor.fetchone()
            
            if not result:
                print("[ERROR] Membership record not found!")
                return
            
            print(f"\nCurrent membership for {result[3]} in {result[4]}:")
            print(f"Role: {result[0]}")
            print(f"Status: {result[1]}")
            print(f"Committee: {result[2] or 'None'}")
            
            print("\nEnter new information (press Enter to keep current value):")
            new_role = input(f"Role ({result[0]}): ") or result[0]
            new_status = input(f"Status ({result[1]}): ") or result[1]
            new_committee = input(f"Committee ({result[2] or 'None'}): ")
            if new_committee.lower() == 'none' or not new_committee.strip():
                new_committee = None
            elif not new_committee.strip():
                new_committee = result[2]
            
            update_query = """UPDATE joins 
                            SET role = %s, status = %s, committee = %s 
                            WHERE student_number = %s AND org_id = %s AND year = %s AND semester = %s"""
            
            self.db.cursor.execute(update_query, (new_role, new_status, new_committee, student_number, org_id, year, semester))
            self.db.connection.commit()
            print("[SUCCESS] Membership updated successfully!")
            
        except ValueError:
            print("[ERROR] Invalid input.")
        except Exception as e:
            print(f"[ERROR] Error updating membership: {e}")
    
    def remove_member_from_org(self):
        """Remove a member from an organization"""
        try:
            student_number = int(input("Student Number: "))
            org_id = int(input("Organization ID: "))
            year = input("Year: ")
            semester = int(input("Semester: "))
            
            # Check if membership exists
            query = """SELECT m.name, o.name 
                      FROM joins j
                      JOIN member m ON j.student_number = m.student_number
                      JOIN org o ON j.org_id = o.org_id
                      WHERE j.student_number = %s AND j.org_id = %s AND j.year = %s AND j.semester = %s"""
            
            self.db.cursor.execute(query, (student_number, org_id, year, semester))
            result = self.db.cursor.fetchone()
            
            if not result:
                print("[ERROR] Membership record not found!")
                return
            
            confirm = input(f"Remove {result[0]} from {result[1]} for {year} semester {semester}? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Operation cancelled.")
                return
            
            # Remove from joins table
            delete_query = """DELETE FROM joins 
                            WHERE student_number = %s AND org_id = %s AND year = %s AND semester = %s"""
            
            self.db.cursor.execute(delete_query, (student_number, org_id, year, semester))
            self.db.connection.commit()
            print("[SUCCESS] Member removed from organization successfully!")
            
        except ValueError:
            print("[ERROR] Invalid input.")
        except Exception as e:
            print(f"[ERROR] Error removing member from organization: {e}")

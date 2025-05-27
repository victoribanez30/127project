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

class FeesManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def manage_fees(self):
        """Main fees management menu"""
        print("\n=== Fees Management ===")
        print("1. Add new fee")
        print("2. Process payment")
        print("3. View member fees")
        print("4. View organization fees")
        print("5. Generate financial reports")
        
        choice = input("Choose option: ")
        
        if choice == '1':
            self.add_fee()
        elif choice == '2':
            self.process_payment()
        elif choice == '3':
            self.view_member_fees()
        elif choice == '4':
            self.view_org_fees()
        elif choice == '5':
            self.generate_reports()
        else:
            print("Invalid choice!")
    
    def add_fee(self):
        """Add a new fee for a member"""
        try:
            student_number = int(input("Student Number: "))
            
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            year = int(input("Year: "))
            semester = int(input("Semester: "))
            due_date = input("Due Date (YYYY-MM-DD): ")
            amount = float(input("Amount: "))
            
            query = """INSERT INTO fee (student_number, org_id, year, semester, 
                      due_date, status, amount) VALUES (%s, %s, %s, %s, %s, 'Unpaid', %s)"""
            values = (student_number, org_id, year, semester, due_date, amount)
            
            self.db.cursor.execute(query, values)
            self.db.connection.commit()
            print("✓ Fee added successfully!")
            
        except ValueError:
            print("✗ Invalid input format.")
        except Error as e:
            print(f"✗ Error adding fee: {e}")
    
    def process_payment(self):
        """Process a fee payment"""
        try:
            fee_id = int(input("Fee ID to pay: "))
            
            # Check if fee exists and is unpaid
            query = """SELECT f.fee_id, m.name, o.name, f.amount, f.status 
                      FROM fee f
                      JOIN member m ON f.student_number = m.student_number
                      JOIN org o ON f.org_id = o.org_id
                      WHERE f.fee_id = %s"""
            
            self.db.cursor.execute(query, (fee_id,))
            result = self.db.cursor.fetchone()
            
            if not result:
                print("✗ Fee not found!")
                return
            
            if result[4] == 'Paid':
                print("✗ This fee has already been paid!")
                return
            
            print(f"Fee Details:")
            print(f"Student: {result[1]}")
            print(f"Organization: {result[2]}")
            print(f"Amount: ₱{result[3]}")
            
            confirm = input("Confirm payment? (yes/no): ")
            if confirm.lower() == 'yes':
                # Use the stored procedure to process payment
                self.db.cursor.callproc('pay_fee', [fee_id])
                self.db.connection.commit()
                print("✓ Payment processed successfully!")
                print("Organization balance has been updated automatically.")
            else:
                print("Payment cancelled.")
                
        except ValueError:
            print("✗ Invalid fee ID.")
        except Error as e:
            print(f"✗ Error processing payment: {e}")
    
    def view_member_fees(self):
        """View all fees for a specific member"""
        try:
            student_number = int(input("Student Number: "))
            
            query = """SELECT f.fee_id, o.name, f.year, f.semester, f.amount, 
                             f.due_date, f.date_of_payment, f.status
                      FROM fee f
                      JOIN org o ON f.org_id = o.org_id
                      WHERE f.student_number = %s
                      ORDER BY f.year DESC, f.semester DESC"""
            
            self.db.cursor.execute(query, (student_number,))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Fee ID", "Organization", "Year", "Semester", "Amount", 
                          "Due Date", "Payment Date", "Status"]
                print(f"\nFees for Student {student_number}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                # Calculate totals
                total_amount = sum(row[4] for row in results)
                paid_amount = sum(row[4] for row in results if row[7] == 'Paid')
                unpaid_amount = total_amount - paid_amount
                
                print(f"\nSummary:")
                print(f"Total Amount: ₱{total_amount:.2f}")
                print(f"Paid Amount: ₱{paid_amount:.2f}")
                print(f"Unpaid Amount: ₱{unpaid_amount:.2f}")
            else:
                print("No fees found for this student!")
                
        except ValueError:
            print("✗ Invalid student number.")
        except Error as e:
            print(f"✗ Error viewing member fees: {e}")
    
    def view_org_fees(self):
        """View all fees for a specific organization"""
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            
            query = """SELECT f.fee_id, m.name, f.year, f.semester, f.amount, 
                             f.due_date, f.date_of_payment, f.status
                      FROM fee f
                      JOIN member m ON f.student_number = m.student_number
                      WHERE f.org_id = %s
                      ORDER BY f.year DESC, f.semester DESC, f.status"""
            
            self.db.cursor.execute(query, (org_id,))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Fee ID", "Student Name", "Year", "Semester", "Amount", 
                          "Due Date", "Payment Date", "Status"]
                print(f"\nFees for Organization {org_id}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
            else:
                print("No fees found for this organization!")
                
        except ValueError:
            print("✗ Invalid organization ID.")
        except Error as e:
            print(f"✗ Error viewing organization fees: {e}")
    
    def generate_reports(self):
        """Generate financial reports"""
        print("\n=== Financial Reports ===")
        print("1. Organization balance summary")
        print("2. Payment status report")
        print("3. Outstanding fees report")
        print("4. Monthly collection report")
        
        choice = input("Choose report type: ")
        
        if choice == '1':
            self.org_balance_report()
        elif choice == '2':
            self.payment_status_report()
        elif choice == '3':
            self.outstanding_fees_report()
        elif choice == '4':
            self.monthly_collection_report()
        else:
            print("Invalid choice!")
    
    def org_balance_report(self):
        """Generate organization balance summary"""
        try:
            query = """SELECT org_id, name, money_balance, type, year_established
                      FROM org
                      ORDER BY money_balance DESC"""
            
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Org ID", "Name", "Balance", "Type", "Established"]
                print("\nOrganization Balance Summary:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_balance = sum(row[2] for row in results)
                print(f"\nTotal System Balance: ₱{total_balance:.2f}")
            else:
                print("No organizations found!")
                
        except Error as e:
            print(f"✗ Error generating balance report: {e}")
    
    def payment_status_report(self):
        """Generate payment status report"""
        try:
            query = """SELECT o.name, 
                             COUNT(*) as total_fees,
                             SUM(CASE WHEN f.status = 'Paid' THEN 1 ELSE 0 END) as paid_fees,
                             SUM(CASE WHEN f.status = 'Unpaid' THEN 1 ELSE 0 END) as unpaid_fees,
                             SUM(f.amount) as total_amount,
                             SUM(CASE WHEN f.status = 'Paid' THEN f.amount ELSE 0 END) as collected_amount
                      FROM org o
                      LEFT JOIN fee f ON o.org_id = f.org_id
                      GROUP BY o.org_id, o.name
                      ORDER BY o.name"""
            
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Organization", "Total Fees", "Paid", "Unpaid", "Total Amount", "Collected"]
                print("\nPayment Status Report:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
            else:
                print("No data found!")
                
        except Error as e:
            print(f"✗ Error generating payment status report: {e}")
    
    def outstanding_fees_report(self):
        """Generate outstanding fees report"""
        try:
            query = """SELECT m.name, o.name, f.amount, f.due_date, 
                             DATEDIFF(CURRENT_DATE, f.due_date) as days_overdue
                      FROM fee f
                      JOIN member m ON f.student_number = m.student_number
                      JOIN org o ON f.org_id = o.org_id
                      WHERE f.status = 'Unpaid'
                      ORDER BY f.due_date ASC"""
            
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student", "Organization", "Amount", "Due Date", "Days Overdue"]
                print("\nOutstanding Fees Report:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_outstanding = sum(row[2] for row in results)
                print(f"\nTotal Outstanding Amount: ₱{total_outstanding:.2f}")
            else:
                print("No outstanding fees!")
                
        except Error as e:
            print(f"✗ Error generating outstanding fees report: {e}")
    
    def monthly_collection_report(self):
        """Generate monthly collection report"""
        try:
            year = int(input("Enter year (e.g., 2023): "))
            month = int(input("Enter month (1-12): "))
            
            query = """SELECT o.name, 
                             COUNT(*) as payments_count,
                             SUM(f.amount) as total_collected
                      FROM fee f
                      JOIN org o ON f.org_id = o.org_id
                      WHERE f.status = 'Paid' 
                        AND YEAR(f.date_of_payment) = %s 
                        AND MONTH(f.date_of_payment) = %s
                      GROUP BY o.org_id, o.name
                      ORDER BY total_collected DESC"""
            
            self.db.cursor.execute(query, (year, month))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Organization", "Payment Count", "Total Collected"]
                print(f"\nMonthly Collection Report for {year}-{month:02d}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_collected = sum(row[2] for row in results)
                print(f"\nTotal Monthly Collection: ₱{total_collected:.2f}")
            else:
                print("No collections found for this month!")
                
        except ValueError:
            print("✗ Invalid year or month.")
        except Error as e:
            print(f"✗ Error generating monthly collection report: {e}")

class AdvancedReports:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def advanced_reports_menu(self):
        """Advanced reports menu with all 10 reporting features"""
        while True:
            print("\n" + "=" * 70)
            print("                    ADVANCED REPORTS")
            print("=" * 70)
            print("1.  View members by role, status, gender, degree program, batch, committee")
            print("2.  View members with unpaid fees for specific semester/year")
            print("3.  View member's unpaid fees across all organizations")
            print("4.  View executive committee members for specific year")
            print("5.  View all Presidents (or any role) by year (chronological)")
            print("6.  View late payments for specific semester/year")
            print("7.  View active vs inactive members percentage (last n semesters)")
            print("8.  View alumni members as of specific date")
            print("9.  View total unpaid/paid fees as of specific date")
            print("10. View members with highest debt for specific semester")
            print("11. Back to main menu")
            
            choice = input("\nEnter your choice (1-11): ")
            
            if choice == '1':
                self.view_members_by_criteria()
            elif choice == '2':
                self.view_unpaid_fees_by_semester()
            elif choice == '3':
                self.view_member_unpaid_fees()
            elif choice == '4':
                self.view_executive_committee()
            elif choice == '5':
                self.view_role_history()
            elif choice == '6':
                self.view_late_payments()
            elif choice == '7':
                self.view_active_inactive_percentage()
            elif choice == '8':
                self.view_alumni_members()
            elif choice == '9':
                self.view_fees_summary_by_date()
            elif choice == '10':
                self.view_highest_debt()
            elif choice == '11':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_members_by_criteria(self):
        """1. View all members of the organization by role, status, gender, degree program, batch, and committee"""
        print("\n=== View Members by Criteria ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            
            print("\nFilter options (press Enter to skip any filter):")
            role_filter = input("Role (e.g., President, Secretary, Member): ")
            status_filter = input("Status (e.g., Active, Inactive): ")
            gender_filter = input("Gender (M/F): ")
            degprog_filter = input("Degree Program: ")
            batch_filter = input("Batch Year: ")
            committee_filter = input("Committee: ")
            
            # Build dynamic query
            base_query = """SELECT m.student_number, m.name, m.gender, m.batch, m.degprog,
                                  j.role, j.status, j.committee, j.year, j.semester
                           FROM member m
                           JOIN joins j ON m.student_number = j.student_number
                           WHERE j.org_id = %s"""
            
            params = [org_id]
            
            if role_filter:
                base_query += " AND j.role LIKE %s"
                params.append(f"%{role_filter}%")
            if status_filter:
                base_query += " AND j.status LIKE %s"
                params.append(f"%{status_filter}%")
            if gender_filter:
                base_query += " AND m.gender = %s"
                params.append(gender_filter.upper())
            if degprog_filter:
                base_query += " AND m.degprog LIKE %s"
                params.append(f"%{degprog_filter}%")
            if batch_filter:
                base_query += " AND m.batch = %s"
                params.append(int(batch_filter))
            if committee_filter:
                base_query += " AND j.committee LIKE %s"
                params.append(f"%{committee_filter}%")
            
            base_query += " ORDER BY j.year DESC, j.semester DESC, j.role, m.name"
            
            self.db.cursor.execute(base_query, params)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Gender", "Batch", "Degree Program", 
                          "Role", "Status", "Committee", "Year", "Semester"]
                print(f"\nMembers of Organization {org_id} (Filtered Results):")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                print(f"\nTotal members found: {len(results)}")
            else:
                print("No members found matching the criteria!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing members: {e}")
    
    def view_unpaid_fees_by_semester(self):
        """2. View members for a given organization with unpaid membership fees for a given semester and year"""
        print("\n=== Members with Unpaid Fees by Semester ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            year = int(input("Academic Year: "))
            semester = int(input("Semester (1 or 2): "))
            
            query = """SELECT m.student_number, m.name, m.phone_number, m.email,
                             f.fee_id, f.amount, f.due_date,
                             DATEDIFF(CURRENT_DATE, f.due_date) as days_overdue
                      FROM member m
                      JOIN fee f ON m.student_number = f.student_number
                      WHERE f.org_id = %s AND f.year = %s AND f.semester = %s 
                        AND f.status = 'Unpaid'
                      ORDER BY f.due_date ASC"""
            
            self.db.cursor.execute(query, (org_id, year, semester))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Phone", "Email", "Fee ID", 
                          "Amount", "Due Date", "Days Overdue"]
                print(f"\nMembers with Unpaid Fees - Year {year}, Semester {semester}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_unpaid = sum(row[5] for row in results)
                print(f"\nSummary:")
                print(f"Total members with unpaid fees: {len(results)}")
                print(f"Total unpaid amount: ₱{total_unpaid:.2f}")
            else:
                print("No unpaid fees found for this semester!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing unpaid fees: {e}")
    
    def view_member_unpaid_fees(self):
        """3. View a member's unpaid membership fees for all their organizations (Member's POV)"""
        print("\n=== Member's Unpaid Fees (All Organizations) ===")
        try:
            student_number = int(input("Student Number: "))
            
            # Get member name for display
            self.db.cursor.execute("SELECT name FROM member WHERE student_number = %s", (student_number,))
            member_result = self.db.cursor.fetchone()
            
            if not member_result:
                print("✗ Member not found!")
                return
            
            query = """SELECT o.name as organization, f.fee_id, f.year, f.semester,
                             f.amount, f.due_date,
                             DATEDIFF(CURRENT_DATE, f.due_date) as days_overdue
                      FROM fee f
                      JOIN org o ON f.org_id = o.org_id
                      WHERE f.student_number = %s AND f.status = 'Unpaid'
                      ORDER BY f.due_date ASC"""
            
            self.db.cursor.execute(query, (student_number,))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Organization", "Fee ID", "Year", "Semester", 
                          "Amount", "Due Date", "Days Overdue"]
                print(f"\nUnpaid Fees for {member_result[0]} (Student No. {student_number}):")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_debt = sum(row[4] for row in results)
                overdue_count = sum(1 for row in results if row[6] > 0)
                
                print(f"\nSummary:")
                print(f"Total unpaid fees: {len(results)}")
                print(f"Total debt: ₱{total_debt:.2f}")
                print(f"Overdue fees: {overdue_count}")
            else:
                print(f"No unpaid fees found for {member_result[0]}!")
                
        except ValueError:
            print("✗ Invalid student number.")
        except Error as e:
            print(f"✗ Error viewing member unpaid fees: {e}")
    
    def view_executive_committee(self):
        """4. View all executive committee members of a given organization for a given academic year"""
        print("\n=== Executive Committee Members ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            year = input("Academic Year (e.g., 2023): ")
            
            # Define executive roles (you can modify this list as needed)
            executive_roles = ['President', 'Vice President', 'Secretary', 'Treasurer', 
                             'Auditor', 'PRO', 'Business Manager']
            
            # Create placeholders for IN clause
            role_placeholders = ','.join(['%s'] * len(executive_roles))
            
            query = f"""SELECT m.student_number, m.name, m.phone_number, m.email,
                              j.role, j.committee, j.semester
                       FROM member m
                       JOIN joins j ON m.student_number = j.student_number
                       WHERE j.org_id = %s AND j.year = %s 
                         AND j.role IN ({role_placeholders})
                       ORDER BY 
                         CASE j.role
                           WHEN 'President' THEN 1
                           WHEN 'Vice President' THEN 2
                           WHEN 'Secretary' THEN 3
                           WHEN 'Treasurer' THEN 4
                           WHEN 'Auditor' THEN 5
                           WHEN 'PRO' THEN 6
                           WHEN 'Business Manager' THEN 7
                           ELSE 8
                         END, j.semester"""
            
            params = [org_id, year] + executive_roles
            self.db.cursor.execute(query, params)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Phone", "Email", "Role", "Committee", "Semester"]
                print(f"\nExecutive Committee Members for Year {year}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                print(f"\nTotal executive members: {len(results)}")
            else:
                print("No executive committee members found!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing executive committee: {e}")
    
    def view_role_history(self):
        """5. View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order"""
        print("\n=== Role History (Chronological) ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            role = input("Role to search (e.g., President, Secretary): ")
            
            query = """SELECT j.year, j.semester, m.student_number, m.name, 
                             m.phone_number, j.committee
                      FROM member m
                      JOIN joins j ON m.student_number = j.student_number
                      WHERE j.org_id = %s AND j.role LIKE %s
                      ORDER BY j.year DESC, j.semester DESC"""
            
            self.db.cursor.execute(query, (org_id, f"%{role}%"))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Year", "Semester", "Student No.", "Name", "Phone", "Committee"]
                print(f"\nHistory of {role} positions (Most Recent First):")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                print(f"\nTotal records found: {len(results)}")
                
                # Show summary by year
                years = list(set(row[0] for row in results))
                years.sort(reverse=True)
                print(f"\nYears with {role} positions: {', '.join(years)}")
            else:
                print(f"No {role} positions found!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing role history: {e}")
    
    def view_late_payments(self):
        """6. View all late payments made by all members of a given organization for a given semester and academic year"""
        print("\n=== Late Payments Report ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            year = int(input("Academic Year: "))
            semester = int(input("Semester (1 or 2): "))
            
            query = """SELECT m.student_number, m.name, f.fee_id, f.amount,
                             f.due_date, f.date_of_payment,
                             DATEDIFF(f.date_of_payment, f.due_date) as days_late
                      FROM member m
                      JOIN fee f ON m.student_number = f.student_number
                      WHERE f.org_id = %s AND f.year = %s AND f.semester = %s
                        AND f.status = 'Paid' 
                        AND f.date_of_payment > f.due_date
                      ORDER BY days_late DESC, f.date_of_payment DESC"""
            
            self.db.cursor.execute(query, (org_id, year, semester))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Fee ID", "Amount", 
                          "Due Date", "Payment Date", "Days Late"]
                print(f"\nLate Payments - Year {year}, Semester {semester}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_late_amount = sum(row[3] for row in results)
                avg_late_days = sum(row[6] for row in results) / len(results)
                
                print(f"\nSummary:")
                print(f"Total late payments: {len(results)}")
                print(f"Total amount (late payments): ₱{total_late_amount:.2f}")
                print(f"Average days late: {avg_late_days:.1f}")
            else:
                print("No late payments found for this semester!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing late payments: {e}")
    
    def view_active_inactive_percentage(self):
        """7. View the percentage of active vs inactive members of a given organization for the last n semesters"""
        print("\n=== Active vs Inactive Members Percentage ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            n_semesters = int(input("Number of semesters to analyze: "))
            
            # Get the last n semesters data
            query = """SELECT j.year, j.semester,
                             COUNT(*) as total_members,
                             SUM(CASE WHEN j.status = 'Active' THEN 1 ELSE 0 END) as active_members,
                             SUM(CASE WHEN j.status != 'Active' THEN 1 ELSE 0 END) as inactive_members
                      FROM joins j
                      WHERE j.org_id = %s
                      GROUP BY j.year, j.semester
                      ORDER BY j.year DESC, j.semester DESC
                      LIMIT %s"""
            
            self.db.cursor.execute(query, (org_id, n_semesters))
            results = self.db.cursor.fetchall()
            
            if results:
                print(f"\nActive vs Inactive Analysis (Last {n_semesters} semesters):")
                
                table_data = []
                for row in results:
                    year, semester, total, active, inactive = row
                    active_pct = (active / total * 100) if total > 0 else 0
                    inactive_pct = (inactive / total * 100) if total > 0 else 0
                    
                    table_data.append([
                        f"{year}-{semester}", total, active, inactive,
                        f"{active_pct:.1f}%", f"{inactive_pct:.1f}%"
                    ])
                
                headers = ["Semester", "Total", "Active", "Inactive", "Active %", "Inactive %"]
                print(tabulate(table_data, headers=headers, tablefmt="grid"))
                
                # Overall summary
                total_all = sum(row[2] for row in results)
                active_all = sum(row[3] for row in results)
                
                if total_all > 0:
                    overall_active_pct = (active_all / total_all * 100)
                    print(f"\nOverall Summary ({n_semesters} semesters):")
                    print(f"Average active percentage: {overall_active_pct:.1f}%")
                    print(f"Average inactive percentage: {100 - overall_active_pct:.1f}%")
            else:
                print("No membership data found!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing active/inactive percentage: {e}")
    
    def view_alumni_members(self):
        """8. View all alumni members of a given organization as of a given date"""
        print("\n=== Alumni Members Report ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            as_of_date = input("As of date (YYYY-MM-DD): ")
            
            # Alumni are members who have graduated (assuming graduated members have status 'Alumni')
            # or members whose batch year + 4 <= current year (typical 4-year degree)
            query = """SELECT DISTINCT m.student_number, m.name, m.batch, m.degprog,
                             m.phone_number, m.email, j.role,
                             YEAR(%s) - m.batch as years_since_entry
                      FROM member m
                      JOIN joins j ON m.student_number = j.student_number
                      WHERE j.org_id = %s 
                        AND (j.status = 'Alumni' 
                             OR (YEAR(%s) - m.batch >= 4 AND j.status != 'Active'))
                      ORDER BY m.batch ASC, m.name"""
            
            self.db.cursor.execute(query, (as_of_date, org_id, as_of_date))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Batch", "Degree Program", 
                          "Phone", "Email", "Last Role", "Years Since Entry"]
                print(f"\nAlumni Members as of {as_of_date}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                # Summary by batch
                batch_summary = {}
                for row in results:
                    batch = row[2]
                    batch_summary[batch] = batch_summary.get(batch, 0) + 1
                
                print(f"\nSummary:")
                print(f"Total alumni: {len(results)}")
                print("Alumni by batch:")
                for batch in sorted(batch_summary.keys()):
                    print(f"  Batch {batch}: {batch_summary[batch]} alumni")
            else:
                print("No alumni members found!")
                
        except ValueError:
            print("✗ Invalid input or date format.")
        except Error as e:
            print(f"✗ Error viewing alumni members: {e}")
    
    def view_fees_summary_by_date(self):
        """9. View the total amount of unpaid and paid fees of a given organization as of a given date"""
        print("\n=== Fees Summary by Date ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            as_of_date = input("As of date (YYYY-MM-DD): ")
            
            # Get organization name
            self.db.cursor.execute("SELECT name FROM org WHERE org_id = %s", (org_id,))
            org_result = self.db.cursor.fetchone()
            
            if not org_result:
                print("✗ Organization not found!")
                return
            
            query = """SELECT 
                         SUM(CASE WHEN f.status = 'Paid' AND f.date_of_payment <= %s THEN f.amount ELSE 0 END) as total_paid,
                         SUM(CASE WHEN f.status = 'Unpaid' AND f.due_date <= %s THEN f.amount ELSE 0 END) as total_unpaid,
                         COUNT(CASE WHEN f.status = 'Paid' AND f.date_of_payment <= %s THEN 1 END) as paid_count,
                         COUNT(CASE WHEN f.status = 'Unpaid' AND f.due_date <= %s THEN 1 END) as unpaid_count,
                         SUM(f.amount) as total_fees_amount,
                         COUNT(*) as total_fees_count
                      FROM fee f
                      WHERE f.org_id = %s AND f.due_date <= %s"""
            
            self.db.cursor.execute(query, (as_of_date, as_of_date, as_of_date, as_of_date, org_id, as_of_date))
            result = self.db.cursor.fetchone()
            
            if result:
                total_paid, total_unpaid, paid_count, unpaid_count, total_amount, total_count = result
                
                # Handle None values
                total_paid = total_paid or 0
                total_unpaid = total_unpaid or 0
                paid_count = paid_count or 0
                unpaid_count = unpaid_count or 0
                total_amount = total_amount or 0
                total_count = total_count or 0
                
                print(f"\nFees Summary for {org_result[0]} as of {as_of_date}:")
                print("=" * 60)
                
                summary_data = [
                    ["Total Paid Amount", f"₱{total_paid:.2f}", f"{paid_count} fees"],
                    ["Total Unpaid Amount", f"₱{total_unpaid:.2f}", f"{unpaid_count} fees"],
                    ["Total Fees Amount", f"₱{total_amount:.2f}", f"{total_count} fees"]
                ]
                
                headers = ["Category", "Amount", "Count"]
                print(tabulate(summary_data, headers=headers, tablefmt="grid"))
                
                if total_amount > 0:
                    collection_rate = (total_paid / total_amount * 100)
                    print(f"\nCollection Rate: {collection_rate:.1f}%")
                
                # Organization current balance
                self.db.cursor.execute("SELECT money_balance FROM org WHERE org_id = %s", (org_id,))
                balance_result = self.db.cursor.fetchone()
                if balance_result:
                    print(f"Current Organization Balance: ₱{balance_result[0]:.2f}")
            else:
                print("No fee data found!")
                
        except ValueError:
            print("✗ Invalid input or date format.")
        except Error as e:
            print(f"✗ Error viewing fees summary: {e}")
    
    def view_highest_debt(self):
        """10. View the member/s with the highest debt of a given organization for a given semester"""
        print("\n=== Members with Highest Debt ===")
        try:
            # Show available organizations
            self.db.cursor.execute("SELECT org_id, name FROM org")
            orgs = self.db.cursor.fetchall()
            
            print("\nAvailable Organizations:")
            for org in orgs:
                print(f"{org[0]}. {org[1]}")
            
            org_id = int(input("Organization ID: "))
            year = int(input("Academic Year: "))
            semester = int(input("Semester (1 or 2): "))
            
            query = """SELECT m.student_number, m.name, m.phone_number, m.email,
                             SUM(f.amount) as total_debt,
                             COUNT(f.fee_id) as unpaid_fees_count,
                             MIN(f.due_date) as earliest_due_date,
                             MAX(DATEDIFF(CURRENT_DATE, f.due_date)) as max_days_overdue
                      FROM member m
                      JOIN fee f ON m.student_number = f.student_number
                      WHERE f.org_id = %s AND f.year = %s AND f.semester = %s 
                        AND f.status = 'Unpaid'
                      GROUP BY m.student_number, m.name, m.phone_number, m.email
                      ORDER BY total_debt DESC, max_days_overdue DESC"""
            
            self.db.cursor.execute(query, (org_id, year, semester))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Phone", "Email", "Total Debt", 
                          "Unpaid Fees", "Earliest Due", "Max Days Overdue"]
                print(f"\nMembers with Highest Debt - Year {year}, Semester {semester}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                # Highlight the highest debt
                highest_debt = results[0][4]
                highest_debt_members = [row for row in results if row[4] == highest_debt]
                
                print(f"\nHighest Debt Analysis:")
                print(f"Maximum debt amount: ₱{highest_debt:.2f}")
                print(f"Number of members with highest debt: {len(highest_debt_members)}")
                
                if len(highest_debt_members) == 1:
                    print(f"Member with highest debt: {highest_debt_members[0][1]} (Student No. {highest_debt_members[0][0]})")
                else:
                    print("Members with highest debt:")
                    for member in highest_debt_members:
                        print(f"  - {member[1]} (Student No. {member[0]})")
                
                # Additional statistics
                total_system_debt = sum(row[4] for row in results)
                print(f"\nAdditional Statistics:")
                print(f"Total debt in system: ₱{total_system_debt:.2f}")
                print(f"Average debt per member: ₱{total_system_debt/len(results):.2f}")
                print(f"Members with debt: {len(results)}")
            else:
                print("No unpaid fees found for this semester!")
                
        except ValueError:
            print("✗ Invalid input.")
        except Error as e:
            print(f"✗ Error viewing highest debt: {e}")

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
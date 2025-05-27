#!/usr/bin/env python3
"""
Fees Management Module
Handles fee creation, payment processing, and financial reporting
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

class FeesManager:
    def __init__(self, db_manager, user_type=None, current_org_id=None, current_student_number=None):
        self.db = db_manager
        self.user_type = user_type
        self.current_org_id = current_org_id
        self.current_student_number = current_student_number
    
    def manage_fees(self):
        """Main fees management menu"""
        while True:
            print("\n" + "=" * 60)
            print("                FEES MANAGEMENT")
            print("=" * 60)
            print("1. View all members with fees (all organizations)")
            print("2. Add new fee")
            print("3. Process payment")
            print("4. View member fees")
            print("5. View organization fees")
            print("6. Generate financial reports")
            print("7. Back to main menu")
            
            choice = input("\nEnter your choice (1-7): ")
            
            if choice == '1':
                self.view_all_members_with_fees()
            elif choice == '2':
                self.add_fee()
            elif choice == '3':
                self.process_payment()
            elif choice == '4':
                self.view_member_fees()
            elif choice == '5':
                self.view_org_fees()
            elif choice == '6':
                self.generate_reports()
            elif choice == '7':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def add_fee(self):
    """Add a new fee for a member with proper validation"""
    try:
        student_number = int(input("Student Number: "))
        
        # First, check if the student exists
        student_check_query = "SELECT student_number, name FROM member WHERE student_number = %s"
        self.db.cursor.execute(student_check_query, (student_number,))
        student_result = self.db.cursor.fetchone()
        
        if not student_result:
            print(f"✗ Error: Student with number {student_number} does not exist!")
            print("Please check the student number or add the student to the system first.")
            return
        
        print(f"✓ Student found: {student_result[1]}")
        
        # Show available organizations
        self.db.cursor.execute("SELECT org_id, name FROM org")
        orgs = self.db.cursor.fetchall()
        
        if not orgs:
            print("✗ No organizations found in the system!")
            return
        
        print("\nAvailable Organizations:")
        for org in orgs:
            print(f"{org[0]}. {org[1]}")
        
        org_id = int(input("Organization ID: "))
        
        # Validate organization exists
        org_check_query = "SELECT org_id, name FROM org WHERE org_id = %s"
        self.db.cursor.execute(org_check_query, (org_id,))
        org_result = self.db.cursor.fetchone()
        
        if not org_result:
            print(f"✗ Error: Organization with ID {org_id} does not exist!")
            return
        
        print(f"✓ Organization found: {org_result[1]}")
        
        # Check if student is a member of this organization
        membership_check_query = """SELECT * FROM member 
                                   WHERE student_number = %s AND org_id = %s"""
        self.db.cursor.execute(membership_check_query, (student_number, org_id))
        membership_result = self.db.cursor.fetchone()
        
        if not membership_result:
            print(f"✗ Warning: Student {student_number} is not a member of {org_result[1]}!")
            confirm = input("Do you want to add a fee for a non-member? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Fee creation cancelled.")
                return
        else:
            print("✓ Student is a member of this organization.")
        
        # Check for duplicate fees (same student, org, year, semester)
        duplicate_check_query = """SELECT fee_id FROM fee 
                                  WHERE student_number = %s AND org_id = %s 
                                  AND year = %s AND semester = %s"""
        
        year = int(input("Year: "))
        semester = int(input("Semester: "))
        
        self.db.cursor.execute(duplicate_check_query, (student_number, org_id, year, semester))
        duplicate_result = self.db.cursor.fetchone()
        
        if duplicate_result:
            print(f"✗ Error: A fee already exists for this student in {org_result[1]} for {year} semester {semester}!")
            print(f"Existing fee ID: {duplicate_result[0]}")
            return
        
        # Validate due date format
        due_date = input("Due Date (YYYY-MM-DD): ")
        try:
            from datetime import datetime
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            print("✗ Error: Invalid date format! Please use YYYY-MM-DD format.")
            return
        
        amount = float(input("Amount: "))
        
        if amount <= 0:
            print("✗ Error: Amount must be greater than 0!")
            return
        
        # Display summary for confirmation
        print(f"\n=== Fee Summary ===")
        print(f"Student: {student_result[1]} ({student_number})")
        print(f"Organization: {org_result[1]}")
        print(f"Academic Period: {year} - Semester {semester}")
        print(f"Due Date: {due_date}")
        print(f"Amount: ₱{amount:.2f}")
        
        confirm = input("\nConfirm fee creation? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Fee creation cancelled.")
            return
        
        # Insert the fee
        query = """INSERT INTO fee (student_number, org_id, year, semester, 
                  due_date, status, amount) VALUES (%s, %s, %s, %s, %s, 'Unpaid', %s)"""
        values = (student_number, org_id, year, semester, due_date, amount)
        
        self.db.cursor.execute(query, values)
        self.db.connection.commit()
        
        # Get the inserted fee ID
        fee_id = self.db.cursor.lastrowid
        print(f"✓ Fee added successfully! Fee ID: {fee_id}")
        
    except ValueError as ve:
        print(f"✗ Invalid input format: {ve}")
        print("Please ensure numeric fields contain valid numbers.")
    except Error as e:
        print(f"✗ Database error adding fee: {e}")
        # Rollback in case of error
        self.db.connection.rollback()
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        self.db.connection.rollback()
    
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
    
    def view_all_members_with_fees(self):
        """View all members with fees regardless of organization"""
        try:
            print("\n=== All Members with Fees ===")
            print("1. View all fees (paid and unpaid)")
            print("2. View only unpaid fees")
            print("3. View only paid fees")
            
            sub_choice = input("Choose option (1-3): ")
            
            if sub_choice == '1':
                status_filter = ""
            elif sub_choice == '2':
                status_filter = "WHERE f.status = 'Unpaid'"
            elif sub_choice == '3':
                status_filter = "WHERE f.status = 'Paid'"
            else:
                print("Invalid choice!")
                return
            
            query = f"""SELECT m.student_number, m.name, m.phone_number, o.name as organization,
                              f.fee_id, f.amount, f.due_date, f.date_of_payment, f.status,
                              f.year, f.semester,
                              CASE 
                                WHEN f.status = 'Unpaid' AND f.due_date < CURRENT_DATE 
                                THEN DATEDIFF(CURRENT_DATE, f.due_date)
                                ELSE 0 
                              END as days_overdue
                       FROM member m
                       JOIN fee f ON m.student_number = f.student_number
                       JOIN org o ON f.org_id = o.org_id
                       {status_filter}
                       ORDER BY o.name, f.year DESC, f.semester DESC, 
                                CASE WHEN f.status = 'Unpaid' THEN 0 ELSE 1 END,
                                f.due_date ASC"""
            
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Phone", "Organization", "Fee ID", 
                          "Amount", "Due Date", "Payment Date", "Status", "Year", 
                          "Semester", "Days Overdue"]
                
                title = "All Members with Fees"
                if sub_choice == '2':
                    title = "All Members with Unpaid Fees"
                elif sub_choice == '3':
                    title = "All Members with Paid Fees"
                
                print(f"\n{title}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                # Summary statistics
                total_amount = sum(row[5] for row in results)
                paid_amount = sum(row[5] for row in results if row[8] == 'Paid')
                unpaid_amount = sum(row[5] for row in results if row[8] == 'Unpaid')
                overdue_count = sum(1 for row in results if row[11] > 0)
                
                print(f"\nSummary:")
                print(f"Total fee records: {len(results)}")
                print(f"Total amount: ₱{total_amount:.2f}")
                
                if sub_choice == '1':
                    print(f"Paid amount: ₱{paid_amount:.2f}")
                    print(f"Unpaid amount: ₱{unpaid_amount:.2f}")
                    print(f"Collection rate: {(paid_amount/total_amount*100):.1f}%" if total_amount > 0 else "Collection rate: 0%")
                
                if sub_choice == '1' or sub_choice == '2':
                    print(f"Overdue fees: {overdue_count}")
                
                # Organization breakdown
                org_summary = {}
                for row in results:
                    org = row[3]
                    if org not in org_summary:
                        org_summary[org] = {'count': 0, 'amount': 0}
                    org_summary[org]['count'] += 1
                    org_summary[org]['amount'] += row[5]
                
                print(f"\nBreakdown by Organization:")
                for org, data in sorted(org_summary.items()):
                    print(f"  {org}: {data['count']} fees, ₱{data['amount']:.2f}")
                    
            else:
                print("No fee records found!")
                
        except Error as e:            print(f"✗ Error viewing members with fees: {e}")
    
    def view_my_fees(self):
        """View fees for the logged-in member"""
        try:
            student_number = self.current_student_number
            if not student_number:
                print("✗ No student number available!")
                return
            
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
                print("\n=== My Fees ===")
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
                print("You have no fees recorded.")
                
        except Exception as e:
            print(f"✗ Error viewing fees: {e}")
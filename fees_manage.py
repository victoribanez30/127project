#!/usr/bin/env python3
"""
Fees Management Module
Handles fee creation, payment processing, and financial reporting
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

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
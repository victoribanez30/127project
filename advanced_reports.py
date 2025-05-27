#!/usr/bin/env python3
"""
Advanced Reports Module for Organization Management System
Contains the AdvancedReports class with 10 advanced reporting features
"""

import mysql.connector
from mysql.connector import Error
from tabulate import tabulate

class AdvancedReports:
    def __init__(self, db_manager, user_type=None, current_org_id=None):
        self.db = db_manager
        self.user_type = user_type
        self.current_org_id = current_org_id
    
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
            base_query = """SELECT m.student_number, m.name, m.username, m.gender, m.batch, m.degprog,
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
                headers = ["Student No.", "Name", "Username", "Gender", "Batch", "Degree Program", 
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
            query = """SELECT m.student_number, m.name, m.username, m.phone_number, m.email,
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
                headers = ["Student No.", "Name", "Username", "Phone", "Email", "Fee ID", 
                          "Amount", "Due Date", "Days Overdue"]
                print(f"\nMembers with Unpaid Fees - Year {year}, Semester {semester}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_unpaid = sum(row[6] for row in results)
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
            self.db.cursor.execute("SELECT name, username FROM member WHERE student_number = %s", (student_number,))
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
                print(f"\nUnpaid Fees for {member_result[0]} (@{member_result[1]}) (Student No. {student_number}):")
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
            query = f"""SELECT m.student_number, m.name, m.username, m.phone_number, m.email,
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
                headers = ["Student No.", "Name", "Username", "Phone", "Email", "Role", "Committee", "Semester"]
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
            query = """SELECT j.year, j.semester, m.student_number, m.name, m.username,
                             m.phone_number, j.committee
                      FROM member m
                      JOIN joins j ON m.student_number = j.student_number
                      WHERE j.org_id = %s AND j.role LIKE %s
                      ORDER BY j.year DESC, j.semester DESC"""
            
            self.db.cursor.execute(query, (org_id, f"%{role}%"))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Year", "Semester", "Student No.", "Name", "Username", "Phone", "Committee"]
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
            query = """SELECT m.student_number, m.name, m.username, f.fee_id, f.amount,
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
                headers = ["Student No.", "Name", "Username", "Fee ID", "Amount", 
                          "Due Date", "Payment Date", "Days Late"]
                print(f"\nLate Payments - Year {year}, Semester {semester}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_late_amount = sum(row[4] for row in results)
                avg_late_days = sum(row[7] for row in results) / len(results)
                
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
            
            query = """SELECT m.student_number, m.name, m.username, m.phone_number, m.email,
                             SUM(f.amount) as total_debt,
                             COUNT(f.fee_id) as unpaid_fees_count,
                             MIN(f.due_date) as earliest_due_date,
                             MAX(DATEDIFF(CURRENT_DATE, f.due_date)) as max_days_overdue
                      FROM member m
                      JOIN fee f ON m.student_number = f.student_number
                      WHERE f.org_id = %s AND f.year = %s AND f.semester = %s 
                        AND f.status = 'Unpaid'
                      GROUP BY m.student_number, m.name, m.username, m.phone_number, m.email
                      ORDER BY total_debt DESC, max_days_overdue DESC"""
            
            self.db.cursor.execute(query, (org_id, year, semester))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Username", "Phone", "Email", "Total Debt", 
                          "Unpaid Fees", "Earliest Due", "Max Days Overdue"]
                print(f"\nMembers with Highest Debt - Year {year}, Semester {semester}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                # Highlight the highest debt
                highest_debt = results[0][5]
                highest_debt_members = [row for row in results if row[5] == highest_debt]
                
                print(f"\nHighest Debt Analysis:")
                print(f"Maximum debt amount: ₱{highest_debt:.2f}")
                print(f"Number of members with highest debt: {len(highest_debt_members)}")
                
                if len(highest_debt_members) == 1:
                    print(f"Member with highest debt: {highest_debt_members[0][1]} (@{highest_debt_members[0][2]}) (Student No. {highest_debt_members[0][0]})")
                else:
                    print("Members with highest debt:")
                    for member in highest_debt_members:
                        print(f"  - {member[1]} (@{member[2]}) (Student No. {member[0]})")
                
                # Additional statistics
                total_system_debt = sum(row[5] for row in results)
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
    
    def basic_reports_menu(self):
        """Basic reports menu for limited access users"""
        while True:
            print("\n" + "=" * 60)
            print("                    BASIC REPORTS")
            print("=" * 60)
            print("1. View organization members")
            print("2. View organization fees summary")
            print("3. View unpaid fees")
            print("4. View payment history")
            print("5. Back to main menu")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == '1':
                self.view_own_org_members()
            elif choice == '2':
                self.view_own_org_fees_summary()
            elif choice == '3':
                self.view_own_org_unpaid_fees()
            elif choice == '4':
                self.view_own_org_payment_history()
            elif choice == '5':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_own_org_members(self):
        """View members of current organization (for limited access)"""
        if self.user_type != "user" or not self.current_org_id:
            print("✗ This function is only available for organization users.")
            return
        
        try:
            query = """SELECT m.student_number, m.name, m.username, m.phone_number, m.email,
                             m.gender, m.batch, m.degprog, j.role, j.status, 
                             j.committee, j.year, j.semester
                      FROM member m
                      JOIN joins j ON m.student_number = j.student_number
                      WHERE j.org_id = %s
                      ORDER BY j.year DESC, j.semester DESC, j.role, m.name"""
            
            self.db.cursor.execute(query, (self.current_org_id,))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student No.", "Name", "Username", "Phone", "Email", "Gender", "Batch", 
                          "Degree Program", "Role", "Status", "Committee", "Year", "Semester"]
                print("\nOrganization Members:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                  # Summary
                total_members = len(results)
                active_members = sum(1 for row in results if row[9] == 'Active')
                
                print(f"\nSummary:")
                print(f"Total members: {total_members}")
                print(f"Active members: {active_members}")
                print(f"Inactive members: {total_members - active_members}")
            else:
                print("No members found for your organization!")
                
        except Error as e:
            print(f"✗ Error viewing organization members: {e}")
    
    def view_own_org_fees_summary(self):
        """View fees summary for current organization"""
        if self.user_type != "user" or not self.current_org_id:
            print("✗ This function is only available for organization users.")
            return
        
        try:
            query = """SELECT 
                         COUNT(*) as total_fees,
                         SUM(f.amount) as total_amount,
                         SUM(CASE WHEN f.status = 'Paid' THEN f.amount ELSE 0 END) as paid_amount,
                         SUM(CASE WHEN f.status = 'Unpaid' THEN f.amount ELSE 0 END) as unpaid_amount,
                         COUNT(CASE WHEN f.status = 'Paid' THEN 1 END) as paid_count,
                         COUNT(CASE WHEN f.status = 'Unpaid' THEN 1 END) as unpaid_count
                      FROM fee f
                      WHERE f.org_id = %s"""
            
            self.db.cursor.execute(query, (self.current_org_id,))
            result = self.db.cursor.fetchone()
            
            if result and result[0] > 0:
                total_fees, total_amount, paid_amount, unpaid_amount, paid_count, unpaid_count = result
                collection_rate = (paid_amount / total_amount * 100) if total_amount > 0 else 0
                
                print("\nFees Summary for Your Organization:")
                print("=" * 50)
                
                summary_data = [
                    ["Total Fees", total_fees, f"₱{total_amount:.2f}"],
                    ["Paid Fees", paid_count, f"₱{paid_amount:.2f}"],
                    ["Unpaid Fees", unpaid_count, f"₱{unpaid_amount:.2f}"],
                    ["Collection Rate", f"{collection_rate:.1f}%", ""]
                ]
                
                headers = ["Category", "Count", "Amount"]
                print(tabulate(summary_data, headers=headers, tablefmt="grid"))
                
                # Current organization balance
                self.db.cursor.execute("SELECT money_balance FROM org WHERE org_id = %s", (self.current_org_id,))
                balance_result = self.db.cursor.fetchone()
                if balance_result:
                    print(f"\nCurrent Organization Balance: ₱{balance_result[0]:.2f}")
            else:
                print("No fee records found for your organization!")
                
        except Error as e:
            print(f"✗ Error viewing fees summary: {e}")
    
    def view_own_org_unpaid_fees(self):
        """View unpaid fees for current organization"""
        if self.user_type != "user" or not self.current_org_id:
            print("✗ This function is only available for organization users.")
            return
        
        try:
            query = """SELECT m.name, m.username, f.fee_id, f.amount, f.due_date,
                             f.year, f.semester,
                             DATEDIFF(CURRENT_DATE, f.due_date) as days_overdue
                      FROM fee f
                      JOIN member m ON f.student_number = m.student_number
                      WHERE f.org_id = %s AND f.status = 'Unpaid'
                      ORDER BY f.due_date ASC"""
            
            self.db.cursor.execute(query, (self.current_org_id,))
            results = self.db.cursor.fetchall()
            
            if results:
                headers = ["Student Name", "Username", "Fee ID", "Amount", "Due Date", "Year", "Semester", "Days Overdue"]
                print("\nUnpaid Fees:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                total_unpaid = sum(row[3] for row in results)
                overdue_count = sum(1 for row in results if row[7] > 0)
                
                print(f"\nSummary:")
                print(f"Total unpaid fees: {len(results)}")
                print(f"Total unpaid amount: ₱{total_unpaid:.2f}")
                print(f"Overdue fees: {overdue_count}")
            else:
                print("No unpaid fees found!")
                
        except Error as e:
            print(f"✗ Error viewing unpaid fees: {e}")
    
    def view_own_org_payment_history(self):
        """View payment history for current organization"""
        if self.user_type != "user" or not self.current_org_id:
            print("✗ This function is only available for organization users.")
            return
        
        try:
            print("\nPayment History Options:")
            print("1. Last 30 days")
            print("2. Last 90 days")
            print("3. This year")
            print("4. All time")
            
            choice = input("Choose option (1-4): ")
            
            if choice == '1':
                date_filter = "AND f.date_of_payment >= DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)"
                title = "Last 30 Days"
            elif choice == '2':
                date_filter = "AND f.date_of_payment >= DATE_SUB(CURRENT_DATE, INTERVAL 90 DAY)"
                title = "Last 90 Days"
            elif choice == '3':
                date_filter = "AND YEAR(f.date_of_payment) = YEAR(CURRENT_DATE)"
                title = "This Year"
            elif choice == '4':
                date_filter = ""
                title = "All Time"
            else:
                print("Invalid choice!")
                return
            
            # Remove username from the query as it doesn't exist in the database
            query = f"""SELECT m.name, f.fee_id, f.amount, f.due_date, f.date_of_payment,
                              f.year, f.semester
                       FROM fee f
                       JOIN member m ON f.student_number = m.student_number
                       WHERE f.org_id = %s AND f.status = 'Paid' {date_filter}
                       ORDER BY f.date_of_payment DESC"""
            
            self.db.cursor.execute(query, (self.current_org_id,))
            results = self.db.cursor.fetchall()
            
            if results:
                # Adjust headers to match the removed username column
                headers = ["Student Name", "Fee ID", "Amount", "Due Date", "Payment Date", "Year", "Semester"]
                print(f"\nPayment History - {title}:")
                print(tabulate(results, headers=headers, tablefmt="grid"))
                
                # Adjust index for amount as it's now at position 2 instead of 3
                total_collected = sum(row[2] for row in results)
                print(f"\nSummary:")
                print(f"Total payments: {len(results)}")
                print(f"Total amount collected: ₱{total_collected:.2f}")
            else:
                print(f"No payments found for {title.lower()}!")
                
        except Error as e:
            print(f"✗ Error viewing payment history: {e}")
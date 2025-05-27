# Organization Management System

A terminal-based application for managing organization memberships and fees, built with Python and MySQL.

## Features

### Core Functionality

#### 1. Membership Management
- **Add, update, delete, and search for members**
  - Complete member profile management (student number, name, contact info, etc.)
  - Search by name, student number, or degree program
  - View all members in a formatted table

- **Track members' roles and membership status**
  - Assign roles: President, Treasurer, Secretary, Member, etc.
  - Track status: Active, Inactive, Expelled, Suspended, Alumni
  - Support for multiple organization memberships per student

- **Organization membership management**
  - Add/remove members to/from organizations
  - Update member roles and status within organizations
  - View organization member lists with detailed information

#### 2. Fees Management
- **Manage membership fees and dues**
  - Add new fees for members
  - Process fee payments with automatic balance updates
  - Track payment status (Paid/Unpaid) and dates
  - Support for semester-based fee tracking

- **Generate comprehensive financial reports**
  - Organization balance summary
  - Payment status reports by organization
  - Outstanding fees with overdue tracking
  - Monthly collection reports
  - Automatic calculation of totals and summaries

#### 3. Organization Management
- **Complete organization lifecycle management**
  - Add new organizations with all required details
  - Update organization information (name, type, balance, credentials)
  - Delete organizations with safety checks for related data
  - Search organizations by name, type, or year established

- **Organization overview and analytics**
  - View all organizations with member and fee statistics
  - Monitor organization balances and financial health
  - Track membership counts across organizations
  - Comprehensive organization profile management

#### 4. Advanced Reports (10 Specialized Views)
- **Detailed member analysis and filtering**
  - View members by role, status, gender, degree program, batch, and committee
  - View members with unpaid fees for specific semesters
  - View individual member's unpaid fees across all organizations
  - View executive committee members by academic year

- **Historical and trend analysis**
  - View role history (e.g., all Presidents) in chronological order
  - View late payment patterns by semester
  - Analyze active vs inactive member percentages over time
  - View alumni members as of specific dates

- **Financial debt analysis**
  - View comprehensive fee summaries by date
  - Identify members with highest debt by semester
  - Track payment trends and collection rates

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- MySQL Server
- Access to the `127project` database (as defined in Project.sql)

### Installation

1. **Clone or download the project files**
   ```
   Project.py
   Project.sql
   requirements.txt
   README.md
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   - Run the `Project.sql` file in your MySQL server to create the database, tables, and sample data
   - Ensure the MySQL server is running and accessible

4. **Configure database connection**
   - The application uses these default connection settings:
     - Host: `localhost`
     - Database: `127project`
     - User: `admin`
     - Password: `admin`
   - Modify the connection parameters in `DatabaseManager.connect()` if needed

## Usage

### Running the Application

```bash
python Project.py
```

### Main Menu Navigation

The application provides an intuitive menu-driven interface:

```
============================================================
                    MAIN MENU
============================================================
1. Membership Management
2. Fees Management
3. Advanced Reports
4. Organization Management
5. Exit
```

### Membership Management Features

1. **Add new member** - Register new students in the system
2. **Update member information** - Modify contact details and personal info
3. **Delete member** - Remove members from the system (with confirmation)
4. **Search members** - Find members by various criteria
5. **Manage organization membership** - Handle organization-specific memberships

#### Organization Membership Sub-menu:
- Add member to organization
- Update member role/status in organization
- Remove member from organization
- View all members of an organization

### Fees Management Features

1. **Add new fee** - Create fee records for members
2. **Process payment** - Mark fees as paid and update organization balances
3. **View member fees** - See all fees for a specific student
4. **View organization fees** - See all fees for a specific organization
5. **Generate financial reports** - Comprehensive reporting system

#### Financial Reports:
- **Organization balance summary** - Current balances of all organizations
- **Payment status report** - Payment statistics by organization
- **Outstanding fees report** - Unpaid fees with overdue information
- **Monthly collection report** - Collection summary for specific months

### Organization Management Features

1. **Add new organization** - Register new organizations with complete details
2. **Update organization information** - Modify organization details, balances, and credentials
3. **Delete organization** - Remove organizations with safety checks for related data
4. **Search organizations** - Find organizations by name, type, or establishment year
5. **View all organizations** - Comprehensive overview with statistics

#### Organization Management Details:
- **Complete organization profiles** - Name, type, establishment year, balance, credentials
- **Data integrity protection** - Warnings when deleting organizations with members/fees
- **Financial oversight** - Monitor and update organization balances
- **Statistical summaries** - View member counts, fee records, and system totals
- **Search and filtering** - Multiple search criteria for easy organization discovery

## Database Schema

The system works with the following main tables:

- **`member`** - Student information and credentials
- **`org`** - Organization details and balances
- **`joins`** - Membership relationships between students and organizations
- **`fee`** - Fee records and payment tracking

## Key Features

### Automatic Balance Updates
- Uses MySQL triggers to automatically update organization balances when payments are processed
- Stored procedures ensure data consistency during payment processing

### Comprehensive Reporting
- Real-time financial status tracking
- Detailed payment history and outstanding balance reports
- Support for filtering by time periods and organizations

### User-Friendly Interface
- Clear menu navigation with numbered options
- Formatted table output using tabulate library
- Input validation and error handling
- Confirmation prompts for destructive operations

### Multi-Organization Support
- Students can be members of multiple organizations
- Separate fee tracking per organization
- Role-based membership management

## Error Handling

The application includes comprehensive error handling for:
- Database connection issues
- Invalid user input
- Missing records
- MySQL constraint violations
- Network connectivity problems

## Security Features

- Password-protected database access
- Input sanitization using parameterized queries
- Protection against SQL injection attacks
- Secure password input for sensitive operations

## Sample Data

The system comes with sample data including:
- 3 sample students
- 2 sample organizations
- Sample membership records
- Sample fee records

This allows you to test all features immediately after setup.

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Verify MySQL server is running
   - Check connection credentials
   - Ensure the `127project` database exists

2. **Permission denied errors**
   - Verify user permissions in MySQL
   - Check if the admin user has proper grants

3. **Module not found errors**
   - Install required dependencies: `pip install -r requirements.txt`
   - Ensure Python path is configured correctly

4. **Invalid input errors**
   - Follow the input format guidelines shown in prompts
   - Use numeric inputs where specified
   - Use proper date format (YYYY-MM-DD) for dates

## Future Enhancements

Potential areas for expansion:
- Web-based interface
- Email notifications for due dates
- Backup and restore functionality
- Advanced reporting with charts
- Integration with external payment systems
- Multi-currency support

## Support

For issues or questions, refer to the error messages displayed by the application, which provide specific guidance for resolving common problems.

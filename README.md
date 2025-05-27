# Organization, Fees, and Members Management System

A terminal-based application for managing organization memberships and fees, built with Python and MySQL.

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



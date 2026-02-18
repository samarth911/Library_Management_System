# Library Management System

A web-based library management application built with **FastAPI** and **Uvicorn**, designed to handle book management, member registration, issue/return transactions, fine calculations, and reporting.

---

## Project Overview

This system provides two main user roles:
- **Admin**: Manages books inventory, memberships, and generates system reports
- **Member/User**: Searches books, issues/returns books, and tracks fines

---

## System Workflow

### 1. **User Authentication**
   - Access `/admin-login` for admin authentication
   - Access `/user-login` for member login
   - Credentials validated against database

### 2. **Admin Operations**
   - **Maintenance**: Add/update books, manage memberships, user management
   - **Reports**: View overdue returns, active issues, complete master list

### 3. **Member Transactions**
   - **Search Books**: Find available books in inventory
   - **Issue Books**: Borrow books from library
   - **Return Books**: Return borrowed books
   - **Fine Tracking**: Track and pay outstanding fines

### 4. **System Reports**
   - Overdue returns monitoring
   - Active issues tracking
   - Master inventory listing

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Library_Management_System
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install fastapi uvicorn
# Install other dependencies as needed (e.g., sqlalchemy, python-dotenv, etc.)
```

### Step 4: Setup Database
```bash
# Run schema.sql to create tables
# Example: sqlite3 library.db < app/database/schema.sql
```

---

## Running the Application

### Start the Server
From the project root directory:

```bash
cd app
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### Access the Application
1. Open your web browser
2. Navigate to: **`http://localhost:8000/admin-login`**
3. Enter admin credentials to login and explore the system

### Available Endpoints
- **Admin Login**: `http://localhost:8000/admin-login`
- **Member Login**: `http://localhost:8000/user-login`
- **Admin Dashboard**: `http://localhost:8000/admin/home` (after login)
- **Member Dashboard**: `http://localhost:8000/user/home` (after login)

---

## Key Features

✅ **Role-based Access Control** (Admin & Member)
✅ **Book Inventory Management** (Add, Update, Search)
✅ **Membership Management** (Register, Update members)
✅ **Issue & Return Transactions** (Track borrowed books)
✅ **Fine Calculation** (Automatic fine tracking)
✅ **Comprehensive Reporting** (Overdue, Active issues, Master list)
✅ **User-friendly Interface** (HTML templates with responsive design)

---

## Technology Stack

- **Backend**: FastAPI (Python)
- **Server**: Uvicorn
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQL (SQLite/PostgreSQL)

---

## Testing the System

1. **Admin Access**:
   - Go to `http://localhost:8000/admin-login`
   - Login with admin credentials
   - Navigate through maintenance and reports sections

2. **Member Access**:
   - Go to `http://localhost:8000/user-login`
   - Login with member credentials
   - Search books and manage transactions

---

## Troubleshooting

### Port 8000 Already in Use
```bash
uvicorn main:app --reload --port 8001
```

### Module Import Errors
Ensure you're in the `/app` directory when running uvicorn:
```bash
cd /path/to/Library_Management_System/app
uvicorn main:app --reload
```

### Database Connection Issues
Verify the database connection string in `app/database/connection.py`

---

## Future Enhancements

- Email notifications for overdue books
- SMS reminders for members
- Online payment integration for fines
- Mobile app version
- Advanced analytics and dashboards

---
## Directory Structure

```
library-management-system/
│
├── app/                                    # Main application package
│   ├── main.py                             # FastAPI app entry point
│   │
│   ├── database/                           # Database configuration
│   │   ├── connection.py                   # DB connection setup
│   │   └── schema.sql                      # Database schema
│   │
│   ├── auth/                               # Authentication module
│   │   ├── login_controller.py             # Login request handling
│   │   └── auth_service.py                 # Authentication logic
│   │
│   ├── maintenance/                        # Admin operations (CRUD)
│   │   ├── add_book.py                     # Add new books
│   │   ├── update_book.py                  # Edit book details
│   │   ├── add_membership.py               # Register new members
│   │   ├── update_membership.py            # Update member info
│   │   └── user_management.py              # User account management
│   │
│   ├── transactions/                       # Core library transactions
│   │   ├── search_book.py                  # Book search functionality
│   │   ├── book_availability.py            # Check book availability
│   │   ├── issue_book.py                   # Issue book to member
│   │   └── return_book.py                  # Process book return
│   │
│   ├── reports/                            # Analytics & reports
│   │   ├── overdue_returns.py              # Overdue books report
│   │   ├── active_issues.py                # Active issued books report
│   │   ├── master_list.py                  # Complete inventory report
│   │   └── reports_service.py              # Report generation logic
│   │
│   └── utils/                              # Helper utilities
│       └── feedback_routes.py              # Feedback/logging routes
│
├── templates/                              # HTML UI templates
│   ├── auth/
│   │   ├── admin_login.html                # Admin login page
│   │   └── user_login.html                 # Member login page
│   │
│   ├── admin/                              # Admin dashboard pages
│   │   ├── home.html                       # Admin home dashboard
│   │   ├── add_book.html                   # Book addition form
│   │   ├── update_book.html                # Book update form
│   │   ├── add_membership.html             # Member registration form
│   │   ├── update_membership.html          # Member update form
│   │   ├── user_management.html            # User management page
│   │   └── reports/                        # Admin reports
│   │       ├── overdue_returns.html
│   │       ├── active_issues.html
│   │       └── master_members.html
│   │
│   ├── user/                               # Member pages
│   │   ├── home.html                       # Member home dashboard
│   │   └── reports/                        # Member reports
│
│   └── shared/                             # Shared components
│       ├── navbar.html                     # Navigation bar
│       ├── confirmation.html               # Confirmation dialog
│       └── cancellation.html               # Cancellation dialog
│
├── static/                                 # Static assets
│   └── css/
│       └── style.css                       # Global styling
│
└── README.md                               # This file
```

---

## License

This project is part of the Library Management System initiative.

---

## Support & Documentation

For issues or questions, please refer to the inline code documentation or contact the development team.

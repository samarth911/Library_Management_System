library-management-system/
│
├── app/                        # Main application
│   ├── main.py                 # Entry point (server start)
│   ├── config.py               # Settings, constants
│
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── seed_data.sql
│
│   ├── models/                 # Tables (Entities)
│   │   ├── user_model.py
│   │   ├── member_model.py
│   │   ├── book_model.py
│   │   ├── movie_model.py
│   │   ├── issue_model.py
│   │   ├── fine_model.py
│   │   └── transaction_model.py
│
│   ├── auth/
│   │   ├── login_controller.py
│   │   ├── auth_service.py
│   │   └── password_utils.py
│
│   ├── maintenance/            # Admin only
│   │   ├── add_book.py
│   │   ├── update_book.py
│   │   ├── add_membership.py
│   │   ├── update_membership.py
│   │   ├── user_management.py
│   │   └── master_data_service.py
│
│   ├── transactions/
│   │   ├── search_book.py
│   │   ├── issue_book.py
│   │   ├── return_book.py
│   │   ├── fine_payment.py
│   │   └── transaction_service.py
│
│   ├── reports/
│   │   ├── overdue_returns.py
│   │   ├── active_issues.py
│   │   └── reports_service.py
│
│   ├── validations/
│   │   ├── form_validators.py
│   │   ├── date_validators.py
│   │   └── permission_validator.py
│
│   └── utils/
│       ├── date_utils.py
│       ├── response_messages.py
│       └── helpers.py
│
├── templates/                  # All UI pages
│   ├── auth/
│   │   ├── admin_login.html
│   │   └── user_login.html
│
│   ├── admin/
│   │   ├── home.html
│   │   ├── maintenance/
│   │   └── reports/
│
│   ├── user/
│   │   ├── home.html
│   │   ├── transactions/
│   │   └── reports/
│
│   └── shared/
│       ├── navbar.html
│       ├── confirmation.html
│       └── cancellation.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── README.md

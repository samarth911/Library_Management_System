CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('ADMIN','USER') NOT NULL,
    status ENUM('ACTIVE','BLOCKED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    membership_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    address TEXT,
    membership_start_date DATE NOT NULL,
    membership_end_date DATE NOT NULL,
    membership_status ENUM('ACTIVE','EXPIRED','CANCELLED') DEFAULT 'ACTIVE',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(150) NOT NULL,
    category ENUM('BOOK','MOVIE') DEFAULT 'BOOK',
    publication_year INT,
    rack_location VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE item_copies (
    copy_id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    serial_no VARCHAR(50) UNIQUE NOT NULL,
    status ENUM('AVAILABLE','ISSUED','LOST','DAMAGED') DEFAULT 'AVAILABLE',
    purchase_date DATE,
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

CREATE TABLE issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    copy_id INT NOT NULL,
    member_id INT NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    issued_by INT,
    status ENUM('ISSUED','RETURNED') DEFAULT 'ISSUED',
    remarks TEXT,
    FOREIGN KEY (copy_id) REFERENCES item_copies(copy_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (issued_by) REFERENCES users(user_id)
);

CREATE TABLE fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    issue_id INT UNIQUE,
    calculated_amount DECIMAL(8,2) DEFAULT 0,
    paid_amount DECIMAL(8,2) DEFAULT 0,
    is_paid BOOLEAN DEFAULT FALSE,
    paid_date DATE,
    remarks TEXT,
    FOREIGN KEY (issue_id) REFERENCES issues(issue_id)
);

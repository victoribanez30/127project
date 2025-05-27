-- ST16L
-- Ibanez, Victor
-- De Guzman, Maria Gracy
-- Manaoat, Tanya

-- Milestone 3: Database Setup

-- Create user and database
CREATE OR REPLACE USER 'admin' IDENTIFIED BY 'admin';
CREATE OR REPLACE USER 'user1' IDENTIFIED BY 'victor';
CREATE OR REPLACE USER 'user2' IDENTIFIED BY 'tanya';
CREATE OR REPLACE USER 'user3' IDENTIFIED BY 'gracy';

CREATE DATABASE IF NOT EXISTS 127project;
USE 127project;

GRANT ALL ON 127project.* TO 'admin';

-- Drop existing tables if they exist
DROP TABLE IF EXISTS fee;
DROP TABLE IF EXISTS joins;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS org;


-- Tables ------------------------------------------------------------------------------------------------
-- Org Table
CREATE TABLE org (
    org_id INT(3) AUTO_INCREMENT PRIMARY KEY,
    money_balance DECIMAL(10,2) NOT NULL,
    type VARCHAR(10),
    name VARCHAR(50) NOT NULL,
    year_established INT(4) NOT NULL,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

-- Member Table
CREATE TABLE member (
    student_number INT(9) PRIMARY KEY,
    phone_number VARCHAR(11) NOT NULL,
    name VARCHAR(55) NOT NULL,
    username VARCHAR(40) NOT NULL,
    gender VARCHAR(1),
    batch INT(4) NOT NULL,
    degprog VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(20) NOT NULL
);

-- Fee Table
CREATE TABLE fee (
    fee_id INT(4) AUTO_INCREMENT PRIMARY KEY,
    student_number INT(9) NOT NULL,
    org_id INT(3) NOT NULL,
    year INT(4) NOT NULL,
    semester INT(1) NOT NULL,
    due_date DATE NOT NULL,
    date_of_payment DATE,
    status VARCHAR(6) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    CONSTRAINT fee_org_org_id FOREIGN KEY(org_id) REFERENCES org(org_id),
    CONSTRAINT fee_member_student_number FOREIGN KEY(student_number) REFERENCES member(student_number)
);

-- Joins Table
CREATE TABLE joins (
    student_number INT(9),
    org_id INT(3),
    year VARCHAR(5),
    semester INT(1),
    committee VARCHAR(10),
    role VARCHAR(10),
    status VARCHAR(10),
    PRIMARY KEY(student_number, org_id, year, semester),
    CONSTRAINT joins_member_student_number FOREIGN KEY (student_number) REFERENCES member(student_number),
    CONSTRAINT joins_org_org_id FOREIGN KEY (org_id) REFERENCES org(org_id)
);

-- Insert sample data into tables
-- Members
INSERT INTO member (student_number, phone_number, name, username, gender, batch, degprog, email, password) VALUES
(202300001, '09123456781', 'Tanya Mabait', 'tanya_mabait', 'F', 2023, 'BS Computer Science', 'tanya.mabait@example.com', 'pass123'),
(202300002, '09123456782', 'Gracy Deneguan', 'gracy_deneguan', 'F', 2023, 'BS Information Technology', 'gracy.deneguan@example.com', 'pass456'),
(202300003, '09123456783', 'Victor Napanis', 'victor_napanis', 'M', 2023, 'BS Computer Science', 'victor.napanis@example.com', 'pass789');

-- Organizations
INSERT INTO org (org_id, money_balance, type, name, year_established, username, password) VALUES
(1, 0.00, 'Academic', 'Alliance of Computer Science Students', 2010, 'acss_admin', 'acss_pass'),
(2, 0.00, 'Tech', 'Young Software Engineer Society', 2012, 'yses_admin', 'yses_pass');

-- Memberships
INSERT INTO joins (student_number, org_id, year, semester, committee, role, status) VALUES
(202300001, 1, '2023', 1, 'Events', 'Member', 'Active'),
(202300002, 2, '2023', 1, 'Finance', 'Member', 'Active'),
(202300003, 1, '2023', 1, 'Executive', 'Secretary', 'Active');

-- Fees
INSERT INTO fee (student_number, org_id, year, semester, due_date, date_of_payment, status, amount) VALUES
(202300001, 1, 2023, 1, '2023-08-15', NULL, 'Unpaid', 500.00),
(202300002, 2, 2023, 1, '2023-08-10', NULL, 'Unpaid', 400.00),
(202300003, 1, 2023, 1, '2023-08-15', NULL, 'Unpaid', 500.00);

-- Create views for user
CREATE VIEW user1_fees AS SELECT * FROM member WHERE student_number = 0;
CREATE VIEW user2_fees AS SELECT * FROM member WHERE student_number = 0;
CREATE VIEW user3_fees AS SELECT * FROM member WHERE student_number = 0;

-- Grant select permission to users
GRANT SELECT ON 127project.user1_fees TO 'user1';
GRANT SELECT ON 127project.user2_fees TO 'user2';
GRANT SELECT ON 127project.user3_fees TO 'user3';

-- General fee view
CREATE VIEW user_fees AS
SELECT 
    f.fee_id,
    o.name AS org_name,
    f.amount,
    f.status
FROM 
    fee f
JOIN 
    org o ON f.org_id = o.org_id;


-- Basic Queries ------------------------------------------------------------------------------------
-- Students and the orgs they joined
SELECT 
    m.name AS student_name,
    o.name AS organization
FROM 
    member m
JOIN 
    joins j ON m.student_number = j.student_number
JOIN 
    org o ON j.org_id = o.org_id;

-- Fee status summary per organization
SELECT 
    o.name AS organization,
    COUNT(*) AS total_members,
    SUM(CASE WHEN f.status = 'Paid' THEN 1 ELSE 0 END) AS paid_members
FROM 
    fee f
JOIN 
    org o ON f.org_id = o.org_id
GROUP BY 
    o.name;

-- Procedure to get all fees for a specific student
-- Trigger to auto-update org balance
DELIMITER //
CREATE TRIGGER trg_update_balance_after_payment
AFTER UPDATE ON fee
FOR EACH ROW
BEGIN
    IF NEW.status = 'Paid' AND OLD.status <> 'Paid' THEN
        UPDATE org
        SET money_balance = money_balance + NEW.amount
        WHERE org_id = NEW.org_id;
    END IF;
END;
//
DELIMITER ;

-- Procedure to mark fee as paid
DELIMITER //
CREATE PROCEDURE pay_fee(IN p_fee_id INT)
BEGIN
    UPDATE fee
    SET status = 'Paid', 
        date_of_payment = CURRENT_DATE()
    WHERE fee_id = p_fee_id;
END;
//
DELIMITER ;

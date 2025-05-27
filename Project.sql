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

DROP PROCEDURE IF EXISTS pay_fee;

DROP VIEW IF EXISTS user_fees;
DROP VIEW IF EXISTS user1_fees;
DROP VIEW IF EXISTS user2_fees;
DROP VIEW IF EXISTS user3_fees;


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
(202300003, '09123456783', 'Victor Napanis', 'victor_napanis', 'M', 2023, 'BS Computer Science', 'victor.napanis@example.com', 'pass789'),

(202300004, '09123456784', 'Alex Rivera', 'alex_riv', 'M', 2023, 'BS Computer Science', 'alex.r@example.com', 'pw1'),
(202300005, '09123456785', 'Bella Cruz', 'bella_crz', 'F', 2022, 'BS Statistics', 'bella.c@example.com', 'pw2'),
(202300006, '09123456786', 'Carlos Tan', 'carlos_tan', 'M', 2024, 'BS Computer Science', 'carlos.t@example.com', 'pw3'),
(202300007, '09123456787', 'Dana Chua', 'dana_chua', 'F', 2023, 'BS Info Systems', 'dana.c@example.com', 'pw4'),
(202300008, '09123456788', 'Enzo Lim', 'enzo_lim', 'M', 2022, 'BS Applied Math', 'enzo.l@example.com', 'pw5'),
(202300009, '09123456789', 'Faith Ong', 'faith_ong', 'F', 2023, 'BS Computer Science', 'faith.o@example.com', 'pw6'),
(202300010, '09123456790', 'Gio Santos', 'gio_santos', 'M', 2022, 'BS Info Tech', 'gio.s@example.com', 'pw7'),
(202300011, '09123456791', 'Hana Yu', 'hana_yu', 'F', 2021, 'BS Computer Science', 'hana.y@example.com', 'pw8'),
(202300012, '09123456792', 'Ivan dela Cruz', 'ivan_dc', 'M', 2024, 'BS Computer Science', 'ivan.dc@example.com', 'pw9'),
(202300013, '09123456793', 'Jade Ramos', 'jade_r', 'F', 2023, 'BS Info Systems', 'jade.r@example.com', 'pw10'),
(202300014, '09123456794', 'Kenji Lee', 'kenji_lee', 'M', 2023, 'BS Statistics', 'kenji.l@example.com', 'pw11'),
(202300015, '09123456795', 'Lana Kim', 'lana_kim', 'F', 2023, 'BS Info Tech', 'lana.k@example.com', 'pw12'),
(202300016, '09123456796', 'Mika Torres', 'mika_t', 'F', 2022, 'BS Math', 'mika.t@example.com', 'pw13'),
(202300017, '09123456797', 'Noah Lim', 'noah_lim', 'M', 2021, 'BS Computer Science', 'noah.l@example.com', 'pw14'),
(202300018, '09123456798', 'Olive Chan', 'olive_c', 'F', 2023, 'BS Info Systems', 'olive.c@example.com', 'pw15'),
(202300019, '09123456799', 'Paulo Reyes', 'paulo_r', 'M', 2023, 'BS Computer Science', 'paulo.r@example.com', 'pw16'),
(202300020, '09123456800', 'Quinn Gonzales', 'quinn_g', 'F', 2022, 'BS Info Tech', 'quinn.g@example.com', 'pw17'),
(202300021, '09123456801', 'Rico Morales', 'rico_m', 'M', 2024, 'BS Computer Science', 'rico.m@example.com', 'pw18'),
(202300022, '09123456802', 'Sasha Dizon', 'sasha_d', 'F', 2023, 'BS Statistics', 'sasha.d@example.com', 'pw19'),
(202300023, '09123456803', 'Toby Uy', 'toby_uy', 'M', 2023, 'BS Math', 'toby.u@example.com', 'pw20');


-- Organizations
INSERT INTO org (org_id, money_balance, type, name, year_established, username, password) VALUES
(1, 0.00, 'Academic', 'Alliance of Computer Science Students', 2010, 'acss_admin', 'acss_pass'),
(2, 0.00, 'Tech', 'Young Software Engineer Society', 2012, 'yses_admin', 'yses_pass');

-- Memberships
INSERT INTO joins (student_number, org_id, year, semester, committee, role, status) VALUES
(202300001, 1, '2023', 1, 'Events', 'Member', 'Active'),
(202300002, 2, '2023', 1, 'Finance', 'Member', 'Active'),
(202300003, 1, '2023', 1, 'Executive', 'Secretary', 'Active'),

(202300004, 1, '2023', 2, 'Docs', 'Member', 'Active'),
(202300005, 2, '2023', 2, 'Finance', 'Treasurer', 'Active'),
(202300006, 1, '2023', 2, 'Events', 'Head', 'Active'),
(202300007, 2, '2023', 1, 'Logistics', 'Member', 'Inactive'),
(202300008, 2, '2023', 1, 'Events', 'VP', 'Active'),
(202300009, 1, '2023', 2, 'Docs', 'Member', 'Inactive'),
(202300010, 1, '2023', 1, 'Exec', 'President', 'Active'),
(202300011, 2, '2023', 1, 'Events', 'Member', 'Active'),
(202300012, 1, '2023', 1, 'Marketing', 'Member', 'Active'),
(202300013, 2, '2023', 2, 'Marketing', 'PRO', 'Active'),
(202300014, 1, '2023', 2, 'Finance', 'Member', 'Active'),
(202300015, 2, '2023', 1, 'Events', 'Secretary', 'Active'),
(202300016, 2, '2023', 1, 'Exec', 'Member', 'Active'),
(202300017, 1, '2023', 1, 'Docs', 'VP', 'Active'),
(202300018, 2, '2023', 2, 'Logistics', 'Member', 'Inactive');

-- NOTE: 202300019 to 202300023 are NON-MEMBERS (no joins)

-- Fees
INSERT INTO fee (student_number, org_id, year, semester, due_date, date_of_payment, status, amount) VALUES
(202300001, 1, 2023, 1, '2023-08-15', NULL, 'Unpaid', 500.00),
(202300002, 2, 2023, 1, '2023-08-10', NULL, 'Unpaid', 400.00),
(202300003, 1, 2023, 1, '2023-08-15', NULL, 'Unpaid', 500.00),

(202300004, 1, 2023, 2, '2023-11-10', NULL, 'Unpaid', 500.00),
(202300005, 2, 2023, 2, '2023-11-10', '2023-11-15', 'Paid', 400.00),
(202300006, 1, 2023, 2, '2023-11-10', NULL, 'Unpaid', 500.00),
(202300007, 2, 2023, 1, '2023-08-15', '2023-08-20', 'Paid', 400.00),
(202300008, 2, 2023, 1, '2023-08-15', NULL, 'Unpaid', 400.00),
(202300009, 1, 2023, 2, '2023-11-10', '2023-11-12', 'Paid', 500.00),
(202300010, 1, 2023, 1, '2023-08-15', '2023-08-18', 'Paid', 500.00),
(202300011, 2, 2023, 1, '2023-08-10', NULL, 'Unpaid', 400.00),
(202300012, 1, 2023, 1, '2023-08-15', NULL, 'Unpaid', 500.00),
(202300013, 2, 2023, 2, '2023-11-10', NULL, 'Unpaid', 400.00),
(202300014, 1, 2023, 2, '2023-11-10', NULL, 'Unpaid', 500.00),
(202300015, 2, 2023, 1, '2023-08-10', '2023-08-11', 'Paid', 400.00),
(202300016, 2, 2023, 1, '2023-08-10', NULL, 'Unpaid', 400.00),
(202300017, 1, 2023, 1, '2023-08-15', NULL, 'Unpaid', 500.00),
(202300018, 2, 2023, 2, '2023-11-10', NULL, 'Unpaid', 400.00);

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

CREATE DATABASE IF NOT EXISTS hospital_bed_allocation;
USE hospital_bed_allocation;

-- =========================
-- 1. DEPARTMENTS TABLE
-- =========================
CREATE TABLE departments (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

INSERT INTO departments (name) VALUES
('Nephrology'),
('Neurology'),
('Cardiology');

-- =========================
-- 2. BEDS TABLE
-- =========================
CREATE TABLE beds (
    id INT NOT NULL AUTO_INCREMENT,
    department_id INT NOT NULL,
    bed_number INT NOT NULL,
    status ENUM('empty', 'occupied', 'maintenance') DEFAULT 'empty',
    PRIMARY KEY (id),
    UNIQUE KEY unique_bed (department_id, bed_number),
    FOREIGN KEY (department_id) REFERENCES departments(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO beds (department_id, bed_number)
SELECT 1, n FROM (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
) numbers;

INSERT INTO beds (department_id, bed_number)
SELECT 2, n FROM (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
) numbers;

INSERT INTO beds (department_id, bed_number)
SELECT 3, n FROM (
    SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10
    UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15
) numbers;

-- =========================
-- 3. PATIENTS TABLE
-- =========================
CREATE TABLE patients (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    age INT NOT NULL,
    disease VARCHAR(255),
    severity ENUM('Extreme', 'High', 'Moderate', 'Normal') NOT NULL,
    required_department_id INT NOT NULL,
    assigned_department_id INT DEFAULT NULL,
    is_shifted BOOLEAN DEFAULT FALSE,
    admitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'waiting', 'discharged') DEFAULT 'active',
    PRIMARY KEY (id),
    FOREIGN KEY (required_department_id) REFERENCES departments(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (assigned_department_id) REFERENCES departments(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- =========================
-- 4. WAITING LIST TABLE
-- =========================
CREATE TABLE waiting_list (
    id INT NOT NULL AUTO_INCREMENT,
    patient_id INT NOT NULL,
    department_id INT NOT NULL,
    priority ENUM('Extreme', 'High', 'Moderate', 'Normal') NOT NULL,
    queue_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- =========================
-- 5. ALLOCATIONS TABLE
-- =========================
CREATE TABLE allocations (
    id INT NOT NULL AUTO_INCREMENT,
    patient_id INT NOT NULL,
    bed_id INT NOT NULL,
    allocated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    discharged_at DATETIME DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (bed_id) REFERENCES beds(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
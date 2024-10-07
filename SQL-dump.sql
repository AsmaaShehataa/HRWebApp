-- Drop database if exists
DROP DATABASE IF EXISTS hr_db;

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS hr_db;
CREATE USER IF NOT EXISTS 'hr_user'@'localhost' IDENTIFIED BY 'hr_db_pwd';
GRANT ALL ON hr_db.* TO 'hr_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hr_user'@'localhost';
FLUSH PRIVILEGES;

-- Use database
USE `hr_db`;

-- Table structure for `employees`
DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees` (
  `id` VARCHAR(60) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` VARCHAR(128) NOT NULL,
  `email` VARCHAR(128) NOT NULL UNIQUE,
  `password` VARCHAR(128) NOT NULL,
  `phone` VARCHAR(128) NOT NULL,
  `department` VARCHAR(128) NOT NULL,
  `start_date` DATETIME NOT NULL,
  `salary` VARCHAR(128) NOT NULL,
  `role` TINYINT DEFAULT 0 COMMENT '0 -> Employee, 1 -> Admin',
  `photo` VARCHAR(250),
  `deleted_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for `admins`
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `admin_id` VARCHAR(60) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `email` VARCHAR(128) NOT NULL UNIQUE,
  `password` VARCHAR(128) NOT NULL,
  `role` TINYINT DEFAULT 1 NOT NULL,
  PRIMARY KEY (`admin_id`),
  FOREIGN KEY (`admin_id`) REFERENCES `employees`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for `settings`
DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings` (
  `key` VARCHAR(128) NOT NULL UNIQUE,
  `value` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for `leave_requests`
DROP TABLE IF EXISTS `leave_requests`;
CREATE TABLE `leave_requests` (
  `leave_id` VARCHAR(60) NOT NULL,
  `employee_id` VARCHAR(60) NOT NULL,
  `from_date` DATETIME NOT NULL,
  `to_date` DATETIME NOT NULL,
  `reason` TEXT NOT NULL,
  `status` TINYINT DEFAULT 0 COMMENT '0 -> Pending, 1 -> Approved, 2 -> Rejected',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`leave_id`),
  FOREIGN KEY (`employee_id`) REFERENCES `employees`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- table structure for `attendance`
DROP TABLE IF EXISTS `attendance`;
CREATE TABLE `attendance` (
  `attendance_id` VARCHAR(60) NOT NULL,
  `employee_id` VARCHAR(60) NOT NULL,
  `date` DATE NOT NULL,
  `status` TINYINT DEFAULT 0 COMMENT '0 -> Absent, 1 -> Present',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`attendance_id`),
  FOREIGN KEY (`employee_id`) REFERENCES `employees`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



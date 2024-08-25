-- Drop database if exists
DROP DATABASE IF EXISTS `hr_db`;

-- Create db if not exists
CREATE DATABASE IF NOT EXISTS `hr_db`;
CREATE USER IF NOT EXISTS 'hr_user'@'localhost' IDENTIFIED BY 'hr_db_pwd';
GRANT ALL ON hr_db.* TO 'hr_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hr_user'@'localhost';
FLUSH PRIVILEGES;

-- Use db
USE `hr_db`;

-- Table structure for `employees`
DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL UNIQUE,
  `password` varchar(128) NOT NULL,
  `phone` varchar(128) NOT NULL,
  `department` varchar(128) NOT NULL,
  `start_date` datetime NOT NULL,
  `salary` varchar(128) NOT NULL,
  `role` TINYINT DEFAULT 0 COMMENT '0 -> Employee, 1 -> Admin',
  `photo` varchar(250),
  `deleted_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for `admins`
DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
  `admin_id` varchar(60) NOT NULL,
  `name` varchar(128) NOT NULL,
  `email` varchar(128) NOT NULL UNIQUE,
  `password` varchar(128) NOT NULL,
  `role` TINYINT DEFAULT 1 NOT NULL,
  PRIMARY KEY (`admin_id`),
  FOREIGN KEY (`admin_id`) REFERENCES `employees`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for `settings`
DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings` (
  `key` varchar(128) NOT NULL UNIQUE,
  `value` varchar(128) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Example insert into `employees`
INSERT INTO `employees` (id, name, email, password, phone, department, start_date, salary, role) 
VALUES ('1', 'Employee', 'employee@example.com', '1234', '1234567890', 'Software Engineer', '2024-08-01 00:00:00', '50000', 0);

-- Example insert into `admins`
INSERT INTO `admins` (admin_id, name, email, password, role) 
VALUES ('1', 'Admin', 'admin@example.com', '12345', 1);

-- Example insert into `settings`
INSERT INTO `settings` (key, value) 
VALUES ('notification', 'sms');

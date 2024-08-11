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

-- Table structure for `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `name` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL UNIQUE,
  `password` varchar(250) NOT NULL,
  `phone` varchar(250) NOT NULL,
  `department` varchar(250) NOT NULL,
  `start_date` datetime NOT NULL,
  `salary` varchar(250) NOT NULL,
  `role` TINYINT DEFAULT 0 COMMENT '0 -> User, 1 -> Admin',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Example insert (you can fill in the details)
INSERT INTO `users` (id, name, email, password, phone, department, start_date, salary, role) 
VALUES ('1', 'Admin', 'admin@example.com', '1234', '1234567890', 'HR', '2024-08-01 00:00:00', '50000', 1);

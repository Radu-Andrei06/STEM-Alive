-- MySQL setup for Login System
CREATE DATABASE IF NOT EXISTS auth_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE auth_system;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create application user
CREATE USER IF NOT EXISTS 'auth_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Auth@1234';
GRANT ALL PRIVILEGES ON auth_system.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;

-- Test user (password: Test@1234)
INSERT IGNORE INTO users (username, email, password) VALUES 
('testuser', 'test@example.com', '\\\.MQRqQz6Y3hN5oW3OQnO7O0XQYfX1J1K');

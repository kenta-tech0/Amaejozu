-- Database initialization script
-- This file is executed when the MySQL container is first created

-- Create database if not exists (usually created by MYSQL_DATABASE env var)
CREATE DATABASE IF NOT EXISTS cosmetics_price_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE cosmetics_price_db;

-- Set timezone
SET time_zone = '+09:00';

-- Grant privileges (usually handled by docker-compose environment variables)
-- GRANT ALL PRIVILEGES ON cosmetics_price_db.* TO 'app_user'@'%';
-- FLUSH PRIVILEGES;

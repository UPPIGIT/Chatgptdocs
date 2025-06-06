-- Step 1: Drop the database if exists
DROP DATABASE IF EXISTS sprintmaster_db;

-- Step 2: Create a fresh database
CREATE DATABASE sprintmaster_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Step 3: Use the new database
USE sprintmaster_db;

-- Step 4: Create USERS table
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(150) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(150) NOT NULL,
    role ENUM('USER', 'LEAD', 'ADMIN') NOT NULL DEFAULT 'USER',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 5: Create SPRINTS table
CREATE TABLE sprints (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 6: Create TASKS table
CREATE TABLE tasks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    story_id VARCHAR(50) NOT NULL,
    description TEXT,
    status ENUM('TO_DO', 'IN_PROGRESS', 'IN_QA', 'COMPLETED', 'BLOCKED') DEFAULT 'TO_DO',
    story_type ENUM('BUG', 'FEATURE', 'SPIKE', 'TASK') NOT NULL,
    dev_date DATE,
    qa_date DATE,
    prod_date DATE,
    blockers TEXT,
    lead_comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Foreign Keys
    sprint_id BIGINT,
    owner_id BIGINT,

    CONSTRAINT fk_task_sprint FOREIGN KEY (sprint_id) REFERENCES sprints(id) ON DELETE CASCADE,
    CONSTRAINT fk_task_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

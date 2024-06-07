-- Drop existing tables
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS Expenses CASCADE;
DROP TABLE IF EXISTS Debts CASCADE;
DROP TABLE IF EXISTS Friends CASCADE;



-- Create Users Table
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    session_key VARCHAR(255) UNIQUE,
    profile_pic VARCHAR(255)
);

-- Create Expenses Table
CREATE TABLE Expenses (
    ExpenseID SERIAL PRIMARY KEY,
    PayerID INT REFERENCES "user"(user_id),
    Amount DECIMAL(10, 2) NOT NULL,
    Description VARCHAR(255),
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Debt Table to track who owes what to whom
CREATE TABLE Debts (
    DebtID SERIAL PRIMARY KEY,
    ExpenseID INT REFERENCES Expenses(ExpenseID),
    OwedToUserID INT REFERENCES "user"(user_id),
    OwedByUserID INT REFERENCES "user"(user_id),
    AmountOwed DECIMAL(10, 2) NOT NULL
);

-- Create Friends Table
CREATE TABLE Friends (
    FriendID SERIAL PRIMARY KEY,
    UserID INT REFERENCES "user"(user_id) ON DELETE CASCADE,
    FriendUserID INT REFERENCES "user"(user_id) ON DELETE CASCADE,
    Status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'accepted', 'rejected'
    LastUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Rahul', 'Sharma', 'rahul', '$2b$12$YAHoV9QGxM8T/.ArdKjLTeG/5o/MLkVig.6FHXUmILpbYO2tJO8tK', 'rahul.sharma@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Anjali', 'Verma', 'anjali.verma', 'Password123!', 'anjali.verma@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Vikram', 'Singh', 'vikram.singh', 'SecurePass!1', 'vikram.singh@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Priya', 'Nair', 'priya.nair', 'MyPass123!', 'priya.nair@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Amit', 'Patel', 'amit.patel', 'PassWord!123', 'amit.patel@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Sneha', 'Kumar', 'sneha.kumar', 'SuperPass!1', 'sneha.kumar@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Rohan', 'Mehta', 'rohan.mehta', 'UltraPass!123', 'rohan.mehta@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Kavita', 'Desai', 'kavita.desai', 'MegaPass!1', 'kavita.desai@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Arjun', 'Joshi', 'arjun.joshi', 'TopPass!123', 'arjun.joshi@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('Nidhi', 'Rao', 'nidhi.rao', 'BestPass!1', 'nidhi.rao@example.com', NULL ,NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic) VALUES ('12', '12', '12', '$2b$12$YAHoV9QGxM8T/.ArdKjLTeG/5o/MLkVig.6FHXUmILpbYO2tJO8tK', '12@12', NULL ,NULL);

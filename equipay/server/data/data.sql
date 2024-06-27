-- Drop existing tables
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS Expenses CASCADE;
DROP TABLE IF EXISTS Debts CASCADE;
DROP TABLE IF EXISTS Friends CASCADE;
DROP TABLE IF EXISTS Groups CASCADE;
DROP TABLE IF EXISTS GroupMembers CASCADE;
DROP TABLE IF EXISTS GroupExpenses CASCADE;
DROP TABLE IF EXISTS GroupDebts CASCADE;
DROP TABLE IF EXISTS ActivityLog CASCADE;

-- Create Users Table
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    session_key VARCHAR(255) UNIQUE,
    profile_pic VARCHAR(255),
    contact_number VARCHAR(20)
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

-- Create Groups Table
CREATE TABLE Groups (
    GroupID SERIAL PRIMARY KEY,
    GroupName VARCHAR(255) NOT NULL,
    CreatedBy INT REFERENCES "user"(user_id),
    profile_picture VARCHAR(255) DEFAULT NULL
);

-- Create GroupMembers Table
CREATE TABLE GroupMembers (
    MemberID SERIAL PRIMARY KEY,
    GroupID INT REFERENCES Groups(GroupID) ON DELETE CASCADE,
    UserID INT REFERENCES "user"(user_id) ON DELETE CASCADE,
    IsAdmin BOOLEAN DEFAULT FALSE
);

-- Create GroupExpenses Table
CREATE TABLE GroupExpenses (
    ExpenseID SERIAL PRIMARY KEY,
    GroupID INT REFERENCES Groups(GroupID) ON DELETE CASCADE,
    PayerID INT REFERENCES "user"(user_id),
    Amount DECIMAL(10, 2) NOT NULL,
    Description VARCHAR(255),
    Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create GroupDebts Table
CREATE TABLE GroupDebts (
    DebtID SERIAL PRIMARY KEY,
    ExpenseID INT REFERENCES GroupExpenses(ExpenseID),
    OwedToUserID INT REFERENCES "user"(user_id),
    OwedByUserID INT REFERENCES "user"(user_id),
    AmountOwed DECIMAL(10, 2) NOT NULL
);

CREATE TABLE ActivityLog (
    LogID SERIAL PRIMARY KEY,
    UserID INT REFERENCES "user"(user_id),
    ActionType VARCHAR(255) NOT NULL,
    Details VARCHAR(255),
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Rahul', 'Sharma', 'rahul', '$2b$12$YAHoV9QGxM8T/.ArdKjLTeG/5o/MLkVig.6FHXUmILpbYO2tJO8tK', 'rahul.sharma@example.com', NULL ,NULL,'+15859575220');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Anjali', 'Verma', 'anjali.verma', 'Password123!', 'anjali.verma@example.com', NULL ,NULL,'+15859575221');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Vikram', 'Singh', 'vikram.singh', 'SecurePass!1', 'vikram.singh@example.com', NULL ,NULL,'+15859575222');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Priya', 'Nair', 'priya.nair', 'MyPass123!', 'priya.nair@example.com', NULL ,NULL,'+15859575223');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Amit', 'Patel', 'amit.patel', 'PassWord!123', 'amit.patel@example.com', NULL ,NULL,'+15859575224');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Sneha', 'Kumar', 'sneha.kumar', 'SuperPass!1', 'sneha.kumar@example.com', NULL ,NULL,'+15859575225');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Rohan', 'Mehta', 'rohan.mehta', 'UltraPass!123', 'rohan.mehta@example.com', NULL ,NULL,'+15859575226');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Kavita', 'Desai', 'kavita.desai', 'MegaPass!1', 'kavita.desai@example.com', NULL ,NULL,'+15859575227');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Arjun', 'Joshi', 'arjun.joshi', 'TopPass!123', 'arjun.joshi@example.com', NULL ,NULL,'+15859575228');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('Nidhi', 'Rao', 'nidhi.rao', 'BestPass!1', 'nidhi.rao@example.com', NULL ,NULL,'+15859575229');
INSERT INTO "user" (firstname, lastname, username, password, email, session_key,profile_pic,contact_number) VALUES ('12', '12', '12', '$2b$12$YAHoV9QGxM8T/.ArdKjLTeG/5o/MLkVig.6FHXUmILpbYO2tJO8tK', '12@12', NULL ,NULL,'+918980387432');


INSERT INTO Friends (UserID, FriendUserID, Status) VALUES ('1', '11', 'accepted');
INSERT INTO Friends (UserID, FriendUserID, Status) VALUES ('2', '11', 'accepted');
INSERT INTO Friends (UserID, FriendUserID, Status) VALUES ('3', '11', 'accepted');

-- First, insert a group
INSERT INTO Groups (GroupName, CreatedBy)
VALUES ('Utility Group', 11);  -- Assuming 'CreatedBy' user_id '11' exists

-- Insert Expenses for May and June
INSERT INTO Expenses (PayerID, Amount, Description, Date)
VALUES
(11, 500.00, 'May Utilities', '2023-05-15'),
(11, 600.00, 'June Utilities', '2023-06-15');

-- Insert corresponding Debts assuming ExpenseID 1 for May and 2 for June
INSERT INTO Debts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed)
VALUES
(1, 11, 1, 166.67),
(1, 11, 2, 166.67),
(1, 11, 3, 166.67),
(2, 11, 1, 200.00),
(2, 11, 2, 200.00),
(2, 11, 3, 200.00);

-- Assuming GroupID 1 has been inserted
-- Insert GroupExpenses for May and June for the created group
INSERT INTO GroupExpenses (GroupID, PayerID, Amount, Description, Date)
VALUES
(1, 11, 500.00, 'May Group Utilities', '2023-05-15'),
(1, 11, 600.00, 'June Group Utilities', '2023-06-15');

-- Assuming ExpenseID 1 and 2 for GroupExpenses as before
-- Insert corresponding GroupDebts
INSERT INTO GroupDebts (ExpenseID, OwedToUserID, OwedByUserID, AmountOwed)
VALUES
(1, 11, 1, 166.67),
(1, 11, 2, 166.67),
(1, 11, 3, 166.67),
(2, 11, 1, 200.00),
(2, 11, 2, 200.00),
(2, 11, 3, 200.00);

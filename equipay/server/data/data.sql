-- Drop tables if they exist
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS Expenses CASCADE;
DROP TABLE IF EXISTS Individuals CASCADE;
DROP TABLE IF EXISTS Groups CASCADE;
DROP TABLE IF EXISTS GroupMembers CASCADE;
DROP TABLE IF EXISTS ExpenseParticipants CASCADE;

-- Groups Table
CREATE TABLE Groups (
    GroupID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Type VARCHAR(255),
    Picture BYTEA
);

-- Users Table
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    session_key VARCHAR(255) UNIQUE
);

-- Expenses Table
CREATE TABLE Expenses (
    ExpenseID SERIAL PRIMARY KEY,
    Date TIMESTAMP NOT NULL,
    Note VARCHAR(255),
    Price DECIMAL(10, 2) NOT NULL,
    Description VARCHAR(255),
    GroupID INT REFERENCES Groups(GroupID)
);

-- Individuals Table
CREATE TABLE Individuals (
    PersonID SERIAL PRIMARY KEY,
    PersonName VARCHAR(255) NOT NULL
);

-- Group Members Table
CREATE TABLE GroupMembers (
    GroupID INT REFERENCES Groups(GroupID),
    PersonID INT REFERENCES Individuals(PersonID),
    PRIMARY KEY (GroupID, PersonID)
);

-- Expense Participants Table
CREATE TABLE ExpenseParticipants (
    ExpenseID INT REFERENCES Expenses(ExpenseID),
    PersonID INT REFERENCES Individuals(PersonID),
    Amount DECIMAL(10, 2),
    PRIMARY KEY (ExpenseID, PersonID)
);

INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Rahul', 'Sharma', 'rahul.sharma', 'Qwerty123!', 'rahul.sharma@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Anjali', 'Verma', 'anjali.verma', 'Password123!', 'anjali.verma@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Vikram', 'Singh', 'vikram.singh', 'SecurePass!1', 'vikram.singh@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Priya', 'Nair', 'priya.nair', 'MyPass123!', 'priya.nair@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Amit', 'Patel', 'amit.patel', 'PassWord!123', 'amit.patel@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Sneha', 'Kumar', 'sneha.kumar', 'SuperPass!1', 'sneha.kumar@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Rohan', 'Mehta', 'rohan.mehta', 'UltraPass!123', 'rohan.mehta@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Kavita', 'Desai', 'kavita.desai', 'MegaPass!1', 'kavita.desai@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Arjun', 'Joshi', 'arjun.joshi', 'TopPass!123', 'arjun.joshi@example.com', NULL);
INSERT INTO "user" (firstname, lastname, username, password, email, session_key) VALUES ('Nidhi', 'Rao', 'nidhi.rao', 'BestPass!1', 'nidhi.rao@example.com', NULL);


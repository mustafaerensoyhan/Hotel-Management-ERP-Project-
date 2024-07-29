CREATE DATABASE HotelManagement;
USE HotelManagement;

CREATE TABLE Users (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(100) NOT NULL,
    PhoneUserIDPasswordUsername VARCHAR(20) NOT NULL,
    Role ENUM('Staff', 'Admin', 'Guest') NOT NULL,
    UNIQUE (Username),
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE RoomCategories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY AUTO_INCREMENT,
    RoomNumber VARCHAR(10) NOT NULL,
    CategoryID INT,
    Status ENUM('Occupied', 'Available', 'Under Maintenance', 'Reserved') NOT NULL,
    Features TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoryID) REFERENCES RoomCategories(CategoryID) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX (CategoryID)
);

CREATE TABLE GroupReservations (
    GroupReservationID INT PRIMARY KEY AUTO_INCREMENT,
    ReservationDetails TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    RoomID INT,
    CheckInDate DATETIME NOT NULL,
    CheckOutDate DATETIME NOT NULL,
    Status ENUM('Confirmed', 'Cancelled', 'Pending') NOT NULL,
    GroupReservationID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (GroupReservationID) REFERENCES GroupReservations(GroupReservationID) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX (UserID),
    INDEX (RoomID),
    INDEX (GroupReservationID)
);

CREATE TABLE Billing (
    BillID INT PRIMARY KEY AUTO_INCREMENT,
    ReservationID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    Date DATETIME NOT NULL,
    PaymentStatus ENUM('Pending', 'Paid') NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (ReservationID)
);

CREATE TABLE Payments (
    PaymentID INT PRIMARY KEY AUTO_INCREMENT,
    BillID INT,
    PaymentMethod ENUM('Credit Card', 'Debit Card', 'Online Payment', 'Mobile Wallet', 'Cash') NOT NULL,
    PaymentDate DATETIME NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (BillID) REFERENCES Billing(BillID) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (BillID)
);

CREATE TABLE Staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Role VARCHAR(50),
    ShiftStart TIME,
    ShiftEnd TIME,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    SupplierName VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    ContactDetails TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Supplies (
    SupplyID INT PRIMARY KEY AUTO_INCREMENT,
    ItemName VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Quantity INT NOT NULL,
    SupplierID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX (SupplierID)
);

CREATE TABLE MaintenanceRequests (
    RequestID INT PRIMARY KEY AUTO_INCREMENT,
    RoomID INT,
    Description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    RequestDate DATE NOT NULL,
    Status ENUM('Pending', 'In Progress', 'Completed', 'Cancelled') NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (RoomID)
);

CREATE TABLE Reports (
    ReportID INT PRIMARY KEY AUTO_INCREMENT,
    ReportType VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    GeneratedDate DATE NOT NULL,
    Details TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Notifications (
    NotificationID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Message TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    Date DATE NOT NULL,
    Type ENUM('System Alert', 'Guest Notification', 'Payment Reminder') NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (UserID)
);

CREATE TABLE Guests (
    GuestID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    ContactDetails TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Preferences TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE HousekeepingTasks (
    TaskID INT PRIMARY KEY AUTO_INCREMENT,
    RoomID INT,
    AssignedTo INT,
    TaskDetails TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Status ENUM('Pending', 'In Progress', 'Completed', 'Delayed') NOT NULL,
    AssignedDate DATE NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (AssignedTo) REFERENCES Staff(StaffID) ON DELETE SET NULL ON UPDATE CASCADE,
    INDEX (RoomID),
    INDEX (AssignedTo)
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY AUTO_INCREMENT,
    EventName VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    EventDate DATE NOT NULL,
    EventDetails TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    ReservationID INT,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ModifiedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ReservationID) REFERENCES Reservations(ReservationID) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (ReservationID)
);

CREATE TABLE UserActivityLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    Activity VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    ActivityType ENUM('Login', 'Logout', 'Data Access', 'Data Modification') NOT NULL,
    Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    INDEX (UserID)
);


-- Insert into Users
INSERT INTO Users (UserID, Username, Password, Email, Phone, Role) VALUES
(1, 'john_doe', 'password123', 'john_doe@example.com', '1234567890', 'Staff'),
(2, 'jane_smith', 'password456', 'jane_smith@example.com', '1234567891', 'Staff'),
(3, 'michael_scott', 'bestboss', 'michael_scott@example.com', '1234567892', 'Admin'),
(4, 'pam_beesly', 'password321', 'pam_beesly@example.com', '1234567893', 'Staff'),
(5, 'jim_halpert', 'password654', 'jim_halpert@example.com', '1234567894', 'Staff'),
(6, 'guest1', 'password5', 'user5@example.com', '1234567895', 'Guest'),
(7, 'guest2', 'password6', 'user6@example.com', '1234567896', 'Guest'),
(8, 'guest3', 'password7', 'user7@example.com', '1234567897', 'Guest'),
(9, 'guest4', 'password8', 'user8@example.com', '1234567898', 'Guest'),
(10, 'guest5', 'password9', 'user9@example.com', '1234567899', 'Guest'),
(11, 'guest6', 'password4', 'user4@example.com', '1234560895', 'Guest'),
(12, 'guest7', 'password3', 'user3@example.com', '1234568896', 'Guest'),
(13, 'guest8', 'password2', 'user2@example.com', '1234561897', 'Guest'),
(14, 'guest9', 'password1', 'user1@example.com', '1234563898', 'Guest'),
(15, 'guest10', 'password0', 'user90@example.com', '1234267899', 'Guest');

-- Insert into RoomCategories
INSERT INTO RoomCategories (CategoryName, Description) VALUES
('Single', 'Single room with a single bed'),
('Double', 'Double room with a double bed'),
('Suite', 'Suite with multiple rooms'),
('Conference Room', 'Room equipped for conferences and meetings');

-- Insert into Rooms
INSERT INTO Rooms (RoomID, RoomNumber, CategoryID, Status, Features) VALUES
(1, '101', 1, 'Available', 'Wi-Fi, TV, AC'),
(2, '102', 1, 'Available', 'Wi-Fi, TV, AC'),
(3, '103', 2, 'Available', 'Wi-Fi, TV, AC, Mini Bar'),
(4, '104', 2, 'Available', 'Wi-Fi, TV, AC, Mini Bar'),
(5, '201', 3, 'Under Maintenance', 'Wi-Fi, TV, AC, Kitchen'),
(6, '202', 3, 'Available', 'Wi-Fi, TV, AC, Kitchen'),
(7, '301', 4, 'Available', 'Projector, Wi-Fi, Whiteboard'),
(8, '302', 4, 'Available', 'Projector, Wi-Fi, Whiteboard');

-- Insert data into GroupReservations with GroupReservationID
INSERT INTO GroupReservations (GroupReservationID, ReservationDetails)
VALUES 
(1, 'Group booking for a corporate event. Includes 10 rooms. Special requests: projectors in conference rooms, vegan meal options.'),
(2, 'Wedding party booking. Includes 15 rooms. Special requests: bridal suite decoration, gluten-free meal options.'),
(3, 'Family reunion. Includes 5 rooms. Special requests: adjacent rooms, extra beds in two rooms.'),
(4, 'School trip. Includes 20 rooms. Special requests: early check-in, breakfast included for all students.'),
(5, 'Conference attendees. Includes 8 rooms. Special requests: late check-out, high-speed internet access.');

-- Insert data into Reservations
INSERT INTO Reservations (ReservationID, UserID, RoomID, CheckInDate, CheckOutDate, Status, GroupReservationID)
VALUES
(1, 6, 1, '2024-08-01 14:00:00', '2024-08-10 12:00:00', 'Confirmed', 1),
(2, 7, 2, '2024-08-01 14:00:00', '2024-08-10 12:00:00', 'Confirmed', 1),
(3, 8, 3, '2024-08-01 14:00:00', '2024-08-10 12:00:00', 'Confirmed', 1),
(4, 9, 4, '2024-08-01 14:00:00', '2024-08-10 12:00:00', 'Confirmed', 1),
(5, 10, 5, '2024-08-01 14:00:00', '2024-08-10 12:00:00', 'Confirmed', 1),
(6, 11, 6, '2024-09-15 15:00:00', '2024-09-20 11:00:00', 'Pending', 2),
(7, 12, 7, '2024-09-15 15:00:00', '2024-09-20 11:00:00', 'Pending', 2),
(8, 13, 8, '2024-09-15 15:00:00', '2024-09-20 11:00:00', 'Pending', 2),
(9, 14, 1, '2024-09-15 15:00:00', '2024-09-20 11:00:00', 'Pending', 2),
(10, 15, 2, '2024-09-15 15:00:00', '2024-09-20 11:00:00', 'Cancelled', 2);

-- Insert into Billing with specific dates
INSERT INTO Billing (BillID, ReservationID, Amount, Date, PaymentStatus, CreatedAt) VALUES
(1, 1, 150.00, '2024-07-01 10:00:00', 'Pending', NOW()),
(2, 2, 300.00, '2024-07-02 11:00:00', 'Paid', NOW()),
(3, 3, 500.00, '2024-07-03 12:00:00', 'Pending', NOW()),
(4, 4, 500.00, '2024-07-04 13:00:00', 'Pending', NOW());

-- Insert into Payments
INSERT INTO Payments (PaymentID, BillID, PaymentMethod, PaymentDate, Amount, CreatedAt) VALUES
(1, 2, 'Credit Card', NOW(), 300.00, NOW());

-- Insert into Staff with StaffID
INSERT INTO Staff (StaffID, Name, Role, ShiftStart, ShiftEnd, CreatedAt) VALUES
(1, 'Alice Johnson', 'Receptionist', '08:00:00', '16:00:00', NOW()),
(2, 'Bob Williams', 'Cleaner', '09:00:00', '17:00:00', NOW()),
(3, 'Jim Halpert', 'Sales', '09:00:00', '17:00:00', NOW()),
(4, 'Dwight Schrute', 'Assistant to the Regional Manager', '08:00:00', '16:00:00', NOW());

-- Insert into Suppliers
INSERT INTO Suppliers (SupplierName, ContactDetails, CreatedAt) VALUES
('Hotel Supplies Co.', '123-456-7890, supply@hotel.com', NOW()),
('Luxury Linens Inc.', '987-654-3210, sales@luxury.com', NOW());

-- Insert into Supplies
INSERT INTO Supplies (ItemName, Quantity, SupplierID, CreatedAt) VALUES
('Towels', 100, 1, NOW()),
('Bedding', 50, 2, NOW()),
('Conference Chairs', 30, 1, NOW()),
('Projector Screens', 5, 2, NOW());

-- Insert into MaintenanceRequests
INSERT INTO MaintenanceRequests (RoomID, Description, RequestDate, Status, CreatedAt) VALUES
(3, 'Fix the air conditioning', '2024-07-05', 'Pending', NOW()),
(1, 'Replace light bulb', '2024-07-06', 'Completed', NOW());

-- Insert into Reports
INSERT INTO Reports (ReportType, GeneratedDate, Details, CreatedAt) VALUES
('Occupancy', '2024-07-01', 'Monthly occupancy report', NOW()),
('Financial', '2024-07-01', 'Monthly financial report', NOW());

-- Insert into Notifications
INSERT INTO Notifications (NotificationID, UserID, Message, Date, Type, CreatedAt) VALUES
(1, 6, 'Your reservation is confirmed', '2024-07-05', 'Guest Notification', NOW()),
(2, 7, 'Your payment is successful', '2024-07-05', 'Payment Reminder', NOW()),
(3, 3, 'Best Boss Ever', '2024-07-05', 'System Alert', NOW());

-- Insert data into the UserActivityLog table
INSERT INTO UserActivityLog (UserID, Activity, ActivityType, Timestamp)
VALUES 
(1, 'User logged in', 'Login', '2024-07-15 08:30:00'),
(2, 'User logged out', 'Logout', '2024-07-15 09:00:00'),
(3, 'User accessed customer data', 'Data Access', '2024-07-15 10:00:00'),
(1, 'User modified product information', 'Data Modification', '2024-07-15 11:00:00'),
(2, 'User logged in', 'Login', '2024-07-16 08:30:00'),
(3, 'User accessed order details', 'Data Access', '2024-07-16 09:15:00'),
(1, 'User logged out', 'Logout', '2024-07-16 10:45:00'),
(3, 'User modified customer data', 'Data Modification', '2024-07-16 11:30:00'),
(2, 'User logged in', 'Login', '2024-07-17 08:30:00'),
(1, 'User accessed supplier data', 'Data Access', '2024-07-17 09:00:00');


-- Insert into Guests
INSERT INTO Guests (Name, ContactDetails, Preferences, CreatedAt) VALUES
('Charlie Brown', 'charlie.brown@example.com, 555-1234', 'No smoking room', NOW()),
('Lucy Van Pelt', 'lucy.vanpelt@example.com, 555-5678', 'Close to elevator', NOW());

-- Insert into HousekeepingTasks
INSERT INTO HousekeepingTasks (RoomID, AssignedTo, TaskDetails, Status, AssignedDate, CreatedAt) VALUES
(1, 2, 'Clean the room', 'Pending', '2024-07-06', NOW()),
(2, 2, 'Restock minibar', 'In Progress', '2024-07-06', NOW());

-- Insert into Events
INSERT INTO Events (EventID, EventName, EventDate, EventDetails, ReservationID, CreatedAt) VALUES
(1, 'Wedding Reception', '2024-08-15', 'Wedding reception for 100 guests', 2, NOW()),
(2, 'Business Conference', '2024-09-01', 'Conference for 50 attendees', 3, NOW());

-- Select all users
SELECT * FROM Users;

-- Select all rooms and their categories
SELECT Rooms.RoomNumber, RoomCategories.CategoryName
FROM Rooms
JOIN RoomCategories ON Rooms.CategoryID = RoomCategories.CategoryID;

-- Select all reservations
SELECT * FROM Reservations;

-- Select all staff members
SELECT * FROM Staff;

-- Select all supplies and their suppliers
SELECT Supplies.ItemName, Suppliers.SupplierName
FROM Supplies
JOIN Suppliers ON Supplies.SupplierID = Suppliers.SupplierID;

-- Select all maintenance requests
SELECT * FROM MaintenanceRequests;

-- Select all events
SELECT * FROM Events;

-- Select all reports
SELECT * FROM Reports;

-- Select all notification
SELECT * FROM Notifications;

-- Select all notification
SELECT * FROM UserActivityLog;

-- Select all billing records
SELECT * FROM Billing;

-- Select all payments
SELECT * FROM Payments;

-- Select all guests
SELECT * FROM Guests;

-- Select all housekeeping tasks
SELECT * FROM HousekeepingTasks;

DELETE FROM Notifications;
DELETE FROM Payments;
DELETE FROM Billing;
DELETE FROM Reservations;
DELETE FROM HousekeepingTasks;
DELETE FROM Events;
DELETE FROM MaintenanceRequests;
DELETE FROM Supplies;
DELETE FROM GroupReservations;
DELETE FROM Guests;
DELETE FROM Rooms;
DELETE FROM RoomCategories;
DELETE FROM Users;
DELETE FROM Staff;
DELETE FROM Suppliers;
DELETE FROM UserActivityLog;

SET FOREIGN_KEY_CHECKS = 0;


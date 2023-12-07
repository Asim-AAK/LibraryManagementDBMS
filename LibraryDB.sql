-- Creating the Students table
CREATE TABLE Students (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255),
    fine FLOAT,
    access BOOLEAN
);

-- Creating the Books table
CREATE TABLE Books (
    bookid INT PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Genre VARCHAR(255),
    Copies_Available INT,
    fine_amount_per_day FLOAT
);

-- Creating the Admin table
CREATE TABLE Admin (
    email VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    password VARCHAR(255)
);

-- Creating the Hold table
CREATE TABLE Hold (
    hold_id INT PRIMARY KEY,
    Student_email VARCHAR(255),
    Admin_email VARCHAR(255),
    holdDate DATE,
    FOREIGN KEY (Student_email) REFERENCES Students(email),
    FOREIGN KEY (Admin_email) REFERENCES Admin(email)
);

-- Creating the Featured_Book table
CREATE TABLE Featured_Book (
    featured_book_id INT PRIMARY KEY,
    book_title_pageImages STRING
);

-- Creating the book_issued table
CREATE TABLE book_issued (
    Student_email VARCHAR(255),
    BookID INT,
    Returned BOOLEAN,
    ReturnDate DATE,
    issue_date DATETIME,
    FOREIGN KEY (Student_email) REFERENCES Students(email),
    FOREIGN KEY (BookID) REFERENCES Books(bookid)
);

-- Creating the rooms table
CREATE TABLE rooms (
    roomid INT PRIMARY KEY,
    Room_number INT,
    capacity INT,
    availability BOOLEAN
);

-- Creating the room_issued table
CREATE TABLE room_issued (
    Student_email VARCHAR(255),
    roomID INT,
    reserved_date DATE,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (Student_email) REFERENCES Students(email),
    FOREIGN KEY (roomID) REFERENCES rooms(roomid)
);





/*-- Inserting sample data into Students table
INSERT INTO Students (email, name, password, fine, access) VALUES
('john.doe@example.com', 'John Doe', 'password123', 0.0, 1),
('jane.smith@example.com', 'Jane Smith', 'password123', 0.0, 1),
('alice.johnson@example.com', 'Alice Johnson', 'password123', 5.0, 1),
('mike.brown@example.com', 'Mike Brown', 'password123', 2.5, 0),
('emma.wilson@example.com', 'Emma Wilson', 'password123', 0.0, 0);

-- Inserting sample data into Books table
INSERT INTO Books (bookid, Title, Author, Genre, Copies_Available, fine_amount_per_day) VALUES
(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 'Novel', 5, 0.50),
(2, '1984', 'George Orwell', 'Dystopian', 3, 0.50),
(3, 'To Kill a Mockingbird', 'Harper Lee', 'Fiction', 4, 0.50),
(4, 'The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 2, 0.50),
(5, 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 3, 0.50);

-- Inserting sample data into Admin table
INSERT INTO Admin (email, name, password) VALUES
('admin@example.com', 'Admin One', 'adminpass1');

-- Inserting sample data into Hold table
INSERT INTO Hold (hold_id, Student_email, Admin_email, holdDate) VALUES
(1, 'john.doe@example.com', 'admin@example.com', '2023-01-01'),
(2, 'jane.smith@example.com', 'admin@example.com', '2023-01-02');

-- Inserting sample data into Featured_Book table
-- Note: The book_title_pageImages data type should be TEXT or BLOB, and the content should be a string or binary data.
INSERT INTO Featured_Book (featured_book_id, book_title_page) VALUES
(1, 'image_path_or_blob_1'),
(2, 'image_path_or_blob_2'),
(3, 'image_path_or_blob_3'),
(4, 'image_path_or_blob_4'),
(5, 'image_path_or_blob_5');

-- Inserting sample data into book_issued table
INSERT INTO book_issued (Student_email, BookID, Returned, ReturnDate, issue_date) VALUES
('john.doe@example.com', 1, 0, NULL, '2023-01-10'),
('jane.smith@example.com', 2, 1, '2023-01-15', '2023-01-10'),
('alice.johnson@example.com', 3, 0, NULL, '2023-01-16'),
('mike.brown@example.com', 4, 1, '2023-01-20', '2023-01-15'),
('emma.wilson@example.com', 5, 0, NULL, '2023-01-25');

-- Inserting sample data into rooms table
INSERT INTO rooms (roomid, Room_number, capacity, availability) VALUES
(1, 101, 2, 1),
(2, 102, 3, 0),
(3, 103, 2, 1),
(4, 104, 1, 1),
(5, 105, 1, 0);

-- Inserting sample data into room_issued table
INSERT INTO room_issued (Student_email, roomID, reserved_date, start_date, end_date) VALUES
('jane.smith@example.com', 2, '2023-01-10', '2023-01-10', '2023-01-12'),
('alice.johnson@example.com', 3, '2023-01-15', '2023-01-15', '2023-01-16'),
('mike.brown@example.com', 4, '2023-01-20', '2023-01-20', '2023-01-21'),
('emma.wilson@example.com', 5, '2023-01-25', '2023-01-25', '2023-01-26');

*/

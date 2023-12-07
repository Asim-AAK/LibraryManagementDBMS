-- Create Student table
CREATE TABLE Student (
    email VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100),
    password INT,
    fine FLOAT,
    Access BIT
);

-- Create Admin table
CREATE TABLE Admin (
    email VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100),
    password INT
);

-- Create Hold table
CREATE TABLE Hold (
    hold_id INT PRIMARY KEY,
    Student_email VARCHAR(100),
    Admin_email VARCHAR(100),
    holdDate DATE,
    FOREIGN KEY (Student_email) REFERENCES Student(email),
    FOREIGN KEY (Admin_email) REFERENCES Admin(email)
);

-- Create Books table
CREATE TABLE Books (
    bookid INT PRIMARY KEY,
    Author VARCHAR(100),
    Title VARCHAR(100),
    Genre VARCHAR(100),
    Copies_Available INT,
    fine_amount_per_day FLOAT
);

-- Create book_issued table
CREATE TABLE book_issued (
    Student_email VARCHAR(100),
    BookID INT,
    Returned BIT,
    ReturnDate DATETIME,
    issue_date DATETIME,
    PRIMARY KEY (Student_email, BookID),
    FOREIGN KEY (Student_email) REFERENCES Student(email),
    FOREIGN KEY (BookID) REFERENCES Books(bookid)
);

-- Create room_issued table
CREATE TABLE room_issued (
    Student_email VARCHAR(100),
    roomID INT,
    reserved_date DATE,
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (Student_email, roomID),
    FOREIGN KEY (Student_email) REFERENCES Student(email),
    FOREIGN KEY (roomID) REFERENCES rooms(roomid)
);

-- Create rooms table
CREATE TABLE rooms (
    roomid INT PRIMARY KEY,
    Room_number INT,
    capcity INT,
    availability BIT
);

-- Create Featured_Book table
CREATE TABLE Featured_Book (
    book_title_page VARCHAR(100),
    featured_book_id INT PRIMARY KEY REFERENCES Books(BookID)
);




/*INSERT INTO Student (email, name, password, fine, Access)
VALUES
    ('student1@example.com', 'John Doe', 123456, 0.00, 1),
    ('student2@example.com', 'Jane Smith', 654321, 5.50, 1),
    ('student3@example.com', 'Bob Johnson', 987654, 2.25, 0),
    ('student4@example.com', 'Alice Williams', 111222, 0.75, 1),
    ('student5@example.com', 'Charlie Brown', 333444, 10.00, 0);



INSERT INTO Admin (email, name, password)
VALUES
    ('admin1@example.com', 'Admin One', 789012),
    ('admin2@example.com', 'Admin Two', 345678),
    ('admin3@example.com', 'Admin Three', 901234),
    ('admin4@example.com', 'Admin Four', 567890),
    ('admin5@example.com', 'Admin Five', 123456);

INSERT INTO Hold (hold_id, Student_email, Admin_email, holdDate)
VALUES
    (1, 'student1@example.com', 'admin1@example.com', '2023-01-01'),
    (2, 'student2@example.com', 'admin2@example.com', '2023-02-15'),
    (3, 'student3@example.com', 'admin3@example.com', '2023-03-20'),
    (4, 'student4@example.com', 'admin4@example.com', '2023-04-10'),
    (5, 'student5@example.com', 'admin5@example.com', '2023-05-05');


INSERT INTO Books (bookid, Author, Title, Genre, Copies_Available, fine_amount_per_day)
VALUES
    (1, 'Author One', 'Book One', 'Fiction', 10, 0.50),
    (2, 'Author Two', 'Book Two', 'Mystery', 15, 0.75),
    (3, 'Author Three', 'Book Three', 'Science Fiction', 8, 1.00),
    (4, 'Author Four', 'Book Four', 'Romance', 12, 0.60),
    (5, 'Author Five', 'Book Five', 'Thriller', 20, 1.25);


INSERT INTO book_issued (Student_email, BookID, Returned, ReturnDate, issue_date)
VALUES
    ('student1@example.com', 1, 1, '2023-01-10', '2023-01-01'),
    ('student2@example.com', 3, 0, NULL, '2023-02-20'),
    ('student3@example.com', 2, 1, '2023-03-25', '2023-03-20'),
    ('student4@example.com', 4, 0, NULL, '2023-04-15'),
    ('student5@example.com', 5, 1, '2023-05-10', '2023-05-05');
*/

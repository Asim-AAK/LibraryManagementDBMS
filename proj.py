from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox
import sys
from PyQt6.QtCore import QDate, QDateTime, QTime
import pyodbc
import datetime

#___________________________________________________database connection__________________________________________________

server = 'LAPTOP-KRFDT15R\DEMENTED'
database = 'LibraryDB'  # Name of your LibraryDB database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication

# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

#____________________________________________________main function______________________________________________________

current_user_email = None # This variable will be used to store the email of the currently logged in user

#---login page------
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Login, self).__init__() 
        # Load the .ui file
        uic.loadUi('1.welcome_screen.ui', self)

        self.close_pushButton.clicked.connect(self.close)  # Close the application
        self.confirm_pushButton.clicked.connect(self.confirm)  # Login button
        self.contactus_pushButton.clicked.connect(self.contactus)  # Contact us button

    # Main page login and contact us functionality
    def confirm(self):
        # Get the entered username and password
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()

        # Validate the credentials
        is_valid, user_type = self.check_credentials_in_database(email, password)

        if is_valid:
            if user_type == 'Admin':
                self.gotoAdminPanel()
            elif user_type == 'Student':
                global current_user_email
                current_user_email = email
                if self.check_student_access(email):
                    self.gotoStudentDecision()
                else:
                    QtWidgets.QMessageBox.warning(
                        self, 'Account Hold', 'You do not have access due to a hold on your account.'
                    )
        else:
            QtWidgets.QMessageBox.warning(self, 'Login Failed', 'The username or password is incorrect.')

        self.contactus_pushButton.clicked.connect(self.contactus)

    # Check the credentials in the database
    def check_credentials_in_database(self, email, password):
        """ Check if the provided credentials match an entry in the table. """
        try:
            # Establish a database connection
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Execute the query
            cursor.execute(
                '''SELECT 'Admin' AS user_type, email
                   FROM Admin
                   WHERE email = ? AND password = ?
                   UNION ALL
                   SELECT 'Student' AS user_type, email
                   FROM Students
                   WHERE email = ? AND password = ?''', (email, password, email, password)
            )

            result = cursor.fetchone()

            # Close the database connection
            connection.close()

            # Return (True, user_type) if credentials are valid, else (False, None)
            return bool(result), result[0] if result else None

        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return False, None

    def check_student_access(self, email):
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT access FROM Students WHERE email = ?', (email,))
                    result = cursor.fetchone()
                    return result[0] == 1 if result else False
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return False

    def gotoAdminPanel(self):  # Admin panel functionality - takes you to the admin panel page
        self.window = AdminPanel()  # Pass the prompt to the main window
        self.window.show()
        self.close()

    def gotoStudentDecision(self):  # Student decision functionality - takes you to the student decision page
        self.window = student_decision()  # Pass the prompt to the main window
        self.window.show()
        self.close()

    def contactus(self):  # Contact us functionality - takes you to the contact us page
        self.hide()
        self.view_window = contact_us()
        self.view_window.show()

        
#---student decision page------
class student_decision(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('2.student_decision.ui', self) 

        self.confirm_pushButton.clicked.connect(self.confirm) # login button
        self.logout_pushButton.clicked.connect(self.logout) # logout button

    def confirm(self): # check if book or room is selected and go to the respective page
        if self.book_radioButton.isChecked():
            self.hide()
            self.view_window = book_issue()
            self.view_window.show()
        elif self.room_radioButton.isChecked():
            self.hide()
            self.view_window = room_issue()
            self.view_window.show()
        else:
            QtWidgets.QMessageBox.information(self, 'Information', 'Please click an option')

    def logout(self): # logout functionality - takes you back to the login page
        self.hide()
        self.view_window = Login()
        self.view_window.show()

#---book issue page------
class book_issue(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        uic.loadUi('3.book_issue.ui', self)  # Ensure this UI file has a QTableWidget named 'booksTableWidget'
        
        self.close_pushButton.clicked.connect(self.revert)
        self.issue_pushButton.clicked.connect(self.issue)
        self.search_pushButton.clicked.connect(self.search)

        # Fetch all books and populate the table during initialization
        self.populate_all_books()

    def populate_all_books(self):
        # Fetch all books from the database
        query = "SELECT bookid, Author, Title, Genre, Copies_Available FROM Books"
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    self.populate_table(cursor.fetchall())  # Populate the table with fetched books
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')


    def search(self):
        author = self.author_lineEdit.text()
        title = self.title_lineEdit.text()
        genre = ''
        if self.fiction_radioButton.isChecked():
            genre = 'Fiction'
        elif self.magazine_radioButton.isChecked():
            genre = 'Magazine'
        elif self.nonfiction_radioButton.isChecked():
            genre = 'NonFiction'

        # Adjust wildcards for partial match for both author and title
        author = f"%{author}%"
        title = f"%{title}%"

        # Construct the SQL query
        query = """
        SELECT bookid, Author, Title, Genre, Copies_Available 
        FROM Books 
        WHERE Author LIKE ? AND Title LIKE ? AND Genre = ?
        """

        # Execute the query and populate the table
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (author, title, genre))
                    search_results = cursor.fetchall()

                    if not search_results:
                        QtWidgets.QMessageBox.warning(self, 'Book Not Found', 'No books matching the search criteria were found.')
                    else:
                        self.populate_table(search_results)  # Pass the results to the table population method
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')

    def populate_table(self, data):
        self.booksTableWidget.setRowCount(0)  # Clear the table first
        for row_number, row_data in enumerate(data):
            self.booksTableWidget.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.booksTableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(cell_data)))
    
    def issue(self):
        # Check if a book is selected first
        selected_row = self.booksTableWidget.currentRow()
        if selected_row < 0:  # No selection
            QtWidgets.QMessageBox.warning(self, 'Selection Required', 'Please select a book to issue.')
            return

        # Extract book details from the selected row
        book_id_item = self.booksTableWidget.item(selected_row, 0)
        book_title_item = self.booksTableWidget.item(selected_row, 1)
        book_author_item = self.booksTableWidget.item(selected_row, 2)
        book_genre_item = self.booksTableWidget.item(selected_row, 3)
        copies_available_item = self.booksTableWidget.item(selected_row, 4)

        # Check if all necessary items are present
        if not all([book_id_item, book_title_item, book_author_item, book_genre_item, copies_available_item]):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Incomplete book details.')
            return

        book_id = book_id_item.text()
        book_title = book_title_item.text()
        book_author = book_author_item.text()
        book_genre = book_genre_item.text()
        copies_available = int(copies_available_item.text())

        # Check if there are available copies to issue
        if copies_available <= 0:
            QtWidgets.QMessageBox.warning(self, 'No Copies Available', 'There are no more available copies of the selected book.')
            return

        # Update Copies_Available and insert into book_issued in a transaction
        try:
            with pyodbc.connect(connection_string, autocommit=False) as conn:
                with conn.cursor() as cursor:
                    # Update Copies_Available in the Books table
                    cursor.execute('UPDATE Books SET Copies_Available = Copies_Available - 1 WHERE bookid = ?', (book_id,))

                    # Insert into book_issued
                    issue_date = datetime.datetime.now()
                    cursor.execute('INSERT INTO book_issued (Student_email, BookID, Returned, ReturnDate, issue_date) VALUES (?, ?, 0, NULL, ?)',
                                   (current_user_email, book_id, issue_date))

                conn.commit()  # Commit the transaction
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')
            return

        # Proceed with issuing the book
        return_date = QDate.currentDate().addDays(14)

        self.book_issued_window = book_issued(book_title, book_author, book_id, book_genre, issue_date, return_date)
        self.book_issued_window.show()
        self.close()

    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

            
#---book issued page displayed to student after issuing a book------
class book_issued(QtWidgets.QMainWindow):
    def __init__(self, book_title, book_author, book_id, book_genre, issue_date, return_date):
        super().__init__()
        uic.loadUi('4.book_issued.ui', self)

        # Set the details in the UI
        self.booktitle_lineEdit.setText(book_title)
        self.bookauthor_lineEdit.setText(book_author)
        self.bookid_lineEdit.setText(book_id)
        self.genre_lineEdit.setText(book_genre)
        self.issueddate_dateTimeEdit.setDate(issue_date) 
        self.returndate_dateTimeEdit.setDate(return_date)

        self.okay_pushButton.clicked.connect(self.close)
        
    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

#---room issue page------
class room_issue(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        uic.loadUi('5.room_issue.ui', self)  # Ensure this UI file has a QTableWidget named 'roomsTableWidget'
        
        self.close_pushButton_2.clicked.connect(self.revert)
        self.issue_pushButton_2.clicked.connect(self.issue)
        self.search_pushButton_2.clicked.connect(self.search)

        # Initialize the QTableWidget
        self.roomsTableWidget.setColumnCount(4)
        self.roomsTableWidget.setHorizontalHeaderLabels(['Room ID', 'Room Number', 'Capacity', 'Availability'])

        # Populate the table when the window is initialized
        self.populate_table()

    def search(self):
        room_id = self.roomid_lineEdit.text()
        room_number = self.roomnumber_lineEdit.text()

        # Adjust wildcards for partial match for both room id and room number
        room_id = f"%{room_id}%"
        room_number = f"%{room_number}%"

        # Construct the SQL query
        query = """
        SELECT roomid, Room_number, capacity, availability
        FROM rooms
        WHERE roomid LIKE ? AND Room_number LIKE ?
        """

        # Execute the query and populate the table
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (room_id, room_number))
                    search_results = cursor.fetchall()

                    if not search_results:
                        QtWidgets.QMessageBox.warning(self, 'Room Not Found', 'No rooms matching the search criteria were found.')
                    else:
                        self.populate_table(search_results)  # Pass the results to the table population method
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')

    def populate_table(self, data=None):
        if data is None:
            # If data is not provided, fetch all data from the rooms table
            try:
                with pyodbc.connect(connection_string) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute('SELECT roomid, Room_number, capacity, availability FROM rooms')
                        data = cursor.fetchall()
            except pyodbc.Error as e:
                QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')

        self.roomsTableWidget.setRowCount(0)  # Clear the table first
        for row_number, row_data in enumerate(data):
            self.roomsTableWidget.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.roomsTableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(cell_data)))

    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

    def issue(self):
        # Check if a room is selected first
        selected_row = self.roomsTableWidget.currentRow()
        if selected_row < 0:  # No selection
            QtWidgets.QMessageBox.warning(self, 'Selection Required', 'Please select a room to issue.')
            return

        # Extract room details from the selected row
        room_id_item = self.roomsTableWidget.item(selected_row, 0)
        room_number_item = self.roomsTableWidget.item(selected_row, 1)
        room_availability_item = self.roomsTableWidget.item(selected_row, 3)

        # Check if all necessary items are present
        if not all([room_id_item, room_number_item, room_availability_item]):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Incomplete room details.')
            return

        room_id = room_id_item.text()
        room_number = room_number_item.text()
        room_availability = room_availability_item.text()

        # Check if the room is available
        if room_availability != 'True':
            print(f"Room ID: {room_id}, Room Number: {room_number}, Availability: {room_availability}")
            QtWidgets.QMessageBox.warning(self, 'Room Unavailable', 'Unable to issue room as the room is currently unavailable.')
            return

        # Update Availability in the database
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE rooms SET availability = 0 WHERE roomid = ?', (room_id,))
                    conn.commit()  # Commit the transaction

                    # Insert the issued room into the room_issued table
                    reserved_date = QDate.currentDate().toString('yyyy-MM-dd')
                    start_date = reserved_date  # You may want to adjust this based on your business logic
                    end_date = QDate.fromString(start_date, 'yyyy-MM-dd').addDays(1).toString('yyyy-MM-dd')
                    cursor.execute('INSERT INTO room_issued (Student_email, roomID, reserved_date, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
                                   (current_user_email, room_id, reserved_date, start_date, end_date))
                    conn.commit()  # Commit the transaction
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')
            return

        # Proceed with issuing the room
        self.room_issued_window = room_issued(room_id, room_number)
        self.room_issued_window.show()
        self.close()

#---room issued page displayed to student after issuing a room------
class room_issued(QtWidgets.QMainWindow):
    def __init__(self, room_id, room_number):
        super().__init__() 
        uic.loadUi('6.room_issued.ui', self)

        # Set the details in the UI
        self.discussionroomnumber_lineEdit.setText(room_number)
        self.discussionroomid_lineEdit.setText(room_id)
        
        # You need to initialize these variables with appropriate values
        reservation_date = QDate.currentDate()
        start_time = QTime.currentTime()
        end_time = QTime.currentTime()

        self.reservationdate_dateTimeEdit.setDate(reservation_date) 
        self.starttime_dateTimeEdit.setTime(start_time) 
        self.endtime_dateTimeEdits.setTime(end_time)

        self.okay_pushButton.clicked.connect(self.revert)

    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

class contact_us(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('7.contact_us.ui', self) 

        self.pushButton_2.clicked.connect(self.search_books)
        self.pushButton.clicked.connect(self.revert)

    def search_books(self):
        student_email = self.studentemail_lineEdit.text()

        # Validate if the student email is entered
        if not student_email:
            QtWidgets.QMessageBox.warning(self, 'Invalid Input', 'Please enter a student email.')
            return

        # Check if the student account is on hold
        is_on_hold = self.check_student_on_hold(student_email)

        if is_on_hold:
            self.onhold_radioButton.setChecked(True)
            #self.notonhold_radioButton.setChecked(False)
            QtWidgets.QMessageBox.information(self, 'Account on Hold', 'The student\'s account is on hold.')
        else:
            #self.onhold_radioButton.setChecked(False)
            self.notonhold_radioButton.setChecked(True)

    def check_student_on_hold(self, student_email):
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT 1 FROM Hold WHERE Student_email = ?', (student_email,))
                    return bool(cursor.fetchone())
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')
            return False

    def revert(self):
        self.hide()
        self.view_window = Login()  # Assuming UI is your main window class
        self.view_window.show()

class AdminPanel(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Admin Panel.ui', self) 

        self.close_pushButton.clicked.connect(self.revert)
        self.confirm_pushButton.clicked.connect(self.confirm)

    def revert(self):
        self.hide()
        self.view_window = Login()
        self.view_window.show()

    def confirm(self):
        if self.discussionRoomsManagement_radioButton.isChecked():
            self.hide()
            self.view_window = Rooms_issued_admin()
            self.view_window.show()
        elif self.issuedBooks_radioButton.isChecked():
            self.hide()
            self.view_window = Issued_books_admin()
            self.view_window.show()
        elif self.userManagement_radioButton.isChecked():
            self.hide()
            self.view_window = User_Access_Admin()
            self.view_window.show()
        elif self.finesAndHolds_radioButton.isChecked():
            self.hide()
            self.view_window = Fine_Hold_Admin()
            self.view_window.show()
        else:
            QtWidgets.QMessageBox.information(self, 'Information', 'Please click an option')

#---issued books page------
class Issued_books_admin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Issued_books_admin.ui', self)

        self.close_pushButton.clicked.connect(self.revert)

        # Populate the table with issued books during initialization
        self.populate_issued_books()

    def revert(self):
        self.hide()
        self.view_window = AdminPanel()
        self.view_window.show()

    def populate_issued_books(self):
        # Fetch issued books data from the database
        query = """
        SELECT bi.Student_email, bi.BookID, b.Author, b.Title, bi.Returned, bi.ReturnDate, bi.issue_date
        FROM book_issued bi
        JOIN Books b ON bi.BookID = b.bookid
        """
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    issued_books_data = cursor.fetchall()

                    # Check if there are issued books
                    if issued_books_data:
                        self.populate_table(issued_books_data)
                    else:
                        QtWidgets.QMessageBox.information(self, 'No Issued Books', 'No books have been issued.')
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')

    def populate_table(self, data):
        self.booksTableWidget.setRowCount(0)  # Clear the table first
        for row_number, row_data in enumerate(data):
            self.booksTableWidget.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.booksTableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(cell_data)))

    
# Global variable to store the current user's email
current_user_email = None

class Rooms_issued_admin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Rooms_issued_admin.ui', self)  # Assuming you have a UI file named RoomsIssuedAdmin.ui

        self.close_pushButton.clicked.connect(self.revert)
        
        # Initialize the QTableWidget
        self.roomsTableWidget.setColumnCount(5)
        self.roomsTableWidget.setHorizontalHeaderLabels(['Student Email', 'Room Number', 'Reserved Date', 'Start Date', 'End Date'])

        # Populate the table when the window is initialized
        self.populate_table()

    def revert(self):
        self.hide()
        self.view_window = AdminPanel()  # Assuming you have an AdminPanel class
        self.view_window.show()

    def populate_table(self):
        # Fetch data from the database and populate the table
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT Student_email, roomID, reserved_date, start_date, end_date FROM room_issued')
                    data = cursor.fetchall()
                    self.populate_table_data(data)
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')

    def populate_table_data(self, data):
        self.roomsTableWidget.setRowCount(0)  # Clear the table first
        for row_number, row_data in enumerate(data):
            self.roomsTableWidget.insertRow(row_number)
            for column_number, cell_data in enumerate(row_data):
                self.roomsTableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(cell_data)))

class User_Access_Admin(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('User Access_Admin.ui', self) 

        # Initialize the QTableWidget
        self.hold_TableWidget.setColumnCount(4)
        self.hold_TableWidget.setHorizontalHeaderLabels(['Hold ID', 'Student Email', 'Admin Email', 'Hold Date'])

        # Populate the table when the window is initialized
        self.populate_table()

        self.confirm_pushButton.clicked.connect(self.confirm)
        self.pushButton.clicked.connect(self.return_to_admin_panel)

    def confirm(self):
        if self.no_radioButton.isChecked():
            selected_row = self.hold_TableWidget.currentRow()
            if selected_row >= 0:
                # Extract Student_email from the selected row
                student_email_item = self.hold_TableWidget.item(selected_row, 1)

                if student_email_item:
                    student_email = student_email_item.text()

                    try:
                        with pyodbc.connect(connection_string) as conn:
                            with conn.cursor() as cursor:
                                # Remove the Hold entry from the Hold table
                                cursor.execute('DELETE FROM Hold WHERE Student_email = ?', (student_email,))
                                conn.commit()

                                # Update access to 1 in the Student table
                                cursor.execute('UPDATE Students SET access = 1 WHERE email = ?', (student_email,))
                                conn.commit()

                                QtWidgets.QMessageBox.information(self, 'Hold Removed', 'Hold has been removed, and access is now granted.')
                                # Refresh the table after the changes
                                self.populate_table()
                    except pyodbc.Error as e:
                        QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')
                else:
                    QtWidgets.QMessageBox.information(self, 'Information', 'Please select a student row.')
            else:
                QtWidgets.QMessageBox.information(self, 'Information', 'Please select a student row.')
        else:
            QtWidgets.QMessageBox.information(self, 'Information', 'Please click on the "No" option.')

    def populate_table(self):
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT hold_id, Student_email, Admin_email, holdDate FROM Hold')
                    data = cursor.fetchall()

                    self.hold_TableWidget.setRowCount(0)  # Clear the table first
                    for row_number, row_data in enumerate(data):
                        self.hold_TableWidget.insertRow(row_number)
                        for column_number, cell_data in enumerate(row_data):
                            self.hold_TableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(cell_data)))
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')
    def return_to_admin_panel(self):
        # Return to the AdminPanel
        self.hide()
        self.view_window = AdminPanel()
        self.view_window.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
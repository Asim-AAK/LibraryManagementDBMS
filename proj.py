from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox
import sys
from PyQt6.QtCore import QDate, QDateTime, QTime
import pyodbc

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

#---login page------
class Login(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Login, self).__init__() 
        # Load the .ui file
        uic.loadUi('1.welcome_screen.ui', self) 

        self.close_pushButton.clicked.connect(self.close) # close the application
        self.confirm_pushButton.clicked.connect(self.confirm) # login button
        self.contactus_pushButton.clicked.connect(self.contactus) # contact us button
    
    # main page login and contact us functionality
    def confirm(self):
        # Get the entered username and password
        email = self.email_lineEdit.text()
        password = self.password_lineEdit.text()

        # Validate the credentials
        is_valid = self.check_credentials_in_database(email, password)

        if is_valid:
            QtWidgets.QMessageBox.information(self, 'Login Successful', 'You have logged in successfully.')
            # You can proceed to the next window after close the login window here
            if (email=='admin@example.com'):
                self.gotoAdminPanel()
            else:
                self.gotoStudentDecision()
          
        else:
            QtWidgets.QMessageBox.warning(self, 'Login Failed', 'The username or password is incorrect.')

        self.contactus_pushButton.clicked.connect(self.contactus)

    # check the credentials in the database
    def check_credentials_in_database(self, email, password):
        """ Check if the provided credentials match an entry in the  table. """
        try:
            # Establish a database connection
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()
            
            # Execute the query
            cursor.execute('''SELECT 'Admin' AS user_type, email
                            FROM Admin
                            WHERE email = ? AND password = ?
                            UNION ALL
                            SELECT 'Student' AS user_type, email
                            FROM Students
                            WHERE email = ? AND password = ?
                            ''', (email, password, email, password))
            
            result = cursor.fetchone()
            
            # Close the database connection
            connection.close()
            
            # Return True if credentials are valid, else False
            return bool(result)
        
        except pyodbc.Error as e:
            print(f"An error occurred: {e}")
            return False

    def gotoAdminPanel(self): # admin panel functionality - takes you to the admin panel page
        self.window = AdminPanel()  # Pass the prompt to the main window
        self.window.show()
        self.close()
    
    
    def gotoStudentDecision(self): # student decision functionality - takes you to the student decision page
        self.window = student_decision()  # Pass the prompt to the main window
        self.window.show()
        self.close()
    

    def contactus(self): # contact us functionality - takes you to the contact us page
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
        
        self.close_pushButton.clicked.connect(self.close)
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

        # Update Copies_Available in the database
        try:
            with pyodbc.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('UPDATE Books SET Copies_Available = Copies_Available - 1 WHERE bookid = ?', (book_id,))
                    conn.commit()  # Commit the transaction
        except pyodbc.Error as e:
            QtWidgets.QMessageBox.warning(self, 'Database Error', f'An error occurred: {e}')
            return

        # Proceed with issuing the book
        issue_date = QDate.currentDate()
        return_date = issue_date.addDays(14)

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
        room_capacity_item = self.roomsTableWidget.item(selected_row, 2)
        room_availability_item = self.roomsTableWidget.item(selected_row, 3)

        # Check if all necessary items are present
        if not all([room_id_item, room_number_item, room_capacity_item, room_availability_item]):
            QtWidgets.QMessageBox.warning(self, 'Error', 'Incomplete room details.')
            return

        room_id = room_id_item.text()
        room_number = room_number_item.text()
        room_capacity = room_capacity_item.text()
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
        #self.submit_pushButton.clicked.connect(self.revert)

    def revert(self):
        self.hide()
        self.view_window = UI()
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
            

class Fine_Hold_Admin(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Fine_Hold_Admin.ui', self)

        self.close_pushButton_2.clicked.connect(self.revert)
        self.confirm_pushButton.clicked.connect(self.revert)
        

    def revert(self):
        self.hide()
        self.view_window = AdminPanel()
        self.view_window.show()

class Issued_books_admin(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Issued_books_admin.ui', self) 

        self.close_pushButton.clicked.connect(self.revert)
    
    def revert(self):
        self.hide()
        self.view_window = AdminPanel()
        self.view_window.show()
    
class Rooms_issued_admin(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('Rooms_issued_admin.ui', self) 

        self.close_pushButton.clicked.connect(self.revert)
    
    def revert(self):
        self.hide()
        self.view_window = AdminPanel()
        self.view_window.show()

class User_Access_Admin(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('User Access_Admin.ui', self) 

        self.confirm_pushButton.clicked.connect(self.confirm)
    
    def confirm(self):
        if (self.student_radioButton.isChecked() or self.staff_radioButton.isChecked()):
            if (self.no_radioButton.isChecked() or self.yes_radioButton.isChecked()):
                #if yes, student gets retracted
                self.hide()
                self.view_window = AdminPanel()
                self.view_window.show()
            else:
                QtWidgets.QMessageBox.information(self, 'Information', 'Please click an option from yes or no')
        else:
            QtWidgets.QMessageBox.information(self, 'Information', 'Please click an option from student or staff')
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
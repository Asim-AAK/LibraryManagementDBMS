from PyQt6 import QtWidgets, uic
import sys
from PyQt6.QtCore import Qt

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(UI, self).__init__() 
        # Load the .ui file
        uic.loadUi('1.welcome_screen.ui', self) 

        self.close_pushButton.clicked.connect(self.close)

        self.confirm_pushButton.clicked.connect(self.confirm)
        self.contactus_pushButton.clicked.connect(self.contactus)

    

    def confirm(self):
        #if id and password in database:
        if self.email_lineEdit.text() == 'admin':
            self.hide()
            self.view_window = AdminPanel()
            self.view_window.show()
        else:
            self.hide()
            self.view_window = student_decision()
            self.view_window.show()

    def contactus(self):
        self.hide()
        self.view_window = contact_us()
        self.view_window.show()

    
        

class student_decision(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('2.student_decision.ui', self) 

        self.confirm_pushButton.clicked.connect(self.confirm)

    def confirm(self):
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

class book_issue(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('3.book_issue.ui', self) 

        self.close_pushButton.clicked.connect(self.revert)
        self.issue_pushButton.clicked.connect(self.issue)
        

    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

    def issue(self):
        #if book in listbox
        self.hide()
        self.view_window = book_issued()
        self.view_window.show()

        

class book_issued(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('4.book_issued.ui', self) 

        self.okay_pushButton.clicked.connect(self.revert)

    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

class room_issue(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('5.room_issue.ui', self) 

        self.close_pushButton_2.clicked.connect(self.revert)
        self.issue_pushButton_2.clicked.connect(self.issue)
        

    def revert(self):
        self.hide()
        self.view_window = student_decision()
        self.view_window.show()

    def issue(self):
        #if book in listbox
        self.hide()
        self.view_window = book_issued()
        self.view_window.show()

class room_issued(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super().__init__() 
        # Load the .ui file
        uic.loadUi('6.room_issued.ui', self) 

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
        self.submit_pushButton.clicked.connect(self.revert)

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
        self.view_window = UI()
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
    window = UI()
    window.show()
    sys.exit(app.exec())
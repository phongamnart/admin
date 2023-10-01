import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from add_product import AddProductWindow
import mysql.connector

class AdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Window')
        self.setGeometry(100, 100, 1290, 720)

        self.login_widget = QWidget(self)
        self.setCentralWidget(self.login_widget)

        self.login_layout = QVBoxLayout()
        self.login_widget.setLayout(self.login_layout)

        username_row = QHBoxLayout()
        self.username_label = QLabel('Username:', self)
        self.username_label.setFont(QFont('Arial', 12))
        username_row.addWidget(self.username_label)
        self.username_input = QLineEdit(self)
        self.username_input.setFixedSize(1150, 30)
        self.username_input.setFont(QFont('Arial', 12))
        username_row.addWidget(self.username_input)
        self.login_layout.addLayout(username_row)

        password_row = QHBoxLayout()
        self.password_label = QLabel('Password:', self)
        self.password_label.setFont(QFont('Arial', 12))
        password_row.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setFixedSize(1150, 30)
        self.password_input.setFont(QFont('Arial', 12))
        self.password_input.setEchoMode(QLineEdit.Password)
        password_row.addWidget(self.password_input)
        self.login_layout.addLayout(password_row)

        self.login_button = QPushButton('Login', self)
        self.login_layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login)
        self.login_button.setFixedSize(200, 50)
        self.login_button.setFont(QFont('Arial', 12))

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # เชื่อมต่อกับฐานข้อมูล MySQL
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='nart',
                password='tamarin17',
                database='product'
            )

            cursor = connection.cursor()
            query = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                QMessageBox.information(self, 'Login Successful', 'Welcome, {}'.format(username))
                self.open_add_product_window()
                self.username_input.clear()
                self.password_input.clear()
            else:
                QMessageBox.warning(self, 'Login Failed', 'Invalid username or password. Please try again.')
                self.password_input.clear()
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
    
    def open_add_product_window(self):
        self.add_product_window = AddProductWindow()
        self.add_product_window.show()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_window = AdminWindow()
    admin_window.show()
    sys.exit(app.exec_())

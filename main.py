import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from customer import CustomerWindow
from admin import AdminWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 1290, 720)

        admin_button = QPushButton('Admin', self)
        admin_button.setGeometry(250, 250, 300, 200)
        admin_button.clicked.connect(self.open_admin_window)
        self.set_button_font(admin_button, 16)

        self.admin_label = QLabel(self)
        self.admin_label.setGeometry(50, 120, 300, 50)
        self.admin_label.setAlignment(Qt.AlignCenter)
        self.admin_label.hide()

        customer_button = QPushButton('Customer', self)
        customer_button.setGeometry(700, 250, 300, 200)
        customer_button.clicked.connect(self.open_customer_window)
        self.set_button_font(customer_button, 16)

    def set_button_font(self, button, font_size):
        font = QFont()
        font.setPointSize(font_size)
        button.setFont(font)

    def open_customer_window(self):
        self.customer_window = CustomerWindow()
        self.customer_window.show()

    def open_admin_window(self):
        self.admin_window = AdminWindow()
        self.admin_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

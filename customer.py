import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
import mysql.connector
import threading
import keyboard
import payment

class CustomerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.scanner_thread = ScannerThread(self.scan_product)
        self.scanner_thread.start()
        self.total_price = 0

    def initUI(self):
        self.setWindowTitle('Customer Window')
        self.setGeometry(100, 100, 1290, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.name_label = QLabel('Name:', self)
        self.name_label.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.name_label)

        self.price_label = QLabel('Price:', self)
        self.price_label.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.price_label)

        self.total_price_label = QLabel('Total:', self)
        self.total_price_label.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.total_price_label)

        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.result_label)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Name Product', 'Price'])
        self.layout.addWidget(self.table)

        # Initialize an empty table
        self.table.setRowCount(0)

        # เพิ่มปุ่ม Next
        self.next_button = QPushButton('Next', self)
        self.next_button.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.next_button)
        self.next_button.clicked.connect(self.open_payment_window)

    def scan_product(self, barcode):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='nart',
                password='tamarin17',
                database='product'
            )

            cursor = connection.cursor()
            query = "SELECT name_product, price FROM add_product WHERE barcode = %s"
            cursor.execute(query, (barcode,))
            data = cursor.fetchone()

            if data is not None:
                name_product, price = data
                self.name_label.setText(f'Name: {name_product}')
                self.price_label.setText(f'Price: {price}')
                self.result_label.setText('')

                rowPosition = self.table.rowCount()
                self.table.insertRow(rowPosition)
                self.table.setItem(rowPosition, 0, QTableWidgetItem(name_product))
                self.table.setItem(rowPosition, 1, QTableWidgetItem(str(price)))

                # คำนวณราคาทั้งหมดและแสดงใน Label แสดงผลราคาทั้งหมด
                self.total_price += price
                self.total_price_label.setText(f'Total: {self.total_price:.2f}')

            else:
                result_text = f'Not found barcode: {barcode}'
                self.result_label.setText(result_text)

                self.name_label.setText('Name:')
                self.price_label.setText('Price:')

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            QMessageBox.warning(self, 'Error', 'An error occurred while scanning the barcode.')

    def open_payment_window(self):
        # เมื่อคลิกปุ่ม Next ให้เปิดหน้า payment.py
        self.payment_window = payment.PaymentWindow(self.total_price)
        self.payment_window.show()

class ScannerThread(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback

    def run(self):
        barcode_value = ""
        while True:
            event = keyboard.read_event(suppress=True)
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "enter":
                    self.callback(barcode_value)
                    barcode_value = ""
                else:
                    barcode_value += event.name

if __name__ == '__main__':
    app = QApplication(sys.argv)
    customer_window = CustomerWindow()
    customer_window.show()
    app.exec_()

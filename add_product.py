import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QFont
import mysql.connector

class AddProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Product Window')
        self.setGeometry(100, 100, 1290, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        name_row = QHBoxLayout()
        self.name_label = QLabel('Name:', self)
        self.name_label.setFont(QFont('Arial', 12))
        self.name_input = QLineEdit(self)
        self.name_input.setFixedSize(1150, 30)
        self.name_input.setFont(QFont('Arial', 12))
        name_row.addWidget(self.name_label)
        name_row.addWidget(self.name_input)
        self.layout.addLayout(name_row)

        barcode_row = QHBoxLayout()
        self.barcode_label = QLabel('Barcode:', self)
        self.barcode_label.setFont(QFont('Arial', 12))
        self.barcode_input = QLineEdit(self)
        self.barcode_input.setFixedSize(1150, 30)
        self.barcode_input.setFont(QFont('Arial', 12))
        barcode_row.addWidget(self.barcode_label)
        barcode_row.addWidget(self.barcode_input)
        self.layout.addLayout(barcode_row)

        price_row = QHBoxLayout()
        self.price_label = QLabel('Price:', self)
        self.price_label.setFont(QFont('Arial', 12))
        self.price_input = QLineEdit(self)
        self.price_input.setFixedSize(1150, 30)
        self.price_input.setFont(QFont('Arial', 12))
        price_row.addWidget(self.price_label)
        price_row.addWidget(self.price_input)
        self.layout.addLayout(price_row)

        quantity_row = QHBoxLayout()
        self.quantity_label = QLabel('Quantity:', self)
        self.quantity_label.setFont(QFont('Arial', 12))
        self.quantity_input = QLineEdit(self)
        self.quantity_input.setFixedSize(1150, 30)
        self.quantity_input.setFont(QFont('Arial', 12))
        quantity_row.addWidget(self.quantity_label)
        quantity_row.addWidget(self.quantity_input)
        self.layout.addLayout(quantity_row)

        self.add_button = QPushButton('Add Product', self)
        self.add_button.setFixedSize(200, 50)
        self.layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_product)
        
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name product', 'Barcode', 'Price', 'Quantity', 'Delete'])
        
        self.load_data()

    def add_product(self):
        name = self.name_input.text()
        barcode = self.barcode_input.text()
        price = self.price_input.text()
        quantity = self.quantity_input.text()

        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='nart',
                password='tamarin17',
                database='product'
            )

            cursor = connection.cursor()
            query = "INSERT INTO add_product (name_product, barcode, price, quantity) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, barcode, price, quantity))
            connection.commit()

            QMessageBox.information(self, 'Success', 'Product added successfully.')
            self.clear_inputs()

            cursor.close()
            connection.close()

            # อัปเดตตารางเมื่อเพิ่มสินค้า
            self.load_data()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            QMessageBox.warning(self, 'Error', 'An error occurred while adding the product.')
            
    def load_data(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='nart',
                password='tamarin17',
                database='product'
            )

            cursor = connection.cursor()
            query = "SELECT name_product, barcode, price, quantity FROM add_product"
            cursor.execute(query)
            data = cursor.fetchall()

            self.table.setRowCount(len(data))

            for row_num, row_data in enumerate(data):
                for col_num, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.table.setItem(row_num, col_num, item)
                    
                delete_button = QPushButton('Delete', self)
                delete_button.clicked.connect(lambda _, row=row_num: self.delete_product(row))
                self.table.setCellWidget(row_num, 4, delete_button)

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            QMessageBox.warning(self, 'Error', 'An error occurred while loading data.')

    def delete_product(self, row):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='nart',
                password='tamarin17',
                database='product'
            )

            cursor = connection.cursor()
            name = self.table.item(row, 0).text()
            reply = QMessageBox.question(self, 'Delete Confirmation', f'Do you want to delete the product "{name}"?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                query = "DELETE FROM add_product WHERE name_product = %s"
                cursor.execute(query, (name,))
                connection.commit()

                self.load_data()

                QMessageBox.information(self, 'Success', 'Product deleted successfully.')
            else:
                QMessageBox.information(self, 'Delete Cancelled', 'Product deletion cancelled.')

            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            QMessageBox.warning(self, 'Error', 'An error occurred while deleting the product.')

    def clear_inputs(self):
        self.name_input.clear()
        self.barcode_input.clear()
        self.price_input.clear()
        self.quantity_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    add_product_window = AddProductWindow()
    add_product_window.show()
    app.exec_()

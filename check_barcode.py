import sys
import mysql.connector
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QFont
import keyboard

class NumberCheckerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.scanner_thread = ScannerThread(self.handle_scan_result)
        self.scanner_thread.start()

    def initUI(self):
        self.setWindowTitle("Check Barcode")
        self.setGeometry(100, 100, 500, 200)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # self.label = QLabel("Barcode on database:")
        # layout.addWidget(self.label)
        #
        # barcode_list = self.get_barcodes_from_database()
        # barcode_text = "\n".join(barcode_list)
        # self.label.setText("Barcode on database: " + barcode_text)

        self.label = QLabel("Wait Scan Barcode...")
        layout.addWidget(self.label)

        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)

        self.close_button = QPushButton("Close program")
        self.close_button.clicked.connect(self.close_program)
        layout.addWidget(self.close_button)

        central_widget.setLayout(layout)

    # def get_barcodes_from_database(self):
    #     barcode_list = []
    #
    #     try:
    #         connection = mysql.connector.connect(
    #             host="localhost",
    #             user="nart",
    #             password="tamarin17",
    #             database="product"
    #         )
    #
    #         cursor = connection.cursor()
    #
    #         # คำสั่ง SQL สำหรับดึงบาร์โค้ดทั้งหมด
    #         query = "SELECT barcode FROM add_product"
    #         cursor.execute(query)
    #
    #         for row in cursor.fetchall():
    #             barcode_list.append(row[0])
    #
    #     except mysql.connector.Error as error:
    #         print(f"Error not connect to MySQL: {str(error)}")
    #
    #     finally:
    #         if connection.is_connected():
    #             cursor.close()
    #             connection.close()
    #
    #     return barcode_list

    def handle_scan_result(self, result):
        num1 = result

        query = "SELECT barcode FROM add_product WHERE barcode = %s"

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="nart",
                password="tamarin17",
                database="product"
            )

            cursor = connection.cursor()

            cursor.execute(query, (num1,))
            result = cursor.fetchone()


            if result:
                self.label.setText(f"Barcode: {result[0]}")
            else:
                self.label.setText("Not found: " + num1)

        except mysql.connector.Error as error:
            self.label.setText(f"Error not connect to MySQL: {str(error)}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def close_program(self):
        self.close()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NumberCheckerApp()
    window.show()
    sys.exit(app.exec_())

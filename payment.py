import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont

class PaymentWindow(QMainWindow):
    def __init__(self, total_price):
        super().__init__()
        self.initUI(total_price)

    def initUI(self, total_price):
        self.setWindowTitle('Payment Window')
        self.setGeometry(100, 100, 1290, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.total_label = QLabel(f'Total: {total_price:.2f}', self)
        self.total_label.setFont(QFont('Arial', 12))
        self.layout.addWidget(self.total_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    payment_window = PaymentWindow(0)  # ในตัวอย่างนี้เราใช้ 0 เป็นราคาทั้งหมดเริ่มต้น
    payment_window.show()
    app.exec_()

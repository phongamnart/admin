from PyQt5.QtWidgets import QMainWindow

class CustomerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Window')
        self.setGeometry(200, 200, 400, 200)

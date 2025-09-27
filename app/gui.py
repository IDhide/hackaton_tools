import sys
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class ApiRequestThread(QThread):
    result_ready = pyqtSignal(str)

    def run(self):
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        if response.status_code == 200:
            self.result_ready.emit(response.text)
        else:
            self.result_ready.emit('Error')

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt API Example")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()
        self.button = QPushButton("Fetch Data", self)
        self.button.clicked.connect(self.fetch_data)
        self.label = QLabel("Response will appear here", self)

        self.layout.addWidget(self.button)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.api_thread = ApiRequestThread()
        self.api_thread.result_ready.connect(self.display_result)

    def fetch_data(self):
        self.label.setText("Loading...")
        self.api_thread.start()

    def display_result(self, data):
        self.label.setText(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

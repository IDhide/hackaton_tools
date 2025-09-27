import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
import requests


class ToolManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Tool Management System")
        self.setGeometry(100, 100, 500, 300)

        # Layout
        self.layout = QVBoxLayout()

        # Upload Image Button
        self.upload_button = QPushButton('Upload Image', self)
        self.upload_button.clicked.connect(self.upload_image)
        self.layout.addWidget(self.upload_button)

        # Result Labels
        self.result_label = QLabel('Recognition Result: ', self)
        self.layout.addWidget(self.result_label)

        self.confidence_label = QLabel('Confidence: ', self)
        self.layout.addWidget(self.confidence_label)

        # Exit Button
        self.quit_button = QPushButton('Exit', self)
        self.quit_button.clicked.connect(self.quit_app)
        self.layout.addWidget(self.quit_button)

        # Central widget
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def upload_image(self):
        # Open file dialog to select an image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.xpm *.jpg)",
                                                   options=options)

        if file_name:
            # Send the image to the backend (FastAPI)
            files = {'file': open(file_name, 'rb')}
            response = requests.post('http://127.0.0.1:8000/tools/upload', files=files)
            result = response.json()

            # Show recognition results
            self.result_label.setText(f"Recognition Result: {result['tool_name']}")
            self.confidence_label.setText(f"Confidence: {result['confidence']}%")

    def quit_app(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolManagementApp()
    window.show()
    sys.exit(app.exec_())


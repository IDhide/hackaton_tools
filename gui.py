import sys
import requests
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QListWidget, QHBoxLayout

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
        self.setWindowTitle("Управление инструментами")
        self.setGeometry(100, 100, 1200, 700)

        main_hbox = QHBoxLayout()

        # Левый блок: кнопки (вертикально)
        left_vbox = QVBoxLayout()
        btn_fetch = QPushButton("Обновить данные")
        btn_issue = QPushButton("Выдать инструмент")
        btn_accept = QPushButton("Принять инструмент")
        btn_exit = QPushButton("Выход")
        min_w, min_h = 150, 50
        for btn in [btn_fetch, btn_issue, btn_accept, btn_exit]:
            btn.setMinimumSize(min_w, min_h)
            left_vbox.addWidget(btn)

        btn_fetch.clicked.connect(self.load_missed_people)
        btn_issue.clicked.connect(self.issue_tools)
        btn_accept.clicked.connect(self.accept_tools)
        btn_exit.clicked.connect(self.close)

        center_vbox = QVBoxLayout()
        label_requests = QLabel("Заявки на выдачу инструментов")
        label_requests.setAlignment(Qt.AlignCenter)
        self.requests_list = QListWidget()
        self.requests_list.setFixedWidth(500)

        center_vbox.addWidget(label_requests)
        center_vbox.addWidget(self.requests_list)

        right_vbox = QVBoxLayout()
        label_misplaced = QLabel("Люди, не сдавшие инструменты")
        label_misplaced.setAlignment(Qt.AlignCenter)
        self.misplaced_people_list = QListWidget()
        self.misplaced_people_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        right_vbox.addWidget(label_misplaced)
        right_vbox.addWidget(self.misplaced_people_list)

        main_hbox.addLayout(left_vbox)
        main_hbox.addLayout(center_vbox)
        main_hbox.addLayout(right_vbox)

        self.setLayout(main_hbox)

        self.load_missed_people()

    def load_missed_people(self):
        # Получение данных через API
        try:
            response = requests.get("http://api_url/endpoint_for_missed_people")
            if response.status_code == 200:
                data = response.json()
                self.misplaced_people_list.clear()
                for person in data:
                    self.misplaced_people_list.addItem(f"{person['name']} (ID: {person['id']})")
            else:
                self.misplaced_people_list.addItem("Ошибка загрузки данных")
        except Exception as e:
            self.misplaced_people_list.addItem(f"Ошибка: {str(e)}")

    def accept_tools(self):
        # Аналогично для принятия
        selected_items = self.misplaced_people_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            person_id = self.extract_id_from_item(item.text())
            if person_id is None:
                continue
            try:
                response = requests.post('https://jsonplaceholder.typicode.com/posts', json={"person_id": person_id})
                if response.status_code == 200:
                    print(f"Принято инструменты {person_id}")
                else:
                    print(f"Ошибка при принятии инструментов {person_id}")
            except Exception as e:
                print(f"Ошибка: {str(e)}")
        self.load_missed_people()

    def issue_tools(self):
        # Отправка запроса на выдачу инструментов
        selected_items = self.misplaced_people_list.selectedItems()
        if not selected_items:
            return  # Нет выбранных элементов
        for item in selected_items:
            person_id = self.extract_id_from_item(item.text())
            if person_id is None:
                continue
            try:
                response = requests.post('https://jsonplaceholder.typicode.com/posts', json={"person_id": person_id})
                if response.status_code == 200:
                    print(f"Инструменты выданы {person_id}")
                else:
                    print(f"Ошибка при выдаче инструментов {person_id}")
            except Exception as e:
                print(f"Ошибка: {str(e)}")
        # Обновить список после операции
        self.load_missed_people()

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

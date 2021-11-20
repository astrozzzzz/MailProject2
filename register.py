import sys
import socket

from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from client_modules.mail_client import Client


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(550, 550)

        # Подключение дизайна
        uic.loadUi('design/registration.ui', self)
        self.setWindowTitle('Вход в почту')
        self.label_2.resize(135, 22)
        self.label_3.setText('')
        self.label_3.resize(160, 41)
        self.lineEdit.setMaxLength(12)

        self.pushButton.clicked.connect(self.login)
        self.pushButton_2.clicked.connect(self.register)

        # Подключение к серверу
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.client.connect(("127.0.0.1", 1234))

    def login(self):
        try:
            # Проверка, есть ли пользователь в базе
            username = self.lineEdit.text()
            if username == '':
                self.label_3.setText('Ввдеите имя пользователя')
            else:
                message = '001' + username
                self.client.send(message.encode("utf-8"))
                response = self.client.recv(2048).decode("utf-8")

                # 500 - Код "ОК"
                if response == '500':
                    # Пользователь вошёл, запускаем саму почту
                    self.hide()
                    self.ex = Client(self.client, username)
                    self.ex.show()
                else:
                    self.label_3.setText('Пользователь не найден')
        except Exception as e:
            self.label_3.setText('Ошибка')
            print(e)

    def register(self):
        try:
            # Проверка, есть ли пользователь в базе
            username = self.lineEdit.text()
            if username == '':
                self.label_3.setText('Введите имя пользователя')
            if '%%' in username:
                self.label_3.setText('Нельзя использовать "%%"')
            else:
                message = '002' + username
                self.client.send(message.encode("utf-8"))
                response = self.client.recv(2048).decode("utf-8")

                if response == '500':
                    self.label_3.setText('Успешная регистрация')
                else:
                    self.label_3.setText('Такой пользователь уже есть')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Registration()
    ex.show()
    sys.exit(app.exec_())

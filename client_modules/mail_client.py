from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import uic
from client_modules.write_mail import MailForm
from client_modules.mail_structure import Mail
from client_modules.mail_view import MailView

MAIN_WINDOW_UI = 'design/main_window.ui'


class Client(QWidget):
    def __init__(self, client, username):
        super().__init__()
        self.client = client
        self.username = username

        # Подключаем дизайн
        uic.loadUi(MAIN_WINDOW_UI, self)
        self.setWindowTitle('Почта')
        self.label_11.setText(username)

        # Кнопки
        self.write_mail_btn.clicked.connect(self.write_mail)
        self.next_page.clicked.connect(self.go_forward)
        self.previuos_page.clicked.connect(self.go_back)
        self.btn_list = [i for i in self.show_btn_group.buttons()]
        self.label_list = [self.message_1, self.message_2, self.message_3, self.message_4, self.message_5,
                           self.message_6, self.message_7]
        self.incoming_rbn.toggled.connect(self.manage_filters)
        self.sent_rbn.toggled.connect(self.manage_filters)
        self.reload_btn.clicked.connect(self.show_messages)

        # Всё что касается показа писем
        self.mails = []
        self.current_page = 1
        self.current_filter = 'Входящие'
        self.show_messages()

    # Работа с фильтрами
    def manage_filters(self):
        filter = self.sender()
        if filter.isChecked():
            if filter.text() == 'Входящие':
                self.current_filter = 'Входящие'
                self.show_messages()
            else:
                self.current_filter = 'Исходящие'
                self.show_messages()

    # Показать письма
    def show_messages(self):
        self.mails = []
        self.current_page = 1
        for i in range(7):
            self.label_list[i].setVisible(False)
            self.btn_list[i].setVisible(False)
        if self.current_filter == 'Входящие':
            self.client.send(f'004{self.username}'.encode("utf-8"))
        else:
            self.client.send(f'005{self.username}'.encode("utf-8"))
        print('got filter')
        while True:
            response = self.client.recv(4096).decode("utf-8").split('%%')
            print(response)
            if response == ['404']:
                break
            self.mails.append(Mail(response[0], response[1], response[2], response[3], response[4]))
        self.mails = list(reversed(self.mails))
        print(self.mails)
        if len(self.mails) <= 7:
            for i in range(len(self.mails)):
                self.label_list[i].setText(self.mails[i].get_short_mail())
                self.label_list[i].setVisible(True)
                self.btn_list[i].setVisible(True)
                self.btn_list[i].clicked.connect(self.message_view)
        else:
            for i in range(7):
                self.label_list[i].setText(self.mails[i].get_short_mail())
                self.label_list[i].setVisible(True)
                self.btn_list[i].setVisible(True)
                self.btn_list[i].clicked.connect(self.message_view)
        if len(self.mails) == 0:
            self.current_page = 1
            self.pages_count = 1
        else:
            self.pages_count = len(self.mails) // 7
            if len(self.mails) % 7 != 0:
                self.pages_count += 1
            self.label_pages.setText(f'Страница {self.current_page}/{self.pages_count}')
            self.current_mail = 1

    # Перемещение по страницам писем вперёд
    def go_forward(self):
        if self.current_page != self.pages_count:
            self.current_page += 1
            for i in range(7):
                ind = i + (self.current_page - 1) * 7
                if ind < len(self.mails):
                    self.label_list[i].setText(self.mails[ind].get_short_mail())
                    self.label_list[i].setVisible(True)
                    self.btn_list[i].setVisible(True)
                    self.btn_list[i].clicked.connect(self.message_view)
                else:
                    self.label_list[i].setVisible(False)
                    self.btn_list[i].setVisible(False)
            self.label_pages.setText(f"Страница {self.current_page}/{self.pages_count}")

    # Перемещение по страницам писем назад
    def go_back(self):
        if self.current_page != 1:
            self.current_page -= 1
            for i in range(7):
                ind = i + (self.current_page - 1) * 7
                if ind < len(self.mails):
                    self.label_list[i].setText(self.mails[ind].get_short_mail())
                    self.label_list[i].setVisible(True)
                    self.btn_list[i].setVisible(True)
                    self.btn_list[i].clicked.connect(self.message_view)
                else:
                    self.label_list[i].setVisible(False)
                    self.btn_list[i].setVisible(False)
            self.label_pages.setText(f"Страница {self.current_page}/{self.pages_count}")

    # Окно для показа письма
    def message_view(self):
        mail = self.mails[(self.current_page - 1) * 7 + self.btn_list.index(self.sender())]
        self.ex = MailView(mail, self.client)
        if mail.sender != self.username:
            self.ex.delete_btn.setVisible(False)
        self.ex.show()

    # Диалоговое окно написания письма
    def write_mail(self, errors=None, content=None):
        self.hide()
        self.ex = MailForm()
        # Если была ошибка
        print(errors)
        if errors is not False:
            self.ex.addressee.setText(content[0])
            self.ex.title.setText(content[1])
            self.ex.main_text.setText(content[2])
            if 'blank user' in errors:
                self.ex.label_not_found.setText('Заполните поле')
                self.ex.label_not_found.setVisible(True)
            elif 'not found' in errors:
                self.ex.label_not_found.setText('Пользователь не найден')
                self.ex.label_not_found.setVisible(True)
            if 'blank title' in errors:
                self.ex.label_title_error.setText('Заполните поле')
                self.ex.label_title_error.setVisible(True)
            if 'blank main text' in errors:
                self.ex.label_error.setText('Заполните поле')
                self.ex.label_error.setVisible(True)
            if '%%main' in errors:
                self.ex.label_error.setText('Нельзя использовать "%%"')
                self.ex.label_error.setVisible(True)
            if '%%title' in errors:
                self.ex.label_title_error.setText('Нельзя использовать "%%"')
        result_dialog = self.ex.exec()
        if result_dialog == QDialog.Rejected:
            self.show()
        elif result_dialog == QDialog.Accepted:
            print('Accepted')
            errors = []
            # Проверка данных
            if len(self.ex.addressee.text()) == 0:
                errors.append('blank user')
            message = '001' + self.ex.addressee.text()
            self.client.send(message.encode('utf-8'))
            response = self.client.recv(2048).decode("utf-8")
            if response != '500':
                errors.append('not found')
            if len(self.ex.title.text()) == 0 or len(self.ex.title.text().replace(' ', '')) == 0:
                errors.append('blank title')
            if len(self.ex.main_text.toPlainText()) == 0 or len(self.ex.main_text.toPlainText().replace(' ', '')) == 0:
                errors.append('blank main text')
            if '%%' in self.ex.main_text.toPlainText():
                errors.append('%%main')
            if '%%' in self.ex.title.text():
                errors.append('%%title')
            if len(errors) != 0:
                data = [self.ex.addressee.text(), self.ex.title.text(), self.ex.main_text.toPlainText()]
                self.write_mail(errors, data)
            # Если ошибки не было
            else:
                print('ok')
                message = '031' + self.username
                self.client.send(message.encode('utf-8'))
                self.client.recv(2048)
                print('sent username')
                message = '032' + self.ex.addressee.text()
                self.client.send(message.encode('utf-8'))
                self.client.recv(2048)
                print('sent username')
                message = '033' + self.ex.title.text()
                self.client.send(message.encode('utf-8'))
                self.client.recv(2048)
                print('sent username')
                message = '034' + self.ex.main_text.toPlainText()
                self.client.send(message.encode('utf-8'))
                print('sent username')
                self.show()

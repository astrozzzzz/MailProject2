from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

MESSAGE_VIEW_UI = 'design/message_view.ui'


class MailView(QWidget):
    def __init__(self, mail, client):
        super().__init__()
        self.mail = mail
        self.client = client

        # Подключаем дизайн
        uic.loadUi(MESSAGE_VIEW_UI, self)
        self.label_sender.setText(self.mail.sender)
        self.label_addressee.setText(self.mail.addressee)
        self.label_title.setText(self.mail.title)
        self.label_date.setText(self.mail.date)
        self.main_text.setText(self.mail.main_text)
        self.main_text.setReadOnly(True)

        # Кнопка удаления записи
        self.delete_btn.clicked.connect(self.delete_mail)

    def delete_mail(self):
        message = '%%'.join([self.mail.sender, self.mail.addressee, self.mail.date, self.mail.title, self.mail.main_text])
        self.client.send(('006' + message).encode("utf-8"))
        self.hide()
import sys

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class MailForm(QDialog):
    def __init__(self):
        super().__init__()

        # Подключаем дизайн
        uic.loadUi('design/mail.ui', self)
        self.setWindowTitle('Написать письмо')
        self.label_error.setVisible(False)
        self.label_not_found.setVisible(False)
        self.label_title_error.setVisible(False)
        self.addressee.setMaxLength(12)
        self.title.setMaxLength(100)

        self.open_txt.clicked.connect(self.read_txt)

    def read_txt(self):
        try:
            file_name = QFileDialog.getOpenFileName(self, 'Выбрать .txt файл', '', 'Файл .txt (*.txt)')[0]
            with open(file_name, 'r', encoding="utf-8") as f:
                content = f.read()
                f.close()
                if len(content) > 3000:
                    self.label_error.setText('Слишком большой файл')
                else:
                    self.main_text.setText(content)
        except Exception:
            pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MailForm()
    result_dialog = ex.exec()
    if result_dialog == QDialog.Rejected:
        print('Нажата "Отмена"')
        sys.excepthook = except_hook
        sys.exit(app.exec())
    elif result_dialog == QDialog.Accepted:
        pass



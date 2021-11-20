import socket

from threading import Thread
from database.db_work import DBHandler

CODES = {
    '001': 'check user',
    '002': 'insert user',
    '031': 'sender',
    '032': 'addressee',
    '033': 'title',
    '034': 'main text',
    '004': 'get messages to user',
    '005': 'get messages from user',
    '006': 'delete mail'
}


class MailServer:
    def __init__(self):
        # Инициализация сервера
        self.server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.server.bind(("127.0.0.1", 1234))
        self.server.listen()
        print('Server is listening')

        # Подключение базы данных
        self.db = DBHandler()

        self.mail = []

    def listen_user(self, user):
        while True:
            try:
                data = user.recv(2048).decode("utf-8")
                if len(data) != 0:
                    action = CODES[data[:3]]
                    if action == 'check user':
                        if self.db.check_user(data[3:]):
                            user.send("500".encode("utf-8"))
                        else:
                            user.send("404".encode("utf-8"))
                    elif action == 'insert user':
                        result = self.db.insert_user(data[3:])
                        if result:
                            user.send("500".encode("utf-8"))
                        else:
                            user.send("404".encode("utf-8"))
                    elif action == 'sender' or action == 'addressee' or action == 'title' or action == 'main text':
                        print('initialized mail part')
                        self.mail.append(data[3:])
                        if action == 'main text':
                            print(self.mail)
                            self.db.insert_mail(*self.mail)
                            self.mail = []
                        else:
                            user.send("500".encode("Utf-8"))
                    elif action == 'get messages to user':
                        mails = self.db.mails_to_user(data[3:])
                        for i in mails:
                            print(i, '1')
                            user.send('%%'.join(i).encode("utf-8"))
                        user.send('404'.encode("utf-8"))
                    elif action == 'get messages from user':
                        mails = self.db.mails_from_user(data[3:])
                        for i in mails:
                            print(i)
                            user.send('%%'.join(i).encode("utf-8"))
                        user.send('404'.encode("utf-8"))
                    elif action == 'delete mail':
                        print(data)
                        print('got delete message')
                        content = data[3:].split('%%')
                        print(content)
                        self.db.delete_mail(*content)
                        print('deleted')
            except Exception as e:
                print(e)

    def start_server(self):
        while True:
            try:
                user_socket, address = self.server.accept()
                print('User connected')
                user_thread = Thread(target=self.listen_user, args=(user_socket,))
                user_thread.start()
            except Exception:
                print('Проблема с подключением юзеров')


server = MailServer()
server.start_server()

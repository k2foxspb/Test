import socket
import sys
import threading
import time
from tkinter import *
from tkinter_app import TK_inter

from var import *


class TK(TK_inter):
    def __init__(self, root):
        super().__init__(root=root, app=M1())


class M1(threading.Thread):

    def __init__(self):
        super().__init__()
        self.conn = None
        self.sock = None
        self.Pack_id = 0
        self.Exchange = 0
        # таймер ожидания данных от М2
        self.timer = 0

    def __str__(self):
        return 'M1'

    def init_socket(self):
        # Готовим сокет
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((IP_ADDRESS, PORT))
        transport.settimeout(0.5)
        self.sock = transport
        self.sock.listen()
        print('Сервер М1 запущен')

    def run(self):
        # Инициализация Сокета
        self.init_socket()
        # Основной цикл программы сервера
        while True:
            try:
                self.conn, addr = self.sock.accept()
            except OSError:
                pass
            else:
                # при соединении выставляем флаг Exchange и запускаем таймер
                print("Установлено соединение с M2", addr)
                self.Exchange = 1
                self.Pack_id = 0
                self.timer = time.time()
                while True:
                    if self.conn and self.Exchange == 1 and time.time() - self.timer < SERVER_INTERVAL:

                        try:
                            time.sleep(1)
                            # получает данные из сокета
                            data_pack = self.conn.recv(B1).decode()
                            # отправляет данные в сокет
                            self.process_client_message(data_pack, self.conn)
                        except:
                            print('соединение разорвано')
                            self.Pack_id = 0
                            self.Exchange = 0
                            sys.exit(0)

    def process_client_message(self, message, client):
        print('Разбор сообщения от М2:', hex(int(message)))
        if EXIT in message:
            client.send(EXIT.encode())
            print('сообщение о завершении работы от М2')
            time.sleep(2)
            self.sock.close()

        elif EXCHANGE in message:
            self.Exchange = 0
            print(f'изменение флага Exchange {self.Exchange}')
        else:
            print('Таймер:', time.time() - self.timer)
            time.sleep(1)
            self.Pack_id += 1
            print(f'пакет c №: {message[2:4]} пришёл от М2, id М1: {self.Pack_id}')
            if self.Pack_id > 10:
                pack_id = self.Pack_id
            else:
                pack_id = '0' + str(self.Pack_id)
            answer = f'{B1}{B2_ANSWER}{pack_id}{message[5:]}'
            client.send(answer.encode())
            print('тело пакета', hex(int(answer)))
            self.timer = time.time()


def main():
    root = Tk()
    TK(root)
    root.mainloop()


if __name__ == '__main__':
    main()

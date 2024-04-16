import socket
import sys
import time
import select

from var import *


class M1:
    def __init__(self):
        self.conn = None
        self.sock = None

        self.Exchange = 0
        # таймер ожидания данных от М2
        self.timer = 0
        self.Pack_id = 0

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
                            data_pack = self.conn.recv(B1).decode()
                            self.process_client_message(data_pack, self.conn)
                        except:
                            print('соединение разорвано')
                            self.Pack_id = 0
                            self.Exchange = 0
                            sys.exit(-1)

    def process_client_message(self, message, client):
        print('Разбор сообщения от М2:', hex(int(message)))
        if message == EXIT:
            print('сообщение о завершении работы от М2')
            sys.exit()
        elif message == EXCHANGE:
            self.Exchange = 0
            print(f'изменение флага Exchange {self.Exchange}')
        else:
            print('Таймер:', time.time() - self.timer)

            self.Pack_id += 1
            print(f'пакет c №: {message[2:4]} пришёл от М2, id М1: {self.Pack_id}')
            if self.Pack_id > 10:
                pack_id = self.Pack_id
            else:
                pack_id = '0' + str(self.Pack_id)
            answer = f'{B1}{B2_ANSWER}{pack_id}{message[5:]}'

            client.send(answer.encode())
            print(answer)
            self.timer = time.time()


def main():
    server = M1()
    server.run()


if __name__ == '__main__':
    main()

import socket
import sys
import time

import serial

from var import *


class M2:
    def __init__(self):
        self.Pack_id = 0
        self.com_port = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_com()
        self.timer = 0
        self.flag = True

    def send_message_to_server(self, pack):
        # Отправляет пакет в сокет.
        self.timer = time.time()
        self.sock.send(pack.encode())
        print(f'Отправлено сообщение на сервер {hex(int(pack))}')

    def send_message_to_com(self, pack):
        # Отправляет пакет в последовательный порт.
        self.com_port.write(pack.encode())
        print('отправлено сообщение на COM порт')

    def get_message_from_server(self):
        # Слушает сокет
        if time.time() - self.timer < M2_INTERVAL:
            out = self.sock.recv(B1).decode()
            print(f'сообщение от сервера: {hex(int(out))} Pack_id M1: {out[3:5]}')
            if out == EXIT:
                self.com_port.write(out.encode())
                self.com_port.close()
                self.flag = False
            return out

        else:
            self.send_message_to_server(EXIT)

    def get_message_from_com(self):
        # слушает последовательный порт.
        if self.com_port.in_waiting > 0:
            request = self.com_port.read(6).decode()
            self.Pack_id += 1
            print(f'сообщение от COM: {hex(int(request))} Pack_id_M3: {request[2:4]}')
            return request

    def run(self):
        # Основной цикл программы. time.sleep() просто для наглядности иллюстрации процесса работы.
        while self.flag:
            try:
                time.sleep(1)
                com_recv = self.get_message_from_com()
                time.sleep(1)
                self.send_message_to_server(com_recv)
                time.sleep(1)
                server_recv = self.get_message_from_server()
                time.sleep(1)
                self.send_message_to_com(server_recv)

            except:
                pass

    def init_com(self):
        """
        Инициализация последовательного порта и сокета.
        После 5 попыток подключения завершает работу
        """

        for i in range(5):
            print(f'Попытка подключения №{i + 1}')
            try:
                self.com_port = serial.Serial('COM9', 9600, timeout=1, bytesize=6)
                self.sock.connect((IP_ADDRESS, PORT))
                print('приложение М2 запущено!')
            except:
                pass
            else:
                break
            time.sleep(1)
            if i > 3:
                sys.exit(-1)


def main():
    module = M2()
    module.run()


if __name__ == '__main__':
    main()

import sys
import threading
import time
import serial
from tkinter import ttk
from tkinter import *

from tkinter_app import TK_inter
from var import *


class TK(TK_inter):
    def __init__(self, root):
        super().__init__(root=root, app=M3())

    def get(self):
        pack_id = ttk.Label(self.mainframe)
        pack_id["text"] = self.app.Pack_id
        pack_id.grid(column=2, row=1)
        self.root.after(2000, self.get)


class M3(threading.Thread):
    def __init__(self):
        super().__init__()
        self.com_port = None
        self.Pack_id = 0
        self.init_com()

    def __str__(self):
        return 'M3'

    def send_data(self, data):
        # Отправляет пакет в М2
        self.Pack_id += 1

        if data == EXIT:
            self.com_port.write(EXIT.encode())
        elif data == EXCHANGE:
            self.com_port.write(EXCHANGE.encode())
        else:
            if data < 16:
                data = '0' + str(data)
            if self.Pack_id < 10:
                str_pack = '0' + str(self.Pack_id)
            else:
                str_pack = self.Pack_id
            try:
                data_pack = self.com_port.write(f'{B1}{B2_WRITE}{str_pack}{data}'.encode())
                print(f'отправлено сообщение:', hex(int(f'{B1}{B2_WRITE}{str_pack}{data}')).encode())
                print(f'длинна пакета: {data_pack} bytes')
            except:
                sys.exit()

    def run(self):
        """
        Основной цикл программы. Вызывает функцию отправки пакета в М2 и слушает СОМ порт

        """
        while True:
            for i in range(1, 100):
                data_pack = i
                self.send_data(data_pack)
                time.sleep(6)
                if self.com_port.inWaiting() > 0:
                    out = self.com_port.read(B1).decode()
                    if out == EXIT:
                        print('COM port закрыт')
                        self.com_port.close()
                        sys.exit()
                    print('Сообщение от М2', hex(int(out)))
                else:
                    self.com_port.close()

    def init_com(self):
        # Инициализация последовательного порта
        try:
            self.com_port = serial.Serial(COM_PORT_1, 9600, timeout=1, bytesize=6)
            print('приложение М3 запущено')
        except OSError:
            print('не удалось подключиться к COM-порту')


def main():
    root = Tk()
    TK(root)
    root.mainloop()


if __name__ == "__main__":
    main()

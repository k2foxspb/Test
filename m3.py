import sys
import time
import serial
from var import *


class M3:
    def __init__(self):
        self.com_port = None
        self.Pack_id = 0
        self.init_com()

    def send_data(self):
        # Отправляет пакет в М2
        self.Pack_id += 1
        data = input('введите данные')
        if data == EXIT:
            self.com_port.write(EXIT.encode())
        elif data == EXCHANGE:
            self.com_port.write(EXCHANGE.encode())
        else:
            if int(data) < 16:
                data = '0' + str(data)
            if self.Pack_id < 10:
                str_pack = '0' + str(self.Pack_id)
            else:
                str_pack = self.Pack_id
            data_pack = self.com_port.write(f'{B1}{B2_WRITE}{str_pack}{data}'.encode())
            print(f'отправлено сообщение:', hex(int(f'{B1}{B2_WRITE}{str_pack}{data}')).encode())
            print(f'длинна пакета: {data_pack} bytes')

    def run(self):
        """
        Основной цикл программы. Вызывает функцию отправки пакета в М2 и слушает СОМ порт

        """
        while True:
            self.send_data()
            time.sleep(6)
            if self.com_port.inWaiting() > 0:
                out = self.com_port.read(B1).decode()
                if out == EXIT:
                    print('COM port закрыт')
                    self.com_port.close()
                    sys.exit()
                print('Сообщение от М2', hex(int(out)))

    def init_com(self):
        # Инициализация последовательного порта
        try:
            self.com_port = serial.Serial('COM8', 9600, timeout=1, bytesize=6)
            print('приложение М3 запущено')
        except OSError:
            print('не удалось подключиться к COM-порту')


def main():
    x = M3()
    x.run()


if __name__ == "__main__":
    main()

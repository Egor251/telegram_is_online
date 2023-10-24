from create_db import DB
import telethon
import asyncio
import datetime
import configparser
import os.path
import time
import sys


class TelegramInfo:

    def __init__(self):  # цепляем конфиг, если нет - создаём
        if not os.path.exists(self.config_path):  # проверяем существует ли файл
            with open(self.config_path, 'w') as config_file:
                self.config.add_section('Settings')
                self.config.set('Settings', 'api_id', '1')
                self.config.set('Settings', 'api_hash', '')
                self.config.write(config_file)  # если не существует - создаём
        self.config.read(self.config_path)  # читаем файл
        self.api_id = self.config.getint('Settings', 'api_id')  # api_id от telegram получать по ссылке my.telegram.org
        self.api_hash = self.config.get('Settings', 'api_hash')  # api_hash от telegram получать по ссылке my.telegram.org
        if self.api_id == 1 or self.api_hash == '':
            print('Enter correct api_id and api_hash in tg_config.ini!')
            print()
            time.sleep(1)
            print('Program is finishing....')
            time.sleep(2)
            sys.exit()

    config = configparser.ConfigParser()  # экземпляр класса конфигпарсера
    api_id = 1  # api_id от telegram получать по ссылке my.telegram.org
    api_hash = ''  # api_hash от telegram получать по ссылке my.telegram.org
    check_every_second = 60  # дефолтное значение раз в сколько секунд проводить проверку
    config_path = 'tg_config.ini'  # имя конфиг файла

    async def is_online(self, chat_peer):  # функция раз в определённое время проверяет статус пользователя

        while True:  # бесконечный цикл
            start_time = time.time()  # время начала цикла, нужно для стабилизации промежутка между запросами
            async with telethon.TelegramClient('anon', self.api_id, self.api_hash) as client:  # создаём сессию подключаясь к api
                if telethon.events.userupdate.UserUpdate(client=client, chat_peer=chat_peer, online=True):  # сама проверка на онлайн статус пользователя
                    DB().insert([chat_peer, datetime.date, datetime.time])  # Если пользователь онлайн - заносим запись в БД
                    print(datetime.time, ": ", chat_peer, ' - online')
                end_time = time.time()  # время окончания цикла
                total_time = start_time-end_time  # суммарное время работы
                if total_time < self.check_every_second:  # если цикл проработал дольше, чем необходимый перерыв между запросами, то будет ошибка
                    await asyncio.sleep(self.check_every_second-(start_time-end_time))
                else:
                    await asyncio.sleep(1)


if __name__ == '__main__':
    TelegramInfo()

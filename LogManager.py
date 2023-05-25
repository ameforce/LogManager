from datetime import datetime
import os


class LogManager:
    def __init__(self, log_level: int = 0, content: str = '', is_print_console: bool = True):
        self.__log_level = log_level
        self.__log_level = self.__refine_level()
        self.__content = content
        self.__is_print_console = is_print_console

    def __refine_level(self) -> str:
        if self.__log_level == 0:
            return 'INFO'
        elif self.__log_level == 1:
            return 'WARNING'
        elif self.__log_level == 2:
            return 'ERROR'
        elif self.__log_level == 3:
            return 'CRITICAL'
        else:
            return 'UNDEFINED'

    def update(self, log_level: int, content: str):
        self.__log_level = log_level
        self.__log_level = self.__refine_level()
        self.__content = content

    def log(self):
        msg = f'[{datetime.now()}] {self.__log_level}: {self.__content}'
        if self.__is_print_console:
            print(msg)
        else:
            if not os.path.exists('./Log'):
                os.mkdir('./Log')
            while not os.path.exists('./Log'):
                continue
            with open(f'./Log/{datetime.year}-{datetime.month}-{datetime.day}', 'a') as f:
                f.write(msg)

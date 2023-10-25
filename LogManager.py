from termcolor import colored
from datetime import datetime
import os


class LogManager:
    def __init__(self, default_log_level: int or str = 0, is_print_console: bool = True,
                 real_time_mode: bool = False, color_mode: bool = True):
        self.__default_log_level = self.__refine_level(default_log_level)
        self.__is_print_console = is_print_console
        self.__real_time_mode = real_time_mode
        self.__color_mode = color_mode
        self.__saved_content = ''

    @staticmethod
    def __refine_level(log_level: int or str) -> str:
        if type(log_level) is int:
            if log_level == 0:
                return 'INFO'
            elif log_level == 1:
                return 'WARNING'
            elif log_level == 2:
                return 'ERROR'
            elif log_level == 3:
                return 'CRITICAL'
            else:
                return 'UNDEFINED'
        else:
            if log_level != "INFO" and log_level != "WARNING" and log_level != "ERROR" and log_level != "CRITICAL":
                return 'UNDEFINED'
            return log_level

    def update(self, default_log_level: int or str or None = None, is_print_console: bool or None = None,
               real_time_mode: bool or None = None, color_mode: bool or None = None):
        if default_log_level is not None:
            self.__default_log_level = self.__refine_level(default_log_level)
        if is_print_console is not None:
            self.__is_print_console = is_print_console
        if real_time_mode is not None:
            self.__real_time_mode = real_time_mode
        if color_mode is not None:
            self.__color_mode = color_mode
        return

    @staticmethod
    def __refine_color_content(content: str, log_level: str) -> str:
        level_color_dict = {'green': [], 'orange': ['WARNING'], 'red': ['ERROR', 'CRITICAL']}
        keyword_color_dict = {'green': ['Success'], 'orange': [], 'red': ['Failure']}
        for level_color in level_color_dict:
            for level in level_color_dict[level_color]:
                if log_level == level:
                    content = colored(content, level_color)
                    return content
        for keyword_color in keyword_color_dict:
            for keyword in keyword_color_dict[keyword_color]:
                if content in keyword:
                    content = content.replace(keyword, colored(keyword, keyword_color))
        return content

    def log(self, content: str, log_level: int or str = None):
        if log_level is None:
            log_level = self.__default_log_level
        else:
            log_level = self.__refine_level(log_level)

        if self.__color_mode:
            content = self.__refine_color_content(content, log_level)

        if self.__saved_content == '':
            content = f'[{datetime.now()}] {log_level}: {content}'
        else:
            content = f'{content}'

        if self.__real_time_mode and self.__saved_content != '':
            content = self.__saved_content + content

        if self.__is_print_console:
            if self.__real_time_mode and self.__saved_content == '':
                print(content, end='\r')
            else:
                print(content)
        else:
            if not os.path.exists('./Log'):
                os.mkdir('./Log')
            while not os.path.exists('./Log'):
                continue
            with open(f'./Log/{datetime.year}-{datetime.month}-{datetime.day}', 'a') as f:
                f.write(content)

        if self.__real_time_mode:
            if self.__saved_content == '':
                self.__saved_content = content
            else:
                self.__saved_content = ''

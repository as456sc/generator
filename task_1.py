import os
import datetime


import hashlib
from datetime import datetime

LOGFILE = 'log_file.txt'


def file_logger(function):
    def _func(*args, **kwargs):
        print(datetime.now())
        result = function(*args, **kwargs)
        return result

    return _func


def logger(logfile):
    def logger_one(function):
        def _func(*args, **kwargs):
            nonlocal logfile
            now = datetime.now()
            with open(logfile, 'a', encoding='utf-8') as log:
                log.write(f'Вызов функции {function.__name__}, время - {now}\n')
            result = function(*args, **kwargs)
            return result

        return _func

    return logger_one



# @logger(LOGFILE)
# def md5gen(file):
#     with open(file, 'r', encoding='utf-8') as f:
#         for line in f:
#             yield hashlib.md5(line.strip().encode('utf-8')).hexdigest()






def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()

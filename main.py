import sys
import time
import schedule

from prepare_sent import prepare_and_sent

# количество аргументов запускаемого скрипта
ARGS_COUNT = 3


def main():
    """

    sys.argv[0]: Аргумент командной строки, по умолчанию путь к скрипту main.py
    sys.argv[1]: Аргумент командной строки, строковое значение email-а админа
    sys.argv[2]: Аргумент командной строки, строковое значение api-токена админа
    :return:
    """
    if sys.argv.__len__() == ARGS_COUNT:
        email = sys.argv[1]
        api_token = sys.argv[2]
        prepare_and_sent(email, api_token)
    else:
        print(
            'Введите три аргумента: \n - путь к запускаемому файлу (main.py) \n - email админа Омнидеск'
            '\n - api-токен админа')


if __name__ == '__main__':
    main()

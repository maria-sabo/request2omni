import sys
from prepare_sent import prepare_and_sent
from request import check_credentials_correct

# количество аргументов запускаемого скрипта
ARGS_COUNT = 4


def main():
    """
    Главная функция

    sys.argv[0]: Аргумент командной строки, по умолчанию путь к скрипту main.py
    sys.argv[1]: Аргумент командной строки, строковое значение email-а админа
    sys.argv[2]: Аргумент командной строки, строковое значение api-токена админа
    sys.argv[3]: Аргумент командной строки, строковое значение поддомента в Омнидеск (например, hr-link)
    :return:
    """
    if sys.argv.__len__() == ARGS_COUNT:
        email = sys.argv[1]
        api_token = sys.argv[2]
        subdomain = sys.argv[3]
        if check_credentials_correct(email, api_token, subdomain):
            prepare_and_sent(email, api_token, subdomain)
    else:
        print(
            'Введите четыре аргумента: \n - путь к запускаемому файлу (main.py) \n - email админа Омнидеск'
            '\n - api-токен админа \n - поддомен в Омнидеск')


if __name__ == '__main__':
    main()

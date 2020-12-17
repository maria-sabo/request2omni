import requests
# тикет успешно отправлен в Омнидеск
POSITIVE_STATUS_CODE = 201

# некорректный логин пользователя в Омнидеск
INVALID_LOGIN_USER_STATUS_CODE = 403

# некорректный api-токен клиента в Омнидеск
INVALID_API_TOKEN_STATUS_CODE = 401

# ошибка
INVALID_STATUS_CODE = 404


def check_credentials_correct(email, api_token, subdomain):
    """
    Функция проверяет переданные данные -- email, api_token, subdomain
    Если они некорректны, то печатаются ошибки и возвращается False
    Иначе True

    :param email: email админа Омнидеск
    :param api_token: api-token админа Омнидеск
    :param subdomain: Поддомен в Омнидеск
    :return: True/False
    """
    try:
        response = requests.get('https://' + subdomain + '.omnidesk.ru/api/1',
                                auth=(email, api_token))

        if response.status_code == INVALID_LOGIN_USER_STATUS_CODE:
            print('Введен некорректный логин админа Омнидеск')
            return False
        elif response.status_code == INVALID_API_TOKEN_STATUS_CODE:
            print('Введен некорректный api-токен админа Омнидеск')
            return False
        elif response.status_code == INVALID_STATUS_CODE:
            print('Что-то пошло не так. Проверьте введенный поддомен')
            return False
        else:
            return True
    except:
        print('Произошла ошибка.')


def send_request(name, request_date, email, api_token, subdomain):
    """
    Функция отправляет POST-запрос в Омнидеск
    То есть в кабинет админа поступает сообщение о новой заявке
    Возвращает True -- сообщение успешно отправлено, False -- что-то пошло не так


    :param name: Строковое значение, имя сотрудника для которого создана заявка на УНЭП
    :param request_date: Строковое значение, дата создания заявки
    :param email: email админа Омнидеск
    :param api_token: api-token админа Омнидеск
    :param subdomain: Поддомен в Омнидеск
    :return: True/False
    """
    data_for_omni = {
        "case": {
            "user_email": "maria_sabo@rambler.ru",
            "user_full_name": "Maria Sabo",
            "subject": "Заявка на выпуск УНЭП",
            "content": "Появилась заявка на выпуск УНЭП" + "\n\n" "УНЭП для сотрудника: " + name + "\n" "Дата заявки: "
                       + request_date,
        }
    }
    try:
        response = requests.post('https://' + subdomain + '.omnidesk.ru/api/cases.json',
                                 auth=(email, api_token),
                                 json=data_for_omni)
        if response.status_code == POSITIVE_STATUS_CODE:
            print('Тикет отправлен в Омнидеск.')
            return True
        else:
            print('Ошибка: ' + str(response.content))
            return False
    except:
        print('Произошла ошибка.')
        return False

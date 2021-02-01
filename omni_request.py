import datetime
import logging
import datetime as dt

import requests

# тикет успешно отправлен в Омнидеск
import config

POSITIVE_STATUS_CODE = 201

# запрос выполнен успешно
POSITIVE_STATUS_CODE_200 = 200

# некорректный логин пользователя в Омнидеск
INVALID_LOGIN_USER_STATUS_CODE = 403

# некорректный api-токен клиента в Омнидеск
INVALID_API_TOKEN_STATUS_CODE = 401

# ошибка
INVALID_STATUS_CODE = 404


def send_request(data2omni, email, api_token, subdomain):
    """
    Функция отправляет POST-запрос в Омнидеск.
    То есть в кабинет админа поступает сообщение о новой заявке.
    Возвращает True -- сообщение успешно отправлено, False -- что-то пошло не так.

    :param person_email:
    :param name: Строковое значение, имя сотрудника для которого создана заявка на УНЭП
    :param request_date: Строковое значение, дата создания заявки
    :param email: email админа Омнидеск
    :param api_token: api-token админа Омнидеск
    :param subdomain: Поддомен в Омнидеск
    :return: True/False
    """
    data_for_omni = {
        "case": {
            "user_email": config.user_email_omni,
            "user_full_name": config.user_full_name_omni,
            "subject": "Заявка на выпуск УНЭП " + data2omni.person_name,
            "content": "Появилась заявка на выпуск УНЭП." + "\n\n" "УНЭП для сотрудника: " + data2omni.person_name +
                       "\n" "Дата заявки: " + data2omni.issue_request_date +
                       "\n\n" + "Номер телефона сотрудика: " + data2omni.person_phone +
                       "\n" + "Почтовый адрес сотрудика: " + data2omni.person_email +
                       "\n" + "Юрлицо сотрудника: " + data2omni.legal_entity_name +
                       "\n" + "Сотрудник входит в клиент: " + data2omni.client_name +
                       "\n\n" + "Нажал \"Выпустить подпись\": " + data2omni.hr_name +
                       "\n" + "Номер телефона того, кто нажал \"Выпустить подпись\" : " + data2omni.hr_phone +
                       "\n" + "Почтовый адрес того, кто нажал \"Выпустить подпись\": " + data2omni.hr_email,
        }
    }
    response = requests.post('https://' + subdomain + '.omnidesk.ru/api/cases.json',
                             auth=(email, api_token),
                             json=data_for_omni)

    logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='INFO: ' + str(dt.datetime.now()) + '%(message)s')

    if response.status_code == POSITIVE_STATUS_CODE:
        logging.info(' Тикет УНЭП(' + data2omni.person_name + ') отправлен в Омнидеск.')
        print(str(datetime.datetime.now()) + ' Тикет УНЭП(' + data2omni.person_name + ') отправлен в Омнидеск.')
        return True
    elif response.status_code == INVALID_LOGIN_USER_STATUS_CODE:
        logging.info(str(datetime.datetime.now()) + ' Тикет УНЭП(' + data2omni.person_name + ') отправлен в Омнидеск.')
        print('Введен некорректный логин админа Омнидеск.')
        return False
    elif response.status_code == INVALID_API_TOKEN_STATUS_CODE:
        print('Введен некорректный api-токен админа Омнидеск.')
        return False
    elif response.status_code == INVALID_STATUS_CODE:
        print('Что-то пошло не так. Проверьте введенный поддомен.')
        return False
    else:
        print('Ошибка: ' + str(response.content))
        return False

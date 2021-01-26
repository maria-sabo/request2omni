from omni_request import send_request
from db_request import request_new_issues_from_db


def prepare_and_send(email, api_token, subdomain):
    """
    Функция берет данные о новый заявках из БД (читает последнюю записанную в файл дату,
    и берет заявки, пришедшие после этой даты).

    Происходит цикл по записям, полученным в результате запроса к БД:
        Из каждой записи берется имя сотрудника, которому выпускается УНЭП, дата заявки.
        С этими данными вызывается функция send_request(), которая отправит сообщение в Омнидеск.
        Если сообщение успешно отправлено, то дата этой заявки перезаписывается в файл.

    :param email: email админа Омнидеск
    :param api_token: api-token админа Омнидеск
    :param subdomain: Поддомен в Омнидеск
    :return:
    """
    rows = request_new_issues_from_db()
    if rows:
        for row in rows:
            name = row[2]['Фамилия'] + ' ' + row[2]['Имя'] + ' ' + row[2]['Отчество']
            created_date = row[1].strftime("%m/%d/%Y, %H:%M:%S")

            isSent = send_request(name, created_date, email, api_token, subdomain)
            if isSent:
                with open('last_nqes_date.txt', 'w') as f:
                    f.write(str(row[1]))
            else:
                break


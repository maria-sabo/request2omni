from data2omni import Data2Omni
from omni_request import send_request
from db_request import request_new_issues_from_db, request_logins_from_db_ekd_id, request_hr_from_db_ekd_id, \
    request_userId_by_personId_from_db_ekd_id, request_data_from_db_ekd_ekd


def prepare_and_send(email, api_token, subdomain):
    """
    Функция берет данные о новый заявках из БД (читает последнюю записанную в файл дату,
    и берет заявки, пришедшие после этой даты).

    Происходит цикл по записям, полученным в результате запроса к БД:
        Из каждой записи берется имя сотрудника, которому выпускается УНЭП, дата заявки.
        Также вызываются запросы к базам данных и берутся данные о сотруднике и кадровике для отправк в Омнидеск.
        Данные хранятся в экземпляре класса Data2Omni.

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
            data2omni = Data2Omni()
            data2omni.person_name = row[3]['Фамилия'] + ' ' + row[3]['Имя'] + ' ' + row[3]['Отчество']
            data2omni.issue_request_date = row[2].strftime("%d.%m.%Y в %H:%M:%S")

            data2omni.person_email = 'Отсутствует на портале'
            data2omni.person_phone = 'Отсутствует на портале'
            logins = request_logins_from_db_ekd_id(row[0])
            for login in logins:
                if login[1] == 'EMAIL':
                    data2omni.person_email = login[2]
                elif login[1] == 'PHONE':
                    data2omni.person_phone = login[2]

            data2omni.hr_email = 'Отсутствует на портале'
            data2omni.hr_phone = 'Отсутствует на портале'
            hr_data = request_hr_from_db_ekd_id(row[1])

            data2omni.hr_name = hr_data[0][0]
            if data2omni.hr_name == '  ':
                data2omni.hr_name = 'Создатель пространства'

            for data in hr_data:
                if data[1] == 'EMAIL':
                    data2omni.hr_email = data[2]
                elif data[1] == 'PHONE':
                    data2omni.hr_phone = data[2]

            user_id = request_userId_by_personId_from_db_ekd_id(row[0])
            response = request_data_from_db_ekd_ekd(user_id[0])
            data2omni.client_name = response[0][0]
            data2omni.legal_entity_name = response[1][0]

            isSent = send_request(data2omni, email, api_token, subdomain)
            if isSent:
                with open('last_nqes_date.txt', 'w') as f:
                    f.write(str(row[2]))
            else:
                break

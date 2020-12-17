from request import send_request
from get_from_db import get_from_db


def prepare_and_sent(email, api_token, subdomain):
    """
    Функция берет данные о заявках из БД
    Если идентификатор заявки есть в файле, то это означает, что извещение уже было отправлено
    Иначе если идентификатора нет в файле, то
        Из записи, полученной из БД, берется имя сотрудника, дата заявки
        С этими данными вызывается функция send_request(), которая отправит сообщение в Омнидеск
        Если сообщение успешно отправлено, то идентификатор этой заявки записывается в файл

    :param email: email админа Омнидеск
    :param api_token: api-token админа Омнидеск
    :param subdomain: Поддомен в Омнидеск
    :return:
    """
    rows = get_from_db()
    try:
        file_write = open('request_ids.txt', 'a+')
        for row in rows:
            request_id = row[0]
            file_read = open('request_ids.txt', 'r')
            if request_id not in file_read.read():
                name = row[2]['Фамилия'] + ' ' + row[2]['Имя'] + ' ' + row[2]['Отчество']
                created_date = row[1].strftime("%m/%d/%Y, %H:%M:%S")

                send = send_request(name, created_date, email, api_token, subdomain)
                if not send:
                    break
                file_write.write(request_id)
                file_write.write('\n')
            else:
                print('Извещение о заявке УНЭП уже было направлено в Омнидеск.')
    except:
        print('Ошибка.')

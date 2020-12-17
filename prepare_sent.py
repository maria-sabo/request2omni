from request import send_request
from get_from_db import get_from_db


def prepare_and_sent(email, api_token):
    rows = get_from_db()
    try:
        file_write = open('request_ids.txt', 'a+')
        for row in rows:
            request_id = row[0]
            file_read = open('request_ids.txt', 'r')
            if request_id not in file_read.read():
                name = row[2]['Фамилия'] + ' ' + row[2]['Имя'] + ' ' + row[2]['Отчество']
                # created_date = (row[1] + timedelta(hours=3)).strftime("%m/%d/%Y, %H:%M:%S")
                created_date = row[1].strftime("%m/%d/%Y, %H:%M:%S")

                file_write.write(request_id)
                file_write.write('\n')
                # file_write.close()
                send_request(name, created_date, email, api_token)
            else:
                print('Извещение о заявке УНЭП уже было направлено в Омнидеск.')
            #file_write.close()
    except:
        print('Ошибка.')
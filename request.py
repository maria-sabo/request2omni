import requests

POSITIVE_STATUS_CODE = 201


def send_request(name, request_date, email, api_token):
    data_for_omni = {
        "case": {
            "user_email": "maria_sabo@rambler.ru",
            "user_full_name": "Maria Sabo",
            "subject": "Заявка на выпуск УНЭП",
            "content": "Появилась заявка на выпуск УНЭП" + "\n\n" "УНЭП для сотрудника: " + name + "\n" "Дата заявки: "
                       + request_date,
        }
    }
    response = requests.post('https://maria991.omnidesk.ru/api/cases.json',
                             auth=(email, api_token),
                             json=data_for_omni)

    if response.status_code == POSITIVE_STATUS_CODE:
        print('Тикет отправлен в Омнидеск.')
    else:
        print('Произошла ошибка.')

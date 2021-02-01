class Data2Omni:
    """
    Экземпляр класса хранит данные о новой заявке для отправки в тикете в Омнидеск.

    person_name: (String) Имя сотрудника, которому выпускается УНЭП
    issue_request_date: (String) Дата, когда была создана заявка
    person_email: (String) Почтовый адрес сотрудника
    person_phone: (String) Номер телефона сотрудника
    client_name: (String) Клиент, в котором создан сотрудник
    legal_entity_name: (String) Юрлицо, в котором создан сотрудник
    hr_name: (String) Имя нажавшего "Выпустить УНЭП"
    hr_email: (String) Почтовый адрес нажавшего "Выпустить УНЭП"
    hr_hr_phone: (String) Номер телефона нажавшего "Выпустить УНЭП"
    """
    person_name = ''
    issue_request_date = ''

    person_email = ''
    person_phone = ''

    client_name = ''
    legal_entity_name = ''

    hr_name = ''
    hr_email = ''
    hr_phone = ''

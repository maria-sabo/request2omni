import datetime as dt
from datetime import datetime

from db_connect import DbConnection


def get_last_nqes_date():
    """
    Функция возвращает дату, записанную в файл last_nqes_date.txt.

    :return:  Дата последней заявки, уведомление о которой, уже было отправлено в Омндеск
    """
    try:
        with open('last_nqes_date.txt') as f:
            first_line = f.readline()
            return first_line.rstrip()
    except FileNotFoundError:
        print('Файл не найден.')


def request_new_issues_from_db():
    """
    Функция подключается к БД ekd_ca.
    Берет записанную в файл дату.
    Если дата является датой,
        то выполняется SQL-запрос, который выбирает записи о заявке УНЭП с кодом 200,
        которые имеют дату создания > записанной в файл.

    :return: Результат SQL-запроса
    Записи, имеющие столбцы:
    1. Идентификатор того, на кого выпускается УНЭП
    2. Идентификатор того, кто нажал "Выпустить УНЭП"
    3. Дата создания заявки на выпуск УНЭП
    4. ФИО сотрудника, для которого создана заявка на выпуск УНЭП
    """
    db_conn = DbConnection("ekd_ca")
    curs = db_conn.curs
    last_nqes_date = get_last_nqes_date()
    try:
        tmp = datetime.strptime(last_nqes_date, "%Y-%m-%d %H:%M:%S.%f")
        db_conn.curs.execute(
            """
            SELECT 
                nqis.person_id,
                nqis.creator_id,
                alog.created_date,
                (request_response::json #> '{event,data,ВладельцыЭП}') -> 0 -> 'ФИО'
            FROM ekd_ca.public.astral_platform_event_log as alog
            LEFT JOIN 
                ekd_ca.public.nqes_issue_request as nqis 
            ON alog.id = nqis.request_event_id
            WHERE event_type like 'USIG_REG_REQUEST'
                AND event_direction like 'OUTBOUND'
                AND request_response::json ->> 'status' like '200'
                AND alog.created_date > %s
            ORDER BY created_date;
            """,
            (last_nqes_date,))
        db_response = curs.fetchall()
        if db_response:
            return db_response
        else:
            print(str(dt.datetime.now()) +
                  ' Все уведомления о новых заявках с текущей даты ' +
                  last_nqes_date +
                  ', записанной в файл last_nqes_date.txt, уже были отправлены в Омнидеск.')
    except ValueError:
        print('Введите корректную дату последней заявки в файл last_nqes_date.txt. '
              'Формат даты: YYYY-mm-dd HH:MM:SS.ffffff.')


def request_logins_from_db_ekd_id(person_id):
    """
    Функция подключается к БД ekd_id.
    Выполняется SQL-запрос, который выбирает email и phone сотрудника, которому выпускается УНЭП.

    :param person_id: Идентификатор сотрудника, которому выпускается УНЭП
    :return: Результат SQL-запроса
    Записи, имеющие столбцы:
    1. Идентификатор того, на кого выпускается УНЭП (user_id)
    2. Тип логина (EMAIL/PHONE)
    3. Логин
    """
    db_conn = DbConnection("ekd_id")
    curs = db_conn.conn.cursor()
    curs.execute(
        """
        SELECT
            user_login.user_id,
            user_login.login_type,
            user_login.login
        FROM user_login
        JOIN (SELECT
                user_id
            FROM ekd_id.public.person
            WHERE id = %s) sel1
        ON user_login.user_id = sel1.user_id;
        """,
        (person_id,))
    db_response = curs.fetchall()
    if db_response:
        return db_response


def request_hr_from_db_ekd_id(creator_id):
    """
    Функция подключается к БД ekd_id.
    Выполняется SQL-запрос, который выбирает ФИО, тип логина, логин сотрудника, который нажал "Выпустить подпись".

    :param creator_id: Идентификатор того, кто нажал "Выпустить подпись"
    :return: Результат SQL-запроса
    Записи, имеющие столбцы:
    1. ФИО сотрудника, который нажал "Выпустить подпись"
    2. Тип логина (EMAIL/PHONE)
    3. Логин
    """
    db_conn = DbConnection("ekd_id")
    curs = db_conn.conn.cursor()

    curs.execute(
        """
        WITH t1 AS (SELECT user_id, last_name, first_name, patronymic
                    FROM person
                    WHERE id in (SELECT id FROM person WHERE user_id = %s)),
        t2 AS (SELECT 
                user_login.user_id,
                user_login.login_type,
                user_login.login
                FROM user_login
                JOIN (SELECT id
                    FROM ekd_id.public.user
                    WHERE id = %s) sel1
                ON user_login.user_id = sel1.id)
        SELECT concat(t1.last_name::text, ' ', t1.first_name::text, ' ', t1.patronymic::text) as name, t2.login_type, t2.login
        FROM t1
        JOIN t2 
        ON t1.user_id = t2.user_id
        """,
        (creator_id, creator_id,))
    db_response = curs.fetchall()
    if db_response:
        return db_response


def request_userId_by_personId_from_db_ekd_id(person_id):
    """
    Функция подключается к БД ekd_id.
    Выполняется SQL-запрос, который по заданному person_id возвращает user_id.

    :param person_id: Идентификатор, которому выпускается УНЭП
    :return: Результат SQL-запроса
    Записи, имеющие столбцы:
    1. Идентификатор user_id
    """
    db_conn = DbConnection("ekd_id")
    curs = db_conn.conn.cursor()

    curs.execute(
        """
        SELECT 
            user_id 
        FROM person 
        WHERE id = %s
        """,
        (person_id,))
    db_response = curs.fetchall()
    if db_response:
        return db_response
    else:
        print('kdk')


def request_data_from_db_ekd_ekd(user_id):
    """
    Функция подключается к БД ekd_ekd.
    Выполняется SQL-запрос, который по заданному user_id возвращает название клиента и юрлицо, в котором создан сотрудник.

    :param user_id: Идентификатор пользователя
    :return: Результат SQL-запроса
    Записи, имеющие столбцы:
    1. Название клиента, в котором создан сотрудник
    2. Название юрлица, в котором создан сотрудник
    """
    db_conn = DbConnection("ekd_ekd")
    curs = db_conn.conn.cursor()

    curs.execute(
        """
        SELECT name
        FROM client
        WHERE id in (SELECT client_id
                    FROM client_user
                    WHERE user_id = %s)
        UNION ALL
        SELECT short_name
        FROM legal_entity
        WHERE id in (SELECT legal_entity_id
                    FROM employee
                    WHERE client_user_id in (SELECT id
                                            FROM client_user
                                            WHERE user_id = %s))
        """,
        (user_id, user_id,))
    db_response = curs.fetchall()
    if db_response:
        return db_response

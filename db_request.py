import psycopg2
from sshtunnel import SSHTunnelForwarder
import config
import psycopg2.extensions
from datetime import datetime


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
    Функция подключается через SSH к БД.
    Берет записанную в файл дату.
    Если дата является датой,
        то выполняется SQL-запрос, который выбирает записи о заявке УНЭП с кодом 200,
        которые имеют дату создания > записанной в файл.


    :return: Результат SQL-запроса (Записи, имеющие столбцы "идентификатор ", "дата создания заявки УНЭП",
    "ФИО сотрудника, для которого создана заявка на УНЭП")
    """
    with SSHTunnelForwarder(
            (config.ssh_host_url, config.ssh_port),
            ssh_private_key=config.ssh_path_to_key,
            ssh_username=config.ssh_username,
            remote_bind_address=('localhost', config.postgres_port),
            local_bind_address=('localhost', config.ssh_port)) as server:
        server.start()

        conn = psycopg2.connect(**config.foreign_db_params)
        curs = conn.cursor()
        last_nqes_date = get_last_nqes_date()
        try:
            tmp = datetime.strptime(last_nqes_date, "%Y-%m-%d %H:%M:%S.%f")
            curs.execute(
                "SELECT id, created_date, (request_response::json #> '{event,data,ВладельцыЭП}') -> 0 "
                "-> 'ФИО' "
                "FROM ekd_ca.public.astral_platform_event_log "
                "WHERE event_type like 'USIG_REG_REQUEST' "
                "AND event_direction like 'OUTBOUND'"
                "AND request_response::json ->> 'status' like '200'"
                "AND created_date > %s"
                "ORDER BY created_date"
                , (last_nqes_date,))
            db_response = curs.fetchall()
            if db_response:
                return db_response
            else:
                print('Все уведомления о новых заявках с текущей даты ' + last_nqes_date + ', записанной в файл last_nqes_date.txt, '
                      'уже были отправлены в Омнидеск.')
        except ValueError:
            print('Введите корректную дату последней заявки в файл last_nqes_date.txt. '
                  'Формат даты: YYYY-mm-dd HH:MM:SS.ffffff.')

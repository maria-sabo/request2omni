from datetime import timedelta

import psycopg2
from sshtunnel import SSHTunnelForwarder
import config
from get_last_id import get_last_id
from request import send_request


def get_from_db():
    with SSHTunnelForwarder(
            (config.ssh_host_url, config.ssh_port),
            ssh_private_key=config.ssh_path_to_key,
            ssh_username=config.ssh_username,
            remote_bind_address=('localhost', config.postgres_port),
            local_bind_address=('localhost', config.ssh_port)) as server:
        server.start()

        conn = psycopg2.connect(**config.foreign_db_params)
        curs = conn.cursor()
        last_id = get_last_id()
        if last_id:
            curs.execute(
                "SELECT id, created_date, (request_response::json #> '{event,data,ВладельцыЭП}') -> 0 -> 'ФИО' "
                "FROM ekd_ca.public.astral_platform_event_log "
                "WHERE event_type like 'USIG_REG_REQUEST' "
                "AND event_direction like 'OUTBOUND'"
                "AND request_response::json ->> 'status' like '200'"
                "AND created_date >= "
                "(SELECT created_date FROM ekd_ca.public.astral_platform_event_log WHERE id = %s)"
                "ORDER BY created_date", (last_id, ))
            return curs.fetchall()
        else:
            curs.execute(
                "SELECT id, created_date, (request_response::json #> '{event,data,ВладельцыЭП}') -> 0 -> 'ФИО' "
                "FROM ekd_ca.public.astral_platform_event_log "
                "WHERE event_type like 'USIG_REG_REQUEST' "
                "AND event_direction like 'OUTBOUND'"
                "AND request_response::json ->> 'status' like '200'"
                "ORDER BY created_date")
            return curs.fetchall()


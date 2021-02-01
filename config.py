ssh_host_url = "host_url"
ssh_path_to_key = "path_to_key"
ssh_username = "user_name"
ssh_port =

postgres_port = 5432


def foreign_db_params(db_name):
    foreign_db_params_ = {
        'dbname': db_name,
        'user': "user_name",
        'password': "db_password",
        'host': 'localhost',
        'port':
    }
    return foreign_db_params_


# настройки для Омнидеск
user_email_omni = ""
user_full_name_omni = ""

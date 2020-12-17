def get_last_id():
    """
    Функция берет последний записанный в файл идентификатор заявки
    Если файл пустой, то возвращает False

    :return:  Идентификатор заявки, либо False
    """
    file_name = 'request_ids.txt'
    f_read = open(file_name, "r")
    num_lines = sum(1 for line in f_read)
    f_read = open(file_name, "r")
    if num_lines > 0:
        last_id = f_read.readlines()[-1]
        return last_id.rstrip()
    else:
        return False

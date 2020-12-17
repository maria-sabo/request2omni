def get_last_id():
    file_name = 'request_ids.txt'
    f_read = open(file_name, "r")
    num_lines = sum(1 for line in f_read)
    f_read = open(file_name, "r")
    if num_lines > 0:
        last_id = f_read.readlines()[-1]
        return last_id[:-1]
    else:
        return False

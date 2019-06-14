import json


def read_token(file_name):
    with open(file_name, 'r') as fd:
        data = json.load(fd)
    return data


def dumps(file_path, data):
    with open(file_path, 'w') as fd:
        json.dump(data, fd)

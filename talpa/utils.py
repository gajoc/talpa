import json


def read_token(file_name):
    with open(file_name, 'r') as fd:
        data = json.load(fd)
    return data

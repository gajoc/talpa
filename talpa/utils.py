import json
import os
import uuid


def read_token(file_name):
    with open(file_name, 'r') as fd:
        data = json.load(fd)
    return data


def dumps(file_path, data, overwrite, extras):
    final_path = str(file_path)

    extras = '' if not extras else extras+'-'

    if not overwrite:
        root, ext = os.path.splitext(file_path)
        final_path = ''.join([root, '-', extras, str(uuid.uuid1()), ext])

    with open(final_path, 'w') as fd:
        json.dump(data, fd)

    return final_path

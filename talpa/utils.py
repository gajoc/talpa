import datetime
import json
import os
import uuid

from marshmallow import fields


def read_token(file_name):
    with open(file_name, 'r') as fd:
        data = json.load(fd)
    return data


read_json = read_token


def dumps(file_path, data, overwrite, extras):
    final_path = str(file_path)

    extras = '' if not extras else extras + '-'

    if not overwrite:
        root, ext = os.path.splitext(file_path)
        final_path = ''.join([root, '-', extras, str(uuid.uuid1()), ext])

    with open(final_path, 'w') as fd:
        json.dump(data, fd)

    return final_path


class CustomDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data):
        if isinstance(value, (datetime.datetime,)):
            return value
        return super()._deserialize(value, attr, data)


class LimitedCounter:

    def __init__(self, limit, msg):
        self.limit = limit
        self.counter = 0
        self.msg = msg

    def __call__(self, *args, **kwargs):
        if self.counter >= self.limit:
            return True
        self.counter += 1
        return False

    def __str__(self):
        return ' '.join([self.msg, str(self.counter)])


class VerboseCounter:

    def __init__(self, msg):
        self.msg = msg
        self.counter = 0

    def __call__(self, *args, **kwargs):
        self.counter += 1

    def __str__(self):
        return ' '.join([self.msg, str(self.counter)])

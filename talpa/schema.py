from marshmallow import Schema, fields, post_dump, ValidationError


def validate_search_mode(value):
    enum = ('REGULAR', 'DESCRIPTIONS', 'CLOSED')
    if value not in enum:
        raise ValidationError(f'search mode must be one of {enum}')


def parse_search_query(data):
    data['category.id'] = data['category_id']
    del data['category_id']

    data['searchMode'] = data['search_mode']
    del data['search_mode']
    return data


class SearchAllegroSchema(Schema):
    category_id = fields.String(required=True)
    phrase = fields.String(required=True)
    search_mode = fields.String(required=True, validate=validate_search_mode)

    @post_dump
    def to_allegro_format(self, data):
        return parse_search_query(data)

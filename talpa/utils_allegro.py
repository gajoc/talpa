from datetime import datetime

from talpa.schema import AllegroMetaDataSchema


def create_meta(query):
    meta = {
        'downloaded_at': datetime.utcnow(),
        'processed_at': None,
        'origin_query': query,
    }

    schema = AllegroMetaDataSchema(strict=True)
    schema.validate(meta)
    return schema.dump(meta).data

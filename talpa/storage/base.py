class BaseCollection:

    def __init__(self, a_collection):
        self._a_collection = a_collection
        self.error_msg = 'collection does not support this operation'

    def __iter__(self):
        return iter(self._a_collection)

    def __len__(self):
        return len(self._a_collection)

    def contains(self, id_) -> bool:
        raise NotImplementedError(self.error_msg)

    def insert(self, item):
        raise NotImplementedError(self.error_msg)

    def remove(self, id_):
        raise NotImplementedError(self.error_msg)

class DatabaseEntityDoesNotExist(Exception):

    def __init__(self, entity_type, reference_id):
        self._entity_type = entity_type
        self._reference_id = reference_id

    @property
    def entity_type(self):
        return self._entity_type

    @property
    def reference_id(self):
        return self._reference_id

    def __str__(self):
        return 'id {} has no entry in as {}'.format(self.reference_id, self.entity_type)

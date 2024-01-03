class Label:

    def __init__(self, uuid, label, source):
        self.uuid = uuid
        self.source = source
        self.label = label

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'source': self.source,
            'label': self.label
        }
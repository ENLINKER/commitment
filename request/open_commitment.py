import json


class OpenCommitment():
    def __init__(self, id, dec_msg):
        self.id = id
        self.dec_msg = dec_msg

    def to_json(self):
        return {
            "id": self.id,
            "dec_msg": self.dec_msg,
        }

    @classmethod
    def from_json(cls, data):
        id = data["id"]
        dec_msg = data["dec_msg"]
        return cls(id, dec_msg)

    def to_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_str(cls, data):
        return cls.from_json(json.loads(data))

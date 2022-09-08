import json


class Post():
    def __init__(self, username, commitment, content):
        self.username = username
        self.commitment = commitment
        self.content = content

    def open_commitment(self, dec_msg):
        self.username = self.commitment.decrypt(dec_msg)

    def to_json(self):
        return {
            "username": self.username,
            "commitment": self.commitment,
            "content": self.content,
        }

    @classmethod
    def from_json(cls, data):
        username = data["username"]
        commitment = data["commitment"]
        content = data["content"]
        return cls(username, commitment, content)

    def to_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_str(cls, data):
        return cls.from_json(json.loads(data))

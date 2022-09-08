from enum import Enum, auto
import json


class RequestType(Enum):
    NEW_POST = auto()
    OPEN_COMMITMENT = auto()
    # GET_POSTS = auto()


class Request():
    def __init__(self, request_type, content):
        self.request_type = request_type
        self.content = content

    def to_json(self):
        return {
            "request_type": self.request_type,
            "content": self.content,
        }

    @classmethod
    def from_json(cls, data):
        request_type = RequestType[data["request_type"]]
        content = data["content"]
        return cls(request_type, content)

    def to_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_str(cls, data):
        return cls.from_json(json.loads(data))

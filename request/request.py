from dataclasses import dataclass
from enum import Enum, auto
import json
from dataclasses_json import dataclass_json


class RequestType(str, Enum):
    # TODO check this part
    NEW_POST = auto()
    OPEN_COMMITMENT = auto()
    # GET_POSTS = auto()


@dataclass_json
@dataclass
class Request():
    type: RequestType
    content: json

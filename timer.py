
from dataclasses import dataclass
import sys
import time
from dataclasses_json import dataclass_json

from utils import get_dict_size, get_list_size, get_object_size


@dataclass_json
@dataclass
class Timer:
    title: str
    start_time: int = 0
    duration: int = 0
    bandwidth: int = 0

    def start(self):
        self.start_time = time.time_ns()

    def end(self):
        self.duration += time.time_ns() - self.start_time

    def add_bandwidth(self, obj):
        self.bandwidth += get_object_size(obj)

    def print(self, round: int = 1):
        t = (self.duration / round) / pow(10, 6)
        b = self.bandwidth // round
        print(f"[{self.title}] {t:.3f} ms, {b} Bytes")

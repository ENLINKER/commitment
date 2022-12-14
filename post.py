from dataclasses import dataclass, field
import sys
from typing import Optional
from hashlib import sha256
from dataclasses_json import dataclass_json

from pyring.one_time import RingSignature, ring_sign, Scalar, ring_verify
from Crypto.Cipher import AES
from uuid import UUID, uuid4


@dataclass_json
@dataclass
class Post:
    message: str
    com: Optional[bytes] = None
    sigma: Optional[RingSignature] = None
    username: Optional[str] = None
    uuid: UUID = field(default_factory=uuid4)

    def __randomname(self, username: str):
        return sha256((self.message + username).encode()).hexdigest()

    def __commit(self, message: str, key: bytes):
        cipher = AES.new(key, AES.MODE_ECB)
        digest = cipher.encrypt(message.encode())
        return digest

    def commit_and_sign(self, username: str, ck: bytes, rpks: list, rsk: Scalar, rsk_index: int):
        randomname = self.__randomname(username)
        self.com = self.__commit(randomname, ck)
        self.sigma = ring_sign(self.message.encode() + self.com, rpks, rsk, rsk_index)

    def verify_sign(self):
        return ring_verify(self.message.encode() + self.com, self.sigma)

    def open(self, username: str, ck: bytes):
        randomname = self.__randomname(username)
        if self.com == self.__commit(randomname, ck):
            self.username = username
            return True
        else:
            return False

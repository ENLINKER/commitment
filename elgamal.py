import json
from random import randrange
from fastecdsa.curve import P256


class ElGamal():
    def __init__(self, c1, c2):
        self.c1, self.c2 = c1, c2

    @classmethod
    def encrypt(cls, pk, m):
        r = randrange(1, P256.q)
        c1 = m + r * pk
        c2 = r * P256.G
        return cls(c1, c2)

    @classmethod
    def gen_decrypt_msg(cls, sk, c2):
        return sk * c2

    def decrypt(self, dec_msg):
        return self.c1 - dec_msg

    def to_json(self):
        return [self.c1, self.c2]

    @classmethod
    def from_json(cls, data):
        c1, c2 = data
        return cls(c1, c2)

    def to_str(self):
        return json.dumps(self.to_json())

    @classmethod
    def from_str(cls, data):
        return cls.from_json(json.loads(data))

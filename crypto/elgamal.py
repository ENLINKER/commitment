import json
from random import randrange
from fastecdsa.curve import P256
from fastecdsa.point import Point
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


def point_encoder(cls: Point):
    return (cls.x, cls.y)


def point_decoder(p):
    return Point(p[0], p[1])


@dataclass_json
@dataclass
class ElGamal:
    c1: Point = field(metadata=config(encoder=point_encoder, decoder=point_decoder))
    c2: Point = field(metadata=config(encoder=point_encoder, decoder=point_decoder))

    @classmethod
    def encrypt(cls, pk: Point, m: Point):
        r = randrange(1, P256.q)
        c1 = m + r * pk
        c2 = r * P256.G
        return cls(c1=c1, c2=c2)

    def decrypt_msg(self, sk: int):
        return sk * self.c2

    def decrypt(self, dec_msg):
        return self.c1 - dec_msg

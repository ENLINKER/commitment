from random import randrange
from fastecdsa.point import Point
from fastecdsa.curve import P256
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config

from crypto.elgamal import point_decoder, point_encoder


@dataclass_json
@dataclass
class SameDLProof:
    grr1: Point = field(metadata=config(encoder=point_encoder, decoder=point_decoder))
    grr2: Point = field(metadata=config(encoder=point_encoder, decoder=point_decoder))
    rrr: int

    @classmethod
    def gen(cls, g1: Point, g2: Point, x: int):
        y1, y2 = g1 * x, g2 * x
        rr = randrange(1, P256.q)
        grr1, grr2 = g1 * rr, g2 * rr

        c = hash((g1.x, g1.y, g2.x, g2.y, y1.x, y1.y, y2.x, y2.y, grr1.x, grr1.y, grr2.x, grr2.y)) % P256.q
        # print(f"gen c = {c}")
        rrr = (rr + (c * x) % P256.q) % P256.q

        assert (g1 * rrr == grr1 + y1 * c)
        assert (g2 * rrr == grr2 + y2 * c)
        return cls(grr1, grr2, rrr)

    def verify(self, g1: Point, g2: Point, y1: Point, y2: Point) -> bool:
        c = hash((g1.x, g1.y, g2.x, g2.y, y1.x, y1.y, y2.x, y2.y,
                 self.grr1.x, self.grr1.y, self.grr2.x, self.grr2.y)) % P256.q
        # print(f"verify c = {c}")
        return (g1 * self.rrr == self.grr1 + y1 * c) and (g2 * self.rrr == self.grr2 + y2 * c)

from dataclasses import dataclass, field
import json
from typing import Optional
from fastecdsa.point import Point

from crypto.elgamal import ElGamal, point_decoder, point_encoder
from dataclasses_json import dataclass_json, config

from post.open_commitment_msg import OpenCommitmentMsg
from fastecdsa.curve import P256
from fastecdsa.keys import gen_private_key, get_public_key, gen_keypair


@dataclass_json
@dataclass
class Post:
    content: str
    id: Optional[int] = field(init=False, default=-1)
    user_pk: Point = field(metadata=config(encoder=point_encoder, decoder=point_decoder))
    commitment: Optional[ElGamal] = None
    anonymous_sk: Optional[int] = field(default=-1, metadata=config(exclude=lambda x: True))

    @ classmethod
    def create(cls, content, user_pk, anonymous=False):
        if anonymous:
            sk, pk = gen_keypair(P256)
            commitment = ElGamal.encrypt(pk, user_pk)
            return cls(content, user_pk=pk, commitment=commitment, anonymous_sk=sk)
        return cls(content, user_pk=user_pk)

    def open(self, open_commitment_msg: OpenCommitmentMsg):
        assert (open_commitment_msg.proof.verify(P256.G, self.commitment.c2, self.user_pk, open_commitment_msg.dec_msg))
        self.user_pk = self.commitment.decrypt(open_commitment_msg.dec_msg)

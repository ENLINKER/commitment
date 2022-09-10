from dataclasses import dataclass, field
from typing import Optional
from fastecdsa.point import Point
from dataclasses_json import dataclass_json, config

from crypto.elgamal import point_decoder, point_encoder
from crypto.same_dl_proof import SameDLProof
from fastecdsa.curve import P256


@dataclass_json
@dataclass
class OpenCommitmentMsg():
    post_id: int
    dec_msg: Optional[Point] = field(metadata=config(encoder=point_encoder, decoder=point_decoder))
    proof: SameDLProof = field()

    @classmethod
    def gen(cls, post):
        post_id = post.id
        dec_msg = post.commitment.decrypt_msg(post.anonymous_sk)
        proof = SameDLProof.gen(P256.G, post.commitment.c2, post.anonymous_sk)
        return OpenCommitmentMsg(post_id, dec_msg, proof)

#!/usr/bin/env python3

import argparse
from dataclasses import dataclass, field
import json
import random
from fastecdsa.keys import gen_private_key, get_public_key, gen_keypair
from fastecdsa.point import Point
from fastecdsa.curve import P256
import socket
import benchmark
from post.open_commitment_msg import OpenCommitmentMsg
from post.post import Post
from request.request import Request, RequestType
import string
import time


@dataclass
class Client:
    host: str
    port: int
    sk: int = field(repr=False, default_factory=lambda: gen_private_key(P256))
    pk: Point = field(init=False)
    posts: list = field(repr=False, default_factory=list)
    anonymous_posts: list = field(repr=False, default_factory=list)

    def __post_init__(self):
        self.pk = get_public_key(self.sk, P256)

    def send_request(self, request):
        t1 = time.time()
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(request.to_json().encode())
        msg = s.recv(1024).decode()
        s.close()
        benchmark.NETWORK += time.time() - t1
        return msg

    def create_post(self, content, anonymous=False):
        post = Post.create(content, user_pk=self.pk, anonymous=anonymous)
        request = Request(type=RequestType.NEW_POST, content=post.to_dict())
        result = self.send_request(request)
        post.id = json.loads(result)["id"]
        if anonymous:
            self.anonymous_posts.append(post)
        else:
            self.posts.append(post)

    def open_commitment(self, post: Post):
        c = OpenCommitmentMsg.gen(post=post)
        request = Request(type=RequestType.OPEN_COMMITMENT, content=c.to_dict())
        self.send_request(request)

    def test(self, iteration=10, anonymous=False):
        if anonymous:
            for i in range(iteration):
                # content = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                content = "Hello World"
                self.create_post(content, anonymous=True)
            for post in self.anonymous_posts:
                self.open_commitment(post)
        else:
            for i in range(iteration):
                # content = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                content = "Hello World"
                self.create_post(content, anonymous=False)


parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default="localhost")
parser.add_argument('--port', type=int, default=8080)

args = parser.parse_args()

# client.test(iteration=1000, anonymous=True)

print("anonymous post")
for iteration in range(100, 1001, 100):
    client = Client(host=args.host, port=args.port)
    # print(client)
    t1 = time.time()
    client.test(iteration=iteration, anonymous=True)
    t2 = time.time()
    print(f"n = {iteration}, time = {t2 - t1:.2f}, {benchmark.ENCRYPT:.2f} {benchmark.GEN_DECRYPT_MSG:.2f} {benchmark.GENERATE_PROOF:.2f}, net {benchmark.NETWORK:.2f}, other {t2 - t1 - benchmark.ENCRYPT - benchmark.GEN_DECRYPT_MSG - benchmark.GENERATE_PROOF - benchmark.NETWORK:.2f}")
    request = Request(type=RequestType.STATUS, content="")
    client.send_request(request)
    benchmark.ENCRYPT = 0
    benchmark.GENERATE_PROOF = 0
    benchmark.NETWORK = 0
    benchmark.GEN_DECRYPT_MSG = 0


# print()
# print("normal post")
# for iteration in range(100, 1001, 100):
#     client = Client(host=args.host, port=args.port)
#     # print(client)
#     t1 = time.time()
#     client.test(iteration=iteration)
#     t2 = time.time()
#     print(f"n = {iteration}, time = {t2 - t1:.2f}, {benchmark.GENERATE_PROOF:.2f}")
#     request = Request(type=RequestType.STATUS, content="")
#     client.send_request(request)
#     benchmark.GENERATE_PROOF = 0

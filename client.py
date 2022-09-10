#!/usr/bin/env python3

import argparse
from dataclasses import dataclass, field
import json
import random
from fastecdsa.keys import gen_private_key, get_public_key, gen_keypair
from fastecdsa.point import Point
from fastecdsa.curve import P256
import socket
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

    def __send_request(self, request):
        s = socket.socket()
        s.connect((self.host, self.port))
        s.send(request.to_json().encode())
        msg = s.recv(1024).decode()
        s.close()
        return msg

    def create_post(self, content, anonymous=False):
        post = Post.create(content, user_pk=self.pk, anonymous=anonymous)
        request = Request(type=RequestType.NEW_POST, content=post.to_dict())
        result = self.__send_request(request)
        post.id = json.loads(result)["id"]
        if anonymous:
            self.anonymous_posts.append(post)
        else:
            self.posts.append(post)

    def open_commitment(self, post: Post):
        c = OpenCommitmentMsg.gen(post=post)
        request = Request(type=RequestType.OPEN_COMMITMENT, content=c.to_dict())
        self.__send_request(request)

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
    print(f"n = {iteration}, time = {t2 - t1}")


print()
print("normal post")
for iterations in range(100, 1001, 100):
    client = Client(host=args.host, port=args.port)
    # print(client)
    t1 = time.time()
    for iteration in range(iterations):
        client.test()
    t2 = time.time()
    print(f"n = {iterations}, time = {t2 - t1}")

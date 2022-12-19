#!/usr/bin/env python3

import string
import random
from pyring.one_time import PrivateKey

from post import Post
from Crypto.Random import get_random_bytes


class User:
    def __init__(self):
        self.cks = {}

        self.username = ''.join(random.choices(string.ascii_lowercase, k=8))
        self.posts = []

    def registration_phase_send(self):
        self.rsk = PrivateKey.generate()
        self.rpk = self.rsk.public_key().point
        self.rsk = self.rsk.scalar
        return self.rpk

    def registration_phase_receive_index(self, rpk_index):
        self.rpk_index = rpk_index

    def registration_phase_receive_rpks(self, rpks: list):
        self.rpks = rpks

    def unlinkable_post_phase_send(self):
        message = ''.join(random.choices(string.ascii_lowercase, k=8))
        post = Post(message)
        ck = get_random_bytes(16)
        post.commit_and_sign(self.username, ck, self.rpks, self.rsk, self.rpk_index)
        self.cks[post.uuid] = ck
        self.posts.append(post)
        return post

    def disclose_phase_send(self, uuid):
        return self.username, self.cks[uuid]

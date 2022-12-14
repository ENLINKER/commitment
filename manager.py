#!/usr/bin/env python3

import sys
from uuid import UUID
from post import Post


class Manager:
    def __init__(self):
        self.rpks = []
        self.posts = {}

    def registration_phase_receive(self, rpk):
        self.rpks.append(rpk)

    def registration_phase_send_rpks(self):
        return self.rpks

    def unlinkable_post_phase_receive(self, post: Post):
        if post.verify_sign():
            self.posts[post.uuid] = post
            return True
        else:
            return False

    def disclose_phase_receive(self, uuid: UUID, username: str, ck: bytes):
        return self.posts[uuid].open(username, ck)

    def count_storage(self):
        return sys.getsizeof(self.rpks) + sys.getsizeof(self.posts)

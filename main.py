#!/usr/bin/env python3

from user import User
from manager import Manager

NUM_USER = 2
POST_PER_USER = 1

manager = Manager()
users = [User() for i in range(NUM_USER)]

print("1. registration phase")
for user in users:
    rpk = user.registration_phase_send()
    manager.registration_phase_receive(rpk)

rpks = manager.registration_phase_send_rpks()
for user in users:
    user.registration_phase_receive_rpks(rpks)

print()
print("2. unlinkable post phase")
for user in users:
    for j in range(POST_PER_USER):
        post = user.unlinkable_post_phase_send()
        success = manager.unlinkable_post_phase_receive(post)
        assert (success)

print()
print("3. disclose post phase")
for user in users:
    for post in user.posts:
        username, ck = user.disclose_phase_send(post.uuid)
        success = manager.disclose_phase_receive(post.uuid, username, ck)
        print(f"Success {success}")
        assert (success)

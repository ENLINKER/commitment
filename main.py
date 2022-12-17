#!/usr/bin/env python3

from timer import Timer
from user import User
from manager import Manager
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", type=int, required=True)
parser.add_argument("-p", "--post", type=int, required=True)
args = parser.parse_args()

NUM_USER = args.user
POST_PER_USER = args.post

manager = Manager()
users = [User() for i in range(NUM_USER)]


print("1. registration phase")

manager_timer1 = Timer("manager phase 1")
user_timer1 = Timer("user phase 1")

for user in users:
    user_timer1.start()
    rpk = user.registration_phase_send()
    user_timer1.end()
    user_timer1.add_bandwidth(rpk)

    manager_timer1.add_bandwidth(rpk)
    manager_timer1.start()
    manager.registration_phase_receive(rpk)
    manager_timer1.end()

for user in users:
    manager_timer1.start()
    rpks = manager.registration_phase_send_rpks()
    manager_timer1.end()
    manager_timer1.add_bandwidth(rpks)

    user_timer1.add_bandwidth(rpks)
    user_timer1.start()
    user.registration_phase_receive_rpks(rpks)
    user_timer1.end()

manager_timer1.print()
user_timer1.print(NUM_USER)


print()
print("2. unlinkable post phase")

manager_timer2 = Timer("manager phase 2")
user_timer2 = Timer("user phase 2")

for user in users:
    for j in range(POST_PER_USER):
        user_timer2.start()
        post = user.unlinkable_post_phase_send()
        user_timer2.end()
        user_timer2.add_bandwidth(post)

        manager_timer2.add_bandwidth(post)
        manager_timer2.start()
        success = manager.unlinkable_post_phase_receive(post)
        manager_timer2.end()
        assert (success)

manager_timer2.print()
user_timer2.print(NUM_USER)


print()
print("3. disclose post phase")

manager_timer3 = Timer("manager phase 3")
user_timer3 = Timer("user phase 3")

for user in users:
    for post in user.posts:
        user_timer3.start()
        username, ck = user.disclose_phase_send(post.uuid)
        user_timer3.end()
        user_timer3.add_bandwidth(post.uuid)
        user_timer3.add_bandwidth(username)
        user_timer3.add_bandwidth(ck)

        manager_timer3.add_bandwidth(post.uuid)
        manager_timer3.add_bandwidth(username)
        manager_timer3.add_bandwidth(ck)
        manager_timer3.start()
        success = manager.disclose_phase_receive(post.uuid, username, ck)
        manager_timer3.end()
        assert (success)

manager_timer3.print()
user_timer3.print(NUM_USER)

print()
print(f"Manager rpk storage: {manager.rpks_storage()} Bytes total")
print(f"Manager rpk storage: {manager.rpks_storage() / NUM_USER} Bytes per user")

print()
print(f"Manager posts storage: {manager.posts_storage()} Bytes total")
print(f"Manager posts storage: {manager.posts_storage() / (NUM_USER * POST_PER_USER)} Bytes per post")

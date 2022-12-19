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

manager_timer11 = Timer("manager phase 1.1")
user_timer11 = Timer("user phase 1.1")

u2m_data = []

user_timer11.start()
for user in users:
    rpk = user.registration_phase_send()
    u2m_data.append(rpk)
user_timer11.end()

user_timer11.add_bandwidth(u2m_data)
manager_timer11.add_bandwidth(u2m_data)

m2u_data = []

manager_timer11.start()
for d in u2m_data:
    rpk_index = manager.registration_phase_receive(d)
    m2u_data.append(rpk_index)
manager_timer11.end()

manager_timer11.add_bandwidth(m2u_data)
user_timer11.add_bandwidth(m2u_data)

user_timer11.start()
for user, d in zip(users, m2u_data):
    user.registration_phase_receive_index(d)
user_timer11.end()

manager_timer11.print()
user_timer11.print(NUM_USER)

manager_timer12 = Timer("manager phase 1.2")
user_timer12 = Timer("user phase 1.2")

data = []

manager_timer12.start()
for user in users:
    rpks = manager.registration_phase_send_rpks()
    data.append(rpks)
manager_timer12.end()

manager_timer12.add_bandwidth(data)
user_timer12.add_bandwidth(data)

user_timer12.start()
for user, d in zip(users, data):
    user.registration_phase_receive_rpks(d)
user_timer12.end()

print()
manager_timer12.print()
user_timer12.print(NUM_USER)


print()
print("2. unlinkable post phase")

manager_timer2 = Timer("manager phase 2")
user_timer2 = Timer("user phase 2")

data = []

user_timer2.start()
for user in users:
    for j in range(POST_PER_USER):
        post = user.unlinkable_post_phase_send()
        data.append(post)
user_timer2.end()

user_timer2.add_bandwidth(data)
manager_timer2.add_bandwidth(data)

manager_timer2.start()
for d in data:
    success = manager.unlinkable_post_phase_receive(d)
    assert (success)
manager_timer2.end()

manager_timer2.print()
user_timer2.print(NUM_USER)


print()
print("3. disclose post phase")

manager_timer3 = Timer("manager phase 3")
user_timer3 = Timer("user phase 3")

data = []

user_timer3.start()
for user in users:
    for post in user.posts:
        username, ck = user.disclose_phase_send(post.uuid)
        data.append([post.uuid, username, ck])
user_timer3.end()

user_timer3.add_bandwidth(data)
manager_timer3.add_bandwidth(data)

manager_timer3.start()
for d in data:
    success = manager.disclose_phase_receive(d[0], d[1], d[2])
    assert (success)
manager_timer3.end()

manager_timer3.print()
user_timer3.print(NUM_USER)

print()
print(f"Manager rpk storage: {manager.rpks_storage()} Bytes")
print(f"Manager rpk storage: {manager.rpks_storage() // NUM_USER} Bytes per user")

print()
print(f"Manager posts storage: {manager.posts_storage()} Bytes")
print(f"Manager posts storage: {manager.posts_storage() // (NUM_USER * POST_PER_USER)} Bytes per post")

print()
print(f"Manager total storage: {manager.rpks_storage() + manager.posts_storage()} Bytes")

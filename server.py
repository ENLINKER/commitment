#!/usr/bin/env python3

import argparse
from datetime import datetime
import socket

from post.post import Post
from request.request import Request, RequestType
from post.open_commitment_msg import OpenCommitmentMsg
import json
import os


class Server:
    def __init__(self, host, port, log_filename):
        self.addr = (host, port)
        os.makedirs(os.path.dirname(log_filename), exist_ok=True)
        self.log_fp = open(log_filename, 'w')
        self.posts = []

    def __del__(self):
        self.log_fp.close()
        self.socket.close()

    def __write_log(self, log):
        time = datetime.now()
        self.log_fp.write(f'{time} {log}\n')
        self.log_fp.flush()

    def start(self):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.addr)
        self.socket.listen()
        print(f'Accepting connection on {self.addr}')

        while True:
            client, addr = self.socket.accept()
            # print(f'Connected by {addr}')
            msg = client.recv(1024).decode()
            # print(f'msg: {msg}')
            request = Request.from_json(msg)
            if request.type == RequestType.NEW_POST:
                post = Post.from_dict(request.content)
                post.id = len(self.posts)
                self.posts.append(post)
                client.send(json.dumps({"id": len(self.posts) - 1}).encode())
            elif request.type == RequestType.OPEN_COMMITMENT:
                open_commitment_msg = OpenCommitmentMsg.from_dict(request.content)
                # print(open_commitment)
                # print()
                # print(self.posts[open_commitment_msg.post_id])
                self.posts[open_commitment_msg.post_id].open(open_commitment_msg)
                # print(self.posts[open_commitment_msg.post_id])
                # print()
                # client.send(json.dumps({"status": "success"}).encode())
            client.close()


parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default="localhost")
parser.add_argument('--port', type=int, default=8080)
parser.add_argument('--log', type=str, default="log/server.log")

args = parser.parse_args()

server = Server(args.host, args.port, args.log)

server.start()

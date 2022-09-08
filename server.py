import argparse
from datetime import datetime
import socket

from request.post import Post
from request.request import Request, RequestType
from request.open_commitment import OpenCommitment
import json


class Server:
    def __init__(self, host, port, log_filename):
        self.addr = (host, port)
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
        self.socket.bind(self.addr)
        self.socket.listen()
        print(f'Accepting connection on {self.addr}')

        while True:
            client, addr = self.socket.accept()
            print(f'Connected by {addr}')
            msg = client.recv(1024).decode()
            print(f'msg: {msg}')
            request = Request.from_str(msg)
            if request.request_type == RequestType.NEW_POST:
                post = Post.from_json(request.content)
                self.posts.append(post)
                client.send(json.dumps({"id", len(self.posts) - 1}))
            elif request.request_type == RequestType.OPEN_COMMITMENT:
                open_commitment = OpenCommitment.from_json(request.content)
                self.posts[open_commitment.id].open_commitment(open_commitment.dec_msg)
            client.close()


parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, default="localhost")
parser.add_argument('port', type=int, defalut=8080)
parser.add_argument('log', type=str, default="log/server.log")

args = parser.parse_args()

server = Server(args.host, args.port, args.log)

server.start()

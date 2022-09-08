

import argparse
from fastecdsa import keys


class Client():
    def __init__(self):
        self.sk, self.pk = keys.gen_keypair()

    def create_post(self, content, anonymous=False):
        pass


parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, default="localhost")
parser.add_argument('port', defalut=8080)

args = parser.parse_args()

client = Client(args.host, args.port)

client.start()

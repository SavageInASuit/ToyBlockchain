from datetime import datetime
from threading import Thread
from hashlib import sha256
from block import Block
import time

class Node(Thread):
    '''Class representing a blockchain node. Does work to try to be the first to put a block together'''
    def __init__(self, node_id, blockchain, network, block_tx_limit=30, difficulty=4):
        super(Node, self).__init__()
        self.id = node_id
        self.address = self.sha_hash(self.id)
        self.blockchain = blockchain
        self.network = network
        self.block_tx_limit = block_tx_limit
        self.difficulty = difficulty

    def sha_hash(self, to_hash):
        return sha256(str(to_hash).encode('utf-8')).hexdigest()

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def run(self):
        txns = []
        while not len(txns) == self.block_tx_limit:
            txns = self.network.get_txns(self.block_tx_limit)
            time.sleep(0.1)
        self.mine(txns)
        self.run()

    def mine(self, txns):
        bar = int('f' * (64 - self.difficulty), 16)
        timestamp = datetime.now()
        info = self.blockchain.get_prev_info()
        secret = -1
        # Find a hash with a value lower than the bar, given the difficulty
        h = self.sha_hash(str(str(info['id'] + 1) + str(timestamp) + str(txns) + str(info['hash'])))
        beaten = False
        while int(h, 16) > bar:
            if self.blockchain.accepting_id(info['id'] + 1):
                secret += 1
                h = Block.compute_hash(info['id'] + 1, timestamp, txns, info['hash'], secret)
            else:
                beaten = True
                break

        if not beaten:
            print("\nNode {} creating block {}".format(self.id, info['id'] + 1))
            b = Block(info['id'] + 1, timestamp, txns, prev_hash=info['hash'], sha_hash=h, secret=secret)
            beaten = not self.blockchain.add(b, address=self.address)
        if beaten:
            print("Node {} beaten to creating block {}".format(self.id, info['id'] + 1))

from datetime import datetime
from random import random, seed
from threading import Lock
from block import Block
from network import Network
from node import Node

class BlockChain(object):
    '''Main class of the blockchain. Holds all blocks and can varify their validity'''
    def __init__(self, network):
        self.blockchain = []
        self.blockchain.append(Block(0, datetime.now(), "Genesis Block", "GENESIS"))
        self.last_block = self.blockchain[-1]
        self.lock = Lock()
        self.network = network


    def accepting_id(self, block_id):
        return block_id == self.last_block.block_id + 1

    def add(self, block, address=None):
        # TODO: Varify that block is legit
        self.lock.acquire()
        self.network.clear_txns(block.data)
        print(block.hash)
        self.blockchain.append(block)
        self.last_block = self.blockchain[-1]
        self.lock.release()
        return True

    def get_prev_info(self):
        return {'hash':self.last_block.hash, 'id':self.last_block.block_id}

verbose = False

def main():
    # Initialise state
    users = ["Tom", "Catherine", "Bob"]
    state = {}
    for user in users:
        state[user] = int(random() * 200)
    print("Account statuses:")
    print(state)
    
    txn_buffer = []
    net = Network(20, txn_buffer, users, state, real=True)
    net.start()
    blockchain = BlockChain(net)
    MAX_TX_PER_BLOCK = 20 
    NODE_COUNT = 4
    nodes = [Node(i, blockchain, net) for i in range(NODE_COUNT)]
    for node in nodes:
        node.start()

if __name__ == "__main__":
    # seed(1)
    main()

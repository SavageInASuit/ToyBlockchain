from datetime import datetime
from random import random, seed
from threading import Lock
from block import Block
from network import Network
from node import Node
from hashlib import sha256

class BlockChain(object):
    '''Main class of the blockchain. Holds all blocks and can varify their validity'''
    def __init__(self, network, difficulty):
        self.blockchain = []
        self.blockchain.append(Block(0, datetime.now(), "Genesis Block", "GENESIS"))
        self.last_block = self.blockchain[-1]
        self.lock = Lock()
        self.network = network
        self.difficulty = difficulty

    def accepting_id(self, block_id):
        return block_id == self.last_block.block_id + 1

    def add(self, block, address=None):
        # TODO: Varify that block is legit
        self.lock.acquire()
        if not self.__is_valid_block(block):
            self.lock.release()
            return False
        self.network.clear_txns(block.data)
        print(block.hash)
        self.blockchain.append(block)
        print(self.blockchain)
        self.last_block = self.blockchain[-1]
        self.lock.release()
        return True

    def sha_hash(self, to_hash):
        return sha256(str(to_hash).encode('utf-8')).hexdigest()

    ''' create a hashing function on the block itself that both the nodes use and the blockchain uses to varify '''
    def __is_valid_block(self, block):
        bar = int('f' * (64 - self.difficulty), 16)
        if int(block.hash, 16) > bar:
            print("Block {}'s hash value was too high!: {}".format(block.block_id, block.hash))
            return False
        # Using the same function as the Node is not giving the same hash... some data must be different
        test_hash = Block.compute_hash(block.block_id, block.timestamp, block.data, prev_hash=block.prev_hash, secret=block.secret)
        if not test_hash == block.hash:
            print("Block {}'s hash is incorrect!: {} != {}".format(block.block_id, test_hash, block.hash))
            return False
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
    blockchain = BlockChain(net, 4)
    MAX_TX_PER_BLOCK = 20 
    NODE_COUNT = 4
    nodes = [Node(i, blockchain, net) for i in range(NODE_COUNT)]
    for node in nodes:
        node.start()

if __name__ == "__main__":
    # seed(1)
    main()

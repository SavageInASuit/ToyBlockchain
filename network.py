from threading import Thread
from random import random
import time
from transaction import Transaction

class Network(Thread):
    def __init__(self, tx_s, txn_buffer, users, state, real = False, inv_pc = 0.0):
        super(Network, self).__init__()
        self.tx_s = int(0.5 * tx_s)
        self.buffer = txn_buffer
        self.users = users
        # This means the thread will quit when the main thread quits
        self.daemon = True
        self.state = state
        self.real = real
        self.txns = []
        self.inv_pc = inv_pc
        self.next_id = 0

        print("Connected to network")

    def run(self):
        if self.real:
                self.generate_background_txns()
        else:
            for _ in range(100):
                tx_to_add = self.tx_s + int(random() * self.tx_s * 2)
                self.buffer.extend(self.generate_txns(tx_to_add, 0.05))
                print("Added more transactions from network!")
                time.sleep(1)

    def clear_txns(self, txns):
        self.apply_transactions(txns)
        ids = list(map(lambda tx: tx.tx_id, txns))
        removed = []
        for i in reversed(range(len(self.txns))):
            if self.txns[i].tx_id in ids:
                removed.append(self.txns[i].tx_id)
                self.txns.pop(i) 

    def apply_transactions(self, txns):
        for tx in txns:
            self.state[tx.u_from] -= tx.amnt
            self.state[tx.u_to] += tx.amnt
        print("State: {}".format(str(self.state)))

    def generate_background_txns(self):
        first_ind = int(random() * len(self.users))
        first = self.users[first_ind]
        second_ind = int(random() * len(self.users)) 
        while second_ind == first_ind:
            second_ind = int(random() * len(self.users)) 
        second = self.users[second_ind] 

        # Txn is someone sending amnt < 100 to another user
        out = int(random() * 100) + 1

        # Need to work in invalid pc
        new_tx = Transaction(self.next_id, first, second, out)
        self.txns.append(new_tx)
        self.next_id += 1

        time.sleep(1 / (self.tx_s + (random() * self.tx_s * 2)))
        self.generate_background_txns()

    def get_txns(self, max_amnt):
        return self.txns[:max_amnt]

    def generate_txns(self, num, inv_pc=0.0):
        txns = []
        for _ in range(num):
            # Get users involved
            first_ind = int(random() * len(self.users))
            first = self.users[first_ind]
            second_ind = int(random() * len(self.users)) 
            while second_ind == first_ind:
                second_ind = int(random() * len(self.users)) 
            second = self.users[second_ind] 

            # Txn is someone sending amnt < 100 to another user
            out = int(random() * 100) + 1
            if random() < inv_pc:
                new_tx = {first: out, second: int(random() * 100)}
            else: 
                new_tx = {first: out, second: -out}
            txns.append(new_tx)
        return txns


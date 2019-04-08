class Transaction(object):
    '''Holds information about transactions to be stored in the blockchain'''
    def __init__(self, tx_id, u_from, u_to, amnt):
        self.tx_id = tx_id
        self.u_from = u_from
        self.u_to = u_to
        self.amnt = amnt

    def varify(self, state):
        print("varifying transaction")

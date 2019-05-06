class Transaction(object):
    '''Holds information about transactions to be stored in the blockchain'''
    def __init__(self, tx_id, u_from, u_to, amnt):
        self.tx_id = tx_id
        self.u_from = u_from
        self.u_to = u_to
        self.amnt = amnt

    def varify(self, state):
        print("varifying transaction")

    def __str__(self):
        return "<Transaction {} from {} to {} >".format(self.amnt, self.u_from, self.u_to)

    def __repr__(self):
        return "<Transaction {} - {} to {}>".format(self.amnt, self.u_from, self.u_to)

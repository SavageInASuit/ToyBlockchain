from hashlib import sha256

class Block:
    def __init__(self, block_id, timestamp, data, prev_hash = None, sha_hash=None, secret=None):
        self.block_id = block_id
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.secret = secret

        if sha_hash is not None:
            self.hash = sha_hash
        elif prev_hash is not None:
            self.hash = Block.compute_hash(block_id, timestamp, data, prev_hash, 0)
        else:
            Exception("Previous hash, or current hash not supplied")

    @staticmethod
    def compute_hash(block_id, timestamp, data, prev_hash, secret):
        return sha256(str(str(block_id) + 
                str(timestamp) + 
                str(data) + 
                str(prev_hash) + str(secret)).encode('utf-8')).hexdigest()
    def __str__(self):
        return '''ID: {}\nTimeStamp: {}\nData: {}\nPrevHash: {}\nHash: {}'''.format(self.block_id, self.timestamp, self.data, self.prev_hash, self.hash)

    def __repr__(self):
        return "<Block {}>".format(self.block_id)


from hashlib import sha256

class Block:
    def __init__(self, block_id, timestamp, data, prev_hash = None, sha_hash=None):
        self.block_id = block_id
        self.timestamp = timestamp
        self.data = data
        
        if sha_hash is not None:
            self.hash = sha_hash
        elif prev_hash is not None:
            self.prev_hash = prev_hash
            self.hash = self.compute_hash()
        else:
            Exception("Previous hash, or current hash not supplied")

    def compute_hash(self):
        return sha256(str(str(self.block_id) + 
                str(self.timestamp) + 
                str(self.data) + 
                str(self.prev_hash)).encode('utf-8')).hexdigest()

    def __str__(self):
        return '''ID: {}\nTimeStamp: {}\nData: {}\nPrevHash: {}\nHash: {}'''.format(self.block_id, self.timestamp, self.data, self.prev_hash, self.hash)

    def __repr__(self):
        return "<Block {}>".format(self.block_id)


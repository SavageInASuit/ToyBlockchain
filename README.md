# ToyBlockchain
A simple blockchain simulator(?) written in Python 3 (WIP)

## Current State
### Blockchain
- Stores list of consecutive blocks
- Accepts new blocks
- Unable to validate new blocks yet
### Blocks
- Store arbitrary data (Transactions currently)
- Hash consists of string representation of the block id, timestamp, data content and previous block hash
### Network
- Simply simulates transactions on a real network
- Transactions created at an average tx/s
### Transactions
- Refer only to sender, receiver and amount sent
- Make no reference to previous transactions (as in Bitcoin: https://en.bitcoin.it/wiki/Transaction)
### Nodes
- Check network to find new transactions to place in block up to defined limit
- Do work to find nonce/secret value that produces a hash with hex value less than specific amount, relative to difficulty
- Adds blocks to blockchain

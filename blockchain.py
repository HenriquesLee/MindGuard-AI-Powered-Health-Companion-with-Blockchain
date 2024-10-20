import hashlib
from hashlib import sha256
import time  


class Block:
    def __init__(self, index, previous_hash, timestamp, username, action_data, block_hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.username = username
        self.action_data = action_data
        self.block_hash = block_hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = {
            'id': 0,
            'action_data': "Genesis Block",
            'timestamp': time.time(),
            'previous_hash': "0"
        }
        genesis_block['hash'] = self.hash_block(genesis_block)
        self.chain.append(genesis_block)

    def add_block(self, username, action_data):
        block = {
            'id': len(self.chain) + 1,
            'action_data': action_data,  # Keeping raw data here for now
            'timestamp': time.time(),
            'previous_hash': self.chain[-1]['hash']
        }
        # Hash the action_data before storing the block
        block['action_data'] = self.hash_data(action_data)
        block['hash'] = self.hash_block(block)
        self.chain.append(block)

    def hash_block(self, block):
        encoded_block = (str(block['id']) + block['action_data'] + str(block['timestamp']) + block['previous_hash']).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def hash_data(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def get_chain(self):
        return self.chain


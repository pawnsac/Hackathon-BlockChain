import time
from Transaction import Transaction

#Blockchain for transaction ledger
class Blockchain: 
    def __init__(self):
        self.unconfirmed_transactions = []
        self.valid_chain = []
        self.create_genesis_block()
        self.difficulty = 5
 
    def create_genesis_block(self):
        genesis_block = Transaction(0,'', '','', 0,time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.valid_chain.append(genesis_block)

    @property
    def last_block(self):
        return self.valid_chain[-1]

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.valid_chain.append(block)
        return True
 
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and
            block_hash == block.compute_hash())

    def add_new_transaction(self, seller, buyer,token,value):
        self.unconfirmed_transactions.append([seller,buyer,token,value])
    
    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block
        trans = self.unconfirmed_transactions[0]

        new_block = Transaction(index=last_block.index + 1,seller=trans[0],buyer=trans[1],token=trans[2],value=trans[3],timestamp=time.time(),previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions.pop(0)
        return new_block.index

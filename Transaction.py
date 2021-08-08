from hashlib import sha256
import json

class Transaction:
    def __init__(self, index, seller, buyer, token, value, signature, time_stamp, previous_hash, nonce=0,for_sale=False):
        self.index = index
        self.seller = seller
        self.buyer = buyer
        self.token = token
        self.value = value
        self.signature = signature
        self.for_sale = for_sale
        self.time_stamp = time_stamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
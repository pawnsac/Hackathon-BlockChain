
class Transaction:
    def __init__(self, index, seller, buyer, token, value, signature, time_stamp, previous_hash, for_sale,nonce=0):
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
        self.signature_token=self.token + self.time_stamp


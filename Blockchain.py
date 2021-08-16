import time
from Transaction import Transaction
from hashing import VerifySignature, SignString
import pickle
import subprocess
from wallet import *
import datetime
from hashlib import sha256
import json
from Node import Node
import os

#Blockchain for transaction ledger
class Blockchain(Node): 
	def __init__(self,host,port):
		Node.__init__(self,host,port)
		self.unconfirmed_transactions = []
		self.valid_chain = []
		self.difficulty = 4
		self.create_genesis_block()
		self.wallets=[]
 
	def create_genesis_block(self):
		genesis_block = Transaction(0,'', '','', 0,'',datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"), "NULL",{})

		self.proof_of_work(genesis_block)
		self.valid_chain.append(genesis_block)

	@property
	def last_block(self):
		return self.valid_chain[-1]

	def proof_of_work(self, block):
		block.nonce = 0
		computed_hash = self.compute_hash(block)
		while not computed_hash.startswith('0' * self.difficulty):
			block.nonce += 1
			computed_hash = self.compute_hash(block)
		return computed_hash

	def add_block(self, block, proof):
		previous_hash = self.compute_hash(self.last_block)
		if previous_hash != block.previous_hash:
			return False
		if not self.is_valid_proof(block, proof):
			return False
		self.valid_chain.append(block)
		return True
 
	def is_valid_proof(self, block, block_hash):
		return (block_hash.startswith('0' * self.difficulty) and
			block_hash == self.compute_hash(block)) and VerifySignature(block.signature_token,block.signature,block.buyer)

	def add_new_transaction(self, seller, buyer,token,value,signature,for_sale,time_stamp):
		self.unconfirmed_transactions.append([seller,buyer,token,value,signature,for_sale,time_stamp])
	
	def mine(self):
		if not self.unconfirmed_transactions:
			return False
		last_block = self.last_block
		trans = self.unconfirmed_transactions[0]
		if not VerifySignature(trans[2]+trans[6],trans[4],trans[1]):
			return False
		new_block = Transaction(index=last_block.index + 1,seller=trans[0],buyer=trans[1],token=trans[2],value=trans[3],signature=trans[4], for_sale=trans[5], time_stamp=trans[6],previous_hash=self.compute_hash(last_block))
		print("Starting Proof of Work")
		proof = self.proof_of_work(new_block)
		self.add_block(new_block, proof)
		if not self.check_inconsistencies(self.valid_chain):
			print ("Validation process failed, block not added")
			self.valid_chain=self.valid_chain[:-1]
		else:
		  print("A new bock added")
		self.unconfirmed_transactions.pop(0)
		return new_block.index
    
	def save_object(self, obj, filename):
		with open(filename, 'wb') as outp:  # Overwrites any existing file.
			pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)
	def save_chain(self):
		for block in self.valid_chain:
			self.save_object(block,"storage/block_"+str(block.index)+".pkl")
		print("Blockchain saved in directory 'storage'")
	def load_chain(self,dir,length):
		new_chain=[]
		for block_index in range(length):
			with open(dir+'/block_{}.pkl'.format(block_index), 'rb') as inp:
				block = pickle.load(inp)
				new_chain.append(block)

		if self.check_inconsistencies(new_chain):
		
			self.valid_chain=new_chain

			print("Blockchain loaded from 'storage' dir!")
		else:
			print ("Blockchain corrupt, not added!")
	def check_inconsistencies(self,chain):
		i=0
		previous_hash="NULL"
		temp_chain=[]
		tokens=[]
		for block in chain:
			if i==0:
				previous_hash=self.compute_hash(block)
				temp_chain.append(block)
				i+=1
				continue
			if not block.previous_hash==previous_hash:
				print("check 2 failed")
				return False
			if block.seller['key'] == block.buyer['key'] and block.token in tokens:
				print("check 3 failed, token already present")
				return False
			if block.seller['key'] == block.buyer['key']:
				tokens.append(block.token)
				previous_hash=self.compute_hash(block)
				temp_chain.append(block)
				continue
			if self.compute_balance(block.buyer, temp_chain) < block.value:
				print("check 4 failed, less coins given")
				return False
			if self.get_for_sale(block.token,temp_chain) == 'n':
				print("check 5 failed, not for sale")
				return False
			if not self.get_for_sale(block.token,temp_chain) == value:
				print("check 6 failed")
				return False
			
			previous_hash=self.compute_hash(block)
			tokens.append(block.token)
			print(tokens)
			temp_chain.append(block)

		return True
	def get_for_sale(self, token,blockchain):
		value=0
		for block in reversed(blockchain):
			if block.token == token:
				if block.for_sale['bool']=='n':
					return 'n'
				else:
					return block.for_sale['value']
		return 'n'
	def compute_balance(self, public_key,blockchain):
		balance=0
		i=0
		for block in blockchain:
			if i==0:
				i+=1
				continue
			if public_key ==block.seller['key']:
				balance+=block.value
			elif public_key==block.buyer['key']:
				balance-=block.value

		return balance
	def compute_hash(self,block):
		block_string = json.dumps(block.__dict__, sort_keys=True)
		block_string=block_string.encode()
		return sha256(block_string).hexdigest()

	def print_chain(self):
		for block in self.valid_chain:
			print ("***************************")
			print("Block index # {}".format(block.index))
			hash=self.compute_hash(block)
			print("hash: {}".format(hash))
			if block.index==0:
				print ("Genesis Block")
				print ("***************************")
				print("")
				continue
			print("Buyer: {}".format(block.buyer['key']) )
			print("Seller: {}".format(block.seller['key']))
			print("Token: {}".format(block.token) )
			print("For_sale (y or n): {}".format(block.for_sale['bool']))
			if block.for_sale['bool']=='y':
				print("For_sale price: {}".format(block.for_sale['value']))
			print("nonce: {}".format(block.nonce) )
			print("previous_hash: {}".format(block.previous_hash) )

			print ("***************************")
			print("")

	def saveUnconfirmed(self):
		with open(os.path.join("mempool","unconfirmed"), "w") as fp:
			fp.write(json.dumps(self.unconfirmed_transactions))

			

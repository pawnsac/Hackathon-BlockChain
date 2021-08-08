from Blockchain import Blockchain

from hashing import *
from nft import *
from wallet import*
import os, os.path
print ("Type add for adding_transactions")
print ("Type mine for mining_transactions")
print ("Type print for printing_blockchain")
print ("Type load for loading_blockchain")
print ("Type save for saving_blockchain")
print ("Type new_wallet for creating a wallet")
print ("Type market for viewing NFT market")
print ("Type broadcast for sending blockchain")
print ("Type img_token for getting token of NFT")
Chain=Blockchain()

while True:
	args=input()
	if args=="add":
		seller={}
		seller['key']=input("Seller Public key: ")
		seller['n']=int(input("Seller Public key 'n' value: "))
		seller['e']=int(input("Seller Public key 'e' value: "))
		buyer={}
		buyer['key']=input("Buyer Private key: ")
		buyer['n']=int(input("Buyer Private key 'n' value: "))
		buyer['d']=int(input("Buyer Private key 'd' value: "))

		buyer_public={}
		buyer_public['key']=input("Buyer Public key: ")
		buyer_public['n']=int(input("Buyer Public key 'n' value: "))
		buyer_public['e']=int(input("Buyer Public key 'e' value: "))
		token=input("Token :")
		for_sale=int(input("For sale (0 or 1): "))
		value=0
		signature=SignString(token,buyer)
				
		Chain.add_new_transaction(seller, buyer_public,token,value,signature,for_sale)
		print ("Transaction added, ready for mining!")

	elif args=="mine":
		Chain.mine()
		print("Mining done!")
	elif args=="save":
		Chain.save_chain()
	elif args=="load":
		DIR=input("Dir of blockchain: ")
		length=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
		Chain.load_chain(DIR,length)
	elif args=="print":
		Chain.print_chain()
	elif args=="new_wallet":
		CreateWallet()
	elif args=="market":
		get_marketplace(Chain.valid_chain)
	elif args=="img_token":
		file=input("Enter img dir: ")
		token=hash_image(file)
		print("Token: ", token)
	else:
		print("Invalid Arguments")
	
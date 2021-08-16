from Blockchain import Blockchain
import threading
from hashing import *
from nft import *
from wallet import*
import os, os.path
import datetime
from Node import Node
import sys
import time



if len(sys.argv) == 4:
	Chain=Blockchain(sys.argv[-3],int(sys.argv[-2]))
	print("Initiating Connection with port",sys.argv[-1],"...")
	Chain.con(sys.argv[-3],int(sys.argv[-1]))
	print("Connected!")
else:
	Chain=Blockchain(sys.argv[-2],int(sys.argv[-1]))


print ("\nType add for adding_transactions")
print ("Type mine for mining_transactions")
print ("Type print for printing_blockchain")
print ("Type load for loading_blockchain")
print ("Type save for saving_blockchain")
print ("Type new_wallet for creating a wallet")
print ("Type market for viewing NFT market")
print ("Type img_token for getting token of NFT")
print ("Type info to get listening (host,port) of Node, its public private key pair, coin balance and tokens belonging to it")
print ("Type network to get all nodes connected in the network")

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
		for_sale_bool=input("For sale (y or n): ")
		for_sale_value=0
		if for_sale_bool=='y':
			for_sale_value=int(input("For sale price: "))
		value=100
		if seller['key']!=buyer_public['key']:
			value=int(input("Coins given to buy: "))
		for_sale={'bool':for_sale_bool,'value':for_sale_value}
		time_stamp=datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
		signature=SignString(token+time_stamp,buyer)
		Chain.add_new_transaction(seller, buyer_public,token,value,signature,for_sale,time_stamp)
		print ("Transaction added, ready for mining!")
		Chain.saveUnconfirmed()
		Chain.broadcastt("mempool","unconfirmed")

	elif args=="mine":
		Chain.mine()
		print("Mining done!")
	elif args=="save":
		Chain.save_chain()
	elif args=="load":
		DIR='storage'
		length=len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
		Chain.load_chain(DIR,length)
	elif args=="print":
		Chain.print_chain()
	elif args=="new_wallet":
		Chain.privateKey, Chain.publicKey =  CreateWallet()
	elif args=="market":
		get_marketplace(Chain.valid_chain)
	elif args=="img_token":
		file=input("Enter img dir: ")
		token=hash_image(file)
		print("Token: ", token)
	elif args=="info":
		print(Chain.info())
	elif args=="network":
		print(Chain.network)
	elif args=="broadcast":
		Chain.broadcast("storage")
	
	else:
		print("Invalid Arguments")
	
import socket 
import threading
import hashlib
import sys
import json
import os
import pickle
from Transaction import *

wallet = ""

class Node:
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.blockchain = "BLOCKCHAIN DATA"
		self.stop = False
		self.network = [(self.host,str(self.port))]
		self.privateKey = ""
		self.publicKey = ""
		print("I am listening at port",port,"...")
		threading.Thread(target = self.listener).start()

	def info(self):
		return "host : " + self.host + "\n" + "port : " + str(self.port) + "\n" + "privateKey : " + json.dumps(self.privateKey) + "\n" + "publicKey : " + json.dumps(self.publicKey) + "\n" 

	def listener(self):
		listener = socket.socket()
		listener.bind( (self.host, self.port) )
		listener.listen(10)
		while not self.stop:
			client, addr = listener.accept()
			threading.Thread(target = self.handleConnection, args = (client, addr)).start()

	def handleConnection(self, client, addr):
		msg = json.loads(client.recv(10000).decode("utf-8"))
		client.close()
		if msg["type"] == "CONNECT":
			host = msg["data"]["host"]
			port = msg["data"]["port"]
			
			self.network.append((host,str(port)))
			self.network = sorted(self.network, key = lambda x: int(x[1]) )

			for h,p in self.network:
				soc = socket.socket()
				soc.connect((h,int(p)))
				# print("sending too",p)
				soc.send((json.dumps({"type":"BROADCAST","data":{"Network":self.network,"Blockchain":self.blockchain}})).encode("utf-8") )
				soc.close()
			print("\nLOG:",port,"Connected\n")

		if msg["type"] == "BROADCAST":
			for host,port in msg["data"]["Network"]:
				if (host,port) not in self.network:
					self.network.append((host,port))
					self.network = sorted(self.network, key = lambda x: int(x[1]) )

		if msg["type"] == "BROADCASTB":
			if not os.path.exists(msg["data"]["Path"]):
				os.makedirs(msg["data"]["Path"])
			newblock = Transaction(msg["data"]["Data"][0],msg["data"]["Data"][1],msg["data"]["Data"][2],msg["data"]["Data"][3],msg["data"]["Data"][4],msg["data"]["Data"][5],msg["data"]["Data"][6],msg["data"]["Data"][7],msg["data"]["Data"][8],msg["data"]["Data"][9])
			with open(os.path.join(msg["data"]["Path"],msg["data"]["Name"]), 'wb') as outp:
				pickle.dump(newblock, outp, pickle.HIGHEST_PROTOCOL)
		

	def con(self, host,port ):
		soc = socket.socket()
		soc.connect((host,port))
		soc.send( json.dumps({"type":"CONNECT","data":{"host":host,"port":self.port}}).encode("utf-8") )
		soc.close()

	def broadcast(self,path):
		files = os.listdir(path)
		# print("files",files)
		for (host,port) in self.network:
			if (host,port) != (self.host,str(self.port)):
				for file in files:
					soc = socket.socket()
					soc.connect((host,int(port)))
					# print("x",x)
					with open(os.path.join(path,file), 'rb') as inp:
						data = pickle.load(inp)				
						index = data.index  
						seller = data.seller
						buyer = data.buyer 
						token = data.token 
						value = data.value 
						signature = data.signature 
						for_sale = data.for_sale 
						time_stamp = data.time_stamp 
						previous_hash=data.previous_hash 
						nonce = data.nonce 
						# data = [index,seller,buyer,token,value,signature,time_stamp,previous_hash,nonce,for_sale]
						data = [index, seller, buyer, token, value, signature, time_stamp, previous_hash, for_sale,nonce]
						# print("SEND",("BROADCASTBXYZ" + json.dumps({"Path":path,"Name":file,"Data":data})  ))
						soc.send( (json.dumps({"type":"BROADCASTB","data":{"Path":path,"Name":file,"Data":data}}  ).encode("utf-8") ))
					soc.close()

# IP = "localhost"

# print(len(sys.argv))
# N = Node(sys.argv[-2],int(sys.argv[-1]))
# print("Press 1 to enter port")
# print("Press 2 to get blockchain")
# print("Press 3 to get network data")
# print("Press 4 to Broadcast")


# while 1:
# 	decision = input()
# 	if decision == "1":
# 		port = int(input("Port: ")) 
# 		N.con(IP,port)
# 	if decision == "2":
# 		print(N.blockchain)
# 	if decision == "3":
# 		print(N.network)
# 	if decision == "4":
# 		N.broadcast("storage")
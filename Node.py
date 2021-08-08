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
	def __init__(self, host, port,wallet):
		self.host = host
		self.port = port
		self.blockchain = "BLOCKCHAIN DATA"
		self.key = self.hasher(host+str(port)+wallet)
		self.stop = False
		self.network = [(self.host,str(self.port))]
		print("I am listening at port",port,"...")
		threading.Thread(target = self.listener).start()

	def listener(self):
		listener = socket.socket()
		listener.bind( (self.host, self.port) )
		listener.listen(10)
		while not self.stop:
			client, addr = listener.accept()
			threading.Thread(target = self.handleConnection, args = (client, addr)).start()
		print ("Shutting down node:", self.host, self.port)

	def handleConnection(self, client, addr):
		Type,msg = client.recv(10000).decode("utf-8").split("XYZ")
		client.close()
		if Type == "CONNECT":
			host,port = msg.split(" ")
			self.network.append((host,str(port)))
			print("present",self.network)

			for h,p in self.network:
				soc = socket.socket()
				soc.connect((h,int(p)))
				print("sending too",p)
				soc.send(("BROADCASTXYZ" + json.dumps({"Network":self.network,"Blockchain":self.blockchain})).encode("utf-8") )
				soc.close()

		if Type == "BROADCAST":
			l = json.loads(msg)
			print("Rec",l)
			print(type(l["Network"]))
			for host,port in l["Network"]:
				if (host,port) not in self.network:
					self.network.append((host,port))

		if Type == "BROADCASTB":
			l = json.loads(msg)
			print("ReX",l)
			if not os.path.exists(l["Path"]):
				os.makedirs(l["Path"])
			newblock = Transaction(l["Data"][0],l["Data"][1],l["Data"][2],l["Data"][3],l["Data"][4],l["Data"][5],l["Data"][6],l["Data"][7],l["Data"][8],l["Data"][9])
			with open(os.path.join(l["Path"],l["Name"]), 'wb') as outp:
				pickle.dump(newblock, outp, pickle.HIGHEST_PROTOCOL)

	def hasher(self, key):
		return int(hashlib.md5(key.encode()).hexdigest(), 16)
	def con(self, host,port ):
		soc = socket.socket()
		soc.connect((host,port))
		soc.send( ("CONNECTXYZ" + host + " " + str(self.port)).encode("utf-8") )
		soc.close()

	def broadcast(self,path):
		files = os.listdir(path)
		print("files",files)
		for (host,port) in self.network:
			if (host,port) != (self.host,str(self.port)):
				soc = socket.socket()
				soc.connect((host,int(port)))
				for file in files:
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
						data = [index,seller,buyer,token,value,signature,time_stamp,previous_hash,nonce,for_sale]
						print("SEND",("BROADCASTBXYZ" + json.dumps({"Path":path,"Name":file,"Data":data})  ))
						soc.send( ("BROADCASTBXYZ" + json.dumps({"Path":path,"Name":file,"Data":data})  ).encode("utf-8") )

				soc.close()


IP = "localhost"

N = Node(sys.argv[-2],int(sys.argv[-1]),wallet)
print("Press 1 to enter port")
print("Press 2 to get blockchain")
print("Press 3 to get network data")
print("Press 4 to Broadcast")


while 1:
	decision = input()
	if decision == "1":
		port = int(input("Port: ")) 
		N.con(IP,port)
	if decision == "2":
		print(N.blockchain)
	if decision == "3":
		print(N.network)
	if decision == "4":
		N.broadcast("storage")
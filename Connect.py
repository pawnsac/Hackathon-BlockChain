import socket 
import threading
import hashlib
import sys
import json

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
		Type,msg = client.recv(1024).decode("utf-8").split("-")
		client.close()
		if Type == "CONNECT":
			host,port = msg.split(" ")
			soc = socket.socket()
			soc.connect((host,int(port)))
			# print(self.network)
			soc.send(("BROADCAST-" + json.dumps({"Network":self.network,"Blockchain":self.blockchain})).encode("utf-8") )
			self.network.append((host,str(port)))
			soc.close()
		if Type == "BROADCAST":
			l = json.loads(msg)
			print(l)
			print(type(l["Network"]))
			for host,port in l["Network"]:
				self.network.append((host,port))

		

	def hasher(self, key):
		return int(hashlib.md5(key.encode()).hexdigest(), 16)
	def con(self, host,port ):
		soc = socket.socket()
		soc.connect((host,port))
		soc.send( ("CONNECT-" + host + " " + str(self.port)).encode("utf-8") )
		soc.close()

IP = "localhost"

N = Node(sys.argv[-2],int(sys.argv[-1]),wallet)
print("Press 1 to enter port")
print("Press 2 to get blockchain")
print("Press 3 to get network data")

while 1:
	decision = input()
	if decision == "1":
		port = int(input("Port: ")) 
		N.con(IP,port)
	if decision == "2":
		print(N.blockchain)
	if decision == "3":
		print(N.network)


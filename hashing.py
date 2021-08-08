from hashlib import sha256

def SignString(string,private_key):
	string_encoded=string.encode()
	hash = int.from_bytes(sha256(string_encoded).digest(), byteorder='big')
	signature = pow(hash, private_key['d'], private_key['n'])
	return signature

def VerifySignature(string,signature,public_key):
	string_encoded=string.encode()
	hash = int.from_bytes(sha256(string_encoded).digest(), byteorder='big')
	hashSignature = pow(signature, public_key['e'], public_key['n'])
	return hash == hashSignature



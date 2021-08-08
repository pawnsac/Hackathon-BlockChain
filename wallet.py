from Crypto.PublicKey import RSA

def CreateWallet(len=1024):
	key_pair = RSA.generate(len)
	public_key=str(key_pair.publickey().exportKey())
	private_key=str(key_pair.exportKey())
	public_key,private_key=StripHeaders(public_key,private_key)
	public_key={'key':public_key,'n':key_pair.n,'e':key_pair.e}
	private_key={'key':private_key,'n':key_pair.n,'d':key_pair.d}
	print("Private Key:",private_key)
	print("Public Key:",public_key)
	return [private_key,public_key]

def StripHeaders(public_key,private_key):
	HEADER_PUB_KEY='-----BEGIN PUBLIC KEY-----'
	HEADER_PUB_KEY_END='-----END PUBLIC KEY-----'
	HEADER_PRIV_KEY='-----BEGIN RSA PRIVATE KEY-----'
	HEADER_PRIV_KEY_END='-----END RSA PRIVATE KEY-----'
	public_key = public_key.replace(HEADER_PUB_KEY, '').replace(HEADER_PUB_KEY_END, '')[4:-3]
	private_key = private_key.replace(HEADER_PRIV_KEY, '').replace(HEADER_PRIV_KEY_END, '')[4:-3]
	return (public_key,private_key)

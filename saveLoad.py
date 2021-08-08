import pickle
from Blockchain import Blockchain

def saveBlockChain(chain_object):
    with open('Blockchain','wb') as fileHandler:
        pickle.dump(chain_object,fileHandler)
    return

def loadBlockChain():
    try:
        # use local copy
        with open('Blockchain','rb') as fileHandler:
            obj = pickle.load(fileHandler)
    except:
        # download from other peers or create new if first node
        obj = Blockchain()
    return obj
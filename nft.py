import hashlib

def hash_image(filename,BUFFER_SIZE=4096):
   hash_function = hashlib.sha512()
   with open(filename,'rb') as file:
       data=True
       while data:
       	   data = file.read(BUFFER_SIZE)
       	   if not data:
       	   	break
           hash_function.update(data)      
   return hash_function.hexdigest()



def get_marketplace(blochchain):
    ItemList=[]
    Items=[]
    NotForSale=[]
    for block in reverse(blochchain):
        if block.for_sale==True and block not in NotForSale:
            ItemList.append({"Seller" : block.buyer, "Token" : block.token})
            Items.append(block)
        elif block.for_sale==False and block not in Items and block not in NotForSale:
            NotForSale.append(block)
    return ItemList




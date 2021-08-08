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





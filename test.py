from hashlib import md5
encrypted = md5("suman5179".encode("UTF-8")).hexdigest()
print(encrypted)
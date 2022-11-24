import json

f = open('firebase.conf', 'r')
print(type(json.loads(f.read())))
f.close()
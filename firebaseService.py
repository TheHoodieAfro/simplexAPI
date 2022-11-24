import pyrebase
import time, os
import json

f = open('firebase/firebase.conf', 'r')
config = json.loads(f.read())
f.close()

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
db = firebase.database()
bucket = firebase.storage()

ranks_collection = db.child('ranks')

# Authentication
#def register(user):
#
#    try:
#        user = auth.create_user(email=user['email'], display_name=user['username'], password=user['password'])
#        return {'message': 'success'}
#    except Exception as e:
#        return f"An Error Occurred: {e}"
#    
#def login(email):
#
#    try:
#        user = auth.get_user_by_email(email)
#        return user.email
#    except Exception as e:
#        return f"An Error Occurred: {e}"

# Ranks
def getRanks():

    try:
        ranks = dict(db.get().val())
        return ranks
    except Exception as e:
        return f"An Error Occurred: {e}"
    
def getRank(id):

    try:
        rank = ranks_collection.order_by_child('id').equal_to(id).get().val()
        return rank
    except Exception as e:
        return f"An Error Occurred: {e}"


def createRank(rank):

    try:
        id = rank['id']
        ranks_collection.child(id).set(rank)
        return rank
    except Exception as e:
        return f"An Error Occurred: {e}"

# Data
def downloadData(data):

    bucket.child("data/"+ data).download("", "data/"+ data)

    while not os.path.exists('data/'+ data):
        time.sleep(1)
        print('slept')
import pyrebase
import firebase_admin
import time, os
import json

from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate('firebase/key.json')
firebase = firebase_admin.initialize_app(cred)

f = open('firebase/firebase.conf', 'r')
config = json.loads(f.read())
f.close()
pirebase = pyrebase.initialize_app(config)

pauth = pirebase.auth()
db = firestore.client()
bucket = pirebase.storage()

ranks_collection = db.collection('ranks')

# Authentication
def register(user):
    
    username = user.get('username')
    email = user.get('email')
    password = user.get('password')
    if email is None or password is None or username is None:
        return {'message': 'Error missing email, password or username'}
    try:
        user = auth.create_user(
               email=email,
               password=password,
               display_name=username
        )
        return {'message': f'Successfully created user {user.display_name}'}
    except Exception as e:
        return f"An Error Occurred: {e}"
    
def login(user):

    try:
        user = pauth.sign_in_with_email_and_password(user['email'], user['password'])
        return {"token": user['idToken']}
    except Exception as e:
        return f"An Error Occurred: {e}"
    
def verifyToken(authorization):
    
    return auth.verify_id_token(authorization)

# Ranks
def getRanks():

    try:
        ranks = [doc.to_dict() for doc in ranks_collection.stream()]
        return ranks
    except Exception as e:
        return f"An Error Occurred: {e}"
    
def getRank(id):

    try:
        rank = ranks_collection.document(id).get()
        return rank.to_dict()
    except Exception as e:
        return f"An Error Occurred: {e}"


def createRank(rank):

    try:
        id = rank['id']
        ranks_collection.document(id).set(rank)
        return rank
    except Exception as e:
        return f"An Error Occurred: {e}"

# Data
def downloadData(data):

    bucket.child("data/"+ data).download("", "data/"+ data)

    while not os.path.exists('data/'+ data):
        time.sleep(1)
        print('slept')
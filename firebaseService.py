from firebase_admin import credentials, firestore, initialize_app, auth, storage

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred, {
    'storageBucket': 'simplexclassifier.appspot.com'
})

db = firestore.client()
bucket = storage.bucket()

ranks_collection = db.collection('ranks')

# Authentication
def register(user):

    try:
        user = auth.create_user(email=user['email'], display_name=user['username'], password=user['password'])
        return {'message': 'success'}
    except Exception as e:
        return f"An Error Occurred: {e}"

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

    source_blob_name = data

    destination_file_name = "data/"+ data

    bucket = storage.bucket()
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)

db = firestore.client()

ranks_collection = db.collection('ranks')

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
        return {"success": True}
    except Exception as e:
        return f"An Error Occurred: {e}"

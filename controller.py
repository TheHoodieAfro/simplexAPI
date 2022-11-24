import firebaseService, classificationService
import jwt

from functools import wraps
from flask import Flask, request, jsonify

# Application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'POGGERS'

# Authentication
@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify(firebaseService.register(request.form))

@app.route('/api/auth', methods=['POST'])
def login():
    return jsonify(firebaseService.login(request.json))

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = firebaseService.verifyToken(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

# Rankings
@app.route('/api/ranks', methods=['GET'])
def getRankings():
    return jsonify(firebaseService.getRanks())

@app.route('/api/ranks/<id>', methods=['GET'])
def getRank(id):
    return jsonify(firebaseService.getRank(id))

#@app.route('/api/ranks', methods=['POST'])
#def createRank():
#    return jsonify(firebaseService.createRank(request.json))

# Models
@app.route('/api/classificator/simplex', methods=['POST'])
@check_token
def useSimplex():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return firebaseService.createRank(classificationService.executeSimplex(data))

@app.route('/api/classificator/knn', methods=['POST'])
@check_token
def useKNN():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return firebaseService.createRank(classificationService.executeKNN(data))

@app.route('/api/classificator/tree', methods=['POST'])
@check_token
def useTree():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return firebaseService.createRank(classificationService.executeTree(data))

# ???????????????????????
if __name__ == '__main__':
    app.run(debug=True)
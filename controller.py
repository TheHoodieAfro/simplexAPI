import firebaseService, classificationService
import jwt
import datetime


from flask import Flask, request, jsonify, make_response

# Application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'POGGERS'

# Authentication
@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify(firebaseService.register(request.json))

@app.route('/api/auth', methods=['POST'])
def login():
    auth = request.authorization

    if auth:
        check = firebaseService.login(auth.username)
        if auth.username == check:
            token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

            return jsonify({'token': token.decode('UTF-8')})

        return make_response(check, 401)
    
    return make_response('Authentication is needed', 401)

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
def useSimplex():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return firebaseService.createRank(classificationService.executeSimplex(data))

@app.route('/api/classificator/knn', methods=['POST'])
def useKNN():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return firebaseService.createRank(classificationService.executeKNN(data))

@app.route('/api/classificator/tree', methods=['POST'])
def useTree():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return firebaseService.createRank(classificationService.executeTree(data))

# ???????????????????????
if __name__ == '__main__':
    app.run(debug=True)
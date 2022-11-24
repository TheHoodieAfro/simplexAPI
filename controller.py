import firebaseService, classificationService

from flask import Flask, request, jsonify

# Application
app = Flask(__name__)

# Authentication
@app.route('/api/auth', methods=['POST'])
def register():
    return jsonify(firebaseService.register(request.json))

# Rankings
@app.route('/api/ranks', methods=['GET'])
def getRankings():
    return jsonify(firebaseService.getRanks())

@app.route('/api/ranks/<id>', methods=['GET'])
def getRank(id):
    return jsonify(firebaseService.getRank(id))

@app.route('/api/ranks', methods=['POST'])
def createRank():
    return jsonify(firebaseService.createRank(request.json))

# Models
def getData(data):

    firebaseService.downloadData(data)

    response = {'message': 'success'}
    return jsonify(response)

@app.route('/api/classificator/simplex', methods=['POST'])
def useSimplex():
    getData(request.args.get('data'))

    response = {'message': 'success'}
    return jsonify(response)

@app.route('/api/classificator/knn', methods=['GET'])
def useKNN():

    getData(request.args.get('data'))

    response = {'message': 'success'}
    return jsonify(response)

@app.route('/api/classificator/tree', methods=['GET'])
def useTree():

    getData(request.args.get('data'))
    
    response = {'message': 'success'}
    return jsonify(response)

# ???????????????????????
if __name__ == '__main__':
    app.run(debug=True)
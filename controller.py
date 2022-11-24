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
@app.route('/api/classificator/simplex', methods=['POST'])
def useSimplex():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return jsonify(classificationService.executeSimplex(data))

@app.route('/api/classificator/knn', methods=['POST'])
def useKNN():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return jsonify(classificationService.executeKNN(data))

@app.route('/api/classificator/tree', methods=['POST'])
def useTree():

    data = request.args.get('data')
    firebaseService.downloadData(data)

    return jsonify(classificationService.executeTree(data))

# ???????????????????????
if __name__ == '__main__':
    app.run(debug=True)
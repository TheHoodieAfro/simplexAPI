import firebaseService, classificationService
import os

from flask import Flask, request, jsonify

# Application
app = Flask(__name__)

# Authentication
@app.route('/api/auth', methods=['POST'])
def authenticate():
    response = {'message': 'success'}
    return jsonify(response)

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
@app.route('/api/classificator/simplex', methods=['GET'])
def useSimplex():
    response = {'message': 'success'}
    return jsonify(response)

@app.route('/api/classificator/knn', methods=['GET'])
def useKNN():
    response = {'message': 'success'}
    return jsonify(response)

@app.route('/api/classificator/tree', methods=['GET'])
def useTree():
    response = {'message': 'success'}
    return jsonify(response)

# ???????????????????????
if __name__ == '__main__':
    app.run(debug=True)
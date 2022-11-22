import simplexCalsificator

from flask import Flask
from flask import jsonify

# Application
app = Flask(__name__)

# Rankings
app.route('/api/ranks', methods=['GET'])
def getRankings():
    response = {'message': 'success'}
    return jsonify(response)

app.route('/api/ranks/<id>', methods=['GET'])
def getRank(id):
    response = {'message': 'success'}
    return jsonify(response)

# Models
app.route('/api/classificator/simplex', methods=['GET'])
def useSimplex():
    response = {'message': 'success'}
    return jsonify(response)

app.route('/api/classificator/knn', methods=['GET'])
def useKNN():
    response = {'message': 'success'}
    return jsonify(response)

app.route('/api/classificator/tree', methods=['GET'])
def useTree():
    response = {'message': 'success'}
    return jsonify(response)

# ???????????????????????
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from BooleanRetrieval import BooleanRetrieval 
from BiwordRetrieval import BiwordRetrieval 
from RankedRetrieval import RankedRetrieval 
from PositionalRetrieval import PositionalRetrieval 

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Project Developed by Shabnam Zare"

@app.route('/boolean', methods=["POST"])
def booleanEndpoint():
    query = request.json['query']
    BooleanRetrievalInstance = BooleanRetrieval(query)
    BooleanRetrievalInstance.split_query_terms()
    return jsonify(BooleanRetrievalInstance.respond_to_query())

@app.route('/ranked', methods=["POST"])
def rankedEndpoint():
    query = request.json['query'] 
    model = RankedRetrieval(query)
    response = model.respond_to_query()
    arrayToResponse = list(map(lambda x: list(x), list(response.keys())))
    for index, item in enumerate(response.values()):
        arrayToResponse[index].append(item)
    return jsonify(arrayToResponse)

@app.route('/positional', methods=["POST"])
def positionalEndpoint():
    query = request.json['query']
    pos = PositionalRetrieval(query)
    response = pos.respond_to_query()
    return jsonify(response)

@app.route('/biword', methods=["POST"])
def biwordEndpoint():
    query = request.json['query']
    pos = BiwordRetrieval(query)
    return jsonify(pos.respond_to_query())
    

if __name__ == '__main__':
    app.run(
        debug=True
    )
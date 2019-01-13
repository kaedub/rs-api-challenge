from flask import Flask, request, jsonify
from flask_json_schema import JsonSchema
from validation import validate_query_params
from models import User, Location, search_users

app = Flask(__name__)

@app.route('/users')
@validate_query_params
def users():
    results = search_users(request.args)

    return jsonify({
        "metadata": {
            "path": request.path,
            # "query": queries
        },
        "num_results": len(results),
        "results": results
    })
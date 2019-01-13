from flask import Flask, request, jsonify
from models import User, Location, search_users

app = Flask(__name__)

def validate_queries(queries):
    gender = queries.get('gender')
    dist = float(queries.get('dist',0))
    origin = queries.get('origin')
    origin = list(map(lambda e: float(e), origin.split(','))) if origin else None
    min_age = int(queries.get('min_age',0))
    max_age = int(queries.get('max_age',0)) or None
    return {
        "gender": gender,
        "dist": dist,
        "origin": origin,
        "min_age": min_age,
        "max_age": max_age
    }

@app.route('/users')
def users():
    queries = validate_queries(dict(request.args.items()))

    results = search_users(queries)

    return jsonify({
        "metadata": {
            "path": request.path,
            "query": queries
        },
        "num_results": len(results),
        "results": results
    })
from flask import Flask, request, jsonify
from validation import validate_query_params
from models import User, Location, search_users

app = Flask(__name__)



def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)

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
    
    return app
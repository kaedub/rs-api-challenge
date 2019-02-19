from flask import Flask, request, jsonify
from validation import validate_query_params
from models import db, connect_db, User, Location

from werkzeug.exceptions import NotFound

def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rsapi'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SECRET_KEY'] = 'dev'

    connect_db(app)
    db.create_all()


    @app.route('/users')
    @validate_query_params
    def users():
        try:
            query_params = {key:val for key,val in request.args.items() if val}
            results = User.match(request.args)
        except NotFound:
            # return empty array instead of 404 if a not existing page is requested
            results = []

        return jsonify({
                "metadata": {
                    "path": request.path,
                    "query": query_params
                },
                "num_results": len(results),
                "results": [result.json() for result in results]
            }) 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
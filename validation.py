from flask import request
from functools import wraps

def _validate_queries(queries):
    gender = queries.get('gender')
    dist = float(queries.get('dist',0)) or None
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

def validate_query_params(func):
    @wraps(func)
    def validate(*args, **kwargs):
        queries = _validate_queries(dict(request.args.items()))
        request.args = queries
        return func(*args, **kwargs)
    return validate
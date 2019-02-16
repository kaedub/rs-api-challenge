from distance import coord_distance
from flask_sqlalchemy import SQLAlchemy

from csv import DictReader
csv_filename = 'users.csv'

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Represents a user"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    locations = db.relationship('Location', backref='user')

    def __repr__(self):
        return f'<User name={self.name} gender={self.gender} age={self.age}>'

    @classmethod
    def match(cls,queries):
        """Return users that match given age range, gender, or distance from origin"""
        
        page = queries.get('page', 1)
        per_page = queries.get('per_page',10)

        if per_page > 20:
            per_page = 20
        elif per_page < 1:
            per_page = 1

        query = User.query

        if queries.get('min_age', 0):
            query = query.filter(User.age >= queries.get('min_age'))
        if queries.get('max_age'):
            query = query.filter(User.age <= queries.get('max_age'))
        if queries.get('gender'):
            query = query.filter(User.gender == queries.get('gender'))
        
        print('page', page)
        pagination = query.paginate(
            page=page, 
            per_page=per_page)
        
        users = pagination.items
        print('users', len(users))
        # if queries.get('origin') and queries.get('distance'):
            # this is a brute force solution, needs refactor
            # users = [user for user in users if any([coord_distance(queries.get('origin'), [loc.latitude,loc.longitude]) <= queries.get('distance') for loc in user.locations])]
        return users

    def json(self):
        return {
            "type": "user",
            "locationHistory": {
                "type": "FeatureCollection",
                "features": list(map(lambda loc: loc.json(), self.locations))
            },
            "properties": {
                "id": self.id,
                "name": self.name,
                "age": self.age,
                "gender": self.gender
            }
        }

class Location(db.Model):
    """Represents a location"""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False)

    def __repr__(self):
        return f'<Location id={self.id} city={self.city} latitude={self.latitude} longitude={self.longitude}>'

    def json(self):
       return {
            "type": "Feature",
            "properties": {
                "city": self.city
            },
            "geometry": {
                "type": "Point",
                "coordinates": [self.latitude, self.longitude]
            }
        } 

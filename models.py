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
    def match(cls, origin=None, distance=None, gender=None, min_age=0, max_age=None):
        """Return users that match given age range, gender, or distance from origin"""
        query = User.query

        if min_age > 0:
            query = query.filter(User.age >= min_age)
        if max_age:
            query = query.filter(User.age <= max_age)
        if gender:
            query = query.filter(User.gender == gender)
        users = query.all()
        if origin and distance:
            # this is a brute force solution, needs refactor
            users = [user for user in users if any([coord_distance(origin, [loc.latitude,loc.longitude]) <= distance for loc in user.locations])]
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

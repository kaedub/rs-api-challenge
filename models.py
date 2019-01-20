from distance import lat_long_dist
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
    name = db.Column(db.Unicode)
    gender = db.Column(db.String)
    age = db.Column(db.Integer)

    locations = db.relationship('Location', backref='user')

    def __repr__(self):
        return f'<User name={self.name} gender={self.gender} age={self.age}>'


class Location(db.Model):
    """Represents a location"""

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False)



class LocationModel(object):
    def __init__(self, city, lat, long):
        self.city = city
        self.lat = float(lat)
        self.long = float(long)

    def json(self):
        return {
            "type": "Feature",
            "properties": {
                "city": self.city
            },
            "geometry": {
                "type": "Point",
                "coordinates": [self.lat, self.long]
            }
        }

class UserModel(object):
    def __init__(self, user_id, user_name, user_age, user_gender, last_location, lat, long):
        self.user_id = int(user_id)
        self.name = user_name
        self.age = int(user_age)
        self.gender = user_gender
        self.locations = [LocationModel(last_location, lat, long)]
    
    def add_location(self, location):
        self.locations.append(location)

    def matches(self, location, gender, dist, origin, min_age, max_age):
        if dist and origin:
            dist_from_origin = lat_long_dist(origin, (location.lat, location.long))
            if dist_from_origin > dist:
                return False

        if gender:
            if gender != self.gender:
                return False
        if max_age:
            if self.age > max_age:
                return False
        if min_age:
            if self.age < min_age:
                return False

        return True

    def json(self):
        return {
            "type": "user",
            "locationHistory": {
                "type": "FeatureCollection",
                "features": list(map(lambda loc: loc.json(), self.locations))
            },
            "properties": {
                "id": self.user_id,
                "name": self.name,
                "age": self.age,
                "gender": self.gender
            }
        }


def search_users(queries):
    matched = {}
    
    with open(csv_filename) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            user = matched.get(row.get('user_name')) or UserModel(**row)
            location = LocationModel(row.get('last_location'), row.get('lat'), row.get('long'))
            if user.matches(location, **queries):

                if matched.get(user.name):
                    city = row.get('last_location')
                    lat = row.get('lat')
                    long = row.get('long')
                    matched[user.name].add_location(location)
                else:
                    matched[user.name] = user
    return list(map(lambda user: user.json(), matched.values()))
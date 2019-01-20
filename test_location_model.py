"""Unit tests for Location model"""

# run the tests with this command
#
#    python3 -m unittest

import os
import unittest
from models import db, User, Location
from generate import seed_db


from app import create_app

class LocationModelTestCase(unittest.TestCase):
    """Test Location model."""

    def setUp(self):
        """Create test client, add sample data."""
        
        app = create_app()

        db.drop_all()
        db.create_all()

        seed_db()
        
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Drops database tables"""

        db.session.commit()
        db.drop_all()

    def test_create_and_read(self):
        """Test create user"""

        user = User(name='Nicholas Cage', age=49, gender='m')
        
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(name='Nicholas Cage').first()

        location1 = Location(
            city="Los Angeles",
            latitude=34.063566,
            longitude=-118.421092)
        
        location2 = Location(
            city="San Francisco",
            latitude=37.69841,
            longitude=-122.454232)
    
        user.locations.extend([location1, location2])

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(name='Nicholas Cage').first()

        locations = Location.query.all()

        self.assertGreater(len(locations), 2)
        
        location = Location.query.filter_by(city='Los Angeles').first()
        self.assertEqual(location.city, 'Los Angeles')
        self.assertEqual(location.latitude, 34.062264)
        self.assertEqual(location.longitude, -118.340361)

    def test_delete(self):

        location = Location.query.filter_by(user_id=1).first()
        user = User.query.filter_by(id=1).first()

        location = Location(
            city="Los Angeles",
            latitude=34.063566,
            longitude=-118.421092)

        user.locations.append(location)
        num_locations = len(user.locations)

        db.session.add(user)
        db.session.commit()
        
        location.query.delete()
        db.session.commit()

        user = User.query.filter_by(id=1).first()
        self.assertLess(len(user.locations), num_locations)

    def test_cascade_delete(self):
        """Test create user"""

        user = User.query.filter_by(name='Taylor Swift').first()

        location = Location(
            city="San Francisco",
            latitude=37.69841,
            longitude=-122.454232)
        
        user.locations.append(location)
        
        db.session.add(user)
        db.session.commit()
        
        user.query.delete()
        db.session.commit()

        result = User.query.filter_by(name='Taylor Swift').first()

        self.assertIsNone(result)
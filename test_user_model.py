"""Unit tests for User model"""

# run the tests with this command
#
#    python3 -m unittest

import os
import unittest
from models import db, User, Location
from generate import seed_db


from app import create_app

class UserModelTestCase(unittest.TestCase):
    """Test User model."""

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

        user1 = User(name='Nicholas Cage', age=49, gender='m')
        user2 = User(name='James Bond', age=62, gender='m')
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        user1 = User.query.filter_by(name='Nicholas Cage').first()
        user2 = User.query.filter_by(name='James Bond').first()
        
        self.assertEqual(user1.name, 'Nicholas Cage')
        self.assertEqual(user1.age, 49)
        self.assertEqual(user1.gender, 'm')

        self.assertEqual(user2.name, 'James Bond')
        self.assertEqual(user2.age, 62)
        self.assertEqual(user2.gender, 'm')

    def test_update(self):
        """Test create user"""

        user = User(name='Nicholas Cage', age=49, gender='m')
        
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(name='Nicholas Cage').first()

        user.age = 52

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(name='Nicholas Cage').first()

        self.assertEqual(user.age, 52)

    def test_delete(self):
        """Test create user"""

        user = User(name='Nicholas Cage', age=49, gender='m')
        
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(name='Nicholas Cage').first()

        self.assertEqual(user.name, 'Nicholas Cage')
        
        user.query.delete()
        db.session.commit()

        result = User.query.filter_by(name='Nicholas Cage').first()

        self.assertIsNone(result)

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

    def test_match(self):
        """Test match users"""
        
        origin = [39.99112,-76.870215]
        distance = 300
        min_age = 20
        gender = 'm'
        max_age = 50
        users = User.match(
            origin=origin,
            distance=distance,
            # gender=gender,
            # min_age=min_age,
            # max_age=max_age
        )
        
        [print(user) for user in users]
        print(len(users))
        

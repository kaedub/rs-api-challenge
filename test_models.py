"""Model unit tests."""

# run the tests with this command
#
#    python3 -m unittest

import os
from unittest import TestCase
from models import db, User, Location
from generate import seed_db


from app import create_app

class ScheduleModelTestCase(TestCase):
    """Test schedule model."""

    def setUp(self):
        """Create test client, add sample data."""
        
        app = create_app()

        db.drop_all()
        db.create_all()
        
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

        user1 = User.query.first()
        user2 = User.query.get(2)

        self.assertEqual(user1.name, 'Nicholas Cage')
        self.assertEqual(user1.age, 49)
        self.assertEqual(user1.gender, 'm')

        self.assertEqual(user2.name, 'James Bond')
        self.assertEqual(user2.age, 62)
        self.assertEqual(user2.gender, 'm')
    
    def test_delete(self):
        """Test create user"""

        user = User(name='Nicholas Cage', age=49, gender='m')
        
        db.session.add(user)
        db.session.commit()

        user = User.query.first()

        self.assertEqual(user.name, 'Nicholas Cage')
        self.assertEqual(user.age, 49)
        self.assertEqual(user.gender, 'm')
        
        user.query.delete()

        db.session.commit()

        result = User.query.first()


        self.assertIsNone(result)

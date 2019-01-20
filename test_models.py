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
        
        # seed_db('users.csv')

        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Drops database tables"""

        db.session.commit()
        db.drop_all()
    
    def test_read_and_write(self):
        """Test create user"""

        nick = User(name='Nicholas Cage', age=49, gender='m')
        
        db.session.add(nick)
        db.session.commit()

        users = User.query.all()
        print(dir(users[0]))
        [self.assertEqual(user.name, 'hello') for user in users]

        # self.assertEqual(user.name, 'Nicholas Cage')
        # self.assertEqual(user.age, 49)
        # self.assertEqual(user.gender, 'm')
    
    def test_delete(self):
        """Test create user"""

        user = User(name='Nicholas Cage', age=49, gender='m')
        
        db.session.add(user)
        db.session.commit()

        user = User.query.first()

        # self.assertEqual(user.name, 'Nicholas Cage')
        # self.assertEqual(user.age, 49)
        # self.assertEqual(user.gender, 'm')



        
# class FeedingModelTestCase(TestCase):
#     """Test feeding model."""

#     def setUp(self):
#         """Create test client, add sample data."""
        
#         app = create_app()

#         db.drop_all()
#         db.create_all()

#         self.client = app.test_client()

#     def tearDown(self):
#         """Drops database tables"""        

#         db.session.commit()
#         db.drop_all()
    
#     def test_feeding_model(self):
#         """Does basic model work?"""

#         schedule = Schedule.query.all()[0]

#         feedings = [Feeding(schedule_id=schedule.id, order=n) for n in range(1,13)]
#         schedule.feedings = feedings
        
#         db.session.add(schedule)
#         db.session.commit()

#         feedings = [Feeding.query.get_or_404(f.id) for f in feedings]

#         for i, feeding in enumerate(feedings):
#             self.assertEqual(feeding.order, i+1)
#             self.assertEqual(feeding.schedule.id, schedule.id)



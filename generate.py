import sys
from csv import DictReader
from models import db, User, Location


from app import create_app

app = create_app()

csv_filename = 'users.csv'

def seed_db(filename='users.csv'):
    with open(filename) as file:
        reader = DictReader(file)
        for row in reader:
            user_id = row.get('user_id')
            name = row.get('user_name')
            gender = row.get('user_gender')
            age = row.get('user_age')
            city = row.get('last_location')
            latitude = row.get('lat')
            longitude = row.get('long')

            user = User.query.get(user_id) or User(name=name, gender=gender, age=age)

            location = Location(
                city=city,
                latitude=latitude,
                longitude=longitude,
                user_id=user.id)

            user.locations.append(location)

            db.session.add(user)
            db.session.commit()

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    if len(sys.argv) > 1:
        seed_db(sys.argv[1])
    else:
        seed_db(csv_filename)
        db.session.commit()
from models import User,Feedback,db,bcrypt
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Feedback.query.delete()



springboard=User(
    username='Springboard',
    password=00000000,
    email='www.springboard.com',
    first_name='Springboard',
    last_name='Bootcamp')

renish=User(
    username='Mentor',
    password=00000000,
    email='www.renish.com',
    first_name='Renish',
    last_name='B')

meddy=User(
    username='Student Adviser',
    password=00000000,
    email='www.adviser.com',
    first_name='Meddy',
    last_name='Best')

db.session.add(springboard)
db.session.add(renish)
db.session.add(meddy)
db.session.commit()


springboard_feedback=Feedback(
    username='Springboard',
    title='Springboard Software Engineer Bootcamp',
    content='The Best Software Engineer Bootcamp out there!!!')

renish_feedback=Feedback(
    username='Mentor',
    title='Mentorship',
    content='The Best Mentor EVER!!!')

meddy_feedback=Feedback(
    username='Student Adviser',
    title='Student Adviser',
    content='This lady is so Helpful, Thank you very much Meddy!!!')

db.session.add(springboard_feedback)
db.session.add(renish_feedback)
db.session.add(meddy_feedback)
db.session.commit()

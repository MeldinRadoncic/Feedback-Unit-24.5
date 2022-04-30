from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import PrimaryKeyConstraint

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

# Models
# User
class User(db.Model):
    __tablename__='users'
    
    
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(30), unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    # Relationship beetween User and Feedback Model
    feedback = db.relationship("Feedback", backref="user")

    # Registration
    @classmethod
    def registration(cls,username,pwd,email,first_name,last_name):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(username=username,password=hashed_utf8,email=email,first_name=first_name,last_name=last_name)
        db.session.add(user)
        return user

    # Authentication
    @classmethod
    def authenticate(cls,username,pwd):
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password,pwd):
            return u
        else:
            return False

# Feedback Model
class Feedback(db.Model):

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # Foreign Key 
    username = db.Column(db.String(20),
        db.ForeignKey('users.username'),
        nullable=False)







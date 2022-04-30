from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Length,Email


class UserRegisterForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(message='Username cannot be empty!'),Length(min=1,max=30, message='Username is to long! Maximun length 30 characters!')])
    password = PasswordField('Password', validators=[InputRequired(message='Password cannot be empty!'),Length(min=8, message='Password must be 8 characters or longer!')])
    email = StringField('Email',validators=[InputRequired(message='Email cannot be empty!'),Email()])
    first_name = StringField('First Name',validators=[Length(max=30, message='First Name is to long! Maximum length of characthers 30')])
    last_name = StringField('Last Name',validators=[Length(max=30, message='Last Name is to long! Maximum length of characthers of 30')])
# 
# login Form 
class LoginForm(FlaskForm):
        username = StringField('Username',validators=[InputRequired(message='Username cannot be empty!'),Length(min=1,max=30, message='Username is to long! Maximun length 30 characters!')])
        password = PasswordField('Password', validators=[InputRequired(message='Password cannot be empty!'),Length(min=8, message='Password must be 8 characters or longer!')])

# Feedback Form
class FeedbackForm(FlaskForm):
    title = StringField("Title",validators=[InputRequired(message='Please Enter a Title!'), Length(max=100, message='Title cannot be longer then 100 characthers!')])
    content = StringField("Content",validators=[InputRequired(message='Content cannot be empty!')])


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
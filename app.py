from email import feedparser
from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db,User,Feedback
from form import UserRegisterForm,LoginForm,FeedbackForm,DeleteForm
from flask_toastr import Toastr
from sqlalchemy.exc import IntegrityError


from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0258@localhost:5432/feedback_db'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"



connect_db(app)
db.create_all()
toastr = Toastr(app)


toolbar = DebugToolbarExtension(app)

# Home page
@app.route('/')
def home_page():
    feedback = Feedback.query.all()
    return render_template('home_page.html',feedback=feedback)


# Register User
@app.route('/register', methods=["GET","POST"])
def register_user():
    form = UserRegisterForm()
    # Validate form
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.registration(username,password,email,first_name,last_name)
        # Check for duplicate Email
        # if email exist throw error if not then save in DB
        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('Email taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username']= new_user.username
        flash(f'Welcome, {new_user.username}','success')
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html',form=form)


# Login Form
@app.route('/login', methods=["GET","POST"])
def login_user():
    # if User is registered and exist in session log him in automatically
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form=LoginForm()
    # Validate form
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)

        if user:
            flash(f'Welcome back,{user.username}','success')
            session['username']=user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors=['Invalid Username/Password']

    return render_template('login.html',form=form)


    #Logout
@app.route('/logout')
def logout():
    session.pop('username')
    flash(f'We hope to see you soon!','info')
    return redirect('/')


# Show User Info
@app.route('/users/<username>')
def secret_page(username):
    # Protect if user is not logged in
    if "username" not in session or username != session['username']:
        flash("Please login first!",'danger')
        return redirect('/login')

    user = User.query.get(username)
    form = DeleteForm()
    return render_template('secret.html',user=user,form=form)

# Create a Feedback
@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    # Don't allow to delete a feedback if user is not registered and logged in
    if "username" not in session or username != session['username']:
        flash('You don"t have permission to do that!')

    user = User.query.get(username)
    db.session.delete(user)
    try:
            db.session.commit()
    except IntegrityError:
            user.username.errors.append('User cannot be deleted')
    session.pop("username")

    return redirect("/login")

# Add new Feedback
@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    # Have to be logged in to add a feedback
    if "username" not in session or username != session['username']:
        flash('Please login first','danger')

    form = FeedbackForm()
    # Validate form
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title,content=content,username=username)

        db.session.add(feedback)
        db.session.commit()
        flash('Thanks for your feedback!','success')
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback.html", form=form)

# Update Feedback
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):

    feedback = Feedback.query.get(feedback_id)
    # Don't allow users who is not logged in to edit anything 
    if "username" not in session or feedback.username != session['username']:
        flash('Please login first!','danger')

    form = FeedbackForm(obj=feedback)
    # Validate form
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

    return render_template("edit_feedback.html", form=form, feedback=feedback)

# Delete Feedback
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    # Don't allow user who is not loggeed in to delete feedback
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash('You don"t have permission to do that','danger')

    form = DeleteForm()
    # Validate form
    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
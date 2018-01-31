"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension

from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    # if session.get("logged_in_msg"):
    #     flash(session["logged_in_msg"])
    #     session.pop("logged_in_msg", None)

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """ Show list of users """

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/login', methods=["GET"])
def show_login():
    """ login user """

    return render_template("login.html")


@app.route("/process_login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter(User.email == email).one()
    if user.password == password:
        # then login
        session["logged_in_user"] = user.user_id
        flash('You were successfully logged in')
        # session["logged_in_msg"] = "You're logged in"
        return redirect('/')
    else:
        flash("Incorrect email/password login info")
        return redirect('/login')


@app.route("/logout")
def logout():

    session.pop('logged_in_user', None)
    flash("You're logged out")
    redirect ("/")



@app.route("/users/<int:user_id>")
def show_userinfo(user_id):

    user = User.query.get(user_id)
    movies = db.session.query(Movie.title).filter(Rating.user_id == user_id,
             Rating.movie_id == Movie.movie_id).order_by(Movie.title).all()

    return render_template("user_info.html", user=user, movies=movies)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

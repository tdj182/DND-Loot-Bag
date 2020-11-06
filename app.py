from flask import Flask, render_template, redirect, request, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import SearchForm, AddUserForm
from models import db, connect_db, User, Lootbag, Item, LootbagItem
from flask_cors import CORS, cross_origin
import os
app = Flask(__name__)
CORS(app)

CURR_USER_KEY = "curr_user"

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///DND_lootbag'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Show Signup Form or sign up user"""

    form = AddUserForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        return redirect("/")

    return render_template("users/signup.html", form=form)


@app.route("/add-item", methods=['POST'])
def add_item():
    """Add a new item to the database"""
    item_name = request.form.get('name')
    rarity = request.form.get('rarity')
    requires_attunement = request.form.get('requires_attunement')
    slug = request.form.get('slug')
    text = request.form.get('text')
    type = request.form.get('type')

    return f"<h1>{item_name}, {slug}</h1><div>{rarity}, {requires_attunement}</div>{text}, <small>{type}</small>"


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        # Get all ids of users that the logged in user follows

        return render_template('index.html')

    else:
        return render_template('home-anon.html')

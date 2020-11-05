from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask_debugtoolbar import DebugToolbarExtension
from forms import SearchForm
import os
app = Flask(__name__)
CORS(app)


# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///DND_lootbag'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """Show homepage."""
    form = SearchForm()
    return render_template("index.html", form=form)

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

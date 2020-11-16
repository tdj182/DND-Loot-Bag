from flask import Flask, render_template, redirect, request, session, g, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, DataError

from forms import SearchForm, UserForm, LootbagForm, ItemForm, LootbagLoginForm
from models import db, connect_db, User, Lootbag, Item, LootbagItem
from flask_cors import CORS, cross_origin
import os
app = Flask(__name__)
CORS(app)

CURR_USER_KEY = "curr_user"
# Will allow a user to stay logged into one lootbag that is not theirs if they have the password
EXTRA_LOOTBAG_PASSWORD = "extra_password"
EXTRA_LOOTBAG_ID = "extra_loot_id"


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

    if EXTRA_LOOTBAG_PASSWORD not in session:
        add_session_lootbag("", -1)


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


def add_session_lootbag(password, id):
    session[EXTRA_LOOTBAG_PASSWORD] = password
    session[EXTRA_LOOTBAG_ID] = id


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Show Signup Form or sign up user"""

    form = UserForm()
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


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = UserForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "secondary")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """logout of user."""

    do_logout()
    flash(f"See you next time", "secondary")
    return redirect("/")


#################################################################
# Users

@app.route('/confirm-delete')
def confirm_delete():
    """Confirm that the user wants to actually wants to delete"""

    return render_template('users/delete.html')


@app.route('/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    flash(f"{g.user.username} has been deleted", "danger")
    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")

#################################################################
# lootbags


@app.route('/lootbag/<int:lootbag_id>', methods=["GET", "POST"])
def lootbag_show(lootbag_id):
    """Show a lootbag."""

    lootbag = Lootbag.query.get_or_404(lootbag_id)
    form = ItemForm()
    if g.user.id == lootbag.owner_id or lootbag.password == session[EXTRA_LOOTBAG_PASSWORD] and lootbag.id == session[EXTRA_LOOTBAG_ID]:
        return render_template('lootbags/show.html', lootbag=lootbag, form=form)
    elif not lootbag.is_shareable:
        import pdb
        pdb.set_trace()
        flash("Access unauthorized.", "danger")
        return redirect("/")

    login_form = LootbagLoginForm()

    if login_form.validate_on_submit():
        if login_form.password.data == lootbag.password:
            add_session_lootbag(login_form.password.data, lootbag.id)
            return render_template('lootbags/show.html', lootbag=lootbag, form=form)

        flash("Access unauthorized.", "danger")
        return redirect('/')

    return render_template('lootbags/login_lootbag.html', lootbag=lootbag, form=login_form)


@app.route('/lootbag/<int:lootbag_id>/edit', methods=["GET", "POST"])
def lootbag_edit(lootbag_id):
    """Edit a lootbag."""

    lootbag = Lootbag.query.get_or_404(lootbag_id)
    form = LootbagForm(obj=lootbag)
    if g.user.id != lootbag.owner_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        lootbag.name = form.name.data
        lootbag.password = form.password.data
        lootbag.is_shareable = form.is_shareable.data
        db.session.commit()
        return redirect('/')

    return render_template('lootbags/edit.html', lootbag=lootbag, form=form)


@app.route('/lootbag/<int:lootbag_id>/convert', methods=["POST"])
def lootbag_convert(lootbag_id):
    """Convert currency in lootbag."""

    lootbag = Lootbag.query.get(lootbag_id)
    platinum = int(request.form.get('platinum'))
    gold = int(request.form.get('gold'))
    electrum = int(request.form.get('electrum'))
    silver = int(request.form.get('silver'))
    copper = int(request.form.get('copper'))

    lootbag.platinum = lootbag.platinum + platinum
    lootbag.gold = lootbag.gold + gold
    lootbag.electrum = lootbag.electrum + electrum
    lootbag.silver = lootbag.silver + silver
    lootbag.copper = lootbag.copper + copper

    db.session.add(lootbag)
    db.session.commit()
    return ('', 204)


@app.route('/add-lootbag', methods=['POST'])
def add_lootbag():

    if not g.user:
        flash("Access unauthorized.", "danger")

    form = LootbagForm()

    if form.validate_on_submit():
        new_bag = Lootbag(name=form.name.data, password=form.password.data)
        g.user.lootbags.append(new_bag)
        db.session.commit()

    return redirect('/')


@app.route("/lootbag/<int:lootbag_id>/delete", methods=["POST"])
def lootbag_delete(lootbag_id):
    """Delete lootbag."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    bag = Lootbag.query.get_or_404(lootbag_id)
    db.session.delete(bag)
    db.session.commit()

    return redirect("/")


#################################################################
#  items


@app.route("/lootbag/<int:lootbag_id>/add-item", methods=['POST'])
def add_item(lootbag_id):
    """Add a new item to the database"""

    lootbag = Lootbag.query.get_or_404(lootbag_id)
    item_name = request.form.get('item_name')
    rarity = request.form.get('rarity')
    requires_attunement = request.form.get('requires_attunement')
    slug = request.form.get('slug')
    text = request.form.get('text')
    type = request.form.get('type')
    quantity = request.form.get('quantity')

    if requires_attunement == 'requires attunement':
        requires_attunement = True
    else:
        requires_attunement = False

    new_item = Item(
        item_name=item_name,
        rarity=rarity,
        text=text,
        requires_attunement=requires_attunement,
        slug=slug,
        type=type,
        quantity=quantity
    )
    db.session.add(new_item)
    db.session.commit()

    new_lootbag_item = LootbagItem(
        lootbag_id=lootbag_id,
        item_id=new_item.id
    )
    db.session.add(new_lootbag_item)
    db.session.commit()

    return ('', 204)


@app.route('/item/<int:item_id>/edit', methods=["GET", "POST"])
def item_edit(item_id):
    """Edit a lootbag."""

    item = Item.query.get_or_404(item_id)
    lootbag = Lootbag.query.get_or_404(item.lootbag[0].id)

    form = ItemForm(obj=item)
    if g.user.id == lootbag.owner_id:
        pass
    elif lootbag.password != session[EXTRA_LOOTBAG_PASSWORD] or lootbag.id != session[EXTRA_LOOTBAG_ID]:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if form.validate_on_submit():
        if form.requires_attunement.data == True:
            item.requires_attunement = True
        else:
            item.requires_attunement = False

        item.item_name = form.item_name.data,
        item.rarity = form.rarity.data,
        item.text = form.text.data,
        item.type = form.type.data,
        item.quantity = form.quantity.data

        db.session.commit()
        return redirect(f'/lootbag/{lootbag.id}')

    return render_template('/items/edit.html', item=item, form=form)


@app.route("/item/<int:item_id>/delete", methods=["POST"])
def item_delete(item_id):
    """Delete item."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    item = Item.query.get_or_404(item_id)
    lootbag = item.lootbag[0]

    db.session.delete(item)
    db.session.commit()

    return redirect(f'/lootbag/{lootbag.id}')


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        # Get all ids of users that the logged in user follows
        lootbags = (Lootbag
                    .query
                    .filter(Lootbag.owner_id == g.user.id).all())
        form = LootbagForm()
        return render_template('home.html', lootbags=lootbags, form=form)

    else:
        return render_template('home-anon.html')
